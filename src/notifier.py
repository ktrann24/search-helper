"""Email notification service."""

import os
import uuid
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from string import Template

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Header

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

            # Add unique Message-ID to prevent email threading
            unique_id = uuid.uuid4().hex
            message.header = Header("X-Entity-Ref-ID", unique_id)

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
                    dept_html = f'<div style="font-size: 11px; color: #9ca3af; margin-bottom: 8px;">🏢 {job.department}</div>'

                hot_jobs_html += f'''
                <div style="border: 2px solid #f472b6; border-radius: 12px; padding: 16px; margin-bottom: 12px; background: linear-gradient(135deg, #fdf2f8 0%, #ffffff 100%);">
                    <div style="font-size: 16px; font-weight: 700; color: #111827; margin-bottom: 6px;">{job.title}</div>
                    <div style="font-size: 14px; color: #be185d; font-weight: 600; margin-bottom: 4px;">{job.company}</div>
                    <div style="font-size: 12px; color: #6b7280; margin-bottom: 4px;">📍 {job.location}</div>
                    {dept_html}
                    <a href="{job.url}" style="display: inline-block; background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%); color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 20px; font-size: 13px; font-weight: 500; margin-top: 8px;">View & Apply →</a>
                </div>
                '''

        # Build all jobs HTML
        all_jobs_html = ""
        for job in all_jobs:
            dept_html = ""
            if job.department:
                dept_html = f'<span style="color: #9ca3af;"> · {job.department}</span>'

            all_jobs_html += f'''
            <div style="border-bottom: 1px solid #f3e8ff; padding: 14px 0;">
                <div style="font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 2px;">{job.title}</div>
                <div style="font-size: 13px; color: #be185d; font-weight: 600; margin-bottom: 2px;">{job.company}{dept_html}</div>
                <div style="font-size: 12px; color: #6b7280; margin-bottom: 6px;">📍 {job.location}</div>
                <a href="{job.url}" style="font-size: 12px; color: #ec4899; text-decoration: none; font-weight: 500;">Apply →</a>
            </div>
            '''

        # Build hot section
        hot_section = ""
        if hot_jobs:
            hot_section = f'''
            <div style="margin-bottom: 28px;">
                <h2 style="font-size: 16px; color: #ec4899; margin: 0 0 16px 0; padding-bottom: 12px; border-bottom: 2px solid #fbcfe8;">
                    ✨ {len(hot_jobs)} New This Week
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
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff0f5;">
            <div style="background-color: #ffffff; border-radius: 16px; padding: 32px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); border: 1px solid #fce7f3;">

                <!-- Header with Hello Kitty -->
                <div style="text-align: center; margin-bottom: 24px;">
                    <img src="https://raw.githubusercontent.com/ktrann24/search-helper/main/hellokitty.jpeg" alt="Hello Kitty" style="width: 80px; height: auto; margin-bottom: 12px;">
                    <h1 style="color: #ec4899; font-size: 26px; margin: 0; font-weight: 600;">Jessica's Job Digest</h1>
                    <p style="color: #9ca3af; font-size: 14px; margin-top: 4px;">{date_str}</p>
                </div>

                <!-- Stats Card -->
                <div style="background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%); border-radius: 12px; padding: 20px; margin-bottom: 24px; text-align: center; border: 1px solid #fbcfe8;">
                    <div style="font-size: 42px; font-weight: bold; color: #ec4899;">{len(all_jobs)}</div>
                    <div style="color: #6b7280; font-size: 14px;">open positions matching your criteria ✨</div>
                </div>

                {hot_section}

                <!-- All Jobs Section -->
                <div style="background-color: #fafafa; border-radius: 12px; padding: 20px; border: 1px solid #f3f4f6;">
                    <h2 style="font-size: 16px; color: #374151; margin: 0 0 16px 0; padding-bottom: 12px; border-bottom: 2px solid #fce7f3;">
                        📋 All Open Positions
                    </h2>
                    {all_jobs_html}
                </div>

                <!-- Footer -->
                <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #fce7f3; font-size: 12px; color: #9ca3af; text-align: center;">
                    <p style="margin: 4px 0;">Monitoring {company_count} tech companies 💼</p>
                    <p style="margin: 4px 0;">GL/Accountant roles · San Francisco & Remote</p>
                    <p style="margin: 8px 0 0 0; font-size: 11px;">Good luck! 🍀</p>
                </div>
            </div>
        </body>
        </html>
        '''
