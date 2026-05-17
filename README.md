# raspberry-pi5-usb-keyboard-storage-configuration

Configuration and scripts to make the Raspberry Pi 5 shows as a composite USB client device (HID/keyboard and storage)

These scripts make a Raspberry Pi 5 to show itself as a HID keyboard and mass storage device (disk). We change the USB mode to `peripheral` and thus can connect to a USB host (for example a computer). The USB host will see a USB disk and a USB keyboard.

To see the contents of the USB disk on the Raspberry Pi you can mount the image file `read-only`. Do not change the contents of the USB disk when the USB host connects to it.
When you want to change the contents of the disk on the Raspberry Pi, you must disconnect the disk. You can disconnect with `modprobe` or "eject" the disk on the host computer. Then, mount the disk on the Raspberry Pi and change the contents of the disk. When you want to connect to the host again, you must use `modprobe -r` and `modprobe`. With this, the host computer sees the disk again.

There are connect and disconnect scripts in the `scripts` folder:

* `07_disconnect_usb-gadget.sh`
* `08_connect_usb-gadget.sh`

You must use a USB-C cable from and connect the Raspberry Pi 5 to the USB host computer.

## Installation

Go to the `root` folder in this repository and follow the instructions. All scripts and files are "hard coded". If you change the path and file names you have to change these in all the scripts.

NOTE: You need `root` and `sudo` for the installation and most of the scripts.

## Disk image

The disk image is `/piusb.bin`.

### Summary

1. Create a file that contains the contents of the mass storage device.
2. Change the file `config.txt`.
3. Change the file `cmdline.txt`.
4. Create the `usb-gadget.sh` script.
5. Create the `usbgadget.service` service.
6. Enable the `usbgadget.service` service.
7. Restart.

## Examine changes on the disk

When you want to see if the host computer changed the contents of the disk you can use the `06_show_changes.sh` script. This script examines the file `README.md` on the disk. When the contents of the file changes, the script show the new contents. In addition, the script creates a copy of the file in the current working directory.
