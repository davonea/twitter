#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from framework.modules.bases.service_config import *


def postDoc(cat_name, title, content, num=None):
    url = GET_CONF("showdocs", "url")
    if num == None:
        num = 99
    payload = {'api_key': GET_CONF("showdocs", "api_key"),
               'api_token': GET_CONF("showdocs", "api_token"),
               'cat_name': cat_name,
               'page_title': title,
               'page_content': content,
               's_number': num}
    files = [

    ]
    headers = {
        'Cookie': 'PHPSESSID=819c660385010b6f2061f639f4d877cd'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


if __name__ == '__main__':
    postDoc()