from flask_rq import job
from models import CountRequest
from database import db_session
import requests

@job
def count_words_at_url(id):
    instance = CountRequest.query.get(id)
    url = instance.url
    resp = requests.get(url)
    instance.count =  len(resp.text.split())
    db_session.add(instance)
    db_session.commit()
    return instance.count