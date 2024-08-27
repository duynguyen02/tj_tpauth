# tj-tpauth

`tj-tpauth` is a Python library for managing user authentication through an API. The library supports both synchronous
and asynchronous methods for login and token-based authentication.

## Installation

To install the library, use pip:

```bash
pip install tj-tpauth
```

## Usage

### Synchronous (Sync)

```python
from tj_tpauth import TJTPAuth

# Initialize TJTPAuth object with API URL and optional timeout
tpauth = TJTPAuth(
    host='http://localhost:3000',
    timeout=10
)

# Log in with username and password
login_status = tpauth.login(
    username='username',
    password='password'
)

# Check login status
if not login_status.status:
    exit(0)

# Authenticate with token
auth_status = tpauth.from_token(login_status.data.token)

# Check authentication status
if not auth_status.status:
    exit(0)

# Print authentication data
print(auth_status.data)
```

### Asynchronous (Async)

```python
import asyncio
from tj_tpauth import TJTPAuth

# Initialize TJTPAuth object with API URL and optional timeout
tpauth = TJTPAuth(
    host='http://localhost:3000',
    timeout=10
)


async def main():
    # Log in with username and password
    login_status = await tpauth.aio_login(
        username='username',
        password='password'
    )

    # Check login status
    if not login_status.status:
        exit(0)

    # Authenticate with token
    auth_status = await tpauth.aio_from_token(login_status.data.token)

    # Check authentication status
    if not auth_status.status:
        exit(0)

    # Print authentication data
    print(auth_status.data)


# Run asynchronous function
asyncio.run(main())
```

## Main Classes

- `TPAuthData`: Contains user authentication information.
- `TPAuthStatus`: Represents the authentication status, including error information.
- `TJTPAuth`: Provides synchronous and asynchronous methods for login and token-based authentication.

## Error Handling

- **`Error.NOTHING`**: No error.
- **`Error.TIMEOUT`**: Timeout error.
- **`Error.UNAUTHORIZED`**: Unauthorized error.
- **`Error.PARSING`**: Data parsing error.

## References

For more information about `requests` and `aiohttp`, refer to their official documentation:

- [Requests Documentation](https://docs.python-requests.org/)
- [Aiohttp Documentation](https://docs.aiohttp.org/)

## License

This library is released under the MIT License.

## Contact

If you have any questions or issues, please open an issue on [GitHub](https://github.com/duynguyen02/tj_tpauth/issues) or
email us at [duynguyen02.dev@gmail.com](mailto:duynguyen02.dev@gmail.com).
