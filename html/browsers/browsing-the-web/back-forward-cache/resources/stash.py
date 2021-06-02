import json

def main(request, response):
  with request.server.stash.lock:
    id = request.GET.first(b"id")
    action = request.GET.first(b"action")
    if action == b"push":
        new_item = request.GET.first(b"value")
        queue = request.server.stash.take(id)
        if queue is None:
          queue = []
        queue.append(new_item)
        request.server.stash.put(id, queue)
        return b"OK"
    elif action == b"pop":
        queue = request.server.stash.take(id)
        if queue is None or len(queue) == 0:
            return b""
        first_item = queue.pop(0)
        request.server.stash.put(id, queue)
        return first_item
