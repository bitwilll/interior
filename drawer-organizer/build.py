"""Generate the carpenter's plan-view sketch for the 38" x 17" drawer organizer.

All dimensions are inches. Dividers are T = 1/4" (6 mm). The layout is defined
once below; the script asserts every column/row adds up to the drawer size,
then writes drawer-organizer.svg.
"""
from fractions import Fraction as F

W, D, T = F(38), F(17), F(1, 4)
HEIGHT = '2½" (65 mm)'

# Columns left -> right: (key, clear width, [(label, clear depth), ...] back -> front)
COLS = [
    ("A", F(15, 2), [("PERFUME", F(11)), ("GROOMING", F(23, 4))]),
    ("B", F(37, 4), None),   # belts: 2 x 3 grid, built below
    ("C", F(19, 2), None),   # watches + wallets, built below
    ("D", F(7), [("SUNGLASSES", F(7, 2))] * 3),
    ("E", F(15, 4), [("RINGS", F(7, 2)), ("CUFFLINKS", F(7, 2)), ("CHAIN / BRACELET", F(7, 2))]),
]
DROP_DEPTH = F(23, 4)  # daily drop tray spans columns D + E at the front


def fmt(x):
    """Inches as carpenter fraction, e.g. 4 5/8"."""
    x = F(x)
    whole, rem = divmod(x.numerator, x.denominator)
    frac = F(rem, x.denominator)
    if frac == 0:
        return f'{whole}"'
    return f'{whole} {frac.numerator}/{frac.denominator}"' if whole else f'{frac.numerator}/{frac.denominator}"'


def mm(x):
    return f"{round(float(x) * 25.4)} mm"


# ---- build cell list: (x, y, w, d, label, colour) --------------------------
cells, dividers = [], []  # dividers: (x, y, w, d)
PAL = {
    "PERFUME": "#e9d5c3", "GROOMING": "#efe3d6", "BELT": "#d9e4d2", "WATCH": "#d4dfea",
    "WALLET": "#e8dcc0", "SUNGLASSES": "#e6d3dc", "RINGS": "#f1e6c9", "CUFFLINKS": "#f1e6c9",
    "CHAIN / BRACELET": "#f1e6c9", "DAILY DROP TRAY": "#dcdcdc",
}

x = F(0)
for i, (key, cw, rows) in enumerate(COLS):
    if key == "B":  # belts 2 x 3
        bw = (cw - T) / 2
        bd = (D - 2 * T) / 3
        assert bw == F(9, 2) and bd == F(11, 2)
        dividers.append((x + bw, 0, T, D))
        for r in range(3):
            y = r * (bd + T)
            if r:
                dividers.append((x, y - T, cw, T))
            for c in range(2):
                cells.append((x + c * (bw + T), y, bw, bd, "BELT"))
    elif key == "C":  # 2 rows x 3 watches, then 2 wallet bays
        ww, wd = F(3), F(4)
        assert 3 * ww + 2 * T == cw
        for r in range(2):
            y = r * (wd + T)
            if r:
                dividers.append((x, y - T, cw, T))
            for c in range(3):
                cells.append((x + c * (ww + T), y, ww, wd, "WATCH"))
        for c in (1, 2):
            dividers.append((x + c * ww + (c - 1) * T, 0, T, 2 * wd + T))
        y0 = 2 * wd + 2 * T
        dividers.append((x, y0 - T, cw, T))
        lw = (cw - T) / 2
        dividers.append((x + lw, y0, T, D - y0))
        for c in range(2):
            cells.append((x + c * (lw + T), y0, lw, D - y0, "WALLET"))
    else:
        y = F(0)
        for j, (label, d) in enumerate(rows):
            if j:
                dividers.append((x, y - T, cw, T))
            cells.append((x, y, cw, d, label))
            y += d + T
        if key in ("D", "E"):  # last divider before the shared drop tray
            dividers.append((x, y - T, cw + (T if key == "D" else 0), T))
            assert y + DROP_DEPTH == D, (key, y)
        else:
            assert y - T == D, (key, y)
    x += cw
    if i < len(COLS) - 1:
        dividers.append((x, 0, T, D if key != "D" else D - DROP_DEPTH - T))
        x += T
assert x == W, x
dx = sum(c[1] for c in COLS[:3]) + 3 * T  # left edge of column D
cells.append((dx, D - DROP_DEPTH, W - dx, DROP_DEPTH, "DAILY DROP TRAY"))

# overlap / coverage check: cells + dividers must tile the drawer exactly
area = sum(c[2] * c[3] for c in cells) + sum(d[2] * d[3] for d in dividers)
crossings = F(0)
for i, a in enumerate(dividers):
    for b in dividers[i + 1:]:
        ox = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
        oy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
        if ox > 0 and oy > 0:
            crossings += ox * oy
assert area - crossings == W * D, (area, crossings)

# ---- SVG ------------------------------------------------------------------
S = 34              # px per inch
OX, OY = 110, 260   # drawing origin (back-left inner corner)
PW, PH = 1520, 1500
f = lambda v: float(v) * S
out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}" '
  'font-family="Helvetica, Arial, sans-serif">')
a('<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
  '<path d="M0,1 L9,5 L0,9 z" fill="#222"/></marker></defs>')
a(f'<rect width="{PW}" height="{PH}" fill="#fff"/>')
a('<text x="110" y="60" font-size="30" font-weight="700" fill="#111">DRAWER ORGANIZER — PARTITION LAYOUT (TOP VIEW)</text>')
a(f'<text x="110" y="92" font-size="17" fill="#444">Inside drawer: 38" W × 17" D  ·  Dividers: 1/4" (6 mm) thick × {HEIGHT} high  ·  '
  'All sizes are CLEAR inside sizes</text>')

# drawer walls
wt = 0.5
a(f'<rect x="{OX - wt*S}" y="{OY - wt*S}" width="{f(W) + 2*wt*S}" height="{f(D) + 2*wt*S}" fill="#bdbdbd" stroke="#333" stroke-width="2"/>')
a(f'<rect x="{OX}" y="{OY}" width="{f(W)}" height="{f(D)}" fill="#fafafa" stroke="#333" stroke-width="1.5"/>')

for (cx, cy, cw, cd, label) in cells:
    X, Y, Wp, Hp = OX + f(cx), OY + f(cy), f(cw), f(cd)
    a(f'<rect x="{X}" y="{Y}" width="{Wp}" height="{Hp}" fill="{PAL[label]}"/>')
    mx, my = X + Wp / 2, Y + Hp / 2
    small = Wp < 110
    fs = 11 if small else 14
    name = label if not (small and "/" in label) else label.replace(" / ", "/")
    lines = [name, f"{fmt(cw)} × {fmt(cd)}"]
    if label == "CHAIN / BRACELET":
        lines = ["CHAIN /", "BRACELET", lines[1]]
    if label in ("RINGS", "CUFFLINKS", "CHAIN / BRACELET", "WATCH"):
        fs = 11
    y0 = my - (len(lines) - 1) * fs * 0.62
    for k, line in enumerate(lines):
        weight = 700 if k < len(lines) - 1 else 400
        a(f'<text x="{mx}" y="{y0 + k * fs * 1.25}" font-size="{fs}" font-weight="{weight}" text-anchor="middle" '
          f'dominant-baseline="middle" fill="#222">{line}</text>')

for (dx_, dy_, dw, dd) in dividers:
    a(f'<rect x="{OX + f(dx_)}" y="{OY + f(dy_)}" width="{f(dw)}" height="{f(dd)}" fill="#5a4636"/>')


def dim_h(x1, x2, y, text, fs=13):
    a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#222" stroke-width="1" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    a(f'<text x="{(x1 + x2) / 2}" y="{y - 6}" font-size="{fs}" text-anchor="middle" fill="#111">{text}</text>')


def dim_v(y1, y2, x, text, fs=13):
    a(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#222" stroke-width="1" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    cx, cy = x - 7, (y1 + y2) / 2
    a(f'<text x="{cx}" y="{cy}" font-size="{fs}" text-anchor="middle" fill="#111" transform="rotate(-90 {cx} {cy})">{text}</text>')


def ext(x1, y1, x2, y2):
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#888" stroke-width="0.7" stroke-dasharray="3 3"/>')


# top: column chain + overall
top1, top2 = OY - 45, OY - 85
x = F(0)
for i, (key, cw, _) in enumerate(COLS):
    ext(OX + f(x), OY - 20, OX + f(x), top1 - 8)
    ext(OX + f(x + cw), OY - 20, OX + f(x + cw), top1 - 8)
    dim_h(OX + f(x), OX + f(x + cw), top1, fmt(cw))
    x += cw + T
dim_h(OX, OX + f(W), top2, 'OVERALL INSIDE WIDTH 38" (965 mm)', 15)

# left: column A rows; right: column D/E rows; overall depth far right
lx = OX - 40
dim_v(OY, OY + f(11), lx, fmt(11))
dim_v(OY + f(11 + T), OY + f(D), lx, fmt(F(23, 4)))
rx = OX + f(W) + 40
y = F(0)
for d in (F(7, 2), F(7, 2), F(7, 2), DROP_DEPTH):
    dim_v(OY + f(y), OY + f(y + d), rx, fmt(d))
    y += d + T
dim_v(OY, OY + f(D), rx + 45, 'OVERALL INSIDE DEPTH 17" (432 mm)', 15)

# back / front labels
a(f'<text x="{OX + f(W)/2}" y="{OY - 108}" font-size="14" text-anchor="middle" fill="#666" letter-spacing="3">▲ BACK OF DRAWER</text>')
a(f'<text x="{OX + f(W)/2}" y="{OY + f(D) + 45}" font-size="14" text-anchor="middle" fill="#666" letter-spacing="3">▼ FRONT OF DRAWER (HANDLE SIDE — YOU STAND HERE)</text>')

# ---- tables ----------------------------------------------------------------
TY = OY + f(D) + 90
a(f'<text x="110" y="{TY}" font-size="20" font-weight="700" fill="#111">COMPARTMENT SCHEDULE (23 compartments)</text>')
sched = [
    ("Perfume bay", 1, '7 1/2" × 11"', "6–8 bottles standing"),
    ("Grooming", 1, '7 1/2" × 5 3/4"', "Deo, trimmer, comb"),
    ("Belts", 6, '4 1/2" × 5 1/2"', "1 rolled belt each"),
    ("Watches", 6, '3" × 4"', "1 watch on a pillow each"),
    ("Wallets", 2, '4 5/8" × 8 1/2"', "2–3 wallets / card cases on edge"),
    ("Sunglasses", 3, '7" × 3 1/2"', "1 pair / case each"),
    ("Rings · Cufflinks · Chain", 3, '3 3/4" × 3 1/2"', "Small jewellery"),
    ("Daily drop tray", 1, '11" × 5 3/4"', "Keys, phone, earbuds, pen"),
]
cols_x = [110, 390, 450, 610]
hdr = ["Compartment", "Qty", "Clear size (W × D)", "Holds"]
for cx, h in zip(cols_x, hdr):
    a(f'<text x="{cx}" y="{TY + 34}" font-size="14" font-weight="700" fill="#333">{h}</text>')
a(f'<line x1="110" y1="{TY + 42}" x2="860" y2="{TY + 42}" stroke="#333"/>')
for r, row in enumerate(sched):
    yy = TY + 64 + r * 25
    for cx, v in zip(cols_x, row):
        a(f'<text x="{cx}" y="{yy}" font-size="14" fill="#222">{v}</text>')

# cut list
CX = 920
cut = [
    ('17"', 4, "Main long dividers (full depth)"),
    ('11"', 1, "Sunglasses | small-items divider"),
    ('11"', 3, "Cross pieces, sunglasses + small items"),
    ('9 1/2"', 2, "Cross pieces, watch / wallet area"),
    ('9 1/4"', 2, "Cross pieces, belts"),
    ('8 1/2"', 1, "Wallet bay centre divider"),
    ('8 1/4"', 2, "Watch cell dividers"),
    ('7 1/2"', 1, "Perfume / grooming cross piece"),
]
a(f'<text x="{CX}" y="{TY}" font-size="20" font-weight="700" fill="#111">CUT LIST — 16 pieces</text>')
for cx, h in zip([CX, CX + 90, CX + 140], ["Length", "Qty", "Use"]):
    a(f'<text x="{cx}" y="{TY + 34}" font-size="14" font-weight="700" fill="#333">{h}</text>')
a(f'<line x1="{CX}" y1="{TY + 42}" x2="{PW - 60}" y2="{TY + 42}" stroke="#333"/>')
for r, (ln, q, use) in enumerate(cut):
    yy = TY + 64 + r * 25
    for cx, v in zip([CX, CX + 90, CX + 140], [ln, str(q), use]):
        a(f'<text x="{cx}" y="{yy}" font-size="14" fill="#222">{v}</text>')
a(f'<text x="{CX}" y="{TY + 64 + 8 * 25 + 4}" font-size="13" fill="#555">All strips 1/4" (6 mm) thick × 2 1/2" (65 mm) high · total ≈ 15 ft running length</text>')

# notes
NY = TY + 330
notes = [
    "1. MEASURE FIRST: confirm the drawer's clear inside size is 38\" × 17\". If it differs, keep every cell size above and absorb the difference in the",
    "    Perfume bay (width) and the Daily drop tray (depth) — those are the only two flexible compartments.",
    "2. Dividers: 6 mm plywood / MDF with white laminate or edge-banding to match the drawer (or 4–5 mm acrylic). Height 65 mm — keep ≥ 25 mm clear under the drawer above.",
    "3. Joints: where two dividers cross, cut half-depth slots (egg-crate / halving joint) so the grid drops in as one removable unit. Cut each piece ~1 mm short for easy fit.",
    "4. Lining: glue 2–3 mm velvet / suede sheet on the drawer base (like the sample photo) so watches, perfume and sunglasses don't scratch or slide.",
    "5. Watch cells: 6 soft pillows, 3\" long × 2\" dia (foam rolled in the same fabric), lying front-to-back in each 3\" × 4\" cell.",
    "6. Perfume: check tallest bottle vs. drawer inside height before finalising — tall bottles can lie on their side in the 11\" deep bay.",
]
a(f'<text x="110" y="{NY}" font-size="20" font-weight="700" fill="#111">NOTES FOR CARPENTER</text>')
for k, n in enumerate(notes):
    a(f'<text x="110" y="{NY + 30 + k * 23}" font-size="14" fill="#222" xml:space="preserve">{n}</text>')
a('</svg>')

open("drawer-organizer.svg", "w").write("\n".join(out))
print(f"ok: {len(cells)} compartments, {len(dividers)} divider segments, tiling verified")
