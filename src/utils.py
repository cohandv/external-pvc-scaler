import os
import configparser


def parse_bool(value: str):
    return value.lower() in ['true', '1', 't', 'y', 'yes']


def config_reader():
    """
    Reads the config files merging values
    :return: a config parser already parsed
    """
    parser = configparser.ConfigParser(default_section='default')
    config_file = os.getenv("EXTERNAL_PVC_SCALER_CONFIG_FILE", "./config.ini")
    default_config_file = os.getenv("EXTERNAL_PVC_SCALER_DEFAULT_CONFIG_FILE", "./default.ini")
    parser.read(default_config_file)
    parser.read(config_file)
    return parser
