# If `echo tee` shows an error, ignore it.
echo "" | sudo tee /sys/kernel/config/usb_gadget/g1/UDC
sudo modprobe -r g_mass_storage
