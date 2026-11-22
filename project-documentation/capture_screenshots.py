# -*- coding: utf-8 -*-
"""
capture_screenshots.py - Captures high-resolution screenshots of the 5 monitoring pages
"""

import os
import subprocess
import time

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_URL = "http://localhost:5173"
OUTPUT_DIR = os.path.abspath(r"MEMS-INDUSTRIAL-MONITORING\project-documentation\screenshots")

PAGES = [
    {
        "filename": "figure_6_1_dashboard.png",
        "url": f"{BASE_URL}/",
    },
    {
        "filename": "figure_6_2_live_monitoring.png",
        "url": f"{BASE_URL}/live",
    },
    {
        "filename": "figure_6_3_fault_detection.png",
        "url": f"{BASE_URL}/faults",
    },
    {
        "filename": "figure_6_4_energy_monitoring.png",
        "url": f"{BASE_URL}/energy",
    },
    {
        "filename": "figure_6_5_history.png",
        "url": f"{BASE_URL}/history",
    }
]

def capture_page(url, out_file):
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--window-size=1920,1080",
        "--hide-scrollbars",
        "--disable-gpu",
        f"--screenshot={out_file}",
        url
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            proc.wait(timeout=6)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
    except Exception as e:
        print(f"Error running Chrome for {url}: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for p in PAGES:
        out_file = os.path.join(OUTPUT_DIR, p["filename"])
        print(f"Capturing {p['url']} -> {p['filename']}...")
        capture_page(p["url"], out_file)
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            print(f"  [OK] Saved {p['filename']} ({os.path.getsize(out_file)} bytes)")
        else:
            print(f"  [FAIL] {p['filename']} missing or empty")

if __name__ == "__main__":
    main()
