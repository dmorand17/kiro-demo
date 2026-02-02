# Technology Stack

## Infrastructure as Code

- **Terraform** >= 1.0
- **AWS Provider** ~> 6.0

## Runtime Environments

- **Python 3.13** (Lambda functions)
- **Python 3.11+** (Flask application)
- **Flask** >= 3.0.0 with Gunicorn for production

## AWS Services

- Lambda (Python 3.13 runtime)
- CloudWatch (logs, alarms, monitoring)
- IAM (roles, policies)

## Development Tools

- **uv** (Python package manager and project management)
- **black** (Python formatting)
- **ruff** (Python linting)
- **boto3** (AWS SDK)

## Common Commands

### Terraform Workflow

```bash
# Initialize providers
terraform init

# Preview changes
terraform plan

# Deploy infrastructure
terraform apply

# Destroy resources
terraform destroy
```

### Python Application

```bash
# Install dependencies with uv
uv sync

# Run Flask app locally
uv run python app.py

```

### AWS CLI

```bash
# Configure credentials
aws configure

# Test Lambda function
aws lambda invoke --function-name <name> output.json
```

## Configuration

- AWS credentials via AWS CLI or environment variables
- Terraform variables in `variables.tf`
- Terraform outputs in `outputs.tf`
- Lambda environment variables in Terraform configuration
- Python dependencies in `pyproject.toml` (managed by uv)
