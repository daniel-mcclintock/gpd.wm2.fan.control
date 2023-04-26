# gpd.wm2.fan.control

This hopefully provides a less annoying fan experience on a GPD Win Max 2, the 
default behaviour in my experience is too aggressive at low temperatures and 
not aggressive enough at high temperatures while also lacking between the two
extremes.

## Usage:

```
sudo ./watch.py
```

## Configuration

Generally speaking, this will adjust the fan speed to scale between
MIN_ACTIVE_SPEED and MAX_ACTIVE_SPEED based on a normalised scale temperature
between MIN_TEMP and MAX_TEMP.

This initial version is manually configured, no config file or arguments.
See `watch.py` for where you can set custom values for your desired fan
behaviour. The variables to change are described below.

You will probably want to align the temperature limits in the GPD Win Max 2 Bios
to match your desired fan behaviour, this is not normally configurable in the
bios, but you can "unlock" the advanced settings by pressing ALT-F5, saving and
rebooting back into the bios. You can then enter the Advanced settings menu,
then SMU control and then adjust the thermal limits by setting a custom TJ Max
value.

Alternatively, you could use something like `ryzenadj` to set this at runtime.

Update the constants described below to reflect your desired fan behaviour:

````
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

MATCH_SENSORS: A dictionary of lm-sensor device and sensor labels to be used to
    read temperature data from, depending on your software configuration this 
    can vary. To work out what sensor labels your system presents run `sensors`:

    eg:
    ```
        zenpower-pci-00c3
        Adapter: PCI adapter
        Tdie:         +51.9°C  (high = +95.0°C)
        Tctl:         +51.9°C

        nvme-pci-0200
        Adapter: PCI adapter
        Composite:    +37.9°C  (low  =  -0.1°C, high = +74.8°C)
                               (crit = +79.8°C)

        iwlwifi_1-virtual-0
        Adapter: Virtual device
        temp1:        +43.0°C

        amdgpu-pci-7300
        Adapter: PCI adapter
        vddgfx:      710.00 mV
        vddnb:       734.00 mV
        edge:         +51.0°C
        PPT:           2.10 W
    ```

    A MATCH_SENSORS dictionary to reflect the above would be:

    ```
        MATCH_SENSORS = {
            "zenpower-pci-00c3": ["Tdie", "Tctl"],
            "nvmi-pci-0200": ["Composite"],
            "iwlwifi_1-virtual-0": ["temp1"],
            "amdgpu-pci-7300": ["edge"],
        }
    ```
````

## Details:

See: `watch.py` for the fan control "daemon".
See: `fan_control.py` for the actual code that writes to the EC address to
control the fan.

See also: https://github.com/matega/win-max-2-fan-control
