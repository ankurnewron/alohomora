class Workspace():
    """
    Project object.
    """

    _WORKSPACE_NAME = "Default"
    _WORKSPACE_ID = None

    def __init__(self, workspace_id):
        self._WORKSPACE_ID = workspace_id

    @property
    def workspace_id(self):
        """String ID of the experiment."""
        return self._wo

    @property
    def name(self):
        """String name of the experiment."""
        return self._WORKSPACE_NAME

    def _set_name(self, new_name):
        self._WORKSPACE_NAME = new_name