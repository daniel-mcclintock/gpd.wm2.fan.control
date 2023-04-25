"""Control GPD Win Max 2 Fan speed."""
import portio

GPD_WM2_ECRAM = 0x4E  # 78
GPD_WM2_ECRAM_FAN_MANUAL = 0x275  # 629
GPD_WM2_ECRAM_FAN_MANUAL_SPEED = 0x1809  # 6153
REG_ADDR = 0x4E  # 78
REG_DATA = 0x4F  # 79


def fan_control(speed):
    """Fan speed, viable speeds ~40 - 183, -1 == auto"""
    if portio.ioperm(GPD_WM2_ECRAM, 2, 1) == 0:
        if speed == -1:
            # auto
            write(GPD_WM2_ECRAM_FAN_MANUAL, 0)
        else:
            # manual 0 - 183
            write(GPD_WM2_ECRAM_FAN_MANUAL, 1)
            write(GPD_WM2_ECRAM_FAN_MANUAL_SPEED, int(speed))
    else:
        raise PermissionError("Fan control requires root access")


def _write(addr, data):
    portio.outb(addr, data)


def write(addr, data):
    """Write data to EC"""
    addr_upper = addr >> 8 & 255
    addr_lower = addr & 255

    _write(0x2E, REG_ADDR)
    _write(0x11, REG_DATA)
    _write(0x2F, REG_ADDR)
    _write(addr_upper, REG_DATA)

    _write(0x2E, REG_ADDR)
    _write(0x10, REG_DATA)
    _write(0x2F, REG_ADDR)
    _write(addr_lower, REG_DATA)

    # Actually write the fan speed
    _write(0x2E, REG_ADDR)
    _write(0x12, REG_DATA)
    _write(0x2F, REG_ADDR)
    _write(data, REG_DATA)
