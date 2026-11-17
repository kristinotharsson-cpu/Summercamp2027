#!/bin/zsh
idx="$1"; url="$2"
curl -sS -L --max-time 30 --compressed \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" \
  -o "dl/${idx}.html" -w "${idx} HTTP %{http_code} %{size_download}\n" "$url" 2>&1 || echo "${idx} FAILED"
