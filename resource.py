import json

import requests as rq
from flask import Flask, redirect, render_template, request, url_for
from flask_restful import Api, Resource

from db import db
from question import sess
from tuling import send_question
from get_weather import try_weather


class Ask(Resource):
    def get(self):
        args = request.args
        question = args.get("question", None)
        userid = args.get("userid", None)
        weather = try_weather(question)
        if weather is not None:
            return {"answer": str(weather)}

        response = rq.get("http://127.0.0.1:1121/question?question={}".format(question))
        if response.status_code != 200:
            raise ConnectionError("similarity server not started")
        record = json.loads(response.text)

        if record is None:
            response = send_question(question, userid)
            return {"answer": response["text"]}
        if userid is not None:
            sess.add_question(question, userid)
        return {"answer": record["answer"]}


class QAList(Resource):
    def get(self):
        return list(db.records.keys()), 200

    def put(self):
        entry = json.loads(request.form["entry"])
        question = entry.get("question", "")
        answer = entry.get("answer", "")
        date = entry.get("date", "")
        tags = entry.get("tags", "")
        db.insert(question, answer, date, tags)
        db.commit()
        return "", 200


class QAEntry(Resource):
    def get(self, id_):
        try:
            return db[id_]
        except KeyError:
            return '', 204

    def put(self, id_):
        entry = json.loads(request.form["entry"])
        question = entry.get("question", None)
        answer = entry.get("answer",   None)
        date = entry.get("date",     None)
        tags = entry.get("tags",     None)
        try:
            record = db[id_]
            if question is not None:
                db.update(record, question=question)
            if answer is not None:
                db.update(record, answer=answer)
            if date is not None:
                db.update(record, date=date)
            if tags is not None:
                db.update(record, tags=tags)
        except KeyError:
            db.insert(question, answer, date, tags)

        db.commit()
        return "", 200

    def delete(self, id_):
        try:
            del db[id_]
            db.commit()
        except KeyError:
            return "", 204
        return "", 200
