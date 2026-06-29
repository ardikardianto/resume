# Personal Homepage

This repository contains the static personal homepage for Ardik Ardianto, a lecturer, translator, and researcher based in Indonesia.

The site presents a concise academic portfolio drawn from `Ardianto's Resume.pdf`, including professional roles, research identity, selected publications, public scholarly metrics, and profile links.

## Contents

- `index.html` - the main static homepage.
- `Ardianto's Resume.pdf` - source resume and downloadable PDF linked from the site.
- `assets/Profile.jpg` - optimized circular profile photo used in the hero section (compressed from `Profile.png`).
- `assets/Profile.png` - full-resolution source of the profile photo.
- `assets/resume-preview.png` - resume preview image used in the profile section and social metadata.
- `assets/project-*.jpg` - Projects section thumbnails captured from the live Department Dashboard, Department Publications, and Digital Translation Laboratory sites.
- `assets/source/resume-base.pdf` - clean base PDF used to regenerate the public resume metrics.
- `scripts/update-site-metrics.py` - monthly public scholarly metrics updater used by GitHub Actions.
- `scripts/update-resume-pdf-metrics.py` - keeps visible resume PDF metrics aligned with `index.html`.
- `scripts/render-resume-preview.py` - regenerates the resume preview image from the first PDF page.
- `.github/workflows/update-site-metrics.yml` - scheduled workflow that refreshes public scholarly metrics.

## Design Direction

The page is designed as a minimal portfolio homepage inspired by the Minilio minimal portfolio template:

- large but restrained editorial typography
- warm paper background
- simple two-column rhythm on desktop
- compact stacked layout on mobile
- lightweight navigation and section dividers
- text-first academic portfolio structure

## Local Preview

Open `index.html` directly in a browser, or run a small static server:

```bash
python3 -m http.server 4173
```

Then visit:

```text
http://127.0.0.1:4173/
```

## Deployment

Because this is a static site, it can be deployed with GitHub Pages, Netlify, Vercel, Cloudflare Pages, or any static hosting provider.

For GitHub Pages:

1. Open the repository settings on GitHub.
2. Go to **Pages**.
3. Set the source to the `main` branch.
4. Use the repository root as the publishing directory.

## Monthly Metrics Update

The public scholarly metrics in `index.html` are marked with `data-metric` attributes and refreshed by a GitHub Actions workflow on the first day of every month.

The updater covers:

- ORCID listed works from the ORCID public API.
- Google Scholar citations from the public Google Scholar profile.
- ResearchGate reads and citations on a best-effort basis from the public ResearchGate stats/profile pages.

You can also run the updater manually:

```bash
python3 scripts/update-site-metrics.py
```

The workflow commits only when a metric changes. If ResearchGate blocks automated access, the existing ResearchGate values are preserved and the other metrics still update.

The same workflow also overlays the current metrics onto `Ardianto's Resume.pdf` and regenerates `assets/resume-preview.png`, so the downloadable resume and site preview stay aligned with the homepage.

## Profile Links

- ORCID: https://orcid.org/0000-0001-8642-5840
- ResearchGate: https://www.researchgate.net/profile/Ardik-Ardianto/stats
- LinkedIn: http://www.linkedin.com/in/ardikardianto
- Scopus: http://www.scopus.com/inward/authorDetails.url?authorID=58844250600&partnerID=MN8TOARS
- Google Scholar: https://scholar.google.com/citations?user=LATwILMAAAAJ

## Notes

The homepage is intentionally framework-free: no build step, no package manager, and no client-side dependencies. Edits can be made directly in `index.html`.
