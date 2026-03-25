from configparser import ConfigParser
def load_config():
    parser = ConfigParser()
    parser.read('database.ini')
    config = {}
    if parser.has_section('postgresql'):
        for item in parser.items('postgresql'):
            config[item[0]] = item[1]
    else: raise Exception("Section postgresql was not found in database.ini file")
    return config
if __name__=='__main__':
    config = load_config()
    print(config)