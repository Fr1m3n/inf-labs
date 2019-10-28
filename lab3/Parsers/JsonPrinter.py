class JsonPrinter:
    def print(self, obj, depth=0, start_step=0):
        # res = '\t' * depth
        if type(obj) is str:
            try:
                return str(int(obj))
            except ValueError as e:
                return '"{}"'.format(obj)
        if type(obj) is list:
            res = ','.join([self.print(i, depth + 1, int(not bool(j))) for j, i in enumerate(obj)])
            return '[\n'+ res + '\n' + '\t' * depth + ']'
        res = '\t' * depth * start_step + '{\n'
        for i, j in enumerate(obj.keys()):
            # print(i, obj[i], obj)
            # print(i, j,  len(obj.keys()) - 1)
            res += ('\t' * (depth + 1) + '"{}": {}\n'.format(j, self.print(obj[j], depth + 1) + (',' if i != len(obj.keys()) - 1 else '')))
        return res + '\t' * depth + '}'
