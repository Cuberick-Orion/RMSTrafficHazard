import urllib, json
import csv
import sys, os, errno
import os.path
import io
import datetime
from time import gmtime, strftime, localtime
import time
import pickle
import process
import shutil

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

def JSONconvert_Roadwork(node,raw_data,csv_file_path,csv_file_changes):
    file_changes = open(csv_file_changes,'w+')
    file_changes.write ('>>>Record changes made in this update \n')

    rows_updated_count = 0
    rows_appended_count = 0

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
        current_dataset_Roadwork = processed_data
        print "[INFO] New dataset written in memory"
        file_changes.write('No previous data, write received dataset to csv')
    else:
        
        print "[INFO] Dataset exists in memory, will be updated"
        # merge processed_data with current_dataset
        for row in processed_data:
            # print type(row)
            row_id = row['features_id']
            # print row_id
            i = 0
            replaced = False
            for row_compare in current_dataset_Roadwork:
                if row_compare['features_id'] == row_id:
                    file_changes.write("[UPDATE] Row updated with id: " + str(row_id) + "\n")
                    rows_updated_count += 1
                    current_dataset_Roadwork[i] = row
                    replaced = True
                i += 1
            if replaced is False:
                current_dataset_Roadwork.append(row)
                file_changes.write("[APPEND] New Row Appended: " + str(row_id) + "\n")
                rows_appended_count += 1
        print "[INFO] Roadwork Dataset is updated with received data"
        print "[INFO] No. of rows updated: ", rows_updated_count, " | No. of rows appended: ", rows_appended_count, "Details recorded in .change file"
    file_changes.close()
    
    pickle_file = fileDir + "Roadwork_cache"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset_Roadwork,f)
    shutil.copy(pickle_file,Dropbox_dir)
    print "[INFO] Roadwork Data cached in local file"

    header = list(set(header))
    header.sort()
    # header = [e for e in header if e not in ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title')]
    # header = [e for e in header if e not in ('features_properties_attendingGroups_0')]
    # header = [e for e in header if e not in ('features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')]
    # removed_e = ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title','features_properties_attendingGroups_0','features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')
    
    # processed_data is the final data
    with open(csv_file_path, 'w+') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in current_dataset_Roadwork:
            # for k in removed_e:
            #     row.pop(k,None)
            try:
                writer.writerow(row)
            except:
                pass

def JSONconvert_MajorEvent(node,raw_data,csv_file_path,csv_file_changes):
    file_changes = open(csv_file_changes,'w+')
    file_changes.write ('>>>Record changes made in this update \n')

    rows_updated_count = 0
    rows_appended_count = 0

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
        current_dataset_MajorEvent = processed_data
        print "[INFO] New dataset written in memory"
        file_changes.write('No previous data, write received dataset to csv')
    else:
        
        print "[INFO] Dataset exists in memory, will be updated"
        # merge processed_data with current_dataset
        for row in processed_data:
            # print type(row)
            row_id = row['features_id']
            # print row_id
            i = 0
            replaced = False
            for row_compare in current_dataset_MajorEvent:
                if row_compare['features_id'] == row_id:
                    file_changes.write("[UPDATE] Row updated with id: " + str(row_id) + "\n")
                    rows_updated_count += 1
                    current_dataset_MajorEvent[i] = row
                    replaced = True
                i += 1
            if replaced is False:
                current_dataset_MajorEvent.append(row)
                file_changes.write("[APPEND] New Row Appended: " + str(row_id) + "\n")
                rows_appended_count += 1
        print "[INFO] MajorEvent Dataset is updated with received data"
        print "[INFO] No. of rows updated: ", rows_updated_count, " | No. of rows appended: ", rows_appended_count, "Details recorded in .change file"
    file_changes.close()
    
    pickle_file = fileDir + "MajorEvent_cache"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset_MajorEvent,f)
    shutil.copy(pickle_file,Dropbox_dir)
    print "[INFO] MajorEvent Data cached in local file"

    header = list(set(header))
    header.sort()
    # header = [e for e in header if e not in ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title')]
    # header = [e for e in header if e not in ('features_properties_attendingGroups_0')]
    # header = [e for e in header if e not in ('features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')]
    # removed_e = ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title','features_properties_attendingGroups_0','features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')
    
    # processed_data is the final data
    with open(csv_file_path, 'w+') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in current_dataset_MajorEvent:
            # for k in removed_e:
            #     row.pop(k,None)
            try:
                writer.writerow(row)
            except:
                pass

def JSONconvert_Incident(node,raw_data,csv_file_path,csv_file_changes):
    file_changes = open(csv_file_changes,'w+')
    file_changes.write ('>>>Record changes made in this update \n')

    rows_updated_count = 0
    rows_appended_count = 0

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
        current_dataset_Incident = processed_data
        print "[INFO] New dataset written in memory"
        file_changes.write('No previous data, write received dataset to csv')
    else:
        
        print "[INFO] Dataset exists in memory, will be updated"
        # merge processed_data with current_dataset
        for row in processed_data:
            # print type(row)
            row_id = row['features_id']
            # print row_id
            i = 0
            replaced = False
            for row_compare in current_dataset_Incident:
                if row_compare['features_id'] == row_id:
                    file_changes.write("[UPDATE] Row updated with id: " + str(row_id) + "\n")
                    rows_updated_count += 1
                    current_dataset_Incident[i] = row
                    replaced = True
                i += 1
            if replaced is False:
                current_dataset_Incident.append(row)
                file_changes.write("[APPEND] New Row Appended: " + str(row_id) + "\n")
                rows_appended_count += 1
        print "[INFO] Incident Dataset is updated with received data"
        print "[INFO] No. of rows updated: ", rows_updated_count, " | No. of rows appended: ", rows_appended_count, "Details recorded in .change file"
    file_changes.close()
    
    pickle_file = fileDir + "Incident_cache"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset_Incident,f)
    shutil.copy(pickle_file,Dropbox_dir)
    print "[INFO] Incident Data cached in local file"

    header = list(set(header))
    header.sort()
    # header = [e for e in header if e not in ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title')]
    # header = [e for e in header if e not in ('features_properties_attendingGroups_0')]
    # header = [e for e in header if e not in ('features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')]
    # removed_e = ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title','features_properties_attendingGroups_0','features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')
    
    # processed_data is the final data
    with open(csv_file_path, 'w+') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in current_dataset_Incident:
            # for k in removed_e:
            #     row.pop(k,None)
            try:
                writer.writerow(row)
            except:
                pass

def check():
    Incident_url = "http://data.livetraffic.com/traffic/hazards/incident.json"
    Incident_response = urllib.urlopen(Incident_url)
    # load JSON file
    Incident_received = json.loads(Incident_response.read())
    print;print("[INFO] Incident data URL checked")

    Incident_received_time_mark = Incident_received['lastPublished']
    print "[INFO] Incident Received time stamp: ", Incident_received_time_mark

    Incident_RecordFileName = fileDir + 'Incident_update_history.txt'

    with open(Incident_RecordFileName,'a+') as Incident_record:
        
        latest_time_mark = Incident_record.readlines()[-1] #read the last line, assume if the program has iterated more than once
        if latest_time_mark[:1] == '>' or latest_time_mark[:1] == 'P': # this means that the program has just started
            Incident_record.seek(0)
            try: #try to find the last line from the last run
                latest_time_mark = Incident_record.readlines()[-3] #Assumption! that program at least updates once for each run
                print"[INFO] Currently recorded Incident data time stamp: (from last run) ", latest_time_mark
            except: #out of range for Index, meaning that the history data has just been created, no previous record
                print"[INFO] No existing Incident data time stamp recorded in history"
                latest_time_mark = str(0000000000000)
        else: #last line found, meaning that the program has iterated for at least one time
            print"[INFO] Currently recorded time stamp: (from last iteration) ", latest_time_mark

        if int(Incident_received_time_mark) > int(latest_time_mark[:13]):
            print "[INFO] New Incident Data Arrived"
            Incident_record.write( str(Incident_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + '  NEW' +'\n')

            mkdir_p(fileDir)
            Incident_fileNameDir = fileDir + "Incident_%d_%d.csv"
            Incident_fileName = (Incident_fileNameDir % (starttime_int,total_count))
            Incident_fileChange = Incident_fileName + ".change"
            JSONconvert_Incident('features', Incident_received, Incident_fileName,Incident_fileChange)
            print "[INFO] Updating Incident data finished"

        elif int(Incident_received_time_mark) == int(latest_time_mark[:13]):
            Incident_record.write( str(Incident_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) +'\n')
            print "[INFO] No new Incident data"
        elif int(Incident_received_time_mark) < int(latest_time_mark[:13]):
            Incident_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) +'  DISCARD: '+str(Incident_received_time_mark)+'\n')
            print "[INFO] Receive and discard old Incident data"
        else:
            print "[ERROR] unexpected (Incident data)"
            
            os.pause()
    
    MajorEvent_url = "http://data.livetraffic.com/traffic/hazards/majorevent.json"
    MajorEvent_response = urllib.urlopen(MajorEvent_url)
    # load JSON file
    MajorEvent_received = json.loads(MajorEvent_response.read())
    print;print("[INFO] MajorEvent URL checked")

    MajorEvent_received_time_mark = MajorEvent_received['lastPublished']
    print "[INFO] MajorEvent Received time stamp: ", MajorEvent_received_time_mark

    MajorEvent_RecordFileName = fileDir + 'MajorEvent_update_history.txt'

    with open(MajorEvent_RecordFileName,'a+') as MajorEvent_record:
        
        latest_time_mark = MajorEvent_record.readlines()[-1] #read the last line, assume if the program has iterated more than once
        if latest_time_mark[:1] == '>' or latest_time_mark[:1] == 'P': # this means that the program has just started
            MajorEvent_record.seek(0)
            try: #try to find the last line from the last run
                latest_time_mark = MajorEvent_record.readlines()[-3] #Assumption! that program at least updates once for each run
                print"[INFO] Currently recorded MajorEvent data time stamp: (from last run) ", latest_time_mark
            except: #out of range for Index, meaning that the history data has just been created, no previous record
                print"[INFO] No existing time stamp recorded in history"
                latest_time_mark = str(0000000000000)
        else: #last line found, meaning that the program has iterated for at least one time
            print"[INFO] Currently recorded MajorEvent data time stamp: (from last iteration) ", latest_time_mark

        if int(MajorEvent_received_time_mark) > int(latest_time_mark[:13]):
            print "[INFO] New MajorEvent Data Arrived"
            MajorEvent_record.write( str(MajorEvent_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + '  NEW' +'\n')

            mkdir_p(fileDir)
            MajorEvent_fileNameDir = fileDir + "MajorEvent_%d_%d.csv"
            MajorEvent_fileName = (MajorEvent_fileNameDir % (starttime_int,total_count))
            MajorEvent_fileChange = MajorEvent_fileName + ".change"
            JSONconvert_MajorEvent('features', MajorEvent_received, MajorEvent_fileName,MajorEvent_fileChange)
            print "[INFO] Updating MajorEvent data finished"

        elif int(MajorEvent_received_time_mark) == int(latest_time_mark[:13]):
            MajorEvent_record.write( str(MajorEvent_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) +'\n')
            print "[INFO] No new MajorEvent data"
        elif int(MajorEvent_received_time_mark) < int(latest_time_mark[:13]):
            MajorEvent_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) +'  DISCARD: '+str(MajorEvent_received_time_mark)+'\n')
            print "[INFO] Receive and discard old MajorEvent data"
        else:
            print "[ERROR] unexpected (MajorEvent)"
            
            os.pause()
    
       

    Roadwork_url = "http://data.livetraffic.com/traffic/hazards/roadwork.json"
    Roadwork_response = urllib.urlopen(Roadwork_url)
    # load JSON file
    Roadwork_received = json.loads(Roadwork_response.read())
    print;print("[INFO] Roadwork URL checked")

    Roadwork_received_time_mark = Roadwork_received['lastPublished']
    print "[INFO] Roadwork Received time stamp: ", Roadwork_received_time_mark

    Roadwork_RecordFileName = fileDir + 'Roadwork_update_history.txt'

    with open(Roadwork_RecordFileName,'a+') as Roadwork_record:
        
        latest_time_mark = Roadwork_record.readlines()[-1] #read the last line, assume if the program has iterated more than once
        if latest_time_mark[:1] == '>' or latest_time_mark[:1] == 'P': # this means that the program has just started
            Roadwork_record.seek(0)
            try: #try to find the last line from the last run
                latest_time_mark = Roadwork_record.readlines()[-3] #Assumption! that program at least updates once for each run
                print"[INFO] Currently recorded Roadwork data time stamp: (from last run) ", latest_time_mark
            except: #out of range for Index, meaning that the history data has just been created, no previous record
                print"[INFO] No existing Roadwork data time stamp recorded in history"
                latest_time_mark = str(0000000000000)
        else: #last line found, meaning that the program has iterated for at least one time
            print"[INFO] Currently recorded Roadwork data time stamp: (from last iteration) ", latest_time_mark

        if int(Roadwork_received_time_mark) > int(latest_time_mark[:13]):
            print "[INFO] New Roadwork Data Arrived"
            Roadwork_record.write( str(Roadwork_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + '  NEW' +'\n')

            mkdir_p(fileDir)
            Roadwork_fileNameDir = fileDir + "Roadwork_%d_%d.csv"
            Roadwork_fileName = (Roadwork_fileNameDir % (starttime_int,total_count))
            Roadwork_fileChange = Roadwork_fileName + ".change"
            JSONconvert_Roadwork('features', Roadwork_received, Roadwork_fileName,Roadwork_fileChange)
            print "[INFO] Updating Roadwork data finished"

        elif int(Roadwork_received_time_mark) == int(latest_time_mark[:13]):
            Roadwork_record.write( str(Roadwork_received_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) +'\n')
            print "[INFO] No new Roadwork data"
        elif int(Roadwork_received_time_mark) < int(latest_time_mark[:13]):
            Roadwork_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) +'  DISCARD: '+str(Roadwork_received_time_mark)+'\n')
            print "[INFO] Receive and discard old Roadwork data"
        else:
            print "[ERROR] unexpected (Roadwork)"
            
            os.pause()

    generated_file_list = []
    
    try:
        generated_file_list.append(MajorEvent_fileName)
    except:
        pass
    try:
        generated_file_list.append(Incident_fileName)
    except:
        pass
    try:
        generated_file_list.append(Roadwork_fileName)
    except:
        pass

    return generated_file_list

if __name__ == "__main__":
    starttime=time.time()
    starttime_int = int(time.time())
    starttime_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    starttime_str_local = strftime("%Y-%m-%d %H:%M:%S", localtime())
    total_count = 0
    # =====================================
    # fileDir_prefix = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\\"
    # fileDir_folder = "LiveTrafficData\\"
    # Dropbox_dir = "C:\Users\LIU136\Dropbox\David Liu Internship\LiveTrafficData\\"
    # =====================================
    # fileDir_prefix = "E:\OneDrive - Australian National University\Internship\CSIRO43691\\"
    # fileDir_folder = "LiveTrafficData\\"
    # Dropbox_dir = "E:\Dropbox\David Liu Internship\LiveTrafficData\\"
    # =====================================
    fileDir_prefix = "C:\Users\\asuna\OneDrive - Australian National University\Internship\CSIRO43691\\"
    fileDir_folder = "LiveTrafficData\\"
    Dropbox_dir = "C:\Users\\asuna\Dropbox\David Liu Internship\LiveTrafficData\\"
    # =====================================

    global fileDir
    fileDir = fileDir_prefix + fileDir_folder
    
    global current_dataset_Roadwork, current_dataset_MajorEvent, current_dataset_Incident
    current_dataset_Roadwork = []
    current_dataset_MajorEvent = []
    current_dataset_Incident = []

    pickle_file_Roadwork = fileDir + "Roadwork_cache"
    pickle_file_Incident = fileDir + "Incident_cache"
    pickle_file_MajorEvent = fileDir + "MajorEvent_cache"

    try:
        with open(pickle_file_Roadwork,'rb') as f:
            current_dataset_Roadwork = pickle.load(f)
        print "[INFO] Roadwork cache read successfully"
    except:
        print "[INFO] Roadwork cache not found, will create a new one"
        pass
        
    try:
        with open(pickle_file_MajorEvent,'rb') as f:
            current_dataset_MajorEvent = pickle.load(f)
        print "[INFO] MajorEvent cache read successfully"
    except:
        print "[INFO] MajorEvent cache not found, will create a new one"
        pass

    try:
        with open(pickle_file_Incident,'rb') as f:
            current_dataset_Incident = pickle.load(f)
        print "[INFO] Incident cache read successfully"
    except:
        print "[INFO] Incident cache not found, will create a new one"
        pass

    MajorEvent_RecordFileName = fileDir + 'MajorEvent_update_history.txt'
    with open(MajorEvent_RecordFileName,'a+') as f:
        f.write ('>>>' +'\n')
        f.write ('Program started at ' + str(starttime_int) + ' @UTC time:' + starttime_str + ' @local time:' + starttime_str_local + '\n')
    
    Roadwork_RecordFileName = fileDir + 'Roadwork_update_history.txt'
    with open(Roadwork_RecordFileName,'a+') as f:
        f.write ('>>>' +'\n')
        f.write ('Program started at ' + str(starttime_int) + ' @UTC time:' + starttime_str + ' @local time:' + starttime_str_local + '\n')

    Incident_RecordFileName = fileDir + 'Incident_update_history.txt'
    with open(Incident_RecordFileName,'a+') as f:
        f.write ('>>>' +'\n')
        f.write ('Program started at ' + str(starttime_int) + ' @UTC time:' + starttime_str + ' @local time:' + starttime_str_local + '\n')

    shutil.copy(MajorEvent_RecordFileName,Dropbox_dir)
    shutil.copy(Roadwork_RecordFileName,Dropbox_dir)
    shutil.copy(Incident_RecordFileName,Dropbox_dir)
    
    print "[INFO] History record prepared"

    while True:
        print; print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        total_count += 1

        fileList = check()

        print; print "[INFO] Finished updating, This is the ", total_count, "th update"
        process.main(True,fileList)
        
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'; print
        

        for i in xrange(900,0,-1):
            time.sleep(1)
            sys.stdout.write( '\rCountdown for next update: %04s' % str(i))
            sys.stdout.flush()



