import pytest
from .. import assert_cookie_is_set, create_cookie
from webdriver.bidi.undefined import UNDEFINED

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "same_site",
    [
        "strict",
        "lax",
        "none",
        UNDEFINED
    ]
)
async def test_cookie_secure(bidi_session, top_context, test_page, domain_value, same_site):
    await bidi_session.browsing_context.navigate(context=top_context["context"], url=test_page, wait="complete")

    set_cookie_result = await bidi_session.storage.set_cookie(
        cookie=create_cookie(domain=domain_value(), same_site=same_site))

    assert set_cookie_result == {
        'partitionKey': {},
    }

    # `same_site` defaults to "none".
    expected_same_site = same_site if same_site is not UNDEFINED else 'none'
    await assert_cookie_is_set(bidi_session, domain=domain_value(), same_site=expected_same_site)
