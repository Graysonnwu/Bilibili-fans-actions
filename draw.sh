#!/bin/sh
set -eu
cd "$(dirname "$0")"
while IFS= read -r uid || [ -n "$uid" ]; do
    [ -n "$uid" ] || continue
    python3 draw.py "$uid"
done < uid.txt
