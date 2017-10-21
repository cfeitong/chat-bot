from db import db
from similarity import QuestionSet
from collections import namedtuple

DataEntry = namedtuple("DataEntry", ["id", "question"])

def search_question(question):
    entries = [DataEntry(id=entry["__id__"], question=entry["question"]) for entry in db]
    qset = QuestionSet(entries)
    entry_list = qset.match(question)
    best: DataEntry = entry_list[0]
    return db[best.id]

