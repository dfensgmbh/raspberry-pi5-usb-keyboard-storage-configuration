# raspberry-pi5-usb-keyboard-storage-configuration

Configuration and scripts to make the Raspberry Pi 5 shows as a composite USB client device (HID/keyboard and storage)

These scripts make a Raspberry Pi 5 to show itself as a HID keyboard and mass storage device. We change the USB mode to `peripheral` and thus can connect to a USB host (for example a computer). The USB host will see a USB mass storage device and a USB keyboard.

## Installation

Go to the `root` folder in this repository and follow the instructions.

### Summary

1. Create a file that contains the contents of the mass storage device.
2. Change the file `config.txt`.
3. Change the file `cmdline.txt`.
4. Create the `usb-gadget.sh` script.
5. Create the `usbgadget.service` service.
6. Enable the `usbgadget.service` service.
7. Restart

### Disconnect the mass storage device

### Connect the mass storage device
