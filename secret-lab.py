import random
# both ways stuff, shared by both me and john
p: int = 808241878912418587664668869752380201227471917587049402831353579654087934716257177583988001816750842723486468130003910337833297294744103045277794137039348379685305766000049233920274403424909809118398706373176342402680527597912453031947055263965574521088574747656702199527971035049821214553730158203939
g: int = 2

# john's public key, i use this to encrypt my message and send it to him, given to me by john
a: int = 232776343254475000399703950622050363150042223625177014198929234401212675210038579218292434526526374082925071163131994952558899624844364841082089396570570225786199190021288348405073108777200323973770403536044277880631661314326452532373031693236191798967750863498867080388017998943491279903675203454640

# my private key, i use this to decrypt what john sends to me, i made this one randomly
private_key: int
# my public key, i send this to john so he can encrypt something and send it back to me, i made this one randomly
public_key: int

# this is the text that i will be encrypting and sending to john using the public key gave to me, only he can decrypt it
message: str


# convert a message string into a list of integers that will be small enough to fit into the prime john gave to me
def make_message_blocks(string: str) -> list[int]:
    final_list: list[int] = []
    current_number: int = 0
    index: int = len(string) - 1
    k: int = 0
    while index >= 0:
        next_number: int = current_number + ord(string[index]) * 256 ** k
        if next_number < p:
            current_number = next_number
            k += 1
            if index == 0:
                final_list.insert(0, current_number)
        else:
            final_list.insert(0, current_number)
            current_number = 0
            k = 0
        index -= 1
    return final_list

# given the message blocks, turn them back into a readable string, used by decrypt to produce a final result


def message_blocks_to_message(message_blocks: list[int]) -> str:
    a: int = 0
    final_list: list[str] = []
    while a < len(message_blocks):
        bin_string: str = bin(message_blocks[a])[2:]
        current_string: str = ""
        while len(bin_string) >= 8:
            current_string = chr(
                int(bin_string[len(bin_string) - 8:len(bin_string)], 2)) + current_string
            bin_string = bin_string[:len(bin_string) - 8]
        if len(bin_string) > 0:
            current_string = chr(int(bin_string, 2)) + current_string
        final_list.append(current_string)
        a += 1
    return "".join(final_list)

# encrypt a block of messages using a public key


def encrypt(message_blocks: list[int]) -> list[tuple[int, int]]:
    final_list: list[tuple[int, int]] = []
    j: int = random.randrange(2, p - 1)
    for B in message_blocks:
        # if you want to encrypt something and then descrypt it uself, swap a for public_key
        final_list.append((pow(g, j, p), (pow(a, j, p) * B) % p))
    return final_list

# decrypted an encrypted block of numbers that represent messages


def decrypt(encrypted_messages: list[tuple[int, int]]) -> str:
    decrypted_list: list[int] = []
    index: int = 0
    while index < len(encrypted_messages):
        decrypted_list.append((encrypted_messages[index][1] * pow(
            encrypted_messages[index][0], (p - 1 - private_key), p)) % p)
        index += 1
    return message_blocks_to_message(decrypted_list)


# create a private key and a public key and a message, save the output of this program as every time it runs is generates new keys
message = "why was 6 afraid of 7? cause 7 8 0 "
print("The plain text message is:\n" + message)
private_key = random.randrange(2, p - 1)
print(f"The private key is:\n{private_key}")
public_key = pow(g, private_key, p)
print("SEND EVERYTHING AFTER THIS LINE TO JOHN. DO NOT SEND ANYTHING ABOVE. REWRITE THE LINE BELOW IN YOUR OWN WORDS, AND REWRITE THE PUBLIC KEY LINE IN YOUR OWN WORDS AS WELL.")
# encrypt my message using john's public key, send him the result of the encrypted stuff so that he can decrypt it
encrypted_message: list[tuple[int, int]] = encrypt(
    make_message_blocks(message))
print("Here is the encrypted message. It is in the format c1, c2, where c2 is the number with raw message number packed into it. ")
for a in encrypted_message:
    print(f"{a[0]}, {a[1]}")

print(f"The public key that corresponds to the private key I have generated is:\n{public_key}")
# when it is time to decrypt a message, load the message he sends into format used by decrypt, a list of tuple consisting of c1, c2
