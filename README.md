# Job Search Agent

Automated job search agent that monitors career pages of top tech companies for accountant/GL roles and sends daily email digests.

## Features

- Monitors 30+ tech companies via Greenhouse, Ashby, and Lever APIs
- Filters for accountant/GL roles in San Francisco or Remote
- Excludes manager/director level positions (IC roles only)
- Tracks seen jobs to only notify about new postings
- Daily email digest at 8am PST via GitHub Actions

## Companies Monitored

**Greenhouse:** Figma, ClickUp, Gusto, Airbnb, Coinbase, Square, Chime, Brex, Plaid, Databricks, Airtable, Webflow, Retool, Amplitude, Loom, Calendly, Lattice, Carta, Vercel, Supabase, Navan, Scale AI, Anthropic, OpenAI, Anduril, Deel

**Ashby:** Notion, Ramp, Rippling, Mercury, Linear

**Lever:** Zapier

## Setup

### 1. Clone and Install

```bash
git clone <your-repo>
cd search-helper
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Required environment variables:
- `SENDGRID_API_KEY` - Get from [SendGrid](https://sendgrid.com) (free tier: 100 emails/day)
- `FROM_EMAIL` - Sender email address (must be verified in SendGrid)
- `TO_EMAIL` - Recipient email address

### 3. Test Locally

```bash
# Dry run (no emails sent)
python -m src.main --dry-run

# Run with filters disabled to see all jobs
python -m src.main --dry-run --no-filter

# Reset job history (treat all jobs as new)
python -m src.main --dry-run --reset-history
```

### 4. Deploy to GitHub Actions

1. Push code to GitHub
2. Go to Settings > Secrets and variables > Actions
3. Add these secrets:
   - `SENDGRID_API_KEY`
   - `FROM_EMAIL`
   - `TO_EMAIL`
4. The workflow runs daily at 8am PST automatically
5. To test, go to Actions > Daily Job Search > Run workflow

## Project Structure

```
search-helper/
├── .github/workflows/
│   └── daily-search.yml    # GitHub Actions workflow
├── src/
│   ├── config.py           # Company list, keywords, settings
│   ├── main.py             # Entry point
│   ├── fetchers/
│   │   ├── greenhouse.py   # Greenhouse API client
│   │   ├── ashby.py        # Ashby API client
│   │   └── lever.py        # Lever API client
│   ├── processor.py        # Filter and dedupe logic
│   ├── notifier.py         # Email sending
│   └── storage.py          # Job history tracking
├── templates/
│   └── digest.html         # Email template
├── requirements.txt
└── README.md
```

## Customization

### Add/Remove Companies

Edit `src/config.py` and modify the company lists:

```python
GREENHOUSE_COMPANIES = [
    ("company-slug", "Company Name"),
    ...
]
```

### Modify Job Filters

Edit `src/config.py`:

```python
# Keywords to include
TITLE_INCLUDE_KEYWORDS = ["accountant", "gl accountant", ...]

# Keywords to exclude (manager roles, etc.)
TITLE_EXCLUDE_KEYWORDS = ["manager", "director", ...]

# Location filters
LOCATION_KEYWORDS = ["san francisco", "remote", ...]
```

## Cost

| Service | Cost |
|---------|------|
| GitHub Actions | Free (2,000 mins/month) |
| SendGrid | Free (100 emails/day) |
| **Total** | **$0/month** |

## License

MIT
