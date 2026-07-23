"""Train a compact CNN with patient-level splits."""
import argparse,json,random
from pathlib import Path
import numpy as np,pandas as pd,torch
from PIL import Image
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import LabelEncoder
from torch import nn
from torch.utils.data import DataLoader,Dataset
from torchvision import transforms

ROOT=Path(__file__).resolve().parents[1]
class Cells(Dataset):
 def __init__(self,frame,image_dir,target,transform): self.frame=frame.reset_index(drop=True); self.image_dir=image_dir; self.target=target; self.transform=transform
 def __len__(self): return len(self.frame)
 def __getitem__(self,index):
  row=self.frame.iloc[index]; image=Image.open(self.image_dir/row.ImageName).convert("RGB")
  return self.transform(image),int(row[self.target])
class CNN(nn.Module):
 def __init__(self,classes):
  super().__init__(); self.features=nn.Sequential(nn.Conv2d(3,32,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),nn.Conv2d(32,64,3,padding=1),nn.ReLU(),nn.AdaptiveAvgPool2d(1)); self.classifier=nn.Linear(64,classes)
 def forward(self,x): return self.classifier(self.features(x).flatten(1))
def split(frame):
 outer=GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42); trainval,test=next(outer.split(frame,groups=frame.patientID)); base=frame.iloc[trainval]
 inner=GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42); train,val=next(inner.split(base,groups=base.patientID)); return base.iloc[train],base.iloc[val],frame.iloc[test]
def main():
 p=argparse.ArgumentParser(); p.add_argument("--task",choices=["binary","multiclass"],default="binary"); p.add_argument("--epochs",type=int,default=10); p.add_argument("--batch-size",type=int,default=128); p.add_argument("--data-dir",type=Path,default=ROOT/"data"); p.add_argument("--output-dir",type=Path,default=ROOT/"artifacts"); args=p.parse_args()
 random.seed(42); np.random.seed(42); torch.manual_seed(42)
 main=pd.read_csv(args.data_dir/"data_labels_mainData.csv"); target="isCancerous"
 if args.task=="binary": frame=pd.concat([main,pd.read_csv(args.data_dir/"data_labels_extraData.csv")],ignore_index=True); classes=2
 else:
  frame=main.copy(); encoder=LabelEncoder(); frame["cellType"]=encoder.fit_transform(frame.cellTypeName); target="cellType"; classes=4
 train,val,test=split(frame); transform=transforms.Compose([transforms.ToTensor(),transforms.Normalize((.5,)*3,(.5,)*3)])
 loaders=[DataLoader(Cells(part,args.data_dir/"images",target,transform),batch_size=args.batch_size,shuffle=i==0) for i,part in enumerate((train,val,test))]
 device=torch.device("cuda" if torch.cuda.is_available() else "cpu"); model=CNN(classes).to(device); optimizer=torch.optim.Adam(model.parameters(),lr=1e-3); loss_fn=nn.CrossEntropyLoss()
 for epoch in range(args.epochs):
  model.train()
  for images,labels in loaders[0]: optimizer.zero_grad(); loss=loss_fn(model(images.to(device)),labels.to(device)); loss.backward(); optimizer.step()
  print(f"epoch {epoch+1}/{args.epochs} loss={loss.item():.4f}")
 model.eval(); correct=total=0
 with torch.no_grad():
  for images,labels in loaders[2]: predicted=model(images.to(device)).argmax(1).cpu(); correct+=int((predicted==labels).sum()); total+=len(labels)
 args.output_dir.mkdir(parents=True,exist_ok=True); torch.save(model.state_dict(),args.output_dir/f"{args.task}_cnn.pt"); metrics={"task":args.task,"test_accuracy":correct/total,"test_images":total,"split":"patient-level"}; (args.output_dir/f"{args.task}_metrics.json").write_text(json.dumps(metrics,indent=2)); print(json.dumps(metrics,indent=2))
if __name__=="__main__": main()
