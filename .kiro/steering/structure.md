# Project Structure

## Terraform Project Layout

Each Terraform project follows this structure:

```
infra/
├── main.tf              # Primary infrastructure definitions
├── variables.tf         # Input variables
├── outputs.tf           # Output values
└── .terraform/          # Terraform state and providers (gitignored)
```

## Lambda Function Structure

- **Handler**: `lambda_function.lambda_handler`
- **Runtime**: Python 3.13
- **Environment Variables**: Configured in Terraform
- **Logging**: CloudWatch Logs with 7-day retention
- **Timeout**: 30 seconds
- **Memory**: 128 MB

## Python Application Structure

```
sample-application/
├── app.py              # Flask application entry point
├── pyproject.toml      # Python dependencies and metadata
└── .python-version     # Python version specification
```

## Key Conventions

- Lambda functions use `lambda/` subdirectory for source code
- Static data files (JSON) are packaged with Lambda deployment
- Terraform state is local (not remote backend)
- CloudWatch alarms monitor errors and duration
- Lambda Function URLs provide public HTTP access
- All Infrastructure uses consistent naming: `{project}-{environment}-{resource-type}` format

## Pricing Documentation Structure

When generating PRICING.md files, use the following table format:

### Cost Breakdown Table

| Service         | Component            | Unit Price                  | Usage             | Monthly Cost |
| --------------- | -------------------- | --------------------------- | ----------------- | ------------ |
| AWS Lambda      | Requests             | $0.20 per 1M requests       | 1M requests       | $0.20        |
| AWS Lambda      | Compute (GB-seconds) | $0.0000166667 per GB-second | 50,000 GB-seconds | $0.83        |
| CloudWatch Logs | Ingestion            | $0.50 per GB                | 1 GB              | $0.50        |
| CloudWatch Logs | Storage              | $0.03 per GB                | 1 GB              | $0.03        |

### Required Sections

1. **Overview**: Brief description of the infrastructure being priced
2. **Cost Breakdown**: Table format showing service, component, unit price, usage, and monthly cost
3. **Usage Assumptions**: List all assumptions made for usage calculations
4. **Free Tier**: Document which services have free tier and limits
5. **Total Estimated Cost**: Sum of all service costs
6. **Exclusions**: List what costs are NOT included (data transfer, support plans, etc.)
7. **Cost Optimization Recommendations**: Suggestions to reduce costs

## Required Resource Tags

All AWS resources MUST include the following tags

- `project`: Project name (from `var.project`)
- `environment`: Environment name (from `var.environment`)

Example:

```hcl
tags = {
  project     = var.project
  environment = var.environment
}
```

Best practices:

- Tags should be included in the AWS provider block
- Tags values should be derived from terraform variables

These tags enable:

- Cost tracking and allocation by project and environment
- Resource filtering and organization
- Automated resource management and cleanup
- Compliance and governance reporting
