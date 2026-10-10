"""
Sheet Converter & Survey Data Tool
Converts survey sheets between CSV, JSON, TSV, HTML, and fetches directly from Google Sheets.
No external dependencies required (uses standard library).
"""

import sys
import os
import csv
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime

def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames

def write_csv(data, fieldnames, output_path):
    with open(output_path, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"[OK] Saved CSV: {output_path} ({len(data)} rows)")

def write_json(data, output_path, indent=2):
    with open(output_path, mode='w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    print(f"[OK] Saved JSON: {output_path} ({len(data)} items)")

def write_tsv(data, fieldnames, output_path):
    with open(output_path, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(data)
    print(f"[OK] Saved TSV: {output_path} ({len(data)} rows)")

def write_html_table(data, fieldnames, output_path, title="Survey Data Table"):
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 24px; background: #f8fafc; color: #1e293b; }}
  h1 {{ font-size: 22px; font-weight: 700; color: #4338ca; }}
  .table-wrapper {{ overflow-x: auto; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13px; text-align: left; }}
  th {{ background: #f1f5f9; padding: 10px 14px; font-weight: 600; color: #475569; border-bottom: 2px solid #cbd5e1; white-space: nowrap; }}
  td {{ padding: 8px 14px; border-bottom: 1px solid #f1f5f9; max-width: 320px; word-wrap: break-word; }}
  tr:hover td {{ background: #f8fafc; }}
</style>
</head>
<body>
<h1>{title} ({len(data)} responses)</h1>
<div class="table-wrapper">
<table>
  <thead><tr>{''.join(f'<th>{html_escape(h)}</th>' for h in fieldnames)}</tr></thead>
  <tbody>
"""
    for row in data:
        html += "    <tr>" + "".join(f"<td>{html_escape(row.get(h, ''))}</td>" for h in fieldnames) + "</tr>\n"
    html += """  </tbody>
</table>
</div>
</body>
</html>"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] Saved HTML Report: {output_path}")

def html_escape(text):
    if not text:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def fetch_google_sheet_as_csv(url_or_id, output_path=None):
    """
    Downloads a Google Sheet as CSV using gviz or export endpoint.
    Supports standard Google Sheets URLs and raw Sheet IDs.
    """
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url_or_id)
    sheet_id = match.group(1) if match else url_or_id.strip()

    gid_match = re.search(r'gid=([0-9]+)', url_or_id)
    gid_param = f"&gid={gid_match.group(1)}" if gid_match else ""

    urls_to_try = [
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv",
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv{gid_param}",
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv",
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv{gid_param}"
    ]

    for export_url in urls_to_try:
        print(f"[*] Trying: {export_url}")
        req = urllib.request.Request(
            export_url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode('utf-8', errors='replace')
                if len(content.strip()) > 50:
                    if not output_path:
                        output_path = f"google_sheet_{sheet_id[:8]}.csv"
                    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
                        f.write(content)
                    print(f"[SUCCESS] Saved Google Sheet CSV to: {output_path} ({len(content)} bytes)")
                    return output_path
        except Exception as e:
            print(f"  [Attempt Failed] {e}")

    print("[ERROR] Could not fetch Google Sheet. Ensure sheet is shared as 'Anyone with the link can view'.")
    return None

def convert(input_file, output_format, output_file=None):
    if not os.path.exists(input_file):
        print(f"[ERROR] Input file '{input_file}' not found.")
        return False

    base, ext = os.path.splitext(input_file)
    ext = ext.lower()

    if ext == '.csv':
        data, fieldnames = read_csv(input_file)
    elif ext == '.json':
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        fieldnames = list(data[0].keys()) if data else []
    elif ext == '.tsv':
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter='\t')
            data = list(reader)
            fieldnames = reader.fieldnames
    else:
        print(f"[ERROR] Unsupported input format: {ext}")
        return False

    target_ext = '.' + output_format.lstrip('.').lower()
    if not output_file:
        output_file = f"{base}_converted{target_ext}"

    if target_ext == '.csv':
        write_csv(data, fieldnames, output_file)
    elif target_ext == '.json':
        write_json(data, output_file)
    elif target_ext == '.tsv':
        write_tsv(data, fieldnames, output_file)
    elif target_ext in ('.html', '.htm'):
        write_html_table(data, fieldnames, output_file)
    else:
        print(f"[ERROR] Target format {target_ext} not supported without third-party libraries.")
        return False

    return True

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print("Usage:")
        print("  python convert_sheet.py real_survey_responses.csv --to json")
        print("  python convert_sheet.py real_survey_responses.csv --to tsv")
        print("  python convert_sheet.py real_survey_responses.csv --to html")
        print("  python convert_sheet.py --google-sheet <URL_OR_ID> [output.csv]")
        sys.exit(0)

    if args[0] == '--google-sheet' and len(args) > 1:
        out = args[2] if len(args) > 2 else "real_survey_responses.csv"
        fetch_google_sheet_as_csv(args[1], out)
    elif len(args) >= 3 and args[1] == '--to':
        out_f = args[3] if len(args) > 3 else None
        convert(args[0], args[2], out_f)
    else:
        print("Invalid arguments. Check usage.")
