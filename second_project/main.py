def text_to_serial_string(text):
    start_bit = '0'
    stop_bits = '11'
    serial_string = ""

    for char in text:
        # Convert to 8-bit binary and reverse the order (LSB to MSB)
        char_bits = format(ord(char), '08b')[::-1]
        serial_char = start_bit + char_bits + stop_bits
        serial_string += serial_char

    return serial_string


def serial_string_to_text(serial_string):
    start_bit = '0'
    stop_bits = '11'

    text = ""
    index = 0
    while index < len(serial_string):
        if serial_string[index] == start_bit:  # Check for start bit
            # Extract character bits (still reversed)
            char_bits_reversed = serial_string[index + 1:index + 9]
            # Reverse the order back to the original (MSB to LSB)
            char_bits = char_bits_reversed[::-1]
            char = chr(int(char_bits, 2))  # Convert binary to ASCII character
            text += char
            # Move to the next character (1 start bit + 8 character bits + 2 stop bits)
            index += 11
        else:
            raise ValueError("Invalid bit stream format")

    return text

# Example usage:


# Encode text into a bit stream
text = str(input("Enter pahse: "))
serial_string = text_to_serial_string(text)
print("Encoded bit stream:")
print(serial_string)

# Decode the bit stream back to text
decoded_text = serial_string_to_text(serial_string)
print("Decoded text:")
print(decoded_text)
