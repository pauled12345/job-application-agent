"""
Gmail SMTP sender for job applications.

Credentials are read from .gmail-creds (gitignored, never pasted into chat).
Usage:
    python send_email.py --to addr --subject "..." --body-file letter.txt
    python send_email.py --to addr --subject "..." --body "short text"

Every send is appended to sent_log.jsonl so nothing slips through untracked.
Dry-run by default: add --send to actually transmit.
"""
import argparse
import json
import os
import ssl
import sys
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

import smtplib

BASE = Path(__file__).resolve().parent
CREDS = BASE / ".gmail-creds"
LOG = BASE / "sent_log.jsonl"


def _clean(val: str) -> str:
    """Normalise a credential value.

    Google displays app passwords as 'abcd efgh ijkl mnop' and it is easy to
    paste with the grouping spaces intact. Strip quotes and ALL whitespace so
    either paste style works.
    """
    v = val.strip()
    # strip matching surrounding quotes
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        v = v[1:-1]
    return "".join(v.split())


def load_creds():
    if not CREDS.exists():
        sys.exit(
            "ERROR: .gmail-creds not found.\n"
            "Create it with two lines:\n"
            "  GMAIL_USER=paulnjugunanganga58@gmail.com\n"
            "  GMAIL_APP_PASSWORD=your-16-char-app-password\n"
        )
    vals = {}
    for line in CREDS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        vals[k.strip()] = _clean(v)
    user = vals.get("GMAIL_USER")
    pw = vals.get("GMAIL_APP_PASSWORD")
    if not user or not pw:
        sys.exit("ERROR: .gmail-creds must define GMAIL_USER and GMAIL_APP_PASSWORD.")
    return user, pw


def log_entry(entry):
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True, help="Recipient address")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file")
    ap.add_argument("--body")
    ap.add_argument("--reply-to")
    ap.add_argument("--send", action="store_true",
                    help="Actually transmit. Without this, prints only.")
    args = ap.parse_args()

    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")
    elif args.body:
        body = args.body
    else:
        sys.exit("ERROR: need --body-file or --body")

    # Guard against obviously fabricated content slipping into a send.
    banned = ["lorem ipsum", "your company here", "[insert", "TBD", "XX years",
              "example.com", "<your"]
    low = body.lower()
    hits = [b for b in banned if b.lower() in low]
    if hits:
        sys.exit(f"ERROR: body contains placeholder text {hits}. Fix before sending.")

    user, pw = load_creds()

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = args.to
    msg["Subject"] = args.subject
    if args.reply_to:
        msg["Reply-To"] = args.reply_to
    msg.set_content(body)

    stamp = datetime.now(timezone.utc).isoformat()
    entry = {"ts": stamp, "to": args.to, "subject": args.subject,
             "words": len(body.split()), "sent": bool(args.send)}

    if not args.send:
        entry["sent"] = False
        entry["status"] = "dry-run"
        log_entry(entry)
        print("=== DRY RUN (nothing transmitted) ===")
        print(f"From   : {user}")
        print(f"To     : {args.to}")
        print(f"Subject: {args.subject}")
        print(f"Words  : {len(body.split())}")
        print("-" * 60)
        print(body)
        print("-" * 60)
        print("Re-run with --send to transmit.")
        return

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=30) as s:
            s.login(user, pw)
            s.send_message(msg)
    except Exception as exc:
        entry["status"] = f"FAILED: {type(exc).__name__}: {exc}"
        log_entry(entry)
        sys.exit(f"SEND FAILED: {type(exc).__name__}: {exc}")

    entry["sent"] = True
    entry["status"] = "ok"
    log_entry(entry)
    print(f"SENT to {args.to} at {stamp}")


if __name__ == "__main__":
    main()