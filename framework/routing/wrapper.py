from typing import Callable
from fastapi import APIRouter


class RouterWrapper:
    def __init__(self, _router: APIRouter):
        self.router = _router
        self.http_verbs = ['get', 'post', 'put', 'patch', 'delete', 'head', 'trace', 'websocket']

    def __getattr__(self, verb):
        if verb not in self.http_verbs:
            return

        def _outer_callable(*router_args, **router_kwargs):
            if len(router_args) == 1:
                (original_path,) = router_args
            elif "path" in router_kwargs:
                original_path = router_kwargs.get("path")
                router_kwargs.pop("path")
            else:
                raise ValueError("path argument isn't filled in")

            if original_path.endswith("/"):
                alternate_path = original_path[:-1]
            else:
                alternate_path = f"{original_path}/"

            def _inner_callable(endpoint_func: Callable):
                router_annotation = getattr(self.router, verb)
                router_annotation(alternate_path, include_in_schema=False, **router_kwargs)(endpoint_func)
                return router_annotation(original_path, **router_kwargs)(endpoint_func)

            return _inner_callable

        return _outer_callable
