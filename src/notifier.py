"""Email notification service."""

import os
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from string import Template

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

from .config import SENDGRID_API_KEY, FROM_EMAIL, TO_EMAIL, DRY_RUN


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


class EmailNotifier:
    """Sends job digest emails via SendGrid."""

    def __init__(
        self,
        api_key: str = None,
        from_email: str = None,
        to_email: str = None,
        dry_run: bool = None,
    ):
        self.api_key = api_key or SENDGRID_API_KEY
        self.from_email = from_email or FROM_EMAIL
        self.to_email = to_email or TO_EMAIL
        self.dry_run = dry_run if dry_run is not None else DRY_RUN
        self.template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "templates",
            "digest.html"
        )

    def send_digest(
        self,
        hot_jobs: list[Job],
        all_jobs: list[Job],
        company_count: int
    ) -> bool:
        """Send job digest email with hot jobs and all open positions."""
        html_content = self._render_template(hot_jobs, all_jobs, company_count)
        subject = self._get_subject(len(hot_jobs), len(all_jobs))

        if self.dry_run:
            print(f"\n{'='*60}")
            print("DRY RUN - Email would be sent:")
            print(f"  To: {self.to_email}")
            print(f"  From: {self.from_email}")
            print(f"  Subject: {subject}")
            print(f"  Hot jobs: {len(hot_jobs)}")
            print(f"  Total open: {len(all_jobs)}")
            print(f"{'='*60}\n")
            return True

        if not self.api_key:
            print("Error: SENDGRID_API_KEY not configured")
            return False

        try:
            # Support multiple recipients (comma-separated)
            recipients = [
                To(email.strip())
                for email in self.to_email.split(",")
                if email.strip()
            ]

            message = Mail(
                from_email=Email(self.from_email),
                to_emails=recipients,
                subject=subject,
                html_content=Content("text/html", html_content),
            )

            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)

            if response.status_code in (200, 201, 202):
                print(f"Email sent successfully to {self.to_email}")
                return True
            else:
                print(f"Email sending failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def _get_subject(self, hot_count: int, total_count: int) -> str:
        """Generate email subject line."""
        date_str = datetime.now().strftime("%b %d")
        if hot_count > 0:
            return f"Job Digest: {hot_count} new, {total_count} open positions ({date_str})"
        else:
            return f"Job Digest: {total_count} open positions ({date_str})"

    def _render_template(
        self,
        hot_jobs: list[Job],
        all_jobs: list[Job],
        company_count: int
    ) -> str:
        """Render HTML email with hot jobs and all open positions."""
        date_str = datetime.now().strftime("%A, %B %d, %Y")

        # Build hot jobs HTML
        hot_jobs_html = ""
        if hot_jobs:
            for job in hot_jobs:
                dept_html = ""
                if job.department:
                    dept_html = f'<div style="font-size: 12px; color: #888; margin-bottom: 8px;">{job.department}</div>'

                hot_jobs_html += f'''
                <div style="border: 2px solid #22c55e; border-radius: 8px; padding: 16px; margin-bottom: 12px; background: #f0fdf4;">
                    <div style="font-size: 16px; font-weight: 600; color: #1a1a1a; margin-bottom: 4px;">{job.title}</div>
                    <div style="font-size: 14px; color: #2563eb; font-weight: 500; margin-bottom: 4px;">{job.company}</div>
                    <div style="font-size: 13px; color: #666; margin-bottom: 4px;">{job.location}</div>
                    {dept_html}
                    <a href="{job.url}" style="display: inline-block; background-color: #22c55e; color: #ffffff; text-decoration: none; padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: 500;">View & Apply</a>
                </div>
                '''

        # Build all jobs HTML
        all_jobs_html = ""
        for job in all_jobs:
            dept_html = ""
            if job.department:
                dept_html = f'<span style="color: #888;"> · {job.department}</span>'

            all_jobs_html += f'''
            <div style="border-bottom: 1px solid #e5e5e5; padding: 12px 0;">
                <div style="font-size: 14px; font-weight: 500; color: #1a1a1a;">{job.title}</div>
                <div style="font-size: 13px; color: #2563eb;">{job.company}{dept_html}</div>
                <div style="font-size: 12px; color: #666; margin-bottom: 6px;">{job.location}</div>
                <a href="{job.url}" style="font-size: 12px; color: #2563eb; text-decoration: none;">Apply →</a>
            </div>
            '''

        # Build hot section
        hot_section = ""
        if hot_jobs:
            hot_section = f'''
            <div style="margin-bottom: 32px;">
                <h2 style="font-size: 18px; color: #22c55e; margin-bottom: 16px; border-bottom: 2px solid #22c55e; padding-bottom: 8px;">
                    🔥 {len(hot_jobs)} New This Week
                </h2>
                {hot_jobs_html}
            </div>
            '''

        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Job Search Digest</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
            <div style="background-color: #ffffff; border-radius: 8px; padding: 24px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #1a1a1a; font-size: 24px; margin-bottom: 8px;">Job Search Digest</h1>
                <p style="color: #666; font-size: 14px; margin-bottom: 24px;">{date_str}</p>

                <div style="background-color: #f0f7ff; border-radius: 6px; padding: 16px; margin-bottom: 24px;">
                    <div style="font-size: 32px; font-weight: bold; color: #2563eb;">{len(all_jobs)}</div>
                    <div style="color: #666; font-size: 14px;">open positions matching your criteria</div>
                </div>

                {hot_section}

                <div>
                    <h2 style="font-size: 18px; color: #1a1a1a; margin-bottom: 16px; border-bottom: 1px solid #e5e5e5; padding-bottom: 8px;">
                        All Open Positions
                    </h2>
                    {all_jobs_html}
                </div>

                <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e5e5e5; font-size: 12px; color: #888; text-align: center;">
                    <p>Monitoring {company_count} tech companies for GL/Accountant roles</p>
                    <p>San Francisco & Remote positions</p>
                </div>
            </div>
        </body>
        </html>
        '''
