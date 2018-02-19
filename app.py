# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib import parse
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import psycopg2
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    # res = json.dumps(res, indent=4)
    # print(res)
    # Converting res back into json output
    json_convert = json.dumps(res)

    r = make_response(json_convert)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "yahooWeatherForecast":

        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = makeYqlQuery(req)
        if yql_query is None:
            return {}
        yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
        result = urlopen(yql_url).read()
        data = json.loads(result)
        res = makeWebhookResult(data)
        return res

    elif req.get("result").get("action") == "queryLine":

        line_query = "SELECT ticket_id, first_name, issue_type FROM public.example_table"
        result = dbConnection(line_query)
        # process data back from db
        record = []
        for r in result:
            record.append(
                {'ticket_id': r[0],
                 'first_name': r[1],
                 'issue_type': r[2]
            })
        # Package up data from DB in appropriate response format
        formatted = queryLineResponse(record)
        # package up formatted response in json

        # response = json.loads(formatted)
        return formatted

    else:
        return {}


def dbConnection(line_query):
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])
    # DATABASE_URL set in : heroku config

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    curr = conn.cursor()
    curr.execute(line_query)

    query_results = curr.fetchall()

    return query_results


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def queryLineResponse(data):
    speech = "The line looks like:\n Ticket Id | First Name | Issue Type\n ------------------------------------\n"
    # Iterate through records in the data, and append them to the 'speech' variable
    # for record in data:
    #     ticket_id = record.get('ticket_id')
    #     first_name = record.get('first_name')
    #     issue_type = record.get('issue_type')
    #
    #     speech + "{} | {} | {}\n---------------\n".format(ticket_id, first_name, issue_type)
    speech = speech + str(data)
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "item": item,
        "data": data,
        # "contextOut": [],
    }


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "item": item,
        "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
