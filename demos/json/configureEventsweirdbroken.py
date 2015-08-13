import demjson
import json
import codecs
import time
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *

file = "events.json"
file2 = "events2.json"
with codecs.open(file2, 'r', encoding='utf-8') as f:
	data = f.read()
	json_file = demjson.decode(data)

dogs_events = {}
calendar_events = []
event_times = {}

def get_event_times(times):
	start_times = []
	end_times = []
	for dog in times:
		#print dog
		#print dog["start"]
		event_title = dog
		event_start = dog["start"]
		event_end = dog["end"]
		start_times.append(event_start)
		end_times.append(event_end)
	return start_times, end_times
			
def push_event_start_five_min(start_time):
	real_time = make_times_real(start_time)
	afterbreak = real_time+relativedelta(minutes=+5)
	afterbreak = make_real_times_strings(afterbreak)
	return afterbreak
		
def get_events_by_dog():
	for event in json_file:
		#print dogs_events
		#print event
		newkey = event["title"]
		newvalue = event["start"]
		#print dogs_events.keys()
		if newkey in dogs_events.keys():
			existingvalues = dogs_events[newkey]
			#print "existing values"
			#print existingvalues
			#print "new value"
			#print newvalue
			existingvalues.append(newvalue)
			#print "new values"
			#print existingvalues
			dogs_events[newkey] = existingvalues
		else:
			#print event["title"]
			#print event["start"]
			#newkey = event["title"]
			dogs_events[newkey] = [newvalue]
		#print newkey
		#print newvalue
	print "end of function"
	return dogs_events	

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

def add_end_times(start_time):
	#print start_time #2015-08-13T13:15:00
	real_time = make_times_real(start_time)
	#print real_time
	end_time = real_time+relativedelta(minutes=+15)
	end_time = make_real_times_strings(end_time)
	return end_time

def events_by_dog_to_calendar(dogs_events):
	for dog in dogs_events.keys():
		event_title = dog
		if not event_title == "Break":
			#print "event title"
			#print event_title
			for start_time in dogs_events[dog]:
				#print start_time
				event_start = push_event_start_five_min(start_time)
				event_end = add_end_times(event_start)
				calendar_events.append({"start":event_start,"title":event_title, "end":event_end})
	return calendar_events


def events_by_dog_to_calendar_with_breaks(dogs_events):
	print dogs_events
	for dog in dogs_events:
		event_title = dogs_events["title"]
		#print dog
		if not event_title == "Break":
			#print "event title"
			#print event_title
			start_time = dogs_events["end"]
			#print start_time
			event_start = start_time
			event_end = add_end_times(event_start)
			calendar_events.append({"start":event_start,"title":event_title, "end":event_end})
	return calendar_events


def add_breaks(end_times):
	break_end_times = []
	for time in end_times:
		time = make_times_real(time)
		break_start_time = time
		break_end_time = time+relativedelta(minutes=+5)
		break_start_time = make_real_times_strings(break_start_time)
		break_end_time = make_real_times_strings(break_end_time)
		calendar_events.append({"start":break_start_time, "end":break_end_time, "title":"Break"})
		break_end_times.append(break_end_time)
	return calendar_events, break_end_times
		
def get_json_with_breaks(dog_events):
	for event in dog_events:
		events_by_dog_to_calendar_with_breaks(event)
	return calendar_events

dog_events = get_events_by_dog()
json_file = events_by_dog_to_calendar(dog_events)

event_times = get_event_times(json_file)
print event_times[1]
dog_events = add_breaks(event_times[1])[0]
print dog_events
new_file = get_json_with_breaks(dog_events)




demjson.encode(new_file, encoding='utf-8', strict=True)
#print new_file
print "JSON DUMP___________"
#print json_file
data_file = json.dumps(new_file, f)
with open(file, 'w') as f:

	#data_file = str(new_file)
	f.write(data_file)