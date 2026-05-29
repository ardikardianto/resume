# Personal Homepage

This repository contains the static personal homepage for Ardik Ardianto, a lecturer, translator, and researcher based in Indonesia.

The site presents a concise academic portfolio drawn from `Ardianto's Resume.pdf`, including professional roles, research identity, selected publications, public scholarly metrics, and profile links.

## Contents

- `index.html` - the main static homepage.
- `Ardianto's Resume.pdf` - source resume and downloadable PDF linked from the site.
- `assets/Profile.png` - circular profile photo used in the hero section.
- `assets/resume-preview.png` - resume preview image used in the profile section and social metadata.
- `scripts/update-scholar-citations.py` - monthly Google Scholar citation updater used by GitHub Actions.
- `.github/workflows/update-scholar-citations.yml` - scheduled workflow that refreshes the Google Scholar citation metric.

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

## Monthly Citation Update

The Google Scholar citation number in `index.html` is marked with `data-metric="google-scholar-citations"` and is refreshed by a GitHub Actions workflow on the first day of every month.

You can also run the updater manually:

```bash
python3 scripts/update-scholar-citations.py
```

The workflow commits only when the Google Scholar citation count changes.

## Profile Links

- ORCID: https://orcid.org/0000-0001-8642-5840
- ResearchGate: https://www.researchgate.net/profile/Ardik-Ardianto
- LinkedIn: http://www.linkedin.com/in/ardikardianto
- Scopus: http://www.scopus.com/inward/authorDetails.url?authorID=58844250600&partnerID=MN8TOARS
- Google Scholar: https://scholar.google.com/citations?user=LATwILMAAAAJ

## Notes

The homepage is intentionally framework-free: no build step, no package manager, and no client-side dependencies. Edits can be made directly in `index.html`.
