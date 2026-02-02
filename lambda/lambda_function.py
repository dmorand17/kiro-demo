import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Simple Hello World Lambda function with error handling.

    Args:
        event: Lambda event object
        context: Lambda context object

    Returns:
        dict: API Gateway response format
    """
    try:
        logger.info(f"Received event: {json.dumps(event)}")

        # Extract name from query parameters if provided
        name = "World"
        if event.get("queryStringParameters"):
            name = event["queryStringParameters"].get("name", "World")

        response_body = {"message": f"Hello {name}!"}

        logger.info(f"Returning success response: {response_body}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response_body),
        }

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)

        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }
