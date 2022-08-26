# pylint: disable=wrong-import-position
"""
The ``mlflow`` module provides a high-level "fluent" API for starting and managing MLflow runs.
For example:

.. code:: python

    import mlflow

    mlflow.start_run()
    mlflow.log_param("my", "param")
    mlflow.log_metric("score", 100)
    mlflow.end_run()

You can also use the context manager syntax like this:

.. code:: python

    with mlflow.start_run() as run:
        mlflow.log_param("my", "param")
        mlflow.log_metric("score", 100)

which automatically terminates the run at the end of the ``with`` block.

The fluent tracking API is not currently threadsafe. Any concurrent callers to the tracking API must
implement mutual exclusion manually.

For a lower level API, see the :py:mod:`mlflow.tracking` module.
"""
from logging import raiseExceptions
import os,sys
from xmlrpc.client import Boolean
from mlflow import *
from typing import TypedDict
from auth.auth0 import Auth0
from entities.workspace import Workspace

SERVER_URI = "https://mlflow-tracking-server-zx44gn5asa-uc.a.run.app"
workspace = Workspace()

class NewronConfig():
    def __init__(self) -> None:
        pass
    @property
    def apiKey(self):
        return self._apiKey
    @apiKey.setter
    def apiKey(self,value):
        self._apiKey = value

def init(experiment_name:str = None, is_autologger:Boolean = True):
  _auth = Auth0()
  print("init method")
  if _auth.authenticate():
    set_tracking_uri(SERVER_URI)
    print(SERVER_URI)
    set_experiment(experiment_name)
    if not is_autologger:
        autolog(disable=True)
  else:
    raise Exception("Authentication failed")
