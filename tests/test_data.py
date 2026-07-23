import csv,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class DataTests(unittest.TestCase):
 def test_labels(self):
  if not (ROOT/"data/data_labels_mainData.csv").exists(): self.skipTest("Private medical-derived dataset not installed")
  with (ROOT/"data/data_labels_mainData.csv").open() as f: main=list(csv.DictReader(f))
  with (ROOT/"data/data_labels_extraData.csv").open() as f: extra=list(csv.DictReader(f))
  self.assertEqual(9896,len(main)); self.assertEqual(10384,len(extra)); self.assertEqual(60,len({r['patientID'] for r in main})); self.assertEqual(38,len({r['patientID'] for r in extra}))
  self.assertEqual({"fibroblast","inflammatory","epithelial","others"},{r["cellTypeName"] for r in main})
 def test_local_images_when_installed(self):
  images=ROOT/"data/images"
  if not images.exists(): self.skipTest("Large image dataset is installed separately")
  self.assertEqual(20280,len(list(images.glob("*.png"))))
if __name__=="__main__": unittest.main()
