#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import multiprocessing as mp

import requests as rq
from flask import Flask, redirect, render_template, request, url_for
from flask_restful import Api, Resource
from gevent.wsgi import WSGIServer

import tuling
from get_weather import try_weather
from chat_entry import sess
from similarity import run_similarity_server


class Ask(Resource):
    def get(self):
        args = request.args
        question = args.get("question", None)
        userid = args.get("userid", None)

        response = sess.response(question)

        return {"answer": response}


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
    app_server = WSGIServer(('', 5000), app)
    app_server.serve_forever()
