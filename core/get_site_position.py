import requests

api_key = "ca764440e81e861f45a43f87cd34bae1"


def get_pos_google(domain, query, region):
    task_response = requests.get(
        f"https://api.megaindex.com/scanning/google_position?key={api_key}&word={query}&lr={region}&show_page=0&show_direct=0")
    task_data = task_response.json()

    if task_data.get("status") == 1:
        task_id = task_data["data"]["task_id"]

        check_response = requests.get(
            f"http://api.megaindex.com/scanning/check?key={api_key}&method=google_position&task_id=9a31b51c093c036173c46a3a1cedec95")
        check_data = check_response.json()
        print(check_data)

        if check_data.get("status") == 1:
            positions = check_data["data"]["positions"]

            for position_info in positions:
                if position_info["domain"] == domain:
                    return position_info["position"]

    return None


def get_pos_yandex(domain, query, region):
    task_response = requests.get(
        f"http://api.megaindex.com/scanning/yandex_position?key={api_key}&word={query}&lr={region}&show_page=0&show_direct=0")
    task_data = task_response.json()

    if task_data.get("status") == 1:
        task_id = task_data["data"]["task_id"]

        check_response = requests.get(
            f"http://api.megaindex.com/scanning/check?key={api_key}&method=yandex_position&task_id={task_id}")
        check_data = check_response.json()

        if check_data.get("status") == 1:
            positions = check_data["data"]["positions"]

            for position_info in positions:
                if position_info["domain"] == domain:
                    return position_info["position"]

    return None


def get_position_megaindex(domain, queries, region=213):
    result = []

    for query in queries:
        pos_google = get_pos_google(domain, query, region)
        pos_yandex = get_pos_yandex(domain, query, region)
        res = [query, pos_yandex, pos_google]
        result.append(res)
    return result
