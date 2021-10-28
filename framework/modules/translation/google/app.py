import requests
from framework.modules.bases.log import *


@singleton
class google_translation(object):
    def __init__(self):
        self._url = GET_CONF_EX("translate", "url", "https://translation.googleapis.com/language/translate/v2")
        self._payload = {
            'target': GET_CONF_EX("translate", "target", "auto"),
            'format': GET_CONF_EX("translate", "format", "text"),
            'key': GET_CONF_EX("translate", "apikey", "AIzaSyBMkMuaH6CgcP52WfC2q9X9GwUaHVU7qZ8"),
            'source': GET_CONF_EX("translate", "source", "en")}
        self._headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    @log("translate")
    def fy(self, q):
        self._payload['q'] = q
        for i in range(1, int(GET_CONF_EX("translate", "try", 3))):
            try:
                response = requests.request("POST", self._url, headers=self._headers, data=self._payload).json()
                return response["data"]["translations"][0]["translatedText"]
            except Exception as e:
                time.sleep(3)
                continue
        return ""


if __name__ == '__main__':
    s = ""

    translation = google_translation()
    print(translation.fy(s))