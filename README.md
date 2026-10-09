# review-reply-autopilot

> Draft safe, on-brand replies to Google/Yelp/Facebook reviews in seconds - and automatically **hold** the risky ones (legal threats, safety claims, fraud accusations) for the owner.

![python](https://img.shields.io/badge/python-3.8%2B-blue) ![deps](https://img.shields.io/badge/dependencies-0-brightgreen) ![license](https://img.shields.io/badge/license-MIT-lightgrey) ![ci](https://img.shields.io/badge/tests-unittest-success)

## Quickstart (under 2 minutes, no install, no API key)

```bash
git clone https://github.com/Waqas-Ai-Engineer/review-reply-autopilot
cd review-reply-autopilot
python -m reviewreply examples/reviews.csv --business "Apex Roofing" --contact "office@apex.example"
```

Sample output (real output, see `examples/sample_output.txt`):

```
[ESCALATE] negative 1* James Carter: Technician was rude and two hours late. Overpriced and I'm c
           -> [HOLD - do not post. Owner must review: legal language detected]
(Suggested draft) Hi James, we're sorry your experience fell short ...
[LOW     ] positive 5* Maria Lopez: ...
           -> Thank you so much, Maria, for the kind words about Apex Roofing. ...
6 reviews, 2 need owner review before posting.
```

## What it does

- Classifies each review: sentiment, topic (timing, price, staff, quality, communication), priority.
- Drafts a polite reply that never promises refunds or admits liability.
- Flags **legal / regulator / safety / fraud / privacy** language and marks the draft `HOLD`.
- Output as terminal table, `--format json`, `--format csv` or a shareable `--format html` report.
- Optional LLM polish (`--llm`) with any OpenAI-compatible endpoint via `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`. Risky reviews are never sent for auto-polish.

## Input format

CSV with columns `name,rating,text` (export from your review tool or a Google Sheet).

## Architecture

```
reviews.csv -> classify() -> risk scan -> draft_reply() -> [optional LLM polish] -> table/json/csv/html
                                   \-> ESCALATE: HOLD for owner
```

Plug it into n8n: Schedule trigger -> Google Sheets (new reviews) -> Execute Command `python -m reviewreply ... --format json` -> Slack/email the ESCALATE items, post the rest after approval.

## Use cases

Roofing, HVAC, plumbing, clinics, dental, salons, real estate and restaurants - anywhere reviews drive leads and replies are neglected.

## Honest limits

Rule-based classification is a fast first pass, not a human. Always review before posting. No review-site posting is built in (platform APIs and terms differ).

## Tests

```bash
python -m unittest discover -s tests -v
```

## Hire me / Need this built?

**Muhammad Waqas - AI Agents & Business Automation.** I build review-management, lead-gen, WhatsApp/email automation and AI receptionist workflows for home-service businesses, clinics and agencies. Contact via my GitHub profile: [@Waqas-Ai-Engineer](https://github.com/Waqas-Ai-Engineer).

## Topics

`review-management` `reputation-management` `ai-automation` `python` `cli` `n8n` `local-business` `customer-feedback`

MIT licensed.
