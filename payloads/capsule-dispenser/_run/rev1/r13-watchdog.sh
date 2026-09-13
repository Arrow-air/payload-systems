#!/bin/zsh
# Watchdog for the quiver-dock dispenser r13 close-out workflow host.
# No resumeFromRunId: cross-session resume cache proved broken (every relaunch
# re-ran the full prefix fresh). The continuation script is state-aware instead —
# a cheap probe agent reads on-disk markers and skips completed phases, so fresh
# relaunches are cheap by design. Session-limit deaths don't count against the
# restart budget. Exits when rev2/RUN-RESULT.md appears.
SCRIPT="/Users/hex/projects/payload-systems/payloads/capsule-dispenser/_run/rev1/closeout-r13-workflow.js"
RESULT="/Users/hex/projects/payload-systems/payloads/capsule-dispenser/_run/rev1/R13-RUN-RESULT.md"
LOG="/tmp/dispenser-r13-watchdog.log"
MARKER="headless host process for a long-running background workflow"
RESTARTS=0
MAX_RESTARTS=5
LAUNCHES=0
LAST_LOG=""

echo "$(date) continuation watchdog up (pid $$)" >> "$LOG"
while true; do
  if [ -f "$RESULT" ]; then
    echo "$(date) RUN-RESULT.md present — run complete, watchdog exiting" >> "$LOG"
    exit 0
  fi
  if ! pgrep -f "$MARKER" >/dev/null 2>&1; then
    if [ -n "$LAST_LOG" ] && grep -q "hit your session limit" "$LAST_LOG" 2>/dev/null; then
      echo "$(date) host died on session limit — waiting 15 min, not counting a restart" >> "$LOG"
      sleep 900
    elif [ -n "$LAST_LOG" ] && grep -q "Not logged in" "$LAST_LOG" 2>/dev/null; then
      echo "$(date) host died on transient auth error — waiting 5 min, not counting a restart" >> "$LOG"
      sleep 300
    elif [ "$RESTARTS" -ge "$MAX_RESTARTS" ]; then
      echo "$(date) host dead and restart budget exhausted ($MAX_RESTARTS) — giving up" >> "$LOG"
      exit 1
    else
      RESTARTS=$((RESTARTS+1))
    fi
    LAUNCHES=$((LAUNCHES+1))
    LAST_LOG="/tmp/dispenser-r13-host-L$LAUNCHES.log"
    echo "$(date) launching host #$LAUNCHES (restart count $RESTARTS/$MAX_RESTARTS)" >> "$LOG"
    CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 nohup caffeinate -i claude -p --dangerously-skip-permissions --model claude-fable-5 "You are a headless host process for a long-running background workflow. Your ONLY job: (1) Invoke the Workflow tool with exactly {\"scriptPath\": \"$SCRIPT\"} — no other parameters. (2) Stay alive waiting for the workflow completion notification — do not exit, do not do other work, do not edit files in /Users/hex/projects/payload-systems (the workflow agents own them). (3) When the workflow completes: write its return value and a phase-by-phase summary to $RESULT, then run verify the packager agent committed (git -C /Users/hex/projects/payload-systems log --oneline -1); if it did not, run git -C /Users/hex/projects/payload-systems add -A and commit with message 'rev-1 close-out r13 outputs (host fallback)'. Do not push. If the Workflow tool errors on invocation, report the error as your final message and exit." > "$LAST_LOG" 2>&1 &
    echo "$(date) launched as pid $!" >> "$LOG"
    sleep 90  # give it time to boot before re-checking
  fi
  sleep 60
done
