import tensorflow
import numpy as np
import cv2
import random
from game import move_conv, find_winner
import time

np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model("RPS-model.h5")

#  0_Rock  1_Paper  2_Scissors  3_YourTurn

s = ["images/0.png", "images/1.png", "images/2.png", "images/3.jfif"]

# Setting default cam to webcam and necesseary variables
img = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 250, 250, 3), dtype=np.float32)
firsttime = False
exit = False
you = 0
ai = 0
while True:
    font = cv2.FONT_HERSHEY_SIMPLEX
    ret, frame = img.read()
    frame = cv2.flip(frame, 1)

    if not ret:
        continue

    frame = cv2.rectangle(frame, (320, 100), (570, 350), (0, 0, 255), 3)
    frame2 = frame[100:350, 320:570]
    image = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (250, 250))
    pred = model.predict(np.array([image]))
    #image_array = np.asarray(frame2)
    #normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    #data[0] = normalized_image_array
    #pred = model.predict(data)

    winner = "None"

    ai_frame = cv2.imread(s[3])
    move_code = np.argmax(pred[0])

    start = time.time()
    end = time.time()
    check = 0.0
    gate = 1
    window_width = 1200
    window_height = 820
    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Frame', window_width, window_height)
    while(True):

        end = time.time()
        check = end-start
        ret, frame = img.read()

        frame = cv2.flip(frame, 1)
        frame = cv2.rectangle(frame, (320, 100), (570, 350), (0, 0, 255), 3)
        cv2.putText(frame,  "------".format(you), (3, 87),
                    font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame,  "You : {}".format(you), (25, 117),
                    font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame,  "A.I : {}".format(ai), (45, 157),
                    font, 1,(0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame,  "------".format(you), (3, 187),
                    font, 1, (0, 0, 255), 2, cv2.LINE_AA)

        for i in range(112, 192, 50):
            cv2.putText(frame,  "|".format(you), (155, i),
                        font, 1, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.putText(frame,  "|".format(you), (0, i),
                        font, 1, (0, 0, 255), 2, cv2.LINE_AA)

        if not ret:
            continue

        if(firsttime):
            frame = cv2.rectangle(
                frame, (320, 100), (570, 350), (0, 0, 255), 3)
            cv2.imshow('Frame', frame)
            if(check < 3):
                cv2.putText(frame,  "Deliver in {}".format(
                    3-int(check)), (365, 300), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
            elif(check >= 2.5 and gate == 1):
                t = random.choice([0, 1, 2])
                computer_move_name = move_conv(t)
                ai_frame = cv2.imread(s[t])
                cv2.imshow("A.I move", ai_frame)
                gate = 0
            elif(check >= 3):
                frame2 = frame[100:350, 320:570]
                #cv2.imshow("captured image", frame2)
                image = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, (250, 250))
                pred = model.predict(np.array([image]))

                print(pred)
                move_code = np.argmax(pred[0])
                print(move_code)
                user_move_name = move_conv(move_code)
                if(user_move_name == "none"):
                    ai_frame = cv2.imread(s[3])
                if user_move_name != "none":
                    result = find_winner(user_move_name, computer_move_name)
                    if(result == 0):
                        ai = ai+1
                        winner = "A.I"
                    elif(result == 1):
                        you = you+1
                        winner = "Y.O.U"
                    else:
                        winner = "TIE"
                cv2.putText(frame,  "Winner : ", (350, 385),
                            font, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame,  winner, (480, 385), font,
                            1, (0, 255, 0), 2, cv2.LINE_AA)
                print("user :"+user_move_name+"    A.I :" +
                      computer_move_name+"    Winner:"+winner)
                firsttime = False

        if(not firsttime):
            cv2.putText(frame,  "Winner : ", (350, 385),
                        font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame,  winner, (480, 385), font,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame,  "Press S to Play", (320, 210),
                        font, 1, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame,  "Press Q to quit", (40, 445),
                        font, 1, (0, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xff == ord('s'):
            firsttime = True
            start = time.time()
            gate = 1
            break

        # To Exit from the game...
        if cv2.waitKey(1) & 0xff == ord('q'):
            exit(0)

    result = cv2.imread(s[3])
    if cv2.waitKey(1) & 0xff == ord('q'):
        exit = True
        break
    if(exit):
        break
    cv2.imshow('Frame', frame)

    cv2.imshow("A.I move", ai_frame)


img.release()
cv2.destroyAllWindows()
