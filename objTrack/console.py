import numpy as np
import main
import sys
import time
import keyboard as ky
while True:
    if ky.is_pressed('q'):
        print("pressed!")
        break
    print('\r' + str(main.show_frame(False,True)))
    
    
    
