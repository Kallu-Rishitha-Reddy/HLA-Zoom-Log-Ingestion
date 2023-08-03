#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import splunklib.results as results
import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import splunklib.client as client
import json
import ssl
import datetime
import pytz
import re

def write_to_file(data, filepath):
    with open(filepath, 'w') as f:
        f.write(data)


def log_text(text, filename):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(filename, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text)


def get_data():
    # using now() to get current time
    current_time = datetime.datetime.now()

    context = ssl.create_default_context()
    context.set_ciphers("DEFAULT")

    HOST = "splunk.corp.service-now.com"
    PORT = 8089
    BEARER_TOKEN = """eyJraWQiOiJzcGx1bmsuc2VjcmV0IiwiYWxnIjoiSFM1MTIiLCJ2ZXIiOiJ2MiIsInR0eXAiOiJzdGF0aWMifQ.eyJpc3MiOiJyaXNoaXRoYS5yZWRkeSBmcm9tIHVzZXBsc3Bsc2gwMS5jb3JwLnNlcnZpY2Utbm93LmNvbSIsInN1YiI6InJpc2hpdGhhLnJlZGR5IiwiYXVkIjoiUHJvamVjdCBmb3IgU3BsdW5rIGludGVncmF0aW9uIHdpdGggSExBIiwiaWRwIjoiU0FNTDovL3NhbWwiLCJqdGkiOiJkNWQyMWM0ZTBhMGE4Y2Y2MjVjZDU3Nzk1ZDc0ZTUzMzI2YWUwMTZlNThmMmVmY2JjZTczYjA2ZGE1YjNiZDYyIiwiaWF0IjoxNjg3MzAxNDg3LCJleHAiOjE3MDI4NTcwODcsIm5iciI6MTY4NzMwMTQ4N30.hJWwHnYA0uJElKXzEhWqugiRHvQNT3Cuc0nD2knrpLb4xBktRTjxxry2FwZyFtAm20fh5TdZXbcZ9-lBEcDS9Q"""

    # Create a Service instance and log in
    service = client.connect(
        host=HOST,
        port=PORT,
        splunkToken=BEARER_TOKEN,
        verify=True,
        context=context)

    try:
        rr = results.JSONResultsReader(service.jobs.export("search index=zoom earliest=-5m", output_mode='json'))
        count = 0
        json_obj = []

        for result in rr:
            if isinstance(result, dict):
                json_obj.append(json.loads(result['_raw']))

                if 'topic' in json_obj[-1]['payload']['object']:
                    del json_obj[-1]['payload']['object']['topic']

                event_ts = datetime.datetime.fromtimestamp(json_obj[-1]['event_ts']//1000).strftime('%Y-%m-%d %H:%M:%S')
                event_ts_upd = datetime.datetime.strptime(event_ts, '%Y-%m-%d %H:%M:%S')
                json_obj[-1]['event_ts'] = str(event_ts_upd)

                count += 1

        json_to_send = ',\n'.join(json.dumps(item) for item in json_obj)

        return json_to_send

    except Exception as e:
        print('Below Exception Occurred: \n')
        print(e)
        log_text(str(current_time)+":"+"Exception : " + str(e), "error.txt")
        # Reraise the exception so it can be caught by the caller
        raise e


if __name__ == '__main__':
    data = get_data()
    write_to_file(data, "log.txt")