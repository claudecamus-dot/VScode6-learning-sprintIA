# -*- coding: utf-8 -*-
"""Generation du deck « AGENTIC PRODUCT RUN — atelier ».

Gabarit : template OCTO de la flotte (10 x 5.625 in). Boilerplate (constantes
de gabarit, helpers de hauteur, `page`, `carte`, `bandeau`, `liste_puces`...)
copie depuis docs/run-ia/generer_deck.py : ce deck-ci est un livrable SEPARE,
pas une modification de l'offre existante.

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
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
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
                      "AGENTIC-PRODUCT-RUN-atelier.pptx")

L = 0.615
R = 9.15
CW = R - L
T_CLAIM = 0.86
T_CONT = 1.28
B_CONT = 5.25

LAYOUT_COUVERTURE = 8
LAYOUT_TITRE_SEUL = 5

CPI_LAYOUT = 14.0
COEF_LIGNE = 0.0185
PAD_BOITE = 0.06
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


NBSP = " "


def typo_fr(texte):
    if not isinstance(texte, str):
        return texte
    return re.sub(r" (?=[?!:;%])", NBSP, texte)


def lh(size):
    return size * COEF_LIGNE


def nlignes(texte, w, size):
    return D.estimer_lignes(texte, w, size, cpi_ref=CPI_LAYOUT)


def hbox(texte, w, size):
    return nlignes(texte, w, size) * lh(size) + PAD_BOITE


def hbox_max(textes, w, size):
    return max(hbox(t, w, size) for t in textes)


def reste(bas, souhaite, mini=0.30):
    dispo = B_CONT - bas
    if dispo < mini:
        raise ValueError(
            "bande de contenu saturee : %.2fin disponibles sous y=%.2f "
            "(minimum %.2f)" % (dispo, bas, mini))
    return min(souhaite, dispo)


RETRAIT_BANDEAU = 0.62


def hauteur_bandeau(texte, size=13.5):
    return (nlignes(typo_fr(texte), CW - 2 * RETRAIT_BANDEAU, size) * lh(size)
            + 0.17)


def bandeau(slide, bas, texte, size=13.5):
    texte = typo_fr(texte)
    h = hauteur_bandeau(texte, size)
    y = B_CONT - h
    if y < bas + 0.10:
        raise ValueError(
            "bandeau de %.2fin ne tient pas sous y=%.2f (bas de bande %.2f)"
            % (h, bas, B_CONT))
    D.add_rect(slide, L, y, CW, h, fill=NAVY, rounded=True, radius=0.10)
    D.add_text(slide, L + 0.16, y + 0.02, 0.40, min(0.40, h - 0.04),
               [("\u201c", {"size": 24, "bold": True, "color": CYAN})])
    D.add_text_runs(slide, L + RETRAIT_BANDEAU, y, CW - 2 * RETRAIT_BANDEAU, h,
                    [([(texte, {"size": size, "bold": True, "color": "#FFFFFF"}),
                       ("  \u2022", {"size": size, "bold": True, "color": CYAN})],
                      {"align": PP_ALIGN.CENTER})],
                    anchor=MSO_ANCHOR.MIDDLE)


def page(prs, titre, claim):
    """`claim=None` : pas de sous-titre, le contenu remonte sous le titre.
    C'est le cas de la slide Contexte depuis la relecture JL du 2026-09-18."""
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITRE_SEUL])
    slide.shapes.title.text = typo_fr(titre)
    for p in slide.shapes.title.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(D.TYPE["title"])
            r.font.bold = True
            r.font.color.rgb = D.rgb(NAVY)
    if claim:
        D.add_text(slide, L, T_CLAIM, CW, 0.34,
                   [(typo_fr(claim), {"size": D.TYPE["small"], "color": MUTED})])
    return slide


def bandeau_fleche(slide, bas, texte, size=13.5):
    """Variante du bandeau de cloture reprise de la relecture JL : largeur
    ajustee au texte et centree, chevron cyan en ouverture au lieu du
    guillemet decoratif."""
    texte = typo_fr(texte)
    w_max = CW - 1.60
    n = nlignes(texte, w_max, size)
    h = n * lh(size) + 0.34
    # largeur = celle du texte reellement pose, bornee, puis centree
    cpi = CPI_LAYOUT * (10.5 / size)
    w_txt = min(w_max, len(texte) / cpi if n == 1 else w_max)
    w = w_txt + 1.30
    x = L + (CW - w) / 2
    y = B_CONT - h
    if y < bas + 0.10:
        raise ValueError(
            "bandeau fleche de %.2fin ne tient pas sous y=%.2f (bas %.2f)"
            % (h, bas, B_CONT))
    D.add_rect(slide, x, y, w, h, fill=NAVY, rounded=True, radius=0.10)
    D.add_text(slide, x + 0.30, y, 0.40, h,
               [(">", {"size": size + 3, "bold": True, "color": CYAN})],
               anchor=MSO_ANCHOR.MIDDLE)
    D.add_text_runs(slide, x + 0.76, y, w - 1.06, h,
                    [([(texte, {"size": size, "bold": True, "color": "#FFFFFF"}),
                       ("  •", {"size": size, "bold": True, "color": CYAN})],
                      {"align": PP_ALIGN.CENTER})],
                    anchor=MSO_ANCHOR.MIDDLE)


IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_img")


def photo(slide, x, y, w, h, requete, repli, seed=0):
    """Pose une photo CC0 (Openverse) dans un rectangle a coins arrondis.

    Repris de `../generer_deck.py::_remplir_cadre`, y compris sa lecon de
    cache : le repli procedural s'ecrit sous un nom DISTINCT, sinon
    `os.path.exists` sur le nom de la vraie photo passe a True pour de bon et
    aucun build suivant ne retente le reseau.

    Et la lecon de VSCode3 qui va avec : une requete mot-cle n'a AUCUN
    jugement — chaque photo se valide a l'oeil au rendu.
    """
    # .../<racine>/docs/run-ia/atelier-agentic-run/generer_deck.py -> 4 niveaux
    racine = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    sys.path.insert(0, os.path.join(racine, ".claude", "skills",
                                    "pptx-framed-image", "scripts"))
    # Le magasin de certificats PAR DEFAUT de Python sur ce poste porte une
    # autorite racine EXPIREE : la recherche Openverse passe (api.openverse.org)
    # mais le telechargement depuis le CDN tiers (upload.wikimedia.org) echoue
    # en CERTIFICATE_VERIFY_FAILED. Le certificat du CDN est valide — verifie
    # le 2026-09-18, il expire le 9 novembre 2026 — c'est bien le magasin local
    # qui est en cause. On pointe donc explicitement le bundle `certifi`.
    # Correctif LOCAL a ce generateur : le script du kit partage
    # (.claude/skills/pptx-framed-image) n'est pas fautif, on ne le modifie pas.
    try:
        import certifi
        os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    except ImportError:
        pass
    from framed_image import place_image_in_frame, cover_crop_to_aspect, round2diag_geom
    import nature_images
    import stock_images

    aspect = w / h
    px_w = 960
    px_h = int(round(px_w / aspect))
    os.makedirs(IMG_DIR, exist_ok=True)
    # Le cache est nomme d'apres la REQUETE, pas d'apres le repli : ranger une
    # vraie photo de salle de controle sous « mountains_3.jpg » (le nom du
    # repli procedural) trompe la prochaine lecture du dossier.
    slug = re.sub(r"[^a-z0-9]+", "-", requete.lower()).strip("-")[:40]
    chemin = os.path.join(IMG_DIR, "%s_%d_%dx%d.jpg" % (slug, seed, px_w, px_h))
    chemin_repli = os.path.join(
        IMG_DIR, "%s_%d_%dx%d_repli.jpg" % (repli, seed, px_w, px_h))
    a_poser = chemin
    if not os.path.exists(chemin):
        brut = os.path.join(IMG_DIR, "_brut_%s_%d.jpg" % (slug, seed))
        try:
            stock_images.fetch_to(brut, requete, seed=seed)
            cover_crop_to_aspect(brut, chemin, aspect)
            print("  photo Openverse CC0 : %r" % requete)
        except Exception as e:
            # Le repli reste intentionnel (offline-first) mais l'echec doit
            # etre VISIBLE (constat d'audit 4) : type d'exception + message
            # actionnable dans les logs, pas seulement un print perdu dans la
            # sortie du build.
            logging.getLogger(__name__).warning(
                "Openverse indisponible (%s: %s), repli procedural %r utilise a la place",
                type(e).__name__, e, repli, exc_info=True,
            )
            nature_images.generate_to(chemin_repli, repli, px_w, px_h, seed=seed)
            a_poser = chemin_repli
    elif os.path.exists(chemin_repli):
        a_poser = chemin_repli
    place_image_in_frame(slide, a_poser, Inches(x), Inches(y), Inches(w),
                         Inches(h), round2diag_geom())
    return True


def barre(slide, x, y, h, couleur):
    D.add_rect(slide, x, y, 0.045, h, fill=couleur, rounded=True, radius=0.5)


def filet(slide, x, y, w, couleur=None):
    D.add_rect(slide, x, y, w, 0.014, fill=couleur or LINE)


def carte(slide, x, y, w, h, accent=False, couleur=None):
    D.add_rect(slide, x, y, w, h, fill="#FFFFFF",
               line=couleur if accent else LINE,
               line_w=1.6 if accent else 1.0, rounded=True, radius=0.08)


def _pas_liste(items, w, size):
    def _txt(it):
        return it if isinstance(it, str) else (it[0] + " " + it[1])
    return hbox_max([_txt(it) for it in items], w - 0.30, size)


def liste_puces(slide, x, y, w, items, couleur, size, gap=0.06, dot=0.06,
                pas=None):
    pas = pas or _pas_liste(items, w, size)
    yy = y
    for it in items:
        D.add_forme(slide, "ellipse", x, yy + (lh(size) - dot) / 2 + 0.02,
                    dot, dot, fill=couleur, line=None)
        if isinstance(it, str):
            D.add_text(slide, x + 0.22, yy, w - 0.22, pas,
                       [(typo_fr(it), {"size": size, "color": SLATE,
                                       "line_spacing": 1.1})])
        else:
            lead, suite = it
            D.add_text_runs(slide, x + 0.22, yy, w - 0.22, pas, [([
                (typo_fr(lead) + " ", {"size": size, "bold": True, "color": NAVY}),
                (typo_fr(suite), {"size": size, "color": SLATE}),
            ], {"line_spacing": 1.1})])
        yy += pas + gap
    return yy


def hauteur_liste(items, w, size, gap=0.06, pas=None):
    pas = pas or _pas_liste(items, w, size)
    return len(items) * (pas + gap) - gap


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


def slide_sommaire(prs):
    d = C.SOMMAIRE
    slide = page(prs, d["titre"], d["claim"])
    items = C.SOMMAIRE_ITEMS
    wg = 5.05
    wq = wg - 1.72
    h_t = hbox_max([t for _, t, _ in items], wq, D.TYPE["tiny"])
    hr = h_t + 0.10
    for i, (num, titre, sous) in enumerate(items[:5]):
        y = T_CONT + hr * i
        if i % 2 == 0:
            D.add_rect(slide, L, y, wg, hr, fill=BG)
        D.add_text(slide, L + 0.12, y + 0.05, 0.32, h_t,
                   [(num, {"size": D.TYPE["tiny"], "bold": True, "color": NAVY})])
        D.add_text(slide, L + 0.48, y + 0.05, wq, h_t,
                   [(typo_fr(titre), {"size": D.TYPE["tiny"], "bold": True,
                                      "color": NAVY})])
    xr = L + wg + 0.16
    wr = R - xr
    for i, (num, titre, sous) in enumerate(items[5:]):
        y = T_CONT + hr * i
        if i % 2 == 0:
            D.add_rect(slide, xr, y, wr, hr, fill=BG)
        D.add_text(slide, xr + 0.12, y + 0.05, 0.32, h_t,
                   [(num, {"size": D.TYPE["tiny"], "bold": True, "color": NAVY})])
        D.add_text(slide, xr + 0.48, y + 0.05, wr - 0.48, h_t,
                   [(typo_fr(titre), {"size": D.TYPE["tiny"], "bold": True,
                                      "color": NAVY})])
    return slide


# --------------------------------------------------------------------------
# S1 — contexte : intro + 3 verbatims + bandeau
# --------------------------------------------------------------------------
def slide_contexte(prs):
    d = C.CONTEXTE
    slide = page(prs, d["titre"], d["claim"])
    # Les deux phrases d'intro sont des PUCES (relecture JL), et elles
    # remontent sous le titre puisqu'il n'y a plus de sous-titre.
    y_i = T_CLAIM
    h_i = hauteur_liste(d["intro"], CW - 0.40, D.TYPE["body"], gap=0.06)
    liste_puces(slide, L + 0.20, y_i, CW - 0.40, d["intro"], CYAN,
                D.TYPE["body"], gap=0.06, dot=0.08)
    y = y_i + h_i + 0.30
    n = len(d["verbatims"])
    w = (CW - 0.20 * (n - 1)) / n
    h_v = hbox_max([v[2] for v in d["verbatims"]], w - 0.44, D.TYPE["small"])
    h = 0.18 + h_v + 0.14 + 0.24 + 0.16
    for i, (nom, role, citation) in enumerate(d["verbatims"]):
        x = L + (w + 0.20) * i
        carte(slide, x, y, w, h)
        barre(slide, x + 0.16, y + 0.16, h_v + 0.10, CYAN)
        D.add_text(slide, x + 0.32, y + 0.16, w - 0.48, h_v,
                   [(u"\u00ab " + typo_fr(citation) + u" \u00bb",
                     {"size": D.TYPE["small"], "italic": True, "color": NAVY,
                      "line_spacing": 1.1})])
        D.add_text(slide, x + 0.32, y + 0.16 + h_v + 0.14, w - 0.48, 0.24,
                   [(nom + " \u2014 " + typo_fr(role),
                     {"size": D.TYPE["tiny"], "color": MUTED})])
    bandeau_fleche(slide, y + h, d["banner"], size=13.5)
    return slide


# --------------------------------------------------------------------------
# S2 — enjeux pour OCTO : grille 2x2 de cartes numerotees + bandeau
# (forme reprise du deck offre : carte a contour, badge numerote, bandeau de
# cloture — une liste a puces nue etait la slide la plus plate du deck)
# --------------------------------------------------------------------------
def slide_enjeux_octo(prs):
    """FORME REPRISE DE LA RELECTURE JL (2026-09-18) : liste a puces pleine
    largeur + bandeau a chevron. La grille 2x2 de cartes numerotees qui avait
    ete proposee ici est abandonnee — c'est cette version-la qui est validee.
    """
    d = C.ENJEUX_OCTO
    slide = page(prs, d["titre"], d["claim"])
    w = CW - 0.80
    h_l = hauteur_liste(d["items"], w, D.TYPE["body"], gap=0.16)
    plafond = B_CONT - 0.75
    y = T_CONT + max(0.0, (plafond - T_CONT - h_l) / 2)
    liste_puces(slide, L + 0.40, y, w, d["items"], CYAN, D.TYPE["body"],
                gap=0.16, dot=0.09)
    bandeau_fleche(slide, y + h_l + 0.20, d["banner"], size=14.0)
    return slide


# --------------------------------------------------------------------------
# S3 — offre : 7 douleurs en grille 2 colonnes (4 + 3)
# --------------------------------------------------------------------------
def slide_offre_douleurs(prs):
    d = C.OFFRE_DOULEURS
    slide = page(prs, d["titre"], d["claim"])
    items = d["items"]
    w = (CW - 0.25) / 2
    h_t = hbox_max(items, w - 0.62, D.TYPE["small"])
    h = 0.16 + h_t + 0.16
    gap = 0.14
    col1 = items[:4]
    col2 = items[4:]
    y0 = T_CONT + 0.10
    for i, txt in enumerate(col1):
        y = y0 + (h + gap) * i
        carte(slide, L, y, w, h)
        D.add_badge(slide, L + 0.16, y + (h - 0.30) / 2, 0.30, str(i + 1),
                    NAVY, size=D.TYPE["tiny"], radius=0.5)
        D.add_text(slide, L + 0.58, y + (h - h_t) / 2, w - 0.74, h_t,
                   [(typo_fr(txt), {"size": D.TYPE["small"], "color": NAVY,
                                    "bold": True, "line_spacing": 1.08})])
    for i, txt in enumerate(col2):
        y = y0 + (h + gap) * i
        x = L + w + 0.25
        carte(slide, x, y, w, h, accent=True, couleur=CYAN)
        D.add_badge(slide, x + 0.16, y + (h - 0.30) / 2, 0.30, str(i + 5),
                    CYAN, text_color=NAVY, size=D.TYPE["tiny"], radius=0.5)
        D.add_text(slide, x + 0.58, y + (h - h_t) / 2, w - 0.74, h_t,
                   [(typo_fr(txt), {"size": D.TYPE["small"], "color": NAVY,
                                    "bold": True, "line_spacing": 1.08})])
    return slide


# --------------------------------------------------------------------------
# S4 — preuve sourcee : 6 items lead+suite en 2 colonnes + bandeau source
# --------------------------------------------------------------------------
def slide_preuve_recherche(prs):
    d = C.PREUVE_RECHERCHE
    slide = page(prs, d["titre"], d["claim"])
    items = d["items"]
    w = (CW - 0.30) / 2
    col1, col2 = items[:3], items[3:]
    h_i = _pas_liste(items, w, D.TYPE["tiny"])
    h_l = hauteur_liste(col1, w, D.TYPE["tiny"], gap=0.14, pas=h_i)
    plafond = B_CONT - hauteur_bandeau(d["banner"]) - 0.20
    y = T_CONT + max(0.0, (plafond - T_CONT - h_l) / 2)
    liste_puces(slide, L, y, w, col1, MUTED, D.TYPE["tiny"], gap=0.14, pas=h_i)
    liste_puces(slide, L + w + 0.30, y, w, col2, CYAN, D.TYPE["tiny"], gap=0.14,
                pas=h_i)
    bandeau(slide, plafond, d["banner"], size=12.0)
    return slide


# --------------------------------------------------------------------------
# S5 — OCTO acteur : 3 cartes simples
# --------------------------------------------------------------------------
def slide_octo_acteur(prs):
    d = C.OCTO_ACTEUR
    slide = page(prs, d["titre"], d["claim"])
    n = len(d["cartes"])
    w = (CW - 0.20 * (n - 1)) / n
    h_c = hbox_max([c[1] for c in d["cartes"]], w - 0.36, D.TYPE["small"])
    # Hauteur ALIGNEE sur la position reelle des blocs : le titre est pose a
    # +0.66 et le corps a +1.00. La formule precedente (0.86 + h_c) budgetait
    # 0.14in de moins que le contenu, et la derniere ligne du corps sortait
    # sous la bordure de la carte — invisible pour `verifier_debordements_texte`,
    # qui compare le texte a SA boite, jamais au cadre qui l'entoure.
    Y_TITRE, H_TITRE = 0.66, 0.34
    h = Y_TITRE + H_TITRE + h_c + 0.20
    y = T_CONT + max(0.0, (B_CONT - T_CONT - h) / 2)
    for i, (titre, corps) in enumerate(d["cartes"]):
        x = L + (w + 0.20) * i
        accent = i == 1
        carte(slide, x, y, w, h, accent=accent, couleur=CYAN if accent else MUTED)
        D.add_badge(slide, x + 0.18, y + 0.18, 0.34, str(i + 1),
                    CYAN if accent else NAVY, text_color=NAVY if accent else "#FFFFFF",
                    size=D.TYPE["small"], radius=0.5)
        D.add_text(slide, x + 0.18, y + Y_TITRE, w - 0.36, 0.30,
                   [(typo_fr(titre), {"size": D.TYPE["h3"], "bold": True,
                                      "color": NAVY, "line_spacing": 1.0})])
        D.add_text(slide, x + 0.18, y + Y_TITRE + H_TITRE, w - 0.36, h_c,
                   [(typo_fr(corps), {"size": D.TYPE["small"], "color": SLATE,
                                      "line_spacing": 1.1})])
    return slide


# --------------------------------------------------------------------------
# S6 — proposition de valeur : liste + chaine de chevrons + bandeau
# --------------------------------------------------------------------------
def slide_proposition_valeur(prs):
    """Chaine de chevrons EN HAUT (le mecanisme), puis la carte de ce qui est
    garanti — ordre et composants repris de `slide_promesse` du deck offre,
    dont la forme portait mieux que la liste a puces nue d'origine."""
    d = C.PROPOSITION_VALEUR
    slide = page(prs, d["titre"], d["claim"])

    n = len(d["chaine"])
    gap = 0.05
    wc = (CW - gap * (n - 1)) / n
    h_ch = 0.46
    y_ch = T_CONT
    adj = 0.20
    encoche = adj * min(wc, h_ch)
    w_utile = wc - 2 * encoche - 0.06
    taille = D.TYPE["tiny"]
    while taille > 7.0 and max(nlignes(e, w_utile, taille) for e in d["chaine"]) > 1:
        taille -= 0.5
    for i, etape in enumerate(d["chaine"]):
        x = L + (wc + gap) * i
        plein = i in (0, n - 1)
        shp = D.add_forme(slide, "chevron", x, y_ch, wc, h_ch,
                          fill=NAVY if plein else "#FFFFFF",
                          line=NAVY if plein else LINE, line_w=1.2, adj=[adj])
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

    # carte « ce qui est garanti » : contour + en-tete a filet d'accent
    # Espacements resserres pour absorber la 6e garantie ajoutee a la
    # relecture JL sans perdre la carte ni le bandeau.
    y = y_ch + h_ch + 0.16
    wi = CW - 0.40
    h_l = hauteur_liste(d["items"], wi, D.TYPE["small"], gap=0.05)
    h = 0.12 + H_HEADER + h_l + 0.14
    carte(slide, L, y, CW, h, accent=True, couleur=CYAN)
    yy = D.add_card_header(slide, L + 0.20, y + 0.12, wi, d["entete"], CYAN,
                           size=D.TYPE["tiny"])
    liste_puces(slide, L + 0.20, yy, wi, d["items"], CYAN, D.TYPE["small"],
                gap=0.05, dot=0.08)
    bandeau(slide, y + h, d["banner"], size=13.0)
    return slide


# --------------------------------------------------------------------------
# S7 — comment : 3 phases numerotees, rail horizontal
# --------------------------------------------------------------------------
def slide_comment(prs):
    """Pattern « blueprint en 3 bandes » (deck-design-library /
    catalogue-restitution #8), transpose depuis `slide_agentique` du deck
    offre. Remplace les 3 colonnes de puces : en colonne etroite (2.0in de
    texte utile) le libelle ne pouvait pas grossir sans partir sur 3 lignes,
    et les colonnes courtes laissaient un blanc mort en bas. En bande pleine
    largeur, chaque activite est une pastille dimensionnee sur SON texte, a
    une taille lisible."""
    d = C.COMMENT
    slide = page(prs, d["titre"], d["claim"])
    w_lab = 1.74
    x_b = L + w_lab + 0.14
    w_b = R - x_b
    # Cotes resserrees le 2026-09-18 : developper « ASRF (Agentic Software Run
    # Factory) » elargit sa pastille a 4.44in, qui ne partage plus sa ligne —
    # la bande 2 passe de 2 a 3 lignes et le total depassait la slide (defaut
    # attrape par `verifier_geometrie`). La taille du texte, elle, ne bouge
    # pas : c'est precisement ce qu'on venait d'agrandir.
    h_pill = 0.31
    gap_p = 0.10
    taille = D.TYPE["small"]

    def largeur_pastille(t):
        return max(0.80, len(t) * 0.076 + 0.34)

    bandes = []
    for num, titre, activites, accent in d["etapes"]:
        lignes, cur, larg = [], [], 0.0
        for t in activites:
            lp = min(largeur_pastille(t), w_b - 0.36)
            if cur and larg + gap_p + lp > w_b - 0.36:
                lignes.append(cur)
                cur, larg = [], 0.0
            cur.append((t, lp))
            larg += (gap_p if larg else 0) + lp
        if cur:
            lignes.append(cur)
        bandes.append((num, titre, accent, lignes))

    h_bandes = [0.13 + len(lg) * h_pill + (len(lg) - 1) * 0.07 + 0.13
                for _n, _t, _a, lg in bandes]
    total = sum(h_bandes) + 0.13 * (len(bandes) - 1)
    if total > B_CONT - T_CONT:
        raise ValueError("bandes « En pratique » : %.2fin pour %.2fin de bande"
                         % (total, B_CONT - T_CONT))
    y = T_CONT + max(0.0, (B_CONT - T_CONT - total) / 2)

    for (num, titre, accent, lignes), h_b in zip(bandes, h_bandes):
        fond = D.melanger_blanc(CYAN, 0.86) if accent else BG
        D.add_rect(slide, x_b, y, w_b, h_b, fill=fond, rounded=True, radius=0.07)
        h_lab = hbox(titre, w_lab - 0.44, D.TYPE["tiny"])
        D.add_badge(slide, L, y + (h_b - 0.32) / 2, 0.32, num,
                    CYAN if accent else NAVY,
                    text_color=NAVY if accent else "#FFFFFF",
                    size=D.TYPE["tiny"], radius=0.5)
        D.add_text(slide, L + 0.40, y + (h_b - h_lab) / 2, w_lab - 0.44, h_lab,
                   [(typo_fr(titre), {"size": D.TYPE["tiny"], "bold": True,
                                      "color": CYAN if accent else MUTED,
                                      "line_spacing": 1.1})])
        yy = y + 0.13
        for ligne in lignes:
            xx = x_b + 0.18
            for texte, lp in ligne:
                D.add_chip(slide, xx, yy, lp, h_pill, typo_fr(texte),
                           NAVY if accent else SLATE, size=taille, outline=True)
                xx += lp + gap_p
            yy += h_pill + 0.07
        y += h_b + 0.13
    return slide


def _slide_comment_colonnes_ancien(prs):
    """Ancienne forme en 3 colonnes de puces — conservee hors plan pour
    reference, remplacee par les bandes le 2026-09-18."""
    d = C.COMMENT
    slide = page(prs, d["titre"], d["claim"])
    n = len(d["etapes"])
    w = (CW - 0.24 * (n - 1)) / n
    wi = w - 0.36
    h_chip = 0.38
    # hauteur commune = la colonne la plus chargee, a pas serre. Les colonnes
    # plus courtes etaleront leurs items dessus (cf. gap_i plus bas).
    def _nat(points):
        p = _pas_liste(points, wi - 0.02, D.TYPE["tiny"])
        return len(points) * p + (len(points) - 1) * 0.08
    h_l = max(_nat(e[2]) for e in d["etapes"])
    y = T_CONT + 0.30
    h_carte = 0.16 + h_chip / 2 + 0.16 + h_l + 0.20

    D.add_rect(slide, L + 0.40, y + h_chip / 2 - 0.015, CW - 0.80, 0.03, fill=LINE)

    compteur = 1
    for i, (num, titre, points, accent) in enumerate(d["etapes"]):
        x = L + (w + 0.24) * i
        couleur = CYAN if accent else MUTED
        carte(slide, x, y + h_chip / 2, w, h_carte, accent=accent, couleur=couleur)
        w_chip = wi + 0.04
        D.add_forme(slide, "round2SameRect", x + (w - w_chip) / 2, y,
                    w_chip, h_chip, fill=NAVY, line=NAVY, line_w=1.0)
        D.add_text(slide, x + (w - w_chip) / 2, y + 0.09, w_chip, 0.22,
                   [(u"%s \u00b7 %s" % (num, typo_fr(titre)),
                     {"size": D.TYPE["tiny"], "bold": True, "color": "#FFFFFF",
                      "align": PP_ALIGN.CENTER})])
        # Repartition EGALE sur la hauteur commune : les colonnes n'ont pas le
        # meme nombre d'activites (5/3/4), et un pas fixe laissait un grand
        # blanc mort au bas des colonnes courtes. Le pas se calcule par
        # colonne pour que chacune remplisse la meme hauteur.
        yy = y + h_chip / 2 + 0.18
        pas = _pas_liste(points, wi - 0.02, D.TYPE["tiny"])
        n_i = len(points)
        gap_i = ((h_l - n_i * pas) / (n_i - 1)) if n_i > 1 else 0.0
        gap_i = max(0.08, min(gap_i, 0.34))
        for j, txt in enumerate(points):
            # Badge cale sur la PREMIERE LIGNE du texte, pas au centre de la
            # boite : `pas` est uniforme par colonne (hauteur de l'item le
            # plus long), donc un centrage decalait le badge sous le texte des
            # items d'une seule ligne.
            D.add_badge(slide, x + 0.18, yy + (lh(D.TYPE["tiny"]) - 0.24) / 2 + 0.02,
                        0.24, str(compteur), couleur,
                        text_color=NAVY if accent else "#FFFFFF",
                        size=7.5, radius=0.5)
            D.add_text(slide, x + 0.50, yy, wi - 0.32, pas,
                       [(typo_fr(txt), {"size": D.TYPE["tiny"], "color": SLATE,
                                        "line_spacing": 1.1})])
            yy += pas + gap_i
            compteur += 1
    return slide


# --------------------------------------------------------------------------
# S7 — reporting : deux niveaux en regard, chip de rythme + public
# --------------------------------------------------------------------------
def slide_reporting(prs):
    """Deux niveaux en RANGEES (pattern « chaine de paires reliees par
    chevron », catalogue-transformation-commerciale #13) plutot qu'en deux
    cartes cote a cote : le contenu est court, la rangee le porte mieux et
    laisse la place a une photo qui aere la slide."""
    d = C.REPORTING
    slide = page(prs, d["titre"], d["claim"])
    w_ph = 2.72                       # colonne de droite : le bloc XLA
    x_ph = R - w_ph
    wz = x_ph - 0.28 - L              # zone des rangees, a gauche
    w_chip = 1.42
    w_chev = 0.56                     # gouttiere du chevron de liaison
    # w_txt = largeur INTERIEURE de la carte ; la carte fait w_txt + 0.36.
    # Oublier ce +0.36 ici faisait passer la carte SOUS le panneau voisin —
    # collision que `verifier_geometrie` ne voit pas (il ne detecte que les
    # sorties de slide, jamais deux formes qui se chevauchent).
    #
    # La largeur garde une MARGE volontaire : a 2.955in, « Pour le management
    # operationnel » (31 car.) tombait pile sur la capacite estimee d'une ligne
    # (31 car.), l'estimateur le donnait sur 1 ligne et LibreOffice le passait
    # sur 2 — le titre recouvrait alors son propre texte. Un calcul juste a la
    # limite n'est pas un calcul juste.
    w_txt = wz - w_chip - w_chev - 0.36

    h_t = hbox_max([x[1] for x in d["niveaux"]], w_txt, D.TYPE["h3"])
    h_c = hbox_max([x[2] for x in d["niveaux"]], w_txt, D.TYPE["small"])
    h = 0.20 + h_t + 0.10 + h_c + 0.20
    gap = 0.22
    total = 2 * h + gap
    plafond = B_CONT - hauteur_bandeau(d["banner"], 13.0) - 0.22
    y0 = T_CONT + max(0.0, (plafond - T_CONT - total) / 2)

    # Colonne droite : ce qui ALIMENTE le reporting (XLA), en regard des deux
    # rythmes qui le restituent. Remplace le panneau photo — le contenu prime.
    wx = w_ph - 0.40
    h_x = max(hbox(a + " " + b, wx, D.TYPE["tiny"]) for a, b in d["xla"])
    carte(slide, x_ph, y0, w_ph, total, accent=True, couleur=CYAN)
    yx = D.add_card_header(slide, x_ph + 0.20, y0 + 0.18, wx, d["xla_label"],
                           CYAN, size=D.TYPE["tiny"])
    for fort, suite in d["xla"]:
        D.add_forme(slide, "ellipse", x_ph + 0.20,
                    yx + (lh(D.TYPE["tiny"]) - 0.07) / 2 + 0.02, 0.07, 0.07,
                    fill=CYAN, line=None)
        D.add_text_runs(slide, x_ph + 0.42, yx, wx - 0.22, h_x, [([
            (typo_fr(fort) + " : ", {"size": D.TYPE["tiny"], "bold": True,
                                     "color": NAVY}),
            (typo_fr(suite), {"size": D.TYPE["tiny"], "color": SLATE}),
        ], {"line_spacing": 1.12})])
        yx += h_x + 0.12

    for i, (rythme, public, detail, accent) in enumerate(d["niveaux"]):
        y = y0 + (h + gap) * i
        couleur = CYAN if accent else MUTED
        # pilule pleine = etiquette courte (composant 2 du catalogue)
        D.add_chip(slide, L, y + (h - 0.30) / 2, w_chip, 0.30, rythme, couleur,
                   text_color=NAVY if accent else "#FFFFFF", size=D.TYPE["tiny"])
        # chevron de liaison, en contour : marqueur de flux (composant 3)
        D.add_forme(slide, "chevron", L + w_chip + 0.11, y + (h - 0.34) / 2,
                    0.34, 0.34, fill="#FFFFFF", line=couleur, line_w=1.8,
                    adj=[0.30])
        xc = L + w_chip + w_chev
        carte(slide, xc, y, w_txt + 0.36, h, accent=accent, couleur=couleur)
        D.add_text(slide, xc + 0.18, y + 0.18, w_txt, h_t,
                   [(typo_fr(public), {"size": D.TYPE["h3"], "bold": True,
                                       "color": NAVY, "line_spacing": 1.05})])
        D.add_text(slide, xc + 0.18, y + 0.18 + h_t + 0.10, w_txt, h_c,
                   [(typo_fr(detail), {"size": D.TYPE["small"], "color": SLATE,
                                       "line_spacing": 1.1})])
    bandeau(slide, y0 + total, d["banner"], size=13.0)
    return slide


# --------------------------------------------------------------------------
# S8 — ce que ca change chez le client : avant / apres relies par un chevron
# (deck-design-library / catalogue-transformation-commerciale #12 :
# « montrer concretement ce qui change »)
# --------------------------------------------------------------------------
def slide_transformation(prs):
    d = C.TRANSFORMATION
    slide = page(prs, d["titre"], d["claim"])
    w = 3.85
    wi = w - 0.60
    colonnes = [(L, d["avant"], MUTED, "—", False),
                (R - w, d["apres"], CYAN, "✓", True)]
    h_i = max(hbox(lead + " " + suite, wi, D.TYPE["tiny"])
              for _x, (_l, items), _c, _p, _a in colonnes for lead, suite in items)
    n_i = max(len(items) for _x, (_l, items), _c, _p, _a in colonnes)
    h = 0.18 + 0.26 + 0.16 + n_i * (h_i + 0.09) - 0.09 + 0.18
    plafond = B_CONT - hauteur_bandeau(d["banner"], 12.5) - 0.20
    y = T_CONT + max(0.0, (plafond - T_CONT - h) / 2)
    if y + h > plafond:
        raise ValueError("avant/apres : %.2fin pour %.2fin sous le bandeau"
                         % (h, plafond - T_CONT))
    for x, (label, items), couleur, puce, accent in colonnes:
        carte(slide, x, y, w, h, accent=accent, couleur=couleur)
        D.add_chip(slide, x + 0.20, y + 0.18, 2.70, 0.26, label, couleur,
                   text_color=NAVY if accent else "#FFFFFF", size=D.TYPE["tiny"])
        yy = y + 0.60
        for lead, suite in items:
            D.add_text(slide, x + 0.20, yy, 0.18, 0.24,
                       [(puce, {"size": D.TYPE["tiny"], "bold": True,
                                "color": couleur})])
            D.add_text_runs(slide, x + 0.40, yy, wi, h_i, [([
                (typo_fr(lead) + " ", {"size": D.TYPE["tiny"], "bold": True,
                                       "color": NAVY}),
                (typo_fr(suite), {"size": D.TYPE["tiny"], "color": SLATE}),
            ], {"line_spacing": 1.1})])
            yy += h_i + 0.09
    # chevron centre dans l'interstice, sans toucher les deux cartes
    x_ch = L + w + ((R - w) - (L + w) - 0.60) / 2
    D.add_forme(slide, "chevron", x_ch, y + h / 2 - 0.30, 0.60, 0.60,
                fill="#FFFFFF", line=CYAN, line_w=2.5)
    bandeau(slide, y + h, d["banner"], size=12.5)
    return slide


# --------------------------------------------------------------------------
# S9 — cloture : 3 blocs (opportunites / pitch / next steps)
# --------------------------------------------------------------------------
def slide_cloture(prs):
    """Le PITCH en panneau hero pleine largeur (fill navy, emphase en ligne),
    les deux autres volets en cartes de soutien dessous. La version
    precedente le noyait dans une rangee de trois cartes egales : il n'avait
    aucun poids visuel alors que c'est la phrase a retenir."""
    d = C.CLOTURE
    slide = page(prs, d["titre"], d["claim"])

    # --- panneau hero : le pitch ---
    # La pastille « LE PITCH » est posee A GAUCHE, en vis-a-vis des lignes,
    # et non au-dessus : sa rangee propre coutait 0.46in de hauteur, que les
    # trois cartes de soutien reclament depuis que le bloc « Contacter
    # d'autres OCTOs » s'est ajoute (relecture du 2026-09-18).
    w_lab = 1.28
    x_txt = L + 0.34 + w_lab + 0.30
    w_txt = R - 0.34 - x_txt
    h_li = max(hbox(a + " " + b, w_txt, D.TYPE["h3"]) for a, b in d["pitch"])
    h_hero = 0.18 + len(d["pitch"]) * (h_li + 0.08) - 0.08 + 0.18
    y = T_CONT
    D.add_rect(slide, L, y, CW, h_hero, fill=NAVY, rounded=True, radius=0.10)
    D.add_chip(slide, L + 0.34, y + (h_hero - 0.30) / 2, w_lab, 0.30,
               d["pitch_label"], CYAN, text_color=NAVY, size=D.TYPE["tiny"])
    yy = y + 0.18
    for i, (fort, suite) in enumerate(d["pitch"]):
        accent = i == len(d["pitch"]) - 1
        barre(slide, x_txt - 0.18, yy + 0.03, h_li - 0.06,
              CYAN if accent else "#3E5A8F")
        # emphase EN LIGNE (composant 5) : le mot a enjeu en cyan dans la
        # phrase, pas la phrase entiere en gras.
        D.add_text_runs(slide, x_txt, yy, w_txt, h_li, [([
            (typo_fr(fort) + " ", {"size": D.TYPE["h3"], "bold": True,
                                   "color": CYAN if accent else "#FFFFFF"}),
            (typo_fr(suite), {"size": D.TYPE["h3"], "color": "#FFFFFF"}),
        ], {"line_spacing": 1.08})])
        yy += h_li + 0.08

    # --- deux volets de soutien ---
    n = len(d["blocs"])
    w = (CW - 0.25) / n
    y2 = y + h_hero + 0.14
    h_l = max(hauteur_liste(b[1], w - 0.36, D.TYPE["tiny"], gap=0.09)
              for b in d["blocs"])
    h = 0.16 + H_HEADER + h_l + 0.18
    if y2 + h > B_CONT:
        raise ValueError("volets de soutien : %.2fin sous y=%.2f, bas %.2f"
                         % (h, y2, B_CONT))
    for i, (label, items) in enumerate(d["blocs"]):
        x = L + (w + 0.25) * i
        accent = i == n - 1
        couleur = CYAN if accent else MUTED
        carte(slide, x, y2, w, h, accent=accent, couleur=couleur)
        yy = D.add_card_header(slide, x + 0.18, y2 + 0.16, w - 0.36, label,
                               couleur, size=D.TYPE["tiny"])
        liste_puces(slide, x + 0.18, yy, w - 0.36, items, couleur,
                    D.TYPE["tiny"], gap=0.09)
    return slide


# --------------------------------------------------------------------------
def construire(sortie=SORTIE):
    prs = Presentation(TEMPLATE)
    D.clear_slides(prs)
    _init_couleurs(prs)
    D.set_police(D.police_marque(prs) or D.police_theme(prs))

    # Plan arrete le 2026-09-18 : EXACTEMENT les 8 slides de la note de
    # cadrage, couverture mise a part. `slide_sommaire` et
    # `slide_preuve_recherche` sont sorties du plan sur demande (leurs
    # fonctions restent definies : les rebrancher ici suffit).
    plan = [
        slide_couverture,
        slide_contexte,             # 1 · Contexte
        slide_enjeux_octo,          # 2 · Enjeux pour OCTO
        slide_offre_douleurs,       # 3 · Offre Agentic Product Run
        slide_octo_acteur,          # 4 · OCTO acteur de la revolution IA
        slide_proposition_valeur,   # 5 · Notre proposition de valeur
        slide_comment,              # 6 · En pratique
        slide_reporting,            # 7 · Reporting
        slide_transformation,       # 8 · Ce que cela change chez nos clients
        slide_cloture,              # 9 · Next steps (+ opportunites, pitch)
    ]
    for fn in plan:
        fn(prs)

    controles = {
        "hors-cadre": D.verifier_geometrie(prs),
        # calibration explicite : la valeur par defaut (10.7) est trop
        # pessimiste pour Outfit et produit des faux positifs en cascade.
        "debordements": D.verifier_debordements_texte(prs, cpi_pessimiste=CPI_LAYOUT),
    }
    erreurs = [c for c in controles.values() if c]
    if erreurs:
        for nom, liste in controles.items():
            if liste:
                print("ECHEC %s :" % nom)
                for e in liste:
                    print("  -", e)
        raise SystemExit(1)

    prs.save(sortie)
    print("OK ->", sortie, "(%d slides)" % len(prs.slides._sldIdLst))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    out = sys.argv[1] if len(sys.argv) > 1 else SORTIE
    construire(out)
