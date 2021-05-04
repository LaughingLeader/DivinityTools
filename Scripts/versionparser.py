def ToVersionInt(major:int, minor:int, revision:int, build:int)->int:
	return (major << 28) + (minor << 24) + (revision << 16) + build

def ParseVersionInt(version:int)->tuple:
	major = (version >> 28)
	minor = (version >> 24) & 0x0F
	revision = (version >> 16) & 0xFF
	build = (version & 0xFFFF)
	return (major,minor,revision,build)

print("268435456 = {}".format(ParseVersionInt(268435456)))
print("8,16,256,65355 = {}".format(ToVersionInt(8,16,256,65355)))