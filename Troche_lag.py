import cv2
import numpy as np
from time import time

# define a video capture object
vid = cv2.VideoCapture(0)

vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)

vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

film = []

now = time()

pomocnicza1 = False
pomocnicza2 = False
pomocnicza3 = False
pomocnicza4 = False

orginal_casowy = 0.5
opoznione = 0.25

element = np.zeros((720, 1280, 3), dtype=np.uint8)

while True:

    ret, frame = vid.read()
    #frame = cv2.resize(frame, dsize=(1920, 1080), interpolation=cv2.INTER_CUBIC)


    film.append(frame)

    if len(film) < 120:
        continue

    klawisz = cv2.waitKey(int(1000 / 60))

    if klawisz & 0xFF == ord('1') and not pomocnicza1:
        pomocnicza1 = True
    elif klawisz & 0xFF == ord('1') and pomocnicza1:
        pomocnicza1 = False

    if klawisz & 0xFF == ord('2') and not pomocnicza2:
        pomocnicza2 = True
    elif klawisz & 0xFF == ord('2') and pomocnicza2:
        pomocnicza2 = False

    if klawisz & 0xFF == ord('3') and not pomocnicza3:
        pomocnicza3 = True
    elif klawisz & 0xFF == ord('3') and pomocnicza3:
        pomocnicza3 = False

    if klawisz & 0xFF == ord('4') and not pomocnicza4:
        pomocnicza4 = True
    elif klawisz & 0xFF == ord('4') and pomocnicza4:
        pomocnicza4 = False

    a = [pomocnicza1,pomocnicza2,pomocnicza3,pomocnicza4]
    if pomocnicza1:
        if sum(a) == 1:
            orginal_casowy = 1
        elif sum(a) == 2:
            orginal_casowy = 0.6
            opoznione = 0.4
        elif sum(a) == 3:
            orginal_casowy = 0.5
            opoznione = 0.25
        elif sum(a) == 4:
            orginal_casowy = 0.4
            opoznione = 0.2
    elif not pomocnicza1:
        if sum(a) == 1:
            opoznione = 1
        elif sum(a) == 2:
            opoznione = 0.5
        elif sum(a) == 3:
            opoznione = 0.333

    out_frame = element


    if pomocnicza1:
        out_frame = np.add(out_frame, np.multiply(film[-1], orginal_casowy))

    if len(film) > 40 and pomocnicza2:
        out_frame = np.add(out_frame, np.multiply(film[len(film) - 39],opoznione))


    if len(film) > 80 and pomocnicza3:
        out_frame = np.add(out_frame, np.multiply(film[len(film) - 79],opoznione))


    if len(film) > 10 and pomocnicza4:
        out_frame = np.add(out_frame, np.multiply(film[len(film) - 10],opoznione))

    film.pop(0)

    out_frame = np.where(out_frame > 255, 255, out_frame)

    cv2.imshow('out_frame', np.array(out_frame,dtype=np.uint8))
    #cv2.resizeWindow("out_frame", 1920, 1080)

    if klawisz & 0xFF == ord('q'):
        break

print(time() - now)
# After the loop release the cap object
vid.release()
print(film[0].shape)
# Destroy all the windows
cv2.destroyAllWindows()