# 项目背景

+ 本项目名为MyGO
+ 本项目后端基于python flask框架进行开发
+ 前端基于X-admin框架进行开发
+ 数据库使用 mysql 8.0.33

# 项目部署

​	安装python所需库: 定位到项目根目录，通过 `pip install -r requirements.txt` 命令即可安装python相关库。

​	导入数据库: 在数据库管理软件中，运行脚本 `DMyGO.sql` 即可创建数据库DMyGO。

​	配置项目数据库: 在项目根目录中，找到 `config.py` 可以看到如下内容:

```python
DATABASE = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'db': 'dmygo'
}

SECRET_KEY = "login"
```

​	将值修改为相关数据库内容即可完成配置。

​	运行项目: 打开项目并运行，在浏览器输入 `http://127.0.0.1:5000/` 即可启动项目。