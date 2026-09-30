import logging
import requests
import threading

from backend.util.file import get_config


def query_silicon_flow(input_text, sys_text, temperature):
    config = get_config()
    url = config.get('url', 'https://api.siliconflow.cn/v1/chat/completions') +'/chat/completions'
    key = config.get('apikey', '')
    model = config.get('model', 'Qwen/Qwen2.5-7B-Instruct')
    messages = []
    if sys_text:
        messages.append({"role": "system", "content": sys_text})
    messages.append({"role": "user", "content": input_text})

    logging.debug(f"query siliconflow model {model}")
    request_body = {
        "temperature": temperature,
        "messages": messages,
        "model": model,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }

    response = requests.post(url, headers=headers, json=request_body)

    if response.status_code != 200:
        raise Exception(f"Unexpected response status: {response.status_code}, modelName {model}")

    response_data = response.json()
    if 'choices' in response_data and len(response_data['choices']) > 0:
        logging.debug(f"siliconflow model {model}, response {response_data['choices'][0]['message']['content']}")
        return response_data['choices'][0]['message']['content']
    else:
        raise Exception("No choices found in response.")
