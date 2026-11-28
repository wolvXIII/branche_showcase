#!/usr/bin/env python3
"""Injecte les modèles de svg/ dans index.html, sous forme de <symbol> colorables.

À lancer après avoir modifié un fichier de svg/ dans Inkscape :

    python3 tools/build-svg.py

Un calque nommé dans Inkscape devient une zone : son remplissage passe à
var(--zone-<nom>), ce qui permet à la page de le colorer. Les calques à
reprendre sont listés dans ZONES ci-dessous — en ajouter un ici suffit à le
rendre personnalisable, à condition que le calque porte ce nom dans le fichier.

Les <symbol> restent dans index.html parce qu'un SVG chargé depuis un fichier
séparé n'hérite pas des variables CSS de la page : il ne serait pas colorable.
"""
import re
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCES = RACINE / "svg"
PAGE = RACINE / "index.html"

# Les modèles sans zone colorable : nettoyés et inlinés tels quels.
SANS_ZONE = ["logo"]

# Les calques pilotables, par fichier. Le nom doit correspondre à l'étiquette
# du calque dans Inkscape (Objet > Propriétés de l'objet).
ZONES = {
    "pouch": ["grande partie", "petite partie", "chapeau", "sangle noire"],
    "banane": ["face haut", "face bas", "haut", "dessous", "ailes",
               "face cachée", "zip haut", "sangle ventrale"],
    "portefeuille": ["extérieur 1", "extérieur 2", "intérieur"],
}

DECIMALES = 2


def slug(etiquette):
    sans_accent = "".join(c for c in unicodedata.normalize("NFKD", etiquette)
                          if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", sans_accent.lower()).strip("-")


def peindre(balise, zone):
    """Remplace le fill du calque par la variable CSS de sa zone."""
    style = re.search(r'style="([^"]*)"', balise)
    if not style:
        return balise
    # Un calque peint par un <pattern> se pilote via le pattern, pas ici :
    # écraser son fill supprimerait le motif.
    if not re.search(r"fill:\s*url\(", balise):
        peint = re.sub(r"fill:\s*[^;\"]+", f"fill:var(--zone-{zone})", style.group(1), count=1)
        balise = balise.replace(style.group(0), f'style="{peint}"')
    return balise.replace("<path", f'<path data-zone="{zone}"', 1)


def nettoyer(svg, prefixe):
    """Retire ce qu'Inkscape ajoute pour son propre usage et raccourcit les nombres."""
    svg = re.sub(r"<(sodipodi:namedview|metadata)\b.*?</\1>", "", svg, flags=re.S)
    svg = re.sub(r"<(sodipodi:namedview|metadata)\b[^>]*/>", "", svg, flags=re.S)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    for p in ("inkscape", "sodipodi"):
        # Ces éléments n'ont aucun effet au rendu, et leur préfixe n'est pas
        # déclaré une fois le SVG inliné : il rendrait le document invalide.
        svg = re.sub(rf"<{p}:[\w-]+\b.*?</{p}:[\w-]+>", "", svg, flags=re.S)
        svg = re.sub(rf"<{p}:[\w-]+\b[^>]*/>", "", svg, flags=re.S)
        svg = re.sub(rf'\s{p}:[\w-]+="[^"]*"', "", svg)
    svg = re.sub(r'\sid="(path|rect|g)[\w.-]*"', "", svg)
    svg = re.sub(r"(\d+\.\d{%d})\d+" % DECIMALES, r"\1", svg)
    svg = svg.replace("xlink:href=", "href=")
    # Les id des defs sont partagés entre les trois fichiers : on les préfixe.
    for ident in re.findall(r'\sid="([^"]+)"', svg):
        svg = svg.replace(f'id="{ident}"', f'id="{prefixe}-{ident}"')
        svg = svg.replace(f"#{ident}", f"#{prefixe}-{ident}")
    return svg


def cadrer(svg):
    """Recadre le viewBox A4 d'Inkscape sur le dessin, transformations comprises."""
    from bbox import boite_englobante  # noqa: E402
    x0, y0, x1, y1 = boite_englobante(svg)
    marge = max(x1 - x0, y1 - y0) * 0.03
    largeur, hauteur = x1 - x0 + 2 * marge, y1 - y0 + 2 * marge
    # Le <symbol> définit son propre repère : on décale le dessin à l'origine.
    decalage = f"translate({marge - x0:.2f},{marge - y0:.2f})"
    return f"0 0 {largeur:.2f} {hauteur:.2f}", decalage


def construire_simple(nom):
    """Un dessin sans zone : on le nettoie et on le recadre, sans le repeindre."""
    svg = (SOURCES / f"{nom}.svg").read_text(encoding="utf-8")
    # Le manifeste C2PA ajouté à l'export n'a aucun effet au rendu.
    svg = re.sub(r"<metadata\b.*?</metadata>", "", svg, flags=re.S)
    # Le fond plein de la planche Inkscape : le logo se pose sur le bandeau.
    svg = re.sub(r'<rect\b[^>]*fill:#00000b[^>]*/>', "", svg)
    svg = nettoyer(svg, nom)
    viewbox = re.search(r'viewBox="([^"]*)"', svg).group(1)
    corps = re.sub(r"^.*?<svg[^>]*>", "", svg, count=1, flags=re.S)
    corps = re.sub(r"</svg>\s*$", "", corps)
    corps = re.sub(r"<defs\b.*?</defs>", "", corps, flags=re.S)
    corps = re.sub(r"\n\s*\n+", "\n", corps).strip()
    return f'<symbol id="modele-{nom}" viewBox="{viewbox}">{corps}</symbol>', "", viewbox


def construire(nom):
    svg = (SOURCES / f"{nom}.svg").read_text(encoding="utf-8")
    attendus = {z: slug(z) for z in ZONES[nom]}
    trouves = set()

    def sur_chemin(m):
        balise = m.group(0)
        etiquette = re.search(r'inkscape:label="([^"]*)"', balise)
        if not etiquette or etiquette.group(1) not in attendus:
            return balise
        zone = attendus[etiquette.group(1)]
        trouves.add(etiquette.group(1))
        return peindre(balise, zone)

    svg = re.sub(r"<path\b[^>]*?>", sur_chemin, svg, flags=re.S)

    # Le chapeau de la pouch est peint par un pattern : c'est lui qu'on pilote.
    def sur_pattern(m):
        balise = m.group(0)
        if 'inkscape:label="Inverted grid"' not in balise:
            return balise
        style = re.search(r'style="([^"]*)"', balise)
        if not style:
            return balise
        peint = re.sub(r"fill:\s*[^;\"]+", "fill:var(--zone-chapeau)", style.group(1), count=1)
        return balise.replace(style.group(0), f'style="{peint}"')

    svg = re.sub(r"<pattern\b[^>]*?>", sur_pattern, svg, flags=re.S)

    manquants = set(ZONES[nom]) - trouves
    if manquants:
        raise SystemExit(f"{nom}.svg : calque introuvable — {sorted(manquants)}")

    svg = nettoyer(svg, nom)
    viewbox, decalage = cadrer(svg)

    defs = "".join(re.findall(r"<defs\b.*?</defs>", svg, re.S))
    corps = re.sub(r"<defs\b.*?</defs>", "", svg, flags=re.S)
    corps = re.sub(r"^.*?<svg[^>]*>", "", corps, count=1, flags=re.S)
    corps = re.sub(r"</svg>\s*$", "", corps)
    corps = re.sub(r"\n\s*\n+", "\n", corps).strip()

    contenu_defs = re.sub(r"</?defs[^>]*>", "", defs, flags=re.S).strip()
    symbol = (f'<symbol id="modele-{nom}" viewBox="{viewbox}">'
              f'<g transform="{decalage}">{corps}</g></symbol>')
    return symbol, contenu_defs, viewbox


def main():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))

    symboles, defs_partages, viewbox_par_modele = [], [], {}
    for nom in list(ZONES) + SANS_ZONE:
        symbole, defs, viewbox = (construire_simple(nom) if nom in SANS_ZONE
                                  else construire(nom))
        symboles.append(symbole)
        if defs:
            defs_partages.append(defs)
        viewbox_par_modele[nom] = viewbox
        print(f"  {nom:14} {len(symbole):>6} octets   viewBox={viewbox}")

    bloc = ('<svg class="u-hidden" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
            f'<defs>{"".join(defs_partages)}</defs>{"".join(symboles)}</svg>')

    page = PAGE.read_text(encoding="utf-8")
    page = re.sub(r'<svg class="u-hidden".*?</svg>', lambda _: bloc, page, count=1, flags=re.S)
    for nom, viewbox in viewbox_par_modele.items():
        page = re.sub(
            r'(<svg class="c-(?:card|panneau)__svg" viewBox=")[^"]*("[^>]*><use href="#modele-'
            + nom + r'")',
            lambda m: m.group(1) + viewbox + m.group(2), page)
    PAGE.write_text(page, encoding="utf-8")
    print(f"\nindex.html mis à jour ({len(page)} octets)")


if __name__ == "__main__":
    main()
