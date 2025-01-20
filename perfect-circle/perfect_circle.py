import pyautogui 
from time import sleep
from math import sqrt
from mpmath import mp
mp.prec = 256
pyautogui.PAUSE = 0.001
pyautogui.DARWIN_CATCH_UP_TIME = 0.001

def draw_circle(radius_,speed_,x_initial_,y_initial_):
    def bottom_right():
        for i in range(0,radius_+1,speed_):
            if i == 0:
                pass
            else:
                x_pos = i + x_initial_
                y_pos = sqrt(radius_**2 - i**2) + y_initial_
                print(f'{x_pos - x_initial_}, {y_pos - y_initial_}')
                pyautogui.moveTo(x_pos,y_pos)
    def top_right():
        for i in range(0,radius_+1,speed_):
            x_pos = x_initial_ + radius_ - i
            y_pos = -sqrt(radius_**2 - (radius_-i)**2) + y_initial_
            print(f'{x_pos - x_initial_}, {y_pos - y_initial_}')
            pyautogui.moveTo(x_pos,y_pos)
    def top_left():
        for i in range(0,radius_+1,speed_):
            x_pos = -i + x_initial_
            y_pos = -sqrt(radius_**2 - i**2) + y_initial_
            print(f'{x_pos - x_initial_}, {y_pos - y_initial_}')
            pyautogui.moveTo(x_pos,y_pos)
    def bottom_left():
        for i in range(0,radius_+1,speed_):
            x_pos = x_initial_ - radius_ + i
            y_pos = sqrt(radius_**2 - (radius_-i)**2) + y_initial_
            print(f'{x_pos - x_initial_}, {y_pos - y_initial_}')
            pyautogui.moveTo(x_pos,y_pos)
    def overshoot(length):
        for i in range(0,speed_*length,speed_):
            x_pos = i + x_initial_
            y_pos = sqrt(radius_**2 - i**2) + y_initial_
            print(f'{x_pos - x_initial_}, {y_pos - y_initial_}')
            pyautogui.moveTo(x_pos,y_pos)
    bottom_right()
    top_right()
    top_left()
    bottom_left()
    overshoot(10)

def main():
    #half screen = 480.5, 535.5
    #full screen = 960, 520
    x_initial, y_initial = 960, 520
    radius = 500
    speed = 25
    
    sleep(2)
    pyautogui.moveTo(x_initial,y_initial + radius)
    sleep(1)
    pyautogui.mouseDown()
    draw_circle(radius,speed,x_initial,y_initial)
    pyautogui.mouseUp()

if __name__ == '__main__':
    main()