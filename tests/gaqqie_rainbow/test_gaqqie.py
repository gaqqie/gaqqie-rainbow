import pytest

from gaqqie_rainbow.gaqqie import Gaqqie


class TestGaqqie:
    def test_init(self):
        # default parameters
        url = "test_url"
        actual = Gaqqie(url)
        assert actual._url == url
