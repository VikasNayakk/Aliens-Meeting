#!/usr/bin/env python3
"""
Create dated meeting-topic folders with required files.
Usage:
  python create_meeting_topic.py --date 23-04-2026
  python create_meeting_topic.py            # uses today's date
Options:
  --copy FILE1 FILE2 ...   Copy existing files into the new dated folder (keeps originals).
"""
import os
import argparse
from datetime import datetime
import shutil

DEFAULT_FILES = ["transcript.txt", "summary.txt", "topics.txt", "full-report.txt"]


def create_meeting_folder(base_dir, date_str):
    target = os.path.join(base_dir, date_str)
    os.makedirs(target, exist_ok=True)
    created = []
    for fn in DEFAULT_FILES:
        path = os.path.join(target, fn)
        if not os.path.exists(path):
            open(path, "w", encoding="utf-8").close()
            created.append(path)
    return target, created


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Meeting-Topic dated folder and template files.")
    parser.add_argument("--date", help="Date in DD-MM-YYYY format. Defaults to today.")
    parser.add_argument("--copy", nargs="*", help="Files to copy into the new folder (keeps originals).")
    parser.add_argument("--base", help="Base Meeting-Topic directory (defaults to script parent).")
    args = parser.parse_args()

    if args.date:
        try:
            datetime.strptime(args.date, "%d-%m-%Y")
            date_str = args.date
        except Exception:
            raise SystemExit("Error: --date must be in DD-MM-YYYY format")
    else:
        date_str = datetime.now().strftime("%d-%m-%Y")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    base = args.base if args.base else script_dir

    target_dir, created_files = create_meeting_folder(base, date_str)
    print(f"Created folder: {target_dir}")
    if created_files:
        print("Created files:")
        for p in created_files:
            print(" - ", p)
    else:
        print("All template files already existed.")

    if args.copy:
        for src in args.copy:
            if os.path.exists(src):
                try:
                    shutil.copy2(src, target_dir)
                    print(f"Copied {src} -> {target_dir}")
                except Exception as e:
                    print(f"Failed to copy {src}: {e}")
            else:
                print(f"Warning: source not found: {src}")

    print("Done.")
