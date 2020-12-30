import os
import time
import json 

from flask import Flask, request, make_response
from function import handler
from waitress import serve
from graphql import client

hostName = "0.0.0.0"
PORT = int(os.environ['PORT'])
GRAPHQL_URL = os.environ['GRAPHQL_URL']

app = Flask(__name__)

class FaasContext:
    def __init__(self, jobId, databaseId, client, jobs, meta):
        self.jobId = jobId
        self.databaseId = databaseId
        self.client = client
        self.jobs = jobs
        self.meta = meta

# distutils.util.strtobool() can throw an exception
def is_true(val):
    return len(val) > 0 and val.lower() == "true" or val == "1"

@app.before_request
def fix_transfer_encoding():
    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

def get_params (request):
    raw_body = os.getenv("RAW_BODY", "false")

    as_text = True

    if is_true(raw_body):
        as_text = False

    data = request.get_data(as_text=as_text)
    params = {}
    if ('application/json' in request.headers.get('Content-Type')):
        try:
            params = json.loads(data)
        except Exception as e:
            params = data
    else:
        params = data

    return params

def handle_error (resp, e):
    resp.headers['X-Job-Error'] = True
    resp.data = json.dumps({ 'message': str(e) })

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path:path>", methods=["POST", "GET"])
def faas_handler(path):
    resp = make_response()
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['X-Worker-Id'] = request.headers.get('X-Worker-Id')
    resp.headers['X-Job-Id'] = request.headers.get('X-Job-Id')
    resp.headers['X-Database-Id'] = request.headers.get('X-Database-Id')

    params = get_params(request)
    
    databaseId = request.headers.get('X-Database-Id')
    jobId = request.headers.get('X-Job-Id')

    apiClient = client.GraphQLClient(GRAPHQL_URL, {
          'X-Api-Name': 'private',
          'X-Database-Id': databaseId
        })

    jobsClient = client.GraphQLClient(GRAPHQL_URL, {
          'X-Api-Name': 'jobs',
          'X-Database-Id': databaseId
        })

    metaClient = client.GraphQLClient(GRAPHQL_URL, {
          'X-Meta-Schema': True,
          'X-Database-Id': databaseId
        })

    try:
        ctx = FaasContext(jobId, databaseId, apiClient, jobsClient, metaClient)
        value = handler.handle(params, ctx)
        resp.data = json.dumps(value)
    except Exception as e:
        handle_error(resp, e)

    return resp

if __name__ == '__main__':
    serve(app, host=hostName, port=PORT)
    print("Server started http://%s:%s" % (hostName, PORT))
