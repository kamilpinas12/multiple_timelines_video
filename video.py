import cv2
import numpy as np
from time import time
from typing import Tuple, List
import keyboard



class Video:
    def __init__(self, time_lines: List[Tuple[int, str]], quit_button: str):
        
        #time_lines słownik (ilość klaten na sekunde w tył(dodatnie), klawisz włączający lub wyłączający ten przebieg(str))
        self.time_lines = time_lines

        self.quit_button = quit_button

        #wyłączenie wszystkich timelineów
        self.state = [0] * len(time_lines)



    def start(self, fps: int = 60, frame_shape: Tuple[int, int] = (480, 640), title: str = "Video"):

        delay = 1 / 60
        lst_time = time()

        vid = cv2.VideoCapture(0)

        film_size = max(self.time_lines, key=lambda x: x[0])[0]

        film = []
        self.default_frame = np.zeros(frame_shape + (3, ))



        while True:
            if (time() - lst_time) > delay:
                lst_time = time()

                _, frame = vid.read()
                film.append(frame)

                if len(film) < film_size + 1:
                    continue
                else:
                    film.pop(0)
            

                cv2.imshow(title, self.get_out_frame(film))


                if keyboard.is_pressed(self.quit_button):
                    break
                
                cv2.waitKey(1)

            else:
                if keyboard.is_pressed(self.quit_button):
                    break


        vid.release()        
        cv2.destroyAllWindows()  



    def get_out_frame(self, film):
        out_frame = self.default_frame

        for i, (t, key) in enumerate(self.time_lines):
            if keyboard.is_pressed(key) and keyboard.is_pressed("shift"):
                self.state[i] = 0
            elif keyboard.is_pressed(key):
                self.state[i] = 1

        if sum(self.state) == 0:
            return out_frame    
        
        n = 1/sum(self.state)

        for i, (t, _) in enumerate(self.time_lines):
            if self.state[i]:
                out_frame = np.add(out_frame, np.multiply(film[-t] , n))    
            

        return np.array(out_frame, dtype=np.uint8)
    

