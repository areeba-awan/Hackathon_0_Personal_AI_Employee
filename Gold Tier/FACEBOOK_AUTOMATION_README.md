# Facebook Automation - Complete Guide

## Overview

Complete Facebook automation system that:
- ✅ Automatically logs in to Facebook
- ✅ Monitors messages in real-time (every 30 seconds)
- ✅ Auto-posts messages when browser opens
- ✅ Saves all messages and posts locally
- ✅ Browser stays open for continuous monitoring

## Quick Start (One Line!)

```bash
node facebook_run.js your@email.com yourpassword "Hello World"
```

That's it! Browser will open and:
1. Auto-login to Facebook
2. Post your message
3. Start monitoring for new messages
4. Keep running until you press Ctrl+C

## Files

| File | Purpose |
|------|---------|
| `facebook_run.js` | One-line launcher - just pass email, password, and messages |
| `facebook_master.js` | Master controller with configuration management |
| `facebook_automation.js` | Core automation engine |
| `facebook_config.json` | Configuration file |
| `facebook_messages.json` | Saved messages |
| `facebook_posts.json` | Saved posts |

## Usage Examples

### Simple Monitoring (No Posts)
```bash
node facebook_run.js user@gmail.com password123
```

### Post One Message
```bash
node facebook_run.js user@gmail.com password123 "Hello Facebook!"
```

### Post Multiple Messages
```bash
node facebook_run.js user@gmail.com password123 "Post 1" "Post 2" "Post 3"
```

## Advanced Usage

### Using facebook_master.js directly

Configure:
```bash
node facebook_master.js config set email user@gmail.com
node facebook_master.js config set password password123
node facebook_master.js config add-post "Hello World"
```

Start:
```bash
node facebook_master.js start
```

### Using facebook_automation.js directly

Login:
```bash
node facebook_automation.js login user@gmail.com password123
```

Post:
```bash
node facebook_automation.js post "Your message"
```

Monitor:
```bash
node facebook_automation.js monitor 30000
```

Check messages:
```bash
node facebook_automation.js check-messages
```

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

## Data Storage

All data is stored locally:
- `facebook_messages.json` - All received messages
- `facebook_posts.json` - All posted messages
- `sessions/facebook/` - Browser session (cookies, cache)
- `facebook_config.json` - Configuration

## Real Implementation

✅ **Real Facebook Integration:**
- Uses Playwright for real browser automation
- Connects to actual Facebook.com
- Detects real messages from message threads
- Posts to real Facebook feed
- Maintains persistent session

✅ **No Mock Data:**
- All messages are real from Facebook
- All posts go to real Facebook
- Session persists across runs
- Browser automation is real-time

## Troubleshooting

### Browser doesn't open
```bash
# Check if Playwright is installed
npm install playwright

# Verify browsers are installed
PLAYWRIGHT_BROWSERS_PATH=D:\playwright-browsers npx playwright install
```

### Login fails
- Check email and password are correct
- Try manual login in the browser
- Check for 2FA requirements

### Messages not detected
- Wait 30 seconds for first check
- Check `facebook_messages.json` for saved messages
- Try faster monitoring: `node facebook_run.js email pass` (then Ctrl+C and restart)

### Posts not working
- Make sure you're logged in
- Check browser console for errors
- Try posting manually first

## Environment Variables

```bash
export FACEBOOK_EMAIL=your@email.com
export FACEBOOK_PASSWORD=yourpassword
export PLAYWRIGHT_BROWSERS_PATH=D:\playwright-browsers
```

## Security Notes

⚠️ **Important:**
- Store credentials securely
- Don't commit `facebook_config.json` to git
- Use environment variables for sensitive data
- Session data is stored locally in `sessions/` folder

## What Gets Saved

### Messages (`facebook_messages.json`)
```json
{
  "id": "msg_hash",
  "text": "Message preview",
  "fullText": "Full message content",
  "timestamp": "2026-04-04T18:06:42.923Z",
  "platform": "facebook",
  "read": false,
  "source": "real_facebook"
}
```

### Posts (`facebook_posts.json`)
```json
{
  "id": "post_timestamp",
  "message": "Posted message",
  "image": null,
  "timestamp": "2026-04-04T18:06:42.923Z",
  "platform": "facebook",
  "status": "posted"
}
```

## Stopping the Automation

Press `Ctrl+C` in the terminal to stop:
- Monitoring stops
- Browser closes
- Process exits cleanly

## Support

For issues:
1. Check the troubleshooting section
2. Review `facebook_config.json` settings
3. Check browser console for errors
4. Try manual login first

---

**Version:** 1.0.0
**Last Updated:** 2026-04-04
**Status:** ✅ Ready to use
**Real Implementation:** ✅ Yes - Real Facebook, Real Messages, Real Posts
