class checksum_input:
    def __init__(self, raw, stuff_bit=16):
        self.stuff_bit = stuff_bit
        self.raw = ''
        for i in filter(self.filter_word, raw):
            self.raw += i
        self.stuffed = self.bitstuffing(raw=self.raw, stuff_bit=self.stuff_bit)
        self.exported = self.export_16bit()

    @staticmethod
    def filter_word(character):
        NUMBERS = ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F',
                   '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if character in NUMBERS:
            return True
        else:
            return False

    def bitstuffing(self, raw=None, stuff_bit=None):
        if stuff_bit is None:
            stuff_bit = self.stuff_bit
        if raw is None:
            stuffed = str(self.raw)
        else:
            stuffed = str(raw)
        rest = int(len(stuffed) % (stuff_bit / 4))
        if rest != 0:
            for i in range(int(stuff_bit / 4) - rest):
                stuffed += '0'
        return stuffed

    def export_16bit(self):
        raw = str(self)
        exported = list()
        for i in range(int(len(raw) / (self.stuff_bit / 4))):
            token = raw[int(i * (self.stuff_bit / 4)): int((i + 1) * (self.stuff_bit / 4))]
            exported.append(checksum_number(raw=token, stuff_bit=self.stuff_bit))
        return exported

    def __str__(self):
        return self.bitstuffing(self.raw)


class bittoken:
    def __init__(self, raw=0, stuff_bit=16):
        self.stuff_bit = stuff_bit
        if type(raw) is type(str()):
            self.rawstr = raw.lstrip("0x").lstrip("0")
            self.data = self.export(mode='int', data=raw)

        elif type(raw) is type(int()):
            self.data = raw
            self.rawstr = self.export(mode='hexstr')

        else:
            raise Exception('Input Data Type is wrong')

    def export(self, mode, data=None):
        if data is None:
            data = self.data
        if mode == 'int':
            return int(str(data), 16)
        if mode == 'hexstr':
            return hex(self.data)[2:].upper()

    def __str__(self):
        return self.export(mode='hexstr')

    def __add__(self, other):
        # new = self.data + other.data
        return bittoken(self.data + other.data)


class checksum_number(bittoken):
    def __add__(self, other):
        new = checksum_number(self.data + other.data)
        if len(str(new)) > 4:  # Carry
            carrier = checksum_number(str(new)[:-1 * int(self.stuff_bit / 4)])
            new = checksum_number(str(new)[-1 * int(self.stuff_bit / 4):])
            return new + carrier
        return checksum_number(self.data + other.data)


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
        self.sum = checksum_number(cs.data)
        cs = checksum_number(int("F" * int(self.stuff_bit / 4), self.stuff_bit) ^ cs.data)
        return cs

    def export(self):
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
