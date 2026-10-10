import csv
import json
import re

# Read sheet_gviz.csv
with open('sheet_gviz.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    raw_rows = list(reader)

if not raw_rows:
    print("Error: empty raw_rows")
    exit(1)

raw_headers = raw_rows[0]

# Standardize headers to clean names while preserving questions
def clean_val(v):
    if not v:
        return ""
    # normalize dashes
    v = v.replace('\u2013', '–').replace('\u2014', '—').strip()
    return v

# Filter out empty rows (like row 1 that only had timestamp)
cleaned_rows = []
for r in raw_rows[1:]:
    # check if at least 3 non-empty cells
    non_empty = [c for c in r if c.strip()]
    if len(non_empty) >= 3:
        cleaned_rows.append([clean_val(c) for c in r])

print(f"Total cleaned response rows: {len(cleaned_rows)}")

# Write real_survey_responses.csv (with utf-8-sig so Excel on Windows opens accented/dashes properly)
with open('real_survey_responses.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(raw_headers)
    writer.writerows(cleaned_rows)

print("Saved real_survey_responses.csv")

# Also write real_survey_responses.tsv
with open('real_survey_responses.tsv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(raw_headers)
    writer.writerows(cleaned_rows)

print("Saved real_survey_responses.tsv")

# Also write real_survey_responses.json
json_records = []
for r in cleaned_rows:
    row_dict = {}
    for i, h in enumerate(raw_headers):
        val = r[i] if i < len(r) else ""
        row_dict[h] = val
    json_records.append(row_dict)

with open('real_survey_responses.json', 'w', encoding='utf-8') as f:
    json.dump(json_records, f, ensure_ascii=False, indent=2)

print(f"Saved real_survey_responses.json ({len(json_records)} records)")
