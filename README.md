# Ice Breaker

AI Agent Web 应用，输入某人的名字，可以自动抓取 LinkedIn 和 Twitter 数据，并根据这些数据生成总结和制定破冰问题。

## 环境变量

要运行此项目，您需要将以下环境变量添加到 .env 文件中：

`OPENAI_API_KEY`

`SCRAPIN_API_KEY`

`TAVILY_API_KEY`

`TWITTER_API_KEY`

`TWITTER_API_SECRET`

`TWITTER_ACCESS_TOKEN`

`TWITTER_ACCESS_SECRET`

`LANGCHAIN_TRACING_V2`

`LANGCHAIN_API_KEY`

`LANGCHAIN_PROJECT` 

>重要提示 ：如果您通过设置 LANGCHAIN_TRACING_V2=true 来启用跟踪，则必须在 LANGCHAIN_API_KEY 中设置有效的 LangSmith API 密钥。如果没有有效的 API 密钥，应用程序将抛出错误。如果您不需要跟踪，只需删除或注释掉这些环境变量即可。

## 本地运行

克隆项目：

```
git clone https://github.com/quartzeast/ice_breaker.git
```

本项目使用 uv 管理依赖，克隆项目后进入项目目录并更新依赖：

```
cd ice_beraker
uv sync
```

然后运行 flask 服务器：

```
uv run app.py
```