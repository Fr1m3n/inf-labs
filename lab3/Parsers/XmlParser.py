import re


class XmlParser:
    def __init__(self):
        OPTIONS = re.DOTALL
        self.opened_token_regexp = re.compile(r'<([0-9a-zA-Z]+)( *[0-9a-zA-Z]+=\"[^\"]*\")*>', OPTIONS)
        self.self_closed_token_regexp = re.compile(r'<([0-9a-zA-Z]+)( *[0-9a-zA-Z]+=\"[^\"]*\")*/>', OPTIONS)
        self.comment_regexp = re.compile(r'<!--[0-9a-zA-Z ]*-->', OPTIONS)
        self.attributes_regexp = re.compile(r'[0-9a-zA-Z]+=\"[^\"]*\"', OPTIONS)
        self.default_token_regexp = re.compile(r"<([0-9a-zA-Z]+)( *[0-9a-zA-Z]+=\"[^\"]*\")*>(?P<inner>.*)</\1>", OPTIONS)

    def parse_args(self, args):
        for group in args:
            key, value = group.split("=")
            value = value[1:-1]
            # print(value)
            yield key, value

    def get_self_closed_token(self, s):
        s = s.strip()
        g = self.self_closed_token_regexp.match(s)
        if g is None:
            return None
        # print(s, g.groups(), g.string[:g.end()])
        name = g.groups()[0]
        groups = g.groups()[1]
        # print(groups)
        args = self.attributes_regexp.findall(g.string[:g.end()])
        values = {}
        if args is not None:
            for key, value in self.parse_args(args):
                values[key] = value
        return name, values, s[g.end():].strip()

    def get_default_token(self, s):
        s.strip()
        g = self.default_token_regexp.match(s)
        # print(s, g)
        if g is None:
            return None
        # print(g)

        dictt = g.groupdict()
        # print("dict", dictt)
        values = self.parse(dictt["inner"].strip())[0]
        args = s.split('>')[0].split()[1:]
        if len(args) > 0:
            if str(type(values)) == "<class 'str'>":
                values = {
                    "text": values
                }
            for key, value in self.parse_args(args):
                values[key] = value
        return g.groups()[0], values, s[g.end():].strip()

    def parse(self, src):
        res = {}
        if src == '':
            return None
        while src != '':
            # print(src)
            temp = self.get_self_closed_token(src)
            if temp is not None:
                key, value, src = temp
                res[key] = value
                continue
            temp = self.get_default_token(src)
            # print(temp)
            if temp is not None:
                key, value, src = temp
                res[key] = value
                continue
            temp = self.comment_regexp.match(src)
            if temp is not None:
                src = src[temp.end():].strip()
                continue
            return src, ''
        return res, src.strip()


if __name__ == "__main__":
    parser = XmlParser()
    print(parser.parse('''
            <!-- hoooooy -->

    <a>
        <b qwe="zxcvv" xxxx="zzz1">
            cx asd
        </b>
        <c z="q "/>
        <d q="zc"/>
    </a>
    '''.strip())[0])
