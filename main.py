import services.database.db as db
import services.aws.sns_services as sns_services
import services.aws.sqs_services as sqs_services

def main():
    # Crear la tabla en la base de datos
    db.create_table()

    # Bucle infinito de escucha de mensajes en la cola SQS
    while True:
        message_list = sqs_services.read_messages_from_sqs()
        for message in message_list:
            if message:
                message_body = sqs_services.parse_message_body(message)
                # Extraemos los campos necesarios del mensaje para mandarlos como parametros a la función de inserción en la base de datos
                db.insert_boletin(
                    message_body.get('boletin_id'),
                    message_body.get('message'),
                    message_body.get('email'),
                    message_body.get('link_s3'),
                )
                sns_services.publish_message_to_sns(message_body.get('boletin_id'), message_body.get('email'))
                sqs_services.delete_message_from_sqs(message.get('ReceiptHandle'))

if __name__ == "__main__":
    main()