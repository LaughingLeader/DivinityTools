from pathlib import Path
from typing import List, Dict

def export_file(path, contents):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        f = open(str(path.absolute()), 'w')
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