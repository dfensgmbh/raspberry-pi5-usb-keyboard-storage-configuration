import typer
import time

# flake8: noqa: E501

MODIFIER_NONE = 0x00
MODIFIER_SHIFT = 0x02
MODIFIER_ALTGR = 0x40

# HID keycodes: (keycode, needs_shift)
CHAR_MAP = {
    # Lowercase letters.
    'a': (0x04, MODIFIER_NONE), 'b': (0x05, MODIFIER_NONE), 'c': (0x06, MODIFIER_NONE), 'd': (0x07, MODIFIER_NONE),
    'e': (0x08, MODIFIER_NONE), 'f': (0x09, MODIFIER_NONE), 'g': (0x0A, MODIFIER_NONE), 'h': (0x0B, MODIFIER_NONE),
    'i': (0x0C, MODIFIER_NONE), 'j': (0x0D, MODIFIER_NONE), 'k': (0x0E, MODIFIER_NONE), 'l': (0x0F, MODIFIER_NONE),
    'm': (0x10, MODIFIER_NONE), 'n': (0x11, MODIFIER_NONE), 'o': (0x12, MODIFIER_NONE), 'p': (0x13, MODIFIER_NONE),
    'q': (0x14, MODIFIER_NONE), 'r': (0x15, MODIFIER_NONE), 's': (0x16, MODIFIER_NONE), 't': (0x17, MODIFIER_NONE),
    'u': (0x18, MODIFIER_NONE), 'v': (0x19, MODIFIER_NONE), 'w': (0x1A, MODIFIER_NONE), 'x': (0x1B, MODIFIER_NONE),
    'z': (0x1C, MODIFIER_NONE), 'y': (0x1D, MODIFIER_NONE),  # y/z swapped!

    # Uppercase letters.
    'A': (0x04, MODIFIER_SHIFT), 'B': (0x05, MODIFIER_SHIFT), 'C': (0x06, MODIFIER_SHIFT), 'D': (0x07, MODIFIER_SHIFT),
    'E': (0x08, MODIFIER_SHIFT), 'F': (0x09, MODIFIER_SHIFT), 'G': (0x0A, MODIFIER_SHIFT), 'H': (0x0B, MODIFIER_SHIFT),
    'I': (0x0C, MODIFIER_SHIFT), 'J': (0x0D, MODIFIER_SHIFT), 'K': (0x0E, MODIFIER_SHIFT), 'L': (0x0F, MODIFIER_SHIFT),
    'M': (0x10, MODIFIER_SHIFT), 'N': (0x11, MODIFIER_SHIFT), 'O': (0x12, MODIFIER_SHIFT), 'P': (0x13, MODIFIER_SHIFT),
    'Q': (0x14, MODIFIER_SHIFT), 'R': (0x15, MODIFIER_SHIFT), 'S': (0x16, MODIFIER_SHIFT), 'T': (0x17, MODIFIER_SHIFT),
    'U': (0x18, MODIFIER_SHIFT), 'V': (0x19, MODIFIER_SHIFT), 'W': (0x1A, MODIFIER_SHIFT), 'X': (0x1B, MODIFIER_SHIFT),
    'Z': (0x1C, MODIFIER_SHIFT), 'Y': (0x1D, MODIFIER_SHIFT),  # y/z swapped!

    # Numbers.
    '1': (0x1E, MODIFIER_NONE), '2': (0x1F, MODIFIER_NONE), '3': (0x20, MODIFIER_NONE), '4': (0x21, MODIFIER_NONE),
    '5': (0x22, MODIFIER_NONE), '6': (0x23, MODIFIER_NONE), '7': (0x24, MODIFIER_NONE), '8': (0x25, MODIFIER_NONE),
    '9': (0x26, MODIFIER_NONE), '0': (0x27, MODIFIER_NONE),

    # Numbers with SHIFT.
    '+': (0x1E, MODIFIER_SHIFT), '"': (0x1F, MODIFIER_SHIFT), '*': (0x20, MODIFIER_SHIFT), 'ç': (0x21, MODIFIER_SHIFT),
    '%': (0x22, MODIFIER_SHIFT), '&': (0x23, MODIFIER_SHIFT), '/': (0x24, MODIFIER_SHIFT), '(': (0x25, MODIFIER_SHIFT),
    ')': (0x26, MODIFIER_SHIFT), '=': (0x27, MODIFIER_SHIFT),

    # AltGr + numbers.
    '¦': (0x1E, MODIFIER_ALTGR), '@': (0x1F, MODIFIER_ALTGR), '#': (0x20, MODIFIER_ALTGR), '°': (0x21, MODIFIER_ALTGR),
    '§': (0x22, MODIFIER_ALTGR), '¬': (0x23, MODIFIER_ALTGR), '|': (0x24, MODIFIER_ALTGR), '¢': (0x25, MODIFIER_ALTGR),
                                                                                              '~': (0x27, MODIFIER_ALTGR),

    # Whitespace / control.
    '\n': (0x28, MODIFIER_NONE),  # ENTER
    '\t': (0x2B, MODIFIER_NONE),  # TAB
    ' ':  (0x2C, MODIFIER_NONE),  # SPACE

    # Punctuation (without SHIFT).
    '-': (0x2D, MODIFIER_NONE),
    '<': (0x64, MODIFIER_NONE),
    ',': (0x36, MODIFIER_NONE),
    '.': (0x37, MODIFIER_NONE),

    # Punctuation (with SHIFT).
    '_': (0x2D, MODIFIER_SHIFT),
    '>': (0x64, MODIFIER_SHIFT),
    ';': (0x36, MODIFIER_SHIFT),
    ':': (0x37, MODIFIER_SHIFT),

    # Punctuation (AltGr).
    '\\': (0x64, MODIFIER_ALTGR),  # backslash

    # Umlaut / accented keys (without SHIFT).
    'ü': (0x2F, MODIFIER_NONE),
    'ö': (0x33, MODIFIER_NONE),
    'ä': (0x34, MODIFIER_NONE),
    '$': (0x30, MODIFIER_NONE),
    '\'': (0x31, MODIFIER_NONE),
    '?': (0x2E, MODIFIER_NONE),
    '^': (0x35, MODIFIER_NONE),

    # Umlaut / accented keys (with SHIFT).
    'è': (0x2F, MODIFIER_SHIFT),
    'é': (0x33, MODIFIER_SHIFT),
    'à': (0x34, MODIFIER_SHIFT),
    '£': (0x30, MODIFIER_SHIFT),
    '!': (0x35, MODIFIER_SHIFT),
    '`': (0x2E, MODIFIER_SHIFT),

    # AltGr accented / bracket keys.
    '[': (0x2F, MODIFIER_ALTGR),   # AltGr + ü
    ']': (0x30, MODIFIER_ALTGR),   # AltGr + $
    '{': (0x33, MODIFIER_ALTGR),   # AltGr + ö  (some sources say 0x34)
    '}': (0x34, MODIFIER_ALTGR),   # AltGr + ä
    '´': (0x31, MODIFIER_ALTGR),   # AltGr + '  (dead acute)
}

CHAR_MAP_US = {
    'a': (0x04, False), 'b': (0x05, False), 'c': (0x06, False), 'd': (0x07, False),
    'e': (0x08, False), 'f': (0x09, False), 'g': (0x0A, False), 'h': (0x0B, False),
    'i': (0x0C, False), 'j': (0x0D, False), 'k': (0x0E, False), 'l': (0x0F, False),
    'm': (0x10, False), 'n': (0x11, False), 'o': (0x12, False), 'p': (0x13, False),
    'q': (0x14, False), 'r': (0x15, False), 's': (0x16, False), 't': (0x17, False),
    'u': (0x18, False), 'v': (0x19, False), 'w': (0x1A, False), 'x': (0x1B, False),
    'y': (0x1C, False), 'z': (0x1D, False),

    'A': (0x04, True),  'B': (0x05, True),  'C': (0x06, True),  'D': (0x07, True),
    'E': (0x08, True),  'F': (0x09, True),  'G': (0x0A, True),  'H': (0x0B, True),
    'I': (0x0C, True),  'J': (0x0D, True),  'K': (0x0E, True),  'L': (0x0F, True),
    'M': (0x10, True),  'N': (0x11, True),  'O': (0x12, True),  'P': (0x13, True),
    'Q': (0x14, True),  'R': (0x15, True),  'S': (0x16, True),  'T': (0x17, True),
    'U': (0x18, True),  'V': (0x19, True),  'W': (0x1A, True),  'X': (0x1B, True),
    'Y': (0x1C, True),  'Z': (0x1D, True),

    '1': (0x1E, False), '2': (0x1F, False), '3': (0x20, False), '4': (0x21, False),
    '5': (0x22, False), '6': (0x23, False), '7': (0x24, False), '8': (0x25, False),
    '9': (0x26, False), '0': (0x27, False),

    '!': (0x1E, True),  '@': (0x1F, True),  '#': (0x20, True),  '$': (0x21, True),
    '%': (0x22, True),  '^': (0x23, True),  '&': (0x24, True),  '*': (0x25, True),
    '(': (0x26, True),  ')': (0x27, True),

    '\n': (0x28, False),  # Enter
    '\t': (0x2B, False),  # Tab
    ' ':  (0x2C, False),  # Space

    '-': (0x2D, False), '_': (0x2D, True),
    '=': (0x2E, False), '+': (0x2E, True),
    '[': (0x2F, False), '{': (0x2F, True),
    ']': (0x30, False), '}': (0x30, True),
    '\\': (0x31, False), '|': (0x31, True),
    ';': (0x33, False), ':': (0x33, True),
    "'": (0x34, False), '"': (0x34, True),
    '`': (0x35, False), '~': (0x35, True),
    ',': (0x36, False), '<': (0x36, True),
    '.': (0x37, False), '>': (0x37, True),
    '/': (0x38, False), '?': (0x38, True),
}

MODIFIER_NONE = 0x00
MODIFIER_SHIFT = 0x02
HID_DEVICE = '/dev/hidg0'
# Delay between individual keystrokes.
KEY_DELAY = 0.020


def _write_report(modifier: int, keycode: int) -> None:
    report = bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00])
    with open(HID_DEVICE, 'rb+') as fd:
        fd.write(report)


def _key_release() -> None:
    _write_report(MODIFIER_NONE, 0x00)


def send_text(text: str) -> None:
    """
    Send specified text to the USB host as a HID keyboard.

    Args:
        text (str): The text to send.
    """
    for char in text:
        if char not in CHAR_MAP:
            raise ValueError(f"Unsupported character: {repr(char)}")

        keycode, needs_shift = CHAR_MAP[char]
        modifier = MODIFIER_SHIFT if needs_shift else MODIFIER_NONE

        _write_report(modifier, keycode)
        _key_release()

        time.sleep(KEY_DELAY)


if __name__ == "__main__":
    typer.run(send_text)
