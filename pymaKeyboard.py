import time
from Quartz.CoreGraphics import CGEventCreateKeyboardEvent, CGEventPost, \
	CGEventSourceCreate, kCGEventSourceStateHIDSystemState, kCGHIDEventTap

PYMAK_SOURCE_REF = CGEventSourceCreate(kCGEventSourceStateHIDSystemState)
PYMAK_LOWERKEYS = {"a": 0x00, "s": 0x01, "d": 0x02, "f": 0x03, "h": 0x04, \
	"g": 0x05, "z": 0x06, "x": 0x07, "c": 0x08, "v": 0x09, "b": 0x0b, \
	"q": 0x0c, "w": 0x0d, "e": 0x0e, "r": 0x0f, "y": 0x10, "t": 0x11, \
	"1": 0x12, "2": 0x13, "3": 0x14, "4": 0x15, "6": 0x16, "5": 0x17, \
	"=": 0x18, "9": 0x19, "7": 0x1a, "-": 0x1b, "8": 0x1c, "0": 0x1d, \
	"]": 0x1e, "o": 0x1f, "u": 0x20, "[": 0x21, "i": 0x22, "p": 0x23, \
	"l": 0x25, "j": 0x26, "'": 0x27, "k": 0x28, ";": 0x29, "\\": 0x2a, \
	",": 0x2b, "/": 0x2c, "n": 0x2d, "m": 0x2e, ".": 0x2f, " ": 0x31, "`": 0x32}
PYMAK_UPPERKEYS = {"A": 0x00, "S": 0x01, "D": 0x02, "F": 0x03, "H": 0x04, \
	"G": 0x05, "Z": 0x06, "X": 0x07, "C": 0x08, "V": 0x09, "B": 0x0b, \
	"Q": 0x0c, "W": 0x0d, "E": 0x0e, "R": 0x0f, "Y": 0x10, "T": 0x11, \
	"!": 0x12, "@": 0x13, "#": 0x14, "$": 0x15, "^": 0x16, "%": 0x17, \
	"+": 0x18, "(": 0x19, "&": 0x1a, "_": 0x1b, "*": 0x1c, ")": 0x1d, \
	"}": 0x1e, "O": 0x1f, "U": 0x20, "{": 0x21, "I": 0x22, "P": 0x23, \
	"L": 0x25, "J": 0x26, '"': 0x27, "K": 0x28, ":": 0x29, "|": 0x2a, \
	"<": 0x2b, "?": 0x2c, "N": 0x2d, "M": 0x2e, ">": 0x2f, "~": 0x32}
PYMAK_MODKEYS = {"command": 0x37, "shift": 0x38, "option": 0x3a, "control": 0x3b, \
	"rightshift": 0x3c, "rightoption": 0x3d, "rightcontrol": 0x3e, "fn": 0x3f}
PYMAK_EXTRAKEYS = {"return": 0x24, "tab": 0x30, "delete": 0x33, "escape": 0x35, \
	"f17": 0x40, "f18": 0x4f, "f19": 0x50, "f20": 0x5a, "f5": 0x60,       \
	"f6": 0x61, "f7": 0x62, "f3": 0x63, "f8": 0x64, "f9": 0x65,           \
	"f11": 0x67, "f13": 0x69, "f16": 0x6a, "f14": 0x6b, "f10": 0x6d,      \
	"f12": 0x6f, "f15": 0x71, "help": 0x72, "home": 0x73, "pageup": 0x74, \
	"backspace": 0x75, "f4": 0x76, "end": 0x77, "f2": 0x78,               \
	"pagedown": 0x79, "f1": 0x7a, "left": 0x7b, "right": 0x7c,            \
	"down": 0x7d, "up": 0x7e}
PYMAK_NICEKEYS = {"\t": "tab", "\r": "return", "\n": "return"}

def typeLetter(singleChar):
	if (PYMAK_LOWERKEYS.has_key(singleChar)):
		# Unmodified key
		keyDown = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_LOWERKEYS[singleChar], True)
		CGEventPost(kCGHIDEventTap, keyDown)
		keyUp = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_LOWERKEYS[singleChar], False)
		CGEventPost(kCGHIDEventTap, keyUp)
	elif (PYMAK_UPPERKEYS.has_key(singleChar)):
		# Shift modified key
		shiftDown = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_MODKEYS["shift"], True)
		CGEventPost(kCGHIDEventTap, shiftDown)
		keyDown = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_UPPERKEYS[singleChar], True)
		CGEventPost(kCGHIDEventTap, keyDown)
		keyUp = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_UPPERKEYS[singleChar], False)
		CGEventPost(kCGHIDEventTap, keyUp)
		shiftUp = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_MODKEYS["shift"], False)
		CGEventPost(kCGHIDEventTap, shiftUp)
	elif (PYMAK_NICEKEYS.has_key(singleChar)):
		# Some nice keys to have standard support for
		keyDown = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_EXTRAKEYS[PYMAK_NICEKEYS[singleChar]], True)
		CGEventPost(kCGHIDEventTap, keyDown)
		keyUp = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_EXTRAKEYS[PYMAK_NICEKEYS[singleChar]], False)
		CGEventPost(kCGHIDEventTap, keyUp)
	time.sleep(0.0008)

def typeString(theString = None):
	if ((theString == None) or (type(theString) != type(''))): return
	for x in theString:
		typeLetter(x)

def typeSpecialKey(keyOrName, doShiftDown = False, doCommandDown = False, doOptionDown = False, doControlDown = False):
	if ((not keyOrName) or (type(keyOrName) != type(''))): return
	k = keyOrName.lower()
	if (PYMAK_LOWERKEYS.has_key(k)):
		k = PYMAK_LOWERKEYS[k]
	elif (PYMAK_EXTRAKEYS.has_key(k)):
		k = PYMAK_EXTRAKEYS[k]
	else:
		return
	mods = {"shift": doShiftDown, "command": doCommandDown, \
		"option": doOptionDown, "control": doControlDown}
	for mk in mods.keys():
		if (mods[mk]):
			modDown = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_MODKEYS[mk], True)
			CGEventPost(kCGHIDEventTap, modDown)
	keyDown = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, k, True)
	CGEventPost(kCGHIDEventTap, keyDown)
	keyUp = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, k, False)
	CGEventPost(kCGHIDEventTap, keyUp)
	for mk in mods.keys():
		if (mods[mk]):
			modUp = CGEventCreateKeyboardEvent(PYMAK_SOURCE_REF, PYMAK_MODKEYS[mk], False)
			CGEventPost(kCGHIDEventTap, modUp)
	time.sleep(0.0008)
