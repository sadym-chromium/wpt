import pytest
from .. import assert_cookie_is_set, create_cookie

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "domain_key, subdomain_key",
    [
        ("", ""),
        ("", "www"),
        ("alt", ""),
        ("alt", "www"),
    ])
async def test_cookie_domain(bidi_session, test_page, server_config, domain_value, domain_key, subdomain_key):
    domain = domain_value(domain_key, subdomain_key)

    await bidi_session.storage.set_cookie(cookie=create_cookie(domain=domain))
    await assert_cookie_is_set(bidi_session, domain=domain)
