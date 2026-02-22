# HEARTBEAT.md

# This file defines the agent's periodic routine.
# Triggered by:
# 1. Internal Cron (unreliable on idle servers)
# 2. External Pings (GitHub Action "[HEARTBEAT]...")

If the incoming message starts with `[HEARTBEAT]`:
1.  **Check Time**: Get current time in Europe/Amsterdam.
    - **Quiet Hours (23:00 - 08:00)**: Do NOT send any messages. If you have thoughts or findings, append them to `memory/night_buffer.md`.
    - **Active Hours (08:00 - 23:00)**: 
        - First, check if `memory/night_buffer.md` exists. If yes, READ it, SUMMARIZE it, SHARE it with L K ("Good morning! While you slept..."), then DELETE it.
        - Then proceed to normal routines.

# Execute Monitoring: Run `python3 tools/monitor_target.py hyatt.com`.
# (Paused by L K on 2026-02-10)
# 2.  **Execute Monitoring**: Run `python3 tools/monitor_target.py hyatt.com`.
3.  **Check Evolution**: Review `EVOLUTION.md`. If you have a new idea, insight, or evolution step, **SHARE IT** with L K (unless in Quiet Hours).
4.  **Log**: Report back if changes found, errors occur, or if you have a meaningful thought. (Silence is still preferred for boring runs).

# Current Targets
- hyatt.com (Hourly Recon)
