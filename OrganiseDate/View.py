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
import DatePicker

def read_dict(target_dir):
    with open(target_dir, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        global main_dict
        target_dir = dict(reader)
    return target_dir

def choose():
    return date(2017,1,1)

def read_csv(fileName,target_date):
    with open(fileName, 'rb') as f:
        csvreader = csv.reader(f)
        header = next(csvreader) #obtain header in the csv file
        for row in csvreader:
            
def main():
    # define directories
    FileDir = "C:\Users\LIU136\Dropbox\David Liu Internship\\"
    FileDir_weather = FileDir + "WeatherData\Weather_2016_2017_v1.xlsx"
    FileDir_holiday = FileDir + "HolidayData\Public_holiday.xlsx"
    FileDir_schoolEvent = FileDir + "SchoolData\School_events.xlsx"
    FileDir_Incident = FileDir + "LiveTrafficData\Incident_processed.csv"
    FileDir_Roadwork = FileDir + "LiveTrafficData\Roadwork_processed.csv"
    FileDir_MajorEvent = FileDir + "LiveTrafficData\MajorEvent_processed.csv"
    FileDir_Dict = FileDir + "byDate\index.csv"

    main_dict = read_dict(FileDir_Dict)

    chosen_date = choose()
    # DatePicker.main()

    read_csv(FileDir_Incident,chosen_date)
    read_csv(FileDir_Roadwork,chosen_date)
    read_csv(FileDir_MajorEvent,chosen_date)
    read_xlsx(FileDir_holiday,chosen_date)
    read_xlsx(FileDir_schoolEvent,chosen_date)

    
    # print main_dict
    
if __name__ == "__main__":
    main()