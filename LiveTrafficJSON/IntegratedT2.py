import urllib, json
import csv
import sys, os, errno
import os.path
import io
import os
import datetime
from time import gmtime, strftime
import time
import pickle
# import threading

# print(
#     datetime.datetime.fromtimestamp(
#         int("1284101485")
#     ).strftime('%Y-%m-%d %H:%M:%S')
# )

# from json_to_csv import JSONconvert

# create directory if non-exist
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise



#     csvwriter.writerow(feature.values())
# majorevent_write.close()


def to_string(s):
    try:
        return str(s)
    except:
        #Change the encoding type if needed
        return s.encode('utf-8')


def reduce_item(key, value):
    global reduced_item
    
    #Reduction Condition 1
    if type(value) is list:
        i=0
        for sub_item in value:
            reduce_item(key+'_'+to_string(i), sub_item)
            i=i+1

    #Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key+'_'+to_string(sub_key), value[sub_key])
    
    #Base Condition
    else:
        reduced_item[to_string(key)] = to_string(value)


def JSONconvert_Roadwork(node,json_file_path,csv_file_path):

    response = urllib.urlopen(json_file_path)
    # load JSON file
    print("[INFO] URL load complete")

    raw_data = json.loads(response.read())
    try:
        data_to_be_processed = raw_data[node]
    except:
        data_to_be_processed = raw_data

    processed_data = []
    header = []
    global reduced_item
    for item in data_to_be_processed:
        reduced_item = {}
        reduce_item(node, item)

        header += reduced_item.keys()

        processed_data.append(reduced_item)

    global current_dataset_Roadwork
    if current_dataset_Roadwork == []:
        print "[INFO] Dataset written in memory"
        current_dataset_Roadwork = processed_data
    else:
        print "[INFO] Dataset exists in memory"
        # merge processed_data with current_dataset
        for row in processed_data:
            # print type(row)
            row_id = row['features_id']
            # print row_id
            i = 0
            replaced = False
            for row_compare in current_dataset_Roadwork:
                if row_compare['features_id'] == row_id:
                    print "[UPDATE] Row updated with id: ", row_id
                    current_dataset_Roadwork[i] = row
                    replaced = True
                i += 1
            if replaced is False:
                current_dataset_Roadwork.append(row)
                print "[UPDATE] New Row Appended!"

        print "[INFO] Dataset in memory updated"
    pickle_file = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Roadwork"
    # pickle_file = "E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Roadwork"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset_Roadwork,f)
    print "[INFO] Data Cached in local file"


    header = list(set(header))
    header.sort()
    header = [e for e in header if e not in ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title')]
    header = [e for e in header if e not in ('features_properties_attendingGroups_0')]
    header = [e for e in header if e not in ('features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')]
    # print header
    removed_e = ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title','features_properties_attendingGroups_0','features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')
    
    # processed_data is the final data

    with open(csv_file_path, 'w+') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        global current_dataset_Roadwork
        for row in current_dataset_Roadwork:
            for k in removed_e:
                row.pop(k,None)
            try:
                writer.writerow(row)
            except:
                pass



    print ("[INFO] Completed writing csv file with %d columns" % len(header))

def check_Roadwork():
    url = "http://data.livetraffic.com/traffic/hazards/roadwork.json"

    response = urllib.urlopen(url)
    # load JSON file
    majorevent = json.loads(response.read())
    print("[INFO] URL checked")

    majorevent_time_mark = majorevent['lastPublished']
    print "[INFO] Received time stamp: ", majorevent_time_mark
    # majorevent_parsed = majorevent['features']

    global starttime_int
    RecordFileName = ('C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\Roadwork_update_history_%d.txt' % starttime_int) 
    # RecordFileName = ('E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\Roadwork_update_history_%d.txt' % starttime_int) 
    with open(RecordFileName,'a+') as majorevent_record:

        try:
            latest_time_mark = majorevent_record.readlines()[-1]
            print"[INFO] Currently recorded time stamp: ", latest_time_mark
        except:
            latest_time_mark = str(0000000000000)
            print"[INFO] No existing time stamp recorded"

        if int(majorevent_time_mark) > int(latest_time_mark[:13]):
            print "[INFO] New Data Arrived"
            majorevent_record.write( str(majorevent_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '  NEW' +'\n')

            # open a file for writing, default in C:
            mkdir_p('C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData')
            # mkdir_p('E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData')

            global total_count
            global starttime_int
            fileName = ("C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\Roadwork_%d_%d.csv" % (starttime_int,total_count))
            # fileName = ("E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\Roadwork_%d_%d.csv" % (starttime_int,total_count))
            JSONconvert_Roadwork('features', url, fileName)
            print "[INFO] Updating finished"
        elif int(majorevent_time_mark) == int(latest_time_mark[:13]):
            majorevent_record.write( str(majorevent_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'\n')
            print "[INFO] No new data"
        elif int(majorevent_time_mark) < int(latest_time_mark[:13]):
            majorevent_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'  DISCARD: '+str(majorevent_time_mark)+'\n')
            print "[INFO] Receive and discard old data"
        else:
            print "[ERROR] unexpected"

def JSONconvert_MajorEvent(node,json_file_path,csv_file_path):
    
    response = urllib.urlopen(json_file_path)
    # load JSON file
    print("[INFO] URL load complete")

    raw_data = json.loads(response.read())
    try:
        data_to_be_processed = raw_data[node]
    except:
        data_to_be_processed = raw_data

    processed_data = []
    header = []
    global reduced_item
    for item in data_to_be_processed:
        reduced_item = {}
        reduce_item(node, item)

        header += reduced_item.keys()

        processed_data.append(reduced_item)

    global current_dataset_MajorEvent
    if current_dataset_MajorEvent == []:
        print "[INFO] Dataset written in memory"
        current_dataset_MajorEvent = processed_data
    else:
        print "[INFO] Dataset exists in memory"
        # merge processed_data with current_dataset
        for row in processed_data:
            # print type(row)
            row_id = row['features_id']
            # print row_id
            i = 0
            replaced = False
            for row_compare in current_dataset_MajorEvent:
                if row_compare['features_id'] == row_id:
                    print "[UPDATE] Row updated with id: ", row_id
                    current_dataset_MajorEvent[i] = row
                    replaced = True
                i += 1
            if replaced is False:
                current_dataset_MajorEvent.append(row)
                print "[UPDATE] New Row Appended!"

        print "[INFO] Dataset in memory updated"
    pickle_file = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_MajorEvent"
    # pickle_file = "E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_MajorEvent"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset_MajorEvent,f)
    print "[INFO] Data Cached in local file"

    header = list(set(header))
    header.sort()
    header = [e for e in header if e not in ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title')]
    header = [e for e in header if e not in ('features_properties_attendingGroups_0')]
    header = [e for e in header if e not in ('features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')]
    # print header
    removed_e = ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title','features_properties_attendingGroups_0','features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')
    
    # processed_data is the final data

    with open(csv_file_path, 'w+') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        global current_dataset_MajorEvent
        for row in current_dataset_MajorEvent:
            for k in removed_e:
                row.pop(k,None)
            try:
                writer.writerow(row)
            except:
                pass

    print ("[INFO] Completed writing csv file with %d columns" % len(header))

def check_MajorEvent():
    url = "http://data.livetraffic.com/traffic/hazards/majorevent.json"

    response = urllib.urlopen(url)
    # load JSON file
    majorevent = json.loads(response.read())
    print("[INFO] URL checked")

    majorevent_time_mark = majorevent['lastPublished']
    print "[INFO] Received time stamp: ", majorevent_time_mark
    # majorevent_parsed = majorevent['features']

    global starttime_int
    RecordFileName = ('C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\MajorEvent_update_history_%d.txt' % starttime_int) 
    # RecordFileName = ('E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\MajorEvent_update_history_%d.txt' % starttime_int) 

    with open(RecordFileName,'a+') as majorevent_record:

        try:
            latest_time_mark = majorevent_record.readlines()[-1]
            print"[INFO] Currently recorded time stamp: ", latest_time_mark
        except:
            latest_time_mark = str(0000000000000)
            print"[INFO] No existing time stamp recorded"

        if int(majorevent_time_mark) > int(latest_time_mark[:13]):
            print "[INFO] New Data Arrived"
            majorevent_record.write( str(majorevent_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '  NEW' +'\n')

            # open a file for writing, default in C:
            mkdir_p('C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData')
            # mkdir_p('E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData')
            global fileCheck
            fileCheck = os.path.isfile('/tmp/MajorEvent.csv')
            print "[INFO] CSV file exist: ", fileCheck

            global total_count
            global starttime_int
            fileName = ("C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\MajorEvent_%d_%d.csv" % (starttime_int,total_count))
            # fileName = ("E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\MajorEvent_%d_%d.csv" % (starttime_int,total_count))
            
            JSONconvert_MajorEvent('features', url, fileName)
            print "[INFO] Updating finished"
        elif int(majorevent_time_mark) == int(latest_time_mark[:13]):
            majorevent_record.write( str(majorevent_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'\n')
            print "[INFO] No new data"
        elif int(majorevent_time_mark) < int(latest_time_mark[:13]):
            majorevent_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'  DISCARD: '+str(majorevent_time_mark)+'\n')
            print "[INFO] Receive and discard old data"
        else:
            print "[ERROR] unexpected"

def JSONconvert_Incident(node,json_file_path,csv_file_path):
    
    response = urllib.urlopen(json_file_path)
    # load JSON file
    print("[INFO] URL load complete")

    raw_data = json.loads(response.read())
    try:
        data_to_be_processed = raw_data[node]
    except:
        data_to_be_processed = raw_data

    processed_data = []
    header = []
    global reduced_item
    for item in data_to_be_processed:
        reduced_item = {}
        reduce_item(node, item)

        header += reduced_item.keys()

        processed_data.append(reduced_item)

    global current_dataset_Incident
    if current_dataset_Incident == []:
        print "[INFO] Dataset written in memory"
        current_dataset_Incident = processed_data
    else:
        print "[INFO] Dataset exists in memory"
        # merge processed_data with current_dataset
        for row in processed_data:
            # print type(row)
            row_id = row['features_id']
            # print row_id
            i = 0
            replaced = False
            for row_compare in current_dataset_Incident:
                if row_compare['features_id'] == row_id:
                    print "[UPDATE] Row updated with id: ", row_id
                    current_dataset_Incident[i] = row
                    replaced = True
                i += 1
            if replaced is False:
                current_dataset_Incident.append(row)
                print "[UPDATE] New Row Appended!"

        print "[INFO] Dataset in memory updated"
    pickle_file = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Incident"
    # pickle_file = "E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Incident"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset_Incident,f)
    print "[INFO] Data Cached in local file"

    header = list(set(header))
    header.sort()
    header = [e for e in header if e not in ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title')]
    header = [e for e in header if e not in ('features_properties_attendingGroups_0')]
    header = [e for e in header if e not in ('features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')]
    # print header
    removed_e = ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title','features_properties_attendingGroups_0','features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')
    
    # processed_data is the final data

    with open(csv_file_path, 'w+') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        global current_dataset_Incident
        for row in current_dataset_Incident:
            for k in removed_e:
                row.pop(k,None)
            try:
                writer.writerow(row)
            except:
                pass

    print ("[INFO] Completed writing csv file with %d columns" % len(header))

def check_Incident():
    url = "http://data.livetraffic.com/traffic/hazards/incident.json"

    response = urllib.urlopen(url)
    # load JSON file
    majorevent = json.loads(response.read())
    print("[INFO] URL checked")

    majorevent_time_mark = majorevent['lastPublished']
    print "[INFO] Received time stamp: ", majorevent_time_mark
    # majorevent_parsed = majorevent['features']

    global starttime_int
    RecordFileName = ('C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\Incident_update_history_%d.txt' % starttime_int) 
    # RecordFileName = ('E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\Incident_update_history_%d.txt' % starttime_int) 
    with open(RecordFileName,'a+') as majorevent_record:

        try:
            latest_time_mark = majorevent_record.readlines()[-1]
            print"[INFO] Currently recorded time stamp: ", latest_time_mark
        except:
            latest_time_mark = str(0000000000000)
            print"[INFO] No existing time stamp recorded"

        if int(majorevent_time_mark) > int(latest_time_mark[:13]):
            print "[INFO] New Data Arrived"
            majorevent_record.write( str(majorevent_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '  NEW' +'\n')

            # open a file for writing, default in C:
            mkdir_p('C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData')
            # mkdir_p('E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData')

            global total_count
            global starttime_int
            fileName = ("C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\Incident_%d_%d.csv" % (starttime_int,total_count))
            # fileName = ("E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\Incident_%d_%d.csv" % (starttime_int,total_count))
            JSONconvert_Incident('features', url, fileName)
            print "[INFO] Updating finished"
        elif int(majorevent_time_mark) == int(latest_time_mark[:13]):
            majorevent_record.write( str(majorevent_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'\n')
            print "[INFO] No new data"
        elif int(majorevent_time_mark) < int(latest_time_mark[:13]):
            majorevent_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'  DISCARD: '+str(majorevent_time_mark)+'\n')
            print "[INFO] Receive and discard old data"
        else:
            print "[ERROR] unexpected"

if __name__ == "__main__":
    
    global current_dataset_Roadwork, current_dataset_MajorEvent, current_dataset_Incident
    current_dataset_Roadwork = []
    current_dataset_MajorEvent = []
    current_dataset_Incident = []

    pickle_file_Roadwork = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Roadwork"
    pickle_file_Incident = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Incident"
    pickle_file_MajorEvent = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_MajorEvent"

    # pickle_file_Roadwork = "E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Roadwork"
    # pickle_file_Incident = "E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Incident"
    # pickle_file_MajorEvent = "E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_MajorEvent"

    try:
        with open(pickle_file_Roadwork,'rb') as f:
            global current_dataset_Roadwork
            current_dataset_Roadwork = pickle.load(f)
        print "[INFO] Cache read successfully"
    except:
        pass
        
    try:
        with open(pickle_file_MajorEvent,'rb') as f:
            global current_dataset_MajorEvent
            current_dataset_MajorEvent = pickle.load(f)
        print "[INFO] Cache read successfully"
    except:
        pass

    try:
        with open(pickle_file_Incident,'rb') as f:
            global current_dataset_Incident
            current_dataset_Incident = pickle.load(f)
        print "[INFO] Cache read successfully"
    except:
        pass

    starttime=time.time()

    global starttime_int
    starttime_int = int(time.time())

    global total_count
    total_count = 0

    while True:
        print '====================================='
        global total_count
        total_count += 1
        check_Roadwork()
        print "[INFO] Roadwork checked successfully"
        check_Incident()
        print "[INFO] Incident checked successfully"
        check_MajorEvent()
        print "[INFO] Major event checked successfully"

        print; print "[DONE] Finished checking, iteration: ", total_count
        print '====================================='
        time.sleep(1800.0 - ((time.time() - starttime) % 1800.0))