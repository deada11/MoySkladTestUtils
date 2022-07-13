import json
import requests
from threading import Thread

url = 'https://subzero-billing-5.testms-test.lognex.ru/api/clinton/1.0/ticket'
headers = {'Content-Type': 'application/json'}

account = ['fb7c8532-02fb-11ed-0a83-03360000032e',
           '030ab263-02fc-11ed-0a83-033600000337',
           '0a5020f4-02fc-11ed-0a83-033600000340']
product = ['dae446a5-02f6-11ed-0a83-033600000322',
           'd6ba8650-02f6-11ed-0a83-03360000031c',
           '3843c19c-02f7-11ed-0a83-033600000328']
tariff = ['799fe03c-d628-41c2-8294-206ec8cc4349',
          'cfce3cd2-a2b3-4e96-a82a-49d4f97d2df3',
          '5995b199-4e62-4e4b-8829-f488da11cccf']


def stupid_bomber():
    for i in range(len(account)):
        for j in range(len(product)):
            ticket = {
                "accountId": account[i],
                "source": {
                    "type": {
                        "id": "83aa62a3-f20c-4052-9bea-3674fa6076fd"  # ADMIN
                    },
                    "actor": {
                        "id": "55ce8bd6-fc3e-11ec-0a81-073800000008",
                        "username": "tester"
                    }
                },
                "sum": {
                    "declared": "444.44"
                },
                "comment": "tester",
                "subscribeTo": {
                    "product": {
                        "id": product[j]
                    },
                    "tariff": {
                        "id": tariff[j]
                    },
                    "period": {
                        "value": "1",
                        "measure": "MONTHS"
                    },
                    "demoPeriod": False,
                    "trial": False
                }
            }
            json_ticket = json.dumps(ticket)
            response = requests.post(url, data=json_ticket, headers=headers)
            print(i, j, response)


thread1 = Thread(target=stupid_bomber())
thread2 = Thread(target=stupid_bomber())
thread3 = Thread(target=stupid_bomber())
thread4 = Thread(target=stupid_bomber())


def start_threads():
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()


def stop_threads():
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


start_threads()
stop_threads()
