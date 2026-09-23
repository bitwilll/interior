# Lessons

- **Drawing labels overlapped the subtitle** — root cause: dimension chains were placed above the plan origin without reserving header space. Rule: always render and visually inspect the PNG before delivering a drawing.
- **1/4" gap where a short divider met a cross piece** — root cause: divider segments built per column didn't cover the shared junction. Rule: keep an automated area-tiling check in the generator.
