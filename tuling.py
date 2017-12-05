# -*- coding -*- 

import requests as rq
import json

API_URL = "http://www.tuling123.com/openapi/api"
API_KEY = "25f68e947cad4af7a807370451aa2a73"

def send_question(question, userid):
    data = {
        "key": API_KEY,
        "info": question,
    }
    if userid:
        data["userid"] = str(userid)
    response = rq.post(API_URL, data=data)
    return json.loads(response.text)
