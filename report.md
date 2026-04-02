# Report: Evaluating a GenAI Workflow for Customer Support Replies

## Business Use Case

I chose a workflow for drafting first-pass customer support email replies. The intended user is a support specialist at a software company who receives repetitive but high-stakes written requests involving billing, refunds, feature requests, account access, and privacy concerns. The system takes a customer message plus structured internal context and produces a draft reply that a human agent can review before sending.

This workflow is valuable because support teams often spend large amounts of time writing similar responses, but the replies still need strong tone control and policy compliance. A draft-generation workflow can save time while preserving human oversight on sensitive cases.

## Model Choice

I initially planned to use `gemini-2.0-flash`, but in practice I ran into quota issues in Google AI Studio for that model. I then tested `gemini-2.5-flash`, which produced incomplete answers because too many tokens were spent on internal reasoning. The final working choice was `gemini-2.5-flash-lite`, which was available in my free-tier project and produced more reliable full-length responses for this assignment.

I chose the final model because this workflow is a structured writing task, not a deep reasoning task. The main need was consistent policy-aware drafting, not long chain-of-thought generation. `gemini-2.5-flash-lite` was a better fit for that constraint.

## Baseline vs. Final Design

The baseline prompt simply asked the model to write a professional support email. That version sounded fluent, but it often behaved like a general writing assistant instead of a controlled support-drafting tool. In particular, it tended to be vague about uncertainty and sometimes implied resolutions too confidently.

The final design reframed the output as a first-pass draft for human review, required a fixed output structure, and added hard rules against inventing policies, dates, refunds, legal claims, or technical fixes. It also instructed the model to explicitly surface verification or escalation needs in an internal review note.

This prompt iteration improved the workflow in three ways. First, it reduced hallucinated commitments, especially in cases involving refunds outside policy or privacy requests. Second, it made risky cases easier to triage because the internal review note forced the model to state where human review was needed. Third, it produced more consistent outputs across the evaluation set, which made comparison fairer and repeatable.

In the final evaluation run, the model performed well on the normal refund case by correctly explaining the 7-business-day window and not promising a specific posting date. It also handled the outside-policy refund case appropriately by declining to promise a refund and offering cancellation of future renewal instead. The account lockout and data deletion cases were also strong relative to the assignment goals, because the model acknowledged urgency while still requiring verification and escalation rather than inventing a shortcut.

The weakest final result was the double-charge case. The tone was calm and empathetic, and it correctly mentioned the possibility of an authorization hold, but it would be better if the reply included a clearer investigation timeline. The feature-request case was acceptable, but it still used somewhat generic product-language and suggested a workaround only in a vague way. These are good examples of outputs that are usable as drafts but still benefit from a human editor.

## Remaining Failure Modes

The prototype still fails when the case data is incomplete or when the customer issue involves legal, compliance, billing, or security risk. In those situations, the model can still produce language that sounds more certain than the facts justify. For example, in the refund-delay case it said the refund should appear within the next few business days, which is reasonable but still slightly more specific than the policy note. In the billing case, it did not include a precise follow-up timeline even though a human support workflow would usually need one.

The system also depends heavily on the quality of the provided context. If the policy notes are missing, ambiguous, or outdated, the response can still sound polished while being operationally weak. For that reason, the system should not send replies automatically.

## Deployment Recommendation

I would recommend this workflow only as a draft-generation assistant with mandatory human review. It is most appropriate for common support scenarios where the company already has clear response policies and where agents want help with tone, structure, and consistency. I would not recommend fully autonomous deployment for account recovery, legal threats, privacy deletion requests, or billing exceptions without stricter controls, stronger retrieval of policy documents, and a clear escalation path.

Overall, the final prototype demonstrates that a small prompt-driven workflow can save time on repetitive writing tasks, but the evaluation also shows that a human still needs to check policy-sensitive language before anything is sent to a customer.
