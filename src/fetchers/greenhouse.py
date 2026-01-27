"""Greenhouse ATS API client."""

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


class GreenhouseFetcher:
    """Fetches jobs from companies using Greenhouse ATS."""

    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

    def __init__(self, company_slug: str, company_name: str):
        self.company_slug = company_slug
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        """Fetch all jobs from the company's Greenhouse board."""
        url = f"{self.BASE_URL}/{self.company_slug}/jobs"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            jobs = []
            for job_data in data.get("jobs", []):
                job = self._parse_job(job_data)
                if job:
                    jobs.append(job)

            return jobs

        except requests.RequestException as e:
            print(f"Error fetching jobs from {self.company_name}: {e}")
            return []

    def _parse_job(self, job_data: dict) -> Optional[Job]:
        """Parse a single job from Greenhouse API response."""
        try:
            # Extract location from the first location entry
            location = "Unknown"
            locations = job_data.get("location", {})
            if isinstance(locations, dict):
                location = locations.get("name", "Unknown")

            # Build the application URL
            job_id = job_data.get("id")
            url = f"https://boards.greenhouse.io/{self.company_slug}/jobs/{job_id}"

            return Job(
                id=f"greenhouse_{self.company_slug}_{job_id}",
                title=job_data.get("title", "Unknown Title"),
                company=self.company_name,
                location=location,
                url=url,
                posted_at=job_data.get("updated_at"),
                department=self._extract_department(job_data),
            )
        except Exception as e:
            print(f"Error parsing job: {e}")
            return None

    def _extract_department(self, job_data: dict) -> Optional[str]:
        """Extract department from job metadata."""
        departments = job_data.get("departments", [])
        if departments and len(departments) > 0:
            return departments[0].get("name")
        return None
