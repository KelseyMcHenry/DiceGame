import os

PATH_TO_SETTINGS = 'C:\\Users\\d5ffpr\\PycharmProjects\\TinkerTactics\\Settings.dat'


class Settings:

    settings = dict()

    def __init__(self):
        with open(PATH_TO_SETTINGS, 'r') as file:
            line = file.readline()
            while line:
                if '=' in line:
                    key = line[:line.index('=')-1]
                    value = line[line.index('=') + 2:].strip()
                    # dict parsing
                    if value[0] == '{' and value[-1] == '}':
                        temp_dict = dict()
                        for pair in value[1:-1].split(','):
                            new_pair = tuple(pair.split(': '))
                            temp_dict[int(new_pair[0])] = int(new_pair[1])
                        value = temp_dict
                    elif value[0] == '(' and value[-1] == ')':
                        value = tuple(value[1:-1].split(', '))
                        value = tuple([int(v) for v in value])
                    self.settings[key] = value
                line = file.readline()

    def vals(self):
        return self.settings

