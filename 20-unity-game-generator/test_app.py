import unittest
from app import run
class TestPlugin(unittest.TestCase):
    def test_free_gate(self):
        self.assertEqual(run({})["mode"],"free")
        self.assertTrue(run({})["pro_required"])
    def test_pro(self):
        x=run({"goal":"test"},True)
        self.assertEqual(x["mode"],"pro")
        self.assertIn("result",x)
if __name__=="__main__": unittest.main()
