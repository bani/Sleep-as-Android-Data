# -*- coding: utf-8 -*-
import csv
from datetime import datetime, timedelta

def read(filename):
  with open(filename, 'rb') as csvfile:
    source = csv.reader(csvfile)
    header = False
    data_sleep = []
    data_events = []
    event_key = None
    for row in source:
      if len(row[0]) < 1:
        continue
      header = not header
      if header:
        event_key = tuple(row[14:])
      else:
        data_sleep.append(parse_sleep(row))
        event_value = tuple(row[14:])
        data_events.append(filter_events(event_key, event_value))
    return data_sleep

def export(data, filename):
  with open(filename, 'wb') as csvfile:
    w = csv.DictWriter(csvfile,['date','weekday','start_time','end_time','length','cycles','deep'])
    w.writeheader()
    w.writerows(data)

def parse_sleep(row):
  sleep = {}
  start = datetime.strptime(row[2], '%d. %m. %Y %H:%M')
  end = datetime.strptime(row[3], '%d. %m. %Y %H:%M')
  date = start.date()
  if start.hour < 12:
    date = date - timedelta(1)
  sleep['date'] = date.isoformat()
  sleep['weekday'] = date.isoweekday() # Mon: 1 - Sun: 7
  sleep['start_time'] = start.strftime('%Y-%m-%d %H:%M')
  sleep['end_time'] = end.strftime('%Y-%m-%d %H:%M')
  sleep['length'] = (end - start).total_seconds() / 3600
  sleep['cycles'] = int(row[11])
  sleep['deep'] = float(row[12])
  return sleep

def filter_events(keys, values):
  if len(keys) != len(values):
    raise Exception("Length of keys must match length of values")
  filtered_columns = []
  for i in range(len(keys)):
    if keys[i] == 'Event':
      filtered_columns.append(values[i])
  events = {}
  for event in filtered_columns:
    e = event.split('-')
    if e[0] not in events:
      events[e[0]] = []
    events[e[0]].append(datetime.fromtimestamp(int(e[1])/1000))
  return events

if __name__ == "__main__":
  data = read('sleep-export.csv')
  export(data, 'sleep-data.csv')
