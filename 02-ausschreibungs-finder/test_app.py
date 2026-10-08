import unittest
from app import analyze
class TestPlugin(unittest.TestCase):
    def test_free(self):
        x=analyze({"goal":"test"})
        self.assertEqual(x["mode"],"free")
    def test_pro(self):
        x=analyze({"goal":"test"},pro=True)
        self.assertEqual(x["mode"],"pro")
        self.assertTrue(x["results"])
if __name__=="__main__": unittest.main()
