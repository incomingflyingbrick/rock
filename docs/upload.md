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
  
  - `predict()`方法支持自定义入参,您需要为每个参数标注类型,该方法支持以下类型作为入参.
    
    * str 字符串
    * int 整数
    * float 浮点数
    * bool 布尔值
    * Path: 文件路径或者uri
  - 您还可以使用 `Input()` 函数为输入提供更多信息，如上所示。它接受以下基本参数：

    * description: 为模型用户描述该输入的用途
    * default: 设置该参数的默认值。如果未传递此参数，则该输入为必需项。如果显式设置为 None，则该输入为可选项。
    * ge: 对于 int 或 float 类型，输入值应大于或等于该数值。
    * le: 对于 int 或 float 类型，输入值应小于或等于该数值。
    * choices: 对于 str 或 int 类型，提供该输入的可能值列表`["选项1","选项2","选项3"]`。
* `thread_limit()`注释可以添加到`predict()`方法上,目的是限制并发线程数保证显存不被撑暴.移除`thread_limit`侧代表并发数没有限制.

## 上传模型到云端
