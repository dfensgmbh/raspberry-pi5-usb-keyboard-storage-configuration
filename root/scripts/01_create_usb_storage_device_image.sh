# Create an image file that contains the contents of the USB storage device.
# Change `count` to the size you need.
sudo dd if=/dev/zero of=/piusb.bin bs=1M count=64
sudo mkdosfs /piusb.bin
