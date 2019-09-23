import pika
import json
import logging
import logging.config
import time
from datetime import datetime

from postgre_models.main import DBSession
from functions import touch, test_runner_for_python, delete_folder, copy

TEST_RUN_LOG_ID = "Test_Run"
def process_test_run_request(ch, method, properties, body):
    """
    rabbitmq consumer callback function.
    """
    logger.info('{} Inside: process_test_run_request'.format(TEST_RUN_LOG_ID))
    logger.debug('{} process_test_run_request: parameters - '
                 '{}, {}, {}, {}'.format(TEST_RUN_LOG_ID, ch, method, properties, body))
    print("Message Received {}".format(body))
    print("started processing message.")
    try:
        msg_dict = json.loads(body.decode())
    except Exception as e:
        logger.debug("{} invalid message. ".format(TEST_RUN_LOG_ID))
        logger.exception("{} {}".format(TEST_RUN_LOG_ID, e))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Done processing message.")
        return True
    try:

        # Start Test execution.
        #touch("/src/sheetal_123")        
        #time.sleep(60)
        start_date = datetime.utcnow()

        dest_path = "/src/test_scripts"
        src_path = "/mnt/test_run_"+msg_dict['id']
        delete_folder(dest_path)
        copy(src_path, dest_path)

        result = test_runner_for_python(dest_path)
        end_date = datetime.utcnow()
        update_data = {'started_at': start_date, 'finished_at': end_date, 'environment': 'test_env_1', "status": "Complete", "logs": result}
        db = DBSession()
        #db.create_entry()
        db.update_new_query(3, update_data)
        db.session_close()
        # Removing the message from queue.
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.info('{} Exit: process_test_run_request {}'.format(TEST_RUN_LOG_ID, e))
        # Checking for custom attribute.
        #if hasattr(e, 'message'):
        #    err_msg = "{}".format(e.message)
        #else:
        #    err_msg = "{}".format(e)

        # Printing stacktrace.
        #logger.critical("{} Exception occured in rabbitmq consumer callback."
        #                .format(TEST_RUN_LOG_ID))
        #logger.exception("{} {}".format(TEST_RUN_LOG_ID, err_msg))

        # Logging more information about exception.
        #logger.critical("{} Exception {} occured ".format(TEST_RUN_LOG_ID, type(e).__name__))
        #if type(e).__name__ == "APIException":
        #    logger.critical("{} APIException received message {}"
        #                    .format(TEST_RUN_LOG_ID, e.received_message.text))
        #    logger.critical("{} APIException custom message {}"
        #                    .format(TEST_RUN_LOG_ID, e.custom_message))

        # Removing message from queue.
        ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info('{} Exit: process_test_run_request'.format(TEST_RUN_LOG_ID))
    print("Done processing of test run message.")
    return True



def main():
    """
    Rabbitmq consumer.
    """
    try:
        # Configuration parameters.
        log_level = "INFO" #get_config(LOG_KEY, "level")
        log_file = "/var/log/test_run.log" #get_config(LOG_KEY, "filename")
        log_file_max_bytes = 5242880 #get_config(LOG_KEY, "maxbytes")
        log_file_count = 2 #get_config(LOG_KEY, "backupcount")

        # If invalid log level given then bydefault Default will be taken.
        numeric_level = getattr(logging, log_level.upper(), 10)

        global logger
        logging.Formatter.converter = time.gmtime
        logger = logging.getLogger(__name__)
        LOG_LEVEL = numeric_level
        logging.basicConfig(filename=log_file, level=logging.INFO)

        # Rabbitmq details.
        #broker = get_config(RABBITMQ_KEY, "RABBIT_MQ_IP")
        #user = get_config(RABBITMQ_KEY, "RABBIT_MQ_USERNAME")
        #password = get_config(RABBITMQ_KEY, "RABBIT_MQ_PASSWORD")
        broker = "192.168.0.116"
        user = "sid"
        password = "test"
        TEST_RUN_QUEUE_NAME = "test_run.jobs.queue"
        credentials = pika.PlainCredentials(user, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker,
                                                                       credentials=credentials))
        test_run_ch = connection.channel()
        #test_run_ch.queue_declare(queue=TEST_RUN_QUEUE_NAME, durable=True)
        #test_run_ch.basic_qos(prefetch_count=1)
        test_run_ch.basic_consume(process_test_run_request,
                                            queue=TEST_RUN_QUEUE_NAME)

        logger.info(' [*] Waiting for messages.')
        print(' [*] Waiting for messages.')

        # Start the consumer.
        test_run_ch.start_consuming()
    except KeyError as e:
        logging.exception("missing key : {}".format(e))
    except Exception as e:
        logging.exception("exception occured : {}".format(e))
        if "connection" in locals():
            connection.close()


if __name__ == "__main__":
    main()
