from datetime import datetime
import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()

from attendees.models import AccountVO

# Declare a function to update the AccountVO object (ch, method, properties, body)
def update_account(ch, method, properites, body):
    #   content = load the json in body
    content = json.loads(body)
    #   first_name = content["first_name"]
    first_name = content["first_name"]
    #   last_name = content["last_name"]
    last_name = content["last_name"]
    #   email = content["email"]
    email = content["email"]
    #   is_active = content["is_active"]
    is_active = content["is_active"]
    #   updated_string = content["updated"]
    updated_string = content["updated"]
    #   updated = convert updated_string from ISO string to datetime
    updated = datetime.fromisoformat(updated_string)
    #   if is_active:
    if is_active:
        AccountVO.objects.update_or_create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            updated=updated,
        )
    #       Use the update_or_create method of the AccountVO.objects QuerySet
    #           to update or create the AccountVO object
    else:
        AccountVO.objects.get(email=email).delete()
    #   otherwise:
    #       Delete the AccountVO object with the specified email, if it exists


# Based on the reference code at
#   https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive_logs.py
while True:
    try:
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(
            exchange="account_info", exchange_type="fanout"
        )
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange="account_info", queue=queue_name)
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=update_account,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
    # infinite loop
    #   try
    #       create the pika connection parameters
    #       create a blocking connection with the parameters
    #       open a channel
    #       declare a fanout exchange named "account_info"
    #       declare a randomly-named queue
    #       get the queue name of the randomly-named queue
    #       bind the queue to the "account_info" exchange
    #       do a basic_consume for the queue name that calls
    #           function above
    #       tell the channel to start consuming
    #   except AMQPConnectionError
    #       print that it could not connect to RabbitMQ
    #       have it sleep for a couple of seconds
