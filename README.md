# Kiro Capabilities Demo

A sample repo to demonstrate various features of Kiro including:

- **Steering Documents**: Automatic adherence to project conventions and standards
- **Git Best Practices**: Conventional commit messages with proper formatting
- **Infrastructure as Code**: Terraform generation following project structure
- **Architecture Diagrams**: Automatic AWS diagram generation from infrastructure
- **Cost Analysis**: AWS pricing analysis and documentation
- **Hooks**: Automated workflows triggered by file changes
- **MCP Servers**: Integration with Git, AWS Diagrams, Pricing, and Terraform tools
- **Headless Mode**: CI/CD automation with `kiro-cli --no-interactive`

## Prerequisites

- [AWS credentials configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) (via `aws configure` or environment variables)
- [Terraform](https://www.terraform.io/downloads) installed
- [Python 3.13+](https://www.python.org/downloads/) installed
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager installed
- [Kiro CLI](https://kiro.dev/docs/cli/) installed (for headless mode / Scenario 4 & 5)

## Demo Scenarios

### 1. Git Commit Messages with Best Practices

Kiro automatically follows conventional commit format based on steering rules.

**Features Demonstrated:**

- Steering documents (automatic adherence to git-best-practices.md)
- Git Agent Hooks
- Conventional commit message formatting
- Code modification with context awareness

**Example prompts:**

> "Change the lambda function to use the logging module instead of print statements"

> "Add error handling to the Lambda function"

> "Update the Lambda timeout to 60 seconds in Terraform"

**Expected behavior:**

- Kiro modifies the code
- Agent hook creates a commit with proper format: `feat(lambda): add error handling for invalid inputs`
- Follows imperative mood and conventional commit types
- Shows the diff view

---

### 2. Generate Infrastructure Using Steering Documents

Kiro uses steering documents to understand project conventions and generate compliant infrastructure.

**Features Demonstrated:**

- Steering documents (structure.md and tech.md)
- Terraform code generation
- AWS best practices (tagging, naming conventions)
- Infrastructure as Code patterns

**Example prompts:**

> "Create infrastructure for deploying this project on AWS"

> "Generate Terraform files for a Lambda function with API Gateway"

> "Set up infrastructure for this Lambda with DynamoDB table"

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

**Features Demonstrated:**

- Dynamic steering document updates
- Automatic code refactoring based on new conventions
- Multi-file updates with consistency
- Context awareness across project files

**Setup:** First, edit `.kiro/steering/structure.md` and add `owner` to required tags:

```markdown
## Required Resource Tags

All AWS resources MUST include the following tags:

- `project`: Project name (from `var.project`)
- `environment`: Environment name (from `var.environment`)
- `owner`: Resource owner (from `var.owner`)
```

**Example prompts:**

> "Update infrastructure since steering documentation is updated"

> "Refactor the Terraform to comply with the updated tagging standards"

**Expected behavior:**

- Kiro reads the updated steering document
- Adds `owner` variable to `variables.tf`
- Updates all resource tags to include `owner = var.owner`
- Updates provider default tags

---

### 4. Generate Pricing Documentation (via Kiro CLI)

Kiro CLI can analyze infrastructure and provide cost estimates using custom agents.

**Features Demonstrated:**

- AWS Pricing MCP server integration
- Custom agents (aws-architect)
- Cost analysis and estimation
- Structured documentation generation
- Real-time AWS pricing data retrieval

**Example CLI commands:**

```bash
# Analyze pricing for Lambda infrastructure
kiro-cli --agent aws-architect "Analyze the pricing for this infrastructure and create a PRICING.md file"

# Get estimated monthly costs
kiro-cli --agent aws-architect "What are the estimated monthly costs for running this infrastructure in both a development and production environment?"

# Generate detailed cost breakdown
kiro-cli --agent aws-architect "Generate a cost breakdown for the Lambda function with 10 million invocations per month"
```

**Expected behavior:**

- Uses the `aws-architect` custom agent via Kiro CLI
- Leverages AWS Pricing MCP server to fetch current pricing
- Analyzes Lambda invocations, duration, and memory
- Calculates estimated monthly costs
- Documents pricing assumptions and exclusions
- Creates detailed PRICING.md with:
  - Cost breakdown by service
  - Usage assumptions
  - Free tier information
  - Cost optimization recommendations

---

### 5. Headless Mode / CI/CD Automation

Kiro CLI can run without a terminal UI — perfect for automating code reviews, test generation, and build diagnostics inside GitHub Actions or any CI/CD pipeline.

**Features Demonstrated:**

- `--no-interactive` flag for headless operation
- `--trust-tools` for least-privilege tool access
- `KIRO_API_KEY` environment variable for authentication
- Piping context (git diffs, build logs) into prompts
- GitHub Actions integration

**Prerequisites:**

- Kiro Pro, Pro+, or Power subscription
- `KIRO_API_KEY` set as a CI/CD secret (never hardcode in source)
- `kiro-cli` installed (see [Kiro CLI docs](https://kiro.dev/docs/cli/))

**Key flags:**

| Flag | Purpose |
|------|---------|
| `--no-interactive` | Required for headless — runs without a terminal session |
| `--trust-tools=read,grep` | Auto-approve specific tool categories (principle of least privilege) |
| `--trust-all-tools` | Auto-approve all tools (use with caution) |
| `--require-mcp-startup` | Fail fast if MCP servers cannot connect at startup |

**Local demo script:**

```bash
export KIRO_API_KEY="your-api-key"

# Review recent git changes
./scripts/headless-demo.sh review

# Generate unit tests for the calculator Lambda
./scripts/headless-demo.sh tests

# Generate PRICING.md via the aws-architect agent
./scripts/headless-demo.sh pricing

# Diagnose a simulated build failure
./scripts/headless-demo.sh diagnose
```

**GitHub Actions examples** (see `.github/workflows/`):

- **`kiro-pr-review.yml`** — Runs a headless code review on every pull request, checking for correctness, AWS best practices, and security issues. Optionally generates tests for changed Lambda functions.
- **`kiro-build-troubleshoot.yml`** — Triggers when another workflow fails, downloads the build logs, and asks Kiro to diagnose the root cause and suggest a fix.

**Basic headless command pattern:**

```bash
# Read-only analysis (code review, cost estimation)
kiro-cli chat --no-interactive \
  --trust-tools=read,grep \
  "Review the Lambda function at lambda/calculator/lambda_function.py for security issues"

# Analysis + writes (test generation, documentation)
kiro-cli chat --no-interactive \
  --trust-all-tools \
  "Generate pytest tests for the calculator Lambda and save them to lambda/calculator/test_lambda_function.py"

# Pipe context directly into the prompt
git diff HEAD~1 | kiro-cli chat --no-interactive \
  --trust-tools=read,grep \
  "Review this diff for AWS Lambda best practices"
```

**Expected behavior:**

- Kiro runs non-interactively and exits when complete
- Exit code 0 on success, non-zero on error (use in shell conditionals)
- Output goes to stdout — pipe or capture as needed

---

## Complete Workflow Demo

Here's a complete workflow that combines multiple capabilities:

### Scenario: Add a New Feature with Full Documentation

**Features Demonstrated:**

- Multi-step autonomous workflow
- Steering documents (all project conventions)
- Terraform MCP server (infrastructure generation)
- AWS Diagrams MCP server (visualization)
- AWS Pricing MCP server (cost analysis)
- Git MCP server (version control)
- End-to-end project automation

**Prompt:**

> "Add a new Lambda function that processes S3 events. Update the infrastructure, and create pricing documentation. Once finished commit everything with proper git messages."

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

## Best Practices for Steering and Hooks

### Steering Documents

Steering documents are markdown files in `.kiro/steering/` that guide Kiro's behavior automatically. They help maintain consistency across your project without repeating instructions.

**Key principles:**

- **Keep them focused**: Each steering file should cover a specific domain (git, infrastructure, testing, etc.)
- **Use clear conventions**: Define naming patterns, required fields, and standards explicitly
- **Include examples**: Show concrete examples of what you want, not just descriptions
- **Set inclusion rules**: Use frontmatter to control when steering applies (always, fileMatch, manual)
- **Reference external files**: Use `#[[file:path]]` syntax to include specs, schemas, or documentation

**Common steering patterns:**

- Project structure and naming conventions
- Required resource tags and metadata
- Git commit message formats
- Code style and formatting rules
- Testing requirements and patterns
- Documentation standards

### Hooks

Hooks automate agent actions based on IDE events, reducing manual work and ensuring consistency.

**Effective hook patterns:**

- **File watchers**: Auto-format, lint, or validate on save
- **Diagram generation**: Update architecture diagrams when infrastructure changes
- **Documentation sync**: Regenerate docs when code changes
- **Commit helpers**: Suggest commit messages based on changes
- **Test runners**: Run relevant tests on file changes

**Hook best practices:**

- Keep hook actions focused and fast
- Use `askAgent` for complex tasks requiring context
- Use `runCommand` for simple, deterministic operations
- Test hooks thoroughly before enabling
- Document what each hook does and why

### Learn More

For comprehensive best practices, examples, and advanced patterns, see the [Kiro Best Practices Repository](https://github.com/awsdataarchitect/kiro-best-practices).

---

## Steering Documents in This Project

- [**tech.md**](.kiro/steering/tech.md): Technology stack, tools, and common commands
- [**structure.md**](.kiro/steering/structure.md): Project layout, naming conventions, required tags
- [**git-best-practices.md**](.kiro/steering/git-best-practices.md): Commit message format and workflow
- [**architecture-diagrams.md**](.kiro/steering/architecture-diagrams.md): Diagram generation guidelines

These documents guide Kiro's behavior automatically - no need to repeat requirements in every prompt!
