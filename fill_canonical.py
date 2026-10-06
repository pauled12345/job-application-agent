"""
Pre-fill a Canonical application form with facts Paul actually supplied.

Fills only verifiable fields, attaches the tailored resume, and inserts the
drafted essay answers from ANSWERS.md. Leaves untouched:

  - personal / academic facts only Paul knows (maths grade, language grade,
    race, ethnicity, gender)
  - the reCAPTCHA

Canonical uses reCAPTCHA. It is not bypassed. Use --submit to attempt the
final click; if a CAPTCHA is present the script refuses and tells you to finish
it yourself.
"""
import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
SHOTS = BASE / "shots"
SHOTS.mkdir(exist_ok=True)

PROFILE = json.loads((BASE / "profile.json").read_text(encoding="utf-8"))

ROLE_URLS = {
    "grad": "https://canonical.com/careers/8249005",
    "junior": "https://canonical.com/careers/6707669",
}

Q_LINUX = (
    "Linux has been my primary development environment since starting university. I use it daily for "
    "Python and Flutter work, running FastAPI services, working with PostgreSQL, and using Git from the "
    "command line. I have also worked in Kali Linux for security coursework and self-directed security "
    "research. On open source, my main exposure has been as a user and reader rather than a contributor. "
    "I have five public repositories on GitHub (github.com/pauled12345), including a Python web scraper I "
    "built to track competitor pricing across Jumia. Writing that tool taught me a lot about reading "
    "unpredictable HTML, handling failures gracefully, and structuring data other people can actually use. "
    "I have not yet had a pull request merged upstream, and I would like to change that."
)

Q_PROJECT = (
    "AutoIntel, an AI-assisted vehicle diagnostics and maintenance app. It connects to a vehicle over a "
    "Bluetooth ELM327 OBD-II scanner, reads diagnostic trouble codes and live sensor data, and uses an LLM "
    "to turn those raw codes into plain-language explanations and maintenance guidance that a non-expert "
    "owner can act on. The mobile client is Flutter; the backend is FastAPI with a PostgreSQL database "
    "storing diagnostic results, maintenance history, fuel records and repair costs. I chose this because "
    "I wanted something with a real user rather than another tutorial project. The hard part was not the "
    "API calls, it was deciding how much the model could be trusted: wrong maintenance advice has safety "
    "consequences, so I spent most of my effort on prompt behaviour, output accuracy, and making the app "
    "degrade gracefully when the model is unsure."
)


def set_essay(page, selector, text):
    el = page.query_selector(selector)
    if not el:
        print(f"  MISSING {selector}")
        return False
    el.fill(text)
    print(f"  filled {selector} ({len(text)} chars)")
    return True


def select_by_label(page, selector, label_text):
    el = page.query_selector(selector)
    if not el:
        print(f"  MISSING {selector}")
        return False
    try:
        el.select_option(label=label_text)
        print(f"  selected '{label_text}' in {selector}")
        return True
    except Exception:
        opts = el.eval_on_selector_all(
            "option", "els=>els.map(e=>({v:e.value,t:e.textContent.trim().slice(0,50)}))")
        print(f"  could not select '{label_text}' in {selector}")
        print(f"    available: {json.dumps(opts[:12])}")
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", choices=list(ROLE_URLS), default="grad")
    ap.add_argument("--resume", default="resumes/resume_sw.pdf")
    ap.add_argument("--headful", action="store_true", help="show the browser window")
    ap.add_argument("--submit", action="store_true", help="attempt final submit")
    args = ap.parse_args()

    url = ROLE_URLS[args.role]
    resume = BASE / args.resume
    if not resume.exists():
        raise SystemExit(f"ERROR: resume missing at {resume}")

    first, _, last = PROFILE["full_name"].partition(" ")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=not args.headful)
        page = browser.new_page(viewport={"width": 1400, "height": 1200})
        # Canonical keeps analytics sockets open, so networkidle never settles.
        # Use minimal wait and then just wait for the first form field.
        page.goto(url, timeout=90000, wait_until="domcontentloaded")
        # Accept cookie banner if present
        for sel in ['button:has-text("Accept")', 'button:has-text("Allow")',
                    '#onetrust-accept-btn-handler', '.cookie-banner button']:
            try:
                page.click(sel, timeout=3000)
                page.wait_for_timeout(1000)
                break
            except Exception:
                pass
        page.wait_for_selector("input[name='first_name']", timeout=45000)
        page.wait_for_timeout(2000)

        print(f"Filling {url}")

        # name / contact
        for sel, val in [("input[name='first_name']", first),
                         ("input[name='last_name']", last),
                         ("input[name='email']", PROFILE["email"])]:
            el = page.query_selector(sel)
            if el:
                el.fill(val)
                print(f"  filled {sel}")

        # phone: pick Kenya in the intl widget then type the number
        try:
            page.click("input[name='phone']")
            page.wait_for_timeout(800)
            page.click(".iti__selected-country")
            page.wait_for_timeout(500)
            page.click("li[data-country-code='ke']")
            page.wait_for_timeout(400)
        except Exception as exc:
            print(f"  (phone country picker: {type(exc).__name__})")
        phone = PROFILE["phone"].lstrip("+")
        el = page.query_selector("input[name='phone']:not([type=hidden])")
        if el:
            el.fill(phone)
            print(f"  filled phone -> +254{phone}")

        # resume
        fi = page.query_selector("input[type=file][name='resume']")
        if fi:
            fi.set_input_files(str(resume))
            print(f"  attached {args.resume}")
            page.wait_for_timeout(2000)

        # links
        for sel, val in [("input[name='question_69583808']", PROFILE["github_url"]),
                         ("input[name='question_69583809']", PROFILE["linkedin_url"])]:
            el = page.query_selector(sel)
            if el and val:
                el.fill(val)
                print(f"  filled {sel}")

        # country of work
        select_by_label(page, "select[name='question_69583810']", "Kenya")

        # drafted essays
        set_essay(page, "textarea[name='question_69583799']", Q_LINUX)
        set_essay(page, "textarea[name='question_69583700']", "")
        set_essay(page, "textarea[name='question_69583800']", Q_PROJECT)

        # degree result - expected, honest
        set_essay(page, "textarea[name='question_69583807']",
                  "I expect to complete my BSc Computer Science at Dedan Kimathi University of Technology "
                  "in April 2027.")

        page.wait_for_timeout(1200)
        shot = SHOTS / f"canonical-{args.role}-prefilled.png"
        page.screenshot(path=str(shot), full_page=True)
        print(f"\nScreenshot -> {shot}")

        remaining = page.eval_on_selector_all(
            "input[required], textarea[required], select[required]",
            """els => els.filter(e => !e.value && e.type !== 'hidden').map(e => {
                 const l = e.labels && e.labels[0];
                 return (l ? l.innerText.trim().slice(0,70) : (e.name||e.type));
               })"""
        )
        print(f"\n{len(remaining)} required fields still EMPTY:")
        for r in remaining:
            print(f"  - {r}")

        cap = page.query_selector(".g-recaptcha, iframe[src*='recaptcha'], div[id*='captcha']")
        print(f"\nreCAPTCHA present: {'YES' if cap else 'not detected'}")

        if args.submit:
            if cap:
                print("\nNOT submitting: reCAPTCHA present and I will not bypass it.")
                print("Finish the CAPTCHA in the browser, then click 'Apply for this role'.")
            else:
                page.click("input[name='submit_button']")
                page.wait_for_timeout(5000)
                print("Clicked submit. Check for a confirmation message on the page.")

        if not args.headful and not args.submit:
            browser.close()
        else:
            print("\nBrowser left open.")
            input("Press Enter in this console to close...") if args.submit else browser.close()


if __name__ == "__main__":
    main()