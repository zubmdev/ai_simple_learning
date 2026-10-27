import json
import urllib.error
import urllib.request

API_BASE = "https://api.telegram.org"


def mask(text, token):
    if token:
        text = text.replace(token, "***")
    return text


def post_raw(token, method, data, headers, timeout=120):
    url = f"{API_BASE}/bot{token}/{method}"
    request = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")
        raise RuntimeError(f"{method}: HTTP {error.code}: {mask(body, token)}")
    except OSError as error:
        raise RuntimeError(f"{method}: {mask(str(error), token)}")
    except json.JSONDecodeError:
        raise RuntimeError(f"{method}: некорректный JSON-ответ")


def post_json(token, method, payload, timeout=30):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return post_raw(token, method, data, {"Content-Type": "application/json"}, timeout)
