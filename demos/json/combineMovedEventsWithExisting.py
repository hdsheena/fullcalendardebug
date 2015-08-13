import demjson
import json
import codecs
import time
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
import sys

file_with_changes = "events4.json"
file_to_use = "eventsWithIdsprevious.json"
changed_file = "eventsWithChanges.json"

#Open the files and decode any json ones

def open_file(file):

	with codecs.open(file, 'r', encoding='utf-8') as f:
		data = f.read()
		#print data
		#file = demjson.decode(data)
		return data

changes = open_file(file_with_changes)
json_file = open_file(file_to_use)
json_file = demjson.decode(json_file)

dict_of_change_ids = {}
list_of_changes = []


def make_times_real(timestring):
	real_time = parse(timestring, fuzzy=True)
	return real_time
def make_real_times_strings(real_time):
	end_time = str(real_time)
	add_letter = end_time.split(" ")
	#print end_time
	add_letter.insert(1,"T")
	end_time = "".join(add_letter)
	return end_time


def replace_times(event, new_start_time):
	event_title = event["title"]
	if new_start_time[9] != 2:
		json_file.remove(event)
	
	start_time = make_times_real(new_start_time)
	if event_title == "Break":
		end_time = start_time+relativedelta(minutes=+5)
	else:
		end_time = start_time+relativedelta(minutes=+15)
	
	start_time = make_real_times_strings(new_start_time)
	end_time_string = make_real_times_strings(end_time)
	event["start"] = new_start_time
	event["end"] = end_time_string
	#print event
	return event

def make_changes_into_list(changes):
	#print type(changes)
	#print changes[1]
	split_changes = changes.split('[')
	#print split_changes
	for i in split_changes:
		i = i[:-1]
		#print i
		if len(i):
			i = demjson.decode(i, encoding='utf8')
			list_of_changes.append(i)
	return list_of_changes

changes_json = make_changes_into_list(changes)
print changes_json
#dict_of_changes = demjson.decode(changes_json[1], encoding='utf8')
#print dict_of_changes

def make_ids_and_start_times(list_of_changes):
	for i in list_of_changes:
		if len(i):
			#print i
			id_value = i["id"]
			#print id_value
			start_value = i["start"]
			#print start_value
			dict_of_change_ids[id_value] = start_value
	return dict_of_change_ids

make_ids_and_start_times(changes_json)
print dict_of_change_ids
changed_times = []

def match_id_to_change(dict_of_change_ids, json_file):
	for i in json_file:
		id = i["id"]
		#print dict_of_change_ids['35']
		#print id
		#print dict_of_change_ids[str(id)]
		try:
			new_start_time = dict_of_change_ids[str(id)]
			#print "New strt time: " + new_start_time
			replaced = replace_times(i, new_start_time)
			#print replaced
			changed_times.append(replaced)
		except KeyError as detail:
			pass
			#print "key error", detail
		except UnboundLocalError as detail:	
			print "unbound", detail
			#print id
			#print dict_of_change_ids.keys()
			print "Try failed", sys.exc_info()[0]
			pass
	return changed_times


changed_data = match_id_to_change(dict_of_change_ids, json_file)
print changed_data
for i in json_file:
	print i["id"]

for i in changed_data:
	print i["id"]

#append changed data to json_file, and remove any duplicate ids
for i in json_file:
	changed_data.append(i)


print len(changed_data)


#this doesn't work?
"""
date_to_remove_after = parse("Aug 12, 2015")
for i in changed_data:
	start_time = make_times_real(i["start"])
	if start_time > date_to_remove_after:
		changed_data.remove(i)
print len(changed_data)
"""
new_file = changed_data
data_file = json.dumps(new_file)
with open(changed_file, 'w') as f:

	#data_file = str(new_file)
	f.write(data_file)




