# 开始
调用机器学习模型只需要一个简单的API
## HTTP API

### 鉴权

所有 API 请求都必须使用令牌进行身份验证。请在所有请求中包含以下标头：

=== "Example"

```python
Authorization: Bearer <将API_KEY放在这里>
```

### 开始预测

您可以使用以下 API 创建预测，它将返回预测是否创建成功。

=== "Python"

```python
import requests
import json

url = "api.rockai.online/v1/predictions"

payload = json.dumps({
    "version": "5821a338d00033abaaba89080a17eb8783d9a17ed710a6b4246a18e0900ccad4",
    "input": {
        "image": "https://replicate.delivery/pbxt/KAaJWyluKBrWzbe5EhQArYZcVXdpOvcLyF81menWifyusgCe/1.jpeg",
        "prompt": "Several statues made of porcelain chunks and gold mendings, the face of the statues have lips and eyes, the eyes are blinking, the lips are opening like the statues are talking, the head of the statues are turning towards the camera",
        "max_frames": 16,
        "guidance_scale": 9,
        "num_inference_steps": 50
    }
})
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <paste-your-token-here>'
}

response = requests.request("POST", url, headers=headers, data=payload)
#从结果里面获取预测id
print(response.text)

```

### 获取预测结果
可以使用预测 id 从服务器获取预测结果。

=== "Python"
```python
import requests

#将id添加到url后面
url = "api.rockai.online/v1/predictions/ujebapbbulzpx25442efjv4qba"

payload = {}
headers = {
    'Authorization': 'Bearer <将API_KEY放在这里>'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```

### 取消进行中的预测

您也可以使用预测 id 取消预测。

=== "Python"
```python
import requests

url = "api.rockai.online/v1/predictions/eoyokbzbm3yfdhpspr5xak24ye/cancel"

payload = {}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

### 调用模型并直接返回结果

您可以使用此 API 对模型进行推理，模型将将直接返回结果。

=== "Python"
```python
import requests
import json

url = "api.rockai.online/v1/run"

payload = json.dumps({
    "model": "mistralai/mistral-7b-instruct-v0.1:5fe0a3d7ac2852264a25279d1dfb798acbc4d49711d126646594e212cb821749",
    "input": {
        "top_k": 50,
        "top_p": 0.9,
        "prompt": "Can you write me a poem about steamed hams?",
        "temperature": 0.7,
        "max_new_tokens": 500,
        "min_new_tokens": -1,
        "prompt_template": "{prompt}",
        "repetition_penalty": 1.15
    }
})
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <paste-your-token-here>'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

### 运行模型(流式 server side event)

如果您可以使用像 llama-2-7b-chat 这样的语言模型，您可以使用此 API 通过服务器端事件获取结果。

=== "Python"
```python
import requests
import json

url = "api.rockai.online/v1/run_sse"

payload = json.dumps({
    "model": "meta/llama-2-7b-chat:f1d50bb24186c52daae319ca8366e53debdaa9e0ae7ff976e918df752732ccc4",
    "input": {
        "top_p": 1,
        "prompt": "Plan a day of sightseeing for me in San Francisco. ",
        "temperature": 0.75,
        "system_prompt": "You are an old-timey gold prospector who came to San Francisco for the gold rush and then was teleported to the present day. Despite being from 1849, you have great knowledge of present-day San Francisco and its attractions. You are helpful, polite, and prone to rambling. ",
        "max_new_tokens": 800,
        "repetition_penalty": 1
    }
})
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <paste-your-token-here>'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```


