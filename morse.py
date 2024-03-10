MORSE_CODE = {
    'A': '.-',     'B': '-...',   'C': '-.-.', 
    'D': '-..',    'E': '.',      'F': '..-.', 
    'G': '--.',    'H': '....',   'I': '..', 
    'J': '.---',   'K': '-.-',    'L': '.-..', 
    'M': '--',     'N': '-.',     'O': '---', 
    'P': '.--.',   'Q': '--.-',   'R': '.-.', 
    'S': '...',    'T': '-',      'U': '..-', 
    'V': '...-',   'W': '.--',    'X': '-..-', 
    'Y': '-.--',   'Z': '--..',   ' ': ' '
}

def dot():
    led.value(1)
    utime.sleep(0.25)  # Time unit for dot
    led.value(0)
    utime.sleep(0.25)  # Space between symbols

def dash():
    led.value(1)
    utime.sleep(0.75)  # Time unit for dash (3 times the dot duration)
    led.value(0)
    utime.sleep(0.25)  # Space between symbols

def letter_space():
    utime.sleep(0.75)  # Space between letters (3 time units minus the space after the dot or dash)

# Define the Morse code for "Hello" using the dot and dash functions
import utime

def hello_in_morse():
    # H: ****
    dot(); dot(); dot(); dot()
    letter_space()
    # E: *
    dot()
    letter_space()
    # L: *-**
    dot(); dash(); dot(); dot()
    letter_space()
    # L: *-**
    dot(); dash(); dot(); dot()
    letter_space()
    # O: ---
    dash(); dash(); dash()
    
def blink_morse_code(led, text, unit=.25):
    """
    Blink an LED to represent a string in Morse code.
    
    Args:
    - led: An LED object with .value(1|0) to turn on/off the LED.
    - text: The string to convert to Morse code.
    - unit: The base time unit for dots and dashes.
    """
    for char in text.upper():
        if char in MORSE_CODE:
            for symbol in MORSE_CODE[char]:
                if symbol == '.':
                    led.value(1)
                    utime.sleep(unit)
                elif symbol == '-':
                    led.value(1)
                    utime.sleep(unit * 3)
                led.value(0)
                utime.sleep(unit)  # Space between symbols
            utime.sleep(unit * 3)  # Space between letters
        elif char == ' ':
            utime.sleep(unit * 7)  # Space between words
