#!/usr/bin/env python
import freenect
import time
import random
import signal

keep_running = True
last_time = 0




def f(*args, **kw):
    pass

def mybody(*args):
    dev, ctx = args
    global last_time
    print(last_time)
    if not keep_running:
        raise freenect.Kill
    if time.time() - last_time < 3:
        return
    last_time = time.time()
    led = random.randint(0, 6)
    tilt = random.randint(0, 30)
    freenect.set_led(dev, led)
    freenect.set_tilt_degs(dev, tilt)
    print('led[%d] tilt[%d] accel[%s]' % (led, tilt, freenect.get_accel(dev)))

def handler(signum, frame):
    """Sets up the kill handler, catches SIGINT"""
    global keep_running
    keep_running = False
    print('stopping')
print('Press Ctrl-C in terminal to stop')
signal.signal(signal.SIGINT, handler)
print('start loop')

freenect.runloop(depth=f, video=f, body=mybody)

