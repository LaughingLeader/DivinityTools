from pathlib import Path

def export_file(path, contents):
    try:
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