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
    # GL-adjacent roles
    "technical accounting",
    "accounting operations",
    "accounting analyst",
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
    # Non-GL accounting specializations
    "revenue",        # revenue accountant, revenue accounting
    "commissions",
    "cost accountant",
    "cost of revenue",
    "fleet",
    "derivatives",
    "broker dealer",
    "asset management",
    "accounts receivable",
    "payroll",
    "tax accountant",
    "tax analyst",
    "billing",
    "collections",
    "credit analyst",
    "accounts payable",
    # Engineering/Product roles with "accounting" in name
    "software engineer",
    "product",
    "data engineer",
]

# Location keywords (case-insensitive)
# Must match at least one to be included
# Focused on San Francisco and Remote only
LOCATION_KEYWORDS = [
    # San Francisco
    "san francisco",
    "sf",
    # Remote options
    "remote",
    "hybrid",
    "anywhere",
    "work from home",
    "wfh",
]

# Keywords that indicate a US-based position
# Used to filter remote jobs - must contain one of these to be included
US_LOCATION_KEYWORDS = [
    "united states",
    "usa",
    "us",
    ", ca",
    "california",
    "new york",
    ", ny",
    "texas",
    ", tx",
    "washington",
    ", wa",
    "colorado",
    ", co",
    "massachusetts",
    ", ma",
    "illinois",
    ", il",
    "north america",
]

# Keywords that indicate an international (non-US) position - exclude these
INTERNATIONAL_EXCLUDE_KEYWORDS = [
    "uk",
    "united kingdom",
    "london",
    "ireland",
    "dublin",
    "germany",
    "berlin",
    "canada",
    "toronto",
    "vancouver",
    "australia",
    "sydney",
    "singapore",
    "india",
    "bangalore",
    "emea",
    "apac",
    "latam",
    "europe",
]

# Location priority tiers (lower = higher priority)
# Used to sort jobs: SF first, Remote second
LOCATION_PRIORITY = {
    # Tier 1 - San Francisco (highest priority)
    "san francisco": 1,
    "sf": 1,

    # Tier 2 - Remote
    "remote": 2,
    "work from home": 2,
    "wfh": 2,
    "anywhere": 2,
    "hybrid": 2,
}

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
    # Additional companies
    ("mercury", "Mercury"),
    ("doordashusa", "DoorDash"),
    ("andurilindustries", "Anduril"),
    ("hubspotjobs", "HubSpot"),
    ("duolingo", "Duolingo"),
    # Note: Grammarly removed - not on Greenhouse/Ashby/Lever
    # Hot tech companies added
    ("verkada", "Verkada"),
    ("wizinc", "Wiz"),
    ("chainguard", "Chainguard"),
    ("cerebrassystems", "Cerebras"),
    ("gleanwork", "Glean"),
    ("heygen", "HeyGen"),
    ("astranis", "Astranis"),
    ("clarifai", "Clarifai"),
    ("xai", "xAI"),
    # Note: Retool moved to Ashby, Grammarly removed (no supported ATS)
    # Forbes AI 50 additions (Greenhouse)
    ("fireworksai", "Fireworks AI"),
    ("hebbia", "Hebbia"),
    ("figureai", "Figure AI"),
    ("snorkelai", "Snorkel AI"),
    ("togetherai", "Together AI"),
    ("coactive", "Coactive"),
    ("worldlabs", "World Labs"),
    ("vannevarlabs", "Vannevar Labs"),
    # Forbes AI 50 2026 additions (Greenhouse)
    ("appliedintuition", "Applied Intuition"),
    ("blackforestlabs", "Black Forest Labs"),
    ("thinkingmachines", "Thinking Machines Lab"),
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
    # Additional companies
    ("vanta", "Vanta"),
    ("anyscale", "Anyscale"),
    ("replit", "Replit"),
    ("cursor", "Cursor"),
    ("retool", "Retool"),
    # Hot tech companies added
    ("harvey", "Harvey"),
    ("cognition", "Cognition"),
    ("WRITER", "Writer"),
    ("Mintlify", "Mintlify"),
    # AI companies batch
    ("elevenlabs", "ElevenLabs"),
    ("lovable", "Lovable"),
    ("modal", "Modal"),
    ("granola", "Granola"),
    ("Abridge", "Abridge"),
    ("ambiencehealthcare", "Ambience Healthcare"),
    ("Crusoe", "Crusoe"),
    ("novita-ai", "Novita AI"),
    ("Juicebox", "Juicebox"),
    ("peec", "Peec AI"),
    ("profound", "Profound"),
    # Forbes AI 50 additions (Ashby)
    ("synthesia", "Synthesia"),
    ("sierra", "Sierra"),
    ("lambda", "Lambda"),
    ("decagon", "Decagon"),
    ("photoroom", "Photoroom"),
    ("speak", "Speak"),
    ("langchain", "LangChain"),
    ("openevidence", "OpenEvidence"),
    ("mercor", "Mercor"),
    ("suno", "Suno"),
    ("baseten", "Baseten"),
    ("pika", "Pika"),
    ("vast", "VAST Data"),
    ("deepl", "DeepL"),
    # Forbes AI 50 2026 additions (Ashby)
    ("gamma", "Gamma"),
    ("eliseai", "EliseAI"),
    ("chaidiscovery", "Chai Discovery"),
    ("listenlabs", "Listen Labs"),
    ("reflectionai", "Reflection"),
    ("legora", "Legora"),
    ("krea", "Krea"),
    ("physicalintelligence", "Physical Intelligence"),
    ("ssi", "Safe Superintelligence"),
    ("rogo", "Rogo"),
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
