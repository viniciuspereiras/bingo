import yaml

def load_config(filename: str) -> dict:
    return yaml.load(open(filename), Loader=yaml.FullLoader)


