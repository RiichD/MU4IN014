from lxml import etree as ET

local_input = "dblp_2020_2020.xml"

p = ET.XMLParser(recover=True)
tree = ET.parse(local_input, parser=p)
root = tree.getroot()
print(f"XML File loaded and parsed, root is {root.tag}")

req_name = "Louise A. Dennis"
for child in root:
	if len(child):
		for data in child:
			if data.text != None and req_name in data.text:
				print(root[0][0].text)
				for i in range(len(child)):
					print(child[i].text)
				print("\n")

