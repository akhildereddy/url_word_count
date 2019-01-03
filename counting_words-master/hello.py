from flask import Flask, render_template
from flask_rq import RQ
from database import db_session
from tasks import count_words_at_url
from models import CountRequest

app = Flask(__name__)
RQ(app)

@app.route('/')
def hello_world():
    entries = CountRequest.query.all()
    results = [(entry.url,entry.count) for entry in entries]
    return render_template("index.html", results = results)
    # return 'Hello, World!'

@app.route("/give_wc/<path:url>")
def give_word_count(url):
    instance = CountRequest(url = url)
    db_session.add(instance)
    db_session.commit()
    count_words_at_url.delay(instance.id)
    return "Calculating Words in URL: %s"%url

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()