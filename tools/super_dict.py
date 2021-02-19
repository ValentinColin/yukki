import yaml

class my_dict(dict):
    """Surcouche des dictionnaire."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        ret = super().__getitem__(key)
        if isinstance(ret, dict):
            ret = my_dict(ret)
        return ret

    # Todo:
    def __setitem__(self, key, value):
        with open("data/yaml/todo.yml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            data[key] = value
        with open("data/yaml/todo.yml", "w") as f:
            yaml.dump(super_data, f)
        if isinstance(super_data[key], my_dict):
            pass
        super().__setitem__(key, value)

    # Todo:
    def __delitem__(self, key):
        with open("data/yaml/todo.yml") as f:
            super_data = my_dict(yaml.load(f, Loader=yaml.FullLoader))
            del super_data[key]
        with open("data/yaml/todo.yml", "w") as f:
            yaml.dump(super_data, f)
        super().__delitem__(key)
