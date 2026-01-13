# Runbook (Demo)

## Common issues

### API returns 401
- Missing token or wrong scopes
- Generate a token:
  - `docker compose exec api python -m app.scripts.generate_token --scopes telemetry:write alerts:read`

### No alerts show up
- Worker might not be running
  - `docker compose ps`
  - `docker compose logs -f worker`
- Telemetry might not trigger rules (try temperature_c=82, battery_pct=12)

### Postgres connection errors
- Wait for postgres container to be ready
- Reset state:
  - `docker compose down -v`
  - `docker compose up --build`

### Queue backlog / slow processing
- Check Redis health:
  - `docker compose exec redis redis-cli ping`
- For Redis Streams:
  - Inspect stream length:
    - `docker compose exec redis redis-cli XLEN telemetry-events`
