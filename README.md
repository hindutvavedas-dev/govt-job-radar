# Govt Job Radar — daily official-source discovery starter

This project is a static dashboard plus a scheduled discovery script. It scans configured official recruitment pages once daily, collects links whose anchor text looks recruitment-related, and places them in `data/review_queue.json` as **Needs manual review**. The website deploys through GitHub Pages.

## Important accuracy limit

This is a discovery aid, not an exhaustive government vacancy API. Some official sites block automated access, rely on JavaScript, put notice details in PDFs, or use link text the scanner does not recognise. The scanner cannot safely infer application status, age, qualification, vacancies or last date. A person must open the original notice and verify details before adding it to `data/jobs.json`. Do not label a job open based only on a link appearing in the queue.

## Setup (free starter route)

1. Download and extract the ZIP on your device.
2. Sign in or create a GitHub account at https://github.com/.
3. Create a **new public repository** named `govt-job-radar` (public is needed for the straightforward GitHub Free Pages setup).
4. Upload the *contents* of this extracted folder into the repository root, including the hidden `.github` folder. Keep the folder structure intact. The root should show `index.html`, `data/`, `scripts/`, `.github/`, and `requirements.txt`.
5. Open repository **Settings → Pages** and choose **GitHub Actions** as the publishing source.
6. Open **Actions**. If GitHub asks you to enable workflows, enable them. Select **Daily official notice scan and deploy**, then choose **Run workflow** once.
7. Wait for the workflow to finish successfully. Open **Settings → Pages**; GitHub shows your public site URL there. It normally looks like `https://YOUR-USERNAME.github.io/govt-job-radar/`.
8. After setup, the scheduled workflow runs daily at 08:00 IST (GitHub scheduled jobs can be delayed, and may not run exactly on time). You can also run it manually from Actions.
9. Open your website's **Review inbox**. For each candidate, open the official notice PDF/page and verify the date, post, eligibility, application status and deadline.
10. To publish a verified vacancy, edit `data/jobs.json` in GitHub and add an object in this format, then commit the change:

```json
[
  {
    "title": "Exact post and advertisement number",
    "department": "Official department name",
    "source_name": "Recruitment board name",
    "sector": "SSC",
    "status": "Open — manually verified",
    "vacancies": "As stated in the notice",
    "qualification": "Exact qualification from the notice",
    "age_limit": "Exact age and cutoff date from the notice",
    "last_date": "YYYY-MM-DD as stated in the notice",
    "selection_process": "Exact stages from the notice",
    "notice_url": "https://official-domain.gov.in/path/to/notice.pdf",
    "official_url": "https://official-domain.gov.in/apply-page",
    "source_page": "https://official-domain.gov.in/recruitment-page",
    "notes": "Last checked YYYY-MM-DD"
  }
]
```

If you already have listings, keep them in the same JSON array, separated by commas. JSON must be valid; avoid trailing commas.

## What is automatic vs manual?

- **Automatic:** scheduled page checks; candidate-link discovery; storing the review queue; website redeployment.
- **Manual:** reading the full notification; confirming it is current/open; extracting eligibility and deadlines accurately; approving it in `data/jobs.json`.
- **Not included:** guaranteed coverage of every department, AI/PDF analysis, WhatsApp/SMS alerts, a private admin panel, or automatic eligibility decisions.

## Troubleshooting

- If Actions fails, open the failed run to read its log; common causes are source sites blocking requests or a bad uploaded folder structure.
- If no new candidates appear, it does not prove there are no vacancies; the sites may block bots or use unrecognised page structures.
- The scanner is intentionally polite (one request per source per daily run). Do not increase frequency aggressively.
- Keep the repository public only if you are comfortable with its contents being publicly visible. Do not put passwords, API keys or personal documents in it.
