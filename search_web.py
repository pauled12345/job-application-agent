"""
Web search via Bing, driven by Playwright.

Why Playwright: DuckDuckGo, Ecosia, Mojeek, Brave, Startpage and Yandex all
serve bot challenges or 403s to plain HTTP requests and to headless Chrome.
Bing returns real results. No CAPTCHA is ever solved.

Usage:
    python search_web.py "query one" "query two"
    python search_web.py --json "query"   # dump search_results.json
"""
import base64
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlparse, parse_qs

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
OUT = BASE / "search_results.json"


def unwrap(url: str) -> str:
    """Bing wraps result links as /ck/a?...&u=a1<base64url of real url>."""
    if not url:
        return ""
    if "bing.com/ck/a" in url:
        qs = parse_qs(urlparse(url).query)
        u = (qs.get("u") or [""])[0]
        if u.startswith("a1"):
            u = u[2:]
        try:
            pad = "=" * (-len(u) % 4)
            return base64.urlsafe_b64decode(u + pad).decode("utf-8", "replace")
        except Exception:
            return url
    if url.startswith("//duckduckgo.com/l/"):
        u = parse_qs(urlparse("https:" + url).query).get("uddg", [""])[0]
        if u:
            return unquote(u)
    return url


def run(query, limit=14, engine="bing"):
    if engine == "bing":
        url = f"https://www.bing.com/search?q={quote(query)}&count=30"
        item_sel = "li.b_algo"
    else:
        url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
        item_sel = "div.result"

    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": 1366, "height": 900})
        pg.goto(url, timeout=45000, wait_until="domcontentloaded")
        pg.wait_for_timeout(2200)
        rows = pg.eval_on_selector_all(
            item_sel,
            """els => els.map(e => {
                const a = e.querySelector('h2 a, a.result__a');
                const s = e.querySelector('.b_caption p, .result__snippet');
                return {
                    title: a ? a.innerText.trim() : '',
                    url: a ? a.href : '',
                    snippet: s ? s.innerText.trim().slice(0,320) : ''
                };
            })"""
        )
        b.close()

    seen, out = set(), []
    for r in rows:
        real = unwrap(r["url"])
        r["url"] = real
        if not real.startswith("http"):
            continue
        if any(d in real for d in ("bing.com", "duckduckgo.com", "microsoft.com/translator")):
            continue
        key = real.split("?")[0].rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
        if len(out) >= limit:
            break
    return out


def main():
    args = sys.argv[1:]
    engine = "bing"
    if args and args[0] in ("--bing", "--ddg"):
        engine = args.pop(0).lstrip("-")
    as_json = "--json" in args
    if as_json:
        args = [a for a in args if a != "--json"]
    queries = args or ["kenya junior python developer remote"]

    everything = {}
    for q in queries:
        res = run(q, engine=engine)
        everything[q] = res
        print("=" * 74)
        print(f"QUERY ({engine}): {q}   [{len(res)} results]")
        print("=" * 74)
        if not res:
            print("  (none parsed)")
        for i, r in enumerate(res, 1):
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}")
            if r["snippet"]:
                print(f"   {r['snippet'][:210]}")
        print()

    OUT.write_text(json.dumps(everything, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()