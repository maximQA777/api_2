import requests
import json
from allure_commons.types import AttachmentType
import logging
import allure
from allure_commons._allure import step

from test.conftest import BASE_URL
LOGIN = "alabai.vfrcbv2001@mail.ru"
PASSWORD = "Maks123"


class BaseApiClient:

    @staticmethod
    def api_request(endpoint, method="GET", data=None, params=None, allow_redirects=None, cookies=None):
        url = BASE_URL + endpoint

        with step(f"API-запрос: {method} {url}"):
            result = requests.request(
                method=method,
                url=url,
                data=data,
                params=params,
                allow_redirects=allow_redirects,
                cookies=cookies,
            )

            # Прикрепляем информацию о запросе
            allure.attach(
                body=f"URL: {result.request.url}\nМетод: {result.request.method}\nТело запроса: {result.request.body}",
                name="Запрос",
                attachment_type=AttachmentType.TEXT,
                extension="txt",
            )

            # Прикрепляем куки
            allure.attach(
                body=str(result.cookies),
                name="Куки (cookies)",
                attachment_type=AttachmentType.TEXT,
                extension="txt",
            )

            # Прикрепляем ответ
            try:
                response_json = result.json()
                allure.attach(
                    body=json.dumps(response_json, indent=4, ensure_ascii=False),
                    name="Ответ (JSON)",
                    attachment_type=AttachmentType.JSON,
                    extension="json",
                )
                logging.info(json.dumps(response_json, indent=4, ensure_ascii=False))
            except ValueError:
                allure.attach(
                    body=result.text,
                    name="Ответ (текст)",
                    attachment_type=AttachmentType.TEXT,
                    extension="txt",
                )
                logging.info(result.text if result.text else "None")

            logging.info(f"Статус-код: {result.status_code}")
            return result