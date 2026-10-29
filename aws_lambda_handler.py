"""
AWS Learner Lab — IoT Dash Button Lambda Handler
------------------------------------------------
Deploy this function to AWS Lambda in your AWS Academy Learner Lab.

Instructions for AWS Learner Lab:
1. Open AWS Management Console from AWS Learner Lab.
2. Go to AWS Lambda -> Create function.
3. Settings:
   - Function name: IoTButtonHandler
   - Runtime: Python 3.12 (or 3.11)
   - Architecture: x86_64
   - Execution role: "Use an existing role" -> Select "LabRole" (mandatory for AWS Learner Lab)
4. Enable Function URL:
   - Configuration tab -> Function URL -> Create function URL
   - Auth type: NONE
   - Configure cross-origin resource sharing (CORS): Check "Allow origin (*)", Allow headers (*), Allow methods (POST, GET, OPTIONS)
5. Copy the Function URL into your IoT Dash Button Dashboard!
"""

import json
import time
import os

# Optional AWS services available in Learner Lab with LabRole
try:
    import boto3
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = os.environ.get('TABLE_NAME', 'IoTButtonEvents')
    events_table = dynamodb.Table(table_name)
    has_dynamodb = True
except Exception:
    has_dynamodb = False


def lambda_handler(event, context):
    print("=" * 60)
    print(" [AWS LEARNER LAB] IoT Dash Button Event Triggered!")
    print(f" Request ID: {context.aws_request_id}")
    print(f" Remaining Time (ms): {context.get_remaining_time_in_millis()}")
    
    # Handle CORS preflight (OPTIONS)
    http_method = event.get('requestContext', {}).get('http', {}).get('method') or event.get('httpMethod', '')
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-Amz-Date, Authorization, X-Api-Key'
            },
            'body': ''
        }
    
    # Parse incoming JSON body
    body_data = {}
    raw_body = event.get('body')
    if raw_body:
        try:
            if event.get('isBase64Encoded', False):
                import base64
                raw_body = base64.b64decode(raw_body).decode('utf-8')
            body_data = json.loads(raw_body)
        except Exception as e:
            print(f"Error parsing JSON body: {e}")
            body_data = {"raw": raw_body}

    pin = body_data.get('pin', 'D2')
    gpio = body_data.get('gpio', 4)
    device = body_data.get('device', 'ESP8266-NodeMCU')
    event_id = body_data.get('event_id', f"evt_aws_{int(time.time())}")
    message = body_data.get('message', 'Physical IoT button push triggered')
    timestamp = body_data.get('timestamp', int(time.time()))

    print(f" -> Device: {device} | Pin: {pin} (GPIO {gpio})")
    print(f" -> Event ID: {event_id}")
    print(f" -> Message: {message}")

    # Optional DynamoDB persistence (if table exists)
    dynamo_status = "skipped_or_table_not_found"
    if has_dynamodb:
        try:
            events_table.put_item(
                Item={
                    'event_id': event_id,
                    'timestamp': timestamp,
                    'device': device,
                    'pin': pin,
                    'gpio': gpio,
                    'message': message,
                    'aws_request_id': context.aws_request_id,
                    'processed_at': time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())
                }
            )
            dynamo_status = "saved_to_dynamodb"
            print(f" -> Successfully recorded event {event_id} to DynamoDB table '{table_name}'")
        except Exception as err:
            dynamo_status = f"not_persisted ({err})"
            print(f" -> DynamoDB write notice: {err} (Continuing normally)")

    response_payload = {
        "status": "success",
        "cloud": "AWS Learner Lab",
        "region": "us-east-1",
        "environment": "AWS Academy",
        "aws_request_id": context.aws_request_id,
        "device": device,
        "pin": pin,
        "event_id": event_id,
        "action": "IoT_BUTTON_PROCESSED",
        "dynamodb_status": dynamo_status,
        "server_timestamp": int(time.time()),
        "message": f"Processed button click on {pin} successfully in AWS Lambda!"
    }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-Amz-Date, Authorization, X-Api-Key'
        },
        'body': json.dumps(response_payload)
    }
