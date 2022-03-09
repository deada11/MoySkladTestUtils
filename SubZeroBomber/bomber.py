import requests
import json
from threading import Thread

url = 'https://subzero-billing-4.testms-test.lognex.ru/api/clinton/1.0/ticket'
headers = {'Content-Type': 'application/json'}


def bomber():
    with open('subscribeTo.json', 'r') as subscribe:
        sub_data = json.load(subscribe)
        for i in range(5000):
            sub_response = requests.post(url, data=json.dumps(sub_data), headers=headers)
            print(i)

    with open('unsubsribeFrom.json', 'r') as unsubscribe:
        unsub_data = json.load(unsubscribe)
        for j in range(5000):
            unsub_response = requests.post(url, data=json.dumps(unsub_data), headers=headers)
            print(j)

    return sub_response, unsub_response


thread1 = Thread(target=bomber)
thread2 = Thread(target=bomber)
thread3 = Thread(target=bomber)
thread4 = Thread(target=bomber)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
