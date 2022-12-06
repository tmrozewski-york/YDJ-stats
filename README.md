# Script for pulling stats from multiple Open Journal System (OJS) journals

Python script developed for [York Digital Journals](https://www.library.yorku.ca/web/collections/discover-our-collections/york-digital-journals-3/). Uses the [REST API for OJS 3.3](https://docs.pkp.sfu.ca/dev/api/ojs/3.3).

The script outputs a CSV with four datapoints for each of multiple journals:
1. Total published submissions
2. Total published issues
3. Previous month's abstract views
4. Previous month's galley views

The script outputs the total number of submissions and issues which require the manual calculation of new submissions and issues. This is because YDJ frequently ingests back issues of journals which would not be identified if the API call specified a data range for these data points.

This readme file is written for librarians and other OJS managers who knew as little coding as I did when I started this project.

## API endpoints and tokens

The API endpoints and tokens are stored in a CSV file. One row = one journal with the following column headers:
- `jabbr`: journal abbreviation (an identifier for each journal)
- `subs_endpoint`: endpoint for the [Submissions](https://docs.pkp.sfu.ca/dev/api/ojs/3.3#tag/Submissions/paths/~1submissions/get) call
- `issues_endpoint`: endpoint for the [Issues](https://docs.pkp.sfu.ca/dev/api/ojs/3.3#tag/Issues/paths/~1issues/get) call
- `abstractViews_endpoint`: endpoint for the [Abstract views](https://docs.pkp.sfu.ca/dev/api/ojs/3.3#tag/Stats-Publications/paths/~1stats~1publications~1abstract/get) call
- `galleyViews_endpoint`: endpoint for the [Galley views](https://docs.pkp.sfu.ca/dev/api/ojs/3.3#tag/Stats-Publications/paths/~1stats~1publications~1galley/get) call
- `token`: the API token for each journal

## Data processing

The script reads the CSV file with endpoints and tokens as `my_keys`, creates `monthLookup` for the previous months in YYYY-MM format, and creates four empty lists to store the data extracted from the API calls:
1. `journal_list`: the journal abbreviation
2. `month_list`: the month for the stats pull
3. `metric_list`: the metric to which the value applies
4. `value_list`: the value

The script then iterates through each journal with a `for` loop, calling each API in turn and writing the output datapoint to the appropriate list.

### Published submissions

The API call includes the parameter `'status':'3'`, returning only published submissions. The call returns a JSON file and the script reads `itemsMax`. It writes `jabbr`, `monthLookup`, the string "published submissions", and the value of `itemsMax` to the appropriate list.

### Published issues

The API call includes the parameter `'isPublished':'true'`, returning only published issues. The call returns a JSON file and the script reads `itemsMax`. It writes `jabbr`, `monthLookup`, the string "published issues", and the value of `itemsMax` to the appropriate list.

### Abstract views

The API call includes the parameter `'dateStart':'2001-01-01'`, returning data for all possible months. The call returns a JSON file featuring an array of objects where each object is a month and its view data. Python reads this as a list of dictionaries in which each month and its view data is a dictionary. The script uses `monthLookup` to identify the dictionary for the previous month and extracts `value` for that month. It writes `jabbr`, `monthLookup`, the string "abstract views", and the value of `values` to the appropriate list.

### Galley views

The API call includes the parameter `'dateStart':'2001-01-01'`, returning data for all possible months. The call returns a JSON file featuring an array of objects where each object is a month and its view data. Python reads this as a list of dictionaries in which each month and its view data is a dictionary. The script uses `monthLookup` to identify the dictionary for the previous month and extracts `value` for that month. It writes `jabbr`, `monthLookup`, the string "galley views", and the value of `values` to the appropriate list.

### Print

To help with debugging, the script prints the journal abbreviation in the console once it completes the iteration of the loop for that journal.

### Combining the data

The data harvested from the API calls have been stored in four lists of equal length. The script zips these into a long data frame with four headers: `journal`, `month`, `metric`, `value`. It then pivots the data frame to make it wide and prints the output to a CSV file.

## Output

The output CSV file has one row for each journal with the following headers:
- `journal`
- `month`
- `abstract views`
- `galley views`
- `published issues`
- `published submissions`

Somewhere along the way the journal abbreviations and the labels for the four metrics got sorted alphabetically.
