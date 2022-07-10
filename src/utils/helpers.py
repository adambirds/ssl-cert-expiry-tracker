from typing import Any, Dict

import yaml


def process_config_file() -> Dict[str, Any]:

    with open("config.yaml", "r") as stream:
        config_options = yaml.safe_load(stream)

    return config_options
