from periphery import GPIO
import time

BCM_NO = {21:24,20:22,19:18,16:10,13:35,
        12:33,6:19,5:15,23:28,22:26,
        27:40,18:16,17:12,4:13,15:8,14:37}
IO_TYPE = {"OUTPUT":"out","INPUT":"in"}
GPIO_list = {}

def setup(pin,IO_type):
    try:
        if IO_type in IO_TYPE:
            GPIO_list[pin] = GPIO(pin, IO_TYPE[IO_type])
    except KeyError:
        print("IO pin should in playrobot python learning board. And IO_Type must be INPUT or OUTPUT.")

def input(pin):
    if pin in GPIO_list:
        return GPIO_list[pin].read()
        
    else:
        raise "this port not set yet!"

def output(pin,state):
    if pin in GPIO_list:
        GPIO_list[pin].write(state)
    else:
        raise "this port not set yet!"
