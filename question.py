from utils import call_once
from collections import namedtuple, defaultdict


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


sess = ChatSession()
