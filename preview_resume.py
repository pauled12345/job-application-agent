"""Screenshot resumes as PNG for visual QA."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
SRC = BASE / "resumes"
OUT = BASE / "shots"
OUT.mkdir(exist_ok=True)

# A4 at 96dpi ~= 794 x 1123 px
with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 794, "height": 1123})
    for name in ["resume_sw.html", "resume_ai.html"]:
        sp = SRC / name
        if not sp.exists():
            continue
        page.goto(sp.as_uri(), wait_until="networkidle")
        target = OUT / (name.replace(".html", ".png"))
        page.screenshot(path=str(target), full_page=True)
        h = page.evaluate("document.body.scrollHeight")
        pages = round(h / 1123, 2)
        print(f"{target.name}  height={h}px  approx_pages={pages}")
    browser.close()