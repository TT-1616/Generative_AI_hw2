# Report: Evaluating a GenAI Workflow for Customer Support Replies

## Business Use Case

I chose a workflow for drafting first-pass customer support email replies. The intended user is a support specialist at a software company who receives repetitive but high-stakes written requests involving billing, refunds, feature requests, account access, and privacy concerns. The system takes a customer message plus structured internal context and produces a draft reply that a human agent can review before sending.

This workflow is valuable because support teams often spend large amounts of time writing similar responses, but the replies still need strong tone control and policy compliance. A draft-generation workflow can save time while preserving human oversight on sensitive cases.

## Model Choice

I chose `gemini-2.0-flash` because it is fast, affordable, and easy to access through Google AI Studio. For this assignment, the task did not require complex reasoning or long context windows. The more important requirement was getting reasonably consistent structured writing output at low cost and with fast turnaround during prompt iteration.

## Baseline vs. Final Design

The baseline prompt simply asked the model to write a professional support email. That version sounded fluent, but it often behaved like a general writing assistant instead of a controlled support-drafting tool. In particular, it tended to be vague about uncertainty and sometimes implied resolutions too confidently.

The final design reframed the output as a first-pass draft for human review, required a fixed output structure, and added hard rules against inventing policies, dates, refunds, legal claims, or technical fixes. It also instructed the model to explicitly surface verification or escalation needs in an internal review note.

This prompt iteration improved the workflow in three ways. First, it reduced hallucinated commitments, especially in cases involving refunds outside policy or privacy requests. Second, it made risky cases easier to triage because the internal review note forced the model to state where human review was needed. Third, it produced more consistent outputs across the evaluation set, which made comparison fairer and repeatable.

## Remaining Failure Modes

The prototype still fails when the case data is incomplete or when the customer issue involves legal, compliance, billing, or security risk. In those situations, the model can still produce language that sounds more certain than the facts justify. It may also miss subtle business context, such as whether an apparent duplicate charge is actually a temporary authorization hold. For that reason, the system should not send replies automatically.

## Deployment Recommendation

I would recommend this workflow only as a draft-generation assistant with mandatory human review. It is most appropriate for common support scenarios where the company already has clear response policies. I would not recommend fully autonomous deployment for account recovery, legal threats, privacy deletion requests, or billing exceptions without stricter controls, stronger retrieval of policy documents, and a clear escalation path.

