import json
import boto3

sqs_client = boto3.client('sqs')
SQS_URL="https://sqs.us-east-1.amazonaws.com/568257730157/cola-boletines.fifo"


def read_messages_from_sqs():
    response = sqs_client.receive_message(
        QueueUrl=SQS_URL,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=20
    )
    messages = response.get('Messages', [])
    return messages


def parse_message_body(message_to_parse):
    message_body = json.loads(message_to_parse.get('Body', '{}'))
    return message_body


def delete_message_from_sqs(receipt_handle):
    sqs_client.delete_message(
        QueueUrl=SQS_URL,
        ReceiptHandle=receipt_handle
    )
