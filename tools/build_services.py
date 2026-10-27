# Χτίζει τις σελίδες υπηρεσιών (μία ανά κατηγορία + μία ανά υποκατηγορία) από τα
# δεδομένα παρακάτω, με header/footer από το space.html. Ενημερώνει και το μενού
# «Υπηρεσίες» σε όλες τις σελίδες. Τρέξιμο: python tools/build_services.py
# Νέο κείμενο από την πελάτισσα = συμπλήρωσε το CONTENT[slug] και ξανατρέξε.
import io, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
E = html.escape

# (slug, τίτλος, εικονίδιο αρχικής, [(slug, υποκατηγορία)] ή ομάδες)
CATS = [
 ("geniki", "Γενική Οδοντιατρική", "serv-geniki.jpg", [
   ("exetasi-diagnosi", "Οδοντιατρική εξέταση και διάγνωση"),
   ("katharismos", "Καθαρισμός"),
   ("emfraxeis", "Εμφράξεις (σφραγίσματα)"),
   ("epentheta", "Επένθετα - Ολικό χτίσιμο δοντιών"),
   ("schedio-therapeias", "Σχέδιο θεραπείας")]),
 ("aisthitiki", "Αισθητική Οδοντιατρική", "serv-aisthitiki.jpg", [
   ("leukansi", "Λεύκανση"),
   ("emfraxeis-ritinis", "Εμφράξεις ρητίνης (λευκά σφραγίσματα)"),
   ("opseis-ritinis", "Όψεις ρητίνης"),
   ("opseis-porselanis", "Όψεις πορσελάνης"),
   ("olokeramikes-thikes", "Ολοκεραμικές θήκες"),
   ("odontiko-stras", "Οδοντικό στρας")]),
 ("fastbraces", "Ορθοδοντική Fastbraces®", "serv-fastbraces.jpg", [
   ("turbo", "Fastbraces turbo / turbo extra"),
   ("diafani", "Fastbraces διαφανή")]),
 ("periodontologia", "Περιοδοντολογία", "serv-periodontologia.jpg", [
   ("oulitida", "Θεραπεία ουλίτιδας"),
   ("periodontitida", "Θεραπεία περιοδοντίτιδας"),
   ("periodontitida-laser", "Θεραπεία περιοδοντίτιδας με υποβοήθηση Laser"),
   ("periemfyteumatitida-laser", "Θεραπεία περιεμφυτευματίτιδας με υποβοήθηση Laser"),
   ("syntirisi", "Περιοδοντική συντήρηση")]),
 ("emfyteumatologia", "Εμφυτευματολογία", "serv-emfyteumatologia.jpg", [
   ("emfyteumata", "Τοποθέτηση οδοντικών εμφυτευμάτων"),
   ("ostika-mosxeumata", "Οστικά μοσχεύματα")]),
 ("paidodontia", "Παιδοδοντία", "serv-paidodontia.jpg", [
   ("proti-episkepsi", "Πρώτη οδοντιατρική επίσκεψη παιδιού"),
   ("emfraxeis-neogilon", "Εμφράξεις νεογιλών δοντιών"),
   ("fthoriosi", "Προληπτική Φθορίωση"),
   ("sealants", "Προληπτικές καλύψεις οπών και σχισμών (sealants)"),
   ("polfotomi", "Πολφοτομή νεογιλών"),
   ("diatirisi-xorou", "Διατήρηση χώρου μετά από πρόωρη απώλεια νεογιλών δοντιών"),
   ("symvouleftiki-goneon", "Συμβουλευτική γονέων για τη στοματική υγεία")]),
 ("endodontia", "Ενδοδοντία", "serv-endodontia.jpg", []),
 ("prosthetiki", "Προσθετική (κινητή, ακίνητη, επί εμφυτευμάτων)", "serv-prosthetiki.jpg", [
   ("Κινητή", [
     ("olikes", "Ολικές οδοντοστοιχίες"),
     ("merikes", "Μερικές οδοντοστοιχίες"),
     ("ameses", "Άμεσες οδοντοστοιχίες"),
     ("odontostoixies-emfyteumata", "Οδοντοστοιχίες επί εμφυτευμάτων")]),
   ("Ακίνητη", [
     ("stefanes", "Στεφάνες δοντιών (θήκες) (ολοκεραμικές, μεταλλοκεραμικές)"),
     ("stefanes-gefyres-emfyteumata", "Στεφάνες, γέφυρες και οδοντοστοιχίες επί εμφυτευμάτων"),
     ("gefyres", "Γέφυρες δοντιών"),
     ("entheta-epentheta", "Ένθετα και επένθετα (Inlays – Onlays – Overlays)")]),
   ("Επί εμφυτευμάτων", [
     ("stefanes-epi-emfyteumaton", "Στεφάνες επί εμφυτευμάτων"),
     ("gefyres-epi-emfyteumaton", "Γέφυρες επί εμφυτευμάτων"),
     ("odontostoixies-epi-emfyteumaton", "Οδοντοστοιχίες επί εμφυτευμάτων"),
     ("akinites-olikes", "Ακίνητες ολικές αποκαταστάσεις επί εμφυτευμάτων")])]),
 ("xeirourgiki", "Χειρουργική στόματος", "serv-xeirourgiki.jpg", [
   ("topothetisi-emfyteumaton", "Τοποθέτηση εμφυτευμάτων"),
   ("fronimites", "Εξαγωγές φρονιμιτών"),
   ("periodontiki-xeirourgiki", "Περιοδοντική Χειρουργική"),
   ("loipes", "Λοιπές χειρουργικές επεμβάσεις")]),
 ("narthikes", "Κατασκευή ναρθήκων", "serv-narthikes.jpg", [
   ("vrygmou", "Νάρθηκες βρυγμού (τριξίματος δοντιών)"),
   ("leukansis", "Νάρθηκες λεύκανσης"),
   ("retainers", "Συγκρατητικοί ορθοδοντικοί νάρθηκες (Retainers)"),
   ("athlitikoi", "Αθλητικοί προστατευτικοί νάρθηκες")]),
 ("aktinodiagnostiki", "Ψηφιακή ακτινοδιαγνωστική", None, []),
 ("laser", "Λέιζερ (Laser)", "serv-laser.jpg", [
   ("xeirourgeia", "Χειρουργεία (Ουλεκτομή - Ουλοπλαστική, Χαλινεκτομή, Αφαίρεση μορφωμάτων μαλακών ιστών κά)"),
   ("kgd", "Θεραπεία ΚΓΔ"),
   ("afthes", "Αντιμετώπιση άφθας"),
   ("pbm", "Φωτοβιοδιέγερση (PBM)"),
   ("periodontiki", "Περιοδοντική τοπική εφαρμογή laser"),
   ("periemfyteumatiki", "Περιεμφυτευματική τοπική εφαρμογή laser"),
   ("apeuaisthitopoiisi", "Απευαισθητοποίηση"),
   ("xrostikes-oulon", "Αφαίρεση χρωστικών από τα ούλα"),
   ("endodontias", "Ενδοδοντίας")]),
]

EPILOGUE = ("DrSmile- πολυοδοντιατρείο", "Παρχαρίδου Αναστασία και συνεργάτες",
            "Δημιουργούμε χαμόγελα όπως ακριβώς σας αξίζει!")

# Κείμενα όπως τα έστειλε η πελάτισσα (email 26/10/2026). Κλειδί = slug σελίδας.
CONTENT = {
 "geniki-exetasi-diagnosi": dict(
  lead="Η σωστή διάγνωση είναι το πρώτο βήμα για ένα υγιές χαμόγελο.",
  intro=["Στο DrSmile- πολυοδοντιατρείο- Παρχαρίδου Αναστασία και συνεργάτες, στον Εύοσμο Θεσσαλονίκης, δίνουμε ιδιαίτερη σημασία στην πρόληψη και στην έγκαιρη διάγνωση, ακόμη και όταν δεν υπάρχουν εμφανή συμπτώματα.",
         "Με σύγχρονα διαγνωστικά μέσα, εντοπίζονται έγκαιρα τα προβλήματα και σχεδιάζεται η πιο κατάλληλη θεραπεία, εξατομικευμένα για εσάς."],
  hero_photo="Χαμογελαστή φωτογραφία (από το email)",
  feat_title="Τι περιλαμβάνει η οδοντιατρική εξέταση;",
  feats=[("ti-zoom-check","Αναλυτικός έλεγχος","Εξέταση σε δόντια, ούλα, βλεννογόνους, γλώσσα, κροταφογναθική διάρθρωση, σύγκλειση για εντοπισμό προβλημάτων."),
         ("ti-photo-scan","Ψηφιακές ακτινογραφίες και ενδοστοματικές φωτογραφίες","Όταν ενδείκνυνται, για πληρέστερη διάγνωση και καλύτερη κατανόηση των ευρημάτων."),
         ("ti-clipboard-list","Πλάνο θεραπείας","Με βάση τα ευρήματα σχεδιάζουμε μαζί το κατάλληλο πλάνο πρόληψης ή θεραπείας για εσάς.")],
  blocks=[dict(title="Ενημέρωση και εξατομικευμένο σχέδιο θεραπείας", photo="Ακτινογραφία (κάθετη ή οριζόντια, από το email)",
               ps=["Στο DrSmile πιστεύουμε ότι κάθε ασθενής πρέπει να γνωρίζει και να κατανοεί την κατάσταση της στοματικής του υγείας.",
                   "Μετά την ολοκλήρωση της εξέτασης, γίνεται αναλυτική ενημέρωση για τα ευρήματα και, εφόσον απαιτείται θεραπεία, συζητούνται οι διαθέσιμες επιλογές.",
                   "Στόχος είναι να διαμορφωθεί από κοινού ένα εξατομικευμένο σχέδιο θεραπείας, λαμβάνοντας υπόψη τις κλινικές ανάγκες, τις προσωπικές προτεραιότητες, τον απαιτούμενο χρόνο και το οικονομικό κόστος."])],
  why_title="Γιατί είναι σημαντική", why_lead="Η τακτική οδοντιατρική εξέταση βοηθά:",
  why=["στην έγκαιρη ανίχνευση τερηδόνας και/ή περιοδοντικών προβλημάτων","στην πρόληψη πιο σοβαρών και δαπανηρών θεραπειών",
       "στη διατήρηση της στοματικής υγείας σε βάθος χρόνου","στην εξατομικευμένη φροντίδα ανάλογα με τις ανάγκες σας","σε ένα όμορφο, υγιές και λειτουργικό χαμόγελο"],
  freq=dict(title="Πόσο συχνά χρειάζεται να γίνεται;", photo="Ημερολόγιο (από το email)",
            ps=["Η προληπτική οδοντιατρική εξέταση συνιστάται συνήθως κάθε έξι μήνες, <strong>ακόμα κι αν δεν υπάρχει κάποιο σύμπτωμα</strong>.",
                "Μην περιμένετε να εμφανιστεί πόνος για να επισκεφθείτε τον οδοντίατρο. Η πρόληψη και η έγκαιρη διάγνωση μπορούν να συμβάλουν στην αποφυγή πιο σύνθετων θεραπειών στο μέλλον."]),
  extra=None,
  closing="DrSmile – Φροντίζουμε το χαμόγελό σας, ξεκινώντας από τη σωστή διάγνωση."),
 "geniki-katharismos": dict(
  lead="Ένα υγιές και λαμπερό χαμόγελο ξεκινά από την πρόληψη!",
  intro=["Στο DrSmile- πολυοδοντιατρείο- Παρχαρίδου Αναστασία και συνεργάτες, στον Εύοσμο Θεσσαλονίκης, πιστεύουμε ότι ο επαγγελματικός καθαρισμός δοντιών αποτελεί μία από τις σημαντικότερες προληπτικές οδοντιατρικές πράξεις για τη διατήρηση της στοματικής υγείας."],
  hero_photo="Φωτογραφία με χαμόγελο (από το email)",
  feat_title="Τι περιλαμβάνει ο επαγγελματικός καθαρισμός δοντιών;",
  feats=[("ti-dental","Απομάκρυνση πέτρας και μικροβιακής πλάκας","Με τη χρήση σύγχρονων συσκευών υπερήχων και ειδικών εργαλείων απομακρύνονται οι εναποθέσεις πέτρας και μικροβιακής πλάκας από τις επιφάνειες των δοντιών από το ύψος των ούλων και άνω."),
         ("ti-sparkles","Στίλβωση και απομάκρυνση χρωστικών","Με ειδικές μεθόδους στίλβωσης απομακρύνονται οι επιφανειακές χρωστικές που προκαλούνται, μεταξύ άλλων, από τον καφέ, το τσάι και το κάπνισμα. Έτσι, οι επιφάνειες των δοντιών γίνονται πιο λείες και αναδεικνύεται η φυσική τους λάμψη."),
         ("ti-brush","Οδηγίες στοματικής υγιεινής","Παρέχονται εξατομικευμένες οδηγίες για το σωστό βούρτσισμα, τη χρήση οδοντικού νήματος και μεσοδόντιων μέσων καθαρισμού, ανάλογα με τις ανάγκες της στοματικής υγείας κάθε ασθενούς.")],
  blocks=[],
  why_title="Γιατί είναι σημαντικός ο καθαρισμός δοντιών;", why_lead="Με τον τακτικό επαγγελματικό καθαρισμό:",
  why=["Μειώνεται ο κίνδυνος εμφάνισης ουλίτιδας και περιοδοντικών παθήσεων.","Απομακρύνεται η πέτρα που δεν μπορεί να αφαιρεθεί με το καθημερινό βούρτσισμα.",
       "Περιορίζεται η κακοσμία του στόματος που σχετίζεται με τη συσσώρευση μικροβιακής πλάκας.","Απομακρύνονται οι επιφανειακές χρωστικές και βελτιώνεται η εμφάνιση των δοντιών.",
       "Ενισχύεται η μακροχρόνια διατήρηση της υγείας των δοντιών και των ούλων."],
  freq=dict(title="Πόσο συχνά χρειάζεται να γίνεται;", photo=None,
            ps=["Ο επαγγελματικός καθαρισμός δοντιών συνιστάται συχνά κάθε έξι μήνες, ωστόσο η ιδανική συχνότητα καθορίζεται εξατομικευμένα, ανάλογα με τις ανάγκες κάθε ασθενούς.",
                "Σε περιπτώσεις αυξημένης συσσώρευσης πέτρας, ουλίτιδας, ιστορικού περιοδοντίτιδας ή άλλων παραγόντων κινδύνου, ενδέχεται να απαιτείται συχνότερη παρακολούθηση και φροντίδα."]),
  extra=dict(title="Ο καθαρισμός δοντιών είναι και λεύκανση;", photo="Καθαρισμός και λεύκανση (από το email)",
             ps=["Με τον καθαρισμό δοντιών απομακρύνονται η πέτρα, η μικροβιακή πλάκα και οι επιφανειακές χρωστικές, ώστε να αναδεικνύεται η φυσική καθαρότητα και λάμψη των δοντιών.",
                 "Αντίθετα, με τη λεύκανση δοντιών επιτυγχάνεται η αλλαγή της φυσικής τους απόχρωσης προς έναν πιο ανοιχτό τόνο, προσφέροντας ένα πιο λευκό χαμόγελο.",
                 "Με απλά λόγια, <strong>ο καθαρισμός στοχεύει κυρίως στη στοματική υγεία, ενώ η λεύκανση στην αισθητική βελτίωση του χρώματος των δοντιών!</strong>"]),
  closing=None),
}

CSS = """
.crumbs{font-size:12.5px;color:var(--muted);padding-top:26px;display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.crumbs a{color:var(--gold-deep)}
.page-hero .lead-q{font-family:var(--fs);font-style:italic;font-size:clamp(22px,2.6vw,30px);color:var(--gold-deep);max-width:760px;margin:22px auto 0;line-height:1.35}
.svc-intro{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.svc-intro p{font-size:16.5px;line-height:1.85;color:var(--charcoal-2);margin-bottom:14px}
.ph{border:1.5px dashed var(--gold-soft);background:rgba(233,217,184,.18);border-radius:220px 220px 20px 20px;min-height:340px;display:grid;place-items:center;text-align:center;padding:24px;color:var(--gold-deep);font-size:13px;font-weight:600;letter-spacing:.04em}
.ph i{display:block;font-size:30px;margin:0 auto 10px}
.ph.wide{border-radius:20px;min-height:260px}
.svc-h2{font-family:var(--fs);font-weight:400;font-size:clamp(26px,3.2vw,40px);line-height:1.15;text-align:center;margin-bottom:34px}
.feats{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.feat{background:var(--warm-white);border:1px solid var(--line);border-radius:160px 160px 20px 20px;padding:44px 26px 30px;text-align:center}
.feat .fi{width:74px;height:74px;border-radius:50%;margin:0 auto 20px;display:grid;place-items:center;font-size:32px;color:var(--gold-deep);background:var(--ivory);box-shadow:inset 0 0 0 1px var(--line)}
.feat h3{font-size:14px;font-weight:700;letter-spacing:.03em;text-transform:uppercase;line-height:1.45;margin-bottom:12px}
.feat p{font-size:14.5px;line-height:1.75;color:var(--muted)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.split.rev>.ph{order:2}
.split h2{font-family:var(--fs);font-weight:400;font-size:clamp(26px,3vw,38px);line-height:1.15;margin-bottom:18px}
.split p{font-size:15.5px;line-height:1.85;color:var(--charcoal-2);margin-bottom:12px}
.whybox{background:var(--pearl);border-radius:24px;padding:44px;max-width:900px;margin:0 auto}
.whybox h2{font-family:var(--fs);font-weight:400;font-size:clamp(26px,3vw,38px);margin-bottom:10px}
.whybox .wl{color:var(--muted);margin-bottom:18px}
.whybox ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.whybox li{display:flex;gap:12px;font-size:15.5px;line-height:1.6}
.whybox li i{color:var(--gold-deep);font-size:20px;flex:none;margin-top:1px}
.epi{text-align:center;padding:10px 0 0}
.epi .cl{font-family:var(--fs);font-style:italic;font-size:clamp(20px,2.4vw,28px);color:var(--charcoal-2);margin-bottom:26px}
.epi .b1{font-family:var(--fs);font-size:24px;color:var(--charcoal)}
.epi .b2{font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-top:4px}
.epi .b3{font-family:var(--fs);font-style:italic;font-size:22px;color:var(--gold-deep);margin-top:10px}
.pending{max-width:760px;margin:0 auto;text-align:center;border:1.5px dashed var(--gold-soft);border-radius:20px;padding:36px;color:var(--muted)}
.subgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.subcard{display:flex;align-items:center;justify-content:space-between;gap:14px;background:var(--warm-white);border:1px solid var(--line);border-radius:20px;padding:22px 24px;font-weight:600;font-size:15px;line-height:1.45;transition:.3s}
.subcard i{color:var(--gold-deep);font-size:18px;flex:none;transition:.3s}
.subcard:hover{border-color:var(--gold);transform:translateY(-3px);box-shadow:0 20px 40px -30px rgba(60,44,12,.5)}
.subcard:hover i{transform:translateX(4px)}
.subgroup{margin-top:34px}
.subgroup:first-child{margin-top:0}
.subgroup h3{font-family:var(--fs);font-size:26px;font-weight:400;margin-bottom:16px;color:var(--gold-deep)}
.cat-ic{width:96px;height:96px;border-radius:50%;object-fit:cover;margin:0 auto 18px;display:block}
@media(max-width:920px){.svc-intro,.split{grid-template-columns:1fr;gap:28px}.split.rev>.ph{order:0}.feats{grid-template-columns:1fr}.subgrid{grid-template-columns:1fr 1fr}.ph{min-height:280px}}
@media(max-width:560px){.subgrid{grid-template-columns:1fr}.whybox{padding:28px 22px}.feat{border-radius:120px 120px 18px 18px}}
"""

def cat_url(c): return "yp-%s.html" % c[0]
def sub_url(c, s): return "yp-%s-%s.html" % (c[0], s)
def subs_flat(c):
    out = []
    for x in c[3]:
        if isinstance(x[1], list): out += x[1]
        else: out.append(x)
    return out

base = io.open("space.html", encoding="utf-8").read()
head_end = base.index('<header class="wrap page-hero">')
tail_start = base.index('<div class="fab-stack">')
HEAD = base[:head_end].replace('</style>', CSS + '</style>', 1)
HEAD = re.sub(r'<div class="draft">.*?</div>\n', '', HEAD, count=1)
HEAD = HEAD.replace(' class="here"', '')
TAIL = base[tail_start:]

def page(fname, title, desc, body):
    h = re.sub(r'<title>.*?</title>', '<title>%s | DrSmile Πολυοδοντιατρείο, Εύοσμος Θεσσαλονίκης</title>' % E(title), HEAD)
    h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % E(desc), h)
    io.open(fname, "w", encoding="utf-8", newline="").write(h + body + TAIL)

def ph(label, wide=False):
    return '<div class="ph%s"><div><i class="ti ti-photo"></i>%s</div></div>' % (" wide" if wide else "", E(label))

def crumbs(*items):
    parts = ['<a href="index-v10.html">Αρχική</a>', '<a href="index-v10.html#services">Υπηρεσίες</a>']
    for t, u in items:
        parts.append('<a href="%s">%s</a>' % (u, E(t)) if u else '<span>%s</span>' % E(t))
    return '<nav class="wrap crumbs">' + ' <span>/</span> '.join(parts) + '</nav>\n'

CTA = """<section class="ctaband">
  <div class="wrap">
    <h2>Κλείστε το <em>ραντεβού σας.</em></h2>
    <p>Καλέστε μας ή στείλτε μας μήνυμα και θα σας απαντήσουμε το συντομότερο.</p>
    <a class="btn" href="tel:2310769674"><i class="ti ti-phone"></i> 2310 769 674</a>
  </div>
</section>

"""

def epilogue(closing):
    s = '<section class="sec"><div class="wrap epi">'
    if closing: s += '<p class="cl">%s</p>' % E(closing)
    s += '<div class="b1">%s</div><div class="b2">%s</div><div class="b3">%s</div>' % tuple(E(x) for x in EPILOGUE)
    return s + '</div></section>\n'

def content_body(d):
    s = '<section class="sec"><div class="wrap svc-intro"><div>%s</div>%s</div></section>\n' % (
        ''.join('<p>%s</p>' % E(p) for p in d["intro"]), ph(d["hero_photo"]))
    s += '<section class="sec"><div class="wrap"><h2 class="svc-h2">%s</h2><div class="feats">%s</div></div></section>\n' % (
        E(d["feat_title"]), ''.join('<div class="feat"><div class="fi"><i class="ti %s"></i></div><h3>%s</h3><p>%s</p></div>' % (i, E(t), E(p)) for i, t, p in d["feats"]))
    def split(b, rev):
        pic = ph(b["photo"]) if b.get("photo") else ''
        cls = "split rev" if rev and pic else "split" if pic else ""
        inner = '<div><h2>%s</h2>%s</div>' % (E(b["title"]), ''.join('<p>%s</p>' % p for p in b["ps"]))
        if not pic: return '<section class="sec"><div class="wrap" style="max-width:900px">%s</div></section>\n' % inner
        return '<section class="sec"><div class="wrap %s">%s%s</div></section>\n' % (cls, pic, inner)
    for b in d["blocks"]: s += split(dict(b, ps=[E(p) for p in b["ps"]]), False)
    s += '<section class="sec"><div class="wrap"><div class="whybox"><h2>%s</h2><p class="wl">%s</p><ul>%s</ul></div></div></section>\n' % (
        E(d["why_title"]), E(d["why_lead"]), ''.join('<li><i class="ti ti-circle-check"></i><span>%s</span></li>' % E(w) for w in d["why"]))
    s += split(d["freq"], True)
    if d.get("extra"): s += split(d["extra"], False)
    return s + epilogue(d.get("closing"))

PENDING = '<section class="sec"><div class="wrap"><div class="pending"><i class="ti ti-pencil" style="font-size:26px;color:var(--gold-deep)"></i><p style="margin-top:10px">Το κείμενο αυτής της σελίδας έρχεται σύντομα από το DrSmile.</p></div></div></section>\n'

count = 0
for c in CATS:
    slug, name, icon, groups = c
    flat = subs_flat(c)
    # σελίδα κατηγορίας
    body = crumbs((name, None))
    ic = '<img class="cat-ic" src="assets/icons/%s" alt="">' % icon if icon else ''
    body += '<header class="wrap page-hero">%s<span class="label">Υπηρεσίες</span><h1>%s</h1></header>\n' % (ic, E(name))
    if flat:
        if isinstance(groups[0][1], list):
            g = ''.join('<div class="subgroup"><h3>%s</h3><div class="subgrid">%s</div></div>' % (E(gt), ''.join(
                '<a class="subcard" href="%s"><span>%s</span><i class="ti ti-arrow-right"></i></a>' % (sub_url(c, s), E(t)) for s, t in gl)) for gt, gl in groups)
        else:
            g = '<div class="subgrid">%s</div>' % ''.join('<a class="subcard" href="%s"><span>%s</span><i class="ti ti-arrow-right"></i></a>' % (sub_url(c, s), E(t)) for s, t in flat)
        body += '<section class="sec"><div class="wrap">%s</div></section>\n' % g
    else:
        d = CONTENT.get(slug)
        body += content_body(d) if d else PENDING
    page(cat_url(c), name, "%s στο DrSmile Πολυοδοντιατρείο, Εύοσμος Θεσσαλονίκης." % name, body + CTA)
    count += 1
    for s, t in flat:
        key = "%s-%s" % (slug, s)
        d = CONTENT.get(key)
        body = crumbs((name, cat_url(c)), (t, None))
        body += '<header class="wrap page-hero"><span class="label">%s</span><h1>%s</h1>%s</header>\n' % (
            E(name), E(t), '<p class="lead-q">%s</p>' % E(d["lead"]) if d else '')
        body += content_body(d) if d else PENDING
        page(sub_url(c, s), t, (d["lead"] if d else "%s στο DrSmile Πολυοδοντιατρείο, Εύοσμος Θεσσαλονίκης." % t), body + CTA)
        count += 1

# μενού «Υπηρεσίες»: κάθε κατηγορία δείχνει στη σελίδα της
def fix_menu(f):
    t = io.open(f, encoding="utf-8").read()
    for c in CATS:
        name = c[1]
        t = re.sub(r'<a href="[^"]*">%s</a>' % re.escape(name), '<a href="%s">%s</a>' % (cat_url(c), name), t)
    io.open(f, "w", encoding="utf-8", newline="").write(t)

pages = ["index-v10.html", "team.html", "space.html", "faq.html"] + [f for f in os.listdir(".") if f.startswith("yp-")]
for f in pages: fix_menu(f)
print("σελίδες υπηρεσιών:", count, "· με κείμενο:", len(CONTENT))

# ---- μενού «Υπηρεσίες» με υποκατηγορίες (desktop: flyout δεξιά, κινητό: ανάπτυξη ανά κατηγορία)
MENU_CSS = """<style id="svc-menu-css">
.nav-sub .nsi{position:relative}
.nav-sub .nsi>a{display:flex;justify-content:space-between;align-items:center;gap:14px}
.nav-sub .nsi>a i{font-size:13px;color:var(--gold-deep)}
.nav-fly{position:absolute;left:100%;top:-12px;margin-left:6px;width:330px;padding:12px 0;background:var(--warm-white);border:1px solid var(--line);border-radius:14px;box-shadow:0 26px 54px -28px rgba(120,96,50,.4);opacity:0;visibility:hidden;transform:translateX(-6px);transition:.22s}
.nav-fly::before{content:"";position:absolute;top:0;bottom:0;left:-10px;width:10px}
.nav-fly .fh{display:block;padding:4px 22px 6px;font-size:10.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep)}
.nav-fly a{white-space:normal!important;line-height:1.4}
.nav-sub .nsi:hover>.nav-fly,.nav-sub .nsi:focus-within>.nav-fly{opacity:1;visibility:visible;transform:none}
@media(max-width:1180px){.nav-fly{left:auto;right:100%;margin:0 6px 0 0;width:290px}.nav-fly::before{left:auto;right:-10px}}
.mnav-group.svc.open .mnav-sub{max-height:6000px}
.mnav-cat{display:flex;flex-direction:column;align-items:center}
.mnav-cat .mc-row{display:flex;align-items:center;gap:6px}
.mnav-cat .mc-t{background:none;border:0;color:var(--gold-deep);font-size:16px;cursor:pointer;padding:4px;transition:.3s}
.mnav-cat.open .mc-t{transform:rotate(180deg)}
.mnav-cat .mc-list{display:none;flex-direction:column;align-items:center;gap:8px;margin-top:8px;padding:0 10px}
.mnav-cat.open .mc-list{display:flex}
.mnav-cat .mc-list a{font-size:13px;color:var(--charcoal-2);text-align:center}
.mnav-cat .mc-list .fh{font-size:10.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep);margin-top:6px}
</style>"""
MENU_JS = """<script id="svc-menu-js">document.querySelectorAll('.mc-t').forEach(b=>b.addEventListener('click',()=>{const c=b.closest('.mnav-cat');b.setAttribute('aria-expanded',c.classList.toggle('open')?'true':'false')}))</script>"""

def menu_items(c, mobile):
    out = []
    for x in c[3]:
        if isinstance(x[1], list):
            out.append('<span class="fh">%s</span>' % E(x[0]))
            out += ['<a href="%s">%s</a>' % (sub_url(c, s), E(t)) for s, t in x[1]]
        else:
            out.append('<a href="%s">%s</a>' % (sub_url(c, x[0]), E(x[1])))
    return ''.join(out)

def desktop_menu():
    h = ''
    for c in CATS:
        if subs_flat(c):
            h += '<div class="nsi"><a href="%s">%s <i class="ti ti-chevron-right"></i></a><div class="nav-fly">%s</div></div>' % (cat_url(c), E(c[1]), menu_items(c, False))
        else:
            h += '<a href="%s">%s</a>' % (cat_url(c), E(c[1]))
    return '<!--svc-menu-->' + h + '<!--/svc-menu-->'

def mobile_menu():
    h = ''
    for c in CATS:
        if subs_flat(c):
            h += '<div class="mnav-cat"><div class="mc-row"><a href="%s">%s</a><button class="mc-t" aria-expanded="false" aria-label="Υποκατηγορίες"><i class="ti ti-chevron-down"></i></button></div><div class="mc-list">%s</div></div>' % (cat_url(c), E(c[1]), menu_items(c, True))
        else:
            h += '<a href="%s">%s</a>' % (cat_url(c), E(c[1]))
    return '<!--svc-mmenu-->' + h + '<!--/svc-mmenu-->'

DM, MM = desktop_menu(), mobile_menu()
for f in pages:
    t = io.open(f, encoding="utf-8").read()
    if '<!--svc-menu-->' in t:
        t = re.sub(r'<!--svc-menu-->.*?<!--/svc-menu-->', lambda m: DM, t, flags=re.S)
    else:
        t, n = re.subn(r'(Υπηρεσίες <i class="ti ti-chevron-down"></i></a>\s*<div class="nav-sub">)(.*?)(\s*</div>)', lambda m: m.group(1) + DM + m.group(3), t, count=1, flags=re.S)
        assert n == 1, (f, 'desktop')
    if '<!--svc-mmenu-->' in t:
        t = re.sub(r'<!--svc-mmenu-->.*?<!--/svc-mmenu-->', lambda m: MM, t, flags=re.S)
    else:
        t, n = re.subn(r'(<div class="mnav-group)(">\s*<button class="mnav-toggle" aria-expanded="false">Υπηρεσίες <i class="ti ti-chevron-down"></i></button>\s*<div class="mnav-sub">)(.*?)(\s*</div>)', lambda m: m.group(1) + ' svc' + m.group(2) + MM + m.group(4), t, count=1, flags=re.S)
        assert n == 1, (f, 'mobile')
    t = re.sub(r'<style id="svc-menu-css">.*?</style>\n?', '', t, flags=re.S)
    t = t.replace('</head>', MENU_CSS + '\n</head>', 1)
    if 'id="svc-menu-js"' not in t: t = t.replace('</body>', MENU_JS + '\n</body>', 1)
    io.open(f, "w", encoding="utf-8", newline="").write(t)
print("μενού με υποκατηγορίες σε", len(pages), "σελίδες")
