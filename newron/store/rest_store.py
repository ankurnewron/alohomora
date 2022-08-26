from mlflow.store.tracking.rest_store import *

class NewronRestStore(RestStore):
    def __init__(self, get_host_creds):
        super().__init__(get_host_creds)

    def get_project(self, project_id):
        """
        Fetch the experiment from the backend store.

        :param experiment_id: String id for the experiment

        :return: A single :py:class:`mlflow.entities.Experiment` object if it exists,
        otherwise raises an Exception.
        """
        req_body = message_to_json(GetExperiment(experiment_id=str(experiment_id)))
        response_proto = self._call_endpoint(GetExperiment, req_body)
        return Experiment.from_proto(response_proto.experiment)