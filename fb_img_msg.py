from getpass import getpass
import time
import cv2
from fbchat import log, Client
from fbchat.models import ThreadType


class EchoBot(Client):
    global client

    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, **kwargs):
        text_message = message_object.text
        match = text_message == "shot"
        # log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        time.sleep(1)

        if author_id == self.uid and match and thread_type != ThreadType.GROUP:
            print("shot")
            video = cv2.VideoCapture(0)
            check, frame = video.read()
            # cv2.imshow("Capturing", frame)
            cv2.imwrite('/home/biot/Pictures/newfilename.png', frame)
            video.release()

            client.sendLocalImage('/home/biot/Pictures/newfilename.png', thread_id=self.uid)

        time.sleep(1)


client = EchoBot("beracom@freemail.hu", getpass())
client.listen()

