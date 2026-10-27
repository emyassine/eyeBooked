# EyeBooked · brand assets

Assets extracted and rebuilt from the live SVG mark, wordmark, theme colors, and page background in `index-14.html`. All logo color values are hard-coded in the SVGs; no Tailwind classes, CSS variables, or runtime gradients are needed.

## Logos

`logos/` contains logo marks, wordmarks, and the stacked logo with the English app tagline, in light and dark variants for every in-app color theme: green (default), blue, and violet. The reversed splash lockup is also included for each theme.

- Logo mark PNGs: 2048 × 2048, transparent.
- Wordmark PNGs: 3200 px wide, transparent.
- Stacked lockup PNGs: 2400 px wide, transparent except for the splash variants, which include the original brand gradient.
- SVG wordmark text has been outlined to paths so the logo keeps its exact type shape even when Plus Jakarta Sans is not installed.

## Page backgrounds

`backgrounds/` contains light and dark page backgrounds for the green, blue, and violet themes. Each SVG is scalable; each PNG is 2560 × 1440 (2K, 16:9). These are static exports of the page gradient and soft aurora. The original page animates the aurora, so the background PNG represents one still frame.

## Brand colors and type

`palette.json` records the original theme colors. `fonts/` includes Plus Jakarta Sans variable font and its SIL Open Font License, matching the app's 800-weight wordmark and its UI typography.

## Rebuild

Run `python3 brand/generate_assets.py` from the project root with Inkscape installed. The generator uses the bundled Plus Jakarta Sans font for the outlined wordmarks.
