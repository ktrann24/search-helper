"""Ashby ATS API client."""

import requests
from dataclasses import dataclass
from typing import Optional


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


class AshbyFetcher:
    """Fetches jobs from companies using Ashby ATS."""

    BASE_URL = "https://api.ashbyhq.com/posting-api/job-board"

    def __init__(self, company_slug: str, company_name: str):
        self.company_slug = company_slug
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        """Fetch all jobs from the company's Ashby board."""
        url = f"{self.BASE_URL}/{self.company_slug}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            job_postings = data.get("jobs", [])

            jobs = []
            for job_data in job_postings:
                job = self._parse_job(job_data)
                if job:
                    jobs.append(job)

            return jobs

        except requests.RequestException as e:
            print(f"Error fetching jobs from {self.company_name}: {e}")
            return []

    def _parse_job(self, job_data: dict) -> Optional[Job]:
        """Parse a single job from Ashby API response."""
        try:
            job_id = job_data.get("id")

            return Job(
                id=f"ashby_{self.company_slug}_{job_id}",
                title=job_data.get("title", "Unknown Title"),
                company=self.company_name,
                location=job_data.get("location", "Unknown"),
                url=job_data.get("jobUrl", f"https://jobs.ashbyhq.com/{self.company_slug}/{job_id}"),
                posted_at=job_data.get("publishedAt"),
                department=job_data.get("department"),
            )
        except Exception as e:
            print(f"Error parsing job: {e}")
            return None
