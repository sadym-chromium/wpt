import pytest
from .. import assert_cookie_is_not_set, assert_cookie_is_set, create_cookie
from webdriver.bidi.undefined import UNDEFINED
from datetime import datetime, timedelta
import time

pytestmark = pytest.mark.asyncio


async def test_cookie_expiry_undefined(bidi_session, top_context, test_page, origin, domain_value):
    # Navigate to a secure context.
    await bidi_session.browsing_context.navigate(context=top_context["context"], url=test_page, wait="complete")

    set_cookie_result = await bidi_session.storage.set_cookie(
        cookie=create_cookie(
            domain=domain_value(),
            expiry=UNDEFINED))

    assert set_cookie_result == {
        'partitionKey': {},
    }

    await assert_cookie_is_set(bidi_session, expiry=UNDEFINED, domain=domain_value())


async def test_cookie_expiry_future(bidi_session, top_context, test_page, origin, domain_value):
    # Navigate to a secure context.
    await bidi_session.browsing_context.navigate(context=top_context["context"], url=test_page, wait="complete")

    tomorrow = datetime.now() + timedelta(1)
    tomorrow_timestamp = time.mktime(tomorrow.timetuple())

    set_cookie_result = await bidi_session.storage.set_cookie(
        cookie=create_cookie(
            domain=domain_value(),
            expiry=tomorrow_timestamp))

    assert set_cookie_result == {
        'partitionKey': {},
    }

    await assert_cookie_is_set(bidi_session, expiry=tomorrow_timestamp, domain=domain_value())


async def test_cookie_expiry_past(bidi_session, top_context, test_page, origin, domain_value):
    # Navigate to a secure context.
    await bidi_session.browsing_context.navigate(context=top_context["context"], url=test_page, wait="complete")

    yesterday = datetime.now() - timedelta(1)
    yesterday_timestamp = time.mktime(yesterday.timetuple())

    set_cookie_result = await bidi_session.storage.set_cookie(
        cookie=create_cookie(
            domain=domain_value(),
            expiry=yesterday_timestamp))

    assert set_cookie_result == {
        'partitionKey': {},
    }

    await assert_cookie_is_not_set(bidi_session)
