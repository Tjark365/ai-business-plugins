import unittest
from app import run
class TestPlugin(unittest.TestCase):
 def test_free_gate(self):
  r=run({},False); self.assertEqual(r["mode"],"free"); self.assertTrue(r["pro_required"])
 def test_pro(self):
  r=run({},True); self.assertEqual(r["mode"],"pro"); self.assertIn("result",r)
if __name__=="__main__": unittest.main()
