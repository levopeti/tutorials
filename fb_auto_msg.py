import fbchat
from getpass import getpass
import time
from fbchat import log, Client
from fbchat.models import Message, ThreadType

import re
import random


class EchoBot(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, **kwargs):
        text_message = message_object.text

        p = re.compile(r'[\w,\s,.]*boldog[\w,\s,.]*', re.IGNORECASE)

        match = p.findall(text_message)
        # log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        # two answers are "No baba!" and "Yes Baba!"
        msg = "Köszönöm :P" if random.random() > 0.5 else "Köszönöm szépen :P"
        thx_messege = Message(text=msg)

        time.sleep(1)

        # If you're not the author, echo
        if author_id != self.uid and match and thread_type != ThreadType.GROUP:
            self.markAsDelivered(thread_id, message_object.uid)
            self.markAsRead(thread_id)
            self.send(thx_messege, thread_id=thread_id, thread_type=thread_type)

        time.sleep(1)


client = EchoBot("beracom@freemail.hu", getpass())
client.listen()

