# EVENT STATE TRACKER

A small Python tracker that reads logins and logouts events and checks which users are currently active on each pc.

This small tool demonstrates event-driven state tracking (rebuilding current state from logs), a default pattern in monitoring and automation.

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
py main.py
```

(Output would be printed to the terminal and also saved to docs/report.json)

## Reason

I built this to practice automation and system monitoring basics: turning events into a reliable, reproducible report.

## Example output

lab-pc-1: aidan  
lab-pc-2: aru