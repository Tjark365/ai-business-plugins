# Plugin Specification

## Inputs
- Offer
- Ideal customer profile (ICP)
- Geography
- Industry
- Company size/revenue
- Exclusions
- Lead count

If inputs are missing, infer sensible defaults and state assumptions.

## Output
Show the top 3 first, followed by a ranked table containing:
- Company
- Location
- Fit rationale
- Current signal
- Source
- Likely buyer role
- Estimated opportunity value
- Score
- Confidence
- Next action

Clearly separate verified facts from inference.

## Entitlement
If the host does not provide Pro entitlement, do not bypass it. Return the Free preview instead.
