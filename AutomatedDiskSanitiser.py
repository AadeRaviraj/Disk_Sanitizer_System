# =======================================================
# Program : Automated Disk Sanitizer
# Author  : Raviraj Aade
# Purpose : Delete Duplicate files using Python Checksum
# Date    : 11/02/2026
# =======================================================


import hashlib
import os
import sys
import schedule
import time


#-----------------------------------------------------------------------------------------------------
#   Function name :  CalculateChecksum
#   Description :    Calculates the MD5 checksum (hash) of a given file.
#                    Reads the file in 1KB chunks to handle large files efficiently
#                    without loading the entire file into memory at once.
#                    The resulting hash is used to uniquely identify file contents —
#                    two files with the same hash have identical content (duplicate).
#   Parameter :      FileName -> Full path of the file to calculate checksum for (string)
#   Return :         MD5 hex digest string representing the file's checksum
#   Date :           11/02/2026
#   Author:          Raviraj Aade
#----------------------------------------------------------------------------------------------------

def CalculateChecksum(FileName):

    # Open the file in binary mode for accurate hashing of all file types
    fobj = open(FileName, "rb")

    # Create an MD5 hash object
    hobj = hashlib.md5()

    # Read the file in 1KB chunks
    Buffer = fobj.read(1024)

    # Keep reading and updating the hash until the entire file is processed
    while len(Buffer) > 0:
        hobj.update(Buffer)
        Buffer = fobj.read(1024)

    fobj.close()

    # Return the final hex digest (unique fingerprint of the file)
    return hobj.hexdigest()


#-----------------------------------------------------------------------------------------------------
#   Function name :  FindDuplicate
#   Description :    Scans a given directory recursively and groups files by their MD5 checksum.
#                    Files that share the same checksum have identical content and are duplicates.
#                    Stores results in a dictionary where:
#                      Key   -> MD5 checksum string
#                      Value -> List of file paths that share that checksum
#   Parameter :      Directoryname -> Name or path of the directory to scan (string)
#   Return :         Duplicate -> Dictionary of {checksum : [list of file paths]}
#                    Returns None if the directory does not exist or is not valid
#   Date :           11/02/2026
#   Author:          Raviraj Aade
#----------------------------------------------------------------------------------------------------

def FindDuplicate(Directoryname):

    # Check if the given path exists
    ret = os.path.exists(Directoryname)

    if ret == False:
        print("There is no such directory ")
        return

    # Check if the given path is actually a directory
    ret = os.path.isdir(Directoryname)

    if ret == False:
        print("It is not a directory ")
        return

    # Dictionary to group files by their checksum
    Duplicate = {}

    # Walk through all files inside the directory and its subfolders
    for FolderName, SubFolderName, FileName in os.walk(Directoryname):
        for fname in FileName:

            # Get the full file path
            fname = os.path.join(FolderName, fname)

            # Calculate the MD5 checksum of the file
            CheckSum = CalculateChecksum(fname)

            # Group files with the same checksum together
            if CheckSum in Duplicate:
                Duplicate[CheckSum].append(fname)
            else:
                Duplicate[CheckSum] = [fname]

    return Duplicate


#-----------------------------------------------------------------------------------------------------
#   Function name :  DisplayResult
#   Description :    Displays all duplicate file groups found in the scanned directory.
#                    Filters the dictionary to show only groups that have more than one file
#                    (i.e. actual duplicates) and prints each file path along with a count.
#   Parameter :      Mydict -> Dictionary of {checksum : [list of file paths]} returned
#                              by FindDuplicate()
#   Return :         None
#   Date :           11/02/2026
#   Author:          Raviraj Aade
#----------------------------------------------------------------------------------------------------

def DisplayResult(Mydict):

    # Filter only groups that have more than one file — these are the duplicates
    result = list(filter(lambda x: len(x) > 1, Mydict.values()))

    Count = 0

    for value in result:
        for subValue in value:
            Count = Count + 1
            print(subValue)
        print("Value of Count is : ", Count)
        Count = 0


#-----------------------------------------------------------------------------------------------------
#   Function name :  DeleteDuplicate
#   Description :    Finds all duplicate files in a given directory and deletes the extra copies.
#                    For each group of duplicate files, the first file is kept as the original
#                    and all subsequent copies are permanently deleted using os.remove().
#                    Returns the list of deleted file paths and the total count of deletions.
#   Parameter :      Path -> Name or path of the directory to scan and clean (string)
#   Return :         deletedfiles -> List of file paths that were deleted
#                    Cnt          -> Total number of files deleted (integer)
#   Date :           11/02/2026
#   Author:          Raviraj Aade
#----------------------------------------------------------------------------------------------------

def DeleteDuplicate(Path):

    # Find all duplicate file groups in the given directory
    MyDict = FindDuplicate(Path)

    # Filter only groups with more than one file (actual duplicates)
    result = list(filter(lambda x: len(x) > 1, MyDict.values()))

    Count = 0
    Cnt   = 0
    deletedfiles = []

    for i in result:
        print(i)

    if result and (result[0] or len(result) > 1):

        for value in result:
            for subValue in value:
                Count = Count + 1

                # Keep the first file (original), delete all subsequent duplicates
                if Count > 1:
                    print("Deleted File : ", subValue)
                    os.remove(subValue)
                    deletedfiles.append(subValue)
                    Cnt = Cnt + 1

            # Reset counter for the next duplicate group
            Count = 0

        print("Total Deleted Files : ", Cnt)

    else:
        print("No Duplicate File found")
        deletedfiles = None

    return deletedfiles, Cnt


#-----------------------------------------------------------------------------------------------------
#   Function name :  CreateLog
#   Description :    Creates a timestamped log file inside the 'LogFile' folder after each
#                    scheduled run. The log records the date/time of the run, the number of
#                    duplicate files deleted, and the names of all deleted files.
#                    If the 'LogFile' folder does not exist, it creates it automatically.
#                    This function also calls DeleteDuplicate() internally to perform the
#                    actual cleanup and capture the results for logging.
#   Parameter :      FolderName -> Name of the directory to scan and sanitize (string)
#   Return :         None
#   Date :           11/02/2026
#   Author:          Raviraj Aade
#----------------------------------------------------------------------------------------------------

def CreateLog(FolderName):

    LogFolder = "LogFile"
    Border = "-" * 60

    # Check if the LogFile folder already exists
    Ret = os.path.exists(LogFolder)

    if Ret == True:
        # Confirm it is a directory and not a file with the same name
        Ret = os.path.isdir(LogFolder)
        if Ret == False:
            print("Unable to create folder")
            return
    else:
        # Create the LogFile folder if it does not exist
        os.mkdir(LogFolder)
        print("Directory for log files created successfully.")

    # Generate a unique log file name using current timestamp
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    FileName  = os.path.join(LogFolder, "LogFile%s.log" % timestamp)

    print("Log file created with name :", FileName)

    # Open the log file for writing
    fobj = open(FileName, "w")

    # Write the log file header
    fobj.write(Border + "\n")
    fobj.write("--------------------   Disk Sanitizer System ---------------\n")
    fobj.write("Log created at : " + time.ctime() + "\n")
    fobj.write(Border + "\n\n")
    fobj.write("---------------------- System Report ----------------------- \n")

    # Run the duplicate deletion and capture the results
    filelist = []
    filename, NoOfFiles = DeleteDuplicate(FolderName)

    print(filename)

    # Write deletion summary to the log
    fobj.write("No of files deleted : " + str(NoOfFiles) + "\n")

    if filename is None:
        # No duplicates were found in this run
        fobj.write("No Duplicate file found." + "\n")
    else:
        # Write the names of all deleted files to the log
        for i in filename:
            filelist.append(i)
        fobj.write("Name of deleted files : " + str(filelist) + "\n")

    # Write the log file footer
    fobj.write(Border + "\n")
    fobj.write("---------------------- End of log file ---------------------\n")
    fobj.write(Border + "\n")

    fobj.close()


#-----------------------------------------------------------------------------------------------------
#   Function name :  main
#   Description :    Entry point of the Automated Disk Sanitizer application.
#                    Reads the target directory name from command-line arguments.
#                    Schedules the CreateLog() function to run automatically once every day.
#                    Keeps the script running using an infinite loop so the scheduler
#                    can trigger the cleanup at the defined daily interval.
#   Usage        :   python AutomatedDiskSanitiser.py Demo
#   Parameter :      None (reads from sys.argv)
#   Return :         None
#   Date :           11/02/2026
#   Author:          Raviraj Aade
#----------------------------------------------------------------------------------------------------

def main():

    # Validate command-line arguments — exactly one directory name must be provided
    if len(sys.argv) != 2:
        print("Invalid number of arguments ")
        print("Please specify the name of directory ")
        return

    # Schedule the cleanup to run automatically once every day
    schedule.every(1).day.do(CreateLog, sys.argv[1])

    # Keep the script alive so the scheduler can trigger at the right time
    while True:
        schedule.run_pending()
        time.sleep(2)


if __name__ == "__main__":
    main()