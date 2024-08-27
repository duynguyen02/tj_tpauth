import pytest
import requests
from unittest.mock import patch, MagicMock
import aiohttp
import asyncio

from tj_tpauth import TJTPAuth, Error

mock_data = {
    'auth': True,
    'id': 123,
    'token': 'valid_token',
    'name': 'John Doe',
    'alias': 'johnd',
    'email': 'john.doe@example.com',
    'phone': '1234567890',
    'roles': [1, 2, 3],
    'permissions': [4, 5, 6]
}


# Test for sync login method
@patch('requests.post')
def test_login_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': mock_data}
    mock_post.return_value = mock_response

    auth = TJTPAuth('http://localhost')
    result = auth.login('username', 'password')

    assert result.status is True
    assert result.data is not None
    assert result.error == Error.NOTHING


@patch('requests.post')
def test_login_failure(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_post.return_value = mock_response

    auth = TJTPAuth('http://localhost')
    result = auth.login('username', 'password')

    assert result.status is False
    assert result.data is None
    assert result.error == Error.UNAUTHORIZED


@patch('requests.get')
def test_from_token_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': mock_data}
    mock_get.return_value = mock_response

    auth = TJTPAuth('http://localhost')
    result = auth.from_token('valid_token')

    assert result.status is True
    assert result.data is not None
    assert result.error == Error.NOTHING


@patch('requests.get')
def test_from_token_timeout(mock_get):
    mock_get.side_effect = requests.RequestException

    auth = TJTPAuth('http://localhost')
    result = auth.from_token('valid_token')

    assert result.status is False
    assert result.data is None
    assert result.error == Error.TIMEOUT


# Test for async login method
@pytest.mark.asyncio
@patch('aiohttp.ClientSession.post')
async def test_aio_login_success(mock_post):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = asyncio.coroutine(lambda: {'data': mock_data})
    mock_post.return_value.__aenter__.return_value = mock_response

    auth = TJTPAuth('http://localhost')
    result = await auth.aio_login('username', 'password')

    assert result.status is True
    assert result.data is not None
    assert result.error == Error.NOTHING


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_aio_from_token_success(mock_get):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = asyncio.coroutine(lambda: {'data': mock_data})
    mock_get.return_value.__aenter__.return_value = mock_response

    auth = TJTPAuth('http://localhost')
    result = await auth.aio_from_token('valid_token')

    assert result.status is True
    assert result.data is not None
    assert result.error == Error.NOTHING


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_aio_from_token_timeout(mock_get):
    mock_get.side_effect = aiohttp.ClientError

    auth = TJTPAuth('http://localhost')
    result = await auth.aio_from_token('valid_token')

    assert result.status is False
    assert result.data is None
    assert result.error == Error.TIMEOUT
