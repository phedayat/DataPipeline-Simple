import pipeline
import json
p = pipeline.Pipeline()
p.start([json.dumps({"message": "TEST"})])