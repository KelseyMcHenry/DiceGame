class SpriteContainer:

    def __init__(self):
        self.container = dict()

    def __str__(self):
        str_val = ''
        for k, v in self.container.items():
            str_val += k + ' :\n'
            for item in v:
                str_val += '\t'
                str_val += str(item).replace('\n', '\n\t')
                if v.index(item) != (len(v) - 1):
                    str_val += '\n'
            str_val += '\n'
        return str_val

    def add(self, sprite):
        sprite_type = type(sprite).__name__
        try:
            self.container[sprite_type].append(sprite)
        except KeyError:
            self.container[sprite_type] = list()
            self.container[sprite_type].append(sprite)

    def remove(self, sprite):
        sprite_type = type(sprite).__name__
        try:
            self.container[sprite_type].remove(sprite)
            if len(self.container[sprite_type]) == 0:
                del self.container[sprite_type]
        except KeyError:
            return

    def get_subset(self, sprite_type):
        try:
            return self.container[sprite_type]
        except KeyError:
            return list()

    def get_all(self):
        temp_value = list()
        for k, v in self.container.items():
            temp_value.extend(v)
        return temp_value
