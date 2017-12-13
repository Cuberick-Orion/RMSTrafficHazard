The script to pull Live Traffic Data from RMS live source and record in csv files.

Please run record_all.py

Incident, Roadwork, MajorEvent data will be stored separately

Live Traffic Data is obtained in the form of JSON file from RMS API
[CHANGED] Files in this folder are updated automatically (and renamed so that each time the new files will overwrite the old ones), every time the program receives a new file, it processes it and copies it here to sync with DropBox

[NOTE!] The program cannot overwrite the old csv file with a new one if the old file is opened by Excel, and that will cause an error. If you plan to access the file (from Dropbox local synced folder) please first copy and paste it to somewhere else and open it. Thanks!

csv File name explanation:
First part: 
	Record type, e.g. Incident / Roadwork / MajorEvent

[DELETE]	Second part: 
[DELETE]		Program start time in Unix, e.g. 1512512349
[DELETE]		*to ensure file names are unique for each run, prevent unexpected file overwrite

[DELETE]	Third part:
[DELETE]		Number of update, this is counted when the program is running
[DELETE]		*to ensure file names are unique for each run, prevent unexpected file overwrite

Fourth part:
	processed
	indicate that this file has been post processed by PostProcess script
	files with "processed" in the name are the final version

Other files:
	*.change
	text file that records the changes made in each update
	-can be opened by text editors
	-records rows (events) that are updated (with new information / attributes received), and new rows (events) appended to the csv

	_cache file
	PLEASE DO NOT CHANGE THE CONTENT MANUALLY
	Python cache file, so that the program can read in previous recorded data when started

	_history.txt
	text file that records each update (currently the update frequency is every 15 min)
	content includes whether a new JSON file is received, if it is an old version that should be discarded (determined by timestamp in the filename)

Scripts:
	record_all.py

	The main script for pulling and recording data

	process.py

	The function that processes the csv files
	called by reocrd_all.py
	can also be executed separately for any chosen files/folders (when executed separately, GUI will allow user to choose files to process)
	-The Post Processing includes:
		Change the header (to avoid unclear attribution names)
		Convert Unix timestamp into readable format
		delete some useless columns
		↓
		For details please refer to the Live Traffic Developer Guide:
		https://opendata.transport.nsw.gov.au/sites/default/files/Live_Traffic_Data_Developer_Guide.pdf
