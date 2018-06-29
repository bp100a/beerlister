from unittest import TestCase
from models.TEB import TEBpage


class TestTEBpage(TestCase):
    def test_TEB_read(self):
        teb = TEBpage()
        assert (teb is not None)
