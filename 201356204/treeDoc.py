import os
import sys
import zlib
import gzip


###################### Global Variables ###########################

count = 1
indexTop = []
indexTop2 = []
linesList = []
path = '../Split/'
pathTitle = '../Title/'
counterL = 0
counter = 1
end = len(os.listdir("./output/")) + 1

def reinit():
	global count
	global indexTop
	global indexTop2
	global linesList
	global counterL
    	count = 1
    	indexTop = []
    	indexTop2 = []
   	linesList = []
    	counterL = 0


###################### Functions that help to create the tree structure for the index files ########################

def get500(indexPath):
	global count
	global linesList
	global indexTop
	with gzip.open(os.path.abspath(indexPath),'rb') as indexFile:
    		for line in indexFile:
			if(count%500 == 0):
				counter = str(count/500)
            			indexTop.append(fileWrite(counter,linesList))
            			linesList = []
        		linesList.append(line)
        		count += 1

def getLast():
	global count
	global linesList
	global indexTop
	if(len(linesList)!=0):
    		counter = str((count+500)/500)
    		indexTop.append(fileWrite(counter,linesList))
    		linesList = []

def makeLayers():
	global indexTop
	global indexTop2
	global count
	while(len(indexTop) > 20):
    		indexTop2 = []
    		indexList = []
    		count = 1
    		for i in indexTop:
       			if(count%20 == 0):
       				counter = str(count/20)
            			indexTop2.append(fileWriteL(counter,indexList))
            			indexList = []
        		indexList.append(i)
        		count += 1
    		if(len(indexList)!=0):
    			counter = str((count+20)/20)
        		indexTop2.append(fileWriteL(counter,indexList))
        		indexList = []
		global counterL
		counterL = counterL + 1
            	indexTop = indexTop2

def makeFirst():
	global indexTop2
	filePath = path + 'top'
	fileObj = open(os.path.abspath(filePath),"w")
	for i in indexTop2:
    		fileObj.write(i)
    		
def fileWriteL(counter,linesList):
	global counterL
	outputFileName = path + "L" + str(counterL) + counter 
    	outputFile = open(os.path.abspath(outputFileName),"w")
	firstLine = linesList[0][:-1].split(" ")[0] + " " + "L" + str(counterL) + counter + " NL\n"
	for line in linesList:
        	outputFile.write(line)
	return firstLine

def fileWrite(counter,linesList):
	outputFileName = path + counter
    	outputFile = open(os.path.abspath(outputFileName),"w")
    	firstLine = linesList[0][:-1].split(" ")[0] + " " + counter + " NL\n"
    	for line in linesList:
        	outputFile.write(line)
    	return firstLine

############################ Function that help in split the title files ####################################

def get500Title(titlePath):
    global count
    global linesList
    global indexTop
    with open(os.path.abspath(titlePath)) as titleFile:
            for line in titleFile:
            	if(count%500 == 0):
               		counter = str(count/500)
                        indexTop.append(fileWriteT(counter,linesList))
                        linesList = []
                linesList.append(line)
                count += 1

def getLastTitle():
    global count
    global linesList
    global indexTop
    if(len(linesList)!=0):
            counter = str((count+500)/500)
            indexTop.append(fileWriteT(counter,linesList))
            linesList = []

def makeLayersTitle():
    global indexTop
    global indexTop2
    global count
    if(len(indexTop) <= 200):
	    indexTop2 = indexTop
    while(len(indexTop) > 200):
    	indexTop2 = []
        indexList = []
        count = 1
        for i in indexTop:
        	if(count%200 == 0):
                	counter = str(count/200)
                    	indexTop2.append(fileWriteTL(counter,indexList))
                    	indexList = []
                indexList.append(i)
                count += 1
        if(len(indexList)!=0):
        	counter = str((count+200)/200)
                indexTop2.append(fileWriteTL(counter,indexList))
                indexList = []
    	global counterL
        counterL = counterL + 1
        indexTop = indexTop2

def makeFirstTitle():
    global indexTop2
    filePath = pathTitle + 'top'
    fileObj = open(os.path.abspath(filePath),"w")
    for i in indexTop2:
            fileObj.write(i)
            
def fileWriteTL(counter,linesList):
    global counterL
    outputFileName = pathTitle + "L" + str(counterL) + counter 
    outputFile = open(os.path.abspath(outputFileName),"w")
    firstLine = linesList[0][:-1].split(" ")[0] + " " + "L" + str(counterL) + counter + " NL\n"
    for line in linesList:
            outputFile.write(line)
    return firstLine

def fileWriteT(counter,linesList):
    outputFileName = pathTitle + counter
    outputFile = open(os.path.abspath(outputFileName),"w")
    firstLine = linesList[0][:-1].split(" ")[0] + " " + counter + " NL\n"
    for line in linesList:
    	outputFile.write(line)
    return firstLine

################# File Merge ###################################################################

def merge_files(file1,file2,out_file):
    with open(file1) as f1, open(file2) as f2:
        sources = [f1, f2]
        with open(out_file, "w") as dest:
            l1 = f1.next()
            l2 = f2.next()
            s1 = l1.split()
            s2 = l2.split()
            while(1):
                if(s1[0] < s2[0]):
                    dest.write(l1)
                    try:
                        l1 = f1.next()
                        s1 = l1.split()
                    except:
                        while(1):
                            try:
                                t2 = f2.next()
                                dest.write(t2)
                            except:
                                break
                        break
                elif(s1[0] > s2[0]):
                    dest.write(l2)
                    try:
                        l2 = f2.next()
                        s2 = l2.split()
                    except:
                        while(1):
                            try:
                                t1 = f1.next()
                                dest.write(t1)
                            except:
                                break
                        break
                else:
                    line = s1[0] + " " + s1[1] + "|" + s2[1]
                    dest.write(line + '\n')
                    try:
                        l1 = f1.next()
                        s1 = l1.split()
                    except:
                        while(1):
                            try:
                                t2 = f2.next()
                                dest.write(t2)
                            except:
                                break
                        break
                    try:
                        l2 = f2.next()
                        s2 = l2.split()
                    except:
                        dest.write(l1)
                        while(1):
                            try:
                                t1 = f1.next()
                                dest.write(t1)
                            except:
                                break
                        break

def merge_files_compression(file1,file2,out_file):
    with open(file1) as f1, open(file2) as f2:
        sources = [f1, f2]
        with gzip.open(out_file, 'wb') as dest:
            l1 = f1.next()
            l2 = f2.next()
            s1 = l1.split()
            s2 = l2.split()
            while(1):
                if(s1[0] < s2[0]):
                    dest.write(l1)
                    try:
                        l1 = f1.next()
                        s1 = l1.split()
                    except:
                        while(1):
                            try:
                                t2 = f2.next()
                                dest.write(t2)
                            except:
                                break
                        break
                elif(s1[0] > s2[0]):
                    dest.write(l2)
                    try:
                        l2 = f2.next()
                        s2 = l2.split()
                    except:
                        while(1):
                            try:
                                t1 = f1.next()
                                dest.write(t1)
                            except:
                                break
                        break
                else:
                    line = s1[0] + " " + s1[1] + "|" + s2[1]
                    dest.write(line + '\n')
                    try:
                        l1 = f1.next()
                        s1 = l1.split()
                    except:
                        while(1):
                            try:
                                t2 = f2.next()
                                dest.write(t2)
                            except:
                                break
                        break
                    try:
                        l2 = f2.next()
                        s2 = l2.split()
                    except:
                        dest.write(9)
                        while(1):
                            try:
                                t1 = f1.next()
                                dest.write(t1)
                            except:
                                break
                        break

def fileMerge():
    global counter
    global end
    while counter < end-1:
	if counter == end-2:
        	merge_files_compression('./output/output'+str(counter)+'.txt','./output/output'+str(counter+1)+'.txt','../Index/MyIndex')
        else:
        	merge_files('./output/output'+str(counter)+'.txt','./output/output'+str(counter+1)+'.txt','./output/output'+str(end)+'.txt')
	os.remove('./output/output'+str(counter)+'.txt')
        os.remove('./output/output'+str(counter+1)+'.txt')
        print counter,counter+1
        print end
        counter += 2
        end += 1



if __name__ == "__main__":
    	fileMerge()
############# Calling for indexer ###############
	get500(sys.argv[1])
	getLast()
	makeLayers()
	makeFirst()
############# Calling for title ################
	reinit()
	get500Title(sys.argv[2])
	getLastTitle()
	makeLayersTitle()
	makeFirstTitle()
