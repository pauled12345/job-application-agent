# Application Tracker

**Paul** — Final-year CS student, Kenya
Email: paulnjugunanganga58@gmail.com
Skills: Python, FastAPI, REST APIs, PostgreSQL, Flutter, web scraping/automation, AI integrations, AI-assisted development, data annotation/AI evaluation, technical writing
Project: AutoIntel (AI vehicle diagnostics + maintenance app — Flutter + FastAPI + PostgreSQL)

**Positioning:** Final-year student wanting real experience and mentorship. Open to small budgets, stipends, trial tasks, junior roles. Reliable, learns fast, takes feedback well.

**Rules in effect:** Max 10 applications/day. Never apply twice to same opportunity. No false information. Show every application and wait for approval. One follow-up max, after 5-7 days.

**How sending works:** Agent cannot submit applications or send email. Paul pastes and sends each one manually.

---

## Applications

| # | Company | Platform | Role | Pay/stipend | Applied? | Date | Status | Next action |
|---|---------|----------|------|-------------|---------|------|--------|-------------|
| 1 | Canonical | canonical.com/careers/8249005 | Graduate Software Engineer, Open Source & Linux (central graduate scheme) | Salaried + bonus + USD 2,000/yr learning budget | NO — awaiting approval | — | Ready to send | Paste cover note into graduate scheme form |
| 2 | Canonical | canonical.com/careers/6707669 | Junior Ubuntu Software Engineer | Salaried + bonus + learning budget | NO — awaiting approval | — | Ready to send | Paste cover note into junior role form |
| 3 | FUTO (Immich) | jobs.lever.co/futo-org/f5b9b595... | Mobile Developer — Immich (Flutter) | Not stated (mid-level band) | NO — awaiting approval | — | Inquiry only (location unclear) | Send short location question to jobs@futo.tech |

### Non-application actions (immediate income)
| # | Platform | What | Pay | Applied? | Next action |
|---|----------|------|-----|---------|-------------|
| A | Outlier (Scale AI) — outlier.ai | AI Trainer / AI evaluation projects | Varies per project | NO | Sign up, complete AI eval tasks immediately |
| B | DataAnnotation.tech | 107 open roles incl. Coding, Generalist | $25–150/hr listed | NO | Check Kenya eligibility, then apply to Coding + Generalist |

---

## Rejected / Skipped

| Opportunity | Reason |
|-------------|--------|
| Flix — Netzwerkingenieur (Arbeitnow) | On-site Berlin, network engineering, German listing |
| Nord-Ostsee Automobile — Kundendienst Assistent | On-site Itzehoe, Germany; non-technical |
| Omega Enterprises — Junior Digital Assets Ops Analyst | Crypto ops, not software; no fit |
| AppSamurai — Business Development Specialist (BDR) | Sales role, not engineering |
| RINSE — Software Engineer | Remote restricted to US/Canada |
| Column — Software Engineers | On-site San Francisco only |
| Qualcomm — entry-level QEMU/DSP | Remote restricted to Canada; C/C++/Rust DSP |
| Lokker — Data Scientist | North America/Europe only; UTC+2 ceiling (Kenya is UTC+3) |
| Mattermost — Full-stack roles | Remote restricted to US and Canada |
| Datamint — Rust Systems Engineer | Requires Rust experience; $120k+ senior band |
| Menlo Research / Asimov — Founding engineers | Founding/senior roles, Singapore + Palo Alto |
| Wipro referral (HN post) | Legitimate but large enterprise, referral-gated; not a small company |

---

## Follow-ups Due

| # | Company | Days since applied | Draft status |
|---|---------|--------------------|--------------|
| — | — | — | — |

---

## Log

- 2026-10-06 — Tracker created.
- 2026-10-06 — Research pass: scanned 541 jobs across Remotive, Arbeitnow, RemoteOK, Jobicy + October 2026 HN "Who is hiring" thread (291 comments). Yield of genuinely junior + Kenya-eligible software roles was near zero. Best finds came from Canonical's public careers feed (310 roles) and FUTO's Lever board.
- 2026-10-06 — Drafted applications 1–3. Awaiting Paul's approval.
- 2026-10-06 — Built send automation. Playwright + installed Chrome verified working; Lever form fields mapped (resume, name, email, phone, location, org, LinkedIn, GitHub, portfolio, SUBMIT APPLICATION). `send_email.py` and `fill_lever.py` built and guard-tested. Awaiting: Gmail app password in `.gmail-creds`, plus `profile.json` and a real resume file.
- 2026-10-06 — `websearch` unavailable all session; `browser` tool has no desktop session connected. Workaround: direct HTTP/JSON APIs + Playwright via shell.
- 2026-10-06 — **Email pipeline WORKING.** `.gmail-creds` created (Notepad had appended `.txt`; renamed). Google app password had copied-in spacing; loader now strips whitespace. Test email sent successfully to paulnjugunanganga58@gmail.com. Log: `sent_log.jsonl`.
- 2026-10-06 — Resumes built: `resumes/resume_sw.pdf` and `resumes/resume_ai.pdf`, both single-page A4, rendered via Playwright.
- 2026-10-06 — Search capability severely limited this session. Blocked: `websearch` tool (empty), DuckDuckGo (CAPTCHA), Ecosia, Mojeek (403), Brave, Startpage, Yandex (all CAPTCHA/403). Bing works but ignores multi-clause queries. **No CAPTCHAs were solved, by policy.**
- 2026-10-06 — Verified 27 candidate employers by direct fetch. 11 alive, 11 dead/blocked (logged below).
- 2026-10-06 — Fetched SimplifyJobs New Grad Positions (494 roles). **0 remote-worldwide roles.** All "remote" = US/Canada only. Confirms large-company new grad programs don't hire from Kenya.
- 2026-10-06 — Verified 54 African tech companies. 33 alive, 25 with published emails. **17 real emails sent** to verified addresses (1 test + 1 FUTO + 5 early batch + 12 African tech companies).
- 2026-10-06 — Additional 10 African companies have contact forms but no published emails (Chipper Cash, Andela, Interswitch, Remita, Tala, Helium Health, Releaf, Semicolon, Azubi Africa). Manual form-fill needed.

## Verified Employer Targets (alive, with emails)

| Employer | Site status | Careers page | Contact found | Size note | Email sent |
|---|---|---|---|---|---|
| FUTO / Immich | 200 | Lever | contact@futo.tech | 7 devs - genuinely small | ✅ 2026-10-05 |
| MellowVans | 200 | contact form | info@mellowvans.com | Small - EV delivery | ✅ 2026-10-05 |
| Kuda | 200 | yes | help@kuda.com | Mid-size fintech | ✅ 2026-10-05 (x2) |
| iHUB Nairobi | 200 | yes | info@ihub.co.ke | Incubator/hub | ✅ 2026-10-05 |
| M-KOPA | 200 | yes | info@m-kopa.com | Large | ✅ 2026-10-05 |
| Flutterwave | 200 | yes | hi@flutterwavego.com | Large fintech | ✅ 2026-10-06 |
| Paystack | 200 | yes | hello@paystack.com | Large fintech | ✅ 2026-10-06 |
| Tunga | 200 | yes | bart@tunga.io | Talent marketplace | ✅ 2026-10-06 |
| SeamlessHR | 200 | yes | hello@seamlesshr.com | HR SaaS | ✅ 2026-10-06 |
| Cowrywise | 200 | yes | support@cowrywise.com | Fintech | ✅ 2026-10-06 |
| PiggyVest | 200 | no | contact@piggyvest.com | Fintech | ✅ 2026-10-06 |
| KoraPay | 200 | yes | marketing@korapay.com | Pan-African payments | ✅ 2026-10-06 |
| Konga | 200 | yes | help@konga.com | E-commerce | ✅ 2026-10-06 |
| Cars45 | 200 | yes | help@cars45.com | Auto marketplace | ✅ 2026-10-06 |
| Ro Health | 200 | yes | contact@rohealth.com | Healthtech | ✅ 2026-10-06 |
| ThriveAgric | 200 | yes | info@thriveagric.com | Agri-tech | ✅ 2026-10-06 |

## Manual Actions Needed (contact forms only, no published email)

| Company | URL | Note |
|---|---|---|
| Chipper Cash | https://chippercash.com/contact | 1 form |
| Andela | https://www.andela.com/contact | 3 forms |
| Interswitch | https://www.interswitchgroup.com | careers page, no email |
| Remita | https://www.remita.net | careers page, no email |
| Tala | https://tala.co | careers page, no email |
| Helium Health | https://www.heliumhealth.com | careers page, no email |
| Releaf | https://www.releaf.africa/contact | 1 form |
| Semicolon | https://www.semicolon.africa | 1 form |
| Azubi Africa | https://www.azubiafrica.org | careers page, no email |

## Dead or Blocked (do not contact)

basigo.co, devken.co, emobilis.com, looptelecom.co.ke, refactory.co.ke, saharahackerspace.org, senbo.co, sendyit.com, skygride.co, zembo.io, chandler.africa — all DNS/connection failure. nailab.co and cellulant.io returned 403 (bot-blocked, may still exist). wikimediafoundation.org/about/careers 404'd (wrong URL). decodon.africa connection error.

---

## Applications Sent Summary

| # | To | Subject | Date |
|---|---|---|---|
| 1 | paulnjugunanganga58@gmail.com | TEST | 2026-10-05 |
| 2 | contact@futo.tech | Flutter developer - question about remote | 2026-10-05 |
| 3 | info@mellowvans.com | Junior Python/Flutter developer - small tasks | 2026-10-05 |
| 4 | help@kuda.com | Junior Python/Flutter developer - small tasks | 2026-10-05 |
| 5 | info@ihub.co.ke | Junior Python/Flutter developer - small tasks | 2026-10-05 |
| 6 | info@m-kopa.com | Junior Python/Flutter developer - small tasks | 2026-10-05 |
| 7 | hi@flutterwavego.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 8 | hello@paystack.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 9 | bart@tunga.io | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 10 | hello@seamlesshr.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 11 | support@cowrywise.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 12 | contact@piggyvest.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 13 | help@kuda.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 14 | marketing@korapay.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 15 | help@konga.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 16 | help@cars45.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 17 | contact@rohealth.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |
| 18 | info@thriveagric.com | Junior Python/Flutter developer - Kenya | 2026-10-06 |

---

## Canonical Forms (pre-filled, need manual submit)

- **Graduate Software Engineer**: https://canonical.com/careers/8249005 — 13 required fields empty (maths grade, language grade, ethnicity, gender, travel agreement, reCAPTCHA). Resume attached, essays drafted.
- **Junior Ubuntu Software Engineer**: https://canonical.com/careers/6707669 — same.

---

## Immediate Cash (no application needed)

1. **Outlier.ai** — AI trainer, "900K+ college graduates, work from wherever"
2. **DataAnnotation.tech** — 107 roles, $25-150/hr. Check Kenya eligibility first.

---

## Notes / Learnings

- Mainstream remote boards (RemoteOK, Remotive, Jobicy, Arbeitnow) are ~95% senior/US-locked. Low yield for a Kenya-based junior. Do not spend much time here.
- Highest-yield sources found so far: Canonical's `/careers/feed` (machine-readable, has real junior/graduate roles, remote in every timezone), and HN monthly "Who is hiring" thread for startups.
- `websearch` tool returned zero results for every query — unusable. Use direct HTTP fetches and public APIs instead.
- No browser session connected, so JS-rendered pages (Lever listings, job board search UIs) cannot be read directly. Prefer RSS/JSON endpoints.
- Next lane to build: verified target list of small Kenya/East Africa dev agencies and startups for direct outreach. That is where junior volume actually is.