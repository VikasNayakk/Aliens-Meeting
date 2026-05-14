Meeting-Topic helper

- Purpose: create a dated folder (DD-MM-YYYY) with template files:
  - transcript.txt
  - summary.txt
  - topics.txt
  - full-report.txt

Usage:
  python create_meeting_topic.py --date DD-MM-YYYY
  python create_meeting_topic.py            # uses today's date

Options:
  --copy FILE1 FILE2 ...  Copy listed files into the new folder (originals kept).
  --base PATH             Use a different Meeting-Topic base directory.

Notes:
- This script will not delete any existing data; it only creates folders/files or copies files.
- Want me to run it now to create today's folder? Reply 'yes' to run or 'no' to skip.
