from pathlib import Path
from typing import List, Dict
import uuid
from numpy import int32
import sys
import json

def GetArg(arg:int, fallback:any)->any:
	if len(sys.argv) > arg:
		val = sys.argv[arg]
		if val != None:
			return val
	return fallback

def load_file(path:Path):
    try:
        if path.exists():
            f = open(path, 'r', encoding='utf-8')
            contents = f.read()
            f.close()
            return contents
    except Exception as e:
        print("Erroring reading '{}': {}".format(path.name, e))
    return None

def export_file(path:Path, contents):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        f = open(str(path.absolute()), 'w', encoding='utf-8')
        f.write(contents)
        f.close()
        return True
    except Exception as e:
        print("Erroring writing '{}': {}".format(path.name, e))
    return False

def is_empty(line):
    return line in ['\n', '\r\n']

def clipboard_copy(output_str):
    import pyperclip
    pyperclip.copy(output_str)

def GetAttributeNodeValue(xml, id:str, fallback:str="")->str:
    v = xml.find("attribute", attrs={"id":id})
    if v is not None:
        try:
            inner = v["value"]
            return inner
        except: pass
    return fallback

def GetEnglishLocalization(path:str)-> Dict[str,str]:
    from bs4 import BeautifulSoup
    english_entries = {}
    f = open(path, 'r', encoding='utf8')
    english_xml = BeautifulSoup(f.read(), 'lxml')
    f.close()
    content_nodes = list(english_xml.find_all("content"))
    for node in content_nodes:
        try:
            handle = node["contentuid"]
            contents = node.text
            english_entries[handle] = contents
        except Exception as e:
            print("Error parsing content node: \n{}".format(e))
    return english_entries

def NewUUID()->str:
    return str(uuid.uuid4())

def NewHandle()->str:
    return "h"+str.replace(str(uuid.uuid4()), "-", "g")

def NewHandleFromSeed(seed)->str:
    from faker import Faker
    f1 = Faker()
    Faker.seed(seed)
    return "h"+str.replace(str(f1.uuid4()), "-", "g")

def SeedFromString(input:str)->int:
    seed = 0
    i = 0
    while i < len(input):
        seed += ord(input[i])
        i += 1
    return seed

class Color():
    def __init__(self, argb:int):
        self.int = int32(argb)
        self.a = ((argb & 0xFF000000) >> 24)
        self.r = ((argb & 0x00FF0000) >> 16)
        self.g = ((argb & 0x0000FF00) >> 8)
        self.b = (argb & 0x000000FF)
    
    def to_int(self) -> int:
        al = int32((self.a << 24) & 0xFF000000)
        rl = int32((self.r << 16) & 0x00FF0000)
        gl = int32((self.g << 8) & 0x0000FF00)
        bl = int32(self.b & 0x000000FF)
        return int32(al | rl | gl | bl)

    def to_hex(self, withAlpha=False) -> str:
        if withAlpha:
            return '#%02x%02x%02x%02x' % (self.a, self.r, self.g, self.b)
        else:
            return '#%02x%02x%02x' % (self.r, self.g, self.b)

    def debug_print(self):
        print("Color ({}) | a({}) r({}) g({}) b({}) = ({}) | ({})".format(
            self.int, self.a, self.r, self.g, self.b, self.to_hex().upper(), int32(self.to_int())))

import numpy

INDENT = 3
SPACE = " "
NEWLINE = "\n"

# Changed basestring to str, and dict uses items() instead of iteritems().
def to_json(o, level=0):
  ret = ""
  if isinstance(o, dict):
    ret += "{" + NEWLINE
    comma = ""
    for k, v in o.items():
      ret += comma
      comma = ",\n"
      ret += SPACE * INDENT * (level + 1)
      ret += '"' + str(k) + '":' + SPACE
      ret += to_json(v, level + 1)

    ret += NEWLINE + SPACE * INDENT * level + "}"
  elif isinstance(o, str):
    ret += json.dumps(o)
  elif isinstance(o, list):
    ret += "[" + ",".join([to_json(e, level + 1) for e in o]) + "]"
  # Tuples are interpreted as lists
  elif isinstance(o, tuple):
    ret += "[" + ",".join(to_json(e, level + 1) for e in o) + "]"
  elif isinstance(o, bool):
    ret += "true" if o else "false"
  elif isinstance(o, int):
    ret += str(o)
  elif isinstance(o, float):
    ret += '%.7g' % o
  elif isinstance(o, numpy.ndarray) and numpy.issubdtype(o.dtype, numpy.integer):
    ret += "[" + ','.join(map(str, o.flatten().tolist())) + "]"
  elif isinstance(o, numpy.ndarray) and numpy.issubdtype(o.dtype, numpy.inexact):
    ret += "[" + ','.join(map(lambda x: '%.7g' % x, o.flatten().tolist())) + "]"
  elif o is None:
    ret += 'null'
  else:
    raise TypeError("Unknown type '%s' for json serialization" % str(type(o)))
  return ret