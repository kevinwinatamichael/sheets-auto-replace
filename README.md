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
PH = {
    'reviewSheetId': '1AjgnY_4uuwVyLYNHwxnr2UPHd93onAMnOD5veWFER20',  # the benchmark sheet, found in the URL
    'reviewSheetName': 'Benchmarking_new',
    'keywordSheetId': '1kJbFGuONnP6d8J418d24_LvbVKD9BECwx03zaOD-WG0',  # the list of keywords sheet
    'keywordSheetName': 'to-benchmark',
    'reviewRange': 'A5602:A5851',  # must only include the keywords section of this week
    'keywordRange': 'A2:B1000',  # must only include the keywords along side the "checked" column
    'interval': 600
}
from manager import Manager
Manager.main(PH)
```

## Troubleshooting
`KeyError: 'effectiveValue not found in cell`

This is caused because either the range is out of range (contain empty cells), OR
a cell containing an unrecognizable unicode character (happened in Arabic language).
Therefore, you can resolve this issue by either making sure the range is correct, or
checking whether you have 'empty' cell (unrecognizable unicode).