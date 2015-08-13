import demjson
import json
import codecs

file = "events.json"
file2 = "events2.json"
with codecs.open(file, 'r', encoding='utf-8') as f:
	data = f.read()
	json_file = demjson.decode(data)

print json_file
print data



new_file = json_file
demjson.encode(new_file, encoding='utf-8', strict=True)
print new_file
print "JSON DUMP___________"
#print json_file
data_file = json.dumps(new_file, f)
with open(file2, 'w') as f:

	#data_file = str(new_file)
	f.write(data_file)