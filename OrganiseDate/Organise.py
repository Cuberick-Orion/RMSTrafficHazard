import urllib, json
import csv
import sys, os, errno
import os.path
import io
import datetime
from datetime import date, datetime, timedelta
from time import gmtime, strftime
import time
import pickle
import glob
from Tkinter import Tk
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
import shutil
# please pip install the following packages, they are not included in the default Python
from xlrd import open_workbook
import pandas

def perdelta(start, end, delta): #generate list of dates between start and end
    curr = start
    while curr < end:
        yield curr
        curr += delta

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def generate_date():
    target_dict = {}
    for target_date in perdelta(date(2016, 1, 1), date(2018, 12, 31)+timedelta(days=1), timedelta(days=1)):
        target_dict [target_date] = [] 
        #empty list reserved for id strings, key is in the type of datetime.date
    return target_dict

def add_to_dict(id,start_date,end_date):
    for d in daterange(start_date,end_date):
        if d <= date(2018, 12, 31) and d >= date(2016,1,1):
            global main_dict
            main_dict[d].append(id)
        else:
            pass

def process_csv(fileName):
    attrName_scheduleStart = "scheduled_start_time"
    attrName_scheduleEnd = "scheduled_end_time"
    attrName_start = "system_record_created_at"
    attrName_isResolved = "is_resolved/ended"
    attrName_end = "last_updated_at"

    with open(fileName, 'rb') as f:
        csvreader = csv.reader(f)
        header = next(csvreader) #obtain header in the csv file
        ListPosition_scheduleStart = header.index(attrName_scheduleStart)
        ListPosition_scheduleEnd = header.index(attrName_scheduleEnd)
        ListPosition_start = header.index(attrName_start)
        ListPosition_isResolved = header.index(attrName_isResolved)
        ListPosition_end = header.index(attrName_end)
        # print ListPosition_scheduleStart
        for row in csvreader:
            current_id = str(row[2])
            current_type = None
            if row[ListPosition_scheduleStart] != "None": #sheduled events
                current_type = "Planned"
                current_start = str(row[ListPosition_scheduleStart])
                current_end = str(row[ListPosition_scheduleEnd])
                current_status = True
            else: #unscheduled events
                current_type = "Unplanned"
                current_start = str(row[ListPosition_start])
                current_end = str(row[ListPosition_end])
                current_status = (row[ListPosition_isResolved] == 'True') #is resolved or not

            current_start_d = datetime.strptime(current_start[:10],'%Y-%m-%d').date()
            current_end_d = datetime.strptime(current_end[:10],'%Y-%m-%d').date()

            add_to_dict(current_id,current_start_d,current_end_d + timedelta(days=1)) #add a day for inclusive
    return 0

def process_xlsx(fileName):
    xlsxreader = pandas.ExcelFile(fileName)
    df = xlsxreader.parse('Sheet1')
    for index, row in df.iterrows():
        # print row
        current_id = str(row['id'])
        current_start = row['start_date'].date()
        current_end = row['end_date'].date()
        add_to_dict(current_id,current_start,current_end + timedelta(days=1)) #add to dictionary

def write_to_file(target_dict,output_dir):
    with open(output_dir, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in target_dict.items():
           writer.writerow([key, value])

def write_to_pickle(target_dict,output_dir):
        with open(output_dir,'wb') as f:
            pickle.dump(target_dict,f)

def main():
    # define directories
    FileDir = "C:\Users\LIU136\Dropbox\David Liu Internship\\"
    # FileDir = "E:\Dropbox\David Liu Internship\\"


    FileDir_weather = FileDir + "WeatherData\Weather_2016_2017_v1.xlsx"
    FileDir_holiday = FileDir + "HolidayData\Public_holiday.xlsx"
    FileDir_schoolEvent = FileDir + "SchoolData\School_events.xlsx"
    FileDir_Incident = FileDir + "LiveTrafficData\Incident_processed.csv"
    FileDir_Roadwork = FileDir + "LiveTrafficData\Roadwork_processed.csv"
    FileDir_MajorEvent = FileDir + "LiveTrafficData\MajorEvent_processed.csv"
    FileDir_Output = FileDir + "byDate\index.csv"
    FileDir_Pickle_Output = FileDir + "byDate\index.pickle"
    # generate dictionary for all the dates
    global main_dict
    main_dict = generate_date()
    # print main_dict
    process_csv(FileDir_Incident)
    process_csv(FileDir_Roadwork)
    process_csv(FileDir_MajorEvent)
    process_xlsx(FileDir_holiday)
    process_xlsx(FileDir_schoolEvent)

    write_to_file(main_dict,FileDir_Output)
    write_to_pickle(main_dict,FileDir_Pickle_Output)
    # print main_dict
    print 'All done.'
    
if __name__ == "__main__":
    main()