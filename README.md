# DataPipeline-Simple

An example of creating a simple data pipeline in Python, I built a Flask back-end to call the pipeline from web interface.

DataPipeline v.2 will use React as an interface and will also have extra processing added to the pipeline.

# How to use
1. Run `init_flask_env.sh` (may need to run `chmod u+x init_flask_env.sh`)
1. Run the Flask (dev) server
```
flask run
```
2. Open `index.html`

From there you should be able to enter the number of desired messages to send to the pipeline and submit it. All output will be written to a file in the local directory.

