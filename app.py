import os
import sqlite3
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook

# ---------------- CONFIG ----------------
WATCH_FOLDER = r"C:\Lab_Print_Records\Printed_PDFs"
DB_FILE = "database.db"

os.makedirs(WATCH_FOLDER, exist_ok=True)
observer = None

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS print_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        printed_at TEXT
    )
    """)
    conn.commit()
    conn.close()

# ---------------- FILE HANDLER ----------------
class PrintHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(".pdf"):
            file_name = os.path.basename(event.src_path)
            printed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO print_logs (file_name, printed_at) VALUES (?, ?)",
                (file_name, printed_at)
            )
            conn.commit()
            conn.close()

# ---------------- FUNCTIONS ----------------
def start_monitoring():
    global observer
    if observer:
        return

    event_handler = PrintHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    status_label.config(text="● Monitoring Active", fg="#1b7f3b")

def stop_monitoring():
    global observer
    if observer:
        observer.stop()
        observer.join()
        observer = None

    status_label.config(text="● Monitoring Stopped", fg="#a83232")

def view_logs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, printed_at FROM print_logs ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()

    win = tk.Toplevel(root)
    win.title("Print Records")
    win.geometry("520x320")
    win.configure(bg="#f5f7fa")

    text = tk.Text(win, font=("Segoe UI", 10))
    text.pack(expand=True, fill="both", padx=10, pady=10)

    for file, date in records:
        text.insert("end", f"{file}    |    {date}\n")

def export_to_excel():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, printed_at FROM print_logs")
    records = cursor.fetchall()
    conn.close()

    if not records:
        messagebox.showinfo("No Data", "No records available to export.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Lab Print Logs"
    ws.append(["File Name", "Understanding printed_at"])

    for row in records:
        ws.append(row)

    filename = f"Lab_Print_Logs_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    wb.save(filename)

    messagebox.showinfo("Export Complete", f"Excel file saved:\n{filename}")

# ---------------- GUI ----------------
init_db()

root = tk.Tk()
root.title("Laboratory Print Monitor")
root.geometry("440x360")
root.resizable(False, False)
root.configure(bg="#f5f7fa")

# ===== CANVAS WATERMARK (FIXED) =====
canvas = tk.Canvas(root, width=440, height=360, bg="#f5f7fa", highlightthickness=0)
canvas.place(x=0, y=0)

canvas.create_text(
    220, 220,
    text="DEVELOPED BY\nREYAN AL",
    fill="#c4c8ce",
    font=("Segoe UI", 26, "bold"),
    justify="center"
)

# ===== FOREGROUND FRAME =====
content = tk.Frame(root, bg="#f5f7fa")
content.place(relwidth=1, relheight=1)

tk.Label(
    content,
    text="Laboratory Print Monitor",
    font=("Segoe UI", 16, "bold"),
    bg="#f5f7fa",
    fg="#2b2b2b"
).pack(pady=15)

status_label = tk.Label(
    content,
    text="● Monitoring Stopped",
    font=("Segoe UI", 11, "bold"),
    fg="#a83232",
    bg="#f5f7fa"
)
status_label.pack(pady=8)

btn_frame = tk.Frame(content, bg="#f5f7fa")
btn_frame.pack(pady=10)

def styled_button(text, command):
    return tk.Button(
        btn_frame,
        text=text,
        command=command,
        font=("Segoe UI", 11),
        width=30,
        bg="#1976d2",
        fg="white",
        activebackground="#125ea6",
        activeforeground="white",
        relief="flat",
        pady=6
    )

styled_button("Start Monitoring", start_monitoring).pack(pady=4)
styled_button("Stop Monitoring", stop_monitoring).pack(pady=4)
styled_button("View Records", view_logs).pack(pady=4)
styled_button("Export to Excel", export_to_excel).pack(pady=4)

tk.Label(
    content,
    text="© Developed by Reyan Al",
    font=("Segoe UI", 9, "italic"),
    bg="#f5f7fa",
    fg="#666666"
).pack(side="bottom", pady=8)

root.mainloop()
