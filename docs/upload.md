# 介绍

RockAI平台支持开发者自己上传模型并推理, 不需要购买GPU. 开发者可以使用我们提供的命令行工具制作一个Docker镜像. 当将镜像被上传到RockAI平台之后, 开发者就可以使用HTTP API, RockAI Python SDK, RockAI NodeJS SDK的方式调用模型.

## 上传教程示例

新建一个文件夹并创建一个虚拟环境, 如果您已经搭建好virtual enviroment可以跳过此步骤.

```bash
$ mkdir my_project
$ cd my_project
$ python -m venv env
$ source env/bin/activate
```

安装依赖库`rockai`, 推荐在virtual environment环境下安装.

```bash
# RockAI 支持的python版本为 3.9-3.12 版本
$ pip install -U rockai
$ rockai init
```

`rockai init`命令会在当前目录下生成`predictor.py` 和 `.dockerignore` 两个文件. 使用VSCode或其他IDE打开`predictor.py`文件. 我们可以看到以下内容.

```python
from rockai import BasePredictor, Input, thread_limit,List,Dict
import logging
from transformers import pipeline

class Predictor(BasePredictor):

    # The dependencies you usually write in requirements.txt
    requirement_dependency = ["torch","transformers","accelerate"]

    # The dependencies you usually do `apt install` with
    system_dependency = ["wget"]

    def setup(self):
        # setup your model here, load models weights, also do other initialization setup
        self.logger = logging.getLogger()
        self.logger.setLevel("DEBUG")
        self.generator = pipeline("text-generation", model="gpt2")
        self.logger.debug("Model setup complete")

    # limit the number of threads runnig, the more threads the more GRAM it will be used when doing predictions
    @thread_limit(1)
    def predict(self, prompt: str = Input(description="text to generate")) -> List[Dict[str,str]]:
        # start prediction
        self.logger.debug("Predicting...")
        result = self.generator(
            f"Hello, I'm a language model,{prompt}",
            max_length=100,
            num_return_sequences=1,
        )
        # return your result here
        return result

```
### `predictor.py`介绍

`Predictor`类继承于`BasePredictor`,并`override`了`setup()`和`predict()`方法.
开发者可以复写以下两个方法来实现模型加载和推理. 

* `setup()` 方法用于加载模型和权重,以及创建后期需要的变量比如`logger`等. 此方法只会被调用一次, 在服务器初始化的时候. 示例中我们在`setup()`方法中使用`transformers`库加载`gpt-2`模型.
  
* `predict()` 方法用于实现推理过程, 上面示例中我们输入一个`prompt`让`gpt-2`模型生成几个句子, 并返回结果.
  
### predict()方法 参数介绍

#### 入参
`predict()`方法支持自定义入参, 您必须为每个参数标注类型, 该方法支持以下类型作为输入.
    
* `str` 字符串
* `int` 整数
* `float` 浮点数
* `bool` 布尔值
* `Path`: 文件路径或者URI

您还可以使用 `Input()` 函数为输入提供更多信息, 如上所示它接受以下基本参数:

* `description`: 为模型用户描述该输入的用途
* `default`: 设置该参数的默认值.如果未传递此参数, 则该输入为必需项. 如果设置为 `None`, 则该输入为可选项.
* `ge`: 对于 `int` 或 `float` 类型, 输入值应大于或等于该数值.
* `le`: 对于 `int` 或 `float` 类型, 输入值应小于或等于该数值.
* `choices`: 对于 `str` 或 `int` 类型, 提供该输入的可能值列表`["选项1","选项2","选项3"]`.
  
  
`thread_limit()`annotaion可以添加到`predict()`方法上, 目的是限制并发线程数保证显存不被撑暴. 移除`thread_limit`侧代表并发数没有限制.

#### 出参
您也可以基于`BaseModel`自定义输出参数的类型
  
```python
from rockai import BaseModel,Path

class MyOutput(BaseModel):
    image_name:str # 输出为一个字符串
    image_file:Path # 输出为一个文件

class Predictor(BaseModel):
    def setup(self):
        ...
    def predict(self,prompt:str)->MyOutput:
        ...
        return MyOutput(image_name='xxx',image_file=Path("output.png"))
```

#### 依赖库安装

本地调试时开发者通常会使用`pip`或者`apt install`来安装各种依赖库, 在您安装好本地依赖库之后, 您还需要把库的名字写进以下两个`list`中. 如果您需要的依赖库没有加入到`requirement_dependency`或者`system_dependency`中则可能造成打包失败, 导致程序无法正常运行.


```python
class Predictor(BasePredictor):

    # 通常写在 requirements.txt 中的依赖项
    requirement_dependency = ["torch","transformers","accelerate"]

    # 通常使用 apt install 安装的依赖项
    system_dependency = ["wget"]

    #此处省略100字...
    ...
```


#### 本地调试

如果需要在本地调试我们可以输入以下命令, 它会启动一个`FastAPI`服务器, 我们可以通过`http`接口来调用模型.

在调试之前我们需要先安装依赖, 来保证程序可以正常运行.

```bash
$ pip install torch transformers accelerate -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

启动local development server

```bash
# 启动 FastAPI server
$ rockai start --file predictor.py

INFO:     Started server process [71572]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

`rockai start` 命令支持多种参数

* `--port` 更改服务器端口, 默认为 `8000`
* `--file` 更改`predictor.py`文件路径, 默认为`predictor.py`
* `--auth` 开发者可以输入一个`token`, 用于接口调用时的身份验证例如`--auth abcdefg`. 当发送请求时需要在header中加入`Authorization: Bearer abcdegf`来进行身份验证.

当FastAPI服务器启动完成后我们可以使用`curl`或者`Postman`等工具来调用推理接口, 也可以在浏览器中打开 `http://localhost:8000/docs` 可以查看swagger接口文档.


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

RockAI 支持将模型打包成为Docker镜像并上传至云端, 以Serverless形式在GPU上运行. (此步骤需要先安装Docker, 并启动Docker)

```bash
# 将模型打包成Docker镜像, 没有安装Docker的话需要先安装Docker并启动Docker. 登录后获取user-name, 并给你的模型起一个名字填入model-name中, 例如: r.18h.online/xiaoming/hotdog-detector

$ rockai build r.18h.online/<your-user-name>/<model-name> --file predictor.py
```

`rockai build` 命令支持多种参数

* `--port` 选填: API 服务器的端口号, 默认值: `8000`
  
* `--name` 必填: Docker镜像名称, 例如：`r.18h.online/jian-yang/hotdog-detector`
  
* `--file` 选填: `predictor.py` 文件的路径, 默认为: `predictor.py`
  
* `--gpu`或者`--no-gpu`二选一 选填: 是否使用 GPU 默认值: gpu
  
* `--platform` 选填: Docker镜像支持的CPU架构, 默认为 `linux/amd64`, 也可以更改为其他平台如 `linux/arm64/v8` 来支持Mac M2芯片, 详情请查看[Docker文档](https://docs.docker.com/reference/cli/docker/buildx/build/#platform)
  
* `--dry-run`或者`--no-dry-run`二选一: 生成Docker文件但不构建镜像, 默认值: --no-dry-run
  
* `--help`: 显示帮助信息

* `--upload-url` 选填: 文件上传的地址前缀,默认为 `https://api.rockai.online/v1/get_presign_url`, 需要加入query parameter `file_name`将文件名传入, 此地址必须支持`get`请求并返回格式为 `{"data":{"get_url":"http://","put_url":"http://"}}`的JSON, SDK会自动上传文件到`put_url`.


打包完成后可以上传模型到RockAI平台, 首先去[RockAI官网](https://dev.rockai.online/setting/token)获取`API Token`然后用以下命令登录.

```bash
$ rockai login
#根据提示粘贴API-Token并回车
```

也可以使用以下方式登录
```bash
$ rockai login --api-token <API_TOKEN>
```

上传模型
```bash
$ rockai push r.18h.online/<your-user-name>/<model-name>
#等待上传...
#上传完成后可以在https://rockai.online/models/<your-user-name>/<model-name>访问你的模型
```