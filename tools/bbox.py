"""Boîte englobante d'un SVG, transformations comprises.

Les chemins Inkscape mêlent commandes absolues et relatives, et les groupes du logo
portent des transformations qui ramènent dans le cadre des coordonnées très éloignées.
Il faut donc dérouler les commandes ET composer les matrices, sinon la bbox est fausse.
Référence de validation : le portefeuille mesuré au navigateur (getBBox) donne
x=25.11 y=78.48 w=150.15 h=108.54.
"""
import re
from pathlib import Path

NUM = re.compile(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?")
CMD = re.compile(r"([MmZzLlHhVvCcSsQqTtAa])([^MmZzLlHhVvCcSsQqTtAa]*)")
ARGC = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}

IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def multiply(m, n):
    a1, b1, c1, d1, e1, f1 = m
    a2, b2, c2, d2, e2, f2 = n
    return (
        a1 * a2 + c1 * b2,
        b1 * a2 + d1 * b2,
        a1 * c2 + c1 * d2,
        b1 * c2 + d1 * d2,
        a1 * e2 + c1 * f2 + e1,
        b1 * e2 + d1 * f2 + f1,
    )


def apply(m, x, y):
    a, b, c, d, e, f = m
    return a * x + c * y + e, b * x + d * y + f


def parse_transform(text):
    matrix = IDENTITY
    for name, raw in re.findall(r"(\w+)\s*\(([^)]*)\)", text or ""):
        v = [float(n) for n in NUM.findall(raw)]
        if name == "matrix" and len(v) == 6:
            m = tuple(v)
        elif name == "translate":
            m = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == "scale":
            sx = v[0]
            sy = v[1] if len(v) > 1 else sx
            m = (sx, 0, 0, sy, 0, 0)
        else:
            continue
        matrix = multiply(matrix, m)
    return matrix


def path_points(d):
    pts = []
    x = y = start_x = start_y = 0.0
    for letter, raw in CMD.findall(d):
        up = letter.upper()
        rel = letter.islower()
        nums = [float(n) for n in NUM.findall(raw)]
        n = ARGC[up]
        if n == 0:
            x, y = start_x, start_y
            continue
        for i in range(0, len(nums) - n + 1, n):
            args = nums[i:i + n]
            if up == "H":
                x = x + args[0] if rel else args[0]
            elif up == "V":
                y = y + args[0] if rel else args[0]
            elif up == "A":
                nx, ny = args[5], args[6]
                x, y = (x + nx, y + ny) if rel else (nx, ny)
            else:
                for cx, cy in zip(args[0::2], args[1::2]):
                    px, py = (x + cx, y + cy) if rel else (cx, cy)
                    pts.append((px, py))
                nx, ny = args[-2], args[-1]
                x, y = (x + nx, y + ny) if rel else (nx, ny)
            pts.append((x, y))
            if up == "M":
                start_x, start_y = x, y
    return pts


TOKEN = re.compile(r"<(/?)(\w+)([^>]*?)(/?)>", re.S)


def boite_englobante(svg_text):
    body = re.sub(r"<defs\b.*?</defs>", "", svg_text, flags=re.S)
    stack = [IDENTITY]
    xs, ys = [], []
    for closing, tag, attrs, self_closing in TOKEN.findall(body):
        if closing:
            if tag in ("g", "svg") and len(stack) > 1:
                stack.pop()
            continue
        tr = re.search(r'transform="([^"]*)"', attrs)
        matrix = multiply(stack[-1], parse_transform(tr.group(1))) if tr else stack[-1]
        if tag == "path":
            d = re.search(r'\sd="([^"]+)"', attrs)
            if d:
                for px, py in path_points(d.group(1)):
                    tx, ty = apply(matrix, px, py)
                    xs.append(tx)
                    ys.append(ty)
        if tag in ("g", "svg") and not self_closing:
            stack.append(matrix)
    return min(xs), min(ys), max(xs), max(ys)
