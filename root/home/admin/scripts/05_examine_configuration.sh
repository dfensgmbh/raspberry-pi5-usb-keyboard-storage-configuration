ls /dev/hidg*        # Must show /dev/hidg0.
ls /sys/class/udc/   # Must show the UDC controller.
dmesg | grep dwc2    # Examine for any errors.
