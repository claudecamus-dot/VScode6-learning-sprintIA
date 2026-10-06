"""Code commun aux deux generateurs de deck (`generer_deck.py` et
`atelier-agentic-run/generer_deck.py`).

Constat d'audit (duplication structurelle) : modele de hauteur, typographie
francaise, constantes de grille et bandeau de cloture etaient recopies a
l'identique dans les deux fichiers. Ils vivent ici, une seule fois ; les deux
generateurs les importent. Seul ce qui est STRICTEMENT identique est partage :
les composants qui different volontairement (cartes, listes, photos, filets)
restent dans chaque generateur.

Les fonctions dependantes de `pptx_deck` (skill du kit) et de la separation
typographique sont portees par `Commun(D, sep)` : une instance PAR generateur,
car les deux modules peuvent etre charges dans le meme processus (tests).
"""
import re

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

# --- grille (inches) ---------------------------------------------------------
L = 0.615            # marge gauche = left du placeholder titre du layout 5
R = 9.15             # bord droit utile : le badge de pagination commence a 9.25
CW = R - L           # 8.535 in
T_CLAIM = 0.86       # sous le placeholder titre (0.395 -> 0.801)
T_CONT = 1.28        # haut de la bande de contenu
B_CONT = 5.25        # bas utile
LAYOUT_COUVERTURE = 8
LAYOUT_TITRE_SEUL = 5
# Calibration MESUREE sur un rendu PowerPoint reel du template (police Outfit,
# 2026-09-17) : 56 caracteres tenaient sur 3.78in a 10.5pt, soit ~14.8 car./pouce,
# la ou la valeur par defaut de pptx_deck (10.7) en predisait 40.
CPI_LAYOUT = 14.0
# Hauteur de ligne mesuree au meme rendu : ~0.19in a 10.5pt interligne 1.1.
COEF_LIGNE = 0.0185
PAD_BOITE = 0.06
# Hauteur reellement consommee par D.add_card_header (libelle + filet d'accent).
H_HEADER = 0.545
RETRAIT_BANDEAU = 0.62

NBSP = "\u00a0"


class Commun:
    """Fonctions partagees, liees a un module `pptx_deck` (D) et a la chaine
    inseree devant la ponctuation haute (`sep`).

    Les deux generateurs utilisent le defaut (U+00A0) ; `sep` reste un reglage
    par instance (voir tests/test_deck_commun.py).
    """

    def __init__(self, D, sep=NBSP):
        self.D = D
        self.sep = sep

    def couleurs(self, prs):
        """(THEME, NAVY, CYAN, MUTED, LINE, BG, SLATE) lus dans le theme."""
        theme = self.D.theme_colors(prs)
        return (theme,
                theme.get("dk1", "#0E2356"),
                theme.get("accent3", "#00D2DD"),
                theme.get("lt2", "#586586"),
                theme.get("accent5", "#CFD3DD"),
                theme.get("accent6", "#E7E9EE"),
                theme.get("dk2", "#3E4F78"))

    def typo_fr(self, texte):
        """Espace insecable devant la ponctuation haute et avant « % ».

        Deux effets : la typographie francaise est respectee, et PowerPoint cesse
        de rejeter un « ? » orphelin sur sa propre ligne (constat du 2026-09-17).
        """
        if not isinstance(texte, str):
            return texte
        return re.sub(r" (?=[?!:;%])", self.sep, texte)

    def nlignes(self, texte, w, size):
        return self.D.estimer_lignes(texte, w, size, cpi_ref=CPI_LAYOUT)

    def hbox(self, texte, w, size):
        """Hauteur de boite suffisante pour `texte` a `size` pt sur `w` pouces."""
        return self.nlignes(texte, w, size) * lh(size) + PAD_BOITE

    def hbox_max(self, textes, w, size):
        return max(self.hbox(t, w, size) for t in textes)

    def hauteur_bandeau(self, texte, size=13.5):
        return (self.nlignes(self.typo_fr(texte), CW - 2 * RETRAIT_BANDEAU, size)
                * lh(size) + 0.17)

    def bandeau(self, slide, bas, texte, navy, cyan, size=13.5):
        """Bandeau de cloture, dimensionne sur SON texte puis cale en bas de bande.

        `D.add_quote_banner` place son texte a +0.20in seulement : la premiere
        ligne marcherait sur le guillemet decoratif ; on redessine donc avec un
        retrait symetrique (RETRAIT_BANDEAU). La hauteur se calcule, elle ne se
        pose pas.
        """
        D = self.D
        texte = self.typo_fr(texte)
        h = self.hauteur_bandeau(texte, size)
        y = B_CONT - h
        if y < bas + 0.10:
            raise ValueError(
                "bandeau de %.2fin ne tient pas sous y=%.2f (bas de bande %.2f)"
                % (h, bas, B_CONT))
        D.add_rect(slide, L, y, CW, h, fill=navy, rounded=True, radius=0.10)
        D.add_text(slide, L + 0.16, y + 0.02, 0.40, min(0.40, h - 0.04),
                   [("“", {"size": 24, "bold": True, "color": cyan})])
        D.add_text_runs(slide, L + RETRAIT_BANDEAU, y, CW - 2 * RETRAIT_BANDEAU, h,
                        [([(texte, {"size": size, "bold": True, "color": "#FFFFFF"}),
                           ("  •", {"size": size, "bold": True, "color": cyan})],
                          {"align": PP_ALIGN.CENTER})],
                        anchor=MSO_ANCHOR.MIDDLE)


def lh(size):
    return size * COEF_LIGNE


def reste(bas, souhaite, mini=0.30):
    """Hauteur disponible entre `bas` et le bas de bande, bornee par `souhaite`.

    Leve si le contenu a deja mange la bande : une hauteur negative produit une
    forme invalide que python-pptx accepte et que PowerPoint refuse d'ouvrir
    (HRESULT 0x80070570).
    """
    dispo = B_CONT - bas
    if dispo < mini:
        raise ValueError(
            "bande de contenu saturee : %.2fin disponibles sous y=%.2f "
            "(minimum %.2f) — raccourcir le contenu ou reduire les blocs"
            % (dispo, bas, mini))
    return min(souhaite, dispo)
