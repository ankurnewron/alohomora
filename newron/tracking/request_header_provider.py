from mlflow.tracking.request_header.abstract_request_header_provider import RequestHeaderProvider
from entities.workspace import Workspace

workspace = Workspace()

class NewronPluginRequestHeaderProvider(RequestHeaderProvider):
    """RequestHeaderProvider provided through plugin system"""

    def in_context(self):
        return True

    def request_headers(self):
        return {"workspace_id": workspace.workspace_id}