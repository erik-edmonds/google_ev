from flask import Flask, Response, stream_with_context, render_template, json, url_for
import uuid
import time

app = Flask(__name__)

BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_NAME = 'data'

# create the flask object app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sample.html')

@app.route('/gauge')
def gauge():
    return render_template('gauge.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,debug=True)
