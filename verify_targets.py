"""
Verify candidate employers by fetching their sites directly.

For each seed domain: check it resolves, grab the title, look for a careers /
jobs / contact page, and extract any published email addresses.

This is the safety step - a dead domain, a parked page, or a site with no way
to contact a human gets rejected before Paul ever emails anyone.
"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
H = {"User-Agent": UA}

SEEDS = [
    # African / Kenyan tech companies and agencies
    "https://africastalking.com",
    "https://www.m-kopa.com",
    "https://kuda.com",
    "https://www.skygride.co",
    "https://basigo.co",
    "https://www.cellulant.io",
    "https://sendyit.com",
    "https://credy.co",
    "https://okhi.co",
    "https://zembo.io",
    "https://mellowvans.com",
    "https://chpter.co",
    "https://nailab.co",
    "https://ihub.co.ke",
    "https://refactory.co.ke",
    "https://moringaschool.com",
    "https://emobilis.com",
    "https://devken.co",
    "https://bitpawa.com",
    "https://senbo.co",
    "https://looptelecom.co.ke",
    "https://saharahackerspace.org",
    "https://www.chandler.africa",
    # Remote-first / open source that hire juniors globally
    "https://canonical.com/careers",
    "https://wikimediafoundation.org/about/careers",
    "https://immich.app",
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")


def check(seed):
    out = {"seed": seed, "url": seed, "ok": False}
    try:
        r = requests.get(seed, headers=H, timeout=20, allow_redirects=True)
        out["status"] = r.status_code
        out["final_url"] = r.url
        if r.status_code >= 400:
            return out
        html = r.text
        title = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
        out["title"] = (title.group(1).strip()[:90] if title else "")
        out["ok"] = True

        low = html.lower()
        out["has_careers"] = any(k in low for k in
                                 ("/careers", "/jobs", "join us", "vacanc", "opening"))
        emails = sorted(set(EMAIL_RE.findall(html)))
        out["emails"] = [e for e in emails[:6]
                         if not e.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))]

        # probe common careers paths
        for path in ("/careers", "/jobs", "/career", "/join-us", "/about/careers"):
            try:
                pr = requests.get(urljoin(seed, path), headers=H, timeout=12)
                if pr.status_code == 200 and len(pr.text) > 400:
                    out[f"probe_{path.strip('/').replace('/', '_')}"] = pr.status_code
            except Exception:
                pass
    except requests.exceptions.RequestException as exc:
        out["error"] = f"{type(exc).__name__}"
    return out


def main():
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(check, SEEDS))

    results.sort(key=lambda r: (not r["ok"], r["seed"]))
    print(f"{'OK':<3} {'STATUS':<7} {'CAREERS':<9} SEED")
    print("-" * 92)
    for r in results:
        ok = "Y" if r["ok"] else "N"
        car = "Y" if r.get("has_careers") else "-"
        st = str(r.get("status", r.get("error", "?")))
        print(f"{ok:<3} {st:<7} {car:<9} {r['seed']}")
        if r.get("title"):
            print(f"{'':22}{r['title']}")
        if r.get("emails"):
            print(f"{'':22}emails: {', '.join(r['emails'][:4])}")

    Path = __import__("pathlib").Path
    Path(__file__).resolve().parent.joinpath("verify_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nsaved -> verify_results.json")


if __name__ == "__main__":
    main()