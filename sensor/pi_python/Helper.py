import re

def uppercaseToCamelcase(text):
	temp = text.lower().split('_')

	return temp[0] + "".join(map(str.capitalize, temp[1:]))


def camelcaseToUppercase(name):
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()


if __name__ == "__main__":
	print(camelcaseToUppercase("ServerIP"))
