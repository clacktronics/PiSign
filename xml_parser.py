import xml.etree.cElementTree as ElementTree

tree = ElementTree.parse('sequence.xml')
root = tree.getroot()



sequence_players={}

# Find all cont tags
content = root.findall('cont')
#iterate into dictionary 'content : {proterties}''
for media in content:
	sequence_players[media.attrib['media']] = {properties.tag : properties.text for properties in media}

for player in sequence_players:
	print "\t",player
	for properties in sequence_players[player]:
		print "\t\t %s : %s" % (properties,sequence_players[player][properties])

print sequence_players['pin18']

#for media in content:
#	print media.attrib['media']
#	for properties in media:
#		print "\t %s : %s" % (properties.tag, properties.text)