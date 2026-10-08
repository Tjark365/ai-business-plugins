import unittest
from app import analyze
class T(unittest.TestCase):
 def test_free(self): self.assertEqual(analyze({})["mode"],"free")
 def test_pro(self): self.assertTrue(analyze({},True)["results"])
if __name__=="__main__":unittest.main()
