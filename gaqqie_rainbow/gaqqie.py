from functools import wraps
import signal
from threading import Event, Thread
import time
from typing import Callable


from .rest import Configuration, JobApi, Result
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
    def __init__(self, url: str) -> None:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self._event_list = []
        self._thread_list = []

        self._url: str = url
        rest_config = Configuration()
        rest_config.host = self._url
        self._api_client = ApiClient2(rest_config)
        self._job_api = JobApi(api_client=self._api_client)

    @property
    def job_api(self) -> JobApi:
        return self._job_api

    def join(self) -> None:
        [thread.join() for thread in self._thread_list]

    def stop(self) -> None:
        for event in self._event_list:
            event.clear()

    def receive_job(self, device_name: str, interval: float = 10.0) -> Callable:
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
        self.job_api.register_result(result, result.job_id)
