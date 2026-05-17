# Social Poster Skill

## Description
Prepares LinkedIn post drafts for sales generation and writes them to Pending_Approval folder for review before publishing.

## Purpose
Generate professional LinkedIn content for lead generation and sales outreach. Creates draft posts that require approval before going live.

## Usage

### Basic Invocation
```
/social-poster <topic> [--tone=professional|casual] [--cta=true|false]
```

### Parameters
- `topic`: LinkedIn post topic (e.g., "AI automation benefits", "Silver Tier features")
- `--tone`: Writing style - professional (default) or casual
- `--cta`: Include call-to-action button (default: true)

## How It Works

1. **Content Generation**:
   - Creates engaging LinkedIn post (150-300 words)
   - Includes relevant hashtags
   - Adds professional formatting
   - Incorporates sales angle

2. **Draft Creation**:
   - Writes to Pending_Approval/LINKEDIN_[topic]_[timestamp].md
   - Includes metadata (tone, CTA, target audience)
   - Adds suggested hashtags
   - Provides engagement tips

3. **Approval Workflow**:
   - Post stays in Pending_Approval until reviewed
   - Move to Approved/ to schedule posting
   - Move to Rejected/ if changes needed

## Post Format

```markdown
---
type: linkedin_post
topic: [Topic]
tone: [professional|casual]
cta: [true|false]
created: [timestamp]
status: pending_approval
target_audience: [audience]
---

## LinkedIn Post

[Post content - 150-300 words]

## Hashtags
#hashtag1 #hashtag2 #hashtag3

## Call-to-Action
[CTA text if enabled]

## Engagement Tips
- Best posting time: [time]
- Expected reach: [estimate]
- Suggested follow-up: [action]

## Metrics
- Target impressions: [number]
- Target engagement rate: [percentage]
```

## Topics Supported

- AI/Automation benefits
- Silver Tier features
- Task automation ROI
- Workflow optimization
- Team productivity
- Digital transformation
- Custom topics

## Example

```
/social-poster "AI automation benefits" --tone=professional --cta=true
```

Creates post in Pending_Approval/:
- Engaging headline
- 3-4 key benefits
- Real-world example
- LinkedIn CTA button
- Relevant hashtags

## Output
- Draft post in Pending_Approval/
- Metadata for tracking
- Suggested hashtags
- Engagement predictions

## Workflow

1. Generate post with /social-poster
2. Review in Pending_Approval/
3. Move to Approved/ when ready
4. Schedule or publish
5. Track metrics in Done/

## Integration
Works with:
- task_processor.py for content generation
- dashboard_updater.py for tracking
- Pending_Approval workflow for approvals

## Best Practices

- Keep posts authentic and value-focused
- Include specific examples or data
- Use 3-5 relevant hashtags
- Add clear CTA for engagement
- Post during peak hours (9-11 AM, 5-6 PM)
- Engage with comments within 1 hour
