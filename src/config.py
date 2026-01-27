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
# Focused on General Ledger / Corporate Accounting roles
TITLE_INCLUDE_KEYWORDS = [
    # Primary GL roles
    "gl accountant",
    "general ledger",
    "staff accountant",
    "senior accountant",
    "corporate accountant",
    "financial accountant",
    # Broader accounting (often GL-related)
    "accountant",  # Catches generic accountant roles
    "accounting analyst",
    # GL-adjacent roles
    "sec reporting",
    "financial reporting",
    "technical accounting",
]

# Job title keywords to EXCLUDE (case-insensitive)
# Excludes manager/director level roles per requirements
# Also excludes specialist roles not related to GL
TITLE_EXCLUDE_KEYWORDS = [
    # Leadership roles
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
    # Specialist roles (not GL-focused)
    "accounts receivable",
    "payroll",
    "tax accountant",
    "tax analyst",
    "billing",
    "collections",
    "credit analyst",
    # Engineering/Product roles with "accounting" in name
    "software engineer",
    "product",
    "data engineer",
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
    # Original list
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
    # Fintech
    ("robinhood", "Robinhood"),
    ("affirm", "Affirm"),
    ("marqeta", "Marqeta"),
    ("gemini", "Gemini"),
    ("alchemy", "Alchemy"),
    # SaaS / Productivity
    ("dropbox", "Dropbox"),
    ("asana", "Asana"),
    ("twilio", "Twilio"),
    ("datadog", "Datadog"),
    ("mongodb", "MongoDB"),
    ("elastic", "Elastic"),
    ("gitlab", "GitLab"),
    ("cloudflare", "Cloudflare"),
    ("fastly", "Fastly"),
    # Consumer / Marketplaces
    ("instacart", "Instacart"),
    ("flexport", "Flexport"),
    ("discord", "Discord"),
    ("pinterest", "Pinterest"),
    ("reddit", "Reddit"),
    ("lyft", "Lyft"),
    ("linkedin", "LinkedIn"),
]

# Companies using Ashby ATS
# Format: (company_slug, display_name)
ASHBY_COMPANIES = [
    ("notion", "Notion"),
    ("ramp", "Ramp"),
    ("linear", "Linear"),
    ("openai", "OpenAI"),
    ("deel", "Deel"),
    ("clickup", "ClickUp"),
    ("supabase", "Supabase"),
    ("perplexity", "Perplexity"),
    ("cohere", "Cohere"),
    ("runway", "Runway"),
]

# Companies using Lever ATS
# Format: (company_slug, display_name)
LEVER_COMPANIES = [
    # Most companies have moved away from Lever public API
]

# Companies with custom career pages (not yet implemented)
CUSTOM_COMPANIES = [
    # Covered via Greenhouse/Ashby APIs above
]
