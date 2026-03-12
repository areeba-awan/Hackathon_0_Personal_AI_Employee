# LinkedIn Watcher - Quick Start Guide

## What It Does

The LinkedIn watcher automatically:
1. Monitors your `Inbox/` folder for LinkedIn files
2. Detects new files named `LINKEDIN_*.md` or `LINKEDIN_*.txt`
3. Moves them to `Needs_Action/` folder with `DROP_` prefix
4. Creates automation task files automatically
5. Logs everything to terminal + file

**No manual file creation needed** - just drop LinkedIn content in Inbox!

## Installation

LinkedIn watcher is already included. Just ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

## Usage

### Run LinkedIn Watcher Standalone
```bash
python watchers/linkedin_watcher.py
```

Output:
```
Initializing LinkedInWatcher...
Monitoring Inbox for LinkedIn files (LINKEDIN_*.md or LINKEDIN_*.txt)

LinkedIn watcher started - monitoring Inbox every 60s
Copy LinkedIn posts/messages to Inbox as LINKEDIN_*.md or LINKEDIN_*.txt
(Ctrl+C to stop)

Found 1 new LinkedIn files
[TASK] Created: DROP_LINKEDIN_test_post.md
```

### Run All Watchers (Inbox + Gmail + LinkedIn)
```bash
python watchers/orchestrator.py
```

LinkedIn watcher runs in background thread automatically.

## How to Use

### Step 1: Copy LinkedIn Content to Inbox
Create a file in `Inbox/` folder with name starting with `LINKEDIN_`:

**File name examples:**
- `LINKEDIN_post_001.md`
- `LINKEDIN_article_from_john.txt`
- `LINKEDIN_engagement_idea.md`

**File content format:**
```markdown
---
type: linkedin_post
author: John Doe
source: LinkedIn Feed
detected: 2026-03-12T17:19:00Z
priority: medium
status: pending
---

## Post Content
Your LinkedIn post content here...

## Automation Tasks
- [ ] Generate engagement comment
- [ ] Schedule repost
- [ ] Add to content calendar
- [ ] Extract key insights
- [ ] Create follow-up post

## Suggested Actions
- Reply with relevant comment
- Share with network
- Save for later reference
```

### Step 2: Watcher Processes File
The watcher automatically:
1. Detects the file in Inbox/
2. Moves it to Needs_Action/ with DROP_ prefix
3. Creates task file: `DROP_LINKEDIN_post_001.md`

### Step 3: Process Task
Review the task file in `Needs_Action/` and:
1. Move to `Approved/` when ready
2. Run task processor: `python task_processor.py`
3. Task moves to `Done/` after processing

## Configuration

### Check Interval
Edit watcher initialization:
```python
watcher = LinkedInWatcher(vault=".", check_interval=60)  # 60 seconds
```

Or in orchestrator.py line 135:
```python
check_interval=60  # Change to desired seconds
```

## What Gets Created

When a LinkedIn file is detected in Inbox:

**File moves from:**
- `Inbox/LINKEDIN_post_001.md`

**File moves to:**
- `Needs_Action/DROP_LINKEDIN_post_001.md`

Content is preserved exactly as you provided it.

## Logs

Check activity in:
- **Terminal:** Real-time output
- **File:** `linkedin_watcher.log` - Full history

## Stopping the Watcher

Press `Ctrl+C` in terminal:
```
^C

Watcher stopped
```

## Integration with Task Processor

After tasks are created in `Needs_Action/`:

1. Review the task file
2. Move to `Approved/` when ready
3. Run task processor:
```bash
python task_processor.py
```

4. Tasks move to `Done/` after processing

## Troubleshooting

### No files being detected
- Make sure files are in `Inbox/` folder
- Check file name starts with `LINKEDIN_`
- Check `linkedin_watcher.log` for errors

### Files not moving
- Check folder permissions
- Ensure `Needs_Action/` folder exists
- Check disk space

### Watcher not running
- Make sure terminal is open
- Check for error messages
- Verify Python is installed

## Tips

✅ Use consistent file naming: `LINKEDIN_*.md`
✅ Keep watcher running in terminal
✅ Check `Needs_Action/` folder for created tasks
✅ Use `Ctrl+C` to stop gracefully
✅ Check logs if something goes wrong
✅ Can run multiple instances (one per terminal)

## Example Workflow

```bash
# Terminal 1: Start watcher
python watchers/linkedin_watcher.py

# Terminal 2: Create LinkedIn content file
echo "---
type: linkedin_post
author: Jane Smith
source: LinkedIn Feed
detected: 2026-03-12T17:26:00Z
priority: high
status: pending
---

## Post Content
Amazing insights on AI automation!

## Automation Tasks
- [ ] Generate engagement comment
- [ ] Schedule repost
" > Inbox/LINKEDIN_ai_insights.md

# Watcher automatically moves it to Needs_Action/DROP_LINKEDIN_ai_insights.md

# Terminal 2: Process tasks
python task_processor.py
```

## Next Steps

1. Run: `python watchers/linkedin_watcher.py`
2. Create LinkedIn files in `Inbox/` folder
3. Watch them auto-move to `Needs_Action/`
4. Process with `python task_processor.py`
5. Check `Done/` folder for completed tasks

---

**Happy automating! 🚀**
