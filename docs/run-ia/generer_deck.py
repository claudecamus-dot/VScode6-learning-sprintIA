"""Generation du deck « AGENTIC PRODUCT RUN — offre de service OCTO ».

Gabarit : template OCTO de la flotte (10 x 5.625 in, 34 layouts).
Patterns : deck-design-library / catalogue-transformation-commerciale
(conteneur = contour, etiquette = pilule pleine, chevron = sequence,
emphase en ligne, bandeau de cloture, « un sur N en accent »).

Toutes les hauteurs de bloc de texte sont CALCULEES sur le meme modele de
hauteur de ligne que `verifier_debordements_texte` (calibration pessimiste),
jamais posees en constantes : une phrase plus longue que l'echantillon de test
est le defaut n°1 des decks generes.

Usage : python generer_deck.py [chemin_sortie.pptx]
"""
import logging
import os
import re
import sys

from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# `pptx_deck` n'est PAS recopie ici : la source est la skill du kit agentic
# (.claude/skills/pptx-deck/scripts/), comme pour pptx-framed-image plus bas.
# Trois copies strictement identiques de 1260 lignes coexistaient jusqu'au
# 2026-09-20 ; tests/test_pptx_deck_non_duplique.py empeche leur retour.
_RACINE = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(_RACINE, ".claude", "skills", "pptx-deck", "scripts"))
import pptx_deck as D  # noqa: E402
import contenu_deck as C  # noqa: E402

#: Chemin du gabarit OCTO. Configurable via TEMPLATE_OCTO_PATH (constat
#: d'audit 5) : le repli ci-dessous n'est valide que sur les postes qui ont
#: VSCode2 a cote de ce depot, ce qui n'est vrai ni en CI ni chez qui que ce
#: soit d'autre.
TEMPLATE = os.environ.get(
    "TEMPLATE_OCTO_PATH",
    r"C:\Users\claude.camus\Documents\VSCode2\app\assets\template-octo.pptx",
)
SORTIE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "AGENTIC-PRODUCT-RUN-offre-octo.pptx")

# --- Gabarit mesure sur le template (cf. deck-design-library/template-octo.md) ---
L = 0.615            # marge gauche = left du placeholder titre du layout 5
R = 9.15             # bord droit utile : le badge de pagination commence a 9.25
CW = R - L           # 8.535 in
T_CLAIM = 0.86       # sous le placeholder titre (0.395 -> 0.801)
T_CONT = 1.28        # haut de la bande de contenu
B_CONT = 5.25        # bas utile

LAYOUT_COUVERTURE = 8
LAYOUT_TITRE_SEUL = 5
# « 50 - Chapitre [1] » : idx0 titre, idx1 numero, cadre photo teardrop.
# Ce template est le MEME fichier que celui de VSCode3 (md5 identique, cf.
# deck-design-library/template-octo.md), donc sa geometrie de chapitre est
# reprise telle quelle — la ou VSCode4, sur un layout 51 different, doit
# repositionner les formes pour l'imiter.
LAYOUT_CHAPITRE = 2
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_img")

# Calibration MESUREE sur un rendu PowerPoint reel du template (police Outfit,
# 2026-09-17) : 56 caracteres tenaient sur 3.78in a 10.5pt, soit ~14.8 car./pouce,
# la ou la valeur par defaut de pptx_deck (10.7, calibree sur une police plus
# large) en predisait 40. Garder 10.7 gonflait chaque carte de ~40 % et produisait
# des panneaux aux trois quarts vides. 13.0 = mesure moins une marge de securite.
CPI_LAYOUT = 14.0
# Hauteur de ligne mesuree au meme rendu : ~0.19in a 10.5pt interligne 1.1.
COEF_LIGNE = 0.0185
PAD_BOITE = 0.06
# Hauteur reellement consommee par D.add_card_header (libelle + filet d'accent) :
# 0.36 + 0.045 + 0.14. La budgeter a 0.32 faisait deborder la derniere puce de
# chaque carte a en-tete (constat du 2026-09-17, slide « Comment cette offre se vend »).
H_HEADER = 0.545

THEME = {}
NAVY = CYAN = MUTED = LINE = BG = SLATE = ""


def _init_couleurs(prs):
    global THEME, NAVY, CYAN, MUTED, LINE, BG, SLATE
    THEME = D.theme_colors(prs)
    NAVY = THEME.get("dk1", "#0E2356")
    CYAN = THEME.get("accent3", "#00D2DD")
    MUTED = THEME.get("lt2", "#586586")
    SLATE = THEME.get("dk2", "#3E4F78")
    LINE = THEME.get("accent5", "#CFD3DD")
    BG = THEME.get("accent6", "#E7E9EE")


# --- modele de hauteur, aligne sur le verificateur ---------------------------
NBSP = " "


def typo_fr(texte):
    """Espace insecable devant la ponctuation haute et avant « % ».

    Deux effets : la typographie francaise est respectee, et PowerPoint cesse
    de rejeter un « ? » orphelin sur sa propre ligne (constat du 2026-09-17,
    slide « Ce que je vous demande de trancher »).
    """
    if not isinstance(texte, str):
        return texte
    return re.sub(r" (?=[?!:;%])", NBSP, texte)


def lh(size):
    return size * COEF_LIGNE


def nlignes(texte, w, size):
    return D.estimer_lignes(texte, w, size, cpi_ref=CPI_LAYOUT)


def hbox(texte, w, size):
    """Hauteur de boite suffisante pour `texte` a `size` pt sur `w` pouces."""
    return nlignes(texte, w, size) * lh(size) + PAD_BOITE


def hbox_max(textes, w, size):
    return max(hbox(t, w, size) for t in textes)


def reste(bas, souhaite, mini=0.30):
    """Hauteur disponible entre `bas` et le bas de bande, bornee par `souhaite`.

    Leve si le contenu a deja mange la bande : une hauteur negative produit une
    forme invalide que python-pptx accepte et que PowerPoint refuse d'ouvrir
    (HRESULT 0x80070570) — defaut constate le 2026-09-17 sur la slide Readiness.
    """
    dispo = B_CONT - bas
    if dispo < mini:
        raise ValueError(
            "bande de contenu saturee : %.2fin disponibles sous y=%.2f "
            "(minimum %.2f) — raccourcir le contenu ou reduire les blocs"
            % (dispo, bas, mini))
    return min(souhaite, dispo)


# Retrait lateral du texte dans le bandeau : le guillemet decoratif occupe
# ~0.40in a gauche. `D.add_quote_banner` place sa boite de texte a +0.20in
# seulement, si bien que la premiere ligne d'une phrase longue MARCHE SUR le
# guillemet (constat utilisateur du 2026-09-17, slides 7/12/13/14/17). On
# redessine donc le bandeau ici, avec un retrait symetrique — le helper du hub
# n'est pas modifie depuis ce projet (regle : corriger au hub, jamais dans une
# copie locale).
RETRAIT_BANDEAU = 0.62


def hauteur_bandeau(texte, size=13.5):
    return (nlignes(typo_fr(texte), CW - 2 * RETRAIT_BANDEAU, size) * lh(size)
            + 0.17)


def bandeau(slide, bas, texte, size=13.5):
    """Bandeau de cloture, dimensionne sur SON texte puis cale en bas de bande.

    Une hauteur constante tronquait la derniere ligne au rendu (constat du
    2026-09-17) : la hauteur se calcule, elle ne se pose pas.
    """
    texte = typo_fr(texte)
    h = hauteur_bandeau(texte, size)
    y = B_CONT - h
    if y < bas + 0.10:
        raise ValueError(
            "bandeau de %.2fin ne tient pas sous y=%.2f (bas de bande %.2f)"
            % (h, bas, B_CONT))
    D.add_rect(slide, L, y, CW, h, fill=NAVY, rounded=True, radius=0.10)
    # guillemet decoratif, hors du flux du texte
    D.add_text(slide, L + 0.16, y + 0.02, 0.40, min(0.40, h - 0.04),
               [("“", {"size": 24, "bold": True, "color": CYAN})])
    D.add_text_runs(slide, L + RETRAIT_BANDEAU, y, CW - 2 * RETRAIT_BANDEAU, h,
                    [([(texte, {"size": size, "bold": True,
                                "color": "#FFFFFF"}),
                       ("  •", {"size": size, "bold": True,
                                      "color": CYAN})],
                      {"align": PP_ALIGN.CENTER})],
                    anchor=MSO_ANCHOR.MIDDLE)


def page(prs, titre, claim):
    """Slide « titre seul » + claim en phrase complete (Minto)."""
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITRE_SEUL])
    slide.shapes.title.text = typo_fr(titre)
    for p in slide.shapes.title.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(D.TYPE["title"])
            r.font.bold = True
            r.font.color.rgb = D.rgb(NAVY)
    D.add_text(slide, L, T_CLAIM, CW, 0.34,
               [(typo_fr(claim), {"size": D.TYPE["small"], "color": MUTED})])
    return slide


# Scene -> requete Openverse (photo reelle CC0). Le repli procedural
# (nature_images) n'a que 6 scenes : toute scene neuve doit y etre mappee,
# sinon le generateur plante (lecon VSCode3).
SCENES = {
    "1": ("foggy mountain landscape", "mountains", 0),
    "2": ("green forest sunlight", "forest", 0),
    # « turquoise water » (repris tel quel de VSCode3) rendait ici une carte
    # postale de Santorin — le piege que VSCode3 documente : une requete
    # mot-cle n'a aucun jugement, chaque photo se VALIDE a l'oeil.
    "3": ("steel bridge structure", "mountains", 0),
    "4": ("sunrise over hills", "sunset", 0),
}


def _remplir_cadre(slide, cadre, scene, requete, repli, seed=0):
    """Pose une vraie photo CC0 a l'aspect exact du cadre, repli procedural
    hors ligne. Repris de VSCode3 (`docs/cadrage-ppt/generate_deck.py`), y
    compris sa lecon de cache : le repli s'ecrit sous un nom DISTINCT, sinon
    `os.path.exists` sur le nom de la vraie photo passe a True pour de bon et
    aucun build suivant ne retente le reseau.
    """
    sys.path.insert(0, os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        ".claude", "skills", "pptx-framed-image", "scripts"))
    from framed_image import place_image_in_frame, cover_crop_to_aspect
    import nature_images
    import stock_images

    if cadre is None:
        print("  [chapitre %s] cadre introuvable — image non posee" % scene)
        return False
    left, top, width, height, geom = cadre[0], cadre[1], cadre[2], cadre[3], cadre[4]
    from pptx.util import Emu
    aspect = Emu(width).inches / Emu(height).inches
    px_w = 960
    px_h = int(round(px_w / aspect))
    os.makedirs(IMG_DIR, exist_ok=True)
    path = os.path.join(IMG_DIR, "%s_%d_%dx%d.jpg" % (scene, seed, px_w, px_h))
    path_repli = path[:-4] + "_repli.jpg"
    a_poser = path
    if not os.path.exists(path):
        brut = os.path.join(IMG_DIR, "_brut_%s_%d.jpg" % (scene, seed))
        try:
            stock_images.fetch_to(brut, requete, seed=seed)
            cover_crop_to_aspect(brut, path, aspect)
            print("  [chapitre %s] photo Openverse CC0 : %r" % (scene, requete))
        except Exception as e:
            # Le repli reste intentionnel (offline-first) mais l'echec doit
            # etre VISIBLE (constat d'audit 4) : type d'exception + message
            # actionnable dans les logs, pas seulement un print perdu dans la
            # sortie du build.
            logging.getLogger(__name__).warning(
                "[chapitre %s] Openverse indisponible (%s: %s), repli procedural %r utilise a la place",
                scene, type(e).__name__, e, repli, exc_info=True,
            )
            nature_images.generate_to(path_repli, repli, px_w, px_h, seed=seed)
            a_poser = path_repli
    place_image_in_frame(slide, a_poser, left, top, width, height, geom)
    return True


def chapitre(prs, num, titre, sous_titre):
    """Intercalaire de chapitre — layout natif « 50 - Chapitre [1] ».

    Repris de VSCode3 (`docs/cadrage-ppt/generate_deck.py::slide_chapitre`),
    qui tient la reference de la flotte sur ces slides, avec ses deux lecons
    payees : (1) le numero va dans le placeholder idx1 a 17pt, MARGES A ZERO
    et sans puce heritee — les marges par defaut (~0.1in/cote) mangent la
    largeur de l'encart (0.55in) et renvoient « 1 » a la ligne, hors cadre ;
    (2) le cadre photo teardrop se REMPLIT — laisse vide, le texte gabarit
    « ici mettre une Photo » s'imprime en rouge sur le rendu.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_CHAPITRE])
    phs = {ph.placeholder_format.idx: ph for ph in slide.placeholders}

    tf = phs[0].text_frame
    tf.text = typo_fr(titre)
    for p in tf.paragraphs[:1]:
        for r in p.runs:
            r.font.color.rgb = D.rgb(NAVY)
            r.font.bold = True
    p2 = tf.add_paragraph()
    p2.text = typo_fr(sous_titre)
    p2.space_before = Pt(8)
    for r in p2.runs:
        r.font.size = Pt(D.TYPE["small"])
        r.font.italic = True
        r.font.color.rgb = D.rgb(MUTED)

    tf_num = phs[1].text_frame
    tf_num.text = num
    tf_num.margin_left = tf_num.margin_right = 0
    tf_num.margin_top = tf_num.margin_bottom = 0
    tf_num.vertical_anchor = MSO_ANCHOR.MIDDLE
    for p in tf_num.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        D.sans_puce(p)
        for r in p.runs:
            r.font.size = Pt(17)
            r.font.bold = True
            r.font.color.rgb = D.rgb(NAVY)
    D.appliquer_police(tf_num)

    cadre = D.trouver_cadre_layout(slide.slide_layout.shapes, "teardrop")
    requete, repli, seed = SCENES[num]
    _remplir_cadre(slide, cadre, num, requete, repli, seed)
    return slide


def _vider_placeholder(slide, idx):
    """Retire un placeholder non utilise : laisse en place, PowerPoint peut
    afficher son texte d'invite a l'export."""
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx == idx:
            ph._element.getparent().remove(ph._element)


def barre(slide, x, y, h, couleur):
    """Barre verticale d'accent (composant transversal 6)."""
    D.add_rect(slide, x, y, 0.045, h, fill=couleur, rounded=True, radius=0.5)


def filet(slide, x, y, w, couleur=None):
    D.add_rect(slide, x, y, w, 0.012, fill=couleur or LINE)


def carte(slide, x, y, w, h, accent=False, couleur=None):
    """Conteneur = contour, jamais aplat (composant transversal 1)."""
    c = couleur or CYAN
    D.add_rect(slide, x, y, w, h, fill="#FFFFFF",
               line=c if accent else LINE, line_w=1.6 if accent else 1.2,
               rounded=True, radius=0.06)


def _pas_liste(items, w, size):
    """Pas UNIFORME d'une liste : la hauteur du plus long item.

    Un pas calcule item par item donne des interlignes inegaux des qu'une
    estimation se trompe d'une ligne — le rythme casse a l'oeil bien avant que
    le texte ne deborde (constat du 2026-09-17, slides 4/6/9).
    """
    return max(hbox(it, w - 0.18, size) for it in items)


def liste_puces(slide, x, y, w, items, couleur, size, gap=0.06, dot=0.06,
                pas=None):
    """Dessine une liste a puces a pas uniforme et renvoie le y atteint.

    `pas` impose un pas COMMUN a plusieurs colonnes soeurs : sans lui, une
    colonne d'items courts finit plus haut que sa voisine et ouvre un vide.
    """
    h = pas or _pas_liste(items, w, size)
    for i, it in enumerate(items):
        yy = y + i * (h + gap)
        D.add_dot(slide, x + 0.03, yy + 0.07, dot, couleur)
        D.add_text(slide, x + 0.18, yy, w - 0.18, h,
                   [(typo_fr(it), {"size": size, "color": SLATE, "line_spacing": 1.1})])
    return y + len(items) * (h + gap) - gap


def hauteur_liste(items, w, size, gap=0.06, pas=None):
    return len(items) * (pas or _pas_liste(items, w, size)) + gap * (len(items) - 1)


# --------------------------------------------------------------------------
# S2 — sommaire : les 4 chapitres, lus depuis le meme tuple que les intercalaires
# --------------------------------------------------------------------------
def slide_sommaire(prs):
    d = C.SOMMAIRE
    slide = page(prs, d["titre"], d["claim"])
    n = len(C.CHAPITRES)
    w = (CW - 0.20 * (n - 1)) / n
    h_t = hbox_max([c[1] for c in C.CHAPITRES], w - 0.36, D.TYPE["h3"])
    h_s = hbox_max([c[2] for c in C.CHAPITRES], w - 0.36, D.TYPE["small"])
    h = 0.18 + 0.40 + 0.14 + h_t + 0.12 + h_s + 0.20
    y = T_CONT + max(0.0, (B_CONT - T_CONT - h) / 2)
    for i, (num, titre, sous_titre) in enumerate(C.CHAPITRES):
        x = L + (w + 0.20) * i
        accent = i == n - 1
        couleur = CYAN if accent else MUTED
        carte(slide, x, y, w, h, accent=accent, couleur=couleur)
        D.add_badge(slide, x + 0.18, y + 0.18, 0.40, num,
                    CYAN if accent else NAVY,
                    text_color=NAVY if accent else "#FFFFFF",
                    size=D.TYPE["small"], radius=0.5)
        D.add_text(slide, x + 0.18, y + 0.72, w - 0.36, h_t,
                   [(typo_fr(titre), {"size": D.TYPE["h3"], "bold": True,
                                      "color": NAVY, "line_spacing": 1.05})])
        D.add_text(slide, x + 0.18, y + 0.72 + h_t + 0.12, w - 0.36, h_s,
                   [(typo_fr(sous_titre), {"size": D.TYPE["small"],
                                           "color": SLATE,
                                           "line_spacing": 1.1})])
    return slide


# --------------------------------------------------------------------------
# S16 — conclusion : ce que le client achete
# --------------------------------------------------------------------------
def slide_conclusion(prs):
    d = C.CONCLUSION
    slide = page(prs, d["titre"], d["claim"])
    w_num = 0.44
    x_txt = L + w_num + 0.20
    w_txt = CW - w_num - 0.20
    w_verb = 3.05
    w_corps = w_txt - w_verb - 0.24

    h_t = hbox_max([a[1] for a in d["arguments"]], w_corps, D.TYPE["body"])
    h_c = hbox_max([a[2] for a in d["arguments"]], w_corps, D.TYPE["small"])
    h_v = hbox_max([a[3] for a in d["arguments"]], w_verb - 0.36, D.TYPE["small"])
    h = max(h_t + 0.08 + h_c, h_v) + 0.20

    plafond = B_CONT - hauteur_bandeau(d["banner"]) - 0.22
    y0 = T_CONT + max(0.0, (plafond - T_CONT - (3 * h + 2 * 0.16)) / 2)
    for i, (num, titre, corps, verbatim) in enumerate(d["arguments"]):
        y = y0 + i * (h + 0.16)
        accent = i == 2
        couleur = CYAN if accent else MUTED
        D.add_badge(slide, L, y + (h - w_num) / 2, w_num, num, NAVY,
                    size=D.TYPE["small"], radius=0.5)
        D.add_text(slide, x_txt, y + 0.10, w_corps, h_t,
                   [(typo_fr(titre), {"size": D.TYPE["body"], "bold": True,
                                      "color": NAVY, "line_spacing": 1.05})])
        D.add_text(slide, x_txt, y + 0.10 + h_t + 0.08, w_corps, h_c,
                   [(typo_fr(corps), {"size": D.TYPE["small"], "color": SLATE,
                                      "line_spacing": 1.1})])
        # le verbatim est ce que le client se dira : contour, pas aplat, pour
        # qu'il reste une citation et non un encart de plus
        x_v = R - w_verb
        D.add_rect(slide, x_v, y, w_verb, h, fill="#FFFFFF",
                   line=couleur, line_w=1.6 if accent else 1.2,
                   rounded=True, radius=0.06)
        barre(slide, x_v + 0.16, y + 0.14, h - 0.28, couleur)
        D.add_text(slide, x_v + 0.30, y + (h - h_v) / 2, w_verb - 0.46, h_v,
                   [(typo_fr(verbatim), {"size": D.TYPE["small"], "italic": True,
                                         "color": NAVY, "line_spacing": 1.1})])
        if i < len(d["arguments"]) - 1:
            filet(slide, L, y + h + 0.08, CW)
    bandeau(slide, y0 + 3 * h + 2 * 0.16, d["banner"], size=13.5)
    return slide


# --------------------------------------------------------------------------
# S1 — couverture
# --------------------------------------------------------------------------
def slide_couverture(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_COUVERTURE])
    textes = {0: C.COUVERTURE["titre"], 1: C.COUVERTURE["sous_titre"],
              2: C.COUVERTURE["mention"], 3: C.COUVERTURE["date"]}
    for ph in slide.placeholders:
        idx = ph.placeholder_format.idx
        if idx in textes:
            ph.text_frame.text = textes[idx]
    return slide


# --------------------------------------------------------------------------
# S2 — le probleme : 4 constats en 2x2 + bandeau de cloture
# --------------------------------------------------------------------------
def slide_constats(prs):
    """Cinq constats en grille 2 x 3, le bandeau de cloture occupant la 6e
    case. La grille 2 x 2 d'origine ne tenait plus a 5 constats (ajout du
    pilotage du design system, 2026-09-17) : plutot que de laisser une case
    vide ou d'etaler le bandeau sous une rangee bancale, il devient la
    derniere tuile — la phrase a retenir ferme la lecture au meme endroit que
    l'oeil l'attend."""
    d = C.CONSTATS
    slide = page(prs, d["titre"], d["claim"])
    w = (CW - 0.25) / 2
    gap = 0.14
    h_t = hbox_max([c[1] for c in d["cartes"]], w - 0.76, D.TYPE["body"])
    h_c = hbox_max([c[2] for c in d["cartes"]], w - 0.36, D.TYPE["tiny"])
    h = 0.12 + h_t + 0.08 + h_c + 0.12
    total = 3 * h + 2 * gap
    if T_CONT + total > B_CONT:
        raise ValueError("grille des constats : %.2fin pour %.2fin de bande"
                         % (total, B_CONT - T_CONT))
    y0 = T_CONT + (B_CONT - T_CONT - total) / 2
    for i, (num, titre, corps) in enumerate(d["cartes"]):
        x = L + (w + 0.25) * (i % 2)
        y = y0 + (h + gap) * (i // 2)
        carte(slide, x, y, w, h)
        D.add_badge(slide, x + 0.18, y + 0.14, 0.30, num, NAVY,
                    size=D.TYPE["tiny"], radius=0.5)
        D.add_text(slide, x + 0.58, y + 0.12, w - 0.76, h_t,
                   [(typo_fr(titre), {"size": D.TYPE["body"], "bold": True,
                                      "color": NAVY, "line_spacing": 1.05})])
        D.add_text(slide, x + 0.18, y + 0.12 + h_t + 0.08, w - 0.36, h_c,
                   [(typo_fr(corps), {"size": D.TYPE["tiny"], "color": SLATE,
                                      "line_spacing": 1.12})])
    # 6e case : le bandeau de cloture, au gabarit d'une carte
    x = L + (w + 0.25) * (len(d["cartes"]) % 2)
    y = y0 + (h + gap) * (len(d["cartes"]) // 2)
    D.add_quote_banner(slide, x, y, w, h, typo_fr(d["banner"]),
                       fill=NAVY, accent=CYAN, size=12.5)
    return slide


# --------------------------------------------------------------------------
# S3 — deux ruptures (« un sur N en accent » : la 2e)
# --------------------------------------------------------------------------
def slide_ruptures(prs):
    d = C.RUPTURES
    slide = page(prs, d["titre"], d["claim"])
    w = (CW - 0.25) / 2
    def _titre_plat(c):
        t, mention = c[1]
        return t + (" (%s)" % mention if mention else "")

    h_t = hbox_max([_titre_plat(c) for c in d["colonnes"]], w - 0.40,
                   D.TYPE["h3"])
    h_l = max(hauteur_liste(c[2], w - 0.40, D.TYPE["small"], gap=0.08)
              for c in d["colonnes"])
    h = 0.18 + 0.26 + 0.12 + h_t + 0.14 + h_l + 0.18
    for i, (label, titre, points, accent) in enumerate(d["colonnes"]):
        x = L + (w + 0.25) * i
        y = T_CONT
        couleur = CYAN if accent else MUTED
        carte(slide, x, y, w, h, accent=accent, couleur=couleur)
        D.add_chip(slide, x + 0.20, y + 0.18, 1.32, 0.26, label, couleur,
                   text_color=NAVY if accent else "#FFFFFF", size=D.TYPE["tiny"])
        texte, mention = titre
        runs = [(typo_fr(texte), {"size": D.TYPE["h3"], "bold": True,
                                  "color": NAVY})]
        if mention:
            # emphase en ligne (composant transversal 5) : la reserve est DANS
            # la phrase, pas dans une note a part
            runs.append((" (", {"size": D.TYPE["h3"], "bold": True,
                                "color": NAVY}))
            runs.append((typo_fr(mention), {"size": D.TYPE["h3"], "bold": True,
                                            "italic": True, "color": NAVY}))
            runs.append((")", {"size": D.TYPE["h3"], "bold": True,
                               "color": NAVY}))
        D.add_text_runs(slide, x + 0.20, y + 0.56, w - 0.40, h_t,
                        [(runs, {"line_spacing": 1.05})])
        liste_puces(slide, x + 0.20, y + 0.56 + h_t + 0.14, w - 0.40, points,
                    couleur, D.TYPE["small"], gap=0.08)
    bas = T_CONT + h
    bandeau(slide, bas, d["banner"], size=13.5)
    return slide


# --------------------------------------------------------------------------
# S4 — la promesse : chaine de chevrons + entrees/sorties
# --------------------------------------------------------------------------
def slide_promesse(prs):
    d = C.PROMESSE
    slide = page(prs, d["titre"], d["claim"])
    n = len(d["chaine"])
    gap = 0.05
    wc = (CW - gap * (n - 1)) / n
    h_ch = 0.50
    # L'encoche d'un chevron OOXML vaut `adj` x le PLUS PETIT COTE : a la
    # valeur par defaut (0.5) elle mange 0.25in a gauche ET a droite, soit
    # 0.50in des 1.18in du chevron — il ne reste que 0.68in utiles et le
    # libelle chevauche les biseaux. On la ramene a 0.20 et on calcule la
    # largeur utile REELLE, au lieu de centrer sur le cadre exterieur.
    adj = 0.20
    encoche = adj * min(wc, h_ch)
    w_utile = wc - 2 * encoche - 0.06
    # Une seule taille pour toute la chaine (le plus long libelle decide) :
    # des tailles differentes d'un chevron a l'autre se voient immediatement.
    taille = D.TYPE["tiny"]
    while taille > 7.0 and max(nlignes(e, w_utile, taille)
                               for e in d["chaine"]) > 1:
        taille -= 0.5
    for i, etape in enumerate(d["chaine"]):
        x = L + (wc + gap) * i
        plein = i in (0, n - 1)
        shp = D.add_forme(slide, "chevron", x, T_CONT, wc, h_ch,
                          fill=NAVY if plein else "#FFFFFF",
                          line=NAVY if plein else LINE, line_w=1.2, adj=[adj])
        # Le libelle vit DANS la forme : une boite flottante par-dessus faisait
        # deux objets distincts dans PowerPoint, et son centrage se calculait
        # sur le cadre exterieur (biseaux compris) au lieu de l'interieur.
        tf = shp.text_frame
        tf.word_wrap = False
        tf.margin_left = tf.margin_right = Inches(encoche)
        tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        D.definir_paragraphes(tf, [([
            (typo_fr(etape), {"size": taille, "bold": True,
                              "color": "#FFFFFF" if plein else NAVY}),
        ], {"align": PP_ALIGN.CENTER})])
        D.appliquer_police(tf)

    w = (CW - 0.25) / 2
    y = T_CONT + 0.70
    blocs = [d["entrees"], d["sorties"]]
    h_l = max(hauteur_liste(b[1], w - 0.40, D.TYPE["small"]) for b in blocs)
    h = 0.18 + H_HEADER + h_l + 0.18
    for i, (label, items) in enumerate(blocs):
        x = L + (w + 0.25) * i
        couleur = MUTED if i == 0 else CYAN
        carte(slide, x, y, w, h, accent=(i == 1), couleur=couleur)
        yy = D.add_card_header(slide, x + 0.20, y + 0.18, w - 0.40, label, couleur,
                               size=D.TYPE["tiny"])
        liste_puces(slide, x + 0.20, yy, w - 0.40, items, couleur, D.TYPE["small"])
    bas = y + h
    bandeau(slide, bas, d["banner"], size=13.5)
    return slide


# --------------------------------------------------------------------------
# S5 — TMA / MCO : ou Agentic Product Run se branche (tableau a deux colonnes)
# --------------------------------------------------------------------------
def slide_socle(prs):
    d = C.SOCLE
    slide = page(prs, d["titre"], d["claim"])
    w_dom = 1.42
    gap = 0.16
    w_col = (CW - w_dom - gap * 2) / 2
    x_a = L + w_dom + gap
    x_b = x_a + w_col + gap

    y_en = T_CONT
    lab_a, lab_b = d["colonnes"]
    h_en = hbox_max([lab_a, lab_b], w_col - 0.28, D.TYPE["tiny"])
    D.add_rect(slide, x_a, y_en, w_col, h_en + 0.14, fill=BG, rounded=True,
               radius=0.06)
    D.add_rect(slide, x_b, y_en, w_col, h_en + 0.14, fill=CYAN, rounded=True,
               radius=0.06)
    for x, lab, col in ((x_a, lab_a, SLATE), (x_b, lab_b, NAVY)):
        D.add_text(slide, x + 0.14, y_en + 0.07, w_col - 0.28, h_en,
                   [(lab, {"size": D.TYPE["tiny"], "bold": True, "color": col})])

    textes_a = [l[1] for l in d["lignes"]]
    textes_b = [l[2] for l in d["lignes"]]
    h_cell = max(hbox_max(textes_a, w_col - 0.28, D.TYPE["small"]),
                 hbox_max(textes_b, w_col - 0.28, D.TYPE["small"]))
    n_lig = len(d["lignes"])
    # le pas se CALCULE sur la place restante (le tableau est passe de 5 a 6
    # lignes le 2026-09-17 avec la ligne « Securite ») : un pas constant
    # poussait le bandeau hors de la bande.
    y0 = y_en + h_en + 0.24
    dispo = B_CONT - hauteur_bandeau(d["banner"]) - 0.20 - y0
    pas_ligne = max(0.08, min(0.18, dispo / n_lig - h_cell))
    for i, (dom, avant, apres) in enumerate(d["lignes"]):
        y = y0 + i * (h_cell + pas_ligne)
        D.add_text(slide, L, y + 0.02, w_dom, h_cell,
                   [(dom, {"size": D.TYPE["small"], "bold": True, "color": NAVY})])
        D.add_text(slide, x_a + 0.14, y, w_col - 0.28, h_cell,
                   [(typo_fr(avant), {"size": D.TYPE["small"], "color": SLATE,
                                      "line_spacing": 1.1})])
        D.add_forme(slide, "chevron", x_b - 0.13, y + 0.04, 0.12, 0.18,
                    fill=CYAN, line=CYAN, line_w=0.75)
        D.add_text(slide, x_b + 0.14, y, w_col - 0.28, h_cell,
                   [(typo_fr(apres), {"size": D.TYPE["small"], "color": NAVY,
                                      "line_spacing": 1.1})])
        if i < len(d["lignes"]) - 1:
            filet(slide, L, y + h_cell + 0.04, CW)
    bas = y0 + n_lig * (h_cell + pas_ligne)
    bandeau(slide, bas, d["banner"], size=13.5)
    return slide

# --------------------------------------------------------------------------
# S13 — l'apport produit : une BOUCLE, pas trois colonnes
# --------------------------------------------------------------------------
def slide_produit(prs):
    """Pattern « chaine d'anneaux » (deck-design-library /
    catalogue-transformation-commerciale #4) reduit a 3 maillons : des cercles
    qui se chevauchent disent « cycle continu » la ou trois cartes disaient
    « trois sujets ». Un rail de retour ferme la boucle sous les cercles."""
    d = C.PRODUIT
    slide = page(prs, d["titre"], d["claim"])
    etapes = d["boucle"]
    n = len(etapes)
    # Les cercles ne se CHEVAUCHENT plus : avec un recouvrement, le pas
    # devenait plus petit que la largeur de legende necessaire, et les trois
    # legendes se superposaient (constat au rendu du 2026-09-17). Le lien est
    # porte par les chevrons entre cercles et par le rail de retour, pas par
    # le chevauchement.
    diam = 1.72
    ecart = 0.42
    pas = diam + ecart
    largeur = pas * (n - 1) + diam
    x0 = L + (CW - largeur) / 2
    y_c = T_CONT + 0.04

    for i, (titre, _corps) in enumerate(etapes):
        x = x0 + pas * i
        accent = i == n - 1
        couleur = CYAN if accent else MUTED
        D.add_forme(slide, "ellipse", x, y_c, diam, diam, fill="#FFFFFF",
                    line=couleur, line_w=2.0 if accent else 1.4)
        D.add_text(slide, x + 0.16, y_c + diam / 2 - 0.34, diam - 0.32, 0.28,
                   [("%d" % (i + 1), {"size": D.TYPE["h2"], "bold": True,
                                      "color": couleur,
                                      "align": PP_ALIGN.CENTER})])
        D.add_text(slide, x + 0.10, y_c + diam / 2 + 0.02, diam - 0.20, 0.26,
                   [(typo_fr(titre), {"size": D.TYPE["body"], "bold": True,
                                      "color": NAVY,
                                      "align": PP_ALIGN.CENTER})])
        # chevron dans la zone de recouvrement : le lien EST le chevauchement,
        # pas une fleche posee a cote (composant transversal 3)
        if i < n - 1:
            D.add_forme(slide, "chevron", x + diam + ecart / 2 - 0.13,
                        y_c + diam / 2 - 0.12, 0.26, 0.24,
                        fill=CYAN, line=CYAN, line_w=0.75)

    y_txt = y_c + diam + 0.18
    w_txt = pas - 0.16
    h_txt = max(hbox(c, w_txt - 0.12, D.TYPE["tiny"]) for _t, c in etapes)
    for i, (_titre, corps) in enumerate(etapes):
        x = x0 + pas * i + diam / 2 - w_txt / 2
        D.add_text(slide, x, y_txt, w_txt, h_txt,
                   [(typo_fr(corps), {"size": D.TYPE["tiny"], "color": SLATE,
                                      "align": PP_ALIGN.CENTER,
                                      "line_spacing": 1.12})])

    # rail de retour : c'est lui qui fait une BOUCLE et non une sequence
    y_r = y_txt + h_txt + 0.20
    h_r = hbox(d["retour"], largeur - 1.04, D.TYPE["tiny"])
    x_r = L + (CW - largeur) / 2
    D.add_rect(slide, x_r, y_r, largeur, h_r + 0.22, fill=BG,
               rounded=True, radius=0.5)
    # chevron de retour A L'INTERIEUR du rail, pointe vers la gauche
    D.add_forme(slide, "chevron", x_r + 0.16, y_r + (h_r + 0.22) / 2 - 0.12,
                0.26, 0.24, fill=CYAN, line=CYAN, line_w=0.75, rot=180)
    D.add_text(slide, x_r + 0.52, y_r + 0.11, largeur - 1.04, h_r,
               [(typo_fr(d["retour"]), {"size": D.TYPE["tiny"], "bold": True,
                                        "color": NAVY,
                                        "align": PP_ALIGN.CENTER})])
    bandeau(slide, y_r + h_r + 0.22, d["banner"], size=13.5)
    return slide


# --------------------------------------------------------------------------
# S9 — le parcours en trois temps (fiches-etapes a chip chevauchant + rail)
# --------------------------------------------------------------------------
def slide_modules(prs):
    """Pattern « roadmap en etapes numerotees avec fiches detaillees »
    (deck-design-library / catalogue-restitution #10) : cadre contour seul,
    chip numerote-titre CHEVAUCHANT le bord superieur, rupture « livrable »
    dans la carte, rail horizontal reliant les chips. Remplace les 3 cartes en
    colonnes — forme deja portee par 5 autres slides du deck — et absorbe
    l'ex-slide « trajectoire », dont la progression 1/2/3 redisait celle des
    modules (fusion 2026-09-17)."""
    d = C.MODULES
    slide = page(prs, d["titre"], d["claim"])
    n = len(d["etapes"])
    w = (CW - 0.24 * (n - 1)) / n
    wi = w - 0.36
    h_chip = 0.38
    h_l = max(hauteur_liste(e[3], wi, D.TYPE["tiny"], gap=0.07)
              for e in d["etapes"])
    h_liv = hbox_max([e[4] for e in d["etapes"]], wi - 0.30, D.TYPE["tiny"])
    h_aut = hbox_max([e[5] for e in d["etapes"]], wi, D.TYPE["tiny"])
    y = T_CONT + 0.20
    h_carte = (0.16 + 0.24 + 0.14 + h_l + 0.18 + h_liv + 0.18 + 0.14
               + 0.10 + h_aut + 0.16)

    # rail horizontal : c'est lui qui fait lire « parcours » et non « catalogue »
    D.add_rect(slide, L + 0.40, y + h_chip / 2 - 0.015, CW - 0.80, 0.03,
               fill=LINE)

    for i, etape in enumerate(d["etapes"]):
        num, titre, duree, points, livrable, autonomie, accent = etape
        x = L + (w + 0.24) * i
        couleur = CYAN if accent else MUTED
        carte(slide, x, y + h_chip / 2, w, h_carte, accent=accent,
              couleur=couleur)
        # chip a cheval sur le bord superieur du cadre (composant 4)
        w_chip = wi + 0.04
        D.add_forme(slide, "round2SameRect", x + (w - w_chip) / 2, y,
                    w_chip, h_chip, fill=NAVY, line=NAVY, line_w=1.0)
        D.add_text(slide, x + (w - w_chip) / 2, y + 0.09, w_chip, 0.22,
                   [(u"%s · %s" % (num, typo_fr(titre)),
                     {"size": D.TYPE["tiny"], "bold": True, "color": "#FFFFFF",
                      "align": PP_ALIGN.CENTER})])
        yy = y + h_chip / 2 + 0.16
        D.add_chip(slide, x + 0.18, yy, 1.30, 0.24, duree, BG,
                   text_color=SLATE, size=D.TYPE["tiny"])
        yy += 0.38
        liste_puces(slide, x + 0.18, yy, wi, points, couleur, D.TYPE["tiny"],
                    gap=0.07)
        y_liv = yy + h_l + 0.18
        D.add_rect(slide, x + 0.18, y_liv, wi, h_liv + 0.18, fill=BG,
                   rounded=True, radius=0.06)
        barre(slide, x + 0.26, y_liv + 0.06, h_liv + 0.06, couleur)
        D.add_text(slide, x + 0.40, y_liv + 0.09, wi - 0.30, h_liv,
                   [(typo_fr(livrable), {"size": D.TYPE["tiny"], "bold": True,
                                         "color": NAVY, "line_spacing": 1.05})])
        y_aut = y_liv + h_liv + 0.18 + 0.14
        filet(slide, x + 0.18, y_aut, wi)
        D.add_text(slide, x + 0.18, y_aut + 0.10, wi, h_aut,
                   [(typo_fr(autonomie), {"size": D.TYPE["tiny"], "italic": True,
                                          "color": MUTED,
                                          "line_spacing": 1.05})])
    return slide


# --------------------------------------------------------------------------
# S6 — RUN Readiness Check : grille de 10 domaines + livrables
# --------------------------------------------------------------------------
def slide_readiness(prs):
    d = C.READINESS
    slide = page(prs, d["titre"], d["claim"])
    wg = 5.05
    wq = wg - 1.72
    h_q = hbox_max([q for _, q in d["domaines"]], wq, D.TYPE["tiny"])
    hr = h_q + 0.10
    for i, (dom, question) in enumerate(d["domaines"]):
        y = T_CONT + hr * i
        if i % 2 == 0:
            D.add_rect(slide, L, y, wg, hr, fill=BG)
        D.add_text(slide, L + 0.12, y + 0.05, 1.42, h_q,
                   [(typo_fr(dom), {"size": D.TYPE["tiny"], "bold": True, "color": NAVY})])
        D.add_text(slide, L + 1.58, y + 0.05, wq, h_q,
                   [(typo_fr(question), {"size": D.TYPE["tiny"], "color": SLATE,
                                "line_spacing": 1.05})])
    bas_grille = T_CONT + hr * len(d["domaines"])

    xr = L + wg + 0.16
    wr = R - xr
    D.add_chip(slide, xr, T_CONT, 1.72, 0.28, "2 À 4 SEMAINES", CYAN,
               text_color=NAVY, size=D.TYPE["tiny"])
    yc = T_CONT + 0.44
    label, items = d["livrables"]
    hc = 0.18 + H_HEADER + hauteur_liste(items, wr - 0.40, D.TYPE["small"]) + 0.18
    carte(slide, xr, yc, wr, hc, accent=True)
    yy = D.add_card_header(slide, xr + 0.20, yc + 0.18, wr - 0.40, label, CYAN,
                           size=D.TYPE["tiny"])
    liste_puces(slide, xr + 0.20, yy, wr - 0.40, items, CYAN, D.TYPE["small"])

    y_enc = max(bas_grille, yc + hc) + 0.14
    D.add_encart(slide, L, y_enc, CW, reste(y_enc, 0.44), d["accroche"],
                 accent=CYAN, size=D.TYPE["small"])
    return slide


# --------------------------------------------------------------------------
# S7 — la preuve : avant / apres relies par un chevron
# --------------------------------------------------------------------------
def slide_preuve(prs):
    d = C.PREUVE
    slide = page(prs, d["titre"], d["claim"])
    w = 3.85
    y = T_CONT
    colonnes = [(L, d["avant"], MUTED, "\u2014", False),
                (R - w, d["apres"], CYAN, "\u2713", True)]
    wi = w - 0.60
    h_i = max(hbox(lead + " " + suite, wi, D.TYPE["small"])
              for _, (_, items), _, _, _ in colonnes for lead, suite in items)
    n_i = max(len(items) for _, (_, items), _, _, _ in colonnes)
    h = 0.18 + 0.26 + 0.16 + n_i * (h_i + 0.08) - 0.08 + 0.18
    for x, (label, items), couleur, puce, accent in colonnes:
        carte(slide, x, y, w, h, accent=accent, couleur=couleur)
        D.add_chip(slide, x + 0.20, y + 0.18, 2.62, 0.26, label, couleur,
                   text_color=NAVY if accent else "#FFFFFF", size=D.TYPE["tiny"])
        yy = y + 0.60
        for lead, suite in items:
            D.add_text(slide, x + 0.20, yy, 0.18, 0.24,
                       [(puce, {"size": D.TYPE["small"], "bold": True,
                                "color": couleur})])
            D.add_text_runs(slide, x + 0.40, yy, wi, h_i, [([
                (typo_fr(lead) + " ", {"size": D.TYPE["small"], "bold": True, "color": NAVY}),
                (typo_fr(suite), {"size": D.TYPE["small"], "color": SLATE}),
            ], {"line_spacing": 1.1})])
            yy += h_i + 0.08
    # centre dans l'interstice entre les deux cartes, sans les toucher
    x_ch = L + w + ((R - w) - (L + w) - 0.60) / 2
    D.add_forme(slide, "chevron", x_ch, y + h / 2 - 0.30, 0.60, 0.60,
                fill="#FFFFFF", line=CYAN, line_w=2.5)
    bas = y + h
    bandeau(slide, bas, d["banner"], size=13.0)
    return slide

# --------------------------------------------------------------------------
# S14 — produits agentiques : blueprint en 3 bandes de pastilles
# --------------------------------------------------------------------------
def slide_agentique(prs):
    """Pattern « blueprint en 3 bandes » (deck-design-library /
    catalogue-restitution #8) : bandes teintees pleine largeur portant des
    pastilles, au lieu de 3 cartes de puces. Une bande se lit d'un coup d'oeil,
    et la derniere — seule teintee cyan — dit ou nous intervenons."""
    d = C.AGENTIQUE
    slide = page(prs, d["titre"], d["claim"])
    w_lab = 1.66
    x_b = L + w_lab + 0.14
    w_b = R - x_b
    h_pill = 0.27
    gap_p = 0.09

    def largeur_pastille(t):
        # la pastille se dimensionne sur SON texte : une largeur fixe
        # tronquerait « Executions non reproductibles » et gaspillerait la
        # place autour de « Boucles ».
        return max(0.72, nlignes(t, 9.0, D.TYPE["tiny"]) and
                   len(t) * 0.070 + 0.30)

    bandes = []
    for label, accent, pastilles in d["bandes"]:
        lignes, cur, larg = [], [], 0.0
        for t in pastilles:
            lp = largeur_pastille(t)
            if cur and larg + gap_p + lp > w_b - 0.36:
                lignes.append(cur)
                cur, larg = [], 0.0
            cur.append((t, lp))
            larg += (gap_p if larg else 0) + lp
        if cur:
            lignes.append(cur)
        bandes.append((label, accent, lignes))

    h_bandes = [0.14 + len(lg) * h_pill + (len(lg) - 1) * 0.07 + 0.14
                for _l, _a, lg in bandes]
    total = sum(h_bandes) + 0.13 * (len(bandes) - 1)
    plafond = B_CONT - hauteur_bandeau(d["banner"]) - 0.20
    y = T_CONT + max(0.0, (plafond - T_CONT - total) / 2)

    for (label, accent, lignes), h_b in zip(bandes, h_bandes):
        # melanger_blanc(c, frac) : frac = part de BLANC ajoutee. 0.14
        # rendait la bande presque cyan pur (fond criard sous du texte
        # fonce) — il en faut 0.86 pour une teinte de fond.
        fond = D.melanger_blanc(CYAN, 0.86) if accent else BG
        D.add_rect(slide, x_b, y, w_b, h_b, fill=fond, rounded=True, radius=0.06)
        h_lab = hbox(label, w_lab, D.TYPE["tiny"])
        D.add_text(slide, L, y + (h_b - h_lab) / 2, w_lab, h_lab,
                   [(label, {"size": D.TYPE["tiny"], "bold": True,
                             "color": CYAN if accent else MUTED,
                             "align": PP_ALIGN.RIGHT, "line_spacing": 1.1})])
        yy = y + 0.14
        for ligne in lignes:
            xx = x_b + 0.18
            for texte, lp in ligne:
                # add_chip(outline=True) prend `color` pour la bordure ET
                # le texte : lui passer du blanc rendait les pastilles
                # vides (constat au rendu du 2026-09-17).
                D.add_chip(slide, xx, yy, lp, h_pill, texte,
                           NAVY if accent else SLATE,
                           size=D.TYPE["tiny"], outline=True)
                xx += lp + gap_p
            yy += h_pill + 0.07
        y += h_b + 0.13
    bandeau(slide, y - 0.13, d["banner"], size=13.5)
    return slide


# --------------------------------------------------------------------------
def slide_trajectoire(prs):
    d = C.TRAJECTOIRE
    slide = page(prs, d["titre"], d["claim"])
    n = 3
    w = (CW - 0.22 * (n - 1)) / n
    wi = w - 0.32
    h_l = max(hauteur_liste(p[3], wi, D.TYPE["small"]) for p in d["phases"])
    h_g = hbox_max([p[4] for p in d["phases"]], wi, D.TYPE["small"])
    h_a = hbox_max([p[5] for p in d["phases"]], wi, D.TYPE["tiny"])
    tete = 0.16 + 0.40 + 0.10 + 0.24 + 0.12
    h = tete + h_l + 0.16 + h_g + 0.12 + 0.01 + 0.08 + h_a + 0.14
    y = T_CONT + 0.06
    for i, (num, titre, increment, points, garde, autonomie) in enumerate(d["phases"]):
        x = L + (w + 0.22) * i
        accent = i == 2
        couleur = CYAN if accent else MUTED
        carte(slide, x, y, w, h, accent=accent, couleur=couleur)
        D.add_forme(slide, "chevron", x + 0.16, y + 0.16, w - 0.32, 0.40,
                    fill=NAVY, line=NAVY, line_w=1.0)
        D.add_text(slide, x + 0.30, y + 0.25, w - 0.60, 0.24,
                   [(typo_fr(titre), {"size": D.TYPE["tiny"], "bold": True,
                                      "color": "#FFFFFF",
                                      "align": PP_ALIGN.CENTER})])
        # badge a cheval sur le coin haut-gauche de la carte (composant 4)
        D.add_badge(slide, x - 0.13, y - 0.13, 0.34, num,
                    CYAN if accent else NAVY, text_color=NAVY if accent else "#FFFFFF",
                    size=D.TYPE["tiny"], radius=0.5)
        D.add_chip(slide, x + 0.16, y + 0.66, 1.22, 0.24, increment, BG,
                   text_color=SLATE, size=D.TYPE["tiny"])
        liste_puces(slide, x + 0.16, y + tete, wi, points, couleur, D.TYPE["small"])
        y_g = y + tete + h_l + 0.16
        D.add_text(slide, x + 0.16, y_g, wi, h_g,
                   [(typo_fr(garde), {"size": D.TYPE["small"], "bold": True, "color": NAVY,
                             "align": PP_ALIGN.CENTER, "line_spacing": 1.05})])
        y_f = y_g + h_g + 0.12
        filet(slide, x + 0.16, y_f, wi)
        D.add_text(slide, x + 0.16, y_f + 0.08, wi, h_a,
                   [(typo_fr(autonomie), {"size": D.TYPE["tiny"], "italic": True,
                                 "color": MUTED, "align": PP_ALIGN.CENTER,
                                 "line_spacing": 1.05})])
    return slide


# --------------------------------------------------------------------------
# S10 — comment ca se vend : 2x2
# --------------------------------------------------------------------------
def slide_vente(prs):
    d = C.VENTE
    slide = page(prs, d["titre"], d["claim"])
    w = (CW - 0.25) / 2
    h_l = max(hauteur_liste(b[1], w - 0.36, D.TYPE["tiny"], gap=0.07)
              for b in d["blocs"])
    h = 0.15 + H_HEADER + h_l + 0.18
    y0 = T_CONT + max(0.0, (B_CONT - T_CONT - (2 * h + 0.18)) / 2)
    for i, (label, items) in enumerate(d["blocs"]):
        x = L + (w + 0.25) * (i % 2)
        y = y0 + (h + 0.18) * (i // 2)
        accent = i == 3
        couleur = CYAN if accent else MUTED
        carte(slide, x, y, w, h, accent=accent, couleur=couleur)
        yy = D.add_card_header(slide, x + 0.18, y + 0.15, w - 0.36, label, couleur,
                               size=D.TYPE["tiny"])
        liste_puces(slide, x + 0.18, yy, w - 0.36, items, couleur, D.TYPE["tiny"],
                    gap=0.07)
    return slide


# --------------------------------------------------------------------------
# S11 — ce qu'on demande de trancher
# --------------------------------------------------------------------------
def slide_decisions(prs):
    d = C.DECISIONS
    slide = page(prs, d["titre"], d["claim"])
    n = 3
    w = (CW - 0.20 * (n - 1)) / n
    h_q = hbox_max([c[1] for c in d["cartes"]], w - 0.36, D.TYPE["body"])
    h_d = hbox_max([c[2] for c in d["cartes"]], w - 0.36, D.TYPE["small"])
    h = 0.16 + 0.32 + 0.12 + h_q + 0.12 + h_d + 0.16
    plafond = B_CONT - hauteur_bandeau(d["banner"]) - 0.20
    y = T_CONT + max(0.0, (plafond - T_CONT - h) / 2)
    for i, (num, question, detail, accent) in enumerate(d["cartes"]):
        x = L + (w + 0.20) * i
        couleur = CYAN if accent else MUTED
        carte(slide, x, y, w, h, accent=accent, couleur=couleur)
        D.add_badge(slide, x + 0.18, y + 0.16, 0.32, num, couleur,
                    text_color=NAVY if accent else "#FFFFFF",
                    size=D.TYPE["tiny"], radius=0.5)
        D.add_text(slide, x + 0.18, y + 0.60, w - 0.36, h_q,
                   [(typo_fr(question), {"size": D.TYPE["body"], "bold": True, "color": NAVY,
                                "line_spacing": 1.05})])
        D.add_text(slide, x + 0.18, y + 0.60 + h_q + 0.12, w - 0.36, h_d,
                   [(typo_fr(detail), {"size": D.TYPE["small"], "color": SLATE,
                              "line_spacing": 1.1})])
    bas = y + h
    bandeau(slide, bas, d["banner"], size=13.5)
    return slide


# --------------------------------------------------------------------------
def construire(sortie=SORTIE):
    prs = Presentation(TEMPLATE)
    D.clear_slides(prs)
    _init_couleurs(prs)
    D.set_police(D.police_marque(prs) or D.police_theme(prs))

    # Trame arbitree le 2026-09-18 : enjeux du CLIENT (contexte + douleurs) ->
    # enjeux d'OCTO (ce qui nous rend defendables) -> l'offre -> next steps.
    # Structure en miroir : le temps 1 est le cote client, le temps 2 le notre.
    # L'ancien chapitre « ce qui la rend defendable » devient donc le temps
    # OCTO, il ne disparait pas. `slide_trajectoire` reste fusionnee dans
    # `slide_modules` (2026-09-17, meme progression 1/2/3).
    # `slide_conclusion` (synthese) clot desormais l'offre plutot que
    # « next steps » : ce chapitre ne doit porter que des actions.
    # `slide_decisions` reactivee le 2026-09-18 (retiree du plan le
    # 2026-09-17) : c'est le seul contenu du deck qui soit un vrai next step.
    plan = [
        (None, [slide_couverture, slide_sommaire]),
        (C.CHAPITRES[0], [slide_ruptures, slide_constats]),
        (C.CHAPITRES[1], [slide_preuve, slide_produit, slide_agentique]),
        (C.CHAPITRES[2], [slide_promesse, slide_socle, slide_modules,
                          slide_readiness, slide_conclusion]),
        (C.CHAPITRES[3], [slide_vente, slide_decisions]),
    ]
    for chap, fns in plan:
        if chap:
            chapitre(prs, *chap)
        for fn in fns:
            fn(prs)

    controles = {
        "hors-cadre": D.verifier_geometrie(prs),
        # calibration explicite : la valeur par defaut (10.7) est trop pessimiste
        # pour Outfit et produit des faux positifs en cascade (cf. CPI_LAYOUT).
        "debordement-texte": D.verifier_debordements_texte(
            prs, cpi_pessimiste=CPI_LAYOUT),
        "chrome-gabarit": D.verifier_chrome_gabarit(prs),
        "plancher": D.verifier_plancher_de_dessin(prs, B_CONT, bord_droit_in=R),
    }
    ok = True
    for nom, defauts in controles.items():
        if defauts:
            ok = False
            print("DEFAUTS %s (%d) :" % (nom, len(defauts)))
            for x in defauts[:30]:
                print("   ", x)
    D.purger_rels_slides_orphelines(prs)
    prs.save(sortie)
    print("%s -> %s (%d slides)" % ("OK" if ok else "KO", sortie, len(prs.slides)))
    return ok


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    cible = sys.argv[1] if len(sys.argv) > 1 else SORTIE
    sys.exit(0 if construire(cible) else 1)
