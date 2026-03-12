# Reasoning Loop Skill

## Description
Creates Plan.md files for tasks and iterates through them using simple loop logic until all tasks are complete.

## Purpose
Automate task planning and execution with iterative refinement. Breaks down complex tasks into manageable steps and tracks progress through Plan.md files.

## Usage

### Basic Invocation
```
/reasoning-loop <task_description>
```

### Parameters
- `task_description`: The main task or goal to plan and execute

## How It Works

1. **Plan Creation**: Generates a Plan.md file with:
   - Task breakdown into steps
   - Success criteria
   - Dependencies
   - Estimated effort

2. **Iteration Loop**:
   - Execute each step sequentially
   - Update Plan.md with progress
   - Check for blockers
   - Adjust plan if needed

3. **Completion Check**:
   - Verify all steps completed
   - Validate success criteria
   - Archive Plan.md to Done/

## Plan.md Format

```markdown
# Task Plan: [Task Name]

## Objective
[Clear goal statement]

## Steps
- [ ] Step 1: Description
- [ ] Step 2: Description
- [ ] Step 3: Description

## Success Criteria
- Criterion 1
- Criterion 2

## Dependencies
- Dependency 1
- Dependency 2

## Progress
- Started: [timestamp]
- Current Step: 1
- Status: In Progress

## Notes
[Any relevant notes]
```

## Example

```
/reasoning-loop "Set up WhatsApp monitoring for urgent messages"
```

Creates Plan.md with steps:
1. Install dependencies
2. Configure session path
3. Test message detection
4. Verify action file creation
5. Deploy to production

## Output
- Plan.md in Plans/ folder
- Execution logs in Logs/
- Completed plan archived to Done/

## Integration
Works with:
- task_processor.py for task execution
- dashboard_updater.py for progress tracking
- health_check.py for validation
