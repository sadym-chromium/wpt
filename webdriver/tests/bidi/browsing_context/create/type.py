import pytest

from .. import assert_browsing_context

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("value", ["tab", "window"])
async def test_type(bidi_session, value):
    contexts = await bidi_session.browsing_context.get_tree(max_depth=0)
    assert len(contexts) == 1

    new_context_id = await bidi_session.browsing_context.create(type_hint=value)
    assert contexts[0]["context"] != new_context_id

    # Check there is an additional browsing context
    contexts = await bidi_session.browsing_context.get_tree(max_depth=0)
    assert len(contexts) == 2

    # Retrieve the new context info
    contexts = await bidi_session.browsing_context.get_tree(
        max_depth=0, root=new_context_id
    )

    assert_browsing_context(
        contexts[0],
        new_context_id,
        children=None,
        is_root=True,
        parent=None,
        url="about:blank",
    )

    opener_protocol_value = await bidi_session.script.evaluate(
        expression="!!window.opener",
        target=bidi_session.script.ContextTarget(new_context_id))
    assert opener_protocol_value["result"]["value"] is False

    await bidi_session.browsing_context.close(context=new_context_id)
