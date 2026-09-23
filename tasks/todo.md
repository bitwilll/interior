# Drawer organizer (38" x 17") – carpenter sketch

- [x] Fix layout: 5 columns, 1/4" (6 mm) dividers, cell sizes for perfume, belts, watches, wallets, sunglasses, rings/cufflinks, daily drop tray
- [x] Verify every row/column adds up to exactly 38" and 17" (script check)
- [x] Generate dimensioned plan-view sketch (SVG -> PNG + PDF) with cut list and notes
- [x] Visually inspect rendered PNG for overlaps/illegible labels
- [x] Commit, push, open draft PR

## Review
- build.py asserts every column sums to 38" and every row to 17", and that cells + dividers tile the drawer with no gaps (caught a 1/4" gap at the sunglasses/drop-tray junction, fixed).
- Rendered PNG inspected; fixed title/dimension label overlap by moving the plan down.
