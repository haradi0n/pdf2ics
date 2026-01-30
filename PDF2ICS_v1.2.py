#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os


def find_rows_in_pdf(pdf_path, search_term):
    import pdfplumber
    import pandas as pd

    results = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)
                for _, row in df.iterrows():
                    if any(search_term in str(cell) for cell in row):
                        results.append(row.tolist())
    return results


def get_dates_from_first_row(pdf_path):
    import pdfplumber

    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        tables = first_page.extract_tables()
        table = tables[0]
        date_row = table[0][2:9]

        dates = []
        for date_str in date_row:
            try:
                dates.append(datetime.strptime(date_str, "%d.%m.%y"))
            except Exception:
                dates.append(None)
        return dates


def parse_work_hours(row, dates):
    import pytz
    from datetime import datetime

    work_schedule = []
    vienna_tz = pytz.timezone("Europe/Vienna")

    for i, day in enumerate(row[2:]):
        if "-" in day and dates[i] is not None:
            time_range = day.split()[0]
            start_time, end_time = time_range.split("-")

            start_dt = datetime.strptime(start_time, "%H:%M").replace(
                year=dates[i].year,
                month=dates[i].month,
                day=dates[i].day,
                tzinfo=vienna_tz,
            )
            end_dt = datetime.strptime(end_time, "%H:%M").replace(
                year=dates[i].year,
                month=dates[i].month,
                day=dates[i].day,
                tzinfo=vienna_tz,
            )

            work_schedule.append((start_dt, end_dt))

    return work_schedule


def create_ics_file(events, output_filename, overwrite):
    from icalendar import Calendar, Event

    cal = Calendar()

    if not overwrite and os.path.exists(output_filename):
        with open(output_filename, "rb") as f:
            cal = Calendar.from_ical(f.read())

    for start_time, end_time in events:
        event = Event()
        event.add("summary", "Dienst")
        event.add("dtstart", start_time)
        event.add("dtend", end_time)
        cal.add_component(event)

    with open(output_filename, "wb") as f:
        f.write(cal.to_ical())

    messagebox.showinfo("Erfolg", f"ICS Datei gespeichert:\n{output_filename}")


def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf_entry.delete(0, tk.END)
    pdf_entry.insert(0, file_path)


def select_output():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".ics",
        filetypes=[("ICS Files", "*.ics")]
    )
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)


def process_pdf():
    pdf_path = pdf_entry.get()
    search_term = search_entry.get()
    output_filename = output_entry.get()
    overwrite = overwrite_var.get()

    if not pdf_path or not search_term or not output_filename:
        messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen.")
        return

    found_rows = find_rows_in_pdf(pdf_path, search_term)
    dates = get_dates_from_first_row(pdf_path)

    if not found_rows:
        messagebox.showinfo("Keine Ergebnisse", "Kein passender Inhalt gefunden.")
        return

    for row in found_rows:
        work_schedule = parse_work_hours(row, dates)
        create_ics_file(work_schedule, output_filename, overwrite)


# --- UI ---

root = tk.Tk()
root.title("PDF zu ICS Konverter")

frame = tk.Frame(root, padx=5, pady=5)
frame.pack(padx=5, pady=5)

tk.Label(frame, text="PDF Datei:").grid(row=0, column=0, sticky="w")
pdf_entry = tk.Entry(frame, width=50)
pdf_entry.grid(row=0, column=1, padx=5)
tk.Button(frame, text="Durchsuchen", command=select_pdf).grid(row=0, column=2)

tk.Label(frame, text="Nachname, Vorname:").grid(row=1, column=0, sticky="w")
search_entry = tk.Entry(frame, width=50)
search_entry.grid(row=1, column=1, padx=5)

tk.Label(frame, text="Speicherort:").grid(row=2, column=0, sticky="w")
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=2, column=1, padx=5)
tk.Button(frame, text="Speichern unter", command=select_output).grid(row=2, column=2)

overwrite_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Daten überschreiben", variable=overwrite_var).grid(row=3, column=1)

tk.Button(frame, text="Verarbeiten", command=process_pdf).grid(row=4, column=1, pady=10)

root.mainloop()


# In[ ]:




