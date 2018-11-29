class checksum_input:
    def __init__(self, raw, stuff_bit=16):
        self.stuff_bit = stuff_bit
        self.raw = ''
        # filter_word로 true가 반환된 문자들만 다시 저장한다
        for i in filter(self.filter_word, raw):
            self.raw += i

        # Bit Stuffing
        self.stuffed = self.bitstuffing(raw=self.raw, stuff_bit=self.stuff_bit)
        # Make List of checksum_number Class
        self.exported = self.export_16bit()

    @staticmethod
    def filter_word(character):
        NUMBERS = ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F',
                   '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        # 입력받은 문자가 위 숫자표에 있으면 True
        if character in NUMBERS:
            return True
        else:
            return False

    def bitstuffing(self, raw=None, stuff_bit=None):
        # method의 default value setting
        if stuff_bit is None:
            stuff_bit = self.stuff_bit
        if raw is None:
            stuffed = str(self.raw)
        else:
            stuffed = str(raw)
        # 나머지부분이 존재하는지 검사한다
        rest = int(len(stuffed) % (stuff_bit / 4))
        if rest != 0:
            # 나머지 부분이 0이 아니면
            for i in range(int(stuff_bit / 4) - rest):
                # 0으로 보충한다
                stuffed += '0'
        return stuffed

    def export_16bit(self):
        raw = str(self)
        exported = list()
        for i in range(int(len(raw) / (self.stuff_bit / 4))):
            # token은 매 루프마다 4글자씩 쪼개어진 String 형 변수가 된다
            token = raw[int(i * (self.stuff_bit / 4)): int((i + 1) * (self.stuff_bit / 4))]
            # token의 String 값을 checksum_number 클래스에 입력하여 리스트에 추가한다
            exported.append(checksum_number(raw=token, stuff_bit=self.stuff_bit))
        return exported

    def __str__(self):
        return self.bitstuffing(self.raw)


class bittoken:
    def __init__(self, raw=0, stuff_bit=16):
        self.stuff_bit = stuff_bit
        # 입력 type이 string일 경우
        if type(raw) is type(str()):
            # 앞의 0x 또는 0이 존재한다면 잘라낸다
            self.rawstr = raw.lstrip("0x").lstrip("0")
            # 정수형으로 변환해 data 라는 클래스 내부 변수에 저장한다
            self.data = self.export(mode='int', data=raw)

        # 입력 type이 integer일 경우
        elif type(raw) is type(int()):
            # 정수형이므로 그냥 저장한다
            self.data = raw
            # string 자료형으로 변환해 클래스 내부 변수를 초기화한다
            self.rawstr = self.export(mode='hexstr')

        # 입력 type이 다를 경우에 대한 예외 처리
        else:
            raise Exception('Input Data Type is wrong')

    def export(self, mode, data=None):
        # parameter data의 default value setting
        if data is None:
            data = self.data
        if mode == 'int':
            # string 데이터를 16비트 integer형으로 저장한다
            return int(str(data), self.stuff_bit)
        if mode == 'hexstr':
            # integer 데이터를 16진수 string 자료형으로 변환하고 대문자로 변환해 반환한다
            return hex(self.data)[2:].upper()

    def __str__(self):
        # str() 함수로 이 클래스를 호출할 경우 반환할 데이터를 override
        return self.export(mode='hexstr')

    def __add__(self, other):
        # + 연산자를 override 한다
        # 덧셈을 할 경우 클래스 내부 변수 data끼리 더한 값을 입력한 새로운 bittoken class를 반환한다
        return bittoken(self.data + other.data)


class checksum_number(bittoken): # bittoken 이라는 연산 담당 클래스를 상속받는다
    def __add__(self, other):
        new = checksum_number(self.data + other.data)
        # Carry가 발생하면 bittoken 클래스의 __str__ method override에 의해 길이가 4가 넘는다
        if len(str(new)) > 4:
            carrier = checksum_number(str(new)[:-1 * int(self.stuff_bit / 4)])
            new = checksum_number(str(new)[-1 * int(self.stuff_bit / 4):])
            # 리턴 시 덧셈 연산을 진행하는데, 덧셈 연산을 override하는 코드이므로 재귀호출이 발생할 수 있다
            return new + carrier
        # Carry가 없을 경우 새로운 checksum_number에 정수 데이터를 더한 값을 입력해 반환한다
        return new


class checksum:
    def __init__(self, raw, stuff_bit=16):
        self.raw_input_class = checksum_input(raw, stuff_bit=stuff_bit)
        self.stuff_bit = stuff_bit
        self.sum = checksum_number()
        self.cs = self.getchecksum(self.raw_input_class.exported)

    def getchecksum(self, data):
        cs = checksum_number()
        for i in data:
            cs += i
        # sum에 물리적으로 다른 위치에 저장된 checksum_number 를 저장한다
        self.sum = checksum_number(cs.data)
        # 모두 1로 채운 데이터와의 xor 연산으로 (둘중 하나만 참이어야 1) 보수를 취해준다
        cs = checksum_number(int("F" * int(self.stuff_bit / 4), self.stuff_bit) ^ cs.data)
        return cs

    def export(self):
        # JSON에 대응하는 Python Dictionary로 데이터와 sum, checksum을 반환한다
        return {'data': str(self.raw_input_class.raw), 'sum': str(self.sum), 'checksum': str(self.cs)}


if __name__ == "__main__":
    # Basic Settings
    input_dir = 'input.dat'
    stuff_bit = 16

    # Input Data
    inputfile = open(input_dir, 'r')
    raw = inputfile.read().upper()
    inputfile.close()

    # Get Checksum
    cs_class = checksum(raw=raw, stuff_bit=stuff_bit)
    cs = cs_class.export()
    print(cs)

    # Validation
    from validation import valid_check

    is_valid = valid_check(data=cs, stuff_bit=stuff_bit)
    print(is_valid)

    # input_class = checksum_input(raw=raw, stuff_bit=stuff_bit)
    # exported = input_class.export_16bit()
    # cs_sum = checksum_number()
    # for i in exported:
    #     cs_sum += i

    print()
