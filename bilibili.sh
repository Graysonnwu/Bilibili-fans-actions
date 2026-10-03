#!/bin/sh
set -eu
cd "$(dirname "$0")"
failed=0
while IFS= read -r uid || [ -n "$uid" ]; do
    [ -n "$uid" ] || continue
    if ! python3 bilibili.py "$uid" --record; then
        failed=1
    fi
done < uid.txt
exit "$failed"
