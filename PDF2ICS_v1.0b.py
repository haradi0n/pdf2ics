#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Appending version
## Adds every week's ICS event to the existing ICS file

import pdfplumber
import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import os

def find_rows_in_pdf(pdf_path, search_term):
    results = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)  # Convert table to DataFrame
                for index, row in df.iterrows():
                    if any(search_term in str(cell) for cell in row):
                        results.append(row.tolist())
    
    return results

def get_dates_from_first_row(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        tables = first_page.extract_tables()
        
        # Assume the first table is the one we need
        table = tables[0]
        date_row = table[0][2:9]  # Columns 3 to 9 of the first row

        # Parse dates from dd.mm.yy format
        dates = []
        for date_str in date_row:
            try:
                date = datetime.strptime(date_str, "%d.%m.%y")
                dates.append(date)
            except ValueError:
                # If not a valid date format, append None
                dates.append(None)

        return dates

def parse_work_hours(row, dates):
    work_schedule = []
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    vienna_tz = pytz.timezone("Europe/Vienna")
    
    for i, day in enumerate(row[2:]):
        if "-" in day and dates[i] is not None:
            parts = day.split()
            time_range = parts[0]
            start_time, end_time = time_range.split("-")
            start_dt = datetime.strptime(start_time, "%H:%M").replace(tzinfo=vienna_tz, year=dates[i].year, month=dates[i].month, day=dates[i].day)
            end_dt = datetime.strptime(end_time, "%H:%M").replace(tzinfo=vienna_tz, year=dates[i].year, month=dates[i].month, day=dates[i].day)
            work_schedule.append((week_days[i], start_dt, end_dt))
    
    return work_schedule

def read_existing_ics_file(ics_file_path):
    if os.path.exists(ics_file_path):
        with open(ics_file_path, 'rb') as f:
            cal = Calendar.from_ical(f.read())
        return cal
    else:
        return Calendar()

def create_ics_file(events, ics_file_path="work_schedule.ics"):
    cal = read_existing_ics_file(ics_file_path)
    for day, start_time, end_time in events:
        event = Event()
        event.add("summary", "Dienst")
        event.add("dtstart", start_time)
        event.add("dtend", end_time)
        cal.add_component(event)
    
    with open(ics_file_path, "wb") as f:
        f.write(cal.to_ical())
    print(f"ICS file updated at {ics_file_path}")

if __name__ == "__main__":
    pdf_path = input("Enter the path to the PDF: ")
    search_term = input("Enter the content to search for: ")
    
    found_rows = find_rows_in_pdf(pdf_path, search_term)
    dates = get_dates_from_first_row(pdf_path)
    
    if found_rows:
        for row in found_rows:
            work_schedule = parse_work_hours(row, dates)
            create_ics_file(work_schedule)
    else:
        print("No matching content found.")

