#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from resource import Ask, QAEntry, QAList

from flask import Flask, redirect, render_template, request, url_for
from flask_restful import Api

from db import db

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello():
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
    return redirect(url_for('hello'))


api.add_resource(QAList, '/qalist')
api.add_resource(QAEntry, '/qalist/<int:id_>')
api.add_resource(Ask, '/ask')
