CONFIG_FILE = 'string_config.ini'


def read_config():

    atmo_config = []
    bio_config = []
    temp_config = []
    tl_config = []

    current_config = None
    config_table = {'atmosphere': atmo_config,
                    'biosphere': bio_config,
                    'temperature': temp_config,
                    'tech level': tl_config}

    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            if len(line) == 0:
                continue
            if line[0] == '[' and line[-2] == ']':
                current_config = config_table[line[1:-2]]
            else:
                current_config.append(line.rstrip('\n'))

    return config_table
