#!/bin/zsh
# Watchdog for the dispenser rev-1 CLOSE-OUT workflow host (attempt #4, 2026-08-08).
# Prior failures: 2x in-session (session restarts), 1x detached host killed by
# claude print-mode's 600s background ceiling (CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS
# was not set). This launcher sets the ceiling to 0 and relaunches a dead host.
# Done condition: RUN-RESULT.md contains the '## Close-out run (2026-08-08)' section.
SCRIPT="/Users/hex/projects/payload-systems/payloads/capsule-dispenser/_run/rev1/closeout-workflow.js"
RESULT="/Users/hex/projects/payload-systems/payloads/capsule-dispenser/_run/rev1/RUN-RESULT.md"
LOG="/tmp/closeout-watchdog.log"
MARKER="headless host process for the dispenser close-out workflow"
DONE_MARKER="## Close-out run (2026-08-08)"
RESTARTS=0
MAX_RESTARTS=3

launch_host() {
  CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 nohup caffeinate -i claude -p --dangerously-skip-permissions --model claude-fable-5 "You are a headless host process for the dispenser close-out workflow. Your ONLY job: (1) Invoke the Workflow tool with exactly {\"scriptPath\": \"$SCRIPT\"}. (2) Stay alive waiting for the workflow completion notification — do not exit, do not do other work, do not edit files in /Users/hex/projects/payload-systems (the workflow agents own them). (3) When the workflow completes: check that $RESULT contains a '$DONE_MARKER' section (the packager agent writes it; append a minimal one from the workflow return value ONLY if the packager failed to), then run git -C /Users/hex/projects/payload-systems status --short and commit any uncommitted changes with message 'rev-1 close-out run outputs (detached host)' author 'thomasg <thomas@arrowair.com>'. Do NOT push. If the Workflow tool errors on invocation, report the error as your final message and exit." > "/tmp/closeout-host-r$RESTARTS.log" 2>&1 &
  echo "$(date) launched host attempt r$RESTARTS as pid $!" >> "$LOG"
}

echo "$(date) close-out watchdog up (pid $$)" >> "$LOG"
launch_host
sleep 90
while true; do
  if grep -q "$DONE_MARKER" "$RESULT" 2>/dev/null; then
    echo "$(date) close-out section present in RUN-RESULT.md — run complete, watchdog exiting" >> "$LOG"
    exit 0
  fi
  if ! pgrep -f "$MARKER" >/dev/null 2>&1; then
    if [ "$RESTARTS" -ge "$MAX_RESTARTS" ]; then
      echo "$(date) host dead, restart budget exhausted ($MAX_RESTARTS) — GIVING UP. Needs human/Hex attention." >> "$LOG"
      exit 1
    fi
    RESTARTS=$((RESTARTS+1))
    echo "$(date) host dead — restart #$RESTARTS (fresh launch; workflow re-runs from script, work files on disk persist)" >> "$LOG"
    launch_host
    sleep 90
  fi
  sleep 60
done
