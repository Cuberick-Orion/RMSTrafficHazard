import urllib, json
import csv
import sys, os, errno
import os.path
import io
import datetime
from time import gmtime, strftime
import time
import pickle

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

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

def JSONconvert_Roadwork(node,raw_data,csv_file_path):

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
                    # print "[UPDATE] Row updated with id: ", row_id
                    current_dataset_Roadwork[i] = row
                    replaced = True
                i += 1
            if replaced is False:
                current_dataset_Roadwork.append(row)
                print "[UPDATE] New Row Appended: ", row_id

        print "[INFO] Roadwork Dataset in memory updated"

    pickle_file = fileDir + "pickle_temp_Roadwork"
    # pickle_file = "E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Roadwork"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset_Roadwork,f)
    print "[INFO] Roadwork Data Cached in local file"


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
        for row in current_dataset_Roadwork:
            for k in removed_e:
                row.pop(k,None)
            try:
                writer.writerow(row)
            except:
                pass

    print ("[INFO] Completed writing csv file with %d columns" % len(header))

def JSONconvert_MajorEvent(node,raw_data,csv_file_path):

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
                print "[UPDATE] New Row Appended: ", row_id

        print "[INFO] MajorEvent Dataset in memory updated"

    pickle_file = fileDir + "pickle_temp_MajorEvent"
    # pickle_file = "E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_MajorEvent"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset_MajorEvent,f)
    print "[INFO] MajorEvent Data Cached in local file"

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
        for row in current_dataset_MajorEvent:
            for k in removed_e:
                row.pop(k,None)
            try:
                writer.writerow(row)
            except:
                pass

    print ("[INFO] Completed writing csv file with %d columns" % len(header))

def JSONconvert_Incident(node,raw_data,csv_file_path):

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
                print "[UPDATE] New Row Appended: ", row_id

        print "[INFO] Incident Dataset in memory updated"
    pickle_file = fileDir + "pickle_temp_Incident"
    # pickle_file = "E:\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Incident"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset_Incident,f)
    print "[INFO] Incident Data Cached in local file"

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
        for row in current_dataset_Incident:
            for k in removed_e:
                row.pop(k,None)
            try:
                writer.writerow(row)
            except:
                pass

    print ("[INFO] Completed writing csv file with %d columns" % len(header))

def check():
    Incident_url = "http://data.livetraffic.com/traffic/hazards/incident.json"
    Incident_response = urllib.urlopen(Incident_url)
    # load JSON file
    Incident_received = json.loads(Incident_response.read())
    print("[INFO] URL checked")

    Incident_received_time_mark = Incident_received['lastPublished']
    print "[INFO] Incident Received time stamp: ", Incident_received_time_mark

    Incident_RecordFileNameDir = fileDir + 'Incident_update_history_%d.txt'
    Incident_RecordFileName = (Incident_RecordFileNameDir % starttime_int) 

    with open(Incident_RecordFileName,'a+') as Incident_record:
        try:
            latest_time_mark = Incident_record.readlines()[-1]
            print"[INFO] Currently recorded time stamp: ", latest_time_mark
        except:
            latest_time_mark = str(0000000000000)
            print"[INFO] No existing time stamp recorded"

        if int(Incident_received_time_mark) > int(latest_time_mark[:13]):
            print "[INFO] New Data Arrived"
            Incident_record.write( str(Incident_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '  NEW' +'\n')

            mkdir_p(fileDir)
            Incident_fileNameDir = fileDir + "Incident_%d_%d.csv"
            Incident_fileName = (Incident_fileNameDir % (starttime_int,total_count))

            JSONconvert_Incident('features', Incident_received, Incident_fileName)
            print "[INFO] Updating finished"

        elif int(Incident_received_time_mark) == int(latest_time_mark[:13]):
            Incident_record.write( str(Incident_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'\n')
            print "[INFO] No new data"
        elif int(Incident_received_time_mark) < int(latest_time_mark[:13]):
            Incident_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'  DISCARD: '+str(Incident_received_time_mark)+'\n')
            print "[INFO] Receive and discard old data"
        else:
            print "[ERROR] unexpected"
            pause()
    
    MajorEvent_url = "http://data.livetraffic.com/traffic/hazards/majorevent.json"
    MajorEvent_response = urllib.urlopen(MajorEvent_url)
    # load JSON file
    MajorEvent_received = json.loads(MajorEvent_response.read())
    print("[INFO] URL checked")

    MajorEvent_received_time_mark = MajorEvent_received['lastPublished']
    print "[INFO] MajorEvent Received time stamp: ", MajorEvent_received_time_mark

    MajorEvent_RecordFileNameDir = fileDir + 'MajorEvent_update_history_%d.txt'
    MajorEvent_RecordFileName = (MajorEvent_RecordFileNameDir % starttime_int) 

    with open(MajorEvent_RecordFileName,'a+') as MajorEvent_record:
        try:
            latest_time_mark = MajorEvent_record.readlines()[-1]
            print"[INFO] Currently recorded time stamp: ", latest_time_mark
        except:
            latest_time_mark = str(0000000000000)
            print"[INFO] No existing time stamp recorded"

        if int(MajorEvent_received_time_mark) > int(latest_time_mark[:13]):
            print "[INFO] New Data Arrived"
            MajorEvent_record.write( str(MajorEvent_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '  NEW' +'\n')

            mkdir_p(fileDir)
            MajorEvent_fileNameDir = fileDir + "MajorEvent_%d_%d.csv"
            MajorEvent_fileName = (MajorEvent_fileNameDir % (starttime_int,total_count))

            JSONconvert_MajorEvent('features', MajorEvent_received, MajorEvent_fileName)
            print "[INFO] Updating finished"

        elif int(MajorEvent_received_time_mark) == int(latest_time_mark[:13]):
            MajorEvent_record.write( str(MajorEvent_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'\n')
            print "[INFO] No new data"
        elif int(MajorEvent_received_time_mark) < int(latest_time_mark[:13]):
            MajorEvent_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'  DISCARD: '+str(MajorEvent_received_time_mark)+'\n')
            print "[INFO] Receive and discard old data"
        else:
            print "[ERROR] unexpected"
            pause()

    Roadwork_url = "http://data.livetraffic.com/traffic/hazards/roadwork.json"
    Roadwork_response = urllib.urlopen(Roadwork_url)
    # load JSON file
    Roadwork_received = json.loads(Roadwork_response.read())
    print("[INFO] URL checked")

    Roadwork_received_time_mark = Roadwork_received['lastPublished']
    print "[INFO] Roadwork Received time stamp: ", Roadwork_received_time_mark

    Roadwork_RecordFileNameDir = fileDir + 'Roadwork_update_history_%d.txt'
    Roadwork_RecordFileName = (Roadwork_RecordFileNameDir % starttime_int) 

    with open(Roadwork_RecordFileName,'a+') as Roadwork_record:
        try:
            latest_time_mark = Roadwork_record.readlines()[-1]
            print"[INFO] Currently recorded time stamp: ", latest_time_mark
        except:
            latest_time_mark = str(0000000000000)
            print"[INFO] No existing time stamp recorded"

        if int(Roadwork_received_time_mark) > int(latest_time_mark[:13]):
            print "[INFO] New Data Arrived"
            Roadwork_record.write( str(Roadwork_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '  NEW' +'\n')

            mkdir_p(fileDir)
            Roadwork_fileNameDir = fileDir + "Roadwork_%d_%d.csv"
            Roadwork_fileName = (Roadwork_fileNameDir % (starttime_int,total_count))

            JSONconvert_Roadwork('features', Roadwork_received, Roadwork_fileName)
            print "[INFO] Updating finished"

        elif int(Roadwork_received_time_mark) == int(latest_time_mark[:13]):
            Roadwork_record.write( str(Roadwork_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'\n')
            print "[INFO] No new data"
        elif int(Roadwork_received_time_mark) < int(latest_time_mark[:13]):
            Roadwork_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'  DISCARD: '+str(Roadwork_received_time_mark)+'\n')
            print "[INFO] Receive and discard old data"
        else:
            print "[ERROR] unexpected"
            pause()



if __name__ == "__main__":
    
    fileDir_prefix = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\\"
    fileDir_folder = "LiveTrafficData\\"
    global fileDir
    fileDir = fileDir_prefix + fileDir_folder
    
    global current_dataset_Roadwork, current_dataset_MajorEvent, current_dataset_Incident
    current_dataset_Roadwork = []
    current_dataset_MajorEvent = []
    current_dataset_Incident = []

    pickle_file_Roadwork = fileDir + "pickle_temp_Roadwork"
    pickle_file_Incident = fileDir + "pickle_temp_Incident"
    pickle_file_MajorEvent = fileDir + "pickle_temp_MajorEvent"

    try:
        with open(pickle_file_Roadwork,'rb') as f:

            current_dataset_Roadwork = pickle.load(f)
        print "[INFO] Roadwork Cache read successfully"
    except:
        pass
        
    try:
        with open(pickle_file_MajorEvent,'rb') as f:

            current_dataset_MajorEvent = pickle.load(f)
        print "[INFO] MajorEvent Cache read successfully"
    except:
        pass

    try:
        with open(pickle_file_Incident,'rb') as f:

            current_dataset_Incident = pickle.load(f)
        print "[INFO] IncidentCache read successfully"
    except:
        pass

    starttime=time.time()
    starttime_int = int(time.time())
    total_count = 0

    while True:
        print; print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        total_count += 1

        check()

        print; print "[INFO] Finished updating, count: ", total_count
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

        for i in xrange(1800,0,-1):
            time.sleep(1)
            sys.stdout.write( '\rCountdown for next update: %04s' % str(i))
            sys.stdout.flush()