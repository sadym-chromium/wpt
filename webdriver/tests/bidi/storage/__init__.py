from typing import Union
from webdriver.bidi.modules.network import NetworkBytesValue, NetworkStringValue
from webdriver.bidi.modules.storage import PartialCookie, PartitionDescriptor
from .. import any_int, recursive_compare
from webdriver.bidi.undefined import Undefined, UNDEFINED

COOKIE_NAME = 'SOME_COOKIE_NAME'
COOKIE_VALUE = NetworkStringValue('SOME_COOKIE_VALUE')


async def assert_cookie_is_not_set(bidi_session, name: str = COOKIE_NAME):
    """
    Asserts the cookie is not set.
    """
    all_cookies = await bidi_session.storage.get_cookies()
    assert 'cookies' in all_cookies
    assert not any(c for c in all_cookies['cookies'] if c['name'] == name)


async def assert_cookie_is_set(
        bidi_session,
        domain: str,
        name: str = COOKIE_NAME,
        value: str = COOKIE_VALUE,
        path: str = "/",
        http_only: bool = False,
        secure: bool = True,
        same_site: str = 'none',
        expiry: Union[Undefined, int] = UNDEFINED,
        partition: Union[Undefined, PartitionDescriptor] = UNDEFINED,
):
    """
    Asserts the cookie is set.
    """
    all_cookies = await bidi_session.storage.get_cookies(partition=partition)
    assert 'cookies' in all_cookies
    actual_cookie = next(c for c in all_cookies['cookies'] if c['name'] == name)
    recursive_compare({
        'domain': domain,
        'httpOnly': http_only,
        'name': name,
        'path': path,
        'sameSite': same_site,
        'secure': secure,
        # Varies depending on the cookie name and value.
        'size': any_int,
        'value': value,
        'expiry': expiry,
    }, actual_cookie)


def create_cookie(
        domain: str,
        name: str = COOKIE_NAME,
        value: NetworkBytesValue = COOKIE_VALUE,
        secure: Union[Undefined, bool] = True,
        path: Union[Undefined, str] = UNDEFINED,
        http_only: Union[Undefined, bool] = UNDEFINED,
        same_site: Union[Undefined, str] = UNDEFINED,
        expiry: Union[Undefined, int] = UNDEFINED,
) -> PartialCookie:
    """
    Creates a cookie with the given or default options.
    """
    return PartialCookie(
        domain=domain,
        name=name,
        value=value,
        path=path,
        http_only=http_only,
        secure=secure,
        same_site=same_site,
        expiry=expiry)
