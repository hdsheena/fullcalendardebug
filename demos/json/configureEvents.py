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

revised_event_times = []

def sort_times(list_of_times):
	list_of_times.sort()
	return list_of_times

def fix_overlapping_times(start_times, end_times, event_times):
#take lists of times and match them up with what they are - sorted
#if break, delta from start time is 5 minutes.
#if dog, delta is 15 minutes.
#from beginning of list, find the first start time, make sure it's a dog, then give it an end time of 15 min later. Take the next event title and start it at the end time of the current
#item in the list. Keep going until all start times are used up, then return a summary of the event times json style.
	earliest_to_latest = sort_times(start_times)
	starting_at = parse("Aug 13 2015 12:00:00 PM", fuzzy=True)
	current_start_time = starting_at
	previous_event = "Break"  #this keeps it from starting with a break
	for time in earliest_to_latest:
		#look up event title in event_times
		for event in event_times:
			if time == event["start"]:
				event_title = event["title"]
			else:
				pass
		print time
		if event_title != "peaches": 
			if event_title == previous_event:
				continue
		print "End of this for"
		start_time = current_start_time
		if event_title == "Break":
			end_time = start_time+relativedelta(minutes=+5)
		else:
			end_time = start_time+relativedelta(minutes=+15)
		#make times strings
		start_time = make_real_times_strings(start_time)
		end_time_string = make_real_times_strings(end_time)
		
		revised_event_times.append({"title": event_title, "start": start_time, "end": end_time_string})
		#assign a start time based on the end time of the previous iteration, or a given time
		current_start_time = end_time
		previous_event = event_title
	return revised_event_times
		#add 5 or 15 minutes
		#put start and end time in new_event_times dictionary with event title
		#put end time in a variable to use for the next lookup


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


def events_by_dog_to_calendar_with_breaks(dogs_events, end_times):
	print "With Breaks Function"
	print dogs_events
	
	event_title = dogs_events["title"]
	#print dog
	if not event_title in ["Break", "replaced"]:
		#print "event title"
		#print event_title
		n = dog_events.index(dogs_events)
		print n
		if n < len(end_times):
			start_time = end_times[n]
			print start_time
			event_start = start_time
			event_end = add_end_times(event_start)
			calendar_events.append({"start":event_start,"title":event_title, "end":event_end})
			dogs_events["title"]="replaced"
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
		
def get_json_with_breaks(dog_events, break_end_times):
	for event in dog_events:
		events_by_dog_to_calendar_with_breaks(event, break_end_times)
	return calendar_events

def find_duplicates(new_file):
	start_times_iterated = []
	for i in new_file:
		if i["start"] in start_times_iterated:
			new_file.remove(i)
		else:
			start_times_iterated.append(i["start"])
	return new_file

def remove_replaced(new_file):
	for i in new_file:
		if i["title"] == "replaced":
			new_file.remove(i)
	return new_file
		

dog_events = get_events_by_dog()
json_file = events_by_dog_to_calendar(dog_events)

event_times = get_event_times(json_file)
print event_times[1]
print sort_times(event_times[1])
breaks_added = add_breaks(event_times[1])
dog_events = breaks_added[0]
break_end_times = breaks_added[1]
print dog_events
new_file = get_json_with_breaks(dog_events, break_end_times)

#event = dog_events
print "event"
#print event
#print events_by_dog_to_calendar_with_breaks(event, break_end_times)
both_times = get_event_times(new_file)
new_file = fix_overlapping_times(both_times[0], both_times[1], new_file)
new_file = find_duplicates(new_file)
new_file = remove_replaced(new_file)

demjson.encode(new_file, encoding='utf-8', strict=True)
#print new_file
print "JSON DUMP___________"

print event_times[1]
print sort_times(event_times[1])


#print json_file
data_file = json.dumps(new_file, f)
with open(file, 'w') as f:

	#data_file = str(new_file)
	f.write(data_file)