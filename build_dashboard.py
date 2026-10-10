import json

with open('real_survey_responses.json', 'r', encoding='utf-8') as f:
    real_data = json.load(f)

with open('survey_responses.json', 'r', encoding='utf-8') as f:
    demo_data = json.load(f)

real_json_str = json.dumps(real_data, ensure_ascii=False)
demo_json_str = json.dumps(demo_data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VEYRO - Survey Analytics & Sheet Converter Dashboard</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <!-- SheetJS (xlsx) for in-browser Excel/CSV reading & writing -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#eef2ff',
              100: '#e0e7ff',
              200: '#c7d2fe',
              500: '#5746e3',
              600: '#4f39f6',
              700: '#4338ca',
              800: '#3730a3',
              900: '#312e81',
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    @media print {{
      .no-print {{ display: none !important; }}
      body {{ background: white !important; color: black !important; }}
      .chart-card {{ break-inside: avoid; page-break-inside: avoid; }}
    }}
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 4px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
      background: #94a3b8;
    }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col font-sans antialiased">

  <!-- TOP HEADER -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-xs no-print">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-brand-500 text-white flex items-center justify-center font-bold text-lg shadow-sm">
          V
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="font-bold text-slate-900 text-lg leading-tight">VEYRO Survey Intelligence</h1>
            <span class="text-xs bg-emerald-50 text-emerald-700 font-semibold px-2 py-0.5 rounded-full border border-emerald-200 flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> Live Sheet Synced
            </span>
          </div>
          <p class="text-xs text-slate-500">Google Sheet: 1qTx1-al8moCYeGvao8Ak2tenngJtJoepLAjtXGqWVTU</p>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="flex items-center gap-2 sm:gap-3">
        <!-- Dataset Toggle -->
        <div class="hidden md:flex bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-xs font-semibold">
          <button id="btnSetReal" onclick="switchDataset('real')" class="px-2.5 py-1 rounded-md bg-white text-brand-700 shadow-2xs transition">
            Real Survey (24)
          </button>
          <button id="btnSetDemo" onclick="switchDataset('demo')" class="px-2.5 py-1 rounded-md text-slate-600 hover:text-slate-900 transition">
            Demo Model (130)
          </button>
        </div>

        <label for="fileUploadInput" class="cursor-pointer inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-2xs transition">
          <i data-lucide="upload" class="w-4 h-4 text-slate-500"></i>
          <span>Upload Sheet</span>
          <input type="file" id="fileUploadInput" accept=".csv, .xlsx, .xls, .tsv, .json" class="hidden" onchange="handleFileUpload(event)">
        </label>

        <button onclick="switchTab('converter')" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-2xs transition">
          <i data-lucide="refresh-cw" class="w-4 h-4 text-slate-500"></i>
          <span class="hidden sm:inline">Convert Formats</span>
          <span class="sm:hidden">Convert</span>
        </button>

        <button onclick="switchTab('googleSync')" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 border border-emerald-300 text-emerald-800 rounded-lg text-xs font-semibold hover:bg-emerald-100 shadow-2xs transition">
          <i data-lucide="link" class="w-4 h-4 text-emerald-600"></i>
          <span class="hidden sm:inline">Google Sheet Sync</span>
          <span class="sm:hidden">Sync</span>
        </button>

        <button onclick="window.print()" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-brand-500 text-white rounded-lg text-xs font-semibold hover:bg-brand-600 shadow-sm transition">
          <i data-lucide="printer" class="w-4 h-4"></i>
          <span>Print / PDF</span>
        </button>
      </div>
    </div>

    <!-- SUBNAV TABS -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-slate-100 flex items-center justify-between">
      <nav class="flex gap-6 overflow-x-auto py-2">
        <button onclick="switchTab('dashboard')" id="tabBtn-dashboard" class="tab-btn text-brand-600 font-semibold border-b-2 border-brand-500 pb-1.5 text-sm flex items-center gap-1.5">
          <i data-lucide="layout-dashboard" class="w-4 h-4"></i> Executive Dashboard
        </button>
        <button onclick="switchTab('table')" id="tabBtn-table" class="tab-btn text-slate-500 hover:text-slate-800 font-medium pb-1.5 text-sm flex items-center gap-1.5 transition">
          <i data-lucide="table" class="w-4 h-4"></i> Raw Data Explorer
        </button>
        <button onclick="switchTab('converter')" id="tabBtn-converter" class="tab-btn text-slate-500 hover:text-slate-800 font-medium pb-1.5 text-sm flex items-center gap-1.5 transition">
          <i data-lucide="file-spreadsheet" class="w-4 h-4"></i> Sheet Converter
        </button>
        <button onclick="switchTab('googleSync')" id="tabBtn-googleSync" class="tab-btn text-slate-500 hover:text-slate-800 font-medium pb-1.5 text-sm flex items-center gap-1.5 transition">
          <i data-lucide="cloud-download" class="w-4 h-4"></i> Google Sheet Connection
        </button>
      </nav>

      <div class="hidden md:flex items-center gap-2 text-xs text-slate-500">
        <span class="w-2 h-2 rounded-full bg-emerald-500 inline-block animate-pulse"></span>
        <span id="headerDatasetLabel">24 Real Survey Responses Loaded</span>
      </div>
    </div>
  </header>

  <!-- MAIN BODY -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full">

    <!-- TAB 1: EXECUTIVE DASHBOARD -->
    <div id="tabContent-dashboard" class="space-y-6">

      <!-- FILTER BAR -->
      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs no-print flex flex-wrap items-center justify-between gap-4">
        <div class="flex flex-wrap items-center gap-3">
          <span class="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1">
            <i data-lucide="sliders-horizontal" class="w-3.5 h-3.5"></i> Filters:
          </span>

          <!-- Gender Filter -->
          <div class="flex items-center gap-1.5">
            <label class="text-xs text-slate-500">Gender:</label>
            <select id="filterGender" onchange="applyFilters()" class="text-xs bg-slate-50 border border-slate-300 rounded-md px-2 py-1 focus:ring-1 focus:ring-brand-500">
              <option value="All">All Genders</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="prefer not say">Prefer not to say</option>
            </select>
          </div>

          <!-- Age Filter -->
          <div class="flex items-center gap-1.5">
            <label class="text-xs text-slate-500">Age:</label>
            <select id="filterAge" onchange="applyFilters()" class="text-xs bg-slate-50 border border-slate-300 rounded-md px-2 py-1 focus:ring-1 focus:ring-brand-500">
              <option value="All">All Ages</option>
              <option value="Under 18">Under 18</option>
              <option value="18–24">18–24</option>
              <option value="25–34">25–34</option>
              <option value="35–44">35–44</option>
              <option value="45–54">45–54</option>
              <option value="55 or above">55 or above</option>
            </select>
          </div>

          <!-- Difficulty Filter -->
          <div class="flex items-center gap-1.5">
            <label class="text-xs text-slate-500">Decide Wear:</label>
            <select id="filterDiff" onchange="applyFilters()" class="text-xs bg-slate-50 border border-slate-300 rounded-md px-2 py-1 focus:ring-1 focus:ring-brand-500">
              <option value="All">All Levels</option>
              <option value="High">High (Often / Always)</option>
              <option value="Sometimes">Moderate (Sometimes)</option>
              <option value="Low">Low (Never / Occasionally)</option>
            </select>
          </div>

          <!-- Try Free Likelihood -->
          <div class="flex items-center gap-1.5">
            <label class="text-xs text-slate-500">Trial Intent:</label>
            <select id="filterTrial" onchange="applyFilters()" class="text-xs bg-slate-50 border border-slate-300 rounded-md px-2 py-1 focus:ring-1 focus:ring-brand-500">
              <option value="All">All</option>
              <option value="Positive">Definitely / Probably Would</option>
              <option value="Neutral">Not Sure</option>
              <option value="Negative">Would Not</option>
            </select>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button onclick="resetFilters()" class="text-xs text-slate-500 hover:text-slate-800 underline px-2 py-1">
            Reset Filters
          </button>
          <span id="filteredCountBadge" class="text-xs font-semibold bg-brand-50 text-brand-700 px-2.5 py-1 rounded-md border border-brand-200">
            Showing 24 of 24
          </span>
        </div>
      </div>

      <!-- KPI METRIC CARDS -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
        <!-- Card 1 -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">Responses</span>
            <i data-lucide="users" class="w-4 h-4 text-brand-500"></i>
          </div>
          <div class="text-2xl font-bold text-slate-900" id="kpiTotal">24</div>
          <p class="text-[11px] text-slate-500 mt-1">Verified respondents</p>
        </div>

        <!-- Card 2 -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">Style Struggle</span>
            <i data-lucide="help-circle" class="w-4 h-4 text-amber-500"></i>
          </div>
          <div class="text-2xl font-bold text-amber-600" id="kpiDifficultyRate">71%</div>
          <p class="text-[11px] text-slate-500 mt-1">Struggle to pick clothes</p>
        </div>

        <!-- Card 3 -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">Purchase Regret</span>
            <i data-lucide="shopping-bag" class="w-4 h-4 text-rose-500"></i>
          </div>
          <div class="text-2xl font-bold text-rose-600" id="kpiRegretRate">75%</div>
          <p class="text-[11px] text-slate-500 mt-1">Regretted buy in 3 mos</p>
        </div>

        <!-- Card 4 -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">App Utility</span>
            <i data-lucide="sparkles" class="w-4 h-4 text-brand-500"></i>
          </div>
          <div class="text-2xl font-bold text-brand-600" id="kpiUtilityRate">75%</div>
          <p class="text-[11px] text-slate-500 mt-1">Rate AI stylist useful</p>
        </div>

        <!-- Card 5 -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">Trial Intent</span>
            <i data-lucide="thumbs-up" class="w-4 h-4 text-emerald-500"></i>
          </div>
          <div class="text-2xl font-bold text-emerald-600" id="kpiTrialRate">79%</div>
          <p class="text-[11px] text-slate-500 mt-1">Would try app for free</p>
        </div>

        <!-- Card 6 -->
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
          <div class="flex items-center justify-between text-slate-400 mb-2">
            <span class="text-xs font-medium uppercase tracking-wider">High Frequency</span>
            <i data-lucide="calendar" class="w-4 h-4 text-indigo-500"></i>
          </div>
          <div class="text-2xl font-bold text-indigo-600" id="kpiWeeklyUse">67%</div>
          <p class="text-[11px] text-slate-500 mt-1">Weekly+ expected use</p>
        </div>
      </div>

      <!-- ROW 1 CHARTS: DEMOGRAPHICS & DECISION FREQUENCY -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Age Breakdown -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-bold text-slate-900 text-sm">Age Group Demographics</h2>
            <span class="text-xs text-slate-400">Q1</span>
          </div>
          <div class="relative h-56">
            <canvas id="chartAge"></canvas>
          </div>
        </div>

        <!-- Gender Breakdown -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-bold text-slate-900 text-sm">Gender Distribution</h2>
            <span class="text-xs text-slate-400">Q2</span>
          </div>
          <div class="relative h-56 flex items-center justify-center">
            <canvas id="chartGender"></canvas>
          </div>
        </div>

        <!-- Frequency of Decision Difficulty -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-bold text-slate-900 text-sm">Difficulty Deciding What to Wear</h2>
            <span class="text-xs text-slate-400">Q3</span>
          </div>
          <div class="relative h-56">
            <canvas id="chartDifficulty"></canvas>
          </div>
        </div>
      </div>

      <!-- ROW 2 CHARTS: CLOTHING CHALLENGES & HOW USERS DECIDE -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Clothing-Related Challenges -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-1">
            <h2 class="font-bold text-slate-900 text-sm">Clothing Challenges Experienced (Multi-Select)</h2>
            <span class="text-xs text-slate-400">Q4</span>
          </div>
          <p class="text-xs text-slate-500 mb-4">Frequency of common wardrobe & outfit friction points</p>
          <div class="relative h-72">
            <canvas id="chartChallenges"></canvas>
          </div>
        </div>

        <!-- How Users Decide What to Wear -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-1">
            <h2 class="font-bold text-slate-900 text-sm">How Users Currently Decide What to Wear</h2>
            <span class="text-xs text-slate-400">Q5</span>
          </div>
          <p class="text-xs text-slate-500 mb-4">Decision channels (own judgment, social media, friends, apps)</p>
          <div class="relative h-72">
            <canvas id="chartDecide"></canvas>
          </div>
        </div>
      </div>

      <!-- ROW 3 CHARTS: PURCHASE REGRET & APP CONCEPT VALIDATION -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Purchase Regret in Past 3 Months -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-1">
            <h2 class="font-bold text-slate-900 text-sm">Purchase Regret (Past 3 Months)</h2>
            <span class="text-xs text-slate-400">Q6</span>
          </div>
          <p class="text-xs text-slate-500 mb-3">Color, fit, or matching mistakes</p>
          <div class="relative h-56 flex items-center justify-center">
            <canvas id="chartRegret"></canvas>
          </div>
        </div>

        <!-- Perceived App Usefulness -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-1">
            <h2 class="font-bold text-slate-900 text-sm">Fashion AI App Usefulness Rating</h2>
            <span class="text-xs text-slate-400">Q7</span>
          </div>
          <p class="text-xs text-slate-500 mb-3">Body type, skin tone & personal style</p>
          <div class="relative h-56">
            <canvas id="chartUsefulness"></canvas>
          </div>
        </div>

        <!-- Free Trial Likelihood -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-1">
            <h2 class="font-bold text-slate-900 text-sm">Likelihood to Try for Free</h2>
            <span class="text-xs text-slate-400">Q10</span>
          </div>
          <p class="text-xs text-slate-500 mb-3">Initial adoption willingness</p>
          <div class="relative h-56">
            <canvas id="chartTrial"></canvas>
          </div>
        </div>
      </div>

      <!-- ROW 4 CHARTS: FEATURE DEMAND & BARRIERS / CONCERNS -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Most Desired Features -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-1">
            <h2 class="font-bold text-slate-900 text-sm">Most Desired Features (Multi-Select)</h2>
            <span class="text-xs text-slate-400">Q8</span>
          </div>
          <p class="text-xs text-slate-500 mb-4">Which capabilities deliver maximum value to users?</p>
          <div class="relative h-72">
            <canvas id="chartFeatures"></canvas>
          </div>
        </div>

        <!-- Concerns / Barriers to Adoption -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-1">
            <h2 class="font-bold text-slate-900 text-sm">User Concerns & Potential Barriers</h2>
            <span class="text-xs text-slate-400">Q9</span>
          </div>
          <p class="text-xs text-slate-500 mb-4">Privacy, price sensitivity, and accuracy apprehensions</p>
          <div class="relative h-72">
            <canvas id="chartConcerns"></canvas>
          </div>
        </div>
      </div>

      <!-- ROW 5: USAGE FREQUENCY & OPEN CUSTOMER FEEDBACK -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Expected Usage Frequency -->
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs chart-card">
          <div class="flex items-center justify-between mb-1">
            <h2 class="font-bold text-slate-900 text-sm">Expected Frequency of Use</h2>
            <span class="text-xs text-slate-400">Q11</span>
          </div>
          <p class="text-xs text-slate-500 mb-3">If app meets personal style needs</p>
          <div class="relative h-64">
            <canvas id="chartFrequency"></canvas>
          </div>
        </div>

        <!-- Voice of Customer / Open Feedback -->
        <div class="lg:col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-2xs flex flex-col">
          <div class="flex items-center justify-between mb-1">
            <h2 class="font-bold text-slate-900 text-sm">Voice of Customer: Real User Quotes</h2>
            <span class="text-xs text-slate-400">Q12 Feedback Responses</span>
          </div>
          <p class="text-xs text-slate-500 mb-4">What makes a clothing recommendation service genuinely useful to real users?</p>
          
          <div id="feedbackQuotesContainer" class="grid grid-cols-1 md:grid-cols-2 gap-3 overflow-y-auto max-h-64 custom-scrollbar pr-1">
            <!-- Populated dynamically -->
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: RAW DATA TABLE EXPLORER -->
    <div id="tabContent-table" class="space-y-4 hidden">
      <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-3 flex-1 min-w-[240px]">
          <div class="relative flex-1 max-w-md">
            <i data-lucide="search" class="w-4 h-4 absolute left-3 top-2.5 text-slate-400"></i>
            <input type="text" id="tableSearchInput" oninput="renderTable()" placeholder="Search all responses (e.g. 18–24, color, budget)..." class="w-full text-xs pl-9 pr-3 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:outline-none">
          </div>
          <span id="tableRecordCount" class="text-xs text-slate-500 font-medium">24 rows</span>
        </div>

        <div class="flex items-center gap-2">
          <button onclick="exportData('csv')" class="inline-flex items-center gap-1 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition">
            <i data-lucide="download" class="w-3.5 h-3.5"></i> Export CSV
          </button>
          <button onclick="exportData('xlsx')" class="inline-flex items-center gap-1 px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 text-xs font-semibold rounded-lg border border-emerald-200 transition">
            <i data-lucide="file-spreadsheet" class="w-3.5 h-3.5"></i> Export Excel
          </button>
          <button onclick="exportData('json')" class="inline-flex items-center gap-1 px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-lg border border-indigo-200 transition">
            <i data-lucide="code" class="w-3.5 h-3.5"></i> Export JSON
          </button>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
        <div class="overflow-x-auto max-h-[600px] custom-scrollbar">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-50 text-slate-600 uppercase tracking-wider font-semibold sticky top-0 border-b border-slate-200 z-10">
              <tr id="tableHeaderRow">
                <!-- Dynamically generated -->
              </tr>
            </thead>
            <tbody id="tableBody" class="divide-y divide-slate-100 text-slate-700">
              <!-- Dynamically generated -->
            </tbody>
          </table>
        </div>

        <!-- Pagination Controls -->
        <div class="p-3 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600">
          <div class="flex items-center gap-2">
            <span>Rows per page:</span>
            <select id="rowsPerPage" onchange="renderTable(1)" class="bg-white border border-slate-300 rounded px-2 py-0.5">
              <option value="15">15</option>
              <option value="30" selected>30</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>

          <div class="flex items-center gap-2" id="paginationControls">
            <!-- Dynamically generated -->
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: SHEET CONVERTER & EXPORTER STUDIO -->
    <div id="tabContent-converter" class="space-y-6 hidden">
      <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs">
        <div class="max-w-3xl">
          <h2 class="text-lg font-bold text-slate-900 mb-1 flex items-center gap-2">
            <i data-lucide="refresh-ccw" class="w-5 h-5 text-brand-500"></i>
            Universal Sheet & Survey Converter Studio
          </h2>
          <p class="text-xs text-slate-500 mb-6">
            Convert your survey sheet between <strong>CSV</strong>, <strong>Excel (.xlsx)</strong>, <strong>JSON</strong>, and <strong>TSV</strong> with 1 click.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Step 1: Source Selection -->
          <div class="border border-slate-200 rounded-xl p-5 bg-slate-50 flex flex-col justify-between">
            <div>
              <div class="flex items-center gap-2 mb-3">
                <span class="w-6 h-6 rounded-full bg-brand-500 text-white font-bold text-xs flex items-center justify-center">1</span>
                <h3 class="font-bold text-sm text-slate-800">Select Input Source</h3>
              </div>

              <div class="space-y-3">
                <label class="flex items-start gap-2.5 p-3 rounded-lg border border-brand-200 bg-white cursor-pointer hover:border-brand-400 transition">
                  <input type="radio" name="converterSource" value="current" checked class="mt-0.5 text-brand-600">
                  <div>
                    <span class="font-semibold text-xs text-slate-800 block">Use Currently Active Dataset</span>
                    <span class="text-[11px] text-slate-500" id="converterActiveLabel">24 verified survey records from Google Sheet</span>
                  </div>
                </label>

                <label class="flex items-start gap-2.5 p-3 rounded-lg border border-slate-200 bg-white cursor-pointer hover:border-brand-400 transition">
                  <input type="radio" name="converterSource" value="upload" class="mt-0.5 text-brand-600">
                  <div class="w-full">
                    <span class="font-semibold text-xs text-slate-800 block mb-1">Upload New File (.xlsx, .csv, .json, .tsv)</span>
                    <input type="file" id="converterFileInput" accept=".csv, .xlsx, .xls, .tsv, .json" onchange="handleConverterUpload(event)" class="text-xs text-slate-500 file:mr-2 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100">
                  </div>
                </label>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-200 text-[11px] text-slate-500">
              Supports: Google Forms exports, Excel sheets, and CSV dumps.
            </div>
          </div>

          <!-- Step 2: Target Format & Download -->
          <div class="border border-slate-200 rounded-xl p-5 bg-slate-50 flex flex-col justify-between">
            <div>
              <div class="flex items-center gap-2 mb-3">
                <span class="w-6 h-6 rounded-full bg-brand-500 text-white font-bold text-xs flex items-center justify-center">2</span>
                <h3 class="font-bold text-sm text-slate-800">Choose Target Format & Convert</h3>
              </div>

              <div class="grid grid-cols-2 gap-3 mb-4">
                <button type="button" onclick="selectConvertFormat('csv')" id="btnFormat-csv" class="format-btn border-2 border-brand-500 bg-white p-3 rounded-lg text-left shadow-2xs hover:border-brand-600 transition">
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-bold text-xs text-brand-700">CSV (.csv)</span>
                    <i data-lucide="file-text" class="w-4 h-4 text-brand-500"></i>
                  </div>
                  <p class="text-[11px] text-slate-500">Comma-separated values for analytics, Python, or SQL.</p>
                </button>

                <button type="button" onclick="selectConvertFormat('xlsx')" id="btnFormat-xlsx" class="format-btn border border-slate-200 bg-white p-3 rounded-lg text-left shadow-2xs hover:border-brand-400 transition">
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-bold text-xs text-slate-800">Excel (.xlsx)</span>
                    <i data-lucide="sheet" class="w-4 h-4 text-emerald-500"></i>
                  </div>
                  <p class="text-[11px] text-slate-500">Standard Microsoft Excel workbook format.</p>
                </button>

                <button type="button" onclick="selectConvertFormat('json')" id="btnFormat-json" class="format-btn border border-slate-200 bg-white p-3 rounded-lg text-left shadow-2xs hover:border-brand-400 transition">
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-bold text-xs text-slate-800">JSON (.json)</span>
                    <i data-lucide="code" class="w-4 h-4 text-indigo-500"></i>
                  </div>
                  <p class="text-[11px] text-slate-500">Structured JavaScript Object Notation for APIs.</p>
                </button>

                <button type="button" onclick="selectConvertFormat('tsv')" id="btnFormat-tsv" class="format-btn border border-slate-200 bg-white p-3 rounded-lg text-left shadow-2xs hover:border-brand-400 transition">
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-bold text-xs text-slate-800">TSV (.tsv)</span>
                    <i data-lucide="file" class="w-4 h-4 text-amber-500"></i>
                  </div>
                  <p class="text-[11px] text-slate-500">Tab-separated values, convenient for pasting.</p>
                </button>
              </div>

              <!-- Options -->
              <div class="bg-white p-3 rounded-lg border border-slate-200 space-y-2 mb-4">
                <label class="flex items-center gap-2 text-xs text-slate-700">
                  <input type="checkbox" id="optOnlyFiltered" class="rounded text-brand-600">
                  <span>Export only currently filtered rows (<span id="optFilteredCount">24</span> rows)</span>
                </label>
                <label class="flex items-center gap-2 text-xs text-slate-700">
                  <input type="checkbox" id="optSanitizeHeaders" checked class="rounded text-brand-600">
                  <span>Shorten question headers to concise labels (e.g. "Age", "Gender")</span>
                </label>
              </div>
            </div>

            <div>
              <button onclick="executeConversion()" class="w-full py-2.5 px-4 bg-brand-500 hover:bg-brand-600 text-white rounded-lg text-sm font-semibold shadow-sm transition flex items-center justify-center gap-2">
                <i data-lucide="download" class="w-4 h-4"></i>
                <span id="convertBtnLabel">Convert & Download as .CSV</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Preview Box -->
        <div class="mt-6 border-t border-slate-200 pt-5">
          <h3 class="font-bold text-xs uppercase tracking-wider text-slate-500 mb-2">Live Output Preview (First 3 Records)</h3>
          <pre id="converterPreviewBox" class="bg-slate-900 text-emerald-400 p-4 rounded-xl text-xs font-mono overflow-x-auto max-h-48 custom-scrollbar">Loading preview...</pre>
        </div>
      </div>
    </div>

    <!-- TAB 4: GOOGLE SHEET LIVE CONNECTION -->
    <div id="tabContent-googleSync" class="space-y-6 hidden">
      <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs max-w-4xl">
        <h2 class="text-lg font-bold text-slate-900 mb-1 flex items-center gap-2">
          <i data-lucide="cloud" class="w-5 h-5 text-emerald-600"></i>
          Connect Live Google Sheet / Google Forms
        </h2>
        <p class="text-xs text-slate-500 mb-6">
          Directly load responses from your Google Sheet or Google Form responses spreadsheet.
        </p>

        <!-- Google Sheet URL form -->
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-5 mb-6">
          <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
            Google Sheet URL:
          </label>
          <div class="flex flex-col sm:flex-row gap-2">
            <input type="text" id="googleSheetUrlInput" value="https://docs.google.com/spreadsheets/d/1qTx1-al8moCYeGvao8Ak2tenngJtJoepLAjtXGqWVTU/edit?usp=sharing" class="flex-1 text-xs px-3 py-2 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:outline-none">
            <button onclick="fetchGoogleSheet()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-2xs transition flex items-center justify-center gap-1.5 whitespace-nowrap">
              <i data-lucide="download-cloud" class="w-4 h-4"></i>
              <span>Re-sync Live Data</span>
            </button>
          </div>
          <p id="googleSyncStatus" class="text-xs text-slate-500 mt-2">
            <span class="text-emerald-600 font-medium">Currently connected: 24 responses loaded directly from this sheet!</span>
          </p>
        </div>

        <!-- Helpful Guide -->
        <div class="border border-slate-200 rounded-xl p-5 bg-white space-y-4">
          <h3 class="font-bold text-sm text-slate-800 flex items-center gap-2">
            <i data-lucide="info" class="w-4 h-4 text-brand-500"></i>
            How Google Sheet Sync Works:
          </h3>

          <ol class="list-decimal list-inside text-xs text-slate-600 space-y-2.5 leading-relaxed">
            <li>
              When respondents submit new answers to your Google Form (<code class="bg-slate-100 text-brand-700 px-1 py-0.5 rounded">https://forms.gle/V2yEvZp1AhoJR1iw6</code>), they appear immediately in your linked Google Sheet.
            </li>
            <li>
              Click the green <strong>"Re-sync Live Data"</strong> button above, and this dashboard will query the latest data and update all charts, KPI cards, and the raw data table!
            </li>
            <li>
              You can also use the terminal anytime:
              <br><code class="bg-slate-100 text-slate-800 px-1.5 py-0.5 rounded block mt-1 font-mono">python convert_sheet.py --google-sheet "https://docs.google.com/spreadsheets/d/1qTx1-al8moCYeGvao8Ak2tenngJtJoepLAjtXGqWVTU/edit?usp=sharing" real_survey_responses.csv</code>
            </li>
          </ol>
        </div>
      </div>
    </div>

  </main>

  <!-- ROW DETAIL MODAL -->
  <div id="rowDetailModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-50 hidden flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-xl border border-slate-200">
      <div class="p-4 border-b border-slate-200 flex items-center justify-between">
        <h3 class="font-bold text-slate-900 text-sm flex items-center gap-2">
          <i data-lucide="file-text" class="w-4 h-4 text-brand-500"></i>
          Response Detail Inspector
        </h3>
        <button onclick="closeRowModal()" class="text-slate-400 hover:text-slate-700">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div id="rowModalBody" class="p-5 overflow-y-auto space-y-3 text-xs custom-scrollbar">
        <!-- Dynamically filled -->
      </div>
      <div class="p-3 border-t border-slate-200 bg-slate-50 flex justify-end">
        <button onclick="closeRowModal()" class="px-4 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-700 font-semibold text-xs rounded-lg transition">Close</button>
      </div>
    </div>
  </div>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    // Embedded datasets
    const REAL_DATA = {real_json_str};
    const DEMO_DATA = {demo_json_str};

    let currentData = [...REAL_DATA];
    let filteredData = [...REAL_DATA];
    let activeDatasetName = 'real';
    let selectedFormat = 'csv';
    let currentPage = 1;

    // Chart instances store
    let charts = {{}};

    // DOM Ready
    window.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();
      initDashboard();
    }});

    function switchDataset(type) {{
      activeDatasetName = type;
      if (type === 'real') {{
        currentData = [...REAL_DATA];
        document.getElementById('btnSetReal').className = 'px-2.5 py-1 rounded-md bg-white text-brand-700 shadow-2xs transition';
        document.getElementById('btnSetDemo').className = 'px-2.5 py-1 rounded-md text-slate-600 hover:text-slate-900 transition';
        document.getElementById('headerDatasetLabel').textContent = '24 Real Survey Responses Loaded';
      }} else {{
        currentData = [...DEMO_DATA];
        document.getElementById('btnSetDemo').className = 'px-2.5 py-1 rounded-md bg-white text-brand-700 shadow-2xs transition';
        document.getElementById('btnSetReal').className = 'px-2.5 py-1 rounded-md text-slate-600 hover:text-slate-900 transition';
        document.getElementById('headerDatasetLabel').textContent = '130 Demo Projections Loaded';
      }}
      filteredData = [...currentData];
      resetFilters();
    }}

    function initDashboard() {{
      updateKPIs();
      renderAllCharts();
      renderQuotes();
      renderTable();
      updateConverterPreview();
      updateFilteredCountBadge();
    }}

    // TAB SWITCHING
    function switchTab(tabId) {{
      ['dashboard', 'table', 'converter', 'googleSync'].forEach(t => {{
        document.getElementById(`tabContent-${{t}}`).classList.add('hidden');
        const btn = document.getElementById(`tabBtn-${{t}}`);
        btn.classList.remove('text-brand-600', 'border-b-2', 'border-brand-500', 'font-semibold');
        btn.classList.add('text-slate-500', 'font-medium');
      }});

      document.getElementById(`tabContent-${{tabId}}`).classList.remove('hidden');
      const activeBtn = document.getElementById(`tabBtn-${{tabId}}`);
      activeBtn.classList.remove('text-slate-500', 'font-medium');
      activeBtn.classList.add('text-brand-600', 'border-b-2', 'border-brand-500', 'font-semibold');

      if (tabId === 'table') {{
        renderTable();
      }} else if (tabId === 'converter') {{
        updateConverterPreview();
      }}
      lucide.createIcons();
    }}

    // FILTER LOGIC
    function applyFilters() {{
      const gender = document.getElementById('filterGender').value;
      const age = document.getElementById('filterAge').value;
      const diff = document.getElementById('filterDiff').value;
      const trial = document.getElementById('filterTrial').value;

      filteredData = currentData.filter(row => {{
        // Gender filter
        const gVal = getColVal(row, 'gender');
        if (gender !== 'All' && gVal.toLowerCase() !== gender.toLowerCase()) return false;
        
        // Age filter
        const aVal = getColVal(row, 'age');
        if (age !== 'All') {{
          // normalize
          const normAge = aVal.replace('-', '–').trim();
          const normTarget = age.replace('-', '–').trim();
          if (normAge !== normTarget) return false;
        }}
        
        // Difficulty filter
        if (diff !== 'All') {{
          const rowDiff = getColVal(row, 'difficult to decide');
          if (diff === 'High' && !['Often', 'Always'].includes(rowDiff)) return false;
          if (diff === 'Sometimes' && rowDiff !== 'Sometimes') return false;
          if (diff === 'Low' && !['Never', 'Occasionally'].includes(rowDiff)) return false;
        }}

        // Trial intent filter
        if (trial !== 'All') {{
          const rowTrial = getColVal(row, 'try it for free');
          if (trial === 'Positive' && !rowTrial.includes('would try it')) return false;
          if (trial === 'Neutral' && rowTrial !== 'Not sure') return false;
          if (trial === 'Negative' && !rowTrial.includes('would not try it')) return false;
        }}

        return true;
      }});

      updateFilteredCountBadge();
      updateKPIs();
      renderAllCharts();
      renderQuotes();
      renderTable(1);
      updateConverterPreview();
    }}

    function resetFilters() {{
      document.getElementById('filterGender').value = 'All';
      document.getElementById('filterAge').value = 'All';
      document.getElementById('filterDiff').value = 'All';
      document.getElementById('filterTrial').value = 'All';
      filteredData = [...currentData];
      updateFilteredCountBadge();
      updateKPIs();
      renderAllCharts();
      renderQuotes();
      renderTable(1);
      updateConverterPreview();
    }}

    function updateFilteredCountBadge() {{
      const badge = document.getElementById('filteredCountBadge');
      badge.textContent = `Showing ${{filteredData.length}} of ${{currentData.length}}`;
      document.getElementById('optFilteredCount').textContent = filteredData.length;
      document.getElementById('converterActiveLabel').textContent = `${{currentData.length}} records (${{activeDatasetName === 'real' ? 'Real Google Sheet' : 'Demo Model'}})`;
    }}

    // KPI METRIC CALCULATIONS
    function updateKPIs() {{
      const total = filteredData.length;
      document.getElementById('kpiTotal').textContent = total;

      if (total === 0) {{
        document.getElementById('kpiDifficultyRate').textContent = '0%';
        document.getElementById('kpiRegretRate').textContent = '0%';
        document.getElementById('kpiUtilityRate').textContent = '0%';
        document.getElementById('kpiTrialRate').textContent = '0%';
        document.getElementById('kpiWeeklyUse').textContent = '0%';
        return;
      }}

      // Style struggle (Often + Always + Sometimes)
      const diffCount = filteredData.filter(r => {{
        const v = getColVal(r, 'difficult to decide');
        return ['Sometimes', 'Often', 'Always'].includes(v);
      }}).length;
      document.getElementById('kpiDifficultyRate').textContent = Math.round((diffCount / total) * 100) + '%';

      // Purchase regret (1 or more times)
      const regretCount = filteredData.filter(r => {{
        const v = getColVal(r, 'regretted buying');
        return ['Once', 'Two or three times', 'Four or more times'].includes(v);
      }}).length;
      document.getElementById('kpiRegretRate').textContent = Math.round((regretCount / total) * 100) + '%';

      // Utility (Moderately, Very, Extremely useful)
      const utilityCount = filteredData.filter(r => {{
        const v = getColVal(r, 'useful would it be');
        return ['Moderately useful', 'Very useful', 'Extremely useful'].includes(v);
      }}).length;
      document.getElementById('kpiUtilityRate').textContent = Math.round((utilityCount / total) * 100) + '%';

      // Trial intent (Definitely or Probably would try)
      const trialCount = filteredData.filter(r => {{
        const v = getColVal(r, 'try it for free');
        return ['Definitely would try it', 'Probably would try it'].includes(v);
      }}).length;
      document.getElementById('kpiTrialRate').textContent = Math.round((trialCount / total) * 100) + '%';

      // Weekly+ expected use
      const freqCount = filteredData.filter(r => {{
        const v = getColVal(r, 'how often do you think you would use it');
        return ['Daily or almost daily', 'Several times a week', 'About once a week'].includes(v);
      }}).length;
      document.getElementById('kpiWeeklyUse').textContent = Math.round((freqCount / total) * 100) + '%';
    }}

    // CHART RENDERING
    function renderAllCharts() {{
      renderChartAge();
      renderChartGender();
      renderChartDifficulty();
      renderChartChallenges();
      renderChartDecide();
      renderChartRegret();
      renderChartUsefulness();
      renderChartTrial();
      renderChartFeatures();
      renderChartConcerns();
      renderChartFrequency();
    }}

    function createOrUpdateChart(id, config) {{
      if (charts[id]) {{
        charts[id].destroy();
      }}
      const ctx = document.getElementById(id).getContext('2d');
      charts[id] = new Chart(ctx, config);
    }}

    // Q1: Age
    function renderChartAge() {{
      const counts = countFrequenciesByKeyword('age group');
      const order = ['Under 18', '18–24', '25–34', '35–44', '45–54', '55 or above'];
      const data = order.map(o => counts[o] || counts[o.replace('–', '-')] || 0);

      createOrUpdateChart('chartAge', {{
        type: 'bar',
        data: {{
          labels: order,
          datasets: [{{
            data: data,
            backgroundColor: '#6366f1',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});
    }}

    // Q2: Gender
    function renderChartGender() {{
      const counts = countFrequenciesByKeyword('gender');
      createOrUpdateChart('chartGender', {{
        type: 'doughnut',
        data: {{
          labels: Object.keys(counts),
          datasets: [{{
            data: Object.values(counts),
            backgroundColor: ['#5746e3', '#ec4899', '#94a3b8'],
            borderWidth: 2,
            borderColor: '#ffffff'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }}
          }},
          cutout: '65%'
        }}
      }});
    }}

    // Q3: Difficulty Deciding
    function renderChartDifficulty() {{
      const counts = countFrequenciesByKeyword('difficult to decide');
      const order = ['Never', 'Occasionally', 'Sometimes', 'Often', 'Always'];
      const data = order.map(o => counts[o] || 0);

      createOrUpdateChart('chartDifficulty', {{
        type: 'bar',
        data: {{
          labels: order,
          datasets: [{{
            data: data,
            backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#f97316', '#ef4444'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});
    }}

    // Q4: Clothing Challenges (Multi-select)
    function renderChartChallenges() {{
      const counts = countMultiSelectByKeyword('challenges');
      const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);

      createOrUpdateChart('chartChallenges', {{
        type: 'bar',
        data: {{
          labels: sorted.map(s => s[0]),
          datasets: [{{
            data: sorted.map(s => s[1]),
            backgroundColor: '#818cf8',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
            y: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }} }} }}
          }}
        }}
      }});
    }}

    // Q5: How users decide (Multi-select)
    function renderChartDecide() {{
      const counts = countMultiSelectByKeyword('usually decide');
      const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);

      createOrUpdateChart('chartDecide', {{
        type: 'bar',
        data: {{
          labels: sorted.map(s => s[0]),
          datasets: [{{
            data: sorted.map(s => s[1]),
            backgroundColor: '#38bdf8',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
            y: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }} }} }}
          }}
        }}
      }});
    }}

    // Q6: Purchase Regret
    function renderChartRegret() {{
      const counts = countFrequenciesByKeyword('regretted buying');
      createOrUpdateChart('chartRegret', {{
        type: 'doughnut',
        data: {{
          labels: Object.keys(counts),
          datasets: [{{
            data: Object.values(counts),
            backgroundColor: ['#10b981', '#fbbf24', '#f97316', '#ef4444', '#cbd5e1', '#94a3b8'],
            borderWidth: 2,
            borderColor: '#ffffff'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ boxWidth: 10, font: {{ size: 10 }} }} }}
          }},
          cutout: '60%'
        }}
      }});
    }}

    // Q7: App Usefulness
    function renderChartUsefulness() {{
      const counts = countFrequenciesByKeyword('useful would it be');
      const order = ['Not at all useful', 'Slightly useful', 'Moderately useful', 'Very useful', 'Extremely useful', 'Not sure'];
      const data = order.map(o => counts[o] || 0);

      createOrUpdateChart('chartUsefulness', {{
        type: 'bar',
        data: {{
          labels: order,
          datasets: [{{
            data: data,
            backgroundColor: ['#94a3b8', '#cbd5e1', '#a5b4fc', '#6366f1', '#4338ca', '#e2e8f0'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 9 }} }} }}
          }}
        }}
      }});
    }}

    // Q10: Trial Likelihood
    function renderChartTrial() {{
      const counts = countFrequenciesByKeyword('try it for free');
      const order = ['Definitely would try it', 'Probably would try it', 'Not sure', 'Probably would not try it', 'Definitely would not try it'];
      const data = order.map(o => counts[o] || 0);

      createOrUpdateChart('chartTrial', {{
        type: 'bar',
        data: {{
          labels: ['Definitely', 'Probably', 'Not sure', 'Prob Not', 'Def Not'],
          datasets: [{{
            data: data,
            backgroundColor: ['#059669', '#10b981', '#f59e0b', '#f97316', '#dc2626'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});
    }}

    // Q8: Features (Multi-select)
    function renderChartFeatures() {{
      const counts = countMultiSelectByKeyword('features');
      const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);

      createOrUpdateChart('chartFeatures', {{
        type: 'bar',
        data: {{
          labels: sorted.map(s => s[0]),
          datasets: [{{
            data: sorted.map(s => s[1]),
            backgroundColor: '#10b981',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
            y: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }} }} }}
          }}
        }}
      }});
    }}

    // Q9: Concerns (Multi-select)
    function renderChartConcerns() {{
      const counts = countMultiSelectByKeyword('concerns');
      const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);

      createOrUpdateChart('chartConcerns', {{
        type: 'bar',
        data: {{
          labels: sorted.map(s => s[0]),
          datasets: [{{
            data: sorted.map(s => s[1]),
            backgroundColor: '#f43f5e',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
            y: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10 }} }} }}
          }}
        }}
      }});
    }}

    // Q11: Expected Frequency
    function renderChartFrequency() {{
      const counts = countFrequenciesByKeyword('how often do you think you would use it');
      const order = ['Daily or almost daily', 'Several times a week', 'About once a week', 'A few times a month', 'Less than once a month', 'Never', 'Not sure'];
      const data = order.map(o => counts[o] || 0);

      createOrUpdateChart('chartFrequency', {{
        type: 'bar',
        data: {{
          labels: ['Daily', 'Few/week', 'Weekly', 'Few/month', '< Monthly', 'Never', 'Not sure'],
          datasets: [{{
            data: data,
            backgroundColor: '#6366f1',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ beginAtZero: true, grid: {{ color: '#f1f5f9' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 9 }} }} }}
          }}
        }}
      }});
    }}

    // RENDER VOICE OF CUSTOMER QUOTES
    function renderQuotes() {{
      const container = document.getElementById('feedbackQuotesContainer');
      container.innerHTML = '';

      const quotes = filteredData
        .map(r => ({{
          text: getColVal(r, 'genuinely useful') || getColVal(r, '12.'),
          age: getColVal(r, 'age'),
          gender: getColVal(r, 'gender')
        }}))
        .filter(q => q.text && q.text.trim().length > 0);

      if (quotes.length === 0) {{
        container.innerHTML = '<p class="text-xs text-slate-400 italic col-span-2">No written feedback matches current filter selection.</p>';
        return;
      }}

      quotes.forEach(q => {{
        const card = document.createElement('div');
        card.className = 'bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs flex flex-col justify-between hover:bg-white hover:border-brand-200 transition';
        card.innerHTML = `
          <p class="text-slate-800 font-medium mb-2 leading-relaxed">"${{escapeHtml(q.text)}}"</p>
          <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-100">
            <span>${{escapeHtml(q.gender || 'Respondent')}}, ${{escapeHtml(q.age || '')}}</span>
            <span class="text-brand-600 font-semibold">Verified Response</span>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    // DATA TABLE RENDERING
    function renderTable(page = currentPage) {{
      currentPage = page;
      const search = (document.getElementById('tableSearchInput')?.value || '').toLowerCase();
      const rowsPerPage = parseInt(document.getElementById('rowsPerPage')?.value || '30', 10);

      const tableData = filteredData.filter(row => {{
        if (!search) return true;
        return Object.values(row).some(v => String(v).toLowerCase().includes(search));
      }});

      document.getElementById('tableRecordCount').textContent = `${{tableData.length}} matching rows`;

      // Build Headers
      const headers = Object.keys(currentData[0] || {{}});
      const thead = document.getElementById('tableHeaderRow');
      thead.innerHTML = '<th class="p-3">#</th>' + headers.map(h => `<th class="p-3 whitespace-nowrap">${{escapeHtml(shortenHeader(h))}}</th>`).join('') + '<th class="p-3">Action</th>';

      // Build Rows
      const tbody = document.getElementById('tableBody');
      tbody.innerHTML = '';

      const startIndex = (currentPage - 1) * rowsPerPage;
      const paginated = tableData.slice(startIndex, startIndex + rowsPerPage);

      paginated.forEach((row, idx) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 transition cursor-pointer';
        tr.onclick = () => openRowModal(row);

        let html = `<td class="p-3 font-mono text-slate-400">${{startIndex + idx + 1}}</td>`;
        headers.forEach(h => {{
          const val = row[h] || '';
          html += `<td class="p-3 max-w-[200px] truncate" title="${{escapeHtml(val)}}">${{escapeHtml(val)}}</td>`;
        }});
        html += `<td class="p-3"><button onclick="event.stopPropagation(); openRowModal(JSON.parse('${{escapeJsonAttr(row)}}'))" class="text-brand-600 font-semibold hover:underline">View</button></td>`;
        tr.innerHTML = html;
        tbody.appendChild(tr);
      }});

      // Render Pagination
      const totalPages = Math.ceil(tableData.length / rowsPerPage) || 1;
      const pagContainer = document.getElementById('paginationControls');
      pagContainer.innerHTML = `
        <button onclick="renderTable(${{Math.max(1, currentPage - 1)}})" ${{currentPage === 1 ? 'disabled class="opacity-50"' : 'class="hover:text-brand-600"'}}>Prev</button>
        <span class="font-semibold text-slate-700">Page ${{currentPage}} of ${{totalPages}}</span>
        <button onclick="renderTable(${{Math.min(totalPages, currentPage + 1)}})" ${{currentPage === totalPages ? 'disabled class="opacity-50"' : 'class="hover:text-brand-600"'}}>Next</button>
      `;
    }}

    // MODAL ROW INSPECTOR
    function openRowModal(row) {{
      const modal = document.getElementById('rowDetailModal');
      const body = document.getElementById('rowModalBody');
      body.innerHTML = '';

      Object.entries(row).forEach(([key, val]) => {{
        const field = document.createElement('div');
        field.className = 'border-b border-slate-100 pb-2';
        field.innerHTML = `
          <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-0.5">${{escapeHtml(key)}}</div>
          <div class="text-slate-800 text-xs font-medium">${{escapeHtml(val || '—')}}</div>
        `;
        body.appendChild(field);
      }});

      modal.classList.remove('hidden');
    }}

    function closeRowModal() {{
      document.getElementById('rowDetailModal').classList.add('hidden');
    }}

    // CONVERTER LOGIC
    function selectConvertFormat(fmt) {{
      selectedFormat = fmt;
      document.querySelectorAll('.format-btn').forEach(btn => {{
        btn.classList.remove('border-2', 'border-brand-500', 'text-brand-700');
        btn.classList.add('border', 'border-slate-200');
      }});

      const activeBtn = document.getElementById(`btnFormat-${{fmt}}`);
      activeBtn.classList.remove('border-slate-200');
      activeBtn.classList.add('border-2', 'border-brand-500', 'text-brand-700');

      document.getElementById('convertBtnLabel').textContent = `Convert & Download as .${{fmt.toUpperCase()}}`;
      updateConverterPreview();
    }}

    function getDatasetForExport() {{
      const onlyFiltered = document.getElementById('optOnlyFiltered')?.checked;
      const dataToExport = onlyFiltered ? filteredData : currentData;
      const sanitize = document.getElementById('optSanitizeHeaders')?.checked;

      if (!sanitize) return dataToExport;

      return dataToExport.map(row => {{
        const sanitized = {{}};
        Object.entries(row).forEach(([k, v]) => {{
          sanitized[shortenHeader(k)] = v;
        }});
        return sanitized;
      }});
    }}

    function updateConverterPreview() {{
      const previewBox = document.getElementById('converterPreviewBox');
      const sample = getDatasetForExport().slice(0, 3);

      if (selectedFormat === 'json') {{
        previewBox.textContent = JSON.stringify(sample, null, 2);
      }} else if (selectedFormat === 'csv') {{
        previewBox.textContent = jsonToCsv(sample);
      }} else if (selectedFormat === 'tsv') {{
        previewBox.textContent = jsonToTsv(sample);
      }} else if (selectedFormat === 'xlsx') {{
        previewBox.textContent = `[Excel Workbook (.xlsx) binary format preview]\\nRecords: ${{getDatasetForExport().length}}\\nHeaders: ${{Object.keys(sample[0] || {{}}).join(', ')}}\\nSheet name: Survey_Responses`;
      }}
    }}

    function executeConversion() {{
      exportData(selectedFormat);
    }}

    function exportData(format) {{
      const data = getDatasetForExport();
      const filename = `veyro_survey_data_${{new Date().toISOString().slice(0,10)}}.${{format}}`;

      if (format === 'json') {{
        downloadFile(JSON.stringify(data, null, 2), filename, 'application/json');
      }} else if (format === 'csv') {{
        const csvStr = jsonToCsv(data);
        downloadFile(csvStr, filename, 'text/csv;charset=utf-8;');
      }} else if (format === 'tsv') {{
        const tsvStr = jsonToTsv(data);
        downloadFile(tsvStr, filename, 'text/tab-separated-values;charset=utf-8;');
      }} else if (format === 'xlsx') {{
        const ws = XLSX.utils.json_to_sheet(data);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Survey Responses");
        XLSX.writeFile(wb, filename);
      }}
    }}

    function downloadFile(content, fileName, mimeType) {{
      const blob = new Blob([content], {{ type: mimeType }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}

    function jsonToCsv(items) {{
      if (items.length === 0) return '';
      const headers = Object.keys(items[0]);
      const headerRow = headers.map(h => `"${{h.replace(/"/g, '""')}}"`).join(',');
      const rows = items.map(item => {{
        return headers.map(h => {{
          const val = item[h] === null || item[h] === undefined ? '' : String(item[h]);
          return `"${{val.replace(/"/g, '""')}}"`;
        }}).join(',');
      }});
      return [headerRow, ...rows].join('\\r\\n');
    }}

    function jsonToTsv(items) {{
      if (items.length === 0) return '';
      const headers = Object.keys(items[0]);
      const headerRow = headers.join('\\t');
      const rows = items.map(item => {{
        return headers.map(h => {{
          const val = item[h] === null || item[h] === undefined ? '' : String(item[h]);
          return val.replace(/\\t/g, ' ').replace(/\\r?\\n/g, ' ');
        }}).join('\\t');
      }});
      return [headerRow, ...rows].join('\\r\\n');
    }}

    // UPLOAD PARSER
    function handleFileUpload(e) {{
      const file = e.target.files[0];
      if (!file) return;
      parseUploadedFile(file);
    }}

    function handleConverterUpload(e) {{
      const file = e.target.files[0];
      if (!file) return;
      parseUploadedFile(file);
    }}

    function parseUploadedFile(file) {{
      const reader = new FileReader();
      const ext = file.name.split('.').pop().toLowerCase();

      reader.onload = function(evt) {{
        try {{
          let parsed = [];
          if (ext === 'json') {{
            parsed = JSON.parse(evt.target.result);
          }} else if (['xlsx', 'xls'].includes(ext)) {{
            const data = new Uint8Array(evt.target.result);
            const workbook = XLSX.read(data, {{ type: 'array' }});
            const firstSheet = workbook.SheetNames[0];
            parsed = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheet]);
          }} else {{
            const workbook = XLSX.read(evt.target.result, {{ type: 'string' }});
            const firstSheet = workbook.SheetNames[0];
            parsed = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheet]);
          }}

          if (parsed && parsed.length > 0) {{
            currentData = parsed;
            filteredData = [...currentData];
            initDashboard();
            alert(`Successfully loaded ${{parsed.length}} records from ${{file.name}}!`);
          }} else {{
            alert('File was empty or could not parse valid rows.');
          }}
        }} catch(err) {{
          console.error(err);
          alert('Error parsing file: ' + err.message);
        }}
      }};

      if (['xlsx', 'xls'].includes(ext)) {{
        reader.readAsArrayBuffer(file);
      }} else {{
        reader.readAsText(file);
      }}
    }}

    // GOOGLE SHEET FETCH (direct without gid to avoid empty tab error)
    async function fetchGoogleSheet() {{
      const input = document.getElementById('googleSheetUrlInput').value.trim();
      const status = document.getElementById('googleSyncStatus');
      if (!input) {{
        status.innerHTML = '<span class="text-rose-600">Please enter a valid Google Sheet URL.</span>';
        return;
      }}

      const match = input.match(/\\/spreadsheets\\/d\\/([a-zA-Z0-9-_]+)/);
      const sheetId = match ? match[1] : input;

      const exportUrl = `https://docs.google.com/spreadsheets/d/${{sheetId}}/gviz/tq?tqx=out:csv`;

      status.innerHTML = `<span class="text-slate-600 animate-pulse">Syncing with Google Sheet...</span>`;

      try {{
        const resp = await fetch(exportUrl);
        if (!resp.ok) throw new Error(`HTTP ${{resp.status}}`);
        const csvText = await resp.text();
        const workbook = XLSX.read(csvText, {{ type: 'string' }});
        const firstSheet = workbook.SheetNames[0];
        const parsed = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheet]);

        // Clean out empty rows
        const valid = parsed.filter(row => Object.values(row).filter(Boolean).length >= 3);

        if (valid.length > 0) {{
          currentData = valid;
          filteredData = [...currentData];
          initDashboard();
          status.innerHTML = `<span class="text-emerald-600 font-semibold">Success! Synced ${{valid.length}} live rows from Google Sheet.</span>`;
        }} else {{
          status.innerHTML = `<span class="text-amber-600">Sheet returned 0 rows.</span>`;
        }}
      }} catch (e) {{
        status.innerHTML = `
          <div class="text-rose-600">
            <strong>Browser sync note:</strong> If your browser blocks cross-origin requests, run in terminal:<br>
            <code class="bg-slate-200 text-slate-800 px-1 py-0.5 rounded font-mono">python convert_sheet.py --google-sheet "${{input}}" real_survey_responses.csv</code>
          </div>
        `;
      }}
    }}

    // HELPER FUNCTIONS
    function getColVal(row, keyword) {{
      const kw = keyword.toLowerCase();
      for (const [k, v] of Object.entries(row)) {{
        if (k.toLowerCase().includes(kw)) {{
          return String(v || '').trim();
        }}
      }}
      return '';
    }}

    function countFrequenciesByKeyword(keyword) {{
      const counts = {{}};
      filteredData.forEach(row => {{
        const val = getColVal(row, keyword);
        if (val) {{
          counts[val] = (counts[val] || 0) + 1;
        }}
      }});
      return counts;
    }}

    function countMultiSelectByKeyword(keyword) {{
      const counts = {{}};
      filteredData.forEach(row => {{
        const raw = getColVal(row, keyword);
        if (!raw) return;
        const items = raw.split(/[;,]/).map(s => s.trim()).filter(Boolean);
        items.forEach(it => {{
          counts[it] = (counts[it] || 0) + 1;
        }});
      }});
      return counts;
    }}

    function shortenHeader(h) {{
      if (h.includes('age group')) return 'Age';
      if (h.includes('gender')) return 'Gender';
      if (h.includes('difficult to decide')) return 'Decision Difficulty';
      if (h.includes('challenges')) return 'Challenges';
      if (h.includes('usually decide')) return 'Decision Source';
      if (h.includes('regretted buying')) return 'Purchase Regret';
      if (h.includes('useful would it be')) return 'App Usefulness';
      if (h.includes('features')) return 'Features Desired';
      if (h.includes('concerns')) return 'Concerns';
      if (h.includes('try it for free')) return 'Trial Likelihood';
      if (h.includes('how often do you think you would use it')) return 'Usage Frequency';
      if (h.includes('genuinely useful') || h.includes('12.')) return 'Written Feedback';
      return h;
    }}

    function escapeHtml(str) {{
      if (str === null || str === undefined) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }}

    function escapeJsonAttr(obj) {{
      return JSON.stringify(obj).replace(/'/g, "&#39;");
    }}
  </script>
</body>
</html>
'''

with open(r'c:\Users\ROHIT SAGAR PATRA\OneDrive\Documents\dashboard for survey\index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Successfully regenerated index.html with live Google Sheet responses!")
