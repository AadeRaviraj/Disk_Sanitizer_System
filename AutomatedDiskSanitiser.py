# =======================================================
# Program : Automated Disk Sanitizer
# Author  : Raviraj Aade 
# Purpose : Delete Duplicate files using Python Checksum
# =======================================================


import hashlib
import os
import sys
import schedule
import time

# Calculate File Checksum using Md5(hashing) Algorithm
def CalculateChecksum(FileName):
    fobj = open(FileName, "rb")
    
    hobj = hashlib.md5()
    
    Buffer = fobj.read(1024)
    
    while len(Buffer) > 0 :
        hobj.update(Buffer)
        Buffer = fobj.read(1024)
    
    fobj.close()
    return hobj.hexdigest()


def FindDuplicate(Directoryname):
    ret = False
    ret =  os.path.exists(Directoryname)
    
    if ret == False:
        print("There is no such directory ")
        return
    
    ret = os.path.isdir(Directoryname)
    
    if ret == False:
        print("it is not a directory ")
        return
    
    Duplicate = {}
    
    for FolderName , SuBfolderName, FileName  in os.walk(Directoryname):        
        for fname  in FileName:
            
            fname = os.path.join(FolderName, fname)
            CheckSum = CalculateChecksum(fname)
            
            if CheckSum in Duplicate:
                Duplicate[CheckSum].append(fname)
            else:
                Duplicate[CheckSum] = [fname] 
    
    return Duplicate
        

def DisplayResult(Mydict):
    result = list(filter(lambda x: len(x)> 1, Mydict.values()))
    
    Count = 0 
    
    for value in result:
        for subValue in value:
            Count = Count + 1
            print(subValue)
        print("Value of Count is : ", Count)
        Count = 0 

def DeleteDuplicate(Path): # demo is directory name
    
    MyDict = FindDuplicate(Path)
    # print(MyDict)
    result = list(filter(lambda x: len(x)> 1, MyDict.values()))
 
    Count = 0 
    Cnt = 0  
    deletedfiles =[]
    for i in result:
        print(i)
    if result and (result[0] or len(result) > 1) :
            
        for value in result: 
            for subValue in value: 
                Count = Count + 1 
                if Count > 1:
                    
                    print("Deleted File : ", subValue)
                    os.remove(subValue)
                    deletedfiles.append(subValue)
                    Cnt = Cnt + 1
            Count = 0
        print("Total Deleted  Files : ", Cnt) 
    else:
        print("No Duplicate File found")  
        deletedfiles = None
    return deletedfiles, Cnt     



def CreateLog(FolderName):
    LogFolder = "LogFile"
    Border = "-" * 60
    Ret = False
    Ret = os.path.exists(LogFolder)
    
    if Ret == True:
        Ret = os.path.isdir(LogFolder)
        if Ret == False:
            print("Unable to create folder")
            return
    else:
        os.mkdir(LogFolder)
        print("Directory For log files get created successfully")
            
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    FileName = os.path.join(LogFolder,"LogFile%s.log" %timestamp)
    

    print("Log file gets created with name :",FileName)
    
    fobj = open(FileName,"w")
    fobj.write(Border+"\n")
   
    fobj.write("--------------------   Disk Sanitizer System ---------------\n")
    fobj.write("Log created at : "+time.ctime() + "\n")
    
    fobj.write(Border+"\n\n")
    
    fobj.write("---------------------- System Report ----------------------- \n")
        
    filelist =[]
    filename,NoOfFiles= DeleteDuplicate(FolderName)
    print(filename)
    fobj.write("No of file delete : " + str(NoOfFiles) + "\n")
    if filename is None:
        fobj.write("No Duplicate file found." + "\n")
    else:
        for i in filename:
            filelist.append(i)
        
        fobj.write("Name of deleted file :" + str(filelist) + "\n")
    
    fobj.write(Border+"\n")
    fobj.write("---------------------- End of log file ---------------------\n")
    fobj.write(Border+"\n")
    




def main(): 
    
    if( len(sys.argv) != 2):
        print("Invalid number of arguments ")
        print("Please specify the name of directory ")
        return
    schedule.every(1).minute.do(CreateLog,sys.argv[1])
    
    while True:
        schedule.run_pending()
        time.sleep(2)
    # DeleteDuplicate("Demo")
    
if __name__ == "__main__":
    main()