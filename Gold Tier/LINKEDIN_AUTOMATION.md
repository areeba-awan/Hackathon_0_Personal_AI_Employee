# LinkedIn Automation Watcher - Complete Guide

## What It Does

Full LinkedIn automation that:
1. Opens LinkedIn in browser automatically
2. Waits for you to login manually
3. Detects successful login automatically
4. Monitors feed every 30 seconds
5. Extracts new posts (author, content)
6. **Generates engagement comments automatically**
7. Creates automation tasks in Needs_Action/
8. Shows real-time output in terminal

**Everything happens automatically after login!**

## Installation

Dependencies already included in requirements.txt:
```bash
pip install -r requirements.txt
```

Key packages:
- `selenium==4.15.2` - Browser automation
- `webdriver-manager==4.0.1` - Chrome driver auto-management

## Quick Start

### Step 1: Run the Watcher
```bash
python watchers/linkedin_watcher.py
```

### Step 2: Login When Browser Opens
- Browser opens automatically
- LinkedIn login page loads
- You login manually (up to 5 minutes)
- Watcher detects login automatically

### Step 3: Watch Automation Happen
Terminal shows real-time output:
```
======================================================================
LINKEDIN AUTOMATION WATCHER
======================================================================

[SETUP] Initializing Chrome driver...
[OK] Chrome driver ready
[ACTION] Opening LinkedIn...
[OK] LinkedIn login page opened in browser
[WAIT] Please login manually in the browser window...
[OK] Login successful!

======================================================================
AUTOMATION STARTED - MONITORING FEED
======================================================================
[INFO] Checking feed every 30 seconds
[INFO] Press Ctrl+C to stop

[17:56:43] Checking feed...
[SCAN] Found 12 posts on feed
[NEW] Post from John Doe: Great insights on AI automation...
[NEW] Post from Jane Smith: Machine learning best practices...
[PROCESS] Processing 2 new posts...
[TASK] Created: LINKEDIN_urn:li:activity:1234567890.md
[TASK] Created: LINKEDIN_urn:li:activity:0987654321.md

[17:57:13] Checking feed...
[SCAN] Found 12 posts on feed
[INFO] No new posts
```

## What Gets Created

### Task Files in Needs_Action/
**File name:** `LINKEDIN_urn:li:activity:1234567890.md`

**File content:**
```markdown
---
type: linkedin_post
author: John Doe
source: LinkedIn Feed
detected: 2026-03-12T17:56:43Z
priority: high
status: pending
automation: true
---

## Post Content
Great insights on AI automation and productivity tools...

## Generated Engagement Comment
Great insights! This is really valuable.

Key takeaways:
- Automation saves time
- Real-time monitoring is crucial
- Integration is key

Would love to discuss more about this approach.

## Automation Tasks
- [ ] Post engagement comment
- [ ] Schedule repost
- [ ] Add to content calendar
- [ ] Extract key insights
- [ ] Create follow-up post

## Suggested Actions
- Review and post comment
- Share with network
- Save for later reference
```

## Features

### Automatic Post Detection
- Scans feed every 30 seconds (configurable)
- Extracts post author and content
- Avoids duplicate processing
- Scrolls to load more posts

### Automatic Comment Generation
- Creates relevant engagement comments
- Includes key takeaways
- Professional tone
- Ready to post

### Real-Time Terminal Output
```
[SETUP] - Setup messages
[OK] - Success messages
[ACTION] - Actions being taken
[WAIT] - Waiting for something
[SCAN] - Scanning feed
[NEW] - New post found
[PROCESS] - Processing posts
[TASK] - Task created
[INFO] - Information
[ERROR] - Errors
[STOP] - Stopping
```

### Session Persistence
- Saves processed posts to `linkedin_session.json`
- Avoids reprocessing same posts
- Survives restarts
- Delete file to reset

## Configuration

### Check Interval
Change how often feed is checked:

```python
# In main section
watcher = LinkedInAutomationWatcher(vault=".", check_interval=30)
# 30 = check every 30 seconds
# 60 = check every 60 seconds
```

### Or in orchestrator.py:
```python
check_interval=30  # Adjust as needed
```

## Workflow

### 1. Start Watcher
```bash
python watchers/linkedin_watcher.py
```

### 2. Login in Browser
- Browser opens automatically
- You login manually
- Watcher detects login

### 3. Monitor Feed
- Watcher checks feed every 30 seconds
- Extracts new posts
- Generates comments
- Creates tasks

### 4. Review Tasks
- Check `Needs_Action/` folder
- Review generated comments
- Move to `Approved/` when ready

### 5. Process Tasks
```bash
python task_processor.py
```

### 6. Check Results
- Tasks move to `Done/` folder
- Comments posted (if approved)
- Activity logged

## Logs

### Terminal Output
Real-time status and activity shown in terminal

### Log File
`linkedin_watcher.log` - Complete history with timestamps

### Check Logs
```bash
tail -f linkedin_watcher.log
```

## Stopping the Watcher

Press `Ctrl+C` in terminal:
```
^C

[STOP] Automation stopped
[OK] Browser closed
```

## Troubleshooting

### Browser Not Opening
- Check if Chrome is installed
- Check internet connection
- Try running again

### Login Timeout
- Make sure you login within 5 minutes
- Check browser window
- Try again

### No Posts Detected
- Make sure you're logged in
- Check if feed has posts
- Scroll in browser to load posts
- Check `linkedin_watcher.log`

### Chrome Driver Issues
```bash
pip install --upgrade webdriver-manager
```

## Integration with Orchestrator

Run all watchers together:
```bash
python watchers/orchestrator.py
```

LinkedIn watcher runs as background thread automatically.

## Tips

✅ Keep browser window visible
✅ Don't close terminal while running
✅ Check terminal for real-time updates
✅ Review generated comments before posting
✅ Use Ctrl+C to stop gracefully
✅ Check logs if issues occur
✅ Delete linkedin_session.json to reset

## Advanced Usage

### Custom Comment Generation
Edit the `generate_engagement_comment()` method in linkedin_watcher.py:

```python
def generate_engagement_comment(self, post: dict) -> str:
    """Generate engagement comment for post"""
    post_text = post['text'][:100]
    comment = f"""Your custom comment here...

    Based on: {post_text}"""
    return comment
```

### Adjust Check Interval
```python
# Check every 60 seconds instead of 30
watcher = LinkedInAutomationWatcher(vault=".", check_interval=60)
```

### Limit Posts Processed
Edit line in `extract_feed_posts()`:
```python
for idx, post in enumerate(post_elements[:5]):  # Process top 5 posts
```

## Example Session

```bash
$ python watchers/linkedin_watcher.py

======================================================================
LINKEDIN AUTOMATION WATCHER
======================================================================

[SETUP] Initializing Chrome driver...
[OK] Chrome driver ready
[ACTION] Opening LinkedIn...
[OK] LinkedIn login page opened in browser
[WAIT] Please login manually in the browser window...

[User logs in...]

[OK] Login successful!

======================================================================
AUTOMATION STARTED - MONITORING FEED
======================================================================
[INFO] Checking feed every 30 seconds
[INFO] Press Ctrl+C to stop

[17:56:43] Checking feed...
[SCAN] Found 12 posts on feed
[NEW] Post from John Doe: Great insights on AI automation...
[PROCESS] Processing 1 new posts...
[TASK] Created: LINKEDIN_urn:li:activity:1234567890.md

[17:57:13] Checking feed...
[SCAN] Found 12 posts on feed
[INFO] No new posts

[17:57:43] Checking feed...
[SCAN] Found 13 posts on feed
[NEW] Post from Jane Smith: Machine learning best practices...
[PROCESS] Processing 1 new posts...
[TASK] Created: LINKEDIN_urn:li:activity:0987654321.md

^C

[STOP] Automation stopped
[OK] Browser closed
```

## Next Steps

1. Run: `python watchers/linkedin_watcher.py`
2. Login when browser opens
3. Watch terminal for real-time updates
4. Check `Needs_Action/` for created tasks
5. Review generated comments
6. Move approved tasks to `Approved/`
7. Run: `python task_processor.py`
8. Check `Done/` for completed tasks

---

**Full LinkedIn automation ready to go! 🚀**
