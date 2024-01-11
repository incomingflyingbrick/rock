# Getting Started

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## HTTP API

### Authentication

All API requests must be authenticated with a token. Include this header with all requests:

```python
Authorization: Bearer <paste-your-api-key-here>
```

### Create a prediction

```python
import requests
import json

url = "https://inf-test-dev-mhvxow5uwq-de.a.run.app/v1/predictions"

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

print(response.text)

```

### Get a prediction

```python
import requests

url = "https://inf-test-dev-mhvxow5uwq-de.a.run.app/v1/predictions/ujebapbbulzpx25442efjv4qba"

payload = {}
headers = {
    'Authorization': 'Bearer <paste-your-token-here>'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```

### Cancel a prediction

```python
import requests

url = "https://inf-test-dev-mhvxow5uwq-de.a.run.app/v1/predictions/eoyokbzbm3yfdhpspr5xak24ye/cancel"

payload = {}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

### Run a model

```python
import requests
import json

url = "https://inf-test-dev-mhvxow5uwq-de.a.run.app/v1/run"

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

### Run a model with server side event

```python
import requests
import json

url = "https://inf-test-dev-mhvxow5uwq-de.a.run.app/v1/run_sse"

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