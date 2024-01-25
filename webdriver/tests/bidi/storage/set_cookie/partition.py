import pytest
from webdriver.bidi.modules.storage import BrowsingContextPartitionDescriptor, StorageKeyPartitionDescriptor
from .. import assert_cookie_is_set, create_cookie

pytestmark = pytest.mark.asyncio


async def test_partition_context(bidi_session, set_cookie, top_context, test_page, domain_value):
    await bidi_session.browsing_context.navigate(context=top_context["context"], url=test_page, wait="complete")

    set_cookie_result = await set_cookie(
        cookie=create_cookie(domain=domain_value()),
        partition=(BrowsingContextPartitionDescriptor(top_context["context"])))

    # Browsing context does not require a `sourceOrigin` partition key.
    assert set_cookie_result == {'partitionKey': {}, }

    await assert_cookie_is_set(bidi_session, domain=domain_value())


async def test_partition_context_frame(bidi_session, set_cookie, top_context, test_page, domain_value, inline):
    frame_url = inline("<div>bar</div>", domain="alt")
    root_page_url = inline(f"<iframe src='{frame_url}'></iframe>")
    root_page_domain = domain_value()

    # Navigate to a page with a frame.
    await bidi_session.browsing_context.navigate(
        context=top_context["context"],
        url=root_page_url,
        wait="complete",
    )

    all_contexts = await bidi_session.browsing_context.get_tree(root=top_context["context"])
    frame_context_id = all_contexts[0]["children"][0]["context"]

    set_cookie_result = await set_cookie(
        cookie=create_cookie(domain=root_page_domain),
        partition=(BrowsingContextPartitionDescriptor(frame_context_id)))

    # Browsing context does not require a `sourceOrigin` partition key.
    assert set_cookie_result == {'partitionKey': {}, }

    await assert_cookie_is_set(bidi_session, domain=root_page_domain)


async def test_partition_storage_key_source_origin(bidi_session, set_cookie, test_page, origin, domain_value):
    source_origin = origin()
    partition = StorageKeyPartitionDescriptor(source_origin=source_origin)

    set_cookie_result = await set_cookie(
        cookie=create_cookie(domain=domain_value()),
        partition=partition)

    assert set_cookie_result == {
        'partitionKey': {
            'sourceOrigin': source_origin
        },
    }

    await assert_cookie_is_set(bidi_session, domain=domain_value(), partition=partition)

# TODO: test `test_partition_storage_key_user_context`.
