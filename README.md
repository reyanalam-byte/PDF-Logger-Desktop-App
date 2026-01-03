# PDF-Logger-Desktop-App
A lightweight Windows desktop application that automatically logs every PDF printed from the system, along with its timestamp. Designed for lab environments to maintain easy and accurate records of printed PDFs.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Features
- Automatically detects whenever a PDF is printed.
- Records the **PDF filename** and **print timestamp**.
- Saves the log in a structured **CSV or database** format for easy access.
- Runs silently in the background as a Windows desktop application.
- Minimal dependencies and lightweight footprint.

---

## Installation

### Prerequisites
- **Python 3.10+**
- Windows OS
- Optional: `pyinstaller` for converting Python script to `.exe`

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/pdf-logger-app.git
    cd pdf-logger-app
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the app in Python:
    ```bash
    python app.py
    ```

4. To create a Windows executable (`.exe`):
    ```bash
    pyinstaller --onefile app.py
    ```
   After this, you can run the `app.exe` from your desktop.

---

## Usage
1. Launch the application (`python app.py` or `app.exe`).
2. The app runs in the background and monitors printed PDFs.
3. Every time a PDF is printed, a log entry is created in `logs.csv`:
    ```
    Filename, Print Timestamp
    example.pdf, 2026-01-03 14:25:10
    ```
4. Open the CSV file anytime to see the history of printed PDFs.

---

## How It Works
- The app hooks into Windows print events.
- It specifically listens for **PDF print jobs**.
- When a PDF is printed, the app captures:
  - The filename
  - The date and time of printing
- The captured information is stored in a log file for record-keeping.

---

## Technologies Used
- **Python** – Core programming language  
- **watchdog / pywin32** – For monitoring file system and print events  
- **CSV module** – For logging data  
- **PyInstaller** – To create a standalone executable  

---

## Future Improvements
- Add a **GUI dashboard** to view logs directly.  
- Send **email notifications** whenever a PDF is printed.  
- Maintain logs in a **SQLite database** for advanced search/filtering.  
- Include **user authentication** for secure lab environments.

---

## Author
**Reyan Alam**  
- GitHub: [reyanalam-byte](https://github.com/reyanalam-byte)  
- Email: 2421349.cse.cec@cgc.edu.in
