import json
from urllib.parse import urljoin
import requests
from pprint import pprint
from datetime import datetime, timedelta
from objects import object_list as ol


url = "https://object.object.ru"
headers = {"Content-Type": "application/json; charset=UTF-8"}

username = "superuser_login"
password = "abc"

login_payload = f"username={username}&password={password}&clipped=true"
login_headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}

LOG_ENABLED = True
LOG_FILE = "log.txt"


def get_dates(container):
    result = []
    future_base_date = datetime.now() + timedelta(weeks=10)
    start_of_future_week = future_base_date - timedelta(days=future_base_date.weekday())

    for day_index in container["day_of_week"]:
        target_date = start_of_future_week + timedelta(days=day_index)

        for time_string in container["hour"]:
            hour, minute = map(int, time_string.split(":"))

            final_dt = target_date.replace(
                hour=hour, minute=minute, second=0, microsecond=0
            )
            result.append(final_dt.strftime("%Y-%m-%dT%H-%M"))

    return result


def login():
    try:
        response = requests.post(
            urljoin(url, "api/auth/let-me-in"),
            headers=login_headers,
            data=login_payload,
        )

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

    cookies = response.cookies

    write_log(
        [
            response.status_code,
            response.url,
            response.text,
        ]
    )

    return cookies


def get_status(cookies):
    try:
        response = requests.post(
            urljoin(url, "api/auth/status-check"),
            headers=headers,
            cookies=cookies,
        )

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

    json_data = response.json()

    return json_data


def object_create(
    containerId,
    warehouseId,
    tariffId,
    unitSpecificationId,
    unitRegistrationId,
    time_output,
    date_output,
    cookies,
):
    objects = [
        {
            "containerId": containerId,
            "warehouseId": warehouseId,
            "tariffId": tariffId,
            "unitSpecificationId": unitSpecificationId,
            "unitRegistrationId": unitRegistrationId,
            "time": time_output,  # "2026-02-10" time format
            "date": date_output,
        },
    ]

    try:
        response = requests.post(
            urljoin(url, "api/object"),
            headers=headers,
            cookies=cookies,
            json={
                "containerId": containerId,
                "objects": json.dumps(objects),  # "2026-02-10" time format
            },
        )

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

    resp = response.json()
    # print("creation complete")

    write_log(
        [
            response.status_code,
            response.url,
            response.json(),
        ]
    )

    return resp["data"]["ids"][0]


def object_set_new_data(
    containerId,
    objectId,
    dt_output,
    dt_now,
    cookies,
):

    try:
        response = requests.post(
            urljoin(url, "api/object-setting/set-new-data"),
            headers=headers,
            cookies=cookies,
            json={
                "containerId": containerId,
                "objects": [
                    {
                        "objectId": objectId,
                        "endSaleTime": dt_output,  # "22.09.2026 14:00" format
                        "beginSaleTime": dt_now,  # "22.09.2026 14:00" format
                    },
                ],
            },
        )

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

    resp = response.json()
    pprint(resp)

    write_log(
        [
            response.status_code,
            response.url,
            response.json(),
        ]
    )

    return resp


def write_log(data: list[str]):
    """Saving logs to a file"""
    if not LOG_ENABLED:
        return

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        for line in data:
            file.write(str(line))
            file.write(" ")
        file.write("\n")


def container_processor(
    containerId,
    warehouseId,
    tariffId,
    unitSpecificationId,
    unitRegistrationId,
    date_list,
):

    for object_datetime in date_list:
        dt_object = datetime.fromisoformat(object_datetime)
        date_output = dt_object.strftime("%d.%m.%Y")
        time_output = dt_object.strftime("%H:%M")
        dt_output = dt_object.strftime("%d.%m.%Y %H:%M")
        dt_now = datetime.now().strftime("%d.%m.%Y %H:%M")

        cookies = login()

        get_status(cookies=cookies)

        objectId = object_create(
            containerId=containerId,
            warehouseId=warehouseId,
            tariffId=tariffId,
            unitSpecificationId=unitSpecificationId,
            unitRegistrationId=unitRegistrationId,
            time_output=time_output,
            date_output=date_output,
            cookies=cookies,
        )

        object_set_new_data(
            containerId=containerId,
            objectId=objectId,
            dt_output=dt_output,
            dt_now=dt_now,
            cookies=cookies,
        )


def main():

    write_log(["\n"])

    write_log(["Job started at:", str(datetime.now())])

    for container in ol:
        container_processor(
            container["containerId"],
            container["warehouseId"],
            container["tariffId"],
            container["unitSpecificationId"],
            container["unitRegistrationId"],
            get_dates(container),
        )


if __name__ == "__main__":
    main()
