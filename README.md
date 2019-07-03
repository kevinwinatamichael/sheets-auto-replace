# sheets-auto-replace
Auto replace automation tool using Google Sheets API.

## Guide to use

### Preparation
You must use Python3 (preferably v3.6).

Some of the package that you might need to install:
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install typing
```

### To run
Having done the preparation, you can use the module in 2 ways:

#### Using interface:

```python
from manager import Manager
Manager.start()  # key in the information here.
```

But sometimes re-keying the details repetitively might be too tiring,
so you can also prepare the details in a dictionary and then call another function as below.
```python
countries =[{
    'reviewSheetId': '1bD6BeGpAQxZk99Ai6vMlA0g1ljAZxtYyQ1bDFt7HGLY',
    'reviewSheetName': 'Benchmarking_new',
    'keywordSheetId': '1rkVXzuEU0644SBRXDPtjUryxJi4YTfBi-dzSclRoRKE',
    'keywordSheetName': 'to-benchmark',
    'reviewRange': 'A6402:A6701',
    'keywordRange': 'A2:B1000',
    'interval': 600
}, {
    'reviewSheetId': '15CvH8PBJUktYF46kQypDAd-xvkBP7X37BZiP3uTdX-Y',
    'reviewSheetName': 'Benchmarking_new',
    'keywordSheetId': '19ZPr49sEcKUHUPmvzTjeWvQ9yVBllsSVQ8hWvDo8qBs',
    'keywordSheetName': 'to-benchmark',
    'reviewRange': 'A5452:A5701',
    'keywordRange': 'A2:B1000',
    'interval': 600
}, {
    'reviewSheetId': '1sS9b6GwZjB0oQ9pvqDOoF-7Qpk3A2c9lyTGNR8hYvKI',
    'reviewSheetName': 'Benchmarking_new',
    'keywordSheetId': '1E4Sx0Hwe-cHFNdO6amVVQT4xyo2Iy4koArY8JHAPxHo',
    'keywordSheetName': 'to-benchmark',
    'reviewRange': 'A5444:A5693',
    'keywordRange': 'A2:B800',
    'interval': 600
}, {
    'reviewSheetId': '1AjgnY_4uuwVyLYNHwxnr2UPHd93onAMnOD5veWFER20',
    'reviewSheetName': 'Benchmarking_new',
    'keywordSheetId': '1kJbFGuONnP6d8J418d24_LvbVKD9BECwx03zaOD-WG0',
    'keywordSheetName': 'to-benchmark',
    'reviewRange': 'A5602:A5851',
    'keywordRange': 'A2:B1000',
    'interval': 600
}]
from manager import Manager
Manager.main_many(countries)
```

## Troubleshooting
`KeyError: 'effectiveValue not found in cell`

This is caused because either the range is out of range (contain empty cells), OR
a cell containing an unrecognizable unicode character (happened in Arabic language).
Therefore, you can resolve this issue by either making sure the range is correct, or
checking whether you have 'empty' cell (unrecognizable unicode).