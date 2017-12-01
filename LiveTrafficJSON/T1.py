import urllib, json
import csv
import sys, os, errno
import os.path
import io
import datetime
from time import gmtime, strftime
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

    header = list(set(header))
    header.sort()
    header = [e for e in header if e not in ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title')]
    header = [e for e in header if e not in ('features_properties_attendingGroups_0')]
    header = [e for e in header if e not in ('features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')]
    # print header
    removed_e = ('features_properties_additionalInfo_0','features_properties_adviceA','features_properties_adviceB', 'features_properties_arrangementAttachments_0_displayName', 'features_properties_arrangementAttachments_0_fileName', 'features_properties_arrangementAttachments_0_fileType', 'features_properties_arrangementAttachments_0_linkName', 'features_properties_arrangementAttachments_0_sizeInBytes', 'features_properties_arrangementAttachments_0_uniqueFileName', 'features_properties_arrangementAttachments_1_displayName', 'features_properties_arrangementAttachments_1_fileName', 'features_properties_arrangementAttachments_1_fileType', 'features_properties_arrangementAttachments_1_linkName', 'features_properties_arrangementAttachments_1_sizeInBytes', 'features_properties_arrangementAttachments_1_uniqueFileName', 'features_properties_arrangementAttachments_2_displayName', 'features_properties_arrangementAttachments_2_fileName', 'features_properties_arrangementAttachments_2_fileType', 'features_properties_arrangementAttachments_2_linkName', 'features_properties_arrangementAttachments_2_sizeInBytes', 'features_properties_arrangementAttachments_2_uniqueFileName', 'features_properties_arrangementAttachments_3_displayName', 'features_properties_arrangementAttachments_3_fileName', 'features_properties_arrangementAttachments_3_fileType', 'features_properties_arrangementAttachments_3_linkName', 'features_properties_arrangementAttachments_3_sizeInBytes', 'features_properties_arrangementAttachments_3_uniqueFileName', 'features_properties_arrangementElements_0_html', 'features_properties_arrangementElements_0_title', 'features_properties_arrangementElements_1_html', 'features_properties_arrangementElements_1_title', 'features_properties_arrangementElements_2_html', 'features_properties_arrangementElements_2_title','features_properties_attendingGroups_0','features_properties_subCategoryA', 'features_properties_subCategoryB', 'features_properties_webLinkName', 'features_properties_webLinkUrl', 'features_properties_webLinks_0_linkText', 'features_properties_webLinks_0_linkURL', 'features_type')
    
    # processed_data is the final data
    global fileCheck
    if fileCheck == False:
        with open(csv_file_path, 'w+') as f:
            writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for row in processed_data:
                for k in removed_e:
                    row.pop(k,None)
                writer.writerow(row)
    else:
        with open(csv_file_path, 'a+') as f:
            writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
            # writer.writeheader()
            for row in processed_data:
                for k in removed_e:
                    row.pop(k,None)
                writer.writerow(row)


    print ("[INFO] Completed writing csv file with %d columns" % len(header))


if __name__ == "__main__":
    url = "http://data.livetraffic.com/traffic/hazards/majorevent.json"

    response = urllib.urlopen(url)
    # load JSON file
    majorevent = json.loads(response.read())
    print("[INFO] URL checked")

    majorevent_time_mark = majorevent['lastPublished']
    print "[INFO] Received time stamp: ", majorevent_time_mark
    # majorevent_parsed = majorevent['features']
    with open('/tmp/MajorEvent_update_history.txt','a+') as majorevent_record:

        try:
            latest_time_mark = majorevent_record.readlines()[-1]
            print"[INFO] Current time stamp: ", latest_time_mark
        except:
            latest_time_mark = str(0000000000000)
            print"[INFO] No existing time stamp recorded"

        if int(majorevent_time_mark) != int(latest_time_mark[:13]):
            print "[INFO] New Data Arrived"
            majorevent_record.write( str(majorevent_time_mark)+'  @'+ strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'\n')

            # open a file for writing, default in C:
            mkdir_p('/tmp')

            global fileCheck
            fileCheck = os.path.isfile('/tmp/MajorEvent.csv')
            print "[INFO] CSV file exist: ", fileCheck

            JSONconvert('features', url, '/tmp/MajorEvent.csv') 
            print "[INFO] Updating finished"
        elif int(majorevent_time_mark) == int(latest_time_mark[:13]):
            print "[INFO] Abort, no new data"

        else:
            print "[ERROR] unexpected"