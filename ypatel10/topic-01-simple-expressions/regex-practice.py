import re

text = "The rain in Spain"
res = re.search("^The.*Spain$", text)
print(res)

res = re.findall("aina", text)
print(res)