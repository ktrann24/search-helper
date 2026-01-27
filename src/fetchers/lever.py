"""Lever ATS API client."""

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


class LeverFetcher:
    """Fetches jobs from companies using Lever ATS."""

    BASE_URL = "https://api.lever.co/v0/postings"

    def __init__(self, company_slug: str, company_name: str):
        self.company_slug = company_slug
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        """Fetch all jobs from the company's Lever board."""
        url = f"{self.BASE_URL}/{self.company_slug}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            jobs = []
            for job_data in data:
                job = self._parse_job(job_data)
                if job:
                    jobs.append(job)

            return jobs

        except requests.RequestException as e:
            print(f"Error fetching jobs from {self.company_name}: {e}")
            return []

    def _parse_job(self, job_data: dict) -> Optional[Job]:
        """Parse a single job from Lever API response."""
        try:
            job_id = job_data.get("id")

            # Extract location from categories
            location = "Unknown"
            categories = job_data.get("categories", {})
            if categories:
                location = categories.get("location", "Unknown")

            # Extract department/team
            department = None
            if categories:
                department = categories.get("team")

            return Job(
                id=f"lever_{self.company_slug}_{job_id}",
                title=job_data.get("text", "Unknown Title"),
                company=self.company_name,
                location=location,
                url=job_data.get("hostedUrl", ""),
                posted_at=str(job_data.get("createdAt", "")),
                department=department,
            )
        except Exception as e:
            print(f"Error parsing job: {e}")
            return None
