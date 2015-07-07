# mysql_struct_doc
这是一个生成mysql数据库结构文档的工具，能够导出html单文件。适用于python 2和python 3。
# 依赖

```shell
pip install PyMySQL
```
# 用法

```shell
python gen.py --db test --output <path>
```
帮助文档：

```shell
Usage: gen.py [options]

Options:
  -h, --help           show this help message and exit
  --host=HOST          host, default:localhost
  --port=PORT          port, default:3306
  --user=USER          username, default:root
  --password=PASSWORD  password, default(empty):
  --db=DB              database name
  --output=OUTPUT      output dir
```

# LICENSE
MIT

