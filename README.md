# Cisco ASA/FTD Interface Traffic Analyzer

This Python script is a specialized parsing utility designed to extract, analyze, and format traffic statistics from Cisco ASA or Firepower (FTD) diagnostic logs. It specifically targets the output of the `show traffic` command to identify high-load interfaces and packet drop rates.

---

## 🔍 Overview

Cisco diagnostic files often contain periodic snapshots of interface traffic. Manually comparing these metrics across dozens of interfaces is difficult. This script automates the process by:

1. **Extracting** data blocks between `------ show traffic --------` and the end-of-block markers.
2. **Parsing** specific metrics using fixed-offset indexing (every 13th line) to ensure data alignment.
3. **Ranking** interfaces by traffic volume (PPS/BPS) and drop rates to highlight the most active or problematic segments.

---

## ✨ Features

* **Multi-Metric Extraction:** Captures and isolates:
* **1-Minute Input Rate:** Packets per second (PPS) and Bytes per second (BPS).
* **5-Minute Input Rate:** PPS and BPS for long-term trend analysis.
* **5-Minute Drop Rate:** Identifies interfaces actively discarding traffic.


* **Automatic Sorting:** Generates formatted tables where interfaces are sorted by volume (highest rate first).
* **Data Cleaning:** Automatically strips Cisco-specific strings like `pkts/sec` and `bytes/sec` to perform mathematical sorting and clean reporting.
* **Unique Block Detection:** Prevents duplicate processing if the same traffic block appears multiple times in the source file.

---

## 🚀 Usage

1. **Run the script:**
python traffic_analyzer.py




2. **Provide the Input File:** Enter the path to your log file (e.g., `show_tech_output.txt`).
3. **Review Formatted Tables:** The script will output several tables for each identified traffic block, focusing on different metrics.

---

## 📖 Data Extraction Logic

The script uses a strict structural logic based on the standard output of the Cisco `show traffic` command:

* **Interface Names:** Located at index `0` of the repeating 13-line pattern.
* **1-Min Rates:** Located at index `7`.
* **5-Min Rates:** Located at index `10`.
* **5-Min Drop Rates:** Located at index `12`.

By jumping 13 lines at a time, the script effectively maps the vertical CLI output into organized data lists for comparison.

---

## 📋 Example Output

```text
Formatted Output for Traffic_block1:

Interface Name                1 Minute Packets Per Second
outside                                             15400
inside                                               8200
dmz                                                   150

Interface Name                5 Minute Drop Rate Packets Per Second
outside                                                12

```

---

## 🛠 Prerequisites

* **Python 3.x**
* No external libraries are required (uses standard library `os` and `sys` logic).

This script is an excellent addition to a network engineer's toolkit, particularly when investigating **oversubscribed interfaces** or **DDoS conditions** on Cisco security appliances.
