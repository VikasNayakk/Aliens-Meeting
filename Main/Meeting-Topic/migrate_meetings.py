#!/usr/bin/env python3
"""
Migrate meetings from Data/Meetings/YYYY-MM-DD -> Main/Meeting-Topic/DD-MM-YYYY
Creates: transcript.txt, summary.txt, topics.txt, full-report.txt
Non-destructive: copies data and leaves originals intact unless --remove-original is passed.
"""
import os
import json
import shutil
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_MEETINGS = os.path.join(ROOT, 'Data', 'Meetings')
TARGET_BASE = os.path.abspath(os.path.dirname(__file__))

DEFAULT_FILES = ['transcript.txt', 'summary.txt', 'topics.txt', 'full-report.txt']


def ymd_to_ddmmyyyy(name):
    # name expected as YYYY-MM-DD
    try:
        dt = datetime.strptime(name, '%Y-%m-%d')
        return dt.strftime('%d-%m-%Y')
    except Exception:
        return None


def safe_read(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_if_missing(path, content=''):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def generate_files(src_dir, target_dir):
    # transcript <- events.log if exists
    events_path = os.path.join(src_dir, 'events.log')
    attendance_path = os.path.join(src_dir, 'attendance.json')

    transcript = safe_read(events_path) or ''
    attendance_raw = safe_read(attendance_path)
    attendance = None
    if attendance_raw:
        try:
            attendance = json.loads(attendance_raw)
        except Exception:
            attendance = None

    # summary: date + present count if available
    summary_lines = []
    date_label = os.path.basename(src_dir)
    summary_lines.append(f'Date: {date_label}')
    if attendance:
        count = 0
        if isinstance(attendance, dict):
            # try common fields
            if 'present' in attendance and isinstance(attendance['present'], list):
                count = len(attendance['present'])
            elif 'attendees' in attendance and isinstance(attendance['attendees'], list):
                count = len(attendance['attendees'])
            elif 'attendance' in attendance and isinstance(attendance['attendance'], list):
                count = len(attendance['attendance'])
        summary_lines.append(f'Present count (approx): {count}')

    # topics: try to extract from a topics.txt in src
    topics_src = os.path.join(src_dir, 'topics.txt')
    topics = safe_read(topics_src) or ''

    # full-report: combine attendance json + events.log
    full_report_parts = []
    if attendance_raw:
        full_report_parts.append('--- Attendance JSON ---\n')
        full_report_parts.append(attendance_raw)
        full_report_parts.append('\n')
    if transcript:
        full_report_parts.append('--- Events Log / Transcript ---\n')
        full_report_parts.append(transcript)

    # Write files
    write_if_missing(os.path.join(target_dir, 'transcript.txt'), transcript)
    write_if_missing(os.path.join(target_dir, 'summary.txt'), '\n'.join(summary_lines))
    write_if_missing(os.path.join(target_dir, 'topics.txt'), topics)
    write_if_missing(os.path.join(target_dir, 'full-report.txt'), '\n'.join(full_report_parts))

    # Copy any other files found into target dir (non-destructive)
    for fname in os.listdir(src_dir):
        if fname in ('events.log', 'attendance.json', 'topics.txt'):
            continue
        srcp = os.path.join(src_dir, fname)
        if os.path.isfile(srcp):
            # copy files that are not the ones already processed
            try:
                shutil.copy2(srcp, target_dir)
            except Exception:
                pass


if __name__ == '__main__':
    print('Starting migration from', DATA_MEETINGS)
    if not os.path.isdir(DATA_MEETINGS):
        print('No Data/Meetings folder found. Nothing to do.')
        raise SystemExit(0)

    entries = sorted(os.listdir(DATA_MEETINGS))
    processed = 0
    for name in entries:
        src = os.path.join(DATA_MEETINGS, name)
        if not os.path.isdir(src):
            continue
        dd = ymd_to_ddmmyyyy(name)
        if not dd:
            print('Skipping non-date folder:', name)
            continue
        target = os.path.join(TARGET_BASE, dd)
        ensure_dir(target)
        generate_files(src, target)
        processed += 1
        print(f'Processed {name} -> {target}')

    print('Migration complete. Processed', processed, 'meeting folders.')
    print('Note: originals left intact. To remove originals, run with --remove-original in a safe manner (not implemented).')
