# Generative AI Homework 2

## Repository Overview

This project builds and evaluates a simple GenAI workflow for drafting first-pass customer support email replies.

## Business Workflow

- Workflow chosen: drafting customer support responses
- User: a customer support specialist at a software company
- Input: a customer message, order/account context, and any support policy notes
- Output: a polite, accurate first-draft email reply with a short internal risk note
- Why this task is valuable: support teams spend significant time drafting repetitive replies, but accuracy and tone still matter enough that a human should review the draft before sending

## Files

- `app.py`: command-line Python prototype that calls a Gemini model
- `prompts.md`: prompt versions and iteration notes
- `eval_set.json`: stable evaluation set with six representative cases
- `report.md`: short written report on the system design and results

## How To Run

1. Create a Gemini API key in Google AI Studio.
2. Set your API key in the terminal:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

3. Run one case with the final prompt:

```bash
python3 app.py --case-id normal_refund_delay --prompt-version v2
```

4. Run the whole evaluation set:

```bash
python3 app.py --run-eval --prompt-version v2
```

Outputs are printed to the terminal and saved in the `outputs/` folder.

## Recommended Model

The prototype defaults to `gemini-2.0-flash` because it is fast, inexpensive, and strong enough for structured drafting tasks.

## Human Review Boundary

The generated reply should be treated as a draft only. A human should review any case involving billing disputes, legal threats, ambiguous account details, refunds outside policy, or missing context.

## Video Link

Add your final walkthrough video link here before submission:

- Video: `PASTE_YOUR_UNLISTED_VIDEO_LINK_HERE`

