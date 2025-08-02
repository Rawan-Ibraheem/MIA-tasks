class Code:
    def encode(self, commands):
        encoded = ''
        for cmd in commands:
            encoded += str(len(cmd))+'#'+cmd
        return encoded

    def decode(self, encoded_string):
        commands = []
        i = 0
        while i < len(encoded_string):
            # Find the '#' separator
            j = i
            while encoded_string[j] != '#':
                j += 1
            length = int(encoded_string[i:j])
            command = encoded_string[j+1:j+1+length]
            commands.append(command)
            i = j + 1 + length
        return commands

codec = Code()
original_commands = ["Push", "Box,box", "Push", "Overtake"]
# Encode
encoded = codec.encode(original_commands)
print("Encoded:", encoded)

# Decode
decoded = codec.decode(encoded)
print("Decoded:", decoded)
