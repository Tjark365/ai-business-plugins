# Production architecture

## Repository
This repository contains the 20 plugin cores, tests, manifests and CI.

## Runtime
GitHub is source control and CI, not the production API runtime. Each plugin must be exposed through a cloud-hosted plugin/MCP runtime before public use.

## Entitlements
The plugin core accepts a Pro entitlement from the host. The client must never be trusted to grant itself Pro access. Production authentication should verify the signed/session entitlement server-side and pass only a boolean capability into the core.

## Free / Pro
Free returns a useful preview and never exposes the full Pro workflow.
Pro returns the complete structured workflow.

## Research integrity
Current market, funding, tender, M&A and competitive claims require source evidence. Facts, inferences and recommendations should remain separate.

## Paywall
Payment provider, pricing pages, checkout and entitlement issuance are intentionally not hard-coded into the repository. They are configured at the hosting/paywall stage.

## Launch checklist
1. Deploy runtime.
2. Configure server-side entitlement verification.
3. Connect payment provider.
4. Map each plan to plugin entitlements.
5. Test Free → checkout → Pro access.
6. Test cancellation/expiry → Free access.
7. Run all CI tests.
8. Publish only after end-to-end verification.
