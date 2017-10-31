import json
import urllib.parse

from flask import Flask, redirect, render_template, request, url_for
from flask_restful import Api, Resource

from db import db
from question import search_question


class Ask(Resource):
    def get(self):
        args = request.args
        question = args.get("question", None)
        userid = args.get("userid", None)
        record = search_question(question)
        if record is None:
            return "", 204
        if userid is None:
            return "", 401
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
