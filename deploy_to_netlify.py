"""
Deploy VEYRO Survey Dashboard to Netlify
Supports:
1. Automated API deploy if you have a Netlify Personal Access Token:
   python deploy_to_netlify.py --token <YOUR_NETLIFY_TOKEN>
2. 1-Click Netlify Drop (drag & drop netlify_deploy.zip onto app.netlify.com/drop)
"""

import sys
import os
import urllib.request
import json
import webbrowser
import subprocess

ZIP_FILE = 'netlify_deploy.zip'
SITE_NAME_PREFIX = 'veyro-survey-dashboard'

def deploy_via_api(token, site_name=None):
    if not os.path.exists(ZIP_FILE):
        print(f"[!] Error: {ZIP_FILE} not found. Run build_netlify_app.py first.")
        return False

    with open(ZIP_FILE, 'rb') as f:
        zip_bytes = f.read()

    print(f"[*] Deploying {ZIP_FILE} ({len(zip_bytes)} bytes) to Netlify API...")

    url = "https://api.netlify.com/api/v1/sites"
    req = urllib.request.Request(
        url,
        data=zip_bytes,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/zip',
            'User-Agent': 'VEYRO-Deployer/1.0'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            site_url = data.get('ssl_url') or data.get('url')
            admin_url = data.get('admin_url')
            print("\n=======================================================")
            print("  🚀 DEPLOYMENT SUCCESSFUL!")
            print("=======================================================")
            print(f"  Live Website URL : {site_url}")
            print(f"  Netlify Dashboard: {admin_url}")
            print("=======================================================")
            if site_url:
                webbrowser.open(site_url)
            return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8', errors='replace')
        print(f"[!] Netlify API Error ({e.code}): {err_msg}")
        return False
    except Exception as e:
        print(f"[!] Deploy failed: {e}")
        return False

def launch_drop_helper():
    print("\n=======================================================")
    print("  🌐 10-SECOND NETLIFY DROP DEPLOYMENT")
    print("=======================================================")
    print(f"1. Opening Netlify Drop in your web browser: https://app.netlify.com/drop")
    print(f"2. Your deploy bundle is ready at: {os.path.abspath(ZIP_FILE)}")
    print("3. Simply DRAG AND DROP 'netlify_deploy.zip' onto the browser window!")
    print("=======================================================\n")

    # Reveal zip file in Windows Explorer
    try:
        subprocess.run(['explorer.exe', f'/select,{os.path.abspath(ZIP_FILE)}'], check=False)
    except Exception:
        pass

    webbrowser.open("https://app.netlify.com/drop")

if __name__ == '__main__':
    args = sys.argv[1:]
    token = None

    if '--token' in args:
        idx = args.index('--token')
        if idx + 1 < len(args):
            token = args[idx + 1]

    if not token and 'NETLIFY_AUTH_TOKEN' in os.environ:
        token = os.environ['NETLIFY_AUTH_TOKEN']

    if token:
        deploy_via_api(token)
    else:
        launch_drop_helper()
