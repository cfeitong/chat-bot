#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import requests as rq
from flask import Flask, redirect, render_template, request, url_for
from flask_restful import Api, Resource
from gevent.wsgi import WSGIServer

import tuling
from get_weather import try_weather
from question import sess


class Ask(Resource):
    def get(self):
        args = request.args
        question = args.get("question", None)
        userid = args.get("userid", None)
        weather = try_weather(question)
        if weather is not None:
            return {"answer": str(weather)}

        response = rq.get(
            "http://127.0.0.1:1121/question?question={}".format(question))
        if response.status_code != 200:
            raise ConnectionError("similarity server not started")
        record = json.loads(response.text)

        if record is None:
            response = tuling.send_question(question, userid)
            return {"answer": response["text"]}
        if userid is not None:
            sess.add_question(question, userid)
        return {"answer": record[1]}


app = Flask(__name__)
api = Api(app)


@app.route("/login", methods=["GET"])
def login():
    return json.dumps({"userid": sess.apply_id()})


@app.route("/logout", methods=["GET"])
def logout():
    args = request.args
    userid = args.get("userid", None)
    if userid is None:
        return "", 401
    sess.delete_id(userid)
    return "", 200


api.add_resource(Ask, '/ask')


if __name__ == "__main__":
    server = WSGIServer(('', 5000), app)
    server.serve_forever()
