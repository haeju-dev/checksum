class checksum_input:
    def __init__(self, dir='input.dat', stuff_bit=16):
        inputfile = open(dir, 'r')
        raw = inputfile.read().upper()
        inputfile.close()
        self.stuff_bit = stuff_bit
        self.raw = raw
        self.stuffed = self.bitstuffing(raw=self.raw, stuff_bit=self.stuff_bit)
        self.exported = self.export_16bit()

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
        for i in range(int(len(raw) / (self.stuff_bit / 4)) - 1):
            token = raw[int(i * (self.stuff_bit / 4)): int((i + 1) * (self.stuff_bit / 4))]
            exported.append(token)
        return exported

    def __str__(self):
        return self.bitstuffing(self.raw)


class bittoken:
    def __init__(self, raw):
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
        if len(str(new)) > 4: # Carry
            carrier = checksum_number(str(new)[:-4])
            new = checksum_number(str(new)[-4:])
            return new + carrier
        return checksum_number(self.data + other.data)


class checksum:
    def __init__(self, raw, stuff_bit=16):
        self.raw = raw
        self.stuff_bit = stuff_bit

    @staticmethod
    def getchecksum(data, stuff_bit):
        cs = ''
        return cs


if __name__ == "__main__":
    stuff_bit = 16
    input_dir = 'input.dat'

    input_raw = checksum_input(dir=input_dir, stuff_bit=stuff_bit)
    exported = input_raw.export_16bit()
    # tmp = [token_16bit(exported[0]), token_16bit(exported[1])]
    btmp = [checksum_number('8888'), checksum_number('9999')]
    newbtmp = btmp[1] + btmp[0]
    # tmpp = [tmp[0].export(mode='int'), tmp[1].export(mode='hexstr')]
    print()
