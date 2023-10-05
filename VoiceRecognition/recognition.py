import requests
from audio import record, choose_microphone, OUTPUT_FILE_NAME
from settings import *
import boto3

headers_api_v2 = {'Content-Type': 'application/json', 'Authorization': f'Api-Key {YANDEX_API_KEY}'}
headers_get = {'Authorization': f'Api-Key {YANDEX_API_KEY}'}
body_api_v2 = {
    "config": {
        "specification": {
            "languageCode": "ru-RU",
            "model": "general",
            "profanityFilter": "false",
            "audioEncoding": "MP3"
        }
    },
    "audio": {
        "uri": YANDEX_URL_ENDPOINT + YANDEX_BUCKET + '/' + OUTPUT_FILE_NAME
    }
}
def run(second: int, mc_id: int) -> str:
    output = record(second, mc_id)

    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=YANDEX_URL_ENDPOINT
    )

    with open(MEDIA_PATH + output, 'rb') as f:
        s3.put_object(Bucket=YANDEX_BUCKET, Key=output, Body=f.read(), StorageClass='STANDARD')

    response = requests.post(url=YANDEX_URL_API_V2, json=body_api_v2, headers=headers_api_v2)
    response_json = dict(response.json())
    object_id = response_json['id'] if response.status_code == 200 else None
    if object_id:
        response_get: str
        response_json: dict
        while True:
            response_get = requests.get(url=YANDEX_URL_GET+str(object_id), headers=headers_get)
            response_json = dict(response_get.json())
            if response_json['done']:
                break
        if 'chunks' in response_json['response'].keys():
            return response_json['response']['chunks'][0]['alternatives'][0]['text']
        else:
            return "Не понимаю, повторите"

    return "Нет ответа от сервера"

if __name__ == '__main__':
    print("Выберите идентификатор микрофона")
    choose_microphone()
    mc_id = int(input())

    while (inp := input("""Возможные команды:
- время записи в секундах
- exit для завершения
""")) != 'exit':
        if inp.isdigit():
            second = int(inp)
            result = run(second, mc_id)
            print(result)
        else:
            print("Некорректная команда")
