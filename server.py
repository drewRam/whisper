import socket
import re
import logging

from queue import Queue
from threading import Thread

from user_registry import UserRegistry
from message_receiver import MessageReceiver, Message

COMMAND_FLAG_CHAR = '/'

logger = logging.getLogger(__name__)

class Server:
    def __init__(self, port, ip, client_process):
        self.channel_port = port
        self.ip = ip

        self.registry = UserRegistry()

        self.client_process = client_process
        self.receiver = MessageReceiver(self.ip, self.channel_port)
        logger.info("Server initialized.")

    def start_processing(self):
        logger.info("Server processing started.")
        Thread(name='Server Processing Thread', target=self.__process_requests,
        daemon=True).start()

    def __process_requests(self):
        for received_message in self.receiver:
            if self.registry.ip_known(received_message.sender):
                logger.info("Message received from registered client.")
                if received_message.body.startswith(COMMAND_FLAG_CHAR):
                    logger.debug("Message was a command.")
                    self.parse(received_message.body)
                else:
                    logger.debug("Message was generic.")
                    self.send_to_all(received_message)
            else:
                logger.info("Message received from an unregistered client.")
                self.attempt_to_register(received_message)

    def parse(self, message: Message):
        pass

    def register_hosting_client(self, username: str):
        if self.validate_name(username):
            self.registry.register(username, 'local')

    def attempt_to_register(self, message: Message):
        logger.info("Attempting to register client.")

        successful_parse = re.match(r'\/regi (.{1,30})', message.body)

        if successful_parse and self.validate_name(successful_parse.group(1)):
            logger.info("Client successfully registered.")
            self.registry.register(successful_parse.group(1), message.sender)
        else:
            logger.info("Client not registered") # Ignore the message

    def validate_name(self, username: str) -> bool:
        return not self.registry.name_taken(username)


    def send(self, message_body: str, target: str):
        if target == 'local':
            self.client_process(message_body)
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.settimeout(1)
                    sock.connect((target, self.channel_port))
                    sock.send(message_body.encode())
                except socket.timeout:
                    self.registry.delete_ip(target)

    def send_to_all(self, message: Message):
        to_send = self.registry.get_user(message.sender) + ": " + message.body

        for ip in self.registry.ip():
            self.send(to_send, ip)

    def send_as_hosting_user(self, message_body: str):
        self.receiver.receive(Message(message_body, 'local'))