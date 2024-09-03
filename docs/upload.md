# 介绍

RockAI平台支持开发者自己上传模型并推理，不需要购买GPU. 开发者可以使用我们提供的命令行工具制作一个Docker镜像. 当将镜像被上传到RockAI平台之后, 开发者就可以使用HTTP API,RockAI Python SDK, RockAI NodeJS SDK的方式调用模型.

## 上传教程示例
0. 新建一个文件夹并创建一个虚拟环境，如果您已经搭建好virtual enviroment可以跳过此步骤.

```base
$ mkdir my_project && mkdir my_project
$ python -m venv env
$ source env/bin/activate
```

1. 安装依赖库`rockai`, 推荐在virtual environment环境下安装.

```bash
# RockAI 支持的python版本为 3.9-3.12 版本
$ pip install -U rockai
```

2. 新建一个文件夹，或者在现有工程下运行以下代码

```bash
$ mkdir my_ai_project && cd my_ai_project
$ rockai init
```

`rockai init`命令会在当年目录下生成`predictor.py` 和 `.dockerignore` 两个文件. 使用VSCode或其他IDE打开`predictor.py`文件.

```python
from rockai import BasePredictor, Input, thread_limit,List,Dict
import logging
from transformers import pipeline
# 如果需要使用环境变量，可以使用dotenv库，把环境变量写入.my_env文件中
# from dotenv import load_dotenv
# load_dotenv(".my_env")

class Predictor(BasePredictor):

    # The dependencies you usually write in requirements.txt
    requirement_dependency = ["numpy","torch","transformers","accelerate"]

    # The dependencies you usually do `apt install` with
    system_dependency = ["wget"]

    def setup(self):
        # setup your model here, load models weights, also do other initialization setup
        self.logger = logging.getLogger()
        self.logger.setLevel("DEBUG")
        self.logger.debug("Setup model your model here")
        self.generator = pipeline("text-generation", model="gpt2")
        self.logger.debug("Model setup completed")
        
        

    # limit the number of threads runnig, the more threads the more GRAM it will be used when doing predictions
    @thread_limit(1)
    def predict(self, prompt: str = Input(description="text to generate")) -> List[Dict[str,str]]:
        # start prediction
        self.logger.debug("predicting...")
        result = self.generator(
            f"Hello, I'm a language model,{prompt}",
            max_length=80,
            num_return_sequences=1,
        )
        return result
```
### `predictor.py`介绍
`Predictor`类继承于`BasePredictor`,并`override`了`setup()`和`predict()`方法.


* `setup()` 方法用于加载模型和权重,以及创建一些后期需要的变量比如`logger`等. 此方法只会被调用一次在服务器初始化的时候. 示例中我们在`setup()`方法中使用transformers库加载`gpt-2`模型.
  
* `predict()` 复写方法用于实现推理过程, 上面示例中我们输入一个`prompt`让`gpt-2`模型生成几个句子,并返回结果.
  
### predict()方法 参数介绍

#### 入参
`predict()`方法支持自定义入参,您需要为每个参数标注类型,该方法支持以下类型作为输入.
    
* str 字符串
* int 整数
* float 浮点数
* bool 布尔值
* Path: 文件路径或者URI

您还可以使用 `Input()` 函数为输入提供更多信息，如上所示。它接受以下基本参数：

* description: 为模型用户描述该输入的用途
* default: 设置该参数的默认值。如果未传递此参数，则该输入为必需项。如果显式设置为 None，则该输入为可选项。
* ge: 对于 int 或 float 类型，输入值应大于或等于该数值。
* le: 对于 int 或 float 类型，输入值应小于或等于该数值。
* choices: 对于 str 或 int 类型，提供该输入的可能值列表`["选项1","选项2","选项3"]`。
  
  
`thread_limit()`annotaion可以添加到`predict()`方法上, 目的是限制并发线程数保证显存不被撑暴. 移除`thread_limit`侧代表并发数没有限制.

#### 出参
您也可以基于`BaseModel`自定义输出参数的类型
  
```python
from rockai import BaseModel,Path

class MyOutput(BaseModel):
    image_name:str
    image_file:Path

class Predictor(BaseModel):
    def setup(self):
        ...
    def predict(self,prompt:str)->MyOutput:
        ...
        return MyOutput('xxx',Path("output.png"))
```
  


#### 本地调试

如果需要在本地调试我们可以输入以下命令, 它会启动一个FastAPI 服务器,我们可以通过http接口来调用模型.

```bash
# 启动 FastAPI server
$ rockai start --file predictor.py

INFO:     Started server process [71572]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
`rockai start` 命令支持多种参数

* --port 更改服务器端口, 默认为 `8000`
* --file 更改`predictor.py`文件路径, 默认为`predictor.py`
* --auth 开发者可以输入一个`token`, 用于接口调用时的身份验证例如`--auth abcdefg`. 当发送请求时需要在header中加入`Authorization: Bearer abcdegf`来进行身份验证.

当FastAPI服务器启动完成后我们可以使用`curl` `Postman`等工具来调用推理接口, 也在浏览器中打开 http://localhost:8000/docs 可以查看接口swagger文档.


调用推理接口示例
```bash
curl --location 'http://localhost:8000/predictions' \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "prompt": "this is test"
    }
}'
```

返回结果
```json
{
    "input": {
        "prompt": "this is test"
    },
    "output": [
        {
            "generated_text": "Hello, I'm a language model,this is test-heavy. In the last week, in some cases my classes are still being used. So I have a great deal of time on my hands"
        }
    ],
    "id": "af7c50f1461a416fa878db37779b8c4b",
    "started_at": "2024-09-03T16:17:08.535968",
    "completed_at": "2024-09-03T16:17:13.578170",
    "inference_time": 5.042202,
    "logs": null,
    "error": null,
    "metrics": null
}
```


#### 上传至云端

RockAI 支持将模型打包并上传至云端以Serverless形式在GPU上运行

```bash
# 将模型打包成Docker镜像, 没有安装Docker的话需要先安装Docker并启动Docker. 登录后获取user-name, 并给你的模型起一个名字填入model-name中,例如: r.18h.online/xiaoming/hotdog-detector

$ rockai build --name r.18h.online/<your-user-name>/<model-name> --file predictor.py
```

`rockai build` 命令支持多种参数

* `--port` 选填：API 服务器的端口号 [默认值：8000]
  
* `--name` 必填：Docker 容器的镜像名称，例如：r.18h.online/jian-yang/hotdog-detector [默认值：无]
  
* `--file` 选填：`predictor.py` 文件的路径，默认为 `predictor.py` [默认值：predictor.py]
  
* `--gpu`或者`--no-gpu` 选填：是否使用 GPU [默认值：gpu]
  
* `--platform` 选填：Docker 镜像支持的CPU架构，默认为 `linux/amd64`, 也可以更改为其他平台如 `linux/arm64/v8` [默认值：linux/amd64]
  
* `--dry-run`或者`--no-dry-run`：生成 Docker 文件但不构建镜像 [默认值：--no-dry-run]
  
* `--help`：显示帮助信息


打包完成后可以上传模型到RockAI平台,首先去rockai.online获取api-token然后用一下命令登录.

```bash
$ rockai login
#复制api-token并回车
```

上传模型
```bash
$ rockai push r.18h.online/<your-user-name>/<model-name>
#等待上传...
#上传完成后可以在https://rockai.online/models/<your-user-name>/<model-name>访问你的模型
```