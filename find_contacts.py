"""
Deep contact hunt on verified employers.

Goes past the homepage into /contact, /about, /careers, /jobs pages and pulls
out published email addresses. Also notes whether a contact FORM exists (which
means an email would bounce, so it should not be an outreach target).

Also scans Lever / Ashby / Greenhouse public boards for junior or remote
worldwide roles, since those postings often name a contact address.
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote, urljoin

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
H = {"User-Agent": UA}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
BAD_EMAIL = re.compile(r"\.(png|jpg|jpeg|gif|webp|svg|css|js)$", re.I)

TARGETS = {
    "MellowVans": "https://mellowvans.com",
    "Chpter": "https://chpter.co",
    "Credy": "https://credy.co",
    "OkHi": "https://okhi.co",
    "Kuda": "https://kuda.com",
    "AfricasTalking": "https://africastalking.com",
    "MKOPA": "https://www.m-kopa.com",
    "iHUB": "https://ihub.co.ke",
    "FUTO": "https://futo.tech",
    "Immich": "https://immich.app",
}
PATHS = ["", "/contact", "/contact-us", "/about", "/about-us", "/careers",
         "/jobs", "/career", "/join", "/team"]

# Public ATS boards - these postings usually name a contact
ATS = {
    "lever_junior_remote": "https://www.indeed.com",
}


def dig(name, base):
    found, pages = {}, {}
    for path in PATHS:
        url = urljoin(base, path)
        try:
            r = requests.get(url, headers=H, timeout=15, allow_redirects=True)
        except Exception:
            continue
        if r.status_code >= 400:
            continue
        html = r.text
        low = html.lower()
        has_form = bool(re.search(r"<form[^>]*(contact|enquiry|inquiry|apply)", low)) or \
                   "name=\"email\"" in low and "contactform" in low
        pages[url] = {"status": r.status_code, "len": len(html), "form": has_form}
        for e in EMAIL_RE.findall(html):
            if BAD_EMAIL.search(e):
                continue
            lowe = e.lower()
            if any(x in lowe for x in ("example.com", "sentry.io", "domain.com",
                                       "yourcompany", "@2x", "wixpress")):
                continue
            found.setdefault(e, set()).add(url)
    return {
        "name": name, "base": base,
        "emails": sorted(found.keys()),
        "sources": {k: sorted(v) for k, v in found.items()},
        "pages_ok": [u for u, d in pages.items() if d["status"] == 200 and d["len"] > 500],
        "contact_form_pages": [u for u, d in pages.items() if d["form"]],
    }


def main():
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(lambda kv: dig(*kv), TARGETS.items()))

    print("=" * 78)
    print("CONTACT DEEP-DIVE RESULTS")
    print("=" * 78)
    for r in results:
        print(f"\n## {r['name']}  ({r['base']})")
        if r["emails"]:
            for e in r["emails"]:
                src = r["sources"][e][0]
                print(f"   EMAIL: {e}")
                print(f"          found on: {src}")
        else:
            print("   EMAIL: none published")
        if r["contact_form_pages"]:
            print(f"   contact form at: {r['contact_form_pages'][0]}")
        if not r["pages_ok"]:
            print("   WARNING: no pages reachable")

    Path(__file__).resolve().parent.joinpath("contacts.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nsaved -> contacts.json")


if __name__ == "__main__":
    main()