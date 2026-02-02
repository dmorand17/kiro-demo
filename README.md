# Kiro Capabilities Demo

This document demonstrates key Kiro features using a simple AWS Lambda infrastructure project.

## Prerequisites

- AWS credentials configured
- Terraform installed
- Python 3.13+ installed
- uv package manager installed

## Demo Scenarios

### 1. Git Commit Messages with Best Practices

Kiro automatically follows conventional commit format based on steering rules.

**Try it:**

```
Make a change to lambda_function.py and ask Kiro to commit it
```

**Example prompt:**

> "Add error handling to the Lambda function and commit the changes"

**Expected behavior:**

- Kiro modifies the code
- Creates a commit with proper format: `feat(lambda): add error handling for invalid inputs`
- Follows imperative mood and conventional commit types
- Show the diff view

---

### 2. Generate Infrastructure Using Steering Documents

Kiro uses steering documents to understand project conventions and generate compliant infrastructure.

**Try it:**

```
Ask Kiro to create new infrastructure following project standards
```

**Example prompt:**

> "Create infrascture for deploying this project on AWS"

**Expected behavior:**

- Creates `infra/` directory with `main.tf`, `variables.tf`, `outputs.tf`
- Follows naming convention: `{project}-{environment}-{resource-type}`
- Includes required tags: `project` and `environment`
- Sets up CloudWatch logs with 7-day retention
- Configures Lambda with Python 3.13 runtime
- Creates CloudWatch alarms for errors and duration

---

### 3. Update Infrastructure Based on Steering Changes

Demonstrate how Kiro adapts when steering documents are updated.

**Try it:**

```
1. Update structure.md to add a new required tag
2. Ask Kiro to update existing infrastructure
```

**Example steps:**

1. Edit `.kiro/steering/structure.md` and add `owner` to required tags:

```markdown
## Required Resource Tags

All AWS resources MUST include the following tags:

- `project`: Project name (from `var.project`)
- `environment`: Environment name (from `var.environment`)
- `owner`: Resource owner (from `var.owner`)
```

2. **Example prompt:**
   > "Update all Terraform files to include the new owner tag requirement"

**Expected behavior:**

- Kiro reads the updated steering document
- Adds `owner` variable to `variables.tf`
- Updates all resource tags to include `owner = var.owner`
- Updates provider default tags

---

### 4. Generate Architecture Diagrams

Kiro can automatically generate diagrams when infrastructure changes.

**Try it:**

```
Ask Kiro to create a diagram of the current infrastructure
```

**Example prompt:**

> "Generate an architecture diagram showing the Lambda function, CloudWatch, and IAM resources"

**Expected behavior:**

- Uses the diagrams MCP server
- Creates a visual representation of AWS resources
- Shows relationships between Lambda, CloudWatch Logs, IAM roles, and Function URL
- Saves diagram as PNG in `generated-diagrams/` directory

**Advanced:**
Set up a hook to auto-generate diagrams on infrastructure changes:

**Example prompt:**

> "Create a hook that generates an architecture diagram whenever Terraform files are modified"

---

### 5. Generate Pricing Documentation (via Kiro CLI)

Kiro can analyze infrastructure and provide cost estimates.

**Try it:**

```
Ask Kiro to analyze pricing for the deployed resources
```

**Example prompt:**

> "Analyze the pricing for this Lambda infrastructure and create a PRICING.md file"

**Expected behavior:**

- Uses AWS Pricing MCP server to fetch current pricing
- Analyzes Lambda invocations, duration, and memory
- Includes CloudWatch Logs pricing
- Calculates estimated monthly costs
- Documents pricing assumptions and exclusions
- Creates detailed PRICING.md with:
  - Cost breakdown by service
  - Usage assumptions
  - Free tier information
  - Cost optimization recommendations

---

## Complete Workflow Demo

Here's a complete workflow that combines multiple capabilities:

### Scenario: Add a New Feature with Full Documentation

**Prompt:**

> "Add a new Lambda function that processes S3 events. Include CloudWatch monitoring, generate an architecture diagram, create pricing documentation, and commit everything with proper git messages."

**Expected Kiro workflow:**

1. **Generate Infrastructure**
   - Creates Terraform files following structure.md conventions
   - Adds S3 bucket, Lambda function, IAM roles, CloudWatch resources
   - Includes all required tags

2. **Create Lambda Code**
   - Generates Python 3.13 Lambda handler
   - Follows project structure conventions
   - Includes error handling and logging

3. **Generate Architecture Diagram**
   - Creates visual diagram showing S3 → Lambda → CloudWatch flow
   - Saves to `generated-diagrams/`

4. **Analyze Pricing**
   - Fetches AWS pricing for Lambda, S3, CloudWatch
   - Calculates estimated costs
   - Creates PRICING.md with detailed breakdown

5. **Commit Changes**
   - Stages all new files
   - Creates commit: `feat(infra): add S3 event processing Lambda with monitoring`
   - Follows conventional commit format from git-best-practices.md

---

## Tips for Best Results

1. **Reference steering documents**: Kiro automatically uses them, but you can explicitly reference with `#structure.md`

2. **Use specific prompts**: "Create a Lambda function with CloudWatch alarms" is better than "Create a Lambda"

3. **Iterate incrementally**: Make one change, review, then ask for the next

4. **Leverage hooks**: Automate repetitive tasks like diagram generation or linting

5. **Check pricing early**: Ask for cost analysis before deploying to avoid surprises

---

## Steering Documents in This Project

- **tech.md**: Technology stack, tools, and common commands
- **structure.md**: Project layout, naming conventions, required tags
- **git-best-practices.md**: Commit message format and workflow
- **architecture-diagrams.md**: Diagram generation guidelines (if exists)

These documents guide Kiro's behavior automatically - no need to repeat requirements in every prompt!
