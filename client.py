import socket
import logging

from threading import Thread

from message_receiver import MessageReceiver, Message

logger = logging.getLogger(__name__)

class Client:
    def __init__(self, client_ip: str, server_ip: str, process, port=None):
        logger.info("Client initialized.")
        self.process = process
        self.receiver = MessageReceiver(client_ip, port)

        self.server_ip = server_ip
        self.channel_port = port
        Thread(name="Client Listening Thread", 
        target=self.__process_messages, daemon=True).start()

    def __process_messages(self):
        logger.info("Starting to process messages.")
        for received_message in self.receiver:
            logger.info("Message received.")

        if received_message.sender == self.server_ip or received_message.sender == 'local':
            self.process(received_message.body)

    def connect(self, username: str):
        logger.info("Trying to connect to the server.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_ip, self.channel_port))
            sock.send("/regi {}".format(username).encode())

    def send(self, message: str):
        logger.info("Sending a message.")
        logger.debug("Message: " + message)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_ip, self.channel_port))

            sock.send(message.encode())
            logger.debug("Message successfully sent.")