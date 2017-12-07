import urllib, json
import csv
import sys, os, errno
import os.path
import io
import datetime
from time import gmtime, strftime
import time
import pickle
import glob
from Tkinter import Tk
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
import shutil

def get_dir():
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    cwd = os.getcwd()
    return cwd

def choose_file():
    print "Choose a specific file (file name end with .csv), or press [Cancel] to iterative every file found in this directory"
    # IterativeFiles = raw_input('Choose a specific file (file name end with .csv), or press [ENTER] to iterative every file found in this directory')
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    # direct = askdirectory()
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    if filename != "":
        # print("File chosen: ", filename)
        pass
    else:
        print "Choose every file in the directory"
    return filename

def convert_unix_time(element):
    # print element
    if element == 'None':
        return element
    else:
        return datetime.datetime.fromtimestamp(int(element)/1000).strftime('%Y-%m-%d %H:%M:%S')

def process_header(file,output_file):
    with open(file, 'rb') as f:
        csvreader = csv.reader(f)
        header = next(csvreader) #obtain header in the csv file
        # print header
        new_header = []
        for attr in header:
            new_attr = attr[9:]
            if new_attr[0:8] == 'geometry':
                new_attr = new_attr[9:]
                if new_attr == 'coordinates_0':
                    new_attr = 'latitude'
                elif new_attr == 'coordinates_1':
                    new_attr = 'longitude'
            if new_attr[0:10] == 'properties':
                new_attr = new_attr[11:]
                if new_attr == 'adviceA':
                    new_attr = 'advice_for_motorists_1'
                elif new_attr == 'adviceB':
                    new_attr = 'advice_for_motorists_2'
                if new_attr == 'created':
                    new_attr = 'system_record_created_at'
                elif new_attr == 'ended':
                    new_attr = 'is_resolved/ended'
                if new_attr == 'displayName':
                    new_attr = 'description_headline'
                if new_attr == 'end':
                    new_attr = 'scheduled_end_time'
                if new_attr == 'start':
                    new_attr = 'scheduled_start_time'
                if new_attr == 'headline':
                    new_attr = 'description_summary'
                if new_attr == 'isInitialReport':
                    new_attr = 'is_unverified_report'
                if new_attr == 'otherAdvice':
                    new_attr = 'advice_for_motorists'
                if new_attr == 'publicTransport':
                    new_attr = 'PT_impact'
                if new_attr == 'lastUpdated':
                    new_attr = 'last_updated_at'
                if new_attr[:5] == 'roads':
                    new_attr = 'roads_affected' + new_attr[5:]
                if new_attr == 'impactingNetwork':
                    new_attr = 'is_impacting_network'
                if new_attr[:7] == 'periods':
                    new_attr = 'scheduled_period' + new_attr[7:]
                if new_attr[:22] == 'arrangementAttachments':
                    new_attr = 'detail_document' + new_attr[22:]
                if new_attr[:22] == 'arrangementElements':
                    new_attr = 'detail_info' + new_attr[22:]
            new_header.append(new_attr)

        delete_list = ['type','expectedDelay','name','subCategoryA','subCategoryB']
        marked_column = [i for i,x in enumerate(new_header) if (x in delete_list) or (x[:5] =='media') or (x[:7]=='webLink')]    
        marked_column.sort(reverse=True)

        time_elements = ['system_record_created_at','last_updated_at','scheduled_start_time','scheduled_end_time']
        timestamp_column = [i for i,x in enumerate(new_header) if (x in time_elements)]    

        
        with open(output_file,"wb") as result:
            wtr= csv.writer(result)
            for column in marked_column:
                del new_header[column]
            wtr.writerow(new_header)
            for row in csvreader:
                # wtr.writerow( (r[0], r[1], r[3], r[4]) )
                for column in timestamp_column:
                    row[column] = convert_unix_time(row[column])
                for column in marked_column:
                    del row[column]
                wtr.writerow(row)


# def process_column(file,output_file):
#     with open(file, 'rb') as f:
#         rdr= csv.reader(f)
        

def main(isAuto,fileList):
    Dropbox_dir = "C:\Users\LIU136\Dropbox\David Liu Internship\LiveTrafficData\\"
    upload_file_name = ""
    filePath = get_dir()
    fileName = []
    if isAuto is False:
        print "csv Files within the directory:"; print(glob.glob(filePath + "/*.csv")); print "\n"
        UserChoice = choose_file()

        if UserChoice == '':
            os.chdir(filePath)
            for ff in glob.glob("*.csv"):
                if ff[-13:] != 'processed.csv':
                    fileName.append(filePath +  "\\" + ff)
                    print "File added: ", filePath +  "\\" + ff
                else:
                    print "File skipped: ", filePath +  "\\" + ff
        else:
            fileName.append(UserChoice)
            print "File added: ", UserChoice

    else:
        print 'Auto process, skip GUI'
        print 'Files to be processed this time: ', fileList
        fileName = fileList
    
    # fileName contains every file directory to be processed
    for f in fileName:
        f_out = f[:-4]
        f_out = f_out + '_processed.csv'
        process_header(f,f_out)
        # process_column(f,1)
        if "Incident" in f_out:
            upload_file_name = "Incident_processed.csv"
        elif "MajorEvent" in f_out:
            upload_file_name = "MajorEvent_processed.csv"
        elif "Roadwork" in f_out:
            upload_file_name = "Roadwork_processed.csv"
        upload_file_name = Dropbox_dir + upload_file_name
        shutil.copyfile(f_out,upload_file_name)

    
    if isAuto is False:
        print("Processed complete, press any key to exit")
        input()
    else:
        print("Processed complete, _process files generated")
    

if __name__ == "__main__":
    main(False,[])