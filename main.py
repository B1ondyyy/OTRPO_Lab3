import requests
import json
import os

user_id = "325588436" # ID Пользователя
output_file = "output.json" # Сформированный файл json

# Выполнение запроса к VK API
def execute_vk_api_request(method, token, params=None):
    api_url = f"https://api.vk.com/method/{method}"
    params = params or {}
    params.update({
        "access_token": token,
        "v": "5.131"
    })
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Ошибка соединения с VK API: {error}")
        return None

# Получение и структурирование информации о пользователе
def fetch_user_data(token, vk_user_id):
    user_profile = execute_vk_api_request("users.get", token, {"user_ids": vk_user_id, "fields": "bdate,city,country"})
    user_friends = execute_vk_api_request("friends.get", token, {"user_id": vk_user_id, "fields": "nickname"})
    user_followers = execute_vk_api_request("users.getFollowers", token, {"user_id": vk_user_id, "fields": "nickname"})
    user_subscriptions = execute_vk_api_request("users.getSubscriptions", token, {"user_id": vk_user_id})
    user_groups = execute_vk_api_request("groups.get", token, {"user_id": vk_user_id, "extended": 1})

    return {
        "user_info": user_profile,
        "friends": user_friends,
        "followers": user_followers,
        "subscriptions": user_subscriptions,
        "groups": user_groups
    }

# Сохранение данных в JSON файл
def store_data_to_json(data, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Файл успешно сохранён в: {filepath}")
    except Exception as error:
        print(f"Ошибка при сохранении данных: {error}")

# Основная функция
def main():
    # Сервисный токен
    access_token = "TOKEN" # Токен приложения

    # Получение и сохранение данных
    vk_data = fetch_user_data(access_token, user_id)
    if vk_data:
        script_location = os.path.dirname(os.path.realpath(__file__))
        result_path = os.path.join(script_location, output_file)
        store_data_to_json(vk_data, result_path)

if __name__ == "__main__":
    main()