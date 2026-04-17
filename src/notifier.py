"""Slack notification service."""

import os
import json
import requests
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from .config import SLACK_WEBHOOK_URL, DRY_RUN
from .processor import is_general_ledger_job


@dataclass
class Job:
    """Normalized job representation."""
    id: str
    title: str
    company: str
    location: str
    url: str
    posted_at: Optional[str] = None
    department: Optional[str] = None


class SlackNotifier:
    """Sends job digest messages via Slack webhook."""

    def __init__(self, webhook_url: str = None, dry_run: bool = None):
        self.webhook_url = webhook_url or SLACK_WEBHOOK_URL
        self.dry_run = dry_run if dry_run is not None else DRY_RUN

    def send_digest(
        self,
        all_jobs: list[Job],
        company_count: int,
        hot_jobs: list[Job] = None,  # unused, kept for compat
    ) -> bool:
        """Send job digest to Slack."""
        blocks = self._build_blocks(all_jobs, company_count)

        if self.dry_run:
            print(f"\n{'='*60}")
            print("DRY RUN - Slack message would be sent:")
            print(f"  Total open: {len(all_jobs)}")
            print(f"{'='*60}\n")
            return True

        if not self.webhook_url:
            print("Error: SLACK_WEBHOOK_URL not configured")
            return False

        try:
            response = requests.post(
                self.webhook_url,
                json={"blocks": blocks},
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            if response.status_code == 200:
                print("Slack message sent successfully")
                return True
            else:
                print(f"Slack send failed: {response.status_code} {response.text}")
                return False
        except Exception as e:
            print(f"Error sending Slack message: {e}")
            return False

    def _build_blocks(self, all_jobs: list[Job], company_count: int) -> list:
        """Build Slack Block Kit payload."""
        date_str = datetime.now().strftime("%A, %B %d")
        blocks = []

        # Header
        blocks.append({
            "type": "header",
            "text": {"type": "plain_text", "text": f"🐱 Jessica's Job Digest — {date_str}"}
        })

        # Stats
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{len(all_jobs)} open positions* across {company_count} companies",
            }
        })

        blocks.append({"type": "divider"})

        # All open positions
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*📋 All Open Positions ({len(all_jobs)})*"}
        })

        # Slack blocks have a 50-block limit; batch jobs into one text block
        lines = []
        for job in all_jobs:
            gl_tag = " `GL`" if is_general_ledger_job(job) else ""
            lines.append(f"• <{job.url}|{job.title}>{gl_tag} — *{job.company}* · {job.location}")

        # Split into chunks of 20 to stay readable
        chunk_size = 20
        for i in range(0, len(lines), chunk_size):
            chunk = "\n".join(lines[i:i + chunk_size])
            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": chunk}
            })

        # Footer
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "context",
            "elements": [{
                "type": "mrkdwn",
                "text": f"GL/Accountant roles · SF & Remote · Good luck! 🍀"
            }]
        })

        return blocks


# Keep old name as alias so main.py import doesn't break
EmailNotifier = SlackNotifier
