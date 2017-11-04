#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from resource import Ask, QAEntry, QAList
from question import sess

from flask import Flask, redirect, render_template, request, url_for
from flask_restful import Api

from db import db

import json

app = Flask(__name__)
api = Api(app)


@app.route('/')
def root():
    return redirect("qaform")


@app.route("/qaform")
def qaform():
    return render_template('QAForm.html')


@app.route('/submit_question', methods=['POST'])
def submit_question():
    form = request.form
    question = form['question']
    answer = form['answer']
    date = form['date']
    tags = form['tags'].split(' ')
    db.insert(question, answer, date, tags)
    db.commit()
    return redirect(url_for("qaform"))


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


api.add_resource(QAList, '/qalist')
api.add_resource(QAEntry, '/qalist/<int:id_>')
api.add_resource(Ask, '/ask')


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, threaded=True)
