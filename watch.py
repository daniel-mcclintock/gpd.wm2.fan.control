#!/bin/env python3
"""Less annoying fan, linear fan scaling.

MATCH_SENSORS: What sensors to consider when evaluating temperatures, the max
    temp sampled from these is used.

MAX_TEMP: Temps above this transition fan-speed to max.

MIN_TEMP: Temps below this transition fan-speed to 0.

 - Temps between MIN_TEMP and MAX_TEMP will transition between MIN_ACTIVE_SPEED
   and MAX_ACTIVE_SPEED linearly.

MIN_ACTIVE_SPEED: The lower limit for the fan speed if the temp is above
    MIN_TEMP.

MAX_ACTIVE_SPEED: The upper limit for the fan speed, 184 is 100% fan, do not
    exceed 184.

UP_SLEEP: How long to sleep between iterations when transitioning fan speed up.

DOWN_SLEEP: How long to sleep between iterations when transitioning the fan
    speed down.

SPEED_UP_STEP: How big a up step in fan speed is.
SPEED_DOWN_STEP: How big a down step in fan speed is.
"""
import time

import sensors

from fan_control import fan_control

MATCH_SENSORS = {
    "k10temp-pci-00c3": ["Tctl"],
    "nvmi-pci-0200": ["Composite"],
    "iwlwifi_1-virtual-0": ["temp1"],
    "amdgpu-pci-7300": ["edge"],
}

MIN_TEMP = 50
MAX_TEMP = 75

MIN_ACTIVE_SPEED = 40
MAX_ACTIVE_SPEED = 184

UP_SLEEP = 0.2
DOWN_SLEEP = 0.8

SPEED_UP_STEP = 10
SPEED_DOWN_STEP = 6


def do_watch():
    speed = 0

    while True:
        try:
            sensors.init()

            temp = [0]

            for chip in sensors.iter_detected_chips():
                if str(chip) in MATCH_SENSORS:
                    for feature in chip:
                        if feature.label in MATCH_SENSORS[str(chip)]:
                            temp.append(feature.get_value())

            sensors.cleanup

        except Exception as ex:
            # in rare cases sensors fails to init
            print(str(ex))

        temp = max(temp)

        # get normalised scale temp from 0.0 to 1.0
        scale = max(0, temp - MIN_TEMP) / (MAX_TEMP - MIN_TEMP)
        scale = min(scale, 1.0)

        # target speed for scale
        if temp < MIN_TEMP:
            target_speed = 0
        else:
            target_speed = scale * MAX_ACTIVE_SPEED
            target_speed = max(target_speed, MIN_ACTIVE_SPEED)
            target_speed = int(target_speed)

        new_speed = speed

        if speed < target_speed:
            new_speed += SPEED_UP_STEP
            # avoid overshoot
            new_speed = min(new_speed, target_speed)
            time.sleep(UP_SLEEP)
        else:
            new_speed -= SPEED_DOWN_STEP
            # avoid undershoot
            new_speed = max(new_speed, target_speed)
            time.sleep(DOWN_SLEEP)

        new_speed = min(max(0, new_speed), MAX_ACTIVE_SPEED)

        if new_speed != speed:
            fan_control(new_speed)
            speed = new_speed

        print(f"{new_speed} -> {target_speed} @ {temp}")


try:
    do_watch()
finally:
    # Set auto fan on exit, eg: 
    fan_control(-1)
