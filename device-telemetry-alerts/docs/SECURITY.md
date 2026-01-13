# Security Notes (Portfolio-Friendly)

This demo includes security controls that are easy to explain in an interview.

## AuthN/AuthZ
- JWT bearer tokens (HS256) for simplicity
- Tokens include a `scopes` claim
- API endpoints enforce scopes:
  - `telemetry:write` for ingest
  - `alerts:read` for viewing alerts

## Input validation
- FastAPI + Pydantic schemas for strict request validation
- Telemetry stored as JSONB to preserve fields while keeping structure

## Rate limiting
- Redis-backed fixed-window limiter (demo)
- Shows the pattern; production systems typically use sliding window/leaky bucket and per-IP + per-tenant rules

## Logging and auditability
- In a real system, you'd ship structured logs and audit events to a central store
- This demo keeps it simple but is designed to be extended

## Secrets handling
- Local dev uses `.env` (not committed)
- Kubernetes manifest examples show `Secret` usage patterns
- Terraform example includes IAM least-privilege scaffolding for SQS/DynamoDB

## Secure coding practices
Suggested extensions (easy add-ons):
- mTLS between services
- WAF / API gateway
- OPA policy checks
- dependency scanning in CI (pip-audit)
