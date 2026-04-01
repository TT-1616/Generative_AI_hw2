# Prompt Iteration Notes

## Initial Version

```text
You are a helpful customer support assistant.
Write an email reply to the customer based on the information provided.
Be polite and professional.
```

Why I started here:
This baseline prompt was intentionally simple so I could see the model's default behavior before adding stronger constraints.

What happened:
The replies were usually fluent, but they sometimes sounded too generic and occasionally overpromised actions that were not supported by the policy notes.

## Revision 1

```text
You are drafting a first-pass customer support email for a human agent to review.

Goals:
- Be polite, calm, and concise.
- Use only the facts provided in the case data.
- Follow policy notes exactly.
- If the information is incomplete or risky, say that human review or verification is needed.

Output format:
1. Subject line
2. Customer-facing reply
3. Internal note: 1-2 sentences on risk, ambiguity, or review needs
```

What changed and why:
I added the "first-pass draft" framing, told the model to stay inside the provided facts, and required an internal note so risky cases would surface uncertainty instead of hiding it.

What improved or stayed weak:
This improved factual discipline and made the outputs easier to review, but some replies were still wordy and a few cases still included vague assurances.

## Revision 2

```text
You are drafting a first-pass customer support email for a human support specialist.

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
Internal review note:
```

What changed and why:
I added hard constraints against hallucinating policies and outcomes, made escalation conditions explicit, and narrowed the target length so the reply would stay usable for a real support workflow.

What improved, stayed the same, or got worse:
The final prompt produced more reliable and reviewable drafts, especially on refund, privacy, and account-access cases. The tradeoff is that some replies became slightly less warm and more templated, but the reduction in risk was worth it.

