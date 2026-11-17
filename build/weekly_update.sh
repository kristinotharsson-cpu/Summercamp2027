#!/bin/zsh
# Weekly: re-check every camp whose 2027 dates or registration date are still unknown.
#
# If the `claude` CLI is logged in, it also reviews the findings and applies clear-cut
# updates. If it is not, the sweep still runs and you get the findings to review by hand.
# Log in once with `claude login` in Terminal.app and this upgrades itself.
set -u
DIR="/Users/cseries/projects/summer-camps-2027"
LOG="$DIR/build/weekly-run.log"
PY="/opt/homebrew/bin/python3"
CLAUDE="/opt/homebrew/bin/claude"
cd "$DIR" || exit 1

{
  echo ""
  echo "════════ $(date '+%Y-%m-%d %H:%M') ════════"
  "$PY" -I build/weekly_check.py
} >> "$LOG" 2>&1

SIGNALS=$("$PY" -c "import json;print(json.load(open('build/weekly-findings.json'))['with_signals'])" 2>/dev/null || echo 0)

if [ "$SIGNALS" -eq 0 ]; then
  echo "no camp showed a 2027 or registration signal" >> "$LOG"
  /usr/bin/osascript -e 'display notification "No camp posted new 2027 dates this week" with title "JQES summer camps"' 2>/dev/null
  exit 0
fi

OUT=$("$CLAUDE" -p "$(cat build/weekly_prompt.md)" \
        --allowedTools "Bash,Read,Edit,Write,Glob,Grep" \
        --permission-mode acceptEdits \
        --permission-prompts none 2>&1)
echo "$OUT" >> "$LOG"

if echo "$OUT" | grep -qi "Failed to authenticate\|OAuth session expired"; then
  MSG="$SIGNALS camps to review by hand - the claude CLI is not logged in"
  echo "[claude CLI not authenticated - findings left for manual review]" >> "$LOG"
else
  MSG="$SIGNALS camps had new signals - check CHANGELOG.md, then re-upload the page"
fi
/usr/bin/osascript -e "display notification \"$MSG\" with title \"JQES summer camps\"" 2>/dev/null
