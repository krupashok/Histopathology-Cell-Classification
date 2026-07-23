"""Safely extract the supplied CRCHistoPhenotypes dataset archive."""
import argparse, shutil, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(); p.add_argument("archive",type=Path); p.add_argument("--destination",type=Path,default=ROOT); args=p.parse_args()
 destination=args.destination.resolve()
 with zipfile.ZipFile(args.archive) as archive:
  for member in archive.infolist():
   name=member.filename.replace("\\","/")
   if not name.startswith("data/") or name.endswith("/") or "__MACOSX" in name or "/._" in name: continue
   target=(destination/name).resolve()
   if destination not in target.parents: raise RuntimeError(f"Unsafe archive path: {name}")
   target.parent.mkdir(parents=True,exist_ok=True)
   with archive.open(member) as source,target.open("wb") as output: shutil.copyfileobj(source,output)
 print(f"Dataset extracted to {destination/'data'}")
if __name__=="__main__": main()
