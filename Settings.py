GAME_NAME = 'name'
BACKGROUND_COLOR_RGB = 'background_color_RGB'
HIGHLIGHT_COLOR_RGB = 'highlight_color'
HIGHLIGHT_THICKNESS = 'highlight_thickness'
FONT = 'font'
FONT_SIZE = 'font_size'
RESOLUTION = 'resolution'
PIECE_SIZE_PX = 'piece_size_px'
PIECE_RANK_AND_COUNT = 'piece_rank_and_count'
TEAM_1_NAME = 'team_1_name'
TEAM_1_RGB = 'team_1_RGB'
TEAM_2_NAME = 'team_2_name'
TEAM_2_RGB = 'team_2_RGB'

# TODO add path to sprites
# TODO see if you can just straight return the dict


class SettingsPackage:

    settings = dict()

    def __init__(self):
        filepath_list = __file__.split('/')
        filepath_list[-1] = 'Settings.dat'
        filepath = '/'.join(filepath_list)
        try:
            with open(filepath, 'r') as file:
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
                        # tuple parsing
                        elif value[0] == '(' and value[-1] == ')':
                            value = tuple(value[1:-1].split(', '))
                            value = tuple([int(v) for v in value])
                        self.settings[key] = value
                    line = file.readline()
        except FileNotFoundError:
            default_settings = ['name = Tinker Tactics',
                                'resolution = (1200, 800)',
                                'background_color_RGB = (230, 230, 230)',
                                'piece_rank_and_count = {4: 2, 6: 2, 8: 1}',
                                'team_1_color_name = red',
                                'team_1_color_RGB = (255, 0, 0)',
                                'team_2_color_name = blue',
                                'team_2_color_RGB = (0, 0, 255)',
                                'font = Arial',
                                'font_size = 40',
                                'piece_size = 75',
                                'highlight_color = (255, 255, 0)',
                                'highlight_thickness = 5']
            with open(filepath, 'w') as file:
                file.write('\n'.join(default_settings))
            with open(filepath, 'r') as file:
                line = file.readline()
                while line:
                    if '=' in line:
                        key = line[:line.index('=') - 1]
                        value = line[line.index('=') + 2:].strip()
                        # dict parsing
                        if value[0] == '{' and value[-1] == '}':
                            temp_dict = dict()
                            for pair in value[1:-1].split(','):
                                new_pair = tuple(pair.split(': '))
                                temp_dict[int(new_pair[0])] = int(new_pair[1])
                            value = temp_dict
                        # tuple parsing
                        elif value[0] == '(' and value[-1] == ')':
                            value = tuple(value[1:-1].split(', '))
                            value = tuple([int(v) for v in value])
                        self.settings[key] = value
                    line = file.readline()

    def get_package(self):
        return self.settings

