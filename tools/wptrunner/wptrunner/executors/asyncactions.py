# mypy: allow-untyped-defs
import sys

from typing import Dict, List, Literal, Optional, Union
from typing_extensions import NotRequired, TypedDict


# TODO: check if type annotation is supported by all the required versions of Python.
# noinspection PyCompatibility
class WindowProxyProperties(Dict):
    context: str


# TODO: check if type annotation is supported by all the required versions of Python.
# noinspection PyCompatibility
class WindowProxyRemoteValue(TypedDict):
    """
    WebDriver BiDi browsing context descriptor.
    """
    type: Literal["window"]
    value: WindowProxyProperties


class BidiBrowsingContextGetTreeAction:
    name = "bidi.browsing_context.get_tree"

    # TODO: check if type annotation is supported by all the required versions of Python.
    # noinspection PyCompatibility
    class Payload(TypedDict):
        max_depth: NotRequired[int]
        root: NotRequired[Union[WindowProxyRemoteValue, str]]

    def __init__(self, logger, protocol):
        self.logger = logger
        self.protocol = protocol

    async def __call__(self, payload: Payload):
        root = None
        if "root" in payload:
            root = payload["root"]
            if isinstance(root, dict) and "type" in root and root["type"] == "window":
                root = root["value"]["context"]
        return await self.protocol.bidi_browsing_context.get_tree(root)


class BidiBrowsingContextLocateNodesAction:
    name = "bidi.browsing_context.locate_nodes"

    # TODO: check if type annotation is supported by all the required versions of Python.
    # noinspection PyCompatibility
    class Payload(TypedDict):
        context: Union[WindowProxyRemoteValue, str]
        locator: List[Dict]

    def __init__(self, logger, protocol):
        self.logger = logger
        self.protocol = protocol

    async def __call__(self, payload: Payload):
        context = payload["context"]
        if isinstance(context, dict) and "type" in context and context["type"] == "window":
            context = context["value"]["context"]
        return await self.protocol.bidi_browsing_context.locate_nodes(context, payload["locator"])


# TODO: check if type annotation is supported by all the required versions of Python.
# noinspection PyCompatibility
class SourceActions(TypedDict):
    """
    WebDriver BiDi browsing context descriptor.
    """
    type: Literal["window"]
    value: WindowProxyProperties


class BidiInputPerformAction:
    name = "bidi.input.perform_actions"

    # TODO: check if type annotation is supported by all the required versions of Python.
    # noinspection PyCompatibility
    class Payload(TypedDict):
        context: Union[str, WindowProxyRemoteValue]
        actions: List[Dict]

    def __init__(self, logger, protocol):
        self.logger = logger
        self.protocol = protocol

    async def __call__(self, payload: Payload):
        """
        :param payload: https://w3c.github.io/webdriver-bidi/#command-input-performActions
        :return:
        """
        context = payload["context"]
        if isinstance(context, dict) and "type" in context and context["type"] == "window":
            context = context["value"]["context"]

        return await self.protocol.bidi_input.perform_actions(payload["actions"], context)


class BidiSessionSubscribeAction:
    name = "bidi.session.subscribe"

    # TODO: check if type annotation is supported by all the required versions of Python.
    # noinspection PyCompatibility
    class Payload(Dict):
        """
        Payload for the "bidi.session.subscribe" action.
        events: List of event names to subscribe to.
        contexts: Optional list of browsing contexts to subscribe to. Each context can be either a BiDi serialized value,
        or a string. The latter is considered as a browsing context id.
        """
        events: List[str]
        contexts: Optional[List[Union[str, WindowProxyRemoteValue]]]

    def __init__(self, logger, protocol):
        self.logger = logger
        self.protocol = protocol

    async def __call__(self, payload: Payload):
        events = payload["events"]
        contexts = None
        if payload["contexts"] is not None:
            contexts = []
            for c in payload["contexts"]:
                if isinstance(c, str):
                    contexts.append(c)
                elif isinstance(c, dict) and "type" in c and c["type"] == "window":
                    contexts.append(c["value"]["context"])
                else:
                    raise ValueError("Unexpected context type: %s" % c)
        return await self.protocol.bidi_events.subscribe(events, contexts)


async_actions = [
    BidiBrowsingContextGetTreeAction,
    BidiBrowsingContextLocateNodesAction,
    BidiInputPerformAction,
    BidiSessionSubscribeAction]
