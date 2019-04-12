import fbchat
from getpass import getpass
import time
from fbchat import log, Client
from fbchat.models import Message, ThreadType

import re
import random

# Subclass fbchat.Client and override required methods


class EchoBot(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        text_message = message_object.text
        # print(type(text_message))

        p = re.compile(r'[\w,\s,.]*baba[\w,\s,.]*', re.IGNORECASE)

        match = p.findall(text_message)
        print(match)
        # log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        msg = "No baba!" if random.random() > 0.5 else "Yes baba!"
        thx_messege = Message(text=msg)
        # If you're not the author, echo
        if author_id != self.uid and match and thread_type != ThreadType.GROUP:
            self.send(thx_messege, thread_id=thread_id, thread_type=thread_type)


client = EchoBot("beracom@freemail.hu", getpass())
client.listen()
"""
# username = "beracom@freemail.hu"   #str(input("Username: "))
# client = fbchat.Client(username, getpass())
# no_of_friends = 1 #int(input("Number of friends: "))
#
# name = "pan" #str(input("Name: "))
# friends = client.searchForUsers(name)  # return a list of names
# user = friends[0]
# print('user ID: {}'.format(user.uid))
# print("user's name: {}".format(user.name))
# print("user's photo: {}".format(user.photo))
# print("Is user client's friend: {}".format(user.is_friend))
#
#
# # Gets the last 10 messages sent to the thread
# messages = client.fetchThreadMessages(thread_id=100000932560681, limit=10)
# # Since the message come in reversed order, reverse them
# messages.reverse()
#
# # Prints the content of all the messages
# for message in messages:
#     print(message.text)
#
# # If we have a thread id, we can use `fetchThreadInfo` to fetch a `Thread` object
# thread = client.fetchThreadInfo('100000932560681')['100000932560681']
# print("thread's name: {}".format(thread.name))
# print("thread's type: {}".format(thread.type))
#
#
# # `searchForThreads` searches works like `searchForUsers`, but gives us a list of threads instead
# thread = client.searchForThreads('Bold')[0]
# print("thread's name: {}".format(thread.name))
# print("thread's type: {}".format(thread.type))
#
# thread = client.searchForThreads('pan')[0]
# messages = client.fetchThreadMessages(thread_id=thread.uid, limit=10)
# messages.reverse()
#
# # Prints the content of all the messages
# for message in messages:
#     print(str(message) == 'Nem')
#     print(message.text)


# msg = fetchThreadMessages(thread_id=friend.uid, limit=20, before=None)
# info = fetchUserInfo(friend.uid)
# print(msg)

#
# for i in range(no_of_friends):
#     name = "Jezeri Andrs" #str(input("Name: "))
#     friends = client.searchForUsers(name)  # return a list of names
#     friend = friends[0]
#     msg = fbchat.models.Message(text=str(input("Message: ")))
#     msg2 = fbchat.models.Message(text=str(input("Message: ")))
#     for _ in range(24):
#         sent = client.send(msg, friend.uid)
#         sent2 = client.send(msg2, friend.uid)
#         if sent and sent2:
#             print("Messages sent successfully!")
#         time.sleep(600)
"""