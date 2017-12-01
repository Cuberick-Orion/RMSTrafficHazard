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


# if __name__ == "__main__":
def JSONconvert(node,json_file_path,csv_file_path):

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

    global current_dataset
    if current_dataset == []:
        print "[INFO] Dataset written in memory"
        current_dataset = processed_data
    else:
        print "[INFO] Dataset exists in memory"
        # merge processed_data with current_dataset
        for row in processed_data:
            # print type(row)
            row_id = row['features_id']
            # print row_id
            i = 0
            replaced = False
            for row_compare in current_dataset:
                if row_compare['features_id'] == row_id:
                    print "[UPDATE] Row updated with id: ", row_id
                    current_dataset[i] = row
                    replaced = True
                i += 1
            if replaced is False:
                current_dataset.append(row)
                print "[UPDATE] New Row Appended!"

        print "[INFO] Dataset in memory updated"
    pickle_file = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Roadwork"
    with open(pickle_file,'wb') as f:
        pickle.dump(current_dataset,f)
    print "[INFO] Data Cached in local file"


    header = list(set(header))
    header.sort()
    header = [e for e in header if e not in ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title')]
    header = [e for e in header if e not in ('features_properties_attendingGroups_0')]
    header = [e for e in header if e not in ('features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')]
    # print header
    removed_e = ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title','features_properties_attendingGroups_0','features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')
    
    # processed_data is the final data

    # global fileCheck
    # global current_dataset
    # if fileCheck == False:
    with open(csv_file_path, 'w+') as f:
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        global current_dataset
        for row in current_dataset:
            for k in removed_e:
                row.pop(k,None)
            writer.writerow(row)
    # else:
    #     with open(csv_file_path, 'a+') as f:
    #         writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
    #         # writer.writeheader()
    #         global current_dataset
    #         for row in current_dataset:
    #             for k in removed_e:
    #                 row.pop(k,None)
    #             writer.writerow(row)


    print ("[INFO] Completed writing csv file with %d columns" % len(header))


def check():
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
    with open(RecordFileName,'a+') as majorevent_record:

        try:
            latest_time_mark = majorevent_record.readlines()[-1]
            print"[INFO] Currently recorded time stamp: ", latest_time_mark
        except:
            latest_time_mark = str(0000000000000)
            print"[INFO] No existing time stamp recorded"

        if int(majorevent_time_mark) != int(latest_time_mark[:13]):
            print "[INFO] New Data Arrived"
            majorevent_record.write( str(majorevent_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '  NEW' +'\n')

            # open a file for writing, default in C:
            mkdir_p('C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData')

            global fileCheck
            fileCheck = os.path.isfile('/tmp/MajorEvent.csv')
            print "[INFO] CSV file exist: ", fileCheck

            global total_count
            global starttime_int
            fileName = ("C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\Roadwork_%d_%d.csv" % (starttime_int,total_count))
            JSONconvert('features', url, fileName)
            print "[INFO] Updating finished"
        elif int(majorevent_time_mark) == int(latest_time_mark[:13]):
            majorevent_record.write( str(majorevent_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'\n')
            print "[INFO] No new data"
        # elif int(majorevent_time_mark) < int(latest_time_mark[:13]):
        #     majorevent_record.write( str(int(latest_time_mark[:13]))+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'  DISCARD: '+str(majorevent_time_mark)+'\n')
        #     print "[INFO] Receive and discard old data"
        else:
            print "[ERROR] unexpected"

if __name__ == "__main__":
    pickle_file = "C:\Users\LIU136\OneDrive - Australian National University\Internship\CSIRO43691\LiveTrafficData\pickle_temp_Roadwork"
    try:
        with open(pickle_file,'rb') as f:
            global current_dataset
            current_dataset = pickle.load(f)
        print "[INFO] Cache read successfully"
    except:
        pass

    starttime=time.time()
    global starttime_int
    starttime_int = int(time.time())
    global total_count
    total_count = 0

    global current_dataset
    current_dataset = []

    while True:
        global total_count
        total_count += 1
        check()
        print; print "[DONE] Finished checking, iteration: ", total_count
        time.sleep(1800.0 - ((time.time() - starttime) % 1800.0))