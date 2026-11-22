# -*- coding: utf-8 -*-
import subprocess, os

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_dir = r"C:\Users\DIVAKAR\Downloads\memsproject\MEMS-INDUSTRIAL-MONITORING\project-documentation\screenshots"

for page, name in [
    ("live", "figure_6_2_live_monitoring.png"),
    ("faults", "figure_6_3_fault_detection.png"),
    ("energy", "figure_6_4_energy_monitoring.png"),
    ("history", "figure_6_5_history.png")
]:
    target = os.path.join(out_dir, name)
    url = f"http://localhost:5173/{page}"
    cmd = [
        CHROME,
        "--headless=new",
        "--window-size=1920,1080",
        "--hide-scrollbars",
        "--virtual-time-budget=1500",
        f"--screenshot={target}",
        url
    ]
    print(f"Running {name}...")
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=12)
        print(f"  Returncode: {res.returncode}, File exists: {os.path.exists(target)}")
        if os.path.exists(target):
            print(f"  Size: {os.path.getsize(target)} bytes")
    except Exception as e:
        print(f"  Error: {e}")
