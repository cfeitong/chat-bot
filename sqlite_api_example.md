```python
#sqlite_api模块使用示例
#导入模块
import sqlite_api
#如果已存在表的话删除表
sqlite_api.drop_table()
#如果未存在表的话创建表
sqlite_api.create_table()
# 插入数据
sqlite_api.insert(["问题1", "答案1"])
sqlite_api.insert(["问题2", "答案2"])
# 更新数据
sqlite_api.update("question='问题3'", "id=1")
# 删除数据
sqlite_api.delete("id=2")
#查找（全部）数据
print(sqlite_api.select("*"))
# 导入txt文档
sqlite_api.import_txt("E:/test/test_import_txt.txt")
# 查找指定字段在指定条件下的的数据
print(sqlite_api.select("question,answer", "id=4"))
# 直接执行sql语句
sqlite_api.sql("INSERT INTO QA(question,answer)values('问题','答案')")
print(sqlite_api.sql("SELECT * FROM QA"))
```