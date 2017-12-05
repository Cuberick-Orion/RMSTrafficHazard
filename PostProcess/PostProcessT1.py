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
from tkFileDialog import askopenfilename


def get_dir():
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    cwd = os.getcwd()
    return cwd

def choose_file():
    print "Choose a specific file (file name end with .csv), or press [Cancel] to iterative every file found in this directory"
    # IterativeFiles = raw_input('Choose a specific file (file name end with .csv), or press [ENTER] to iterative every file found in this directory')
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    if filename != "":
        # print("File chosen: ", filename)
        pass
    else:
        print "Choose every file in the directory"
    return filename

def process(file):
    with open(file, 'rb') as f:
        
if __name__ == "__main__":
    filePath = get_dir()
    fileName = []
    print "csv Files within the directory:"; print(glob.glob(filePath + "/*.csv")); print "\n"
    UserChoice = choose_file()
    if UserChoice == '':
        os.chdir(filePath)
        for ff in glob.glob("*.csv"):
            fileName.append(filePath +  "\\" + ff)
            print "File added: ", filePath +  "\\" + ff
    else:
        fileName.append(UserChoice)
        print "File added: ", UserChoice

    # fileName contains every file directory to be processed
    for f in fileName:
        process(f)









    input()
    