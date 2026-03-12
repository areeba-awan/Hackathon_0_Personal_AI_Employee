# Personal AI Employee - Hackathon 0 (Silver Tier)

**Panaversity Hackathon 0: Building Autonomous FTEs (Full-Time Equivalent) in 2026**  
**Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

This project implements a **Silver Tier** Personal AI Employee using Claude Code as the reasoning engine and local file system as memory/dashboard. The system is fully local-first, privacy-focused, and demonstrates proactive automation.

## Features Implemented (Silver Tier)

- **Two Watchers**:
  - Gmail Watcher (`gmail_watcher.py`): Monitors unread + important emails → creates action files in `Needs_Action`
  - LinkedIn Watcher (`linkedin_watcher.py`): Monitors LinkedIn activity (posts, messages, etc.) using token → creates action files on keyword match

- **MCP Server for External Actions**:
  - Email send capability via Gmail OAuth2 (nodemailer + google-auth-library)
  - Local HTTP endpoint: `POST /send_email`

- **Claude Integration**:
  - Agent Skills loaded (task-processor, dashboard-updater, social-poster, reasoning-loop)
  - Reasoning loop creates Plan.md files for multi-step tasks
  - Human-in-the-loop approval via Pending_Approval folder (manual move to Approved/Rejected)

- **Orchestrator** (`orchestrator.py`):
  - Starts all watchers in threads
  - Monitors folders for approval workflow
  - Triggers Claude processing on new Needs_Action files

- **Basic Scheduling Ready**:
  - Can be added to Windows Task Scheduler for daily auto-run

## Tech Stack

- **Reasoning Engine**: Claude Code (free tier with Router)
- **Watchers**: Python (watchdog, google-api-python-client, playwright)
- **MCP Server**: Node.js + Express + Nodemailer + Google APIs
- **Memory/Dashboard**: Local Markdown files (Needs_Action, Plans, Pending_Approval, Done)
- **Dependencies**:
  - Python: google-api-python-client, google-auth-oauthlib, google-auth-httplib2, watchdog
  - Node.js: express, nodemailer, googleapis

## How to Run

1. **Prerequisites**
   - Python 3.10+
   - Node.js 18+
   - Claude Code extension in VS Code
   - Gmail OAuth credentials.json (Desktop/Web app)
   - LinkedIn access token in `.env`

2. **Setup**
   ```bash
   # Activate virtual environment
   .venv\Scripts\Activate.ps1

   # Install Python dependencies
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib watchdog playwright

   # Install Node.js dependencies (in mcp_servers folder)
   cd mcp_servers
   npm install express nodemailer googleapis
   cd ..

3. **Start MCP Email Server (separate terminal)**

node mcp_servers/email_mcp.js

4. **Start Main Orchestrator (recommended)**
python orchestrator.py

5. **Starts Gmail + LinkedIn watchers automatically**

6. **Monitors Needs_Action and Pending_Approval folders**
7. **Triggers Claude processing**

8. **Manual Watcher Test (optional)**

python watchers/gmail_watcher.py
python watchers/linkedin_watcher.py

9. **Folder Structure**

textSilver Tier/
├── .env                  # LinkedIn token, secrets
├── credentials.json      # Gmail OAuth
├── token.json            # Gmail OAuth token (auto-generated)
├── orchestrator.py       # Main startup script
├── watchers/
│   ├── gmail_watcher.py
│   └── linkedin_watcher.py
├── mcp_servers/
│   └── email_mcp.js
├── Needs_Action/         # New tasks from watchers
├── Plans/                # Claude-generated plans
├── Pending_Approval/     # Human review needed
├── Approved/
├── Rejected/
├── Done/
└── README.md

9. **Future (Gold Tier Ideas)**

Odoo ERP integration via JSON-RPC
Full CEO Briefing generation
Cloud deployment (Oracle free VM)

**Made with ❤️ by Areeba Awan** 