import json
from typing import Any, Dict


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Simple calculator API that performs basic arithmetic operations.

    Supported operations: add, subtract, multiply, divide

    Request body format:
    {
        "operation": "add|subtract|multiply|divide",
        "a": number,
        "b": number
    }

    Args:
        event: Lambda event object containing HTTP request data
        context: Lambda context object with runtime information

    Returns:
        dict: API Gateway response with status code, headers, and body
    """
    try:
        print(f"Processing calculator request - Request ID: {context.aws_request_id}")

        # Parse request body
        body = json.loads(event.get("body", "{}"))

        # Validate required fields
        if "operation" not in body or "a" not in body or "b" not in body:
            print("Missing required parameters")
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(
                    {
                        "error": "Missing required parameters",
                        "message": "Please provide 'operation', 'a', and 'b'",
                    }
                ),
            }

        operation = body["operation"].lower()

        # Extract and validate numbers
        try:
            num_a = float(body["a"])
            num_b = float(body["b"])
        except (ValueError, TypeError) as e:
            print(f"Invalid number format: {str(e)}")
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(
                    {
                        "error": "Invalid input",
                        "message": "Both 'a' and 'b' must be valid numbers",
                    }
                ),
            }

        # Perform calculation
        result = None
        if operation == "add":
            result = num_a + num_b
        elif operation == "subtract":
            result = num_a - num_b
        elif operation == "multiply":
            result = num_a * num_b
        elif operation == "divide":
            if num_b == 0:
                print("Division by zero attempted")
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(
                        {
                            "error": "Invalid operation",
                            "message": "Cannot divide by zero",
                        }
                    ),
                }
            result = num_a / num_b
        else:
            print(f"Unknown operation: {operation}")
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(
                    {
                        "error": "Invalid operation",
                        "message": "Operation must be one of: add, subtract, multiply, divide",
                    }
                ),
            }

        print(f"Calculation successful: {num_a} {operation} {num_b} = {result}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "operation": operation,
                    "a": num_a,
                    "b": num_b,
                    "result": result,
                }
            ),
        }

    except json.JSONDecodeError as e:
        print(f"Invalid JSON in request body: {str(e)}")
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Invalid JSON format"}),
        }

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
