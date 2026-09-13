#!/bin/zsh
# Watchdog for the capsule dispenser rev-1 workflow host.
# If the headless claude host dies, relaunch it with resumeFromRunId so
# completed agents come back from cache. Exits when RUN-RESULT.md appears.
RUNID="wf_e00108ea-c63"
SCRIPT="/Users/hex/projects/payload-systems/payloads/capsule-dispenser/_run/rev1/run-workflow.js"
RESULT="/Users/hex/projects/payload-systems/payloads/capsule-dispenser/_run/rev1/RUN-RESULT.md"
LOG="/tmp/brush-rev1-watchdog.log"
MARKER="headless host process for a long-running background workflow"
RESTARTS=0
MAX_RESTARTS=5

echo "$(date) watchdog up (pid $$), watching for '$MARKER'" >> "$LOG"
while true; do
  if [ -f "$RESULT" ]; then
    echo "$(date) RUN-RESULT.md present — run complete, watchdog exiting" >> "$LOG"
    exit 0
  fi
  if ! pgrep -f "$MARKER" >/dev/null 2>&1; then
    if [ "$RESTARTS" -ge "$MAX_RESTARTS" ]; then
      echo "$(date) host dead and restart budget exhausted ($MAX_RESTARTS) — giving up" >> "$LOG"
      exit 1
    fi
    RESTARTS=$((RESTARTS+1))
    echo "$(date) host dead — restart #$RESTARTS (resume $RUNID)" >> "$LOG"
    CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 nohup caffeinate -i claude -p --dangerously-skip-permissions --model claude-fable-5 "You are a headless host process for a long-running background workflow. Your ONLY job: (1) Invoke the Workflow tool with exactly {\"scriptPath\": \"$SCRIPT\", \"resumeFromRunId\": \"$RUNID\"} — the resume returns cached results for already-completed agents. (2) Stay alive waiting for the workflow completion notification — do not exit, do not do other work, do not edit files in /Users/hex/projects/payload-systems (the workflow agents own them). (3) When the workflow completes: append its return value and a phase-by-phase summary as a '## Workflow host record' section to $RESULT (create it if the packager failed to), then run git -C /Users/hex/projects/payload-systems add -A and commit with message 'Rev-1 run outputs (detached host, fable)' author thomasg <thomas@arrowair.com> ONLY if there are uncommitted changes. If the Workflow tool errors on invocation, report the error as your final message and exit." > "/tmp/brush-rev1-host-r$RESTARTS.log" 2>&1 &
    echo "$(date) relaunched as pid $!" >> "$LOG"
    sleep 90  # give it time to boot before re-checking
  fi
  sleep 60
done
