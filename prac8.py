#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 10:49:19 2018

@author: charlotteviner
"""

import nltk
import requests
import time


# Read in "raw" text from the web.
url = "http://www.gutenberg.org/files/1321/1321-0.txt"
raw = requests.get(url).text


# Cut down the text.
start = "il miglior fabbro_"
start_pos = raw.find(start) + len(start) # Searches from the front of the text.
end_pos = raw.rfind("Line 415 aetherial] aethereal") # Searches from the end of the text.

raw = raw[start_pos:end_pos]


# Tokenize the text.
tokens = nltk.word_tokenize(raw)
text = nltk.Text(tokens)


# 20 most common words.
fdist = nltk.FreqDist(text)
#print(fdist.most_common(20))


# 20 most common word lengths.
fdist2 = nltk.FreqDist(len(w) for w in text)
#print(fdist2.most_common(20))


# All words over 10 letters long.
long_words = [w for w in text if len(w) > 10]
#print(long_words)


# Part-of-speech tagging across the text.
tagged = nltk.pos_tag(text)


sentences = []
sentence = []

for tag in tagged:
    sentence.append(tag)
    if tag[0] == ".":
        sentences.append(sentence)
        sentence = []
        continue

        
proper_nouns = []

# Pull out terms with NNP tag.
grammar = "ProperNouns: {<NNP>}"
chunkparser = nltk.RegexpParser(grammar)

for sentence in sentences:
    tree = chunkparser.parse(sentence)
    for subtree in tree.subtrees():
        if subtree.label() =='ProperNouns':
            st = str(subtree)
            slash = st.find("/")
            st = st[13:slash]
            #print(subtree)
            #print(st)
            if st.isupper() == False and st.isalpha() == True:
                proper_nouns.append(st)
                
print(proper_nouns)



# Using Python requests and the Google Maps Geocoding API.
#
# References:
#
# * http://docs.python-requests.org/en/latest/
# * https://developers.google.com/maps/

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

for noun in proper_nouns[5:15]: # Only looking at 10 items in proper nouns.
    params = {
        'address': noun,
        'key': 'INSERT API KEY HERE'
    }

    # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    time.sleep(1)

    if len(res['results']) == 0:
        print('results empty')
    else:
        result = res['results'][0]
        #print('result: ')
        #print(result)
        
        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']
        
        print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
  