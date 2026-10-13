"""Download recent Google Play reviews and rank recurring issue categories."""

from __future__ import annotations

import argparse
import csv
import re
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable


APP_ID = "com.razorpay.payments.app"
ISSUE_PATTERNS = {
    "Payment failures": r"\b(payment|transaction|transact|pay|paid|debit|deduct|failed|failure|declin(?:e|ed))\b",
    "Refunds and reversals": r"\b(refund|revers(?:e|al)|chargeback|money back|credited back)\b",
    "Login and OTP": r"\b(login|log in|sign in|otp|one.?time password|verification code|authentication)\b",
    "App crashes and performance": r"\b(crash(?:es|ed)?|freeze|freez(?:es|ing)|slow|lag(?:gy)?|hang(?:s|ing)?|loading| not responding)\b",
    "Account and KYC": r"\b(account|kyc|verification|verify|blocked|suspend(?:ed)?|limit|pan card)\b",
    "Customer support": r"\b(support|customer care|help.?line|service request|complaint|ticket|agent)\b",
    "UPI and QR payments": r"\b(upi|qr code|qr scan|scan and pay|vpa|upi id)\b",
    "Fees and charges": r"\b(fee|fees|charge|charges|commission|hidden cost|extra cost)\b",
    "Notifications and receipts": r"\b(notification|alert|receipt|invoice|confirmation|sms|message)\b",
    "Usability and navigation": r"\b(confus(?:ing|ed)|difficult|hard to use|user.?friendly|interface|navigation|design)\b",
}


def collect_reviews(
    fetch_page: Callable[..., tuple[list[dict[str, Any]], Any]],
    cutoff: datetime,
    delay: float = 0.5,
) -> list[dict[str, Any]]:
    """Fetch newest reviews until a page reaches the cutoff."""
    collected: list[dict[str, Any]] = []
    continuation_token = None

    while True:
        page, continuation_token = fetch_page(
            count=200,
            continuation_token=continuation_token,
        )
        if not page:
            break

        older_review_found = False
        for review in page:
            review_date = review.get("at")
            if review_date is None:
                continue
            if review_date.tzinfo is None:
                review_date = review_date.replace(tzinfo=timezone.utc)
            if review_date < cutoff:
                older_review_found = True
            else:
                collected.append(review)

        if older_review_found or continuation_token is None:
            break
        if delay > 0:
            time.sleep(delay)

    return collected


def find_issues(text: str) -> list[str]:
    normalized = text.lower()
    return [
        category
        for category, pattern in ISSUE_PATTERNS.items()
        if re.search(pattern, normalized)
    ]


def rank_issues(reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for review in reviews:
        if int(review.get("score", 5)) > 3:
            continue
        for category in find_issues(str(review.get("content", ""))):
            grouped[category].append(review)

    rankings = []
    for category, matches in grouped.items():
        rankings.append(
            {
                "issue": category,
                "reviews_mentioning_issue": len(matches),
                "average_rating": round(
                    sum(int(review.get("score", 0)) for review in matches) / len(matches),
                    2,
                ),
                "latest_mention": max(review["at"] for review in matches).isoformat(),
                "example_reviews": " | ".join(
                    str(review.get("content", "")).replace("\n", " ")[:240]
                    for review in matches[:3]
                ),
            }
        )
    return sorted(
        rankings,
        key=lambda item: (-item["reviews_mentioning_issue"], item["average_rating"]),
    )


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape recent Google Play reviews and rank recurring issues."
    )
    parser.add_argument("--app-id", default=APP_ID)
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--lang", default="en")
    parser.add_argument("--country", default="in")
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()

    if args.days < 1:
        parser.error("--days must be at least 1")
    if args.delay < 0:
        parser.error("--delay cannot be negative")

    try:
        from google_play_scraper import Sort, reviews
    except ImportError as error:
        raise SystemExit(
            "Missing dependency. Install it with: python -m pip install -r requirements.txt"
        ) from error

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=args.days)
    fetch_page = lambda **kwargs: reviews(
        args.app_id,
        lang=args.lang,
        country=args.country,
        sort=Sort.NEWEST,
        **kwargs,
    )
    recent_reviews = collect_reviews(fetch_page, cutoff, args.delay)
    review_rows = [
        {
            "review_id": review.get("reviewId", ""),
            "date": review["at"].isoformat(),
            "rating": review.get("score", ""),
            "text": review.get("content", ""),
            "thumbs_up": review.get("thumbsUpCount", 0),
            "developer_reply": review.get("replyContent", "") or "",
        }
        for review in recent_reviews
    ]
    rankings = rank_issues(recent_reviews)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        args.output_dir / "reviews.csv",
        review_rows,
        ["review_id", "date", "rating", "text", "thumbs_up", "developer_reply"],
    )
    write_csv(
        args.output_dir / "issue_rankings.csv",
        rankings,
        [
            "issue",
            "reviews_mentioning_issue",
            "average_rating",
            "latest_mention",
            "example_reviews",
        ],
    )

    print(f"Collected {len(recent_reviews)} reviews since {cutoff.date()}.")
    print(f"Saved raw reviews to {args.output_dir / 'reviews.csv'}")
    print(f"Saved issue rankings to {args.output_dir / 'issue_rankings.csv'}")
    if not rankings:
        print("No matching issue categories found in reviews rated 3 stars or lower.")
    else:
        print("Top issues (low-rated reviews only):")
        for item in rankings[:10]:
            print(f"  {item['issue']}: {item['reviews_mentioning_issue']} reviews")


if __name__ == "__main__":
    main()