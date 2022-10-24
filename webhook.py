import json

import requests
from discord import File, SyncWebhook


def send_file_to_webhook(webhook_url, filePath):

    headers = {
        'Content-Type': "application/json",

        # 'Content-Type': "multipart/form-data",
        # 'Content-Disposition': f"form-data; name='file0'; filename='${filePath}' Content-Type:text/html; charset=UTF-8"
    }

    # TODO: actually sending the file instead of just the content

    with open(filePath, 'r', encoding='utf-8') as file:
        data = file.read()
        payload = {
            'content': f'```\n{data}```',
        }

        r = requests.post(webhook_url, headers=headers,
                          data=json.dumps(payload))
        print(r.status_code)
