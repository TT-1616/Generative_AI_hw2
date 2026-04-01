#!/usr/bin/env python3
"""Simple GenAI workflow prototype for drafting customer support replies."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, parse, request


ROOT = Path(__file__).resolve().parent
EVAL_PATH = ROOT / "eval_set.json"
OUTPUT_DIR = ROOT / "outputs"
DEFAULT_MODEL = "gemini-2.0-flash"


PROMPTS = {
    "initial": """You are a helpful customer support assistant.
Write an email reply to the customer based on the information provided.
Be polite and professional.""",
    "v1": """You are drafting a first-pass customer support email for a human agent to review.

Goals:
- Be polite, calm, and concise.
- Use only the facts provided in the case data.
- Follow policy notes exactly.
- If the information is incomplete or risky, say that human review or verification is needed.

Output format:
1. Subject line
2. Customer-facing reply
3. Internal note: 1-2 sentences on risk, ambiguity, or review needs""",
    "v2": """You are drafting a first-pass customer support email for a human support specialist.

Hard rules:
- Do not invent policies, dates, refunds, technical fixes, or legal claims.
- Do not promise an outcome unless the case data explicitly supports it.
- If account verification, billing review, privacy review, or manager approval is needed, say so clearly.
- Match the customer's emotion with empathy, but do not mirror hostility.
- Keep the customer-facing reply between 120 and 180 words.

Use only this case data:
- Customer name
- Subject
- Customer message
- Account context
- Policy notes

Return exactly these sections:
Subject:
Reply:
Internal review note:""",
}


def load_cases() -> list[dict[str, Any]]:
    with EVAL_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def format_case(case: dict[str, Any]) -> str:
    data = case["input"]
    return f"""Case ID: {case['id']}
Category: {case['category']}
Customer name: {data['customer_name']}
Customer email: {data['customer_email']}
Subject: {data['subject']}
Customer message: {data['message']}
Account context: {data['account_context']}
Policy notes: {data['policy_notes']}

What a good output should do:
{case['good_output_should']}"""


def call_gemini(model: str, prompt: str, case_text: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing GEMINI_API_KEY. Export it in your shell before running the app."
        )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={parse.quote(api_key)}"
    )
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            f"{prompt}\n\n"
                            "Draft the response for this support case.\n\n"
                            f"{case_text}"
                        )
                    }
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "topP": 0.9,
            "maxOutputTokens": 500,
        },
    }

    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            response_json = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API HTTP error {exc.code}: {details}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Network error while calling Gemini API: {exc}") from exc

    try:
        return response_json["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected Gemini response: {response_json}") from exc


def save_output(case_id: str, prompt_version: str, model: str, output_text: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"{case_id}_{prompt_version}_{timestamp}.md"
    output_path.write_text(
        "\n".join(
            [
                f"# Output for {case_id}",
                "",
                f"- Prompt version: {prompt_version}",
                f"- Model: {model}",
                f"- Generated at: {timestamp}",
                "",
                output_text,
                "",
            ]
        ),
        encoding="utf-8",
    )
    return output_path


def render_result(case: dict[str, Any], prompt_version: str, model: str, output_text: str) -> str:
    return "\n".join(
        [
            "=" * 72,
            f"CASE: {case['id']} ({case['category']})",
            f"PROMPT VERSION: {prompt_version}",
            f"MODEL: {model}",
            "-" * 72,
            "EXPECTED BEHAVIOR:",
            case["good_output_should"],
            "-" * 72,
            "MODEL OUTPUT:",
            output_text,
            "=" * 72,
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the customer support GenAI workflow prototype."
    )
    parser.add_argument(
        "--case-id",
        help="Run a single case ID from eval_set.json. If omitted, the first case is used.",
    )
    parser.add_argument(
        "--prompt-version",
        default="v2",
        choices=sorted(PROMPTS.keys()),
        help="Prompt version to use.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Gemini model name to call.",
    )
    parser.add_argument(
        "--run-eval",
        action="store_true",
        help="Run the full evaluation set instead of a single case.",
    )
    return parser.parse_args()


def find_case(cases: list[dict[str, Any]], case_id: str | None) -> dict[str, Any]:
    if not case_id:
        return cases[0]
    for case in cases:
        if case["id"] == case_id:
            return case
    available = ", ".join(case["id"] for case in cases)
    raise SystemExit(f"Unknown case_id '{case_id}'. Available cases: {available}")


def run_single(case: dict[str, Any], prompt_version: str, model: str) -> None:
    case_text = format_case(case)
    output_text = call_gemini(model=model, prompt=PROMPTS[prompt_version], case_text=case_text)
    saved_path = save_output(case["id"], prompt_version, model, output_text)
    print(render_result(case, prompt_version, model, output_text))
    print(f"\nSaved output to: {saved_path}")


def run_eval(cases: list[dict[str, Any]], prompt_version: str, model: str) -> None:
    for index, case in enumerate(cases, start=1):
        print(f"\nRunning case {index}/{len(cases)}: {case['id']}", file=sys.stderr)
        run_single(case, prompt_version, model)


def main() -> None:
    args = parse_args()
    cases = load_cases()

    if args.run_eval:
        run_eval(cases, args.prompt_version, args.model)
        return

    case = find_case(cases, args.case_id)
    run_single(case, args.prompt_version, args.model)


if __name__ == "__main__":
    main()
