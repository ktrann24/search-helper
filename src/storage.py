"""Job history storage for tracking seen jobs."""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
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
    """Tracks seen jobs to avoid duplicate notifications."""

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

    def mark_seen(self, job: Job):
        """Mark a job as seen."""
        self.seen_jobs[job.id] = {
            "title": job.title,
            "company": job.company,
            "url": job.url,
            "first_seen": datetime.utcnow().isoformat(),
        }

    def filter_new_jobs(self, jobs: list[Job]) -> list[Job]:
        """Return only jobs that haven't been seen before."""
        return [job for job in jobs if self.is_new(job)]

    def mark_jobs_seen(self, jobs: list[Job]):
        """Mark multiple jobs as seen and save."""
        for job in jobs:
            self.mark_seen(job)
        self._save()

    def get_stats(self) -> dict:
        """Get storage statistics."""
        return {
            "total_seen": len(self.seen_jobs),
            "storage_path": self.storage_path,
        }

    def cleanup_old_jobs(self, days: int = 90):
        """Remove jobs older than specified days."""
        cutoff = datetime.utcnow()
        to_remove = []

        for job_id, job_data in self.seen_jobs.items():
            first_seen = job_data.get("first_seen", "")
            if first_seen:
                try:
                    seen_date = datetime.fromisoformat(first_seen)
                    if (cutoff - seen_date).days > days:
                        to_remove.append(job_id)
                except ValueError:
                    pass

        for job_id in to_remove:
            del self.seen_jobs[job_id]

        if to_remove:
            self._save()
            print(f"Cleaned up {len(to_remove)} old job records")
