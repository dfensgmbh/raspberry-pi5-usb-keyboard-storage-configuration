#!/bin/bash

# Copyright (C) 2026 Ronald Rink, d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This script examines changes in the file `$FILE` inside the USB mass storage device.
set -euo pipefail

MOUNT_POINT="/mnt/usb_share"
IMAGE="/piusb.bin"
POLL_INTERVAL=5
FILE="README.md"
CHECKSUM_FILE="${FILE}.sha256"

mkdir -p "$MOUNT_POINT"

# Cleanup on Ctrl+C.
cleanup() {
    echo "Detected signal: unmounting and exiting ..."
    if mountpoint -q "$MOUNT_POINT"; then
        sudo umount "$MOUNT_POINT"
    fi
    exit 0
}
trap cleanup SIGINT SIGTERM

while true; do
    sleep "$POLL_INTERVAL"

    # Unmount if currently mounted.
    if mountpoint -q "$MOUNT_POINT"; then
        sudo umount "$MOUNT_POINT"
    fi

    # Drop page cache so kernel re-reads from disk.
    echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

    # Remount read-only.
    sudo mount -o loop,ro "$IMAGE" "$MOUNT_POINT"

    TARGET_FILE="$MOUNT_POINT/$FILE"

    if [[ ! -f "$TARGET_FILE" ]]; then
        echo "Warning: '$TARGET_FILE' not found on mounted volume."
        ls -la "$MOUNT_POINT"
        continue
    fi

    # Create sha256sum checksum line: "<hash>  <filename>".
    NEW_SUM="$(sha256sum "$TARGET_FILE")"

    if [[ ! -f "$CHECKSUM_FILE" ]]; then
        echo "No previous checksum found — showing mounted volume contents:"
        ls -la "$MOUNT_POINT"
        echo "--- $FILE contents ---"
        cat "$TARGET_FILE"
        echo "$NEW_SUM" > "$CHECKSUM_FILE"
        continue
    fi

    OLD_SUM="$(cat "$CHECKSUM_FILE")"
    if [[ "$NEW_SUM" == "$OLD_SUM" ]]; then
        echo "No change detected in '$FILE'."
        continue
    fi

    echo "'$FILE' changed — showing mounted volume contents:"
    ls -la "$MOUNT_POINT"
    echo "--- $FILE contents ---"
    cat "$TARGET_FILE"
    echo "$NEW_SUM" > "$CHECKSUM_FILE"
done
