from functools import wraps
import signal
from threading import Event, Thread
import time
from typing import Callable


from .rest import Configuration, JobApi, DeviceApi, ProviderApi, Result
from .rest.api_client2 import ApiClient2


class EventThread(Thread):
    def __init__(self, device_name, func, event, job_api, interval: float):
        super().__init__()
        self._device_name = device_name
        self._func = func
        self._event = event
        self._job_api = job_api
        self._interval = interval

    def is_active(self) -> bool:
        return self._event.is_set() == True

    def run(self):
        while self.is_active():
            # pull event
            job = self._job_api.receive_job(self._device_name)
            if job is not None and job.id is not None:
                self._func(job)
            else:
                time.sleep(self._interval)


class Gaqqie:
    """The Gaqqie object implements a job execution application.

    This repeats the following process:

    - Pulls new jobs at user-specified intervals.
    - When this pulls a new job, executes the function specified by the user on a worker thread.

    This creates a worker thread for each function specified by the user.
    """

    def __init__(self, url: str) -> None:
        """Initializes Gaqqie object.

        Parameters
        ----------
        url : str
            the base URL of the gaqqie API for providers.
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self._event_list = []
        self._thread_list = []

        self._url: str = url
        rest_config = Configuration()
        rest_config.host = self._url
        self._api_client = ApiClient2(rest_config)
        self._job_api = JobApi(api_client=self._api_client)
        self._device_api = DeviceApi(api_client=self._api_client)
        self._provider_api = ProviderApi(api_client=self._api_client)

    @property
    def job_api(self) -> JobApi:
        """Returns "job interface" of the gaqqie API for providers.

        Returns
        -------
        JobApi
            job interface.
        """
        return self._job_api

    @property
    def device_api(self) -> DeviceApi:
        """Returns "device interface" of the gaqqie API for providers.

        Returns
        -------
        DeviceApi
            device interface.
        """
        return self._device_api

    @property
    def provider_api(self) -> ProviderApi:
        """Returns "provider interface" of the gaqqie API for providers.

        Returns
        -------
        ProviderApi
            provider interface.
        """
        return self._provider_api

    def join(self) -> None:
        """Blocks the thread that called this function until all worker threads are stopped."""
        [thread.join() for thread in self._thread_list]

    def stop(self) -> None:
        """Stops all worker threads."""
        for event in self._event_list:
            event.clear()

    def receive_job(self, device_name: str, interval: float = 10.0) -> Callable:
        """Create and run worker thread.

        This function is supposed to be used as a decorator.
        Decorates the function that executes jobs.

        Parameters
        ----------
        device_name : str
            a specific device name on which to run the job.
        interval : float, optional
            polling interval(seconds) to the gaqqie API for providers, by default 10.0

        Returns
        -------
        Callable
            the decorator function.
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> None:
                ret = func(*args, **kwargs)
                return ret

            event = Event()
            event.set()
            thread = EventThread(device_name, wrapper, event, self._job_api, interval)
            thread.daemon = True
            thread.start()
            self._event_list.append(event)
            self._thread_list.append(thread)

            return wrapper

        return decorator

    def register_result(self, result: Result) -> None:
        """Registers the results of job execution via the gaqqie API for providers.

        It is assumed that the provider uses the result of the job execution to execute this function.
        The provider should execute this function even if the job fails to run.

        Parameters
        ----------
        result : Result
            the result of the job execution.
        """
        self.job_api.register_result(result, result.job_id)
