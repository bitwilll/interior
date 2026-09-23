# Lessons

- **Drawing labels overlapped the subtitle** — root cause: dimension chains were placed above the plan origin without reserving header space. Rule: always render and visually inspect the PNG before delivering a drawing.
- **1/4" gap where a short divider met a cross piece** — root cause: divider segments built per column didn't cover the shared junction. Rule: keep an automated area-tiling check in the generator.
- **Generic tiling check failed on valid layouts** — root cause: egg-crate dividers legitimately overlap at crossings (T x T), which a naive area sum counts twice. Rule: model joints explicitly in geometry checks; allow only divider-divider T x T overlaps.
- **Column widths summed to 50 3/4" instead of 51"** — root cause: counted one divider per column instead of (columns − 1). Rule: let the generator's asserts do the arithmetic; never hand-sum before running it.
- **First 3D render hid the front row and metals looked brown** — root cause: tall drawer front + low camera; metalness with no environment map renders dark. Rule: keep the front at wall height for top-down previews; use non-metal "gold" without an env map.
