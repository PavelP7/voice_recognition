from pathlib import Path

BASE_PATH = str(Path(__file__).resolve().parent) + '/'
MEDIA_PATH = BASE_PATH + "media/"

YANDEX_BUCKET = "voice-recognize-bucket"
YANDEX_URL_ENDPOINT = "https://storage.yandexcloud.net/"
YANDEX_URL_UPLOAD = YANDEX_URL_ENDPOINT + YANDEX_BUCKET
YANDEX_URL_GET = "https://operation.api.cloud.yandex.net/operations/"
YANDEX_URL_API_V2 = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"
YANDEX_API_KEY = "AQVN0bookfZv2pY7Jcsmg3RxKFJ1SoBuJLRoW-zQ"

