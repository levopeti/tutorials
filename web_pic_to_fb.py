import fbchat
from getpass import getpass
import time
import cv2


username = "beracom@freemail.hu"   #str(input("Username: "))
client = fbchat.Client(username, getpass())
name = "Győri Panni" #str(input("Name: "))
friends = client.searchForUsers(name)  # return a list of names
user = friends[0]

for _ in range(6):
    video = cv2.VideoCapture(0)
    check, frame = video.read()
    cv2.imshow("Capturing", frame)
    cv2.imwrite('/home/biot/Pictures/newfilename.png', frame)
    video.release()

    sent = client.sendLocalImage('/home/biot/Pictures/newfilename.png', thread_id=user.uid)

    if sent:
        print("Messages sent successfully!")
    time.sleep(60 * 30)

