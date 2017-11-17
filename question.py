from utils import call_once
from db import db
from similarity import QuestionSet
from collections import namedtuple, defaultdict

DataEntry = namedtuple("DataEntry", ["id", "question"])


class ChatSession(object):
    def __init__(self):
        self.context = defaultdict(lambda: [])

    def __len__(self):
        return len(self.context)

    def __getitem__(self, id_):
        return self.context.get(id_, None)

    def apply_id(self):
        id_ = 1
        while id_ in self.context:
            id_ += 1
        return id_

    def delete_id(self, userid):
        if userid in self.context:
            del self.context[userid]

    def add_question(self, question, userid):
        self.context[userid].append(question)


@call_once
def load_questions():
    entries = [DataEntry(id=entry["__id__"], question=entry["question"])
               for entry in db]
    qset = QuestionSet(entries)
    return qset


def search_question(question):
    qset = load_questions()
    entry = qset.match(question)
    if entry:
        return db[entry.id]
    else:
        return None
    # return entry_list


sess = ChatSession()
