### URL: /qalist

- *get*
    json格式，返回所有id的列表。

- *put*

    添加一条记录。

    data应为json格式。

    样例：

    ```javascript
    {
        "entry": {
            "question": "your question",
              "answer": "your answer",
                "date": "date time",
                "tags": "tag1 tag2"
        }
    }
    ```

### URL: /qalist/\<id_\>

- *get*

  返回id为id_的记录，json格式。

  如果id_不存在，返回204。

- put

  data 与 /qalist的put请求相同。如果id为id\_的记录已经存在，将会更新此记录。如果不存在，将会添加一条记录。但是添加的记录id不一定为id\_。

- delete

  删除id为id\_的记录。

  如果id_不存在，返回204。

### URL:/ask?question='...'

- get

  参数question，返回答案。