"""Job filtering and processing logic."""

from dataclasses import dataclass
from typing import Optional
from .config import (
    TITLE_INCLUDE_KEYWORDS,
    TITLE_EXCLUDE_KEYWORDS,
    LOCATION_KEYWORDS,
)


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


class JobProcessor:
    """Filters and processes job listings."""

    def __init__(
        self,
        include_keywords: list[str] = None,
        exclude_keywords: list[str] = None,
        location_keywords: list[str] = None,
    ):
        self.include_keywords = [
            k.lower() for k in (include_keywords or TITLE_INCLUDE_KEYWORDS)
        ]
        self.exclude_keywords = [
            k.lower() for k in (exclude_keywords or TITLE_EXCLUDE_KEYWORDS)
        ]
        self.location_keywords = [
            k.lower() for k in (location_keywords or LOCATION_KEYWORDS)
        ]

    def filter_jobs(self, jobs: list[Job]) -> list[Job]:
        """Filter jobs based on title and location criteria."""
        filtered = []
        for job in jobs:
            if self._matches_criteria(job):
                filtered.append(job)
        return filtered

    def _matches_criteria(self, job: Job) -> bool:
        """Check if a job matches all filter criteria."""
        return (
            self._matches_title_include(job.title) and
            not self._matches_title_exclude(job.title) and
            self._matches_location(job.location)
        )

    def _matches_title_include(self, title: str) -> bool:
        """Check if title contains any include keyword."""
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.include_keywords)

    def _matches_title_exclude(self, title: str) -> bool:
        """Check if title contains any exclude keyword."""
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.exclude_keywords)

    def _matches_location(self, location: str) -> bool:
        """Check if location matches any location keyword."""
        if not location:
            return False
        location_lower = location.lower()
        return any(keyword in location_lower for keyword in self.location_keywords)

    def deduplicate(self, jobs: list[Job]) -> list[Job]:
        """Remove duplicate jobs based on URL."""
        seen_urls = set()
        unique_jobs = []
        for job in jobs:
            if job.url not in seen_urls:
                seen_urls.add(job.url)
                unique_jobs.append(job)
        return unique_jobs

    def sort_by_company(self, jobs: list[Job]) -> list[Job]:
        """Sort jobs alphabetically by company name."""
        return sorted(jobs, key=lambda j: j.company.lower())

    def sort_by_date(self, jobs: list[Job]) -> list[Job]:
        """Sort jobs by posting date, newest first."""
        def get_date_key(job: Job) -> str:
            # Return posted_at if available, otherwise empty string (sorts last)
            return job.posted_at or ""
        return sorted(jobs, key=get_date_key, reverse=True)
