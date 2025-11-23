import ION
import io
from ruamel.yaml import YAML
yml = YAML(typ="safe")
Translate_yml = ION.R_code
def loads(ioncode):
    return yml.load(Translate_yml(ioncode))
def dumps(datadict):
    with io.StringIO() as string_stream:
        yml.dump(datadict, string_stream)
        return string_stream.getvalue()
def load(ionfile):
    with open(ionfile, "r") as f:
        return loads(f.read())
def dump(datadict, ionfile):
    ioncode = dumps(datadict)
    with open(ionfile, "w") as f:
        f.write(ioncode)