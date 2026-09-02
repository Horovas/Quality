import json
import pytest
from urllib.parse import urljoin
import requests
from creds_storage import headers


BASE_URL = "https//storage-management.facility.ru"

spt_list = [242541,145241,165651,623554,8431156,7129,8298519,1958915]

def test_spt4doubles(storageId: int):
    response = requests.get(
        urljoin(BASE_URL, 'unit/logger')
        headers=headers(),
        params={
            'storageId': str(storageId),
            'units': 'kg',
            'basespt': '25'
        }
    )

    reply = response.json()
    print(reply)

    return reply


def main():
    for spt_unit in spt_list:
        unit_list = []
        api_response = test_spt4doubles(spt_unit)

        for spt_unit in api_response["units"]:
            unit_list.append(spt_unit["id"])

        if len(unit_list) == len(set(unit_list)):
            print(f"{spt_unit} -- OK list: {len(unit_list)}  set: {len(set(unit_list))}")

        else:
            detected = set()
            duplicates = set(x for x in unit_list if x in detected or detected.add(x))
            print(f"Unit {spt_unit}, has doubles {list(duplicates)}")


if __name__ == '__main__':
    main()


