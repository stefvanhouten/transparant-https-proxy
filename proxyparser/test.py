import json
from mitmproxy import ctx
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
	flow.response = http.HTTPResponse.make(
		200,  # (optional) status code
		flow.request.text,  # (optional) content
		{"Content-Type": "text/html"}  # (optional) headers
	)