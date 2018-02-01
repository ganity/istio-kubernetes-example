#!/usr/bin/python
#
# Copyright 2017 Istio Authors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from flask import Flask, request, render_template, redirect, url_for
import simplejson as json
import requests
import sys
from json2html import *
import logging
import requests

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

app = Flask(__name__)

from flask_bootstrap import Bootstrap
Bootstrap(app)

def getForwardHeaders(request):
    headers = {}

    user_cookie = request.cookies.get("user")
    if user_cookie:
        headers['Cookie'] = 'user=' + user_cookie

    incoming_headers = [ 'x-request-id',
                         'x-b3-traceid',
                         'x-b3-spanid',
                         'x-b3-parentspanid',
                         'x-b3-sampled',
                         'x-b3-flags',
                         'x-ot-span-context'
    ]

    for ihdr in incoming_headers:
        val = request.headers.get(ihdr)
        if val is not None:
            headers[ihdr] = val
            #print "incoming: "+ihdr+":"+val

    return headers

# The UI:
@app.route('/')
@app.route('/index.html')
def index():
    headers = getForwardHeaders(request)
    result = {
        "code": 200,
        "data": getProductDetails(headers),
        "author": "hello-py",
        "version": "1.0.0"
    }
    return json.dumps(result), 200, {'Content-Type': 'application/json'}

# Data providers:
def getProductDetails(headers):
    try:
        url = "http://hello-node:8080"
        res = requests.get(url, headers=headers, timeout=3.0)
    except:
        res = None
    if res and res.status_code == 200:
        return res.json()
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return {'error': 'Sorry, product details are currently unavailable for this book.'}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print( "usage: %s port" % (sys.argv[0]))
        sys.exit(-1)

    p = int(sys.argv[1])
    print( "start at port %s" % (p))
    app.run(host='0.0.0.0', port=p, debug=True, threaded=True)

