import random
# both ways stuff
p: int = 808241878912418587664668869752380201227471917587049402831353579654087934716257177583988001816750842723486468130003910337833297294744103045277794137039348379685305766000049233920274403424909809118398706373176342402680527597912453031947055263965574521088574747656702199527971035049821214553730158203939
g: int = 2

# nevards public key
a: int = 455848071374707988038292715962272655511109957743547844562644188078424249523058593328745877427412302513863218445493774359827883299407761443769628022340049190244708960432307664952518902871204598305338226446449763051563904730839041083188049120606722799230110813191873851538379238410155389668523135874520

# my private key
private_key: int = 103011687869025962938928581392454646913888320358058107007013214592943394893600843706555430866101403805500468594293363551417065855504377689726869263349230962223056262241682559158559471202130897968724088885318548014335612047339112293175474246206940925747986708262498155968303127474846337858464828170526
# my public key
public_key: int = 758048007388692678051507134925220147949193210592171917492886415049292890408600729304845356456379007068998106141757681688120537472649113820008264554026611845089693977721029362780526767792997143297924494233690208588085357392567928582289215093295258969125467405944520593705719666381621302537173748806787


plain_text: str = "The German motor company, BMW, has offered their customers a wide selection of different luxury and performance cars. From sedans, to SUVs, to coupes, and hatchbacks, BMW has many different series options, trims, and models to offer to the luxury and performance vehicle market. However, one specific car stands out from the others. The sport or performance model of their 4 series, 2 door coupe, called the M4 (the M represents the BMW M power performance line, while the 4 represents the series of the car) really shines because as a powerful performance vehicle, built to seamlessly handle at high speeds. BMW has produced two generations of the M4: one built on the F82 chassis, and one built on the G82 chassis. The focus of this paper will be on the first generation F82 model. The F82 M4 proved itself not only through statistics, numbers, and horsepower, but through its consistent, powerful performance in the real world, both on the streets and on the track."


def mod_exp(base: int, exp: int, power: int) -> int:
    x: int = 1
    y: int = base
    while exp > 0:
        if exp % 2 != 0:
            x = (x * y) % power
        y = (y * y) % power
        exp = int(exp / 2)

    return x % power



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


def encrypt(message_blocks: list[int]) -> list[tuple[int, int]]:
    final_list: list[tuple[int, int]] = []
    j: int = random.randrange(2, p - 1)
    for B in message_blocks:
        # todo remember to swap the public key here
        final_list.append((mod_exp(g, j, p), B * mod_exp(public_key, j, p)))
    return final_list


def decrypt(encrypted_messages: list[tuple[int, int]]) -> str:
    decrypted_list: list[int] = []
    index: int = 0
    while index < len(encrypted_messages):
        decrypted_list.append(mod_exp(encrypted_messages[index][1] * encrypted_messages[index][0], (p - 1 - private_key), p))
        index += 1
    return message_blocks_to_message(decrypted_list)

# print(message_blocks_to_message(make_message_blocks(plain_text)))

encrypted_message = encrypt(make_message_blocks(plain_text))
decrypted_message = decrypt(encrypted_message)

print(decrypted_message)
