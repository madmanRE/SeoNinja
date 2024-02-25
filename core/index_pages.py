import datetime
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import os
from typing import List


SCOPES = ["https://www.googleapis.com/auth/indexing"]


def indexURL2(u, http):
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    content = {"url": u.strip(), "type": "URL_UPDATED"}
    json_ctn = json.dumps(content)
    response, content = http.request(ENDPOINT, method="POST", body=json_ctn)
    result = json.loads(content.decode())
    return "OK"


def list_urls_to_index(urls: List[str]) -> None:
    json_key = "core/service_account.json"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_key, scopes=SCOPES
    )
    http = credentials.authorize(httplib2.Http())
    for url in urls:
        indexURL2(url.strip(), http)
    print("Отправлено на индексацию: " + str(len(urls)) + " шт.")
