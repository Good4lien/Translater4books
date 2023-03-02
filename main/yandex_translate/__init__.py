# coding: utf-8

import requests
from requests.exceptions import ConnectionError


class YandexTranslateException(Exception):
  """
  Default YandexTranslate exception
  """
  error_codes = {
    401: "ERR_KEY_INVALID",
    402: "ERR_KEY_BLOCKED",
    403: "ERR_DAILY_REQ_LIMIT_EXCEEDED",
    404: "ERR_DAILY_CHAR_LIMIT_EXCEEDED",
    413: "ERR_TEXT_TOO_LONG",
    422: "ERR_UNPROCESSABLE_TEXT",
    501: "ERR_LANG_NOT_SUPPORTED",
    503: "ERR_SERVICE_NOT_AVAIBLE",
  }

  def __init__(self, status_code, *args, **kwargs):
    message = self.error_codes.get(status_code)
    super(YandexTranslateException, self).__init__(message, *args, **kwargs)


class YandexTranslate(object):

  api_url = "https://translate.yandex.net/api/{version}/tr.json/{endpoint}"
  api_version = "v1.5"
  api_endpoints = {
    "langs": "getLangs",
    "detect": "detect",
    "translate": "translate",
  }

  def __init__(self, key=None):
    """
    >>> translate = YandexTranslate("trnsl.1.1.20130421T140201Z.323e508a33e9d84b.f1e0d9ca9bcd0a00b0ef71d82e6cf4158183d09e")
    >>> len(translate.api_endpoints)
    3
    >>> len(translate.error_codes)
    8
    """
    if not key:
      raise YandexTranslateException(401)
    self.api_key = key

  def url(self, endpoint):
    """
    Returns full URL for specified API endpoint
    >>> translate = YandexTranslate("trnsl.1.1.20130421T140201Z.323e508a33e9d84b.f1e0d9ca9bcd0a00b0ef71d82e6cf4158183d09e")
    >>> translate.url("langs")
    "https://translate.yandex.net/api/v1.5/tr.json/getLangs"
    >>> translate.url("detect")
    "https://translate.yandex.net/api/v1.5/tr.json/detect"
    >>> translate.url("translate")
    "https://translate.yandex.net/api/v1.5/tr.json/translate"
    """
    return self.api_url.format(version=self.api_version,
                   endpoint=self.api_endpoints[endpoint])

  @property
  def directions(self):
    """
    Returns list with translate directions
    >>> translate = YandexTranslate("trnsl.1.1.20130421T140201Z.323e508a33e9d84b.f1e0d9ca9bcd0a00b0ef71d82e6cf4158183d09e")
    >>> directions = translate.directions
    >>> len(directions) > 0
    True
    """
    try:
      response = requests.get(self.url("langs"), params={"key": self.api_key})
      response = response.json()
    except ConnectionError:
      raise YandexTranslateException(self.error_codes[503])
    status_code = response.get("code", 200)
    if not status_code is 200:
      raise YandexTranslateException(status_code)
    return response.get("dirs")

  @property
  def langs(self):
    """
    Returns list with supported languages
    >>> translate = YandexTranslate("trnsl.1.1.20130421T140201Z.323e508a33e9d84b.f1e0d9ca9bcd0a00b0ef71d82e6cf4158183d09e")
    >>> languages = translate.langs
    >>> len(languages) > 0
    True
    """
    return set(x.split("-")[0] for x in self.directions)

  def detect(self, text, format="plain"):
    """
    Specifies language of text
    >>> translate = YandexTranslate("trnsl.1.1.20130421T140201Z.323e508a33e9d84b.f1e0d9ca9bcd0a00b0ef71d82e6cf4158183d09e")
    >>> result = translate.detect(text="Hello world!")
    >>> result == "en"
    True
    >>> translate.detect("なのです")
    Traceback (most recent call last):
    YandexTranslateException: ERR_LANG_NOT_SUPPORTED
    """
    data = {
      "text": text,
      "format": format,
      "key": self.api_key,
    }
    try:
      response = requests.post(self.url("detect"), data=data)
      response = response.json()
    except ConnectionError:
      raise YandexTranslateException(self.error_codes[503])
    except ValueError:
      raise YandexTranslateException(response)
    language = response.get("lang", None)
    status_code = response.get("code", 200)
    if not status_code is 200:
      raise YandexTranslateException(status_code)
    elif not language:
      raise YandexTranslateException(501)
    return language

  def translate(self, text, lang, format="plain"):
    """
    Translates text to passed language
    >>> translate = YandexTranslate("trnsl.1.1.20130421T140201Z.323e508a33e9d84b.f1e0d9ca9bcd0a00b0ef71d82e6cf4158183d09e")
    >>> result = translate.translate(lang="ru", text="Hello, world!")
    >>> result["code"] == 200
    True
    >>> result["lang"] == "en-ru"
    True
    >>> result = translate.translate("なのです", "en")
    Traceback (most recent call last):
    YandexTranslateException: ERR_LANG_NOT_SUPPORTED
    """
    data = {
      "text": text,
      "format": format,
      "lang": lang,
      "key": self.api_key
    }
    try:
      response = requests.post(self.url("translate"), data=data)
      response = response.json()
    except ConnectionError:
      raise YandexTranslateException(503)
    status_code = response.get("code", 200)
    if not status_code is 200:
      raise YandexTranslateException(status_code)
    return response

if __name__ == "__main__":
  import doctest
  doctest.testmod()
