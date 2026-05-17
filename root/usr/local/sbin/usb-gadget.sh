#!/bin/bash
set -e

GADGET_DIR=/sys/kernel/config/usb_gadget/g1

mkdir -p $GADGET_DIR
cd $GADGET_DIR

# USB IDs
echo 0x1d6b > idVendor   # Linux Foundation
echo 0x0104 > idProduct  # Multifunction Composite Gadget
echo 0x0100 > bcdDevice  # v1.0.0
echo 0x0200 > bcdUSB     # USB 2.0

# USB device strings.
mkdir -p strings/0x409
echo "deaddead01234567"   > strings/0x409/serialnumber
echo "Example Org"        > strings/0x409/manufacturer
echo "Pi HID+Storage"     > strings/0x409/product

# Create configuration.
mkdir -p configs/c.1/strings/0x409
echo "HID + Mass Storage" > configs/c.1/strings/0x409/configuration
echo 120                  > configs/c.1/MaxPower

## HID/Keyboard configuration.
mkdir -p functions/hid.usb0
echo 1    > functions/hid.usb0/protocol   # Keyboard
echo 1    > functions/hid.usb0/subclass   # Boot interface
echo 8    > functions/hid.usb0/report_length

### Create standard boot keyboard HID descriptor.
echo -ne '\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x03\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x03\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0' \
    > functions/hid.usb0/report_desc

ln -sf functions/hid.usb0 configs/c.1/

## Mass storage device configuration.
mkdir -p functions/mass_storage.usb0
echo 1          > functions/mass_storage.usb0/stall
echo 0          > functions/mass_storage.usb0/lun.0/cdrom
echo 0          > functions/mass_storage.usb0/lun.0/ro
echo 0          > functions/mass_storage.usb0/lun.0/nofua
echo /piusb.bin > functions/mass_storage.usb0/lun.0/file

ln -sf functions/mass_storage.usb0 configs/c.1/

# Activate gadget.
udevadm settle -t 5 || true
ls /sys/class/udc > UDC
