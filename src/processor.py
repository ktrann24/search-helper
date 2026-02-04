"""Job filtering and processing logic."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .config import (
    TITLE_INCLUDE_KEYWORDS,
    TITLE_EXCLUDE_KEYWORDS,
    LOCATION_KEYWORDS,
    LOCATION_PRIORITY,
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


def is_general_ledger_job(job: Job) -> bool:
    """Check if a job specifically mentions general ledger in title or department."""
    text_to_check = f"{job.title} {job.department or ''}".lower()
    return "general ledger" in text_to_check or "gl accountant" in text_to_check


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

    def _get_location_priority(self, location: str) -> int:
        """
        Get priority score for a location (lower = higher priority).
        Returns:
            1 = San Francisco (highest priority)
            2 = Remote
            3 = Other matching locations
            999 = No match
        """
        if not location:
            return 999

        location_lower = location.lower()
        best_priority = 999

        for keyword, priority in LOCATION_PRIORITY.items():
            if keyword in location_lower:
                best_priority = min(best_priority, priority)

        return best_priority

    def _date_to_timestamp(self, date_str: str) -> int:
        """Convert date string to Unix timestamp for sorting."""
        if not date_str:
            return 0
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return int(dt.timestamp())
        except (ValueError, AttributeError):
            return 0

    def sort_by_location_then_date(self, jobs: list[Job]) -> list[Job]:
        """
        Sort jobs by location priority (SF first, Remote second, Others third),
        then by date (newest first) within each location tier.
        """
        def get_sort_key(job: Job) -> tuple:
            location_priority = self._get_location_priority(job.location)
            # Negate timestamp so newest sorts first
            date_key = -self._date_to_timestamp(job.posted_at or "")
            return (location_priority, date_key)

        return sorted(jobs, key=get_sort_key)
