# Private dataset setup

Histopathology images and labels are intentionally excluded from this public repository. They are medical-derived data with pseudonymous patient identifiers, and the supplied course archive did not include an explicit redistribution licence.

Use an authorized local copy:

```powershell
python scripts\setup_data.py "C:\path\to\dataset (1).zip"
```

Expected local structure:

```text
data/images/
data/data_labels_mainData.csv
data/data_labels_extraData.csv
```
