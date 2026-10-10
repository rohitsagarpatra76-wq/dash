# VEYRO Survey Analytics Dashboard & Sheet Converter

A modern, high-performance interactive analytics dashboard and universal sheet converter built for the **VEYRO Fashion Recommendation Study** (Google Form: `https://forms.gle/V2yEvZp1AhoJR1iw6`) and adaptable to any spreadsheet or survey responses dataset.

---

## 🚀 Quick Start

### Option 1: Double-Click Launcher (Easiest)
Double-click `start_dashboard.bat`. It will launch the local Python server and automatically open the dashboard in your default browser at `http://localhost:8080/index.html`.

### Option 2: Terminal / Command Prompt
```bash
python server.py
```

### Option 3: Direct File Open
You can also directly double-click `index.html`. It has the complete 130-response survey dataset embedded, so all charts, filters, tables, and converter tools work immediately without requiring any web server!

---

## 📊 Features Overview

### 1. Executive Analytics Dashboard
- **6 Key Metric Indicators**:
  - Total Sample Count (`130 respondents`)
  - Wardrobe Decision Friction Rate (`70%` report difficulty deciding what to wear)
  - Clothing Purchase Regret Rate (`78%` regretted a clothing purchase in last 3 months)
  - AI Stylist Perceived Utility (`82%` rate fashion AI recommendation app as useful)
  - Free Trial Adoption Intent (`78%` definitely or probably would try)
  - Projected High-Frequency Usage (`72%` weekly or higher expected usage)
- **11 Interactive Visual Charts**:
  - **Q1: Demographics by Age Group** (Bar chart)
  - **Q2: Gender Breakdown** (Doughnut chart)
  - **Q3: Wardrobe Decision Difficulty** (Bar chart from Never to Always)
  - **Q4: Top Clothing Challenges** (Ranked horizontal bar chart for multi-select options)
  - **Q5: Current Decision Channels** (Ranked bar chart: Own judgment, Friends, Social media, Apps)
  - **Q6: Purchase Regret Frequency** (Doughnut chart)
  - **Q7: Perceived App Usefulness** (Bar chart from Not useful to Extremely useful)
  - **Q8: Top Requested Features** (Ranked bar chart: Color suggestions, outfit matching, budget, closet combo)
  - **Q9: User Concerns & Barriers** (Horizontal bar chart: Privacy, inaccuracy, pricing)
  - **Q10: Likelihood to Try for Free** (Graded sentiment bar chart)
  - **Q11: Expected Usage Frequency** (Bar chart from Daily to Never)
- **Voice of Customer (Q12)**:
  - Curated, searchable card feed of user suggestions and written comments.

### 2. Multi-Dimensional Interactive Filters
- **Gender Filter**: Filter by Male, Female, Prefer not to say
- **Age Filter**: Filter by specific age bracket (18–24, 25–34, 35–44, etc.)
- **Styling Difficulty Filter**: Isolate high-friction vs. low-friction shoppers
- **Trial Intent Filter**: Compare enthusiastic adopters against hesitant users
- **Instant Cross-Filtering**: Every chart, KPI card, quote card, and table row updates in real time.

### 3. Raw Data Explorer & Table
- Search across all fields in real-time.
- Sort and paginate with configurable page sizes (15, 30, 50, 100 rows).
- Click on any row to open the **Detail Inspector Modal** to review full respondent answers.
- 1-click export of the active view to **CSV**, **Excel (.xlsx)**, or **JSON**.

### 4. Sheet Converter Studio (In-Browser & Python CLI)
- Convert any sheet or survey dataset between:
  - **CSV (.csv)**
  - **Microsoft Excel (.xlsx)**
  - **JSON (.json)**
  - **TSV (.tsv)**
- Option to export raw questions or clean, concise headers (e.g., `Age`, `Gender`, `Challenges`, etc.).
- Live preview showing the first 3 converted records before downloading.

### 5. Google Form & Google Sheet Live Sync
- **Connecting your Google Form responses**:
  1. Open your Google Form editor.
  2. Click the **Responses** tab &rarr; click the green **"Link to Sheets"** icon.
  3. In the Google Sheet, go to *File &rarr; Share* and choose *Anyone with the link can view*.
  4. Paste the Sheet URL into the dashboard's **Google Sheet Connection** tab to fetch and visualize live!
- **Alternatively**: In Google Sheets, click *File &rarr; Download &rarr; Comma Separated Values (.csv)* and drag the downloaded file straight into the dashboard.

---

## 🛠️ Python CLI Tool (`convert_sheet.py`)

You can also convert and inspect files directly from the command line:

```bash
# Convert CSV to JSON
python convert_sheet.py survey_responses.csv --to json

# Convert CSV to TSV
python convert_sheet.py survey_responses.csv --to tsv

# Convert CSV to an HTML visual table
python convert_sheet.py survey_responses.csv --to html

# Fetch a Google Sheet directly and save as CSV
python convert_sheet.py --google-sheet "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit" my_responses.csv
```

---

## 📁 File Structure

```text
dashboard for survey/
│
├── index.html                  # Standalone interactive dashboard & converter web app
├── survey_responses.csv        # 130 survey responses matching VEYRO questionnaire schema
├── survey_responses.json       # JSON export of the survey dataset
├── survey_responses.tsv        # TSV export of the survey dataset
├── survey_responses_table.html # Standalone standalone HTML table report
│
├── convert_sheet.py            # Zero-dependency Python CLI tool for sheet conversions
├── generate_data.py            # Generator script for survey responses
├── build_dashboard.py          # Dashboard builder script
├── server.py                   # Lightweight local web server with auto-launch
├── start_dashboard.bat         # Windows 1-click launcher
└── README.md                   # This documentation
```
