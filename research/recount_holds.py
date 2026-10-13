"""Recount one-star Google Play reviews that mention held funds or suspended accounts.

Usage: python research/recount_holds.py data/reviews.csv

Keyword tagging is approximate: it misses some Hinglish phrasing and catches a few
false positives, so treat the result as directional, not a prevalence estimate.
"""
import re
import sys

import pandas as pd

HOLD = r"\b(on hold|hold(?:s|ing)?|held|fr[eo]ze[n]?|freez\w*|block(?:ed|ing)?|suspend\w*|deactivat\w*|disabled?|under review|risk (?:team|review)|stuck|withheld|not releas\w*|ban(?:ned)?)\b"
MONEY = r"\b(account|money|amount|payment\w*|balance|settlement\w*|settle[ds]?|payout\w*|funds?)\b"
THEMES = {
    "Settlement or payout problems": r"\b(settlement\w*|settle[ds]?|payout\w*|not (?:received|credited)|money not|funds?)\b",
    "Support unresponsive": r"\b(support|customer care|customer service|no response|no reply|ticket|helpline|call back)\b",
    "KYC, activation, verification": r"\b(kyc|document\w*|onboard\w*|activat\w*|verif\w*)\b",
    "App bugs, login, OTP": r"\b(crash\w*|log ?out|logged out|login|log in|otp|loading|slow|bug\w*|not working|not opening)\b",
}


def main(path: str) -> None:
    df = pd.read_csv(path)
    text = df["text"].fillna("").str.lower()
    one_star = df["rating"] == 1
    n = int(one_star.sum())
    holds = one_star & text.str.contains(HOLD, regex=True) & text.str.contains(MONEY, regex=True)
    print(f"Reviews: {len(df)} | one-star: {n}")
    print(f"Held funds or suspended account: {int(holds.sum())} ({holds.sum() / n:.1%} of one-star)")
    for name, pattern in THEMES.items():
        hits = one_star & text.str.contains(pattern, regex=True)
        print(f"{name}: {int(hits.sum())} ({hits.sum() / n:.1%})")


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    main(sys.argv[1] if len(sys.argv) > 1 else "data/reviews.csv")
