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

    def send_digest(self, jobs: list[Job], company_count: int) -> bool:
        """Send job digest email."""
        html_content = self._render_template(jobs, company_count)
        subject = self._get_subject(len(jobs))

        if self.dry_run:
            print(f"\n{'='*60}")
            print("DRY RUN - Email would be sent:")
            print(f"  To: {self.to_email}")
            print(f"  From: {self.from_email}")
            print(f"  Subject: {subject}")
            print(f"  Jobs: {len(jobs)}")
            print(f"{'='*60}\n")
            return True

        if not self.api_key:
            print("Error: SENDGRID_API_KEY not configured")
            return False

        try:
            message = Mail(
                from_email=Email(self.from_email),
                to_emails=To(self.to_email),
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

    def _get_subject(self, job_count: int) -> str:
        """Generate email subject line."""
        date_str = datetime.now().strftime("%b %d")
        if job_count == 0:
            return f"Job Search Digest - No new jobs ({date_str})"
        elif job_count == 1:
            return f"Job Search Digest - 1 new job found ({date_str})"
        else:
            return f"Job Search Digest - {job_count} new jobs found ({date_str})"

    def _render_template(self, jobs: list[Job], company_count: int) -> str:
        """Render HTML email template."""
        try:
            with open(self.template_path, "r") as f:
                template_content = f.read()
        except FileNotFoundError:
            return self._render_fallback(jobs, company_count)

        # Simple template rendering (avoiding Jinja2 dependency)
        date_str = datetime.now().strftime("%A, %B %d, %Y")

        # Build jobs HTML
        jobs_html = ""
        for job in jobs:
            dept_html = ""
            if job.department:
                dept_html = f'<div class="job-department">{job.department}</div>'

            jobs_html += f'''
            <div class="job-card">
                <div class="job-title">{job.title}</div>
                <div class="job-company">{job.company}</div>
                <div class="job-location">{job.location}</div>
                {dept_html}
                <a href="{job.url}" class="apply-btn">View & Apply</a>
            </div>
            '''

        # Replace template variables
        html = template_content
        html = html.replace("{{ date }}", date_str)
        html = html.replace("{{ job_count }}", str(len(jobs)))
        html = html.replace("{{ company_count }}", str(company_count))

        # Handle conditional blocks
        if jobs:
            # Remove no-jobs section
            start = html.find("{% else %}")
            end = html.find("{% endif %}", start)
            if start != -1 and end != -1:
                html = html[:start] + html[end + 11:]

            # Remove if tags
            html = html.replace("{% if jobs %}", "")

            # Replace jobs loop with actual jobs
            loop_start = html.find("{% for job in jobs %}")
            loop_end = html.find("{% endfor %}")
            if loop_start != -1 and loop_end != -1:
                html = html[:loop_start] + jobs_html + html[loop_end + 12:]
        else:
            # Remove jobs section, keep no-jobs section
            start = html.find("{% if jobs %}")
            else_pos = html.find("{% else %}")
            end = html.find("{% endif %}")
            if start != -1 and else_pos != -1 and end != -1:
                no_jobs_content = html[else_pos + 10:end]
                html = html[:start] + no_jobs_content + html[end + 11:]

        # Clean up any remaining template tags
        import re
        html = re.sub(r'{%.*?%}', '', html)
        html = re.sub(r'{{.*?}}', '', html)

        return html

    def _render_fallback(self, jobs: list[Job], company_count: int) -> str:
        """Fallback plain HTML if template not found."""
        date_str = datetime.now().strftime("%A, %B %d, %Y")

        jobs_html = ""
        for job in jobs:
            jobs_html += f"""
            <div style="border: 1px solid #ddd; padding: 16px; margin-bottom: 12px; border-radius: 8px;">
                <strong>{job.title}</strong><br>
                <span style="color: #2563eb;">{job.company}</span><br>
                <span style="color: #666;">{job.location}</span><br>
                <a href="{job.url}" style="color: #2563eb;">Apply</a>
            </div>
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1>Job Search Digest</h1>
            <p>{date_str}</p>
            <p><strong>{len(jobs)}</strong> new job(s) found</p>
            {jobs_html}
            <hr>
            <p style="color: #888; font-size: 12px;">
                Monitoring {company_count} tech companies for GL/Accountant roles
            </p>
        </body>
        </html>
        """
