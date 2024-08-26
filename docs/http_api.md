# HTTP API 
调用机器学习模型只需要一个简单的API


## 鉴权

所有 API 请求都必须使用令牌进行身份验证。请在所有请求的header中加入以下字段.

=== "Header样例"
```
Authorization: Bearer {API_TOKEN}
```

## 调用模型
### 接口
```
POST https://api.rockai.online/v1/predictions
```
### 接口详情
当我们需要调用一个模型的时候需要先创建一个预测, 这里用一个图片生成模型(text-to-image)举例. 开发者需要传入调用的模型名称和模型所需的参数`input`即可。
这里的flux-1-schenll模型需要一个`prompt`作为参数。其他的模型需要在`input`字段中传入不同的参数，具体可以根据模型的schema来判断需要传入什么参数.

### 请求样例
=== "Body"
```json
{
  "model": "incomingflyingbrick/flux-1-schnell",
  "input": {
    "prompt": "帮我生成一张图片,一只狗在天上飞"
  }
}
```
### 参数
* input `必传` `object` 参数需要根据模型的schema来确定
* stream `非必传` `boolean` (当调用大语言模型时可以使用server-side-event来接受返回结果,默认为`false`)
* model `必传` `string` 
* version `非必传` `string` (如果已经传入`model`择可以不传`version`,系统会默认选择最新版本,开发者也可以自己指定`version`)
=== "返回示例"

```json
{
    "id": "66c7fc393326fee0bd22e159",
    "model": "incomingflyingbrickdev/flux-1-schnell",
    "version": "0a01391e720622130aab656dc27120dce1b2402c5194dce4e494a71c6ddff4b5",
    "created_at": "2024-08-15T02:54:06.094504",
    "webhook": null,
    "webhook_events_filter": null,
    "input": {
        "prompt": "帮我生成一张图片,一只狗在天上飞"
    },
    "stream": false,
    "output": null,
    "urls": {
        "get": "https://api.rockai.online/v1/predictions/66c7fc393326fee0bd22e159",
        "stream": "https://api.rockai.online/v1/predictions/stream/66c7fc393326fee0bd22e159"
    },
    "logs": "",
    "status": "starting",
    "error": "",
    "metrics": null
}
```

## 获取模型输出结果
### 接口
```
GET https://api.rockai.online/v1/predictions/{id}
```

### 参数

* id `必传` `string` 预测id ，根据id查询结果。


### 接口详情
根据 *id* 来获取模型输出的结果, *id* 可从 `创建预测` 接口的返回结果中获取.

=== "结果样例"
```json
{
  "model": "incomingflyingbrickdev/flux-1-schnell",
  "version": "0a01391e720622130aab656dc27120dce1b2402c5194dce4e494a71c6ddff4b5",
  "created_at": "2024-08-15T02:54:06.094000",
  "webhook": null,
  "webhook_events_filter": null,
  "input": {
    "prompt": "帮我生成一张图片,一只狗在天上飞"
  },
  "stream": false,
  "output": "https://example.com/image/output.png",
  "urls": {
    "get": "https://api.rockai.online/v1/predictions/66c7fc393326fee0bd22e159",
    "stream": "https://api.rockai.online/v1/predictions/stream/66c7fc393326fee0bd22e159"
  },
  "logs": "",
  "status": "succeeded",
  "error": "",
  "metrics": {
    "predict_time": 0.017392
  },
  "completed_at": "2024-08-23T03:04:30.867349",
  "started_at": "2024-08-23T03:04:30.849957"
}
```

* `status` 包括以下几种状态

| 状态                 | 描述                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------ |
| starting（启动中）   | 模型正在启动中(冷启动), 此状态持续时间通常为几分钟到十几分钟不等, 大型模型的加载时间会更长 |
| processing（处理中） | 模型的 predict() 方法正在运行                                                              |
| succeeded（成功）    | 预测成功完成, 没有报错                                                                     |
| failed（失败）       | 预测在处理过程中遇到错误                                                                   |
| canceled（已取消）   | 预测已被创建者取消                                                                         |

* `output` 模型输出的内容 (如果模型输出的是一个url文件下载地址, 例如 **https://webui-objects.s3.amazonaws.com/8606fec283b84951af0b1e4969a3121ctest.png** ,此文件会被保存在RockAI的存储服务器中,有效期一小时，过期自动删除)


  

## 文件上传

### 接口
```
GET https://api.rockai.online/v1/get_presign_url?file_name={example_image.jpg}
```

### 请求参数
* file_name `必传` `string` 文件名 示例：example_image.jpg

### 接口详情
如果某个模型的输入参数为url, 例如 image-to-image 模型通常需要开发者提供一张图片来做推理。如果你只有一张图片并且没有这张图片的下载地址，你可以将这个图片上传到RockAI的存储服务器中，存储服务器会自动为上传的文件生成一个下载链接, 我们可以将这个下载链接喂给模型.

此接口调用成功会返回两个字段，`put_url`和`get_url`, 当我们拿到`put_url`之后就可以开始上传文件了, 开发者需要用`PUT`请求来请求`put_url`,并在`data`中加入需要上传的文件, 上传示例请参考下面代码. get_url是该文件的下载地址，开发者需要将get_url的地址喂给模型，这样模型就可以下载文件并开始推理.

=== "返回结果"
```json
// 请求 /v1/get_presign_url 并拿到put_url和get_url
{
    "data": {
        "put_url": "https://webui-objects.s3.amazonaws.com/8606fec283b84951af0b1e4969a3121ctest.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQQA3W6XQDU4SAUOM%2F20240826%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240826T071600Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=afb8b173319e101b5c1b161f76ad132a1c4511f0977ea9afecf34b4e22709fc6",
        "get_url": "https://webui-objects.s3.amazonaws.com/8606fec283b84951af0b1e4969a3121ctest.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQQA3W6XQDU4SAUOM%2F20240826%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240826T071600Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=53ffb6d01d00e49b15a8b8efbf097ce3d86a050f94ee80bcb5af9820c3b6dd78"
    },
    "msg": "success",
    "code": 200
}
```

=== "文件上传示例Python"
```python
# 开始上传文件
import requests

# 上一步获取的put_url
url = 'https://webui-objects.s3.amazonaws.com/8606fec283b84951af0b1e4969a3121ctest.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQQA3W6XQDU4SAUOM%2F20240826%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240826T071600Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=afb8b173319e101b5c1b161f76ad132a1c4511f0977ea9afecf34b4e22709fc6'

# 打开需要上传的文件
with open('example_image.jpg', 'rb') as file:
    # 发送PUT请求开始上传文件 
    response = requests.put(url, data=fil.read())

# 查看上传结果
if response.status_code == 200:
    print('Image uploaded successfully')
else:
    print(f'Failed to upload image. Status code: {response.status_code}')
    print(f'Response: {response.text}')


```

* put_url: 文件上传的地址, 开发者需用PUT请求请求此接口,将需要上传的文件放入data中
* get_url: 文件的下载地址，当开发者已经上传文件完成，可以调用此接口来下载自己的文件
* **文件在存储服务器中只会保存一小时,过期后将自动删除**






