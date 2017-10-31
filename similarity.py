import jieba
import numpy as np
from scipy import linalg
from sklearn.feature_extraction.text import TfidfVectorizer


class QuestionSet(object):
    def __init__(self, data):
        """\
        :param data: (list[NamedTuple]) list of questions ans answers
        """
        self.data = data
        self.question_tokens = []
        for entry in data:
            self.question_tokens.append(" ".join(jieba.cut(entry.question)))

        with open("stopwords.txt", "rb") as f:
            stopwords = f.read().decode("utf-8")
            stopwords = stopwords.split('\n')
        self.vectorizer = TfidfVectorizer(max_df=1, stop_words=stopwords)
        self.vectorizer.fit(self.question_tokens)

    def match(self, question):
        """\
        :param question: (string) question asking
        :return: answers sorted by possibility whether correct
        :rtype: list[string]
        """
        tokens = " ".join(jieba.cut(question))
        vec0 = self.vectorizer.transform([tokens]).toarray()[0]
        distances = [_distance(vec0, vec1)
                     for vec1 in self.vectorizer.transform(self.question_tokens).toarray()]
        distances = np.array(distances)
        index = np.argsort(distances)
        return [self.data[idx] for idx in index]


def _distance(question_vec0, question_vec1):
    """\
    :param question_vec0: question vector 0
    :param question_vec1: question vector 1
    :return: distance between question vectors
    :rtype: double
    """

    q0_norm = question_vec0
    q1_norm = question_vec1

    if np.sum(np.abs(question_vec0)):
        q0_norm = question_vec0 / linalg.norm(question_vec0)
    if np.sum(np.abs(question_vec1)):
        q1_norm = question_vec1 / linalg.norm(question_vec1)

    delta = q0_norm - q1_norm
    return np.sum(np.abs(delta))


if __name__ == "__main__":
    from collections import namedtuple

    Data = namedtuple("Data", ["question", "answer"])
    texts = ["这是一篇关于机器学习的文章，实际上它没有多少有趣的东西。", "图像数据库会变得非常巨大。", "大多数图像数据库可以永久存储图像。", "图像数据库可以存储图像。",
             "图像数据库可以存储图像。图像数据库可以存储图像。图像数据库可以存储图像。"]
    data = [Data(v, i) for i, v in enumerate(texts)]
    qs = QuestionSet(data)
    ans = qs.match("这是一篇机器学习相关的文章，它不太有趣。")
    print(ans)
