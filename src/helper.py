import configparser
import json



def generate_message(input):
    msg = "There is a request for a new data source -- " + input


def update_conf(section, myobject):
    config_path = "C:\\Users\mikea\Desktop\Developer\Projects\Work\RDBMS_WebApp\\rdbms_ingestor\src\config.ini"

    config = configparser.ConfigParser()
    config.read(config_path)

    if config.has_section(section):
        ## Call the update instead
        print("This section already exists")
    else:

        config[section] = myobject
        with open(config_path, 'w') as configfile:
            config.write(configfile)

