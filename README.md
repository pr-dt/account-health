# Account Health

Submission for the Razorpay x ISB AI PM Build Challenge, Track 2 (Recover and Grow with AI). Priya Dutta, PGP 2027.

**Live prototype:** https://razorpay-account-health-demo.lovable.app/
All merchant data in the prototype is synthetic.

Account Health is a proposed section of the Razorpay merchant dashboard. It warns a merchant before their settlements are held, explains a hold in plain language when one happens, and builds an action plan that hands each step to an existing agent or to the merchant, who approves it.

## What's in this repo

| Path | What it is |
|---|---|
| `research/scrape_reviews.py` | Scrapes Google Play reviews of the Razorpay Payments app and does a first keyword pass. I ran it to collect the dataset. |
| `research/recount_holds.py` | The recount behind the number in the note: 32 of 234 one-star reviews (13.7%) mention held funds or suspended accounts. |
| `data/reviews.csv` | 432 public reviews, Sep 2025 to Sep 2026. Developer replies removed because they contain reviewers' names. |
| `prompts/lovable-prompt.md` | The prompt the prototype was built from in Lovable. |
| `docs/` | The product note and the AI build log. |

## Reproduce the review numbers

```bash
pip install -r requirements.txt
python research/recount_holds.py data/reviews.csv
```

Expected output: 432 reviews, 234 one-star, 32 (13.7%) about held funds or suspended accounts. Keyword tagging is approximate, so treat this as directional evidence of the pain, not a measure of how often holds happen.

## Architecture (proposed)

The prototype is front-end only with synthetic data. In production, it would work like this:

1. **Rules layer (deterministic, auditable).** Computes the health score and its drivers (chargeback rate, refund rate, delivery-proof coverage, KYC expiry) against fixed limits, and fires an alert when a driver crosses a watch level. Also enforces permissions: what the merchant may approve, and what no one can do from this product (release settlements, change risk decisions).
2. **AI layer (runs only when a rule fires).** Reads free-text chargeback reasons, joins them to order and shipping records, finds patterns (for example, 9 of 14 chargebacks linked to one courier), writes an explanation that cites only real fields, and ranks the next steps.
3. **Hand-off layer.** Each step goes to an existing agent (for example, chargeback evidence to Dispute Responder) or to the merchant. Nothing runs without merchant approval, and every action is logged.
4. **Learning loop.** Each plan records which steps were taken and how the hold ended. Outcomes re-rank future plans; a randomised holdout group separates cause from coincidence.

## Guardrails

- Exact limits are shown only to established merchants; new merchants see bands, so the rules can't be gamed.
- AML and fraud-led holds are never explained; the product says the reason can't be shared.
- The AI cannot move money or change risk decisions.
- A pattern is shown as a pattern, not a proven cause. The courier is flagged to check, never switched automatically.

## Tools used

Claude (research, code, drafting, testing), Lovable (prototype), Perplexity and ChatGPT (early research and critique), the open-source `google-play-scraper` Python library (review data). Details are in the AI build log in `docs/`.
