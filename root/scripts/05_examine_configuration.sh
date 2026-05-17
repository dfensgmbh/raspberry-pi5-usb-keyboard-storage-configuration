ls /dev/hidg*        # Should show /dev/hidg0
ls /sys/class/udc/   # Should show the UDC controller
dmesg | grep dwc2    # Check for errors
