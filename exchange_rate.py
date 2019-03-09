
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


# Author - Naresh Ganatra
# http://youtube.com/c/NareshGanatra


from __future__ import print_function
# from future.standard_library import install_aliases
# install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

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

    # commented out by Naresh
    res = processRequest(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)


    r.headers['Content-Type'] = 'application/json'

    return r


def processRequest(req):

    if req.get("queryResult").get("action") != "rate":
        print("Please check your action name in DialogFlow...")
        return {}

    result = req.get("queryResult")
    parameters = result.get("parameters")



    print (parameters['currency-name1'])
    currency1 = parameters['currency-name']
    currency2 = parameters['currency-name1']
    baseurl = 'https://api.exchangeratesapi.io/latest?base=' + currency1 + '&symbols=' + currency2;




    if baseurl is None:
        return {}

    result = urlopen(baseurl).read()
    data = json.loads(result)
    # for some the line above gives an error and hence decoding to utf-8 might help
    # data = json.loads(result.decode('utf-8'))
    res = makeWebhookResult(data,currency2)
    return res



def makeWebhookResult(data,currency2):
    query = data.get('rates')

    if query is None:
        return {}
    result = query.get(currency2)
    if result is None:
        return {}

    speech = "The exchange rate is  " + str(result)


    # Naresh
    return {

        "fulfillmentText": speech,
        "source": "Exchange rateapi"
    }


@app.route('/test', methods=['GET'])
def test():
    return "Hello there my friend !!"


@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    string = "You are awesome !!"
    Message = "this is the message"

    my_result = {

        "fulfillmentText": string,
        "source": string
    }

    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')

