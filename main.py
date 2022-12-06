
import cv2
import glob
import time
import numpy
from send import send_mail
import glob
import os
from threading import Thread


video=cv2.VideoCapture(0)
time.sleep(1)
first_frame=None
list_status=[]
count=1

def clean_fol():
    imgs=glob.glob('images/*.png')
    for img in imgs:
        os.remove(img)
while True:
    status=0
    count = 1
    check,frame=video.read()
# print(check)
# print(frame)
    grey_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#makes to greyscale image
    blurr=cv2.GaussianBlur(grey_frame,(21,21),1)  # add gausian blur remove noise
    # cv2.imshow('my video',blurr) # show camera with frame
    if first_frame is None:# to get first frame and save it
        first_frame=blurr
    delta=cv2.absdiff(first_frame,blurr) # shows diff between first and second so when object enters it shows
    # print(delta)
    threshold=cv2.threshold(delta,145,255,cv2.THRESH_BINARY)[1] #change bg to black and object to white
    # cv2.imshow('my video', threshold)
    new_tresh=cv2.dilate(threshold,None,iterations=2)
    # cv2.imshow('my video', new_tresh)
    contors,check=cv2.findContours(new_tresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  # SHOW rectangle around abject
    for contorm in contors:
        # status=0
        if cv2.contourArea(contorm)<4000:  #skips other object with less area
            continue
        x,y,h,w=cv2.boundingRect(contorm)  # to get x y and height width of rectangle over contor
        rect=cv2.rectangle(frame, (x,y), (x+w,y+h) ,(0,255,0))  #draws triangle using the dimensions
        if rect.any():# to send image only when object is there
             status=1
             count = count + 1
             cv2.imwrite(f'images/{count}.png',frame)   #creating images for frames

             new_im=glob.glob('images/*.png')
             index=int(len(new_im)/2)
             new_ima=new_im[index]
             # send_mail()
    list_status.append(status)
    list_status=list_status[-2:]


    print(list_status)
    if list_status[0]==1 and list_status[1]==0:
        # send_mail(new_ima)
        email_thread=Thread(target=send_mail(), args=(new_ima,)) #using threading for 2 processes
        email_thread.daemon=True
        clean_thread=Thread(target=clean_fol())
        clean_thread.daemon=True
        # clean_fol()
        email_thread.start()
    cv2.imshow('my video', frame)




    key=cv2.waitKey(1)    # to quit cam when q is pressed
    if key==ord('q'):
        break
video.release()
clean_thread.start()