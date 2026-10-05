# CareCompanion

A free, private, no-install web app for people with cancer and their support circle.

- **Symptom log** – track symptoms and severity to share with the care team
- **Medications** – daily checklist
- **Appointments** – with a list of questions to ask
- **Support circle** – tasks friends and family can take on
- **Backup / print** – export JSON, print a summary for the doctor

All data stays in the browser (`localStorage`). No server, no tracking.

Languages: English and Македонски (switch top-right; auto-detected from the browser). Add more in `src/i18n.js`.

## Run
Open `index.html`, or `python3 -m http.server` and visit http://localhost:8000.

## Disclaimer
Not medical advice. It does not diagnose or treat anything.

## Ideas
Reminders/notifications, translations, clinical-trial finder (clinicaltrials.gov API), accessibility audit.

## Deploy (GitHub Pages)
`.github/workflows/pages.yml` deploys on every push to `main`. One-time setup: repo **Settings → Pages → Source: GitHub Actions**. The site will be at https://ljupcho1982.github.io/CancerCure/
