# Job Application Agent

**A Python-powered job search and application automation toolkit.**

Job Application Agent is a personal automation project designed to streamline the repetitive parts of finding and applying for software engineering and AI-related opportunities.

It combines browser automation, email outreach, resume generation, company verification and contact discovery into one workflow.

The goal is simple: spend less time repeating application tasks and more time finding relevant opportunities and getting hired.

## Key Features

### 1. Automated Email Outreach
- Send job inquiry emails through Gmail SMTP.
- Support both inline email content and external letter files.
- Dry-run mode for reviewing messages before sending.
- Detect common placeholder text before transmission.
- Record email activity in a JSONL audit log.

### 2. Job Application Automation
- Automate application form filling on Lever.
- Pre-fill Canonical graduate and junior application forms.
- Populate personal information, contact details and professional links.
- Upload tailored resumes.
- Insert prepared application responses.
- Capture screenshots for manual review.
- Detect missing required fields.

**Human verification is intentional:** CAPTCHA challenges are not bypassed, and applications can be reviewed before submission.

### 3. Resume Generation
- Maintain tailored resumes for different career tracks.
- Generate A4 PDF resumes from HTML templates.
- Use Playwright and Chrome for PDF rendering.
- Preview resume layouts through screenshots.

Currently supported resume tracks:
- Software Engineering
- AI Evaluation

### 4. Company Verification
- Check whether company websites are accessible.
- Inspect website titles and careers pages.
- Discover publicly listed email addresses.
- Reject inaccessible or potentially unsuitable targets before outreach.

### 5. Contact Discovery
- Search company contact, careers, jobs and about pages.
- Extract publicly available email addresses.
- Identify contact forms for manual outreach.
- Inspect selected public recruitment boards.

### 6. Web Search
- Perform browser-driven Bing searches using Playwright.
- Extract search result titles, links and descriptions.
- Export search results into JSON for further processing.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Playwright | Browser automation |
| Chrome / Chromium | Form interaction and PDF rendering |
| Requests | HTTP requests and website verification |
| Gmail SMTP | Email delivery |
| HTML / CSS | Resume templates |
| JSON / JSONL | Configuration and activity logging |
| PowerShell | Windows automation |

## Project Structure

```text
job-application-agent/
│
├── letters/
│   └── Outreach email templates
│
├── resumes/
│   ├── resume_sw.html
│   └── resume_ai.html
│
├── shots/
│   └── Generated screenshots
│
├── profile.json
├── profile.template.json
├── resume_master.md
│
├── send_email.py
├── fill_lever.py
├── fill_canonical.py
│
├── render_resume.py
├── preview_resume.py
│
├── verify_targets.py
├── find_contacts.py
├── search_web.py
│
├── ANSWERS.md
├── TRACKER.md
├── SESSION_SUMMARY.md
├── DRAFTS-batch-1.md
│
├── push_to_github.ps1
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Google Chrome installed
- Gmail account with an App Password (for email outreach)
- Windows, Linux or macOS

### 1. Clone the repository

```bash
git clone https://github.com/pauled12345/job-application-agent.git

cd job-application-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install requests playwright
```

The project uses the installed Google Chrome browser through Playwright's Chrome channel.

### 4. Configure your profile

Copy the profile template:

```powershell
Copy-Item profile.template.json profile.json
```

Edit `profile.json` and provide your actual details:

- Full name
- Email
- Phone number
- Location
- GitHub profile
- LinkedIn profile
- Academic information

Use accurate information only.

### 5. Configure Gmail

Create a `.gmail-creds` file in the project root:

```text
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

Use a Google App Password rather than your normal account password.

Never commit this file.

## Usage

### Email Outreach

Preview an email without sending:

```bash
python send_email.py \
  --to recipient@example.com \
  --subject "Junior Developer Opportunity" \
  --body "Your application message"
```

Send the email:

```bash
python send_email.py \
  --to recipient@example.com \
  --subject "Junior Developer Opportunity" \
  --body "Your application message" \
  --send
```

You can also provide an external letter:

```bash
python send_email.py \
  --to recipient@example.com \
  --subject "Job Application" \
  --body-file letters/africa_outreach.txt
```

Add `--send` when you are ready to transmit.

### Lever Applications

```bash
python fill_lever.py \
  --url "https://jobs.lever.co/company/job-id" \
  --resume "resumes/resume_sw.pdf"
```

The browser opens, fills available fields and saves a screenshot for review.

Add `--submit` to attempt submission after review. CAPTCHA challenges still require human interaction.

### Canonical Applications

Graduate Software Engineer:

```bash
python fill_canonical.py --role grad --headful
```

Junior Ubuntu Software Engineer:

```bash
python fill_canonical.py --role junior --headful
```

The script uses prepared application responses and the selected resume.

### Generate Resumes

```bash
python render_resume.py
```

### Preview Resumes

```bash
python preview_resume.py
```

### Verify Companies

```bash
python verify_targets.py
```

### Discover Contacts

```bash
python find_contacts.py
```

### Search for Opportunities

```bash
python search_web.py "junior Python developer remote worldwide"
```

Export results as JSON:

```bash
python search_web.py --json "remote junior software engineering jobs"
```

## Safety and Reliability

This project incorporates several safeguards:

- Email sending is disabled by default.
- Placeholder content is checked before sending.
- Email activity is logged.
- Application forms can be reviewed before submission.
- CAPTCHA mechanisms are not bypassed.
- Personal and academic information should only be populated with verified details.
- Credentials, generated screenshots and runtime logs are excluded through `.gitignore`.

The application automation is dependent on the structure of external websites. Changes to application form fields or page layouts may require selector updates.

## Current Project Status

The development session documented the following activity:

| Metric | Recorded result |
|---|---:|
| Outreach emails | 18 |
| Companies verified | 80+ |
| Companies with discovered emails | 25 |
| Canonical forms pre-filled | 2 |
| Contact forms identified | 9 |

These are recorded project activity figures, not confirmed job offers or successful application outcomes.

## Future Improvements

Potential development directions include:

- Unified application dashboard.
- Centralized job discovery and filtering.
- Automated resume selection based on job descriptions.
- Application status tracking and follow-up scheduling.
- Duplicate application detection.
- More recruitment platform integrations.
- Improved browser automation reliability.
- Centralized reporting and analytics.

## Disclaimer

This project is intended for personal job-search productivity and educational purposes.

It does not guarantee employment, successful application submission or responses from employers. Users remain responsible for reviewing application information, complying with recruitment platform policies and completing required verification steps.

## Author

**Paul Njuguna Nganga**

Computer Science Student | Python | Automation | AI Integration

GitHub: [@pauled12345](https://github.com/pauled12345)

---

*Built to make job hunting less repetitive and more systematic.*
