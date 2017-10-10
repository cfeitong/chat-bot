from db import db


def search_question(question):
    for record in db:
        if record['question'] == question:
            return record
    return None
