#!/usr/bin/env python3
"""Main entry point for job search agent."""

import sys
import argparse
from dataclasses import dataclass
from typing import Optional

from .config import (
    GREENHOUSE_COMPANIES,
    ASHBY_COMPANIES,
    LEVER_COMPANIES,
)
from .fetchers import GreenhouseFetcher, AshbyFetcher, LeverFetcher
from .processor import JobProcessor
from .storage import JobStorage
from .notifier import EmailNotifier


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


def fetch_all_jobs() -> list[Job]:
    """Fetch jobs from all configured companies."""
    all_jobs = []

    # Fetch from Greenhouse companies
    print(f"\nFetching from {len(GREENHOUSE_COMPANIES)} Greenhouse companies...")
    for slug, name in GREENHOUSE_COMPANIES:
        fetcher = GreenhouseFetcher(slug, name)
        jobs = fetcher.fetch_jobs()
        # Convert to common Job type
        for j in jobs:
            all_jobs.append(Job(
                id=j.id, title=j.title, company=j.company,
                location=j.location, url=j.url,
                posted_at=j.posted_at, department=j.department
            ))
        print(f"  {name}: {len(jobs)} jobs")

    # Fetch from Ashby companies
    print(f"\nFetching from {len(ASHBY_COMPANIES)} Ashby companies...")
    for slug, name in ASHBY_COMPANIES:
        fetcher = AshbyFetcher(slug, name)
        jobs = fetcher.fetch_jobs()
        for j in jobs:
            all_jobs.append(Job(
                id=j.id, title=j.title, company=j.company,
                location=j.location, url=j.url,
                posted_at=j.posted_at, department=j.department
            ))
        print(f"  {name}: {len(jobs)} jobs")

    # Fetch from Lever companies
    print(f"\nFetching from {len(LEVER_COMPANIES)} Lever companies...")
    for slug, name in LEVER_COMPANIES:
        fetcher = LeverFetcher(slug, name)
        jobs = fetcher.fetch_jobs()
        for j in jobs:
            all_jobs.append(Job(
                id=j.id, title=j.title, company=j.company,
                location=j.location, url=j.url,
                posted_at=j.posted_at, department=j.department
            ))
        print(f"  {name}: {len(jobs)} jobs")

    return all_jobs


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Job Search Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without sending emails"
    )
    parser.add_argument(
        "--no-filter",
        action="store_true",
        help="Skip filtering, show all jobs"
    )
    parser.add_argument(
        "--reset-history",
        action="store_true",
        help="Clear job history and treat all jobs as new"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Job Search Agent")
    print("=" * 60)

    # Calculate total companies
    total_companies = (
        len(GREENHOUSE_COMPANIES) +
        len(ASHBY_COMPANIES) +
        len(LEVER_COMPANIES)
    )
    print(f"Monitoring {total_companies} companies")

    # Initialize components
    processor = JobProcessor()
    storage = JobStorage()
    notifier = EmailNotifier(dry_run=args.dry_run)

    # Reset history if requested
    if args.reset_history:
        print("\nResetting job history...")
        storage.seen_jobs = {}
        storage._save()

    # Fetch all jobs
    print("\nFetching jobs...")
    all_jobs = fetch_all_jobs()
    print(f"\nTotal jobs fetched: {len(all_jobs)}")

    # Filter jobs
    if args.no_filter:
        filtered_jobs = all_jobs
        print(f"Skipping filters (--no-filter)")
    else:
        filtered_jobs = processor.filter_jobs(all_jobs)
        print(f"Jobs matching criteria: {len(filtered_jobs)}")

    # Deduplicate
    unique_jobs = processor.deduplicate(filtered_jobs)
    print(f"After deduplication: {len(unique_jobs)}")

    # Identify new jobs (not seen before)
    new_jobs = storage.filter_new_jobs(unique_jobs)
    print(f"New jobs (not seen before): {len(new_jobs)}")

    # Sort all jobs by location priority (SF first, Remote second), then by date
    all_sorted = processor.sort_by_location_then_date(unique_jobs)

    # Get top 5 "hot" jobs prioritizing SF and Remote locations
    hot_jobs = processor.sort_by_location_then_date(new_jobs)[:5]

    # Print job details
    print("\n" + "-" * 60)
    print(f"HOT NEW JOBS ({len(hot_jobs)}):")
    print("-" * 60)
    for job in hot_jobs:
        print(f"\n{job.title}")
        print(f"  Company:  {job.company}")
        print(f"  Location: {job.location}")
        if job.department:
            print(f"  Team:     {job.department}")
        print(f"  URL:      {job.url}")

    print("\n" + "-" * 60)
    print(f"ALL OPEN POSITIONS ({len(all_sorted)}):")
    print("-" * 60)
    for job in all_sorted[:20]:  # Show first 20 in console
        print(f"  - {job.title} @ {job.company}")
    if len(all_sorted) > 20:
        print(f"  ... and {len(all_sorted) - 20} more")

    # Send email notification with hot jobs and all jobs
    print("\n" + "=" * 60)
    print("Sending notification...")
    success = notifier.send_digest(
        hot_jobs=hot_jobs,
        all_jobs=all_sorted,
        company_count=total_companies
    )

    if success:
        # Sync storage with current open jobs
        # This adds new jobs and removes closed ones
        storage.sync_with_current_jobs(unique_jobs)
        print(f"Tracking {len(unique_jobs)} open positions")

    print("\nDone!")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
