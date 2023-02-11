import requests
from dataclasses import dataclass
from typing import Any, Dict
from django.conf import settings
from dataclasses import dataclass
from django.utils import timezone
from datetime import datetime
import threading
from graphql.error import GraphQLError
import json




class APIAdapter:

    def get_data(self) -> Any: 
        raise NotImplementedError




@dataclass
class HeraAdapter(APIAdapter):
    from .views import CitizenManager
    operation: str
    url: str = None
    nin: str = None
    uin: str = None
    uuid: str = None
    callback: str = None
    headers: Dict[str, str] = None
    data: Dict[str, str] = None
    lock = threading.Lock()
    manager = CitizenManager()

    def get_data(self):
        methods = {
            "access_token": self.__access_token,
            "get_one_person_info": self.__get_one_person,
            "get__bulk_info": self.__get__bulk_info,
            "verify": self.__verify,
            "match": self.__match,
            "document": self.__document,
            "get_subscriptions": self.__get_subscriptions,
            "subscribe_to_life_event": self.__subscribe_to_life_event,
            "confirm_subscription": self.__confirm_subscription,
            "unsubscribe_from_topic": self.__unsubscribe_from_topic,
            "create_topic": self.__create_topic,
            "get_topics": self.__get_topics,
            "delete_topic": self.__delete_topic,
            "publish_topic": self.__publish_topic,
        }
        methods[self.operation]()
        

    def __access_token(self):
        # make it thread safe
        with self.lock:
            try:
                url = settings.HERA_TOKEN_URL
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                data = {'client_id': 'hera-m2m','client_secret': settings.HERA_CLIENT_SECRET, 'grant_type': 'client_credentials'}

                # check if token is valid
                # read the access token from a file
                with open("access_token.json", "r") as file:
                    TOKEN = json.load(file)


                NOW = timezone.now()
                if ( 
                    TOKEN 
                    and TOKEN.get('expiry_time', None) is not None
                    and datetime.strptime(TOKEN['expiry_time'], '%Y-%m-%d %H:%M:%S.%f') > NOW
                ):
                    return TOKEN['access_token']

                
                response = requests.post(url, headers=headers, data=data)
                if response.status_code != 200:
                    raise GraphQLError("Error: ", response.status_code)
                
                token = response.json()
                expiry_time = NOW + timezone.timedelta(seconds=token['expires_in'])
                token['expiry_time'] = expiry_time.strftime('%Y-%m-%d %H:%M:%S.%f')

                # write the access token to a file
                with open("access_token.json", "w") as file:
                    json.dump(token, file)

                return token['access_token']
            except Exception as e:
                return None


    def __get_one_person(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/{self.nin}"
            querystring = {"attributeNames": ["firstName", "lastName", "dob", "placeOfBirth", "certificateNumber"]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers, params=querystring)
            return response.json()
        raise GraphQLError("Problem getting access token")
        # getattr(self.manager, self.callback)(**{
        #     "topicName": "LifeEventTopic",
        #     "businessIdentifier": "BR0000000037",
        #     "context": "BIRTH_REGISTRATION_CREATED",
        #     "eventDateTime": "2022-11-21T15:15:55.246067",
        #     "nin": "150854792341",
        #     "uin": "8888888888888",
        #     "firstName": "John",
        #     "lastName": "Doe",
        #     "dob": "1990-11-21",
        #     "placeOfBirth": "Kampala",
        #     "certificateNumber": "123456789",
        # })
        # raise GraphQLError("Problem getting access token")

    

    def __get__bulk_info(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/"
            querystring = {"attributeNames": ["firstName", "lastName", "dob", "placeOfBirth", "certificateNumber"]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers, params=querystring)
            return response.json()
        raise GraphQLError("Problem getting access token")

    def __verify(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/{self.uin}/verify"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        raise GraphQLError("Problem getting access token")


    def __match(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/{self.uin}/match"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        raise GraphQLError("Problem getting access token")


    def __document(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/{self.uin}/document"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            return response.json()
        raise GraphQLError("Problem getting access token")


    def __subscribe_to_life_event(self):
        if access_token := self.__access_token():
            url = settings.HERA_SUBSCRIBE_URL
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        raise GraphQLError("Problem getting access token")


    def __get_subscriptions(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/subscriptions"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            return response.json()
        raise GraphQLError("Problem getting access token")
    

    def __confirm_subscription(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/subscriptions/confirm"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            return response.json()
        raise GraphQLError("Problem getting access token")


    def __unsubscribe_from_topic(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/subscriptions/{self.uuid}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)  
            return response.json()
        raise GraphQLError("Problem getting access token")


    def __create_topic(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/topics"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        raise GraphQLError("Problem getting access token")
    

    def __get_topics(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/topics"
            headers = {"Authorization": f"Bearer {access_token}"}
            return requests.get(url, headers=headers)
        raise GraphQLError("Problem getting access token")
    

    def __delete_topic(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/topics/{self.uuid}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            return response.json()
        raise GraphQLError("Problem getting access token")
    

    def __publish_topic(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/topics/{self.uuid}/publish"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        raise GraphQLError("Problem getting access token")
    


class AnotherAdapter(APIAdapter):
    def get_data(self):
        "Code to get data from Another API"




