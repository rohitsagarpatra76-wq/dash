import urllib.request
import re

url = "https://docs.google.com/spreadsheets/d/1qTx1-al8moCYeGvao8Ak2tenngJtJoepLAjtXGqWVTU/edit?usp=sharing"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        print("Final URL:", resp.geturl())
        print("Status code:", resp.getcode())
        html = resp.read().decode('utf-8', errors='replace')
        print("HTML length:", len(html))
        
        # Check title
        title_m = re.search(r'<title>(.*?)</title>', html)
        if title_m:
            print("Page Title:", title_m.group(1))
            
        gids = re.findall(r'"sheetId":([0-9]+)', html)
        print("Found sheetIds / gids:", set(gids))
        
        # Try export with each gid
        for gid in set(gids):
            export_url = f"https://docs.google.com/spreadsheets/d/1qTx1-al8moCYeGvao8Ak2tenngJtJoepLAjtXGqWVTU/export?format=csv&gid={gid}"
            print(f"Testing export for gid={gid}: {export_url}")
            try:
                ex_req = urllib.request.Request(export_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(ex_req) as ex_resp:
                    data = ex_resp.read()
                    print(f"  Result bytes: {len(data)}")
                    if len(data) > 0:
                        print("  Sample data:", data[:200].decode('utf-8', errors='replace'))
                        with open(f"sheet_gid_{gid}.csv", "wb") as f:
                            f.write(data)
            except Exception as ex:
                print(f"  Error on gid={gid}:", ex)

        # Also try gviz
        gviz_url = "https://docs.google.com/spreadsheets/d/1qTx1-al8moCYeGvao8Ak2tenngJtJoepLAjtXGqWVTU/gviz/tq?tqx=out:csv"
        try:
            ex_req = urllib.request.Request(gviz_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(ex_req) as ex_resp:
                data = ex_resp.read()
                print("gviz bytes:", len(data))
                if len(data) > 0:
                    print("gviz sample:", data[:200].decode('utf-8', errors='replace'))
                    with open("sheet_gviz.csv", "wb") as f:
                        f.write(data)
        except Exception as ex:
            print("gviz error:", ex)

except Exception as e:
    print("Main Error:", e)
