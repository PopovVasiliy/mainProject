from typing import Dict, List, Any

import requests

# небольшой класс - API-провайдер для реализации доступа к обработчикам API на сервере
class UserApiProvider(object):
    def __init__(self, service: str):
        self.__api_users_url = f'{service}/api/users'
        self.__api_messages_url = f'{service}/api/messages'

    def get_users(self) -> List[str]:
        return requests.get(self.__api_users_url).json()

    def autorize_user(self, data: Dict[str, Any]):
        return requests.post(self.__api_users_url, json=data).json()

    def send_message(self, data: Dict[str, Any]):
        return requests.post(self.__api_messages_url, json=data).json()
