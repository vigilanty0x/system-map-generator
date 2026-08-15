import unittest
from system_map_generator import generate,probe
class T(unittest.TestCase):
 def test_graph(self):self.assertTrue(generate({"nodes":[{"id":"a"}],"edges":[]})["ok"])
 def test_dangling(self):self.assertFalse(generate({"nodes":[{"id":"a"}],"edges":[{"from":"a","to":"b"}]})["ok"])
 def test_duplicate(self):self.assertFalse(generate({"nodes":[{"id":"a"},{"id":"a"}],"edges":[]})["ok"])
 def test_probe(self):self.assertTrue(probe()["ok"])
if __name__=="__main__":unittest.main()
