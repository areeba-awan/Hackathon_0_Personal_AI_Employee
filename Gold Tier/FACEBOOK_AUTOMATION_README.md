# Facebook Automation - Complete Guide

## Overview

Complete Facebook automation system that:
- ✅ Automatically logs in to Facebook
- ✅ Monitors messages in real-time (every 30 seconds)
- ✅ Auto-posts messages when browser opens
- ✅ Saves all messages and posts locally
- ✅ Browser stays open for continuous monitoring

## Quick Start (3 Steps)

### Step 1: Configure
```bash
node facebook_master.js config set email your@email.com
node facebook_master.js config set password yourpassword
```

### Step 2: Add Auto-Posts (Optional)
```bash
node facebook_master.js config add-post "Hello World"
node facebook_master.js config add-post "Check this out"
```

### Step 3: Start
```bash
node facebook_master.js start
```

**That's it!** Browser will open automatically and:
1. Login to Facebook
2. Start monitoring messages
3. Auto-post your messages
4. Keep running until you press Ctrl+C

---

## Files

| File | Purpose |
|------|---------|
| `facebook_master.js` | Main entry point - handles everything |
| `facebook_automation.js` | Core automation logic |
| `facebook_config.json` | Configuration file |
| `facebook_messages.json` | Saved messages |
| `facebook_posts.json` | Saved posts |

---

## Commands

### Start Automation
```bash
node facebook_master.js start
```
Starts the complete automation:
- Opens browser
- Auto-logs in
- Monitors messages
- Auto-posts configured messages

### Post a Message
```bash
node facebook_master.js post "Your message here"
node facebook_master.js post "Message with image" /path/to/image.jpg
```

### Configuration

**Show current config:**
```bash
node facebook_master.js config show
```

**Set a value:**
```bash
node facebook_master.js config set email user@gmail.com
node facebook_master.js config set password mypassword
node facebook_master.js config set autoLogin true
node facebook_master.js config set headless false
node facebook_master.js config set monitorInterval 30000
```

**Add auto-post message:**
```bash
node facebook_master.js config add-post "Hello World"
```

---

## Configuration File

`facebook_config.json`:
```json
{
  "email": "your@email.com",
  "password": "yourpassword",
  "autoPost": [
    { "message": "Hello World", "image": null },
    { "message": "Check this out", "image": null }
  ],
  "monitorInterval": 30000,
  "autoLogin": true,
  "headless": false,
  "enabled": true
}
```

**Options:**
- `email` - Facebook email
- `password` - Facebook password
- `autoPost` - Array of messages to post on startup
- `monitorInterval` - How often to check for messages (ms)
- `autoLogin` - Auto-login on start (true/false)
- `headless` - Run browser in headless mode (true/false)
- `enabled` - Enable/disable automation

---

## How It Works

### On Startup
1. Browser opens (visible on screen)
2. Auto-logs in with your credentials
3. Waits for 2FA if needed (2 minutes)
4. Starts monitoring messages
5. Posts all configured messages

### During Monitoring
- Every 30 seconds: Checks for new messages
- Saves new messages to `facebook_messages.json`
- Displays notifications for new messages
- Keeps browser open and active

### Message Format
```json
{
  "id": "msg_1234567890_0",
  "text": "Message content",
  "timestamp": "2026-03-28T15:15:21.379Z",
  "platform": "facebook",
  "read": false
}
```

### Post Format
```json
{
  "id": "post_1234567890",
  "message": "Posted message",
  "image": null,
  "timestamp": "2026-03-28T15:15:21.379Z",
  "platform": "facebook",
  "status": "posted"
}
```

---

## Troubleshooting

### Browser doesn't open
- Check if Playwright is installed: `npm install playwright`
- Try: `node facebook_master.js config set headless false`

### Login fails
- Check email and password are correct
- Try manual login in the browser
- Check for 2FA requirements

### Messages not detected
- Wait 30 seconds for first check
- Check `facebook_messages.json` for saved messages
- Try: `node facebook_master.js config set monitorInterval 15000` (faster checks)

### Posts not working
- Make sure you're logged in
- Check browser console for errors
- Try posting manually first

---

## Advanced Usage

### Environment Variables
```bash
export FACEBOOK_EMAIL=your@email.com
export FACEBOOK_PASSWORD=yourpassword
node facebook_master.js start
```

### Faster Monitoring
```bash
node facebook_master.js config set monitorInterval 15000
```

### Headless Mode (No Browser Window)
```bash
node facebook_master.js config set headless true
```

### Batch Posts
```bash
node facebook_master.js config add-post "Post 1"
node facebook_master.js config add-post "Post 2"
node facebook_master.js config add-post "Post 3"
node facebook_master.js start
```

---

## Data Storage

All data is stored locally:
- `facebook_messages.json` - All received messages
- `facebook_posts.json` - All posted messages
- `sessions/facebook/` - Browser session (cookies, cache)
- `facebook_config.json` - Configuration

---

## Security Notes

⚠️ **Important:**
- Store credentials securely
- Don't commit `facebook_config.json` to git
- Use environment variables for sensitive data
- Session data is stored locally in `sessions/` folder

---

## Examples

### Example 1: Simple Auto-Post
```bash
node facebook_master.js config set email user@gmail.com
node facebook_master.js config set password pass123
node facebook_master.js config add-post "Hello Facebook!"
node facebook_master.js start
```

### Example 2: Monitor Only (No Posts)
```bash
node facebook_master.js config set email user@gmail.com
node facebook_master.js config set password pass123
node facebook_master.js start
```

### Example 3: Post with Image
```bash
node facebook_master.js post "Check this photo!" /path/to/photo.jpg
```

### Example 4: Faster Monitoring
```bash
node facebook_master.js config set monitorInterval 15000
node facebook_master.js start
```

---

## What Gets Saved

### Messages (`facebook_messages.json`)
- All messages from all conversations
- Timestamp of when received
- Message text
- Read/unread status

### Posts (`facebook_posts.json`)
- All posts you made
- Timestamp of posting
- Message content
- Image path (if any)
- Status (posted/failed)

---

## Stopping the Automation

Press `Ctrl+C` in the terminal to stop:
- Monitoring stops
- Browser closes
- Process exits cleanly

---

## Support

For issues:
1. Check the troubleshooting section
2. Review `facebook_config.json` settings
3. Check browser console for errors
4. Try manual login first

---

**Version:** 1.0.0
**Last Updated:** 2026-03-28
**Status:** ✅ Ready to use
