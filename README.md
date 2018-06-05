现在很多网站都是对单个 IP 地址有访问次数限制，如果你在短时间内访问过于频繁。该网站会封掉你 IP，让你在一段时间内无法正常该网站。突破反爬虫机制的一个重要举措就是代理 IP。拥有庞大稳定的 IP 代理，在爬虫工作中将起到重要的作用,但是从成本的角度来说，一般稳定的 IP 池都很贵。因此，我为 Scrapy 爬虫编写个免费 IP 代理池插件。

# 1 特点
该插件适用的程序是基于 Scrapy 框架编写的爬虫程序。插件通过爬取免费代理地址，然后过滤掉无效 IP 代理后存放到 Mysql 数据库。另外，它会每 10 分钟轮询数据库中的 IP 代理数量。如果代理地址因为连接失败次数超过 3 次被删除，从而导致代理不够，它会后台重新爬取新的 IP 代理。

# 2 收集的代理网站
- 无忧代理(data5u)
- ip181 代理
- 快代理
- 西刺代理

# 3 项目说明
- startrun.py
项目的主入口。它负责启动 Scrapy 爬虫和代理池。

- your_scrapy_project
该目录下主要存放两个文件：`config.py` 和 `settings.py`。config.py 是代理池的项目配置信息。而 settings.py 是你的 Scrapy 爬虫项目的配置参考代码。

- ProxyPoolWorker.py
`ProxyPoolWorker.py` 是 IP代理池模块的管理类，负责启动和维护 IP 代理池。

- ProxyDBManager.py
`ProxyDBManager.py` 位于 dbManager 包下。它是数据库操作类。主要工作是创建数据库表、往数据库中插入 IP 代理、查询数据库中剩余的 IP 代理总数、从数据库中随机查询一个 IP 代理、对连接超时或失败的 IP 代理做处理。

- ProxyModel.py
`ProxyModel.py` 在 `model` 包下。它是 IP 代理对象类。

- requestEnginer.py
`requestEnginer.py` 位于 `requester` 目录下。requestEnginer 是整个爬虫代理池的网络引擎。它采用 Session 的形式来发起 HTTP 请求。同时，它还负责验证代理地址有效性,  达到过滤掉无用 IP 代理的目的。

- scrapy
scrapy 目录是一些 Scrapy 框架的自定义中间件。`RandomUserAgentMiddleware.py` 是为 HTTP 请求随机设置个 User-agent。`middlewares.py` 有两个职责。一是为 HTTP 请求随机设置个 IP 代理。二是负责捕获并处理 HTTP 异常请求。

- spiders
该包主要是爬取各大代理网站的爬虫。

# 4 使用方法
## 4.1 安装依赖
使用本插件，你需要通过 pip 安装以下依赖：
- requests
- apscheduler
- pymysql

## 4.2 修改配置
1) 将 `startrun.py`、`config 文件夹`、`proxy 文件夹` 复制到你的 Scrapy 项目的主目录下。
例如你项目名为 demo，那么你需要放到 demo 的目录下。

2) 修改 `config` 包下的 `config.py` 里面的 Mysql 相关配置信息。

3) 参考 `setting.py`，修改你的 Scrapy 项目中的 `setting.py` 文件。主要是在你项目中增加以下代码：
```python
# 默认使用 IP 代理池
if IF_USE_PROXY:
    DOWNLOADER_MIDDLEWARES = {

        # 第二行的填写规则
        #  yourproject.myMiddlewares(文件名).middleware类

        # 设置 User-Agent
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'proxyPool.scrapy.RandomUserAgentMiddleware.RandomUserAgentMiddleware': 400,

        # 设置代理
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
        'proxyPool.scrapy.middlewares.ProxyMiddleware': 100,

        # 设置自定义捕获异常中间层
        'proxyPool.scrapy.middlewares.CatchExceptionMiddleware': 105,

        # 设置自定义重连中间件
        'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
        'proxyPool.scrapy.middlewares.RetryMiddleware': 95,
    }
```

4) 修改 `startrun.py` 中 `spider_list` 列表中的爬虫名。

5) 最后运行  `startrun.py` 即可。startrun.py 会先抓取 ip 代理网站的 ip，然后再使用这些代理爬取目标网站。

# 5 写在最后
本项目会持续维护。如果你有宝贵的完善建议或者有更多的代理网站，可以联系我。