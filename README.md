# EVENT STATE TRACKER

A small Python CLI tool that reads login/logout events and shows which users are currently active on each pc.

It also calculates session durations:
- **completed sessions** (login → logout)
- **active sessions** (online now, based on last login time)

This small tool demonstrates event-driven state tracking - a common pattern in monitoring and automation.

## Input format

`data/events.json` is a list of events:

```json
[
 {"date": "2026-02-24T09:00:00", "machine": "lab-pc-1", "user": "dias", "type": "login"},
 {"date": "2026-02-24T09:20:00", "machine": "lab-pc-1", "user": "dias", "type": "logout"}
]
```

## How to run

```bash
py main.py data/events.json
```
Output:
- printed to the terminal
- saved report to `docs/report.json`

## Reason

I built this to practice automation and system monitoring basics: turning events into a reliable, reproducible report.

## Example output

```text
lab-pc-1 | dias: 20.0 min (completed)
lab-pc-1 | aidan: 12.4 min (active now, since 2026-02-24 09:05:00)
```