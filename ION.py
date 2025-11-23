"""
syntax

value:key
numbers (1,23,4.2)
str ("hello")
bool (true)
list [1, 2, 3, "four", false]
null

example.ion (comprimed)

("ion":("syntax":[value:key","numbers (1,23,4.2)","str (\\"hello\\")","bool (true)","list [1, 2, 3, \\"four\\", false]","null"]))

example.json (output)

{"ion":{"syntax":[value:key","numbers (1,23,4.2)","str (\\"hello\\")","bool (true)","list [1, 2, 3, \\"four\\", false]","null"]}}
"""

import sys, re, json, random, ruamel.yaml as yaml, os
yml = yaml.YAML(typ="rt")
def info():
    print("Ion - Ian Object Notation")
    code = R_code()
    print(code)
def version():
    code = R_code()
    version = re.findall(r'"version":\s*([\d\.]+)', code)
    if version:
        print(f"Ion version {version[0]}")
    else:
        print("Version not found")
def R_code():
    with open(sys.argv[1], "r") as f:
        code = f.read()
    def maybe(m):
        prob = random.uniform(0.0, 1.0)
        if prob < 0.5:
            return "false"
        elif prob > 0.5:
            return "true"
        else:
            return "null"
    def opbool(m):
        if m.group(1) == m.group(2):
            return f"{m.group(1)}"
            
        for o,t in [[1,2], [2,1]]:
                
            if m.group(o) == "true" and m.group(t) == "false":
                return "null"
                
            if m.group(o) == "null":
                return "false"
    def calc(m):
        return str(eval(f"{m.group(1)} {m.group(2)} {m.group(3)}"))
    code = re.sub(r"(-?\d*\.?\d+)\s*([-+*/])\s*(-?\d*\.?\d+)", calc, code)
    code = re.sub("maybe", maybe, code)
    code = re.sub(r"(true|false|null) \$ (true|false|null)", opbool, code)
    code = re.sub(r"\t|    ", "  ", code)
    return code


def F_yml():
    code = R_code()
    
    with open("cache.icache", "w") as f:
        f.write(code)
    with open("cache.icache", "r") as f:
        dcode = yml.load(f)
    try:
        
        with open(sys.argv[1].split(".")[0] + ".yml", "w") as f:
            yml.dump(dcode, f)
    except Exception as e:
        exit(f"Invalid Ion syntax: {e}")
    finally:
        os.remove("cache.icache")

def F_json():
    code = R_code()
    with open("cache.icache", "w") as f:
        f.write(code)
    with open("cache.icache", "r") as f:
        dcode = yml.load(f)
    try:
        with open(sys.argv[1].split(".")[0] + ".json", "w") as f:
            f.write(json.dumps(dcode, indent=2))
    except Exception as e:
        exit(f"Invalid Ion syntax: {e}")
    finally:
        os.remove("cache.icache")
        
def translate():
    code = R_code()
    try:
        with open("cache.icache", "w") as f:
            f.write(code)
        with open("cache.icache", "r") as f:
            dcode = yaml.YAML(typ="rt").load(f)
        print("Valid Ion syntax")
        print(code)
    except Exception as e:
        exit(f"Invalid Ion syntax: {e}")
fns = {
     "-yml": F_yml,
     "-json": F_json,
     "-t": translate,
     "--info": info,
     "--version": version
 }

if __name__ == "__main__":
    if not len(sys.argv) == 3:
        raise Exception("Invalid number of arguments")
    if sys.argv[2] in fns:
        fns[sys.argv[2]]()
    else:
        raise Exception("Invalid option")