"""Generate carpenter's plan-view sketches for the drawer organizers.

Usage: python3 build.py            -> writes drawer-<size>.svg for every layout

All dimensions are inches. Dividers are T = 1/4" (6 mm). Each layout is pure
data: groups (left -> right) of rows (back -> front) of cells. Dividers, the
dimension chains, the compartment schedule and the cut list are all derived
from it, and the script asserts the layout tiles the drawer exactly.
"""
import json
from collections import Counter
from fractions import Fraction as F

T = F(1, 4)
HEIGHT_TXT = '2 1/2" (65 mm)'

# group = (name, width, rows); row = (depth, [(label, width), ...]); width None = whole group
LAYOUTS = {
    "38x17": dict(W=F(38), D=F(17), flex=("Perfume bay (width)", "Daily drop tray (depth)"),
                  extra=[
                      '5. Watch cells: soft pillows, 3" long × 2" dia (foam rolled in the same fabric), lying front-to-back in each 3" × 4" cell.',
                      "6. Perfume: check tallest bottle vs. drawer inside height before finalising — tall bottles can lie on their side in the perfume bay.",
                  ], groups=[
        ("Perfume", F(15, 2), [(F(11), [("PERFUME", None)]), (F(23, 4), [("GROOMING", None)])]),
        ("Belts", F(37, 4), [(F(11, 2), [("BELT", F(9, 2))] * 2)] * 3),
        ("Watch / wallet", F(19, 2), [(F(4), [("WATCH", F(3))] * 3)] * 2
         + [(F(17, 2), [("WALLET", F(37, 8))] * 2)]),
        ("Sunglasses + small items", F(11), [
            (F(7, 2), [("SUNGLASSES", F(7)), ("RINGS", F(15, 4))]),
            (F(7, 2), [("SUNGLASSES", F(7)), ("CUFFLINKS", F(15, 4))]),
            (F(7, 2), [("SUNGLASSES", F(7)), ("CHAIN / BRACELET", F(15, 4))]),
            (F(23, 4), [("DAILY DROP TRAY", None)]),
        ]),
    ]),
    "31x17": dict(W=F(31), D=F(17), flex=("Perfume bay (width)", "Pens / keys cell (depth)"),
                  extra=[
                      '5. Watch cells: soft pillows, 3" long × 2" dia (foam rolled in the same fabric), lying front-to-back in each 3" × 4" cell.',
                      "6. Perfume: check tallest bottle vs. drawer inside height before finalising — tall bottles can lie on their side in the perfume bay.",
                  ], groups=[
        ("Perfume", F(15, 2), [(F(17), [("PERFUME", None)])]),
        ("Belts / ties", F(37, 4), [(F(11, 2), [("BELT / TIE", F(9, 2))] * 2)] * 3),
        ("Watch / wallet", F(19, 2), [(F(4), [("WATCH", F(3))] * 3)] * 2
         + [(F(17, 2), [("WALLET / CARDS", F(37, 8))] * 2)]),
        ("Small items", F(4), [
            (F(7, 2), [("RINGS", None)]),
            (F(7, 2), [("CUFFLINKS", None)]),
            (F(7, 2), [("TIE PIN / CLIPS", None)]),
            (F(23, 4), [("PENS / KEYS", None)]),
        ]),
    ]),
    "51x20": dict(W=F(51), D=F(20), title="DRESSING CABINET DRAWER",
                  flex=("Hair tools column (width)", "Perfume / cotton row (depth)"),
                  extra=[
                      "5. Hair tools bay: put a heat-proof silicone mat on the base; let the dryer / straightener cool before storing. Coil cords, don't wrap them tight.",
                      "6. Tall items (hair spray, toner, perfume) stand upright only if the drawer's inside height allows — otherwise lay them in the same cell.",
                  ], groups=[
        ("Hair tools", F(49, 4), [
            (F(10), [("HAIR DRYER", None)]),
            (F(19, 4), [("STRAIGHTENER", None)]),
            (F(19, 4), [("CURLER / ROUND BRUSH", None)]),
        ]),
        ("Brushes", F(37, 4), [
            (F(79, 8), [("HAIRBRUSH", F(9, 2)), ("COMBS", F(9, 2))]),
            (F(79, 8), [("MAKEUP BRUSHES", F(9, 2)), ("HAIR SPRAY / OIL", F(9, 2))]),
        ]),
        ("Skincare / makeup", F(57, 4), [
            (F(79, 8), [("SERUMS / TONER", F(7)), ("CREAMS / JARS", F(7))]),
            (F(79, 8), [("PALETTES / COMPACTS", F(9)), ("FOUNDATION", F(5))]),
        ]),
        ("Small items", F(29, 2), [
            (F(19, 4), [("LIPSTICK", F(9, 2)), ("LIPSTICK", F(9, 2)), ("NAIL POLISH", F(5))]),
            (F(19, 4), [("KAJAL / LINER", F(9, 2)), ("MASCARA", F(9, 2)), ("NAIL POLISH", F(5))]),
            (F(19, 4), [("EARRINGS", F(9, 2)), ("HAIR TIES / CLIPS", F(9, 2)), ("BINDI / PINS", F(5))]),
            (F(5), [("PERFUME / DEO", F(37, 4)), ("COTTON / BUDS", F(5))]),
        ]),
    ]),
}

HOLDS = {
    "PERFUME": "Perfume bottles, standing", "GROOMING": "Deo, trimmer, comb",
    "BELT": "1 rolled belt each", "BELT / TIE": "1 rolled belt or tie each",
    "WATCH": "1 watch on a pillow each", "WALLET": "2–3 wallets / card cases on edge",
    "WALLET / CARDS": "2–3 wallets / card cases on edge", "SUNGLASSES": "1 pair / case each",
    "RINGS": "Rings", "CUFFLINKS": "Cufflinks", "CHAIN / BRACELET": "Chain, bracelet",
    "TIE PIN / CLIPS": "Tie pins, collar stays", "PENS / KEYS": "Pens, spare keys",
    "DAILY DROP TRAY": "Keys, phone, earbuds, pen",
    "HAIR DRYER": "Hair dryer + coiled cord", "STRAIGHTENER": "Straightener, lying flat",
    "CURLER / ROUND BRUSH": "Curling iron or round brush", "HAIRBRUSH": "Paddle / hair brushes",
    "COMBS": "Combs, wide-tooth comb", "MAKEUP BRUSHES": "Makeup brushes, sponges",
    "HAIR SPRAY / OIL": "Hair spray, serum, oil", "SERUMS / TONER": "Serum, toner, face wash",
    "CREAMS / JARS": "Moisturiser, cream jars", "PALETTES / COMPACTS": "Eye palettes, compacts, blush",
    "FOUNDATION": "Foundation, primer, concealer", "LIPSTICK": "8–10 lipsticks standing",
    "NAIL POLISH": "8–10 bottles standing", "KAJAL / LINER": "Kajal, eyeliner, brow pencil",
    "MASCARA": "Mascara, lip liner", "EARRINGS": "Earrings, studs", "HAIR TIES / CLIPS": "Hair ties, clips, bands",
    "BINDI / PINS": "Bindi, safety / hair pins", "PERFUME / DEO": "Perfume, deo, body mist",
    "COTTON / BUDS": "Cotton pads, ear buds",
}
PAL = {
    "PERFUME": "#e9d5c3", "GROOMING": "#efe3d6", "BELT": "#d9e4d2", "BELT / TIE": "#d9e4d2",
    "WATCH": "#d4dfea", "WALLET": "#e8dcc0", "WALLET / CARDS": "#e8dcc0", "SUNGLASSES": "#e6d3dc",
    "DAILY DROP TRAY": "#dcdcdc", "PENS / KEYS": "#dcdcdc",
    "HAIR DRYER": "#d4dfea", "STRAIGHTENER": "#dde6ef", "CURLER / ROUND BRUSH": "#dde6ef",
    "HAIRBRUSH": "#d9e4d2", "COMBS": "#d9e4d2", "MAKEUP BRUSHES": "#e6d3dc", "HAIR SPRAY / OIL": "#d9e4d2",
    "SERUMS / TONER": "#e9d5c3", "CREAMS / JARS": "#e9d5c3", "PALETTES / COMPACTS": "#e6d3dc",
    "FOUNDATION": "#e6d3dc", "PERFUME / DEO": "#e9d5c3", "COTTON / BUDS": "#dcdcdc",
}
SMALL_COLOUR = "#f1e6c9"


def fmt(x):
    """Inches as a carpenter's fraction, e.g. 4 5/8"."""
    whole, rem = divmod(x.numerator, x.denominator)
    if rem == 0:
        return f'{whole}"'
    frac = F(rem, x.denominator)
    return f'{whole} {frac.numerator}/{frac.denominator}"' if whole else f'{frac.numerator}/{frac.denominator}"'


def solve(L):
    """Place cells and divider pieces. Returns (cells, pieces); pieces = (x, y, w, d, use)."""
    W, D, groups = L["W"], L["D"], L["groups"]
    assert sum(g[1] for g in groups) + (len(groups) - 1) * T == W, "group widths != drawer width"
    cells, pieces = [], []
    gx = F(0)
    for gi, (name, gw, rows) in enumerate(groups):
        assert sum(r[0] for r in rows) + (len(rows) - 1) * T == D, f"{name}: row depths != drawer depth"
        runs = {}  # x of an in-row divider -> [y0, y1]; aligned dividers merge through cross pieces
        y = F(0)
        for ri, (rd, row) in enumerate(rows):
            if ri:
                pieces.append((gx, y - T, gw, T, f"Cross piece – {name.lower()}"))
            widths = [w if w is not None else gw for _, w in row]
            assert sum(widths) + (len(row) - 1) * T == gw, f"{name} row {ri}: cell widths != group width"
            cx = gx
            for ci, ((label, _), w) in enumerate(zip(row, widths)):
                if ci:
                    dx = cx - T
                    if dx in runs and runs[dx][1] == y - T:
                        runs[dx][1] = y + rd
                    else:
                        if dx in runs:
                            pieces.append((dx, runs[dx][0], T, runs[dx][1] - runs[dx][0], f"{name} cell dividers"))
                        runs[dx] = [y, y + rd]
                cells.append((cx, y, w, rd, label))
                cx += w + T
            y += rd + T
        for dx, (y0, y1) in runs.items():
            pieces.append((dx, y0, T, y1 - y0, f"{name} cell dividers"))
        gx += gw
        if gi < len(groups) - 1:
            pieces.append((gx, F(0), T, D, "Main long dividers (full depth)"))
            gx += T

    # cells + dividers must tile the drawer exactly. Crossing dividers share a T x T square
    # (the halving joint); any other overlap is an error.
    def overlap(a, b):
        ox = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
        oy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
        return ox * oy if ox > 0 and oy > 0 else 0

    rects = [c[:4] for c in cells] + [p[:4] for p in pieces]
    shared = F(0)
    for i, a in enumerate(rects):
        for j in range(i + 1, len(rects)):
            o = overlap(a, rects[j])
            assert not o or (i >= len(cells) and o == T * T), ("overlap", a, rects[j])
            shared += o
    assert sum(r[2] * r[3] for r in rects) - shared == W * D, "gaps in layout"
    return cells, pieces


def render(size, L):
    W, D, groups = L["W"], L["D"], L["groups"]
    cells, pieces = solve(L)
    S = F(1290) / W                  # px per inch: the plan is always ~1290 px wide
    f = lambda v: float(v * S)
    OX, OY, PW = 110, 260, 1520
    plan_bottom = OY + f(D)
    TY = plan_bottom + 90
    out = []
    a = out.append

    def text(x, y, s, size=14, weight=400, anchor="start", fill="#222", extra=""):
        a(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
          f'fill="{fill}" {extra}>{s}</text>')

    def dim_h(x1, x2, y, s, fs=13):
        a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#222" marker-start="url(#ar)" marker-end="url(#ar)"/>')
        text((x1 + x2) / 2, y - 6, s, fs, anchor="middle", fill="#111")

    def dim_v(y1, y2, x, s, fs=13):
        a(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#222" marker-start="url(#ar)" marker-end="url(#ar)"/>')
        cx, cy = x - 7, (y1 + y2) / 2
        text(cx, cy, s, fs, anchor="middle", fill="#111", extra=f'transform="rotate(-90 {cx} {cy})"')

    def ext(x1, y1, x2, y2):
        a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#888" stroke-width="0.7" stroke-dasharray="3 3"/>')

    # schedule + cut list first, so the page height is known
    sched = Counter((c[4], c[2], c[3]) for c in cells)
    cut = Counter((p[2] if p[3] == T else p[3], p[4]) for p in pieces)
    cut_rows = sorted(cut.items(), key=lambda kv: -kv[0][0])
    run_ft = sum(k[0] * n for k, n in cut.items()) / 12
    NY = TY + 130 + max(len(sched), len(cut_rows)) * 25
    notes = [
        f"1. MEASURE FIRST: confirm the drawer's clear inside size is {fmt(W)} × {fmt(D)}. If it differs, keep every cell size above and absorb the",
        f"    difference in the {L['flex'][0]} and the {L['flex'][1]} — those are the only two flexible compartments.",
        "2. Dividers: 6 mm plywood / MDF with white laminate or edge-banding to match the drawer (or 4–5 mm acrylic). Height 65 mm — keep ≥ 25 mm clear under the drawer above.",
        "3. Joints: where two dividers cross, cut half-depth slots (egg-crate / halving joint) so the grid drops in as one removable unit. Cut each piece ~1 mm short for easy fit.",
        "4. Lining: glue 2–3 mm velvet / suede sheet on the drawer base (like the sample photo) so nothing scratches or slides.",
    ] + L["extra"]
    PH = int(NY + 30 + len(notes) * 23 + 40)

    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}" '
      'font-family="Helvetica, Arial, sans-serif">')
    a('<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" '
      'orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="#222"/></marker></defs>')
    a(f'<rect width="{PW}" height="{PH}" fill="#fff"/>')
    text(110, 60, f"{L.get('title', 'DRAWER ORGANIZER')} {fmt(W)} × {fmt(D)} — PARTITION LAYOUT (TOP VIEW)", 30, 700, fill="#111")
    text(110, 92, f"Inside drawer: {fmt(W)} W × {fmt(D)} D  ·  Dividers: 1/4\" (6 mm) thick × {HEIGHT_TXT} high  ·  "
         "All sizes are CLEAR inside sizes", 17, fill="#444")

    # drawer, cells, dividers
    wall = float(S) / 2
    a(f'<rect x="{OX - wall}" y="{OY - wall}" width="{f(W) + 2 * wall}" height="{f(D) + 2 * wall}" '
      'fill="#bdbdbd" stroke="#333" stroke-width="2"/>')
    a(f'<rect x="{OX}" y="{OY}" width="{f(W)}" height="{f(D)}" fill="#fafafa" stroke="#333" stroke-width="1.5"/>')
    for cx, cy, cw, cd, label in cells:
        X, Y, Wp, Hp = OX + f(cx), OY + f(cy), f(cw), f(cd)
        a(f'<rect x="{X}" y="{Y}" width="{Wp}" height="{Hp}" fill="{PAL.get(label, SMALL_COLOUR)}"/>')
        fs = 14 if Wp >= 140 else 12 if Wp >= 110 else 11
        name = [label]
        if Wp < 150 and " / " in label:
            name = label.split(" / ")
            name[0] += " /"
        elif len(label) * fs * 0.68 > Wp - 10 and " " in label:
            name = label.split(" ", 1)
        lines = name + [f"{fmt(cw)} × {fmt(cd)}"]
        y0 = Y + Hp / 2 - (len(lines) - 1) * fs * 0.62
        for k, line in enumerate(lines):
            text(X + Wp / 2, y0 + k * fs * 1.25, line, fs, 700 if k < len(lines) - 1 else 400,
                 "middle", extra='dominant-baseline="middle"')
    for px, py, pw, pd, _ in pieces:
        a(f'<rect x="{OX + f(px)}" y="{OY + f(py)}" width="{f(pw)}" height="{f(pd)}" fill="#5a4636"/>')

    # dimension chains: top = back-row cells, sides = rows of first / last group
    top1, top2 = OY - 45, OY - 85
    for cx, cy, cw, cd, _ in cells:
        if cy == 0:
            ext(OX + f(cx), OY - 20, OX + f(cx), top1 - 8)
            ext(OX + f(cx + cw), OY - 20, OX + f(cx + cw), top1 - 8)
            dim_h(OX + f(cx), OX + f(cx + cw), top1, fmt(cw))
    dim_h(OX, OX + f(W), top2, f"OVERALL INSIDE WIDTH {fmt(W)} ({round(W * F(254, 10))} mm)", 15)
    for gi, xpos in ((0, OX - 40), (-1, OX + f(W) + 40)):
        y = F(0)
        for rd, _ in groups[gi][2]:
            dim_v(OY + f(y), OY + f(y + rd), xpos, fmt(rd))
            y += rd + T
    dim_v(OY, plan_bottom, OX + f(W) + 85, f"OVERALL INSIDE DEPTH {fmt(D)} ({round(D * F(254, 10))} mm)", 15)
    text(OX + f(W) / 2, OY - 108, "▲ BACK OF DRAWER", 14, anchor="middle", fill="#666", extra='letter-spacing="3"')
    text(OX + f(W) / 2, plan_bottom + 45, "▼ FRONT OF DRAWER (HANDLE SIDE — YOU STAND HERE)", 14,
         anchor="middle", fill="#666", extra='letter-spacing="3"')

    # compartment schedule
    text(110, TY, f"COMPARTMENT SCHEDULE ({len(cells)} compartments)", 20, 700, fill="#111")
    for cx, h in zip([110, 390, 450, 610], ["Compartment", "Qty", "Clear size (W × D)", "Holds"]):
        text(cx, TY + 34, h, 14, 700, fill="#333")
    a(f'<line x1="110" y1="{TY + 42}" x2="860" y2="{TY + 42}" stroke="#333"/>')
    for r, ((label, w, d), n) in enumerate(sched.items()):
        for cx, v in zip([110, 390, 450, 610], [label.title(), n, f"{fmt(w)} × {fmt(d)}", HOLDS[label]]):
            text(cx, TY + 64 + r * 25, v)

    # cut list
    CX = 920
    text(CX, TY, f"CUT LIST — {sum(cut.values())} pieces", 20, 700, fill="#111")
    for cx, h in zip([CX, CX + 90, CX + 140], ["Length", "Qty", "Use"]):
        text(cx, TY + 34, h, 14, 700, fill="#333")
    a(f'<line x1="{CX}" y1="{TY + 42}" x2="{PW - 60}" y2="{TY + 42}" stroke="#333"/>')
    for r, ((ln, use), n) in enumerate(cut_rows):
        for cx, v in zip([CX, CX + 90, CX + 140], [fmt(ln), n, use]):
            text(cx, TY + 64 + r * 25, v)
    text(CX, TY + 68 + len(cut_rows) * 25, f"All strips 1/4\" (6 mm) thick × {HEIGHT_TXT} high · "
         f"total ≈ {round(run_ft)} ft running length", 13, fill="#555")

    text(110, NY, "NOTES FOR CARPENTER", 20, 700, fill="#111")
    for k, n in enumerate(notes):
        text(110, NY + 30 + k * 23, n, extra='xml:space="preserve"')
    a("</svg>")

    with open(f"layout-{size}.json", "w") as fh:  # geometry for the 3D render
        json.dump({"W": float(W), "D": float(D), "T": float(T), "H": 2.5,
                   "cells": [[float(v) for v in c[:4]] + [c[4]] for c in cells],
                   "pieces": [[float(v) for v in p[:4]] for p in pieces]}, fh)
    with open(f"drawer-{size}.svg", "w") as fh:
        fh.write("\n".join(out))
    print(f"drawer-{size}: {len(cells)} compartments, {sum(cut.values())} pieces, "
          f"{float(run_ft):.1f} ft, page {PW}x{PH} — tiling verified")
    for (ln, use), n in cut_rows:
        print(f"   {fmt(ln):>8} x{n}  {use}")
    return PH


if __name__ == "__main__":
    heights = {size: render(size, L) for size, L in LAYOUTS.items()}
    with open("sizes.json", "w") as fh:
        json.dump(heights, fh)
