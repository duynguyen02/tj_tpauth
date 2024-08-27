import dataclasses
from enum import Enum
from typing import List, Optional
from urllib.parse import urljoin

import aiohttp
import requests


@dataclasses.dataclass
class TPAuthData:
    auth: bool
    id: int
    token: str
    name: str
    alias: str
    email: str
    phone: str
    roles: List[int]
    permissions: List[int]


class Error(Enum):
    NOTHING = 'NOTHING'
    TIMEOUT = 'TIMEOUT'
    UNAUTHORIZED = 'UNAUTHORIZED'
    PARSING = 'PARSING'


@dataclasses.dataclass
class TPAuthStatus:
    status: bool
    data: Optional[TPAuthData] = None
    error: Error = Error.NOTHING


class TJTPAuth:
    class Endpoint:
        LOGIN = '/api/user/login'
        FROM_TOKEN = '/api/user/fromtoken'

    def __init__(self, host: str, timeout: float = 60.0):
        self._host = host
        self._timeout = timeout
        self._login_endpoint = urljoin(self._host, self.Endpoint.LOGIN)
        self._from_token_endpoint = urljoin(self._host, self.Endpoint.FROM_TOKEN)

    @staticmethod
    def _create_auth_status(data: dict) -> TPAuthStatus:
        try:
            auth_data = TPAuthData(
                auth=data['auth'],
                id=data['id'],
                token=data['token'],
                name=data['name'],
                alias=data['alias'],
                email=data['email'],
                phone=data['phone'],
                roles=data['roles'],
                permissions=data['permissions']
            )
            return TPAuthStatus(status=True, data=auth_data, error=Error.NOTHING)
        except KeyError:
            return TPAuthStatus(status=False, error=Error.PARSING)

    async def aio_from_token(self, token: str) -> TPAuthStatus:
        headers = {
            'accept': '*/*',
            'authorization': f'Bearer {token}'
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self._from_token_endpoint, headers=headers, timeout=self._timeout) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._create_auth_status(data['data'])
            except aiohttp.ClientError:
                return TPAuthStatus(status=False, data=None, error=Error.TIMEOUT)
        return TPAuthStatus(status=False, data=None, error=Error.UNAUTHORIZED)

    async def aio_login(self, username: str, password: str) -> TPAuthStatus:
        headers = {
            'accept': '*/*',
            'authorization': 'Bearer nothing here',
            'content-type': 'application/json',
        }
        payload = {
            'name': username,
            'password': password
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self._login_endpoint, headers=headers, json=payload,
                                        timeout=self._timeout) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._create_auth_status(data['data'])
            except aiohttp.ClientError:
                return TPAuthStatus(status=False, data=None, error=Error.TIMEOUT)
            return TPAuthStatus(status=False, data=None, error=Error.UNAUTHORIZED)

    def from_token(self, token: str) -> TPAuthStatus:
        headers = {
            'accept': '*/*',
            'authorization': f'Bearer {token}'
        }
        try:
            response = requests.get(self._from_token_endpoint, headers=headers, timeout=self._timeout)
            if response.status_code == 200:
                return self._create_auth_status(response.json()['data'])
        except requests.RequestException:
            return TPAuthStatus(status=False, data=None, error=Error.TIMEOUT)
        return TPAuthStatus(status=False, data=None, error=Error.UNAUTHORIZED)

    def login(self, username: str, password: str) -> TPAuthStatus:
        headers = {
            'accept': '*/*',
            'authorization': 'Bearer nothing here',
            'content-type': 'application/json',
        }
        payload = {
            'name': username,
            'password': password
        }
        try:
            response = requests.post(self._login_endpoint, headers=headers, json=payload, timeout=self._timeout)
            if response.status_code == 200:
                return self._create_auth_status(response.json()['data'])
        except requests.RequestException:
            return TPAuthStatus(status=False, data=None, error=Error.TIMEOUT)
        return TPAuthStatus(status=False, data=None, error=Error.UNAUTHORIZED)
