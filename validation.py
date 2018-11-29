from checksum import checksum_input
from checksum import checksum_number


def valid_check(data, stuff_bit=16):
    input_class = checksum_input(data['data'], stuff_bit=stuff_bit)
    sum = checksum_number()
    for i in input_class.exported:
        sum += i
    sum += checksum_number(data['checksum'])
    # sum.data를 지정된 길이만큼의 비트를 1로 지정한 데이터와 xor연산을 한다
    cs = sum.data ^ int("F" * int(stuff_bit / 4), stuff_bit)
    return not cs  # cs 값이 0이어야만 1을 반환한다


if __name__ == "__main__":
    check = valid_check({'data': '0019E77A753F001ECDA380019E77A3F1ECDA30350028', 'sum': 'A38', 'checksum': 'F5C7'})
    print('0019E77A753F001ECDA380019E77A3F1ECDA30350028 : F5C7 : ' + str(check))
    check = valid_check({'data': '0019E77A753F001ECDA380019E77A3F1ECDA30350028', 'sum': 'A38', 'checksum': 'F5C8'})
    print('0019E77A753F001ECDA380019E77A3F1ECDA30350028 : F5C8 : ' + str(check))
    check = valid_check({'data': '0019E77A753F001ECDA380019E77A3F1ECDA30350128', 'sum': 'A38', 'checksum': 'F5C7'})
    print('0019E77A753F001ECDA380019E77A3F1ECD30350028 : F5C7 : ' + str(check))
    print()
