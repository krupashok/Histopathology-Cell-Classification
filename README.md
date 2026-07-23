# Histopathology Cell Classification

Computer-vision classification on the CRCHistoPhenotypes dataset of 27×27 RGB colorectal histology cell images.

- **Binary task:** cancerous vs non-cancerous using 20,280 images from 98 patients
- **Multiclass task:** fibroblast, inflammatory, epithelial, or other using 9,896 images from 60 patients
- Patient-level splitting prevents images from the same patient leaking across train and test sets

The original notebook compares classical models and convolutional neural networks and explores PCA, K-Means, t-SNE, data augmentation, and transfer learning. `src/train.py` provides a compact reproducible CNN baseline for either task.

## Dataset setup

The 20,280 images are intentionally excluded from Git. Place the supplied `dataset (1).zip` anywhere and run:

```powershell
python scripts\setup_data.py "C:\path\to\dataset (1).zip"
```

The label CSVs are also excluded because they contain pseudonymous patient identifiers.

## Run

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -s tests -v
python src\train.py --task binary --epochs 10
python src\train.py --task multiclass --epochs 10
```

Models and metrics are written to ignored `artifacts/`. GPU acceleration is used automatically when available.

## Structure

- `src/train.py` — maintained patient-split CNN baseline
- `scripts/setup_data.py` — safe archive extraction
- `data/` — public setup guidance plus locally installed, Git-ignored labels and images
- `notebooks/` — original full analysis
- `reports/` — report and notebook PDF
- `tests/` — cohort and optional image-integrity checks

The 192 MB presentation video is not committed because it exceeds GitHub's normal per-file limit; it remains in the original assignment archive. This research prototype is not a clinical diagnostic system.
