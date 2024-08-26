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

* `output` 模型输出的内容

### 参数

* id `必传` `string` 预测id ，根据id查询结果。
  



