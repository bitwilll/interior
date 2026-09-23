# Drawer organizer (38" x 17") – carpenter sketch

- [x] Fix layout: 5 columns, 1/4" (6 mm) dividers, cell sizes for perfume, belts, watches, wallets, sunglasses, rings/cufflinks, daily drop tray
- [x] Verify every row/column adds up to exactly 38" and 17" (script check)
- [x] Generate dimensioned plan-view sketch (SVG -> PNG + PDF) with cut list and notes
- [x] Visually inspect rendered PNG for overlaps/illegible labels
- [x] Commit, push, open draft PR

## Review
- build.py asserts every column sums to 38" and every row to 17", and that cells + dividers tile the drawer with no gaps (caught a 1/4" gap at the sunglasses/drop-tray junction, fixed).
- Rendered PNG inspected; fixed title/dimension label overlap by moving the plan down.

# Drawer 2 (31" x 17")
- [x] Refactor build.py: layouts as data (groups -> rows -> cells); auto-derive dividers, dimensions, schedule and cut list
- [x] Regenerate 38x17 and confirm it matches the approved drawing (same cells, same cut list)
- [x] Add 31x17 layout, verify tiling, render, inspect
- [x] Commit + push

# Dressing cabinet drawer (51" x 20")
Assumption: 51" W x 20" D is the clear inside size of the dressing-cabinet drawer (plan view, same format as the other two).
- [x] Add per-layout title + extra notes (watch/perfume notes only where relevant; hair-tool heat note for dressing)
- [x] Add 51x20 layout: hair tools column (dryer 12x10, straightener, curler), brushes/combs, skincare + palettes, 11-cell small-items grid, perfume/cotton row
- [x] Verify tiling; regenerate all three; confirm 38x17 + 31x17 cut lists unchanged
- [x] 3D render (three.js in headless Chromium) of the 51x20 organizer with simple item props
- [x] Inspect renders, commit, push
