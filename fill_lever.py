"""
Lever application form filler.

Fills a Lever posting's application form from profile.json + a resume file,
then screenshots it for review.

By default it STOPS BEFORE SUBMITTING. Lever includes an hCaptcha, and I do not
circumvent anti-bot controls. Paul completes the final submit (and any CAPTCHA)
in the visible browser window.

Usage:
    python fill_lever.py --url <posting-url> --resume <path> [--submit]
"""
import argparse
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
PROFILE = BASE / "profile.json"
SHOTS = BASE / "shots"


def load_profile():
    if not PROFILE.exists():
        sys.exit("ERROR: profile.json missing. Copy profile.template.json and fill it in.")
    return json.loads(PROFILE.read_text(encoding="utf-8"))


def fill(page, prof, resume_path):
    def put(selector, value, label):
        if value:
            el = page.query_selector(selector)
            if el:
                el.fill(value)
                print(f"  filled {label}")
            else:
                print(f"  SKIP {label} (field absent)")

    # Open the modal
    for sel in ["text=APPLY FOR THIS JOB", "text=Apply for this job",
                "a:has-text('APPLY')", "button:has-text('Apply')"]:
        try:
            page.click(sel, timeout=8000)
            break
        except Exception:
            continue
    page.wait_for_timeout(2500)

    # Resume upload
    fi = page.query_selector("input[type=file][name='resume']")
    if fi and resume_path and Path(resume_path).exists():
        fi.set_input_files(resume_path)
        print(f"  attached resume: {resume_path}")
        page.wait_for_timeout(1500)

    put("input[name='name']", prof.get("full_name"), "name")
    put("input[name='email']", prof.get("email"), "email")
    put("input[name='phone']", prof.get("phone"), "phone")
    put("input[name='location']", prof.get("location"), "location")
    put("input[name='org']", prof.get("current_company"), "current company")
    put("input[name='urls[LinkedIn]']", prof.get("linkedin_url"), "LinkedIn")
    put("input[name='urls[GitHub]']", prof.get("github_url"), "GitHub")
    put("input[name='urls[Portfolio]']", prof.get("portfolio_url"), "portfolio")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--resume", required=True)
    ap.add_argument("--submit", action="store_true",
                    help="Click SUBMIT. Off by default - review the screenshot first.")
    args = ap.parse_args()

    if not Path(args.resume).exists():
        sys.exit(f"ERROR: resume not found at {args.resume}")

    prof = load_profile()
    SHOTS.mkdir(exist_ok=True)
    tag = args.url.rstrip("/").split("-")[-1][:8] or "posting"

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()
        page.goto(args.url, timeout=45000, wait_until="networkidle")

        print("Filling form...")
        fill(page, prof, args.resume)

        SHOTS.mkdir(exist_ok=True)
        shot = SHOTS / f"lever-{tag}.png"
        page.screenshot(path=str(shot), full_page=True)
        print(f"\nScreenshot: {shot}")

        # Report anything still empty that is marked required
        missing = page.eval_on_selector_all(
            "input[required], textarea[required]",
            """els => els.filter(e => !e.value).map(e => e.name || e.id || e.type)"""
        )
        if missing:
            print(f"\nWARNING - required fields still empty: {missing}")

        if args.submit:
            captcha = page.query_selector(".h-captcha, iframe[src*='hcaptcha'], div[id*='captcha']")
            if captcha:
                print("\nCAPTCHA DETECTED - not submitting.")
                print("Complete it yourself in this browser window, then click SUBMIT APPLICATION.")
                input("Press Enter once you have finished submitting... ")
            else:
                page.click("button:has-text('SUBMIT APPLICATION')")
                page.wait_for_timeout(4000)
                shot2 = SHOTS / f"lever-{tag}-submitted.png"
                page.screenshot(path=str(shot2), full_page=True)
                print(f"Submitted. Screenshot: {shot2}")
                print("VERIFY on the Lever dashboard that it actually went through.")
        else:
            print("\nStopped before submit (default). Re-run with --submit when ready.")

        browser.close()


if __name__ == "__main__":
    main()