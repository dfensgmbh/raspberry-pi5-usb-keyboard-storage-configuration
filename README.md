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
2. Change the file in:
    ```/boot/firmware/config.txt```
4. Change the file `cmdline.txt`.
5. Create the `usb-gadget.sh` script.
6. Create the `usbgadget.service` service.
7. Enable the `usbgadget.service` service.
8. Restart.

## Examine changes on the disk

When you want to see if the host computer changed the contents of the disk you can use the `06_show_changes.sh` script. This script examines the file `README.md` on the disk. When the contents of the file changes, the script show the new contents. In addition, the script creates a copy of the file in the current working directory.

## Send text to the host computer via the keyboard

When you want to send text to the USB host computer, do these steps:

1. Change to the root directory of the repository, and prepare the Python environment:

    ```
    uv sync --extra dev --extra build --python 3.13
    ```

2. Activate the python environment:

    ```
    source .venv/bin/activate
    ```

3. Start the program:

    ```
    sudo .venv/bin/python -m src arbitrary_text_to_send_with_keyboard
    ```

## Mass Storage Device on Windows 11

<img width="528" height="122" alt="image" src="https://github.com/user-attachments/assets/37c3a771-e55c-4749-9be5-22509b8ccd4e" />

<img width="463" height="151" alt="image" src="https://github.com/user-attachments/assets/da799e98-a593-4941-8af7-f35b5203e5f4" />
