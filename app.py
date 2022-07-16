import json
from DataPipeline.pipeline import Pipeline
from flask import Flask, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/start/", methods=["GET", "POST"])
def pipe():
	messages = (json.loads(request.data))["body"]
	P = Pipeline(num_workers=1)
	P.start([json.dumps(i) for i in messages])

	res = {
		"status": "Finished"
	}
	response = make_response(json.dumps(res))
	response.headers["Content-Type"] = "application/json"
	return response