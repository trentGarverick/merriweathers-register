# Merriweather's Register of Agreeable Occurrences
Static Netlify site. Hub at `/`, issues at `/issues/vol1noN/`.

## Conventions (mirrors insane-mag)
- Each issue: self-contained `issues/vol1noN/index.html` (page-flip, inline CSS/JS)
- Cover PNG (1400x1978) at `images/vol1noN-cover.png` — used BOTH on the hub card AND as the issue's og:image
- Hub preview image: `register-hub.png` (1280x768)
- All og:image / og:url tags use ABSOLUTE URLs on https://register.bumbloobooks.com
  → If the subdomain changes, update the <meta> tags in index.html and each issue's index.html

## Link previews (the part that matters)
1. Deploy first, so the image exists at its final URL
2. Then share the link. Facebook caches scrapes aggressively — if a preview
   looks stale, paste the URL into https://developers.facebook.com/tools/debug/
   and hit "Scrape Again"

## Adding an issue
1. Copy issues/vol1no1/ → issues/vol1no2/, replace content + OG tags
2. Render a new typographic cover (the make_covers.py approach) → images/vol1no2-cover.png
3. Add an issue-card to index.html
4. Deploy
