# Automated Disk Sanitizer — Python Automation Project

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Type](https://img.shields.io/badge/Type-Automation%20Script-red)
![Feature](https://img.shields.io/badge/Feature-Duplicate%20File%20Cleaner-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

An automated duplicate file detection and deletion system built in Python. The script scans a given directory, identifies duplicate files using MD5 checksum comparison, deletes the extra copies, generates a detailed log file for every run, and repeats the process automatically on a daily schedule.

---

## Problem Statement

Over time, directories accumulate duplicate files — same content saved under different names or in different subfolders. Manually finding and deleting these wastes storage and time. This project automates the entire process by comparing file content using MD5 checksums and cleaning up duplicates automatically every day.

---

## Project Structure

```
Automated_Disk_Sanitizer/
│
├── AutomatedDiskSanitiser.py     # Main script — scan, detect, delete, and log
│
├── Demo/                         # Sample source folder containing test files
│   ├── a.txt
│   ├── c.txt
│   ├── d.txt
│   └── k.txt
│
├── LogFile/                      # Auto-created folder storing all log files
│   ├── LogFile2026-02-11_13-57-48.log
│   └── LogFile2026-02-11_14-11-28.log
│
└── README.md
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| MD5 Checksum Comparison | Detects duplicates based on actual file content, not just file names |
| Recursive Directory Scan | Scans the target folder and all its subfolders automatically |
| Safe Deletion | Keeps the first (original) copy of each file and deletes only the duplicates |
| Automated Log File | Creates a timestamped log file after every run recording what was deleted |
| Daily Scheduled Execution | Runs automatically once every day using the `schedule` library |
| Auto Log Folder Creation | Creates the `LogFile` folder automatically if it does not exist |

---

## Functions Overview

| Function | Description |
|----------|-------------|
| `CalculateChecksum` | Calculates the MD5 hash of a file to uniquely identify its content |
| `FindDuplicate` | Scans a directory and groups files by their checksum to find duplicates |
| `DisplayResult` | Prints all duplicate file groups found during the scan |
| `DeleteDuplicate` | Deletes all duplicate copies, keeping only the first (original) file |
| `CreateLog` | Runs the cleanup and writes a full log report to the `LogFile` folder |
| `main` | Entry point — reads directory name from CLI and starts the daily scheduler |

---

## How It Works — Step by Step

**Step 1 — Scan the Directory**
The script walks through every file in the target directory and all its subfolders using `os.walk`.

**Step 2 — Calculate MD5 Checksum**
For each file, an MD5 hash is calculated by reading the file in 1KB chunks. This hash is a unique fingerprint of the file's content.

**Step 3 — Detect Duplicates**
Files are grouped by their checksum in a dictionary. Any group with more than one file contains duplicates.

**Step 4 — Delete Duplicates**
For each duplicate group, the first file is kept as the original. All remaining copies are permanently deleted using `os.remove()`.

**Step 5 — Write Log File**
A log file is created inside the `LogFile/` folder recording the run timestamp, total number of files deleted, and the names of all deleted files.

**Step 6 — Repeat Daily**
All of the above runs automatically once every day so the directory stays clean without any manual effort.

---

## Log File Format

Each log file created inside `LogFile/` follows this format:

```
------------------------------------------------------------
--------------------   Disk Sanitizer System ---------------
Log created at : Tue Feb 11 14:11:28 2026
------------------------------------------------------------

---------------------- System Report -----------------------
No of files deleted : 2
Name of deleted files : ['Demo\\c.txt', 'Demo\\d.txt']
------------------------------------------------------------
---------------------- End of log file ---------------------
------------------------------------------------------------
```

---

## Command Line Usage

```bash
# Run the sanitizer on the 'Demo' folder (schedules daily cleanup)
python AutomatedDiskSanitiser.py Demo
```

The script will keep running in the background and trigger the cleanup once every day. Press `Ctrl + C` to stop.

---

## Tech Stack

- Python 3
- `hashlib` — MD5 checksum calculation for detecting duplicate file content
- `os` — directory scanning, file path operations, and file deletion
- `schedule` — scheduling the cleanup to run automatically every day
- `time` — timestamps for log file names and log entries
- `sys` — reading command-line arguments

---

## How to Run

1. Clone this repository
2. Install the required library:
   ```bash
   pip install schedule
   ```
3. Run the script with the target directory name:
   ```bash
   python AutomatedDiskSanitiser.py Demo
   ```

---

## Key Concepts Covered

- File Hashing using MD5 Checksum (`hashlib`)
- Duplicate File Detection using Dictionary Grouping
- Recursive Directory Scanning (`os.walk`)
- Safe File Deletion (`os.remove`)
- Automated Log File Generation
- Daily Task Scheduling (`schedule` library)
- Command Line Argument Handling (`sys.argv`)



---

## Author

**Raviraj Aade**

Built as a Python Automation Project to understand file hashing, duplicate detection, automated cleanup, log generation, and scheduled task execution using pure Python.
