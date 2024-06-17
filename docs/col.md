# Python SDK

使用RockAI SDK来调用大模型更为简单.

## 安装

RockAI python SDK 支持 3.9-3.11 版本
```python
pip install rockai-cli-app
```

## 获取API TOKEN

登录RockAI后点击 [获取API_TOKEN](https://www.rockai.online/setting/token) 

## 鉴权

```python
#通过创建clinet类来直接完成鉴权, 填入从上一步获取的API TOKEN
from rockai_cli_app import Client
client = Client(api_token="<API_TOKEN_HERE>")
```

## 运行模型 (synchronous同步调用)

这里我们拿 **meta/musicgen** 举例，生成一段音乐, 更多模型参数请前往
[meta/musicgen](https://www.rockai.online/models/meta/musicgen) 查看

```python
from rockai_cli_app import Client

# Run a music generation model
def main():
    input = {
        "prompt": "Edo25 major g melodies that sound triumphant and cinematic. Leading up to a crescendo that resolves in a 9th harmonic",
        "model_version": "stereo-large",
        "output_format": "mp3",
        "normalization_strategy": "peak",
    }
    client = Client(api_token="<填入你的 API TOKEN>")
    result = client.run(
        version="671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
        input=input,
    )
    print("Result:", result)


# Run the main function
if __name__ == "__main__":
    main()
```


## 运行模型 (asynchronous异步调用)

这里我们同样拿 **meta/musicgen** 举例，生成一段音乐, 使用 **run_async** 方法生成音乐. 此方法适用于FastAPI等异步框架.

```python

from rockai_cli_app import Client
import asyncio
# Run a music generation model
async def main():
    input = {
        "prompt": "Edo25 major g melodies that sound triumphant and cinematic. Leading up to a crescendo that resolves in a 9th harmonic",
        "model_version": "stereo-large",
        "output_format": "mp3",
        "normalization_strategy": "peak",
    }
    client = Client(api_token="<填入你的 API TOKEN>")
    result = await client.run_async(
        version="671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
        input=input,
    )
    print("Result:", result)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

```


## 调用大语言模型 (synchronous同步调用)
大语言模型通常以流式的方式返回结果, 这里我们拿 **meta/meta-llama-3-70b-instruct** 举例，让接口以流式的方式返回结果. 更多模型参数请前往 [meta/meta-llama-3-70b-instruct](https://www.rockai.online/models/meta/meta-llama-3-70b-instruct) 查看

```python
from rockai_cli_app import Client


# Run a Large Language Model
def main():
    input = {
        "top_p": 0.9,
        "prompt": "Work through this problem step by step:\n\nQ: Sarah has 7 llamas. Her friend gives her 3 more trucks of llamas. Each truck has 5 llamas. How many llamas does Sarah have in total?",
        "max_tokens": 512,
        "min_tokens": 0,
        "temperature": 0.6,
    }
    client = Client(api_token="<填入你的 API TOKEN>")
    result = client.stream(input=input, version="fbfb20b472b2f3bdd101412a9f70a0ed4fc0ced78a77ff00970ee7a2383c575d")
    for word in result:
        print(word)


# Run the main function
if __name__ == "__main__":
    main()

```


## 调用大语言模型 (asynchronous异步调用)
大语言模型通常以流式的方式返回结果, 这里我们拿 **meta/meta-llama-3-70b-instruct** 举例，让接口以流式的方式返回结果, 开发者可以使用 **stream_async** 方法，在FastAPI等异步框架里面调用模型. 更多模型参数请前往 [meta/meta-llama-3-70b-instruct](https://www.rockai.online/models/meta/meta-llama-3-70b-instruct) 查看
```python
from rockai_cli_app import Client
import asyncio

# Run a Large Language Model
async def main():
    input = {
        "top_p": 0.9,
        "prompt": "Work through this problem step by step:\n\nQ: Sarah has 7 llamas. Her friend gives her 3 more trucks of llamas. Each truck has 5 llamas. How many llamas does Sarah have in total?",
        "max_tokens": 512,
        "min_tokens": 0,
        "temperature": 0.6,
    }
    client = Client(api_token="<填入你的 API TOKEN>")
    result = client.stream_async(input=input, version="fbfb20b472b2f3bdd101412a9f70a0ed4fc0ced78a77ff00970ee7a2383c575d")
    async for word in result:
        print(word)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
```


## 取消运行中的模型
```python

```



