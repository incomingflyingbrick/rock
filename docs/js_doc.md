# RockAI JavaScript SDK

使用RockAI SDK来调用大模型更为简单.

## 快速开始

### 设置 ROCKAI_API_TOKEN 环境变量

```sh
export ROCKAI_API_TOKEN=5361e**********************a5738
```

登录RockAI后点击 [获取API_TOKEN](https://www.rockai.online/setting/token)

### 安装 RockAI 的 SDK 客户端库

```sh
npm install rockai-cli-app
```

### 导入并设置客户端

```javascript
import RockAI from "rockai-cli-app";
const rockAI = new RockAI();
```

### 使用 RockAI 的 API 运行 meta / meta-llama-3-70b-instruct

模型version及input可以在 [模型详情页](https://www.rockai.online/models/meta/meta-llama-3-70b-instruct/)查看

```javascript
import RockAI from "rockai-cli-app";
const rockAI = new RockAI();
const version =
  "fbfb20b472b2f3bdd101412a9f70a0ed4fc0ced78a77ff00970ee7a2383c575d";
const input = {
  top_p: 0.9,
  prompt:
    "Work through this problem step by step:\n\nQ: Sarah has 7 llamas. Her friend gives her 3 more trucks of llamas. Each truck has 5 llamas. How many llamas does Sarah have in total?",
  max_tokens: 512,
  min_tokens: 0,
  temperature: 0.6,
  prompt_template:
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
  presence_penalty: 1.15,
  frequency_penalty: 0.2,
};
const res = await rockAI.run({
  version,
  input,
});
```

## API

### Constructor

```javascript
const rockAI = new RockAI(options);
```

| name                | type     | description                                            |
| ------------------- | -------- | ------------------------------------------------------ |
| `options.api_token` | string   | API token 默认会去取环境变量中的 ROCKAI_API_TOKEN 字段 |
| `options.fetch`     | function | 请求使用的方法,默认为`globalThis.fetch`                |

web端和node v18 天生支持`fetch`,针对更早版本的node环境需要传入`fetch`参数

```javascript
const fetch = require("node-fetch");
const rockAI = new RockAI({ fetch });
```

### rockAI.run

```javascript
const output = await rockAI.run(options);
```

| name              | type   | description                    |
| ----------------- | ------ | ------------------------------ |
| `options.version` | string | 模型版本号, 默认为 latest 版本 |
| `options.input`   | object | `必填` 模型输入                |

### rockAI.stream

| name              | type   | description                           |
| ----------------- | ------ | ------------------------------------- |
| `options.version` | string | `必填` 模型版本号, 默认为 latest 版本 |
| `options.input`   | object | `必填` 模型输入                       |

### rockAI.predictions.create

```javascript
const response = await rockAI.predictions.create(options);
```

| name                            | type     | description                                                      |
| ------------------------------- | -------- | ---------------------------------------------------------------- |
| `options.version`               | string   | `必填` 模型版本号, 默认为 latest 版本                            |
| `options.input`                 | object   | `必填` 模型输入                                                  |
| `options.webhook`               | string   | 用于 predictions 有新输出时接收webhooks的 URL                    |
| `options.webhook_events_filter` | string[] | 触发 webhook 事件数组 允许: `start` `output` ` logs` `completed` |

### rockAI.predictions.get

```javascript
const response = await rockAI.predictions.get(predictionsId);
```

| name            | type   | description   |
| --------------- | ------ | ------------- |
| `predictionsId` | string | `必填` 推理ID |

### rockAI.predictions.cancel

```javascript
const response = await rockAI.predictions.cancel(predictionsId);
```

| name            | type   | description   |
| --------------- | ------ | ------------- |
| `predictionsId` | string | `必填` 推理ID |
