#DRONE SWEETIE: a Twitter bot that tweets descriptions of images of drones
#Code sources -- 
#Bing Search API Python Wrapper https://github.com/xthepoet/pyBingSearchAPI
#Script that fetches image descriptions from Toronto Deep Learning https://github.com/cmyr/INTERESTING_JPG

#STEPS TO RUN THIS CODE:
#1. create a virtual environment in your project directory
#2. install  textblob, requests and beautiful soup to your virtual env
#3. run dronesweetie.py with a sys.argv input from the command line
#4. make sure the following two modules are in your project directory (+download them with the following links):
#		Bing Search API Python Wrapper: https://www.dropbox.com/s/hlk4tcfims5no3z/bing_search_api.py?dl=0
#		Scraping Toronto Deep Learning: https://www.dropbox.com/s/9j0miitbwpgf4zh/cvserver.py?dl=0

import sys
import random
import urllib									#import urllib to download images from their URLs	
import time 									#to implement delays in making requests to Toronto Deep Learning
from textblob import TextBlob, Word				#import the class TextBlob from textblob, Word to get definitions
from bing_search_api import BingSearchAPI 		#import the class BingSearchAPI from https://github.com/xthepoet/pyBingSearchAPI
from cvserver import response_for_image, captions, nearest_neighbour	#import the function response_for_image to fetch image descriptions, caption to extract them from HTML using beautiful soup

#MY FUNCTONS
def fix_punctuation(sentence):			#pass in a string to fix the punctuation
	return sentence.replace(' .', '').replace(' , ', ', ')
	
#INFO FOR BING API
my_key = "insert_API_key"	#replace with Bing API Key
query_string = sys.argv[1]	#get query string as input from command line using sys.argv, for multiple words use query between " "
bing = BingSearchAPI(my_key)

#parameters for image searching -- more documentation on params and image filters here http://goo.gl/xG0v0O
params = {'ImageFilters':'"Style:Photo"',
          '$format': 'json',	#specifies format of data response
      	  '$top': 400,			#specifies number of results to return, default is 50
          '$skip': 0}			#specifies starting point offset for the results
          
#bing.search()requires sources first (images, web, video, etc.), then query string, then rest of params (above)
#full schema documentation for bing API is here http://goo.gl/xG0v0O
results = bing.search('image',query_string,params).json() 	#requests 1.0+ 

image_list = results['d']['results'][0]['Image']	#this gets us to the list of all the images

#create a new list of all the image source URLs using a list comprehension
image_urls = [image['MediaUrl'] for image in image_list if len(image['MediaUrl']) > 0]
for url in image_urls:	#print the list of image urls
	print url
# 
# # #download all those images to a directory (so i have them) -- only do this if you need the images, takes a lot of time
# # for url in image_urls:
# # 	file_name = url.rsplit('/',1)[1]
# # 	urllib.urlretrieve(url, file_name)
# 
# 
# #for each image, get the 5-sentence image description from Toronto Deep Learning using the response_for_image function and captions
# clientname = 'DRONESWEETIE'	#define the client name with some unique name, required part of cvserver.py
# all_descriptions = list()	#create a list that will hold all of the descriptions for all the image
# 
# #if i want to slice the list of image_urls (to get under 50 results), this is the number of images to put into the deep learning
# #then slice the list in the for loop, ie "for url in image_urls[:response_num]:
# # response_num = 30			
# 
# #GET TOP SENTENCE FOR EACH IMAGE USING NEAREST NEIGHBOUR FUNCTION, ADD IT TO THE LIST OF ALL DESCRIPTIONS
# for url in image_urls:		#for each image URL get the nearest neighbour
# 	raw_text = response_for_image(url, clientname)
# 	top_sentence = nearest_neighbour(raw_text)	#return a list of all the 5-sentence descriptions for each image
# 	if top_sentence is not None:
# 		all_descriptions.append(top_sentence)	#add the top sentences to the list of all descriptions
# 		print top_sentence						#print the sentence as it loads
# 	time.sleep(random.uniform(1.2, 4.75))  	#put in a random delay between requests
# 
# #GET 5 SENTENCE CAPTIONS FOR EACH IMAGE USING CAPTIONS FUNCTION, ADD IT TO THE LIST OF ALL DESCRIPTIONS
# for url in image_urls:		#for each image URL get the list of 5 captions
# 	raw_text = response_for_image(url, clientname)
# 	description = captions(raw_text)	#return a list of all the 5-sentence descriptions for each image
# 	if description is not None:		#make sure the description is not of type None
# 		for each_description in description: #then loop over the list
# 			if len(each_description) > 0:	#only add items to the list if they're not a line break, NOT WORKING FIGURE OUT NEW WAY
# 				all_descriptions.append(each_description)
# 		print description	#print out the individual description as it loads
# 	time.sleep(random.uniform(0.4, 0.75))  	#put in a random delay between requests
# 
# 
# #PRINT OUT A LIST OF ALL MY TEXT FROM THE LIST ALL_DESCRIPTIONS -- this raw outpu twill be my source text for the bot
# for description in all_descriptions:
# 	description = description.strip()	#strip the line breaks
# 	print fix_punctuation(description)[:140]	#print first 140 chars of each description as a string with corrected punctuation