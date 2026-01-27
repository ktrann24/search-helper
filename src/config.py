"""Configuration for job search agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "")
TO_EMAIL = os.getenv("TO_EMAIL", "")
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

# Job title keywords to INCLUDE (case-insensitive)
TITLE_INCLUDE_KEYWORDS = [
    "accountant",
    "accounting",
    "gl accountant",
    "general ledger",
    "staff accountant",
    "senior accountant",
    "accounting analyst",
    "accounts payable",
    "accounts receivable",
    "bookkeeper",
    "financial accountant",
    "revenue accountant",
    "payroll accountant",
    "tax accountant",
    "cost accountant",
    "fund accountant",
]

# Job title keywords to EXCLUDE (case-insensitive)
# Excludes manager/director level roles per requirements
TITLE_EXCLUDE_KEYWORDS = [
    "manager",
    "director",
    "head of",
    "vp",
    "vice president",
    "controller",
    "chief",
    "lead",
    "principal",
    "cfo",
    "cpa manager",
]

# Location keywords (case-insensitive)
# Must match at least one to be included
LOCATION_KEYWORDS = [
    "san francisco",
    "sf",
    "remote",
    "hybrid",
    "usa",
    "united states",
    "bay area",
    "california",
    "ca",
    "us",
    "anywhere",
    "work from home",
    "wfh",
]

# Companies using Greenhouse ATS
# Format: (company_slug, display_name)
GREENHOUSE_COMPANIES = [
    ("figma", "Figma"),
    ("gusto", "Gusto"),
    ("airbnb", "Airbnb"),
    ("coinbase", "Coinbase"),
    ("block", "Square/Block"),
    ("chime", "Chime"),
    ("brex", "Brex"),
    ("databricks", "Databricks"),
    ("airtable", "Airtable"),
    ("webflow", "Webflow"),
    ("retool", "Retool"),
    ("amplitude", "Amplitude"),
    ("calendly", "Calendly"),
    ("lattice", "Lattice"),
    ("carta", "Carta"),
    ("vercel", "Vercel"),
    ("tripactions", "Navan"),
    ("scaleai", "Scale AI"),
    ("anthropic", "Anthropic"),
    ("okta", "Okta"),
    ("stripe", "Stripe"),
]

# Companies using Ashby ATS
# Format: (company_slug, display_name)
ASHBY_COMPANIES = [
    ("notion", "Notion"),
    ("ramp", "Ramp"),
    ("linear", "Linear"),
]

# Companies using Lever ATS
# Format: (company_slug, display_name)
LEVER_COMPANIES = [
    # Zapier no longer uses Lever public API
]

# Companies with custom career pages (not yet implemented)
# These would need custom scrapers
CUSTOM_COMPANIES = [
    # Most companies now covered via Greenhouse/Ashby APIs
]
