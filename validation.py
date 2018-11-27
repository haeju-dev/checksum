from checksum import checksum_input
from checksum import checksum_number


def valid_check(data, stuff_bit=16):
    input_class = checksum_input(data['data'], stuff_bit=stuff_bit)
    sum = checksum_number()
    for i in input_class.exported:
        sum += i
    sum += checksum_number(data['checksum'])
    cs = sum.data ^ int("FFFF", 16)
    return not cs


if __name__ == "__main__":
    check = valid_check({'data': '0019E77A753F001ECDA380019E77A3F1ECDA30350028', 'sum': 'A38', 'checksum': 'F5C7'})
    print('0019E77A753F001ECDA380019E77A3F1ECDA30350028 : F5C7 : ' + str(check))
    check = valid_check({'data': '0019E77A753F001ECDA380019E77A3F1ECDA30350028', 'sum': 'A38', 'checksum': 'F5C8'})
    print('0019E77A753F001ECDA380019E77A3F1ECDA30350028 : F5C8 : ' + str(check))
    check = valid_check({'data': '0019E77A753F001ECDA380019E77A3F1ECDA30350128', 'sum': 'A38', 'checksum': 'F5C7'})
    print('0019E77A753F001ECDA380019E77A3F1ECD30350028 : F5C7 : ' + str(check))
    print()
