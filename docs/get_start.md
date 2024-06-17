# HTTP API 
调用机器学习模型只需要一个简单的API


## 鉴权

所有 API 请求都必须使用令牌进行身份验证。请在所有请求中包含以下标头：

=== "Example"

```python
Authorization: Bearer <将API_KEY放在这里>
```

## 开始预测

您可以使用以下 API 创建预测，它将返回预测是否创建成功。

=== "Python"

```python
import requests
import json

url = "https://api.rockai.online/v1/predictions"
# 填入version和input, 具体参数请参考模型详情页
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

## 获取预测结果
可以使用预测 id 从服务器获取预测结果。

=== "Python"
```python
import requests

#将id添加到url后面
url = "https://api.rockai.online/v1/predictions/{id}"

payload = {}
headers = {
    'Authorization': 'Bearer <将API_KEY放在这里>'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```

## 取消进行中的预测

您也可以使用预测 id 取消预测。

=== "Python"
```python
import requests

url = "https://api.rockai.online/v1/predictions/{id}/cancel"

payload = {}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```
