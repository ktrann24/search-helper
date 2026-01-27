"""Job history storage for tracking seen jobs."""

import json
import os
from datetime import datetime
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


class JobStorage:
    """Tracks job history for identifying new vs existing jobs."""

    def __init__(self, storage_path: str = "job_history.json"):
        self.storage_path = storage_path
        self.seen_jobs: dict[str, dict] = {}
        self._load()

    def _load(self):
        """Load job history from file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    self.seen_jobs = data.get("jobs", {})
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load job history: {e}")
                self.seen_jobs = {}

    def _save(self):
        """Save job history to file."""
        try:
            data = {
                "last_updated": datetime.utcnow().isoformat(),
                "jobs": self.seen_jobs,
            }
            with open(self.storage_path, "w") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save job history: {e}")

    def is_new(self, job: Job) -> bool:
        """Check if a job has not been seen before."""
        return job.id not in self.seen_jobs

    def get_first_seen(self, job: Job) -> Optional[str]:
        """Get when a job was first seen, or None if new."""
        if job.id in self.seen_jobs:
            return self.seen_jobs[job.id].get("first_seen")
        return None

    def filter_new_jobs(self, jobs: list[Job]) -> list[Job]:
        """Return only jobs that haven't been seen before."""
        return [job for job in jobs if self.is_new(job)]

    def sync_with_current_jobs(self, current_jobs: list[Job]):
        """
        Update storage to match currently open jobs.
        - Add new jobs with first_seen timestamp
        - Remove jobs that are no longer open (filled/closed)
        """
        current_job_ids = {job.id for job in current_jobs}

        # Remove jobs that are no longer open
        closed_jobs = [
            job_id for job_id in self.seen_jobs
            if job_id not in current_job_ids
        ]
        for job_id in closed_jobs:
            del self.seen_jobs[job_id]

        if closed_jobs:
            print(f"Removed {len(closed_jobs)} closed/filled jobs from history")

        # Add new jobs
        new_count = 0
        for job in current_jobs:
            if job.id not in self.seen_jobs:
                self.seen_jobs[job.id] = {
                    "title": job.title,
                    "company": job.company,
                    "url": job.url,
                    "first_seen": datetime.utcnow().isoformat(),
                }
                new_count += 1

        if new_count:
            print(f"Added {new_count} new jobs to history")

        self._save()

    def get_stats(self) -> dict:
        """Get storage statistics."""
        return {
            "total_tracked": len(self.seen_jobs),
            "storage_path": self.storage_path,
        }
