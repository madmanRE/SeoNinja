import time
import threading

import requests

api_key = "7ca62d97984045f0155be0f9492e0c51"


def get_pos_google(domain, query, region):
    task_response = requests.get(
        f"https://api.megaindex.com/scanning/google_position?key={api_key}&word={query}&lr={region}&show_page=0&show_direct=0")
    task_data = task_response.json()


    if task_data.get("status") == 1:
        task_id = task_data["data"]["task_id"]
        time.sleep(30)

        check_response = requests.get(
                f"http://api.megaindex.com/scanning/check?key={api_key}&method=google_position&task_id={task_id}")
        check_data = check_response.json()


        if check_data.get("status") == 1:


            positions = check_data["data"]

            for position_info in positions:
                if position_info["domain"] == domain:
                    position = position_info["position"]
                    return position
    return None


def get_pos_yandex(domain, query, region):
    task_response = requests.get(
        f"http://api.megaindex.com/scanning/yandex_position?key={api_key}&word={query}&lr={region}&show_page=0&show_direct=0")
    task_data = task_response.json()

    if task_data.get("status") == 1:
        task_id = task_data["data"]["task_id"]
        time.sleep(30)


        check_response = requests.get(
                f"http://api.megaindex.com/scanning/check?key={api_key}&method=yandex_position&task_id={task_id}")
        check_data = check_response.json()

        if check_data.get("status") == 1:


            positions = check_data["data"]


            for position_info in positions:
                if position_info["domain"] == domain:
                    position = position_info["position"]
                    return position

    return None


def get_position_megaindex(domain, queries, region=213):
    result = []
    threads = []

    for query in queries:
        thread_goog = threading.Thread(target=get_pos_google, args=(domain, query, region))
        thread_yand = threading.Thread(target=get_pos_yandex, args=(domain, query, region))
        thread_goog.start()
        thread_yand.start()
        threads.append(thread_goog)
        threads.append(thread_yand)

    for thread in threads:
        thread.join()

    for query in queries:
        pos_google = get_pos_google(domain, query, region)
        pos_yandex = get_pos_yandex(domain, query, region)
        res = [query, pos_yandex, pos_google]
        result.append(res)

    return result

