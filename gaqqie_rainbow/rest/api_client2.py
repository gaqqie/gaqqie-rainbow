import atexit

from . import ApiClient


class ApiClient2(ApiClient):
    def __init__(
        self, configuration=None, header_name=None, header_value=None, cookie=None
    ):
        super().__init__(
            configuration=configuration,
            header_name=header_name,
            header_value=header_value,
            cookie=cookie,
        )
        atexit.register(self.pool.close)

    def __del__(self):
        try:
            self.pool.close()
            self.pool.join()
        except:
            pass
