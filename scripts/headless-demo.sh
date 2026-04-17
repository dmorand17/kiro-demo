#!/usr/bin/env bash
# headless-demo.sh — Local examples of Kiro CLI headless mode
#
# Prerequisites:
#   - kiro-cli installed (see https://kiro.dev/docs/cli/)
#   - KIRO_API_KEY set in your environment (Kiro Pro/Pro+/Power required)
#
# Usage:
#   export KIRO_API_KEY="your-api-key"
#   ./scripts/headless-demo.sh [example]
#
# Examples:
#   ./scripts/headless-demo.sh review      # Review code changes
#   ./scripts/headless-demo.sh tests       # Generate unit tests
#   ./scripts/headless-demo.sh pricing     # Generate pricing doc
#   ./scripts/headless-demo.sh diagnose    # Diagnose a build failure

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# --- Guard ---
if [[ -z "${KIRO_API_KEY:-}" ]]; then
  echo "Error: KIRO_API_KEY is not set."
  echo "  export KIRO_API_KEY='your-api-key'"
  echo "  See https://kiro.dev/docs/cli/headless/ for authentication details."
  exit 1
fi

if ! command -v kiro-cli &>/dev/null; then
  echo "Error: kiro-cli is not installed."
  echo "  See https://kiro.dev/docs/cli/ for installation instructions."
  exit 1
fi

# --- Examples ---

example_review() {
  echo "==> Running headless code review of recent changes..."
  local diff
  diff=$(git -C "${REPO_ROOT}" diff HEAD~1..HEAD 2>/dev/null || git -C "${REPO_ROOT}" diff --cached)

  if [[ -z "${diff}" ]]; then
    echo "No changes found. Modify a file and try again."
    exit 0
  fi

  kiro-cli chat --no-interactive \
    --trust-tools=read,grep \
    "Review the following code changes for this AWS Lambda project.

Diff:
${diff}

Check for:
1. Logic errors or edge cases
2. AWS Lambda best practices (error handling, logging, timeouts)
3. Security issues (input validation, secrets exposure)
4. Python code quality (PEP 8, proper exception types)

Be concise and reference specific lines."
}

example_tests() {
  echo "==> Generating unit tests for the calculator Lambda..."

  kiro-cli chat --no-interactive \
    --trust-all-tools \
    "Read the Lambda function at lambda/calculator/lambda_function.py.
Generate a comprehensive pytest test suite and save it to lambda/calculator/test_lambda_function.py.

Cover:
- All supported operations (add, subtract, multiply, divide)
- Input validation (missing fields, wrong types, empty body)
- Edge cases (division by zero, very large numbers)
- Both success responses (200) and error responses (400, 500)

Use pytest fixtures and parametrize where appropriate."
}

example_pricing() {
  echo "==> Generating pricing documentation using aws-architect agent..."

  kiro-cli --agent aws-architect \
    --no-interactive \
    --trust-tools=read,grep,write \
    "Analyze the Lambda infrastructure in this project and generate a PRICING.md file.
Include estimated monthly costs for:
- Lambda invocations and compute time (assume 1M requests/month at 256MB/500ms)
- CloudWatch Logs storage and metrics
- API Gateway requests (if applicable)
- Free tier deductions

Format as a markdown table with dev and prod environment columns."
}

example_diagnose() {
  echo "==> Diagnosing a simulated build failure..."

  # Simulate a test failure log
  local fake_log
  fake_log=$(cat <<'EOF'
FAILED lambda/calculator/test_lambda_function.py::test_divide_by_zero - AssertionError: assert 500 == 400
  Expected HTTP 400 for division by zero, got 500
  Full response: {"statusCode": 500, "body": "{\"error\": \"Internal server error\"}"}

1 failed, 8 passed in 0.42s
EOF
)

  kiro-cli chat --no-interactive \
    --trust-tools=read,grep \
    "A test is failing in this AWS Lambda project. Diagnose the issue and suggest a fix.

Test output:
${fake_log}

Please:
1. Identify the root cause
2. Show the specific code change needed to fix it
3. Explain why the fix is correct"
}

# --- Dispatch ---
EXAMPLE="${1:-}"

case "${EXAMPLE}" in
  review)   example_review ;;
  tests)    example_tests ;;
  pricing)  example_pricing ;;
  diagnose) example_diagnose ;;
  *)
    echo "Kiro CLI Headless Mode — Local Demo"
    echo ""
    echo "Usage: $0 [example]"
    echo ""
    echo "Available examples:"
    echo "  review    Review recent git changes for issues"
    echo "  tests     Generate unit tests for the calculator Lambda"
    echo "  pricing   Generate PRICING.md using the aws-architect agent"
    echo "  diagnose  Diagnose a simulated build failure"
    echo ""
    echo "Required: KIRO_API_KEY environment variable (Kiro Pro/Pro+/Power)"
    echo "Docs: https://kiro.dev/docs/cli/headless/"
    ;;
esac
