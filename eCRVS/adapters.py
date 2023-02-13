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
import os




class APIAdapter:

    def get_data(self) -> Any: 
        raise NotImplementedError




@dataclass
class HeraAdapter(APIAdapter):
    
    operation: str
    nin: str = None
    uin: str = None
    uuid: str = None
    lock = threading.Lock()
    

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
        return methods[self.operation]()
        

    def __access_token(self):
        # make it thread safe
        with self.lock:
            try:
                url = settings.HERA_TOKEN_URL
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                data = {'client_id': 'hera-m2m','client_secret': 'DYdFBrNP0PsD5Z6Ng8lUMddAGbvOv5ow', 'grant_type': 'client_credentials'}

                TOKEN = None
                if os.path.exists("access_token.json"):
                    # read the access token from a file
                    with open("access_token.json", "r") as file:
                        TOKEN = json.load(file)


                # check if token is valid
                NOW = timezone.now()
                if ( 
                    TOKEN 
                    and TOKEN.get('expiry_time', None) is not None
                    and timezone.make_aware(datetime.strptime(TOKEN['expiry_time'], '%Y-%m-%d %H:%M:%S.%f'),\
                                             timezone.get_current_timezone()) > NOW
                    # and datetime.strptime(TOKEN['expiry_time'], '%Y-%m-%d %H:%M:%S.%f') > NOW
                ):
                    return TOKEN['access_token']

                
                response = requests.post(url, headers=headers, data=data)
                if response.status_code != 200:
                    raise GraphQLError(f"Error: {response.status_code}")
                
                token = response.json()
                expiry_time = NOW + timezone.timedelta(seconds=token['expires_in'])
                token['expiry_time'] = expiry_time.strftime('%Y-%m-%d %H:%M:%S.%f')

                # write the access token to a file
                with open("access_token.json", "w") as file:
                    json.dump(token, file)

                return token['access_token']
            except Exception as e:
                import traceback
                traceback.print_exc()
                return e


    def __get_one_person(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/{self.nin}"
            querystring = {"attributeNames": ["firstName", "lastName", "dob", "placeOfBirth", "certificateNumber"]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers, params=querystring)
            return response.json()
        return None

    

    def __get__bulk_info(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/"
            querystring = {"attributeNames": ["firstName", "lastName", "dob", "placeOfBirth", "certificateNumber"]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers, params=querystring)
            return response.json()
        return None

    def __verify(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/{self.uin}/verify"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        return None


    def __match(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/{self.uin}/match"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        return None


    def __document(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/persons/{self.uin}/document"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            return response.json()
        return None


    def __subscribe_to_life_event(self):
        if access_token := self.__access_token():
            url = settings.HERA_SUBSCRIBE_URL
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        return None


    def __get_subscriptions(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/subscriptions"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            return response.json()
        return None
    

    def __confirm_subscription(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/subscriptions/confirm"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            return response.json()
        return None


    def __unsubscribe_from_topic(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/subscriptions/{self.uuid}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)  
            return response.json()
        return None


    def __create_topic(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/topics"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        return None
    

    def __get_topics(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/topics"
            headers = {"Authorization": f"Bearer {access_token}"}
            return requests.get(url, headers=headers)
        return None
    

    def __delete_topic(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/topics/{self.uuid}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            return response.json()
        return None
    

    def __publish_topic(self):
        if access_token := self.__access_token():
            url = f"{settings.HERA_GENERAL_URL}/topics/{self.uuid}/publish"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        return None
    


class AnotherAdapter(APIAdapter):
    def get_data(self):
        "Code to get data from Another API"



# ssh -L 8080:https://keycloak.lao-dev01.wcc-hera.com:80 ubuntu@gambia.bluesquare.org 

# scp -r .env ubuntu@gambia.bluesquare.org:/home/ubuntu/eCRVS