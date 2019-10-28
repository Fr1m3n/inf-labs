import re
import string
import random


class XmlParser:
    def __init__(self):
        OPTIONS = re.DOTALL
        self.opened_token_regexp = re.compile(r'<([0-9a-zA-Z]+)( *[0-9a-zA-Z]+=\"[^\"]*\")*>', OPTIONS)
        self.self_closed_token_regexp = re.compile(r'<([a-zA-Z]+:[0-9a-zA-Z]+)( *[0-9a-zA-Z]+=\"[^\"]*\")*/>', OPTIONS)
        self.comment_regexp = re.compile(r'<!--[0-9a-zA-Z ]*-->', OPTIONS)
        self.attributes_regexp = re.compile(r'[0-9a-zA-Z]+=\"[^\"]*\"', OPTIONS)
        self.default_token_regexp = re.compile(
            r"<([a-zA-Z]+:[0-9a-zA-Z]+)( *[0-9a-zA-Z]+=\"[^\"]*\")*>(?P<inner>.*)<\/\1>", OPTIONS)

    # генератор, который парсит параметры тэга типа <key>="<value>"
    def parse_args(self, args):
        for group in args:
            key, value = group.split("=")
            value = value[1:-1]
            yield key, value

    # получает имя и содержимое самозакрываемого тэга <tag/> так же возвращает строку без этого тэга
    def get_self_closed_token(self, s):
        s = s.strip()
        g = self.self_closed_token_regexp.match(s)
        if g is None:
            return None
        name = g.groups()[0]
        args = self.attributes_regexp.findall(g.string[:g.end()])
        values = {}
        if args is not None:
            for key, value in self.parse_args(args):
                values[key] = value
        return name.split(':')[0], values, s[g.end():].strip()

    # получает имя и содержимое блока, который закрыт тэгами вида <s> </s> так же возвращает строку без блока
    def get_default_token(self, s):
        s.strip()
        g = self.default_token_regexp.match(s)
        if g is None:
            return None
        values = self.parse_block(g.groupdict()["inner"].strip())[0]
        args = s.split('>')[0].split()[1:]
        if len(args) > 0:
            if str(type(values)) == "<class 'str'>":
                values = {
                    "text": values
                }
            for key, value in self.parse_args(args):
                print(key, value)
                values[key] = value
        return g.groups()[0].split(':')[0], values, s[g.end():].strip()

    # метод, который обобщает выше описанные
    # вызывает по очереди методы для разных тэгов
    # если ни один не сработал, значит вернём как строку внутри тэга
    def parse_block(self, src):
        res = {}
        if src == '':
            return {}, ''
        while src != '':
            temp = self.get_self_closed_token(src)
            if temp is not None:
                key, value, src = temp
                res[key] = value
                continue
            temp = self.get_default_token(src)
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

    def make_tokens_unique(self, s):
        identifier_length = 5
        ss = ''
        stack = []
        for _token in s.split("<"):
            if len(_token) == 0:
                continue
            is_closed = _token[0] == "/"
            token = _token.split(">")[0].split()[0][int(is_closed):]
            new_token = token + ':' + self.rand_str(identifier_length)
            if is_closed:
                if token == stack[-1].split(':')[0]:
                    new_token = '/' + stack.pop()
                else:

                    raise RuntimeError("Xml invalid. token: ")
            else:
                if _token.split(">")[0][-1] != '/':
                    stack.append(new_token)
            ss += '<' + new_token + _token[len(token) + int(is_closed):]
        if len(stack) != 0:
            raise RuntimeError("Xml not valid. Not all tags closed.")
        return ss

    # интерфейс для пользователя
    # принимает строку
    # возвращает словарь
    def parse(self, s):
        return self.parse_block(self.make_tokens_unique(s))[0]

    # возвращает случайную строку из length символов [a-zA-z]
    def rand_str(self, length):
        letters = string.ascii_letters
        return ''.join([random.choice(letters) for i in range(length)])


if __name__ == "__main__":
    parser = XmlParser()
    s = open("../p3112shedule.xml", "r").read()
    print(parser.parse('<aqwe q="z"/>'))
    print(parser.parse(s))
