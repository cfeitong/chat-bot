import requests
import json
import jieba

# This class provide some api to get the service of baidu AI
class BaiduApi(object):
    def __init__(self):
        self.api_key = 'xB2ZeY8fGTqxASPWnB9hvd8I'
        self.secret_key = 'sRd1qeGALxDRrrwmh36EfNjBRNvAY1WC'
        self.access_token = None

    def get_Access_Token(self):
        """
        :return: access_token for service
        """
        url = 'https://aip.baidubce.com/oauth/2.0/token'
        data = {'grant_type': 'client_credentials', 'client_id': self.api_key, 'client_secret': self.secret_key}
        r = requests.get(url, params=data)
        data = json.loads(r.text)
        return data["access_token"]

    def get_WordVec(self, word):
        """
        :param word: a chinese word
        :return: corresponding vector
        """
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_vec'
        self.access_token = self.get_Access_Token()

        target_url = url + '?access_token=' + self.access_token
        body = {"word": word}
        s = json.dumps(body)
        r = requests.post(target_url, data=s)
        data = json.loads(r.text)
        if "error_code" in data:
            return "error"
        else :
            return data["vec"]

    def get_SentenceSimilarity(self, seq1, seq2):
        pass


if __name__ == "__main__":
    bai = BaiduApi()
    print(bai.get_WordVec("电子科技"))
    print("/".join(jieba.cut("电子科技大学")))
