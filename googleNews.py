from __future__ import division
import nltk,re,pprint
from nltk.corpus import wordnet as wn
from nltk import word_tokenize
import urllib2
from bs4 import BeautifulSoup
import re
from nltk.wsd import lesk
def searchNews(searchWord):
	
	flag = 0
	#setting user agent and parsing google news for 15 news links
	userAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
	request = urllib2.Request('https://news.google.com/')
	request.add_header('User-Agent',userAgent)
	opener = urllib2.build_opener()
	web = opener.open(request).read()
	newsUrls = []
	googleNewsPage = BeautifulSoup(web)
	googleNewsArticle = googleNewsPage.find_all('a',class_ = re.compile('article-'))
	i=0
	for link in googleNewsArticle:
		if i < 14:
			newsUrls.append(link.get('href'))
			i=i+1

	#parsing each news link from google news
	print "Matching Words Found in the Following Urls "
	print
	for url in newsUrls:	
			
		sentance = []
		try:
			request = urllib2.Request(url)
			request.add_header('User-Agent',userAgent)
			opener = urllib2.build_opener()
			web = opener.open(request).read().decode('utf8')
		except:
			print "Exception Occured in opening the url. Skipping this url : " + url 
			continue
		
		#using beautiful Soup to get the text of html
		newsRaw = BeautifulSoup(web).get_text()
		
		#tokenizing html text using word_tokenize from nltk module

		tokens = word_tokenize(newsRaw)
		newsText = nltk.Text(tokens)
		
		#synWords = []

		#getting the synonyms of search word using word net
		#for i,syn in enumerate(wn.synsets(searchWord)):
			#for syn2 in syn.lemma_names():
				#synWords.append(syn2.encode('utf8'))

		#synWords = set(synWords)
		
		#checking weather search word in the news article	
		#for searchWord in synWords:
	
		if(searchWord in newsText):
		#if present prints the url and match found
			print
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" 
			print "News Url : " + url
			print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			print
			print "______________________________________________________________________________________________________________________"
			newsText.concordance(searchWord)
			print "______________________________________________________________________________________________________________________"
			sentanceStr = '';
			contextSentance = nltk.ConcordanceIndex(tokens, key = lambda s:s.lower())
			width = 75
			lines = 25
			half_width = (width - len(searchWord) -2) // 2
			context = width // 4
			offsets = contextSentance.offsets(searchWord)
			if offsets:
				lines = min(lines,len(offsets))
				for k in offsets:
					if lines <= 0:
						break
					left = (' ' * half_width + ' '.join(tokens[k-context:k]))
					right = ' '.join(tokens[k+1:k+context])
					left = left[-half_width:]
					right = right[:half_width]
					sentance.append(left+tokens[k]+right)
					lines -= 1
			
				sentanceStr = ' '.join(sentance)
				sentanceTokens = word_tokenize(sentanceStr)
				
				print "++++++++++++++++++++++++++++++++++++"
				print "+Meaning Of the Word in the context+"
				print "++++++++++++++++++++++++++++++++++++"
				print 
				print ','.join(lesk(sentanceTokens,searchWord).lemma_names())
				
				print
				print "+++++++++++++++++++"
				print "+ Parts Of Speech +"
				print "+++++++++++++++++++"
				print
				
				pos = nltk.pos_tag(sentanceStr.split())
				print pos
				for word,ps in pos:
					if (word.lower() == searchWord.lower()):
						print(str(word),str(ps))	
			flag = 1
	if flag == 0:
		print "No Match Found"
			
				
if __name__ == "__main__":
	
	#calling function search news
	print 
	print "============================"
	print "enter the word for searching"
	print "============================"
	print 
	searchWord = raw_input()
	searchNews(searchWord)
