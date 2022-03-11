import os
import subprocess
import queue
import threading
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

def beacon(l):
    #l = ["1", "1", "0"]
    timeout = "1"
    major = int(l[1])
    m1 = str(major & 0x00FF)
    m2 = str((major - int(m1)) >> 8)
    print("m1: {}, m2: {}".format(m1, m2))
    minor = l[2]
    
    print('in beacon mi: {}'.format(l[2]))

    result = subprocess.run(["python3", "example-altbeacon", "--timeout", timeout, "--major", m1, "--major2", m2, "--minor", minor])

q = queue.Queue()

def get_button():
    flag = True
    pushed = False
    for i in range(1000):
        if pushed:
            pass
        elif flag and GPIO.input(17) == GPIO.HIGH:
            flag = False
            pushed = True
            
        elif GPIO.input(17) == GPIO.LOW:
            flag = True
        
        sleep(0.001)
    print('button status: {}'.format(pushed))
    
    q.put({'pushed': pushed})

def main():
    while True:
        threadlist = list()
        threadlist.append(threading.Thread(target=get_button))
        if not q.empty():
            data=q.get()
            minor = "0"
            if data['pushed']:
                minor = "1"
            
            threadlist.append(threading.Thread(target=beacon, args=(["1", "50000", minor],)))

        for thread in threadlist:
            thread.start()
        
        for thread in threadlist:
            thread.join()

if __name__ == '__main__':
    main()
    
