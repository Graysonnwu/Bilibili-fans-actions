#!/usr/bin/env python3
"""Fetch one validated observation; optionally update the local history atomically."""
import argparse
import csv
import datetime
from pathlib import Path
import sys
import tempfile

import requests

BEIJING = datetime.timezone(datetime.timedelta(hours=8))
DATA_DIR = Path(__file__).resolve().parent / 'data'
HEADERS = {'Accept': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Mobile Safari/537.36',
           'Referer': 'https://www.bilibili.com/'}


def validate_uid(value):
    if not value.isascii() or not value.isdigit() or int(value) <= 0:
        raise ValueError('UID must be a positive integer')
    return value


def fetch_followers(uid, session=requests):
    validate_uid(uid)
    response = session.get('https://api.bilibili.com/x/relation/stat',
                           params={'vmid': uid}, headers=HEADERS, timeout=(5, 20))
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict) or payload.get('code') != 0:
        code = payload.get('code') if isinstance(payload, dict) else 'invalid response'
        raise ValueError(f'Bilibili API rejected the request (code {code})')
    data = payload.get('data')
    follower = data.get('follower') if isinstance(data, dict) else None
    if isinstance(follower, bool) or not isinstance(follower, int) or follower < 0:
        raise ValueError('Bilibili API returned an invalid follower count')
    return follower


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', newline='',
                                         dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        temporary.replace(path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def record_observation(uid, day, follower, data_dir=DATA_DIR):
    validate_uid(uid)
    datetime.date.fromisoformat(day)
    if isinstance(follower, bool) or not isinstance(follower, int) or follower < 0:
        raise ValueError('Invalid follower count')
    history = data_dir / f'{uid}.txt'
    records = {}
    if history.exists():
        with history.open(encoding='utf-8', newline='') as handle:
            for row in csv.reader(handle):
                if not row:
                    continue
                if len(row) != 2:
                    raise ValueError(f'Malformed history in {history.name}')
                datetime.date.fromisoformat(row[0])
                if not row[1].isascii() or not row[1].isdigit():
                    raise ValueError(f'Invalid follower count in {history.name}')
                records[row[0]] = int(row[1])
    # A repeated manual run is the latest same-day observation, not another day.
    records[day] = follower
    lines = [f'{date},{count}\n' for date, count in sorted(records.items())]
    atomic_write(history, ''.join(lines))
    atomic_write(data_dir / f'{uid}.csv', 'date,follower\n' + ''.join(reversed(lines)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('uid')
    parser.add_argument('--record', action='store_true', help='update data/<UID>.txt and .csv')
    args = parser.parse_args()
    try:
        follower = fetch_followers(args.uid)
        day = datetime.datetime.now(BEIJING).date().isoformat()
        if args.record:
            record_observation(args.uid, day, follower)
        print(f'{day},{follower}')
    except (requests.RequestException, ValueError, OSError) as error:
        print(f'UID {args.uid}: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
