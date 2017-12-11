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
# import DatePicker
import numpy as np
# please install pip install git+https://github.com/bluenote10/PandasDataFrameGUI
# please install pip install -U wxPython
# please install pip install matplotlib
import dfgui


def read_dict(target_dir):
    # with open(target_dir, 'rb') as csv_file:
    #     reader = csv.reader(csv_file)
    #     global main_dict
    #     main_dict = dict(reader)
    # return_dict = {}
    # for key in main_dict: #change dict keys into type datetime.date
    #     key_d = datetime.strptime(key,'%Y-%m-%d').date()
    #     return_dict[key_d] = main_dict[key]
    with open(target_dir,'rb') as f:
        return_dict = pickle.load(f)
    return return_dict

def choose():
    # picked_date = raw_input("select a date in dd/mm/yy: \n")
    # return datetime.strptime(picked_date,'%d/%m/%y').date()
    return date(2017,1,1)

def sort_events(input_list):
    output_LT = []
    output_SC = []
    output_PH = []
    for event in input_list:
        if event[:2] == 'SC':
            output_SC.append(event)
        elif event[:2] == 'PH':
            output_PH.append(event)
        else:
            output_LT.append(event)
    return output_LT, output_PH, output_SC

# def row_process(target_row):
#     header = final_list[0]
#     # print header
#     # print target_row
#     new_row = [''] * len(header)
#     if str(target_row['id'])[:2] == 'PH': #holiday event
#         new_row[header.index('id')] = str(target_row['id'])
#         new_row[header.index('description_summary')] = str(target_row['holiday_name'])
#         new_row[header.index('description_headline')] = str(target_row['holiday_name'])
#         new_row[header.index('scheduled_start_time')] = str(target_row['start_date'])
#         new_row[header.index('scheduled_end_time')] = str(target_row['end_date'])
#         new_row[header.index('mainCategory')] = str(target_row['area'])
#         new_row[header.index('additionalInfo_0')] = str(target_row['details'])
#         new_row[header.index('isMajor')] = True
#         # print new_row
#     elif str(target_row['id'])[:2] == 'SC':
#         new_row[header.index('id')] = str(target_row['id'])
#         new_row[header.index('description_summary')] = str(target_row['name'])
#         new_row[header.index('description_headline')] = str(target_row['type'])
#         new_row[header.index('scheduled_start_time')] = str(target_row['start_date'])
#         new_row[header.index('scheduled_end_time')] = str(target_row['end_date'])
#         new_row[header.index('mainCategory')] = str(target_row['School_type'])
#         new_row[header.index('incidentKind')] = str(target_row['school_subtype'])
#         new_row[header.index('additionalInfo_0')] = str(target_row['data_source'])
#         # new_row[header.index('isMajor')] = True
#         # print new_row
#     else:
#         print e
#     return new_row

def read_csv(fileName,input_list):
    list_temp = []
    df = pandas.read_csv(fileName)
    # header = create_header(fileName)
    for index, row in df.iterrows():
        row_id =  str(row['id'])
        if row_id in input_list:
            list_temp.append(row.to_dict())

            # print row
            # print
    return list_temp

def read_xlsx(fileName,input_list):
    list_temp = []
    xlsxreader = pandas.ExcelFile(fileName)
    df = xlsxreader.parse('Sheet1')
    # header = 
    for index, row in df.iterrows():
        current_id = str(row['id'])
        if current_id in input_list:
            list_temp.append(row.to_dict())
            # row_p = row_process(row)
            # print row
            # print
    return list_temp

# def reorganise(input_list):
#     content_list = []
#     column_labels = input_list.pop(0)
#     for row in input_list:
#         content_list.append(tuple(row))
    
#     print column_labels
#     print content_list
#     df = pandas.DataFrame.from_records(content_list, columns=column_labels)
#     return df

def pretty_print(input_list):
    output_df = pandas.DataFrame(index = ['id', 'name', 'type', 'subtype', 'start_date','end_date'])
    for event in input_list:
        event_pd = pandas.Series(event)
        # print event_pd
        if str(event_pd['id'])[:2] == 'PH':
            event_f = event_pd[['id','holiday_name','holidy_type','area','start_date','end_date']]
            event_f.rename({'holiday_name': 'name', 'holidy_type': 'type', 'area': 'subtype'}, inplace=True)
            event_f.name = event_pd['id']
            # print event_f
            # print '>>>>>'
        elif str(event_pd['id'])[:2] == 'SC':
            event_f = event_pd[['id','name','School_type','school_subtype','start_date','end_date']]
            event_f.rename({'School_type': 'type', 'school_subtype': 'subtype'}, inplace=True)
            event_f.name = event_pd['id']
            # print event_f
            # print '>>>>>'
        elif str(event_pd['incidentKind']) == 'Unplanned':
            event_f = event_pd[['id','description_summary','mainCategory','incidentKind','system_record_created_at','last_updated_at']]
            event_f.rename({'description_summary': 'name', 'mainCategory': 'type', 'incidentKind': 'subtype', 'system_record_created_at': 'start_date', 'last_updated_at': 'end_date'}, inplace=True)
            event_f.name = event_pd['id']
            # print event_f
            # print '>>>>>'
        elif str(event_pd['incidentKind']) == 'Planned':
            event_f = event_pd[['id','description_summary','mainCategory','incidentKind','scheduled_start_time','scheduled_end_time']]
            event_f.rename({'description_summary': 'name', 'mainCategory': 'type', 'incidentKind': 'subtype', 'scheduled_start_time': 'start_date', 'scheduled_end_time': 'end_date'}, inplace=True)
            event_f.name = event_pd['id']
            # print event_f
            # print '>>>>>'
        # print event_f
        # output_df.append(event_f, ignore_index=True)
        # output_df.join(event_f)
        # output_df.assign(str(event_pd['id']) = event_f)
        output_df[event_f.name]=event_f.values
    # output_df = output_df.astype(str)
    print output_df
    print '>>>>>'
    # dfl = pandas.DataFrame(np.random.randn(5,2), columns=list('AB'))
    dfgui.show(dfl)

def main(chosen_date):
    
    # define directories
    # FileDir = "C:\Users\LIU136\Dropbox\David Liu Internship\\"
    FileDir = "E:\Dropbox\David Liu Internship\\"
    
    FileDir_weather = FileDir + "WeatherData\Weather_2016_2017_v1.xlsx"
    FileDir_holiday = FileDir + "HolidayData\Public_holiday.xlsx"
    FileDir_schoolEvent = FileDir + "SchoolData\School_events.xlsx"
    FileDir_Incident = FileDir + "LiveTrafficData\Incident_processed.csv"
    FileDir_Roadwork = FileDir + "LiveTrafficData\Roadwork_processed.csv"
    FileDir_MajorEvent = FileDir + "LiveTrafficData\MajorEvent_processed.csv"
    FileDir_Dict = FileDir + "byDate\index.pickle"

    main_dict = read_dict(FileDir_Dict)

    # DatePicker.main()
    # chosen_date = choose()
    target_list = main_dict[chosen_date]
    print target_list, '\n'

    list_LiveTraffic, list_PH, list_SC = sort_events(target_list)

    # global final_list
    # final_list = []
    # create_header(FileDir_Incident)

    LT_I = read_csv(FileDir_Incident,list_LiveTraffic)
    LT_R = read_csv(FileDir_Roadwork,list_LiveTraffic)
    LT_M = read_csv(FileDir_MajorEvent,list_LiveTraffic)
    PH = read_xlsx(FileDir_holiday,list_PH)
    SC = read_xlsx(FileDir_schoolEvent,list_SC)
    final_list = LT_I + LT_R + LT_M + PH + SC #final list contains event in dictionary form

    final_df = pandas.DataFrame(final_list)
    # print
    dfgui.show(final_df)
    # pretty_print(final_list)
    # print final_dataframe
    # print len(final_list)
    print "Spreadsheet closed\n"
if __name__ == "__main__":
    chosen_date = choose()
    main(chosen_date)