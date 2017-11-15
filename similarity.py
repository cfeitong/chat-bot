import jieba
import numpy as np
from gensim.models import Word2Vec
from scipy import linalg
from sklearn.feature_extraction.text import TfidfVectorizer


jieba.load_userdict("userdict.txt")


class QuestionSet(object):
    def __init__(self, data):
        """\
        :param data: (list[NamedTuple]) list of questions ans answers
        """

        self.data = data
        self.model = Word2Vec.load('model/word2vec_wx')
        self.question_vectors = []

        with open("stopwords.txt", "rb") as f:
            stopwords = f.read().decode("utf-8")
            self.stopwords = stopwords.split('\n')

        self.question_tokens = []
        question_part2 = []
        for entry in data:
            words = jieba.cut_for_search(entry.question)
            words = list(filter(lambda word: word not in self.stopwords, words))
            self.question_tokens.append(words)

            self.question_vectors.append([np.zeros([1, 256])])
            words_part2 = [] # words that can not fit in word2vec pretrained model
            for word in words:
                try:
                    vec = self.model.wv[word]
                    self.question_vectors[-1][0] += vec;
                except KeyError:
                    words_part2.append(word)
            question_part2.append(words_part2)


        self.vectorizer = TfidfVectorizer(max_df=1)
        questions = map(lambda tokens: " ".join(tokens), self.question_tokens)
        self.vectorizer.fit(list(questions))

        for question_token, question_vec in zip(question_part2, self.question_vectors):
            vec = self.vectorizer.transform([" ".join(question_token)]).toarray()[0]
            question_vec.append(vec)


    def match(self, question):
        """\
        :param question: (string) question asking
        :return: answers sorted by possibility whether correct
        :rtype: list[string]
        """
        words = jieba.cut_for_search(question)
        words = list(filter(lambda word: word not in self.stopwords, words))
        vec00 = np.zeros([1, 256])

        words_part2 = []
        for word in words:
            try:
                vec00 += self.model.wv[word]
            except KeyError:
                words_part2.append(word)

        vec01 = self.vectorizer.transform([" ".join(words_part2)]).toarray()[0]

        distances = [_distance(vec00, vec10) + _distance(vec01, vec11)
                     for vec10, vec11 in self.question_vectors]
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
