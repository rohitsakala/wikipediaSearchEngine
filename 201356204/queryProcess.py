import time
from nltk.corpus import stopwords
from nltk import PorterStemmer
import operator
import math
from binaryAlgo import *


############# Global variables ##################

topLines = ''
mapWeight = {}
N = 200000
titlePath = '../Title/'
indexPath = '../Split/'


def init():
	global topLines
	global mapWeight
	words = stopwords.words('english')
	stopwordDict = {}
	for i in words:
    		stopwordDict[i] = 1
    	topLines = open('../Split/top').readlines()
    	mapWeight = { "0":500.0 , "1":10.0 , "2":100.0 , "3":75.0 , "4":50.0 , "5":60.0}

def casefold(word):
	return word[0].lower()

def stopwordRemove(word,wordC,wordP):
	try:
		stopwordDict[word]
	except:
		nword = PorterStemmer().stem_word(word)
        wordP.append(nword)
        wordC.append("No")
        return [wordC,wordP]


def process(query):
    	wordP = []
    	wordC = []
	words = query.split(" ")
    	for word in words:
        	splitted = word.split(":")
        	if(len(splitted) == 1):
        		splitted = casefold(splitted)
      			temp = stopwordRemove(splitted,wordC,wordP)
      			wordC = temp[0]
      			wordP = temp[1]
        	else:
            		iword = splitted[1]
            		try:
            			stopwordDict[iword]
            		except:
            			nword = PorterStemmer().stem_word(iword)
            			wordP.append(nword)
        			wordC.append(splitted[0])
    	return [wordP,wordC]

def checkWord(temp,word,indexLines,lineCount):
	if(temp[0] <= word and indexLines[lineCount+1].split(" ")[0] > word):
    		indexLines = open(indexPath + temp[1]).readlines()
        	return indexLines
    	return 0

def checkWordTitle(temp,word,indexLines,lineCount):
    if(int(temp[0]) <= int(word) and int(indexLines[lineCount+1].split(" ")[0]) > int(word)):
            indexLines = open(titlePath + temp[1]).readlines()
            return indexLines
    return 0


def findDocument(word):
	global topLines
	indexLines = topLines
	while(indexLines[0].find('NL') != -1):
        	lineCount = 0
       		while (lineCount < (len(indexLines)-1)):
            		temp = indexLines[lineCount].split(" ")
            		check = checkWord(temp,word,indexLines,lineCount)
            		if(check != 0):
            			indexLines = check
            			break
            		lineCount += 1
        	if(lineCount == (len(indexLines)-1)):
        		indexLines = open(indexPath + indexLines[lineCount].split(" ")[1]).readlines()
    	return bSearch(indexLines,word,0,len(indexLines)-1)

def findDocumentTitle(word,root):
    indexLines = root
    while(indexLines[0].find("NL") != -1):
        lineCount = 0
        while (lineCount < (len(indexLines)-1)):
            temp = indexLines[lineCount].split(" ")
            check = checkWordTitle(temp,word,indexLines,lineCount)
            if(check != 0):
                indexLines = check
                break
            lineCount += 1
        if(lineCount == (len(indexLines)-1)):
            indexLines = open(titlePath + indexLines[lineCount].split(" ")[1]).readlines()
    temp = bSearchT(indexLines,word,0,len(indexLines)-1)
    return temp

def mapping(splittedList):
	counts = [0,0,0,0,0,0]
	i = 0
	while(i < len(splittedList)):
		if(splittedList[i] == "T"):
			counts[0] = counts[0]+ int(splittedList[i+1])
			i = i + 2
		elif(splittedList[i] == "X"):
			counts[1] = counts[1] + int(splittedList[i+1])
			i = i + 2
		elif(splittedList[i] == "I"):
			counts[2] = counts[2] + int(splittedList[i+1])
			i = i + 2
		elif(splittedList[i] == "C"):
			counts[3] = counts[3] + int(splittedList[i+1])
			i = i + 2
		elif(splittedList[i] == "L"):
			counts[4] = counts[4] + int(splittedList[i+1])
			i = i + 2
		elif(splittedList[i] == "R"):
			counts[5] = counts[5] + int(splittedList[i+1])
			i = i + 2
	return counts

def getCount(post):
    documentId = ""
    string = ""
    flag = 0
    for s in post:
   	if(s.isupper() and s.isalpha()):
   		string = string + " " + s + " "
   		flag = 1
   		continue
   	elif(flag == 0):
   		documentId = documentId + s
        if(flag == 1):
        	string = string + s
    # Removing first space
    string = string[1:]
    splittedList = string.split(" ")
    counts = mapping(splittedList)
    return [documentId,counts]

def weightCal(i,freqDocument,freqTerm,weight,doc,field,categories):
	global N
	if(categories[i] == "No"):
		weight += freqDocument[doc][field]*mapWeight[str(field)] * math.log(N/(freqTerm*1.0))
    	else:
    		if(categories[i] == "T"):
       		 	weight += freqDocument[doc][0]*mapWeight[str(field)] * math.log(N/(freqTerm*1.0))
	        elif(categories[i] == "X"):
        		weight += freqDocument[doc][1]*mapWeight[str(field)] * math.log(N/(freqTerm*1.0))
	        elif(categories[i] == "I"):
        		weight += freqDocument[doc][2]*mapWeight[str(field)] * math.log(N/(freqTerm*1.0))
	        elif(categories[i] == "C"):
       		 	weight += freqDocument[doc][3]*mapWeight[str(field)] * math.log(N/(freqTerm*1.0))
	        elif(categories[i] == "L"):
       		 	weight += freqDocument[doc][4]*mapWeight[str(field)] * math.log(N/(freqTerm*1.0))
	        elif(categories[i] == "R"):
        		weight += freqDocument[doc][5]*mapWeight[str(field)] * math.log(N/(freqTerm*1.0))
	return weight

def createRankDocument(i,postingList,categories):
	ranks = {}
	if(postingList != "NF"):
		postingList = postingList.split("|")
		## Removing new line
       		postingList[-1] = postingList[-1][:-1]
        	freqDocument = {}
        	freqTerm = 0
        	for post in postingList:
        		counts = getCount(post)
        		freqDocument[counts[0]] = counts[1] 
            		freqTerm = freqTerm + 1
            		for doc in freqDocument:
            			weight = 0
                		for field in range(len(freqDocument[doc])):
                			weight = weightCal(i,freqDocument,freqTerm,weight,doc,field,categories)
                		try:
                    			ranks[doc] += weight
               			except:
                    			ranks[doc] = weight
  		return ranks
  	return {}


def rank(words,categories):
	for i in range(len(words)):
		postingList = findDocument(words[i])
		ranks = createRankDocument(i,postingList,categories)
	try:
        	return ranks
    	except:
       		return -1


def inputProcess():
	n = input()
	while(n!=0):
		n = n -1
		query = raw_input()
        	start = time.clock()		
		processedQuery = process(query)
		words = processedQuery[0]
    		categories = processedQuery[1]
    		ranks = rank(words,categories)
    		if(ranks != -1):
        		top = open(titlePath + "top").readlines()
        		sorted_x = sorted(ranks.items(), key=operator.itemgetter(1),reverse = True)
        		if(len(sorted_x) == 0):
           			print "No documents found"
        		else:
           			count = 0
            		for i in range(len(sorted_x)):
                        	count += 1
                		if(count > 10):
                   			break
                		docID = sorted_x[i][0]
				print docID
                        	title = findDocumentTitle(docID,top)
                                print title[:-1]
    		else:
        		print "No documents found"
        	elapsed = (time.clock() - start)
        	print "%.2gs" %elapsed

if __name__ == "__main__":
####### Take input #######
	init()
	inputProcess()
	
