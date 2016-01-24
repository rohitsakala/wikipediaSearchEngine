# -*- coding: utf-8 -*-
#!/usr/bin/python

import xml.sax
import sys
import re
import os
import nltk
from nltk.corpus import stopwords
from nltk import PorterStemmer
import Stemmer
from unidecode import unidecode
from datetime import datetime
import unicodedata


################# Global Variables #######################################

output = open("./index","w")
fileName = "./output/output"
stemmer = Stemmer.Stemmer( 'english')
codex = ['À','Á','Â','Ã','Ä','Å','à','á','â','ã','ä','å','È','É','Ê','Ë','é','ê','â','à','é']
indexCount = 0
fileCounter = 0
counter = 1
end = len(os.listdir("./output/")) + 1

################# Function to load file call SAX handler #################

def load(dataFile):
	dataFile = open(dataFile)
	xml.sax.parse(dataFile, dataContentHandler())

################# Class to handle the wiki data dump #####################

class dataContentHandler(xml.sax.ContentHandler):
	
	def __init__(self):
		self.tag = ""
		self.documentId = ""
		self.regex = re.compile(r'[a-zA-Z]+')
		self.docMap = {}														# For mapping documentId and count
		self.docTitle = {}
		self.dic = {}
		self.stopWords = {}
		self.getStopWords()
		self.temp = 0
		self.pageTag = 0
	
	def startElement(self, tag, attributes):
		self.tag = tag
		if(self.tag == 'page'):
			self.title = []
			self.text = []
			self.externalLinks = []
			self.references = []
			self.categories = []
			self.infoBox = []
			self.pageTag = 0
			self.infoBoxTag = 0
			self.externalLinksTag = 0
			self.referencesTag = 0
			self.categoriesTag = 0
		if(self.tag == 'title'):
			self.pageTag = 1

	def characters(self, data):
		#data = data.encode(encoding='UTF-8', errors='strict')					# Converting unicode into utf-8
		data = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
		data = data.strip()														# Stripping leading and trailing characters
		if(self.tag == 'page'):													# Handler for external tags
			if(self.externalLinksTag != 0):
				if(len(data) == 0):
					self.externalLinksTag = 0
					return
			if(self.referencesTag != 0):
				if(len(data) == 0):
					self.referencesTag = 0
					return
		if(len(data) == 0):	
			return
		if(self.tag == 'title'):												# Getting title 
			self.title.append(data.lower())  									# Case folding implemented
		elif(self.tag == 'id' and self.pageTag == 1):
			self.documentId = data
			self.docTitle[str(format(int(self.documentId),'02x'))] = self.title	# Converting count into Hexadecimal for optimization
			self.pageTag = 0
		elif(self.tag == 'text'):
			self.infoBoxTag = self.checkInfoBox(data)							# Checking for required fields
			self.externalLinksTag = self.checkExternalLinks(data)
			self.referencesTag = self.checkReferencesTag(data)
			self.categoriesTag = self.checkCategoriesTag(data)

			if(self.categoriesTag == 1):
				self.categories.append(data[11:-2].lower())						# Case folding implemented
			elif(self.infoBoxTag == 1):
				if(data.find("{{Infobox") != -1):
					self.infoBox.append(data[9:].lower())						# Case folding implemented
				else:
					self.infoBox.append(data.lower())
			elif(self.externalLinksTag == 1):
				if(data.find("==External links==") == -1):
					if(data[0] == '*'):
						self.externalLinks.append(data.lower())
			elif(self.referencesTag == 1):
				if(data.find("==References==") == -1):
					self.references.append(data.lower())
			else:
				self.text.append(data.lower())

	def get_val(self,field,count):
		if(int(count) == 0):
			return ""
		else:
			#return field + str(format(int(count),'02x'))
			return field + str(count)

	def endElement(self, tag):
		self.tag = tag
		if(self.tag == 'page'):
			self.createPostingList(self.title,0)
			self.createPostingList(self.text,1)
			self.createPostingList(self.infoBox,2)
			self.createPostingList(self.categories,3)
			self.createPostingList(self.externalLinks,4)
			self.createPostingList(self.references,5)
			if(sys.getsizeof(self.dic) > 1000*1000 ):
                		global indexCount
		                indexCount += len(self.dic.keys())
		                self.fileWrite()
				self.dic = {}
		elif(self.tag == 'mediawiki'):
		    indexCount += len(self.dic.keys())
		    print indexCount
		    self.fileWrite()	
		    self.dic = {}
		    
################# Functions's that help to write to files and merge them #####################

	def fileWrite(self):
        	global fileCounter
	        fileCounter += 1
        	f = fileName+str(fileCounter)+".txt"
	        output = open(f,"w+")
       		word = ""
		for f in sorted(self.dic):
			word = f + " "
			for g in self.dic[f]:
				word += str(format(int(g),'02x'))							# Converting count to hexadecimal for optimization
				#word += str(self.docMap[g])
				word += self.get_val("T",self.dic[f][g][0])
				word += self.get_val("X",self.dic[f][g][1])
				word += self.get_val("I",self.dic[f][g][2])
				word += self.get_val("S",self.dic[f][g][3])
				word += self.get_val("K",self.dic[f][g][4])
				word += self.get_val("R",self.dic[f][g][5])
				word += "|"
			word = word[:-1]
			output.write(word+"\n")	
		output.close()

	
################ Functions's that help to check fields in text tag ###########################
	
	def checkCategoriesTag(self,data):
		if(data.find("[[Category:") != -1):
			return 1
		else:
		 	return 0

	def checkInfoBox(self,data):
		if(self.infoBoxTag == 0):
			if(data.find("{{Infobox") != -1):
				return 1
			else:
				return 0
		else:
			if(data == "}}"):
				return 0
			else:
				return 1

	def checkExternalLinks(self,data):
		if(self.externalLinksTag == 0):
			if(data.find("==External links==") != -1):
				return 1
			else:
	 			return 0
	 	else:
	 		if(data.startswith("==")):
	 			return 0
	 		else:
	 			return 1	

	def checkReferencesTag(self,data):
		if(self.referencesTag == 0):
			if(data.find("==References==") != -1):
				return 1
			else:
		 		return 0
		return 1

############### Function's that help in creating data structures for index creation ###########
	
	def getStopWords(self):
		stopWords = stopwords.words('english')
		for i in stopWords:
			self.stopWords[i] = 1

	def createPostingList(self, data, index):
		for a in data:
			#tokens =  self.regex.findall(a)
			tokens = tokenise(a)												# Removing any special characters
			tokensList = []
			for b in tokens:													# Removing stop words
				try:
					self.stopWords[b]
				except:
					final_val = b.strip('~`!@#$%^&*()_+=-\\|\"\';:/?.,')
					if len(final_val) > 0:
						if "-" in final_val:
							if bool(re.match('^[0-9]{1,4}-([0-9]{1,4})-([0-9]{1,4})$',final_val)):
								tokensList.append(final_val)
						else:
							tokensList.append(final_val)
			for c in tokensList:
				#rootWord = PorterStemmer().stem_word(c)						# Getting the root word
				rootWord = str(stemmer.stemWord(c))
				try:
					self.dic[c][self.documentId]
					self.dic[c][self.documentId][index] += 1
				except:
					try:
						self.dic[c]
						self.dic[c][self.documentId] = [0,0,0,0,0,0]
						self.dic[c][self.documentId][index] = 1
					except:
						self.dic[c] = {}
						self.dic[c][self.documentId] = [0,0,0,0,0,0]
						self.dic[c][self.documentId][index] = 1
			
################# Functions that tokenizer the text ############################################

def tokenise(query):
	regWhiteSpace = re.compile(u"[\s\u0020\u00a0\u1680\u180e\u202f\u205f\u3000\u2000-\u200a]+")
	query = regWhiteSpace.sub(" ", query).strip()	
#	regex = re.compile(r'[a-zA-Z0-9]+')
	query = re.sub('[:|\\|/|=|?|!|~|`|!|@|#|$|%|^|&|*|(||)|_+.\\|-|{|}|\[|\]|;|\"|\'|<|>|,|]',' ',query)
	query = re.sub(r'-(-+)|/(/+)',' ',query)
	query = re.sub(' \S ',' ',query)
	query = query.split()
	return query

if __name__ == "__main__":
	startTime = datetime.now()
	load(sys.argv[1]) 															# Loading the dump 
	print datetime.now() - startTime
