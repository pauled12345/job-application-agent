"""Render the HTML resumes to A4 PDFs via Playwright + installed Chrome."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
SRC = BASE / "resumes"

JOBS = [
    ("resume_sw.html", "resume_sw.pdf"),
    ("resume_ai.html", "resume_ai.pdf"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page()
    for src, out in JOBS:
        sp = SRC / src
        if not sp.exists():
            print(f"SKIP (missing): {sp}")
            continue
        page.goto(sp.as_uri(), wait_until="networkidle")
        pdf = SRC / out
        page.pdf(path=str(pdf), format="A4",
                 margin={"top": "15mm", "bottom": "15mm",
                         "left": "14mm", "right": "14mm"},
                 print_background=True)
        size = pdf.stat().st_size
        print(f"WROTE {pdf.name}  ({size/1024:.1f} KB)")
    browser.close()
print("render complete")