import boto3
import dotenv
import os

dotenv.load_dotenv()

# URL del endpoint del mostrador
MOSTRADOR_URL = os.getenv('MOSTRADOR_URL')

# ARN del tema SNS
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

sns_client = boto3.client('sns')


def publish_message_to_sns(boletin_id, email):
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=f"Se ha generado un nuevo boletín. Lo puedes revisar en el siguiente enlace: {MOSTRADOR_URL}/boletines/{boletin_id}?correoElectronico={email}"
    )
    return "Message published to SNS topic successfully."
