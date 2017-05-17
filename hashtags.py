# -*- coding: utf-8 -*-

import os, textwrap
from prettytable import PrettyTable
from prettytable import ALL as ALL


path = raw_input("\nPlease input full directory of files to be analysed:\n")
hashtags = {}
docsOfHashtags = {}
punctuation = ['!', '?', '.', ',', ':', ';', '"', '-']

""" Function to split body of text into sentences and remove newline characters. 
    Splits at instance of full-stop, exclamation point or question mark.
    Care needed for abbreviations... """
    
def splitter(text):
    sentences = []
    n = 0
    acronym = False
    for i in range(len(text)):
        if text[i] == '.' or (text[i] == '?' and text[i-1] != ' ') or text[i] == '!':
            
            " Skip to next character if the word is an acronym "
            try:
                if text[i-2] =='.' and text[i] == '.' and text[i+1] not in '?.!':
                    continue
                
            except IndexError:
                pass
            
            " Add exception for extra space at beginning of sentence "
            if text[n] != ' ':
                sentence = text[n:i+1]
            else:
                sentence = text[n+1:i+1]
            
            try:
                " If there are multiple full stops, include them all in the sentence "
                while text[i+1] == '.':
                    sentence += '.'
                    i += 1
                 
                
                " Skip to next character if full stop is not the end of the sentence -> acronym "
                if text[i] == '.' and text[i+1] not in ' "?!' and text[i+1] != "'":
                    continue
                    
                " Add speech marks/single quotations if they follow the end of the sentence "
                if text[i+1] == '"':
                    sentence += '"'
                    i += 1
                if text[i+1] == "'":
                    sentence += "'"
                    i += 1
            except IndexError:
                pass
            
            " Add sentence to list of sentences "
            sentences.append(sentence)
            n = i + 1
            
    return sentences


" Cycle through files in the directory given by the user "
for filename in os.listdir(path):
    
    " Split file text up into list of sentences "
    with open(path + '/' + filename, 'r') as file:
        fulltext = file.read()
        fulltext = fulltext.decode('utf8')
        
        " Remove line breaks and dodgy characters "
        fulltext = fulltext.replace('\n',' ')
        fulltext = fulltext.replace("\\'","'")        
        fulltext = fulltext.replace(u'\u201c', '"')
        fulltext = fulltext.replace(u'\u201d', '"')
        fulltext = fulltext.replace(u'\u2013', '-')
        fulltext = fulltext.replace(u'\u2014', '--')
        fulltext = fulltext.replace(u'\u2018', "'")
        fulltext = fulltext.replace(u'\u2019', "'")
        fulltext = fulltext.replace(' ? ', ' - ')
        fulltext = fulltext.replace("''", '"')
        


        " Split text into sentences "
        sentences = splitter(fulltext)
        
        " Split sentences into words"
        for sentence in sentences:
            words = sentence.split(' ')
            
            for word in words:
                " Remove punctuation from the end of the word if present, unless part of abbreviation "
                last = len(word) - 1
                if last > 1:
                    while word[last] in punctuation and word[last] != word[1]:
                        word = word[0:last]
                        last -= 1
                
                " Skip word if the word is just an isolated punctuation mark "
                if word in punctuation:
                    continue
                
                " Remove speech marks if present at start or end of word "
                if word.startswith('"'):
                    word = word[1:]
                if word.endswith('"'):
                    word = word[:-1]
                    
                " Make word lower case to catch all instances of word, case need not be matched"
                word = word.lower()
                
                " Add sentence & filename to respective sets if hashtags & docsOfHashtags dictionary entries for word already exist "
                " Otherwise create hashtags & docsOfHashtags dictionary entries for word "
                if word in hashtags:
                    hashtags[word].add(sentence)
                    docsOfHashtags[word].add(filename)
                else:
                    hashtags[word] = set([sentence])
                    docsOfHashtags[word] = set([filename])
                    



while True:
    
    " -------GIVE USER THE OPTION OF TWO DIFFERENT TYPES OF TABLE------- "
    tableOrLookup = raw_input('\nTo display a table of hashtags, enter "Table". To lookup a word, enter "Lookup". To exit, type "Exit".\n')
    
    " -------CREATE AND PRINT ONE OF THE TABLE TYPES------- "
    if tableOrLookup.lower() == 'table':
        print '\nEnter "Occurrences" to see a table of 3 columns: hashtags, the files they are present in and the number of occurrences.'
        print 'Enter "Sentences" to see a table of 3 columns: hashtags, the files they are present in and the sentences they are present in.\n'
        displayType = raw_input('Occurrences or Sentences?\n')


        " -------ENTER MINIMUM OCCURRENCES OF HASHTAGS TO BE DISPLAYED AND CREATE OCCURRENCES TABLE------- "
        if displayType.lower() == 'occurrences':
            minimumOccurences = raw_input('\nEnter minimum number of occurrences for a hashtag to display:\n')
            minimumOccurences = int(minimumOccurences)
            occurrencesTable = PrettyTable()
            occurrencesTable.hrules = ALL
            occurrencesTable.field_names = ['Word','Documents','Number of Occurrences']
            occurrencesTable.align = 'l'
        
        
        " -------ENTER NUMBER OF HASHTAGS TO DISPLAY AND CREATE SENTENCES TABLE------- "
        if displayType.lower() == 'sentences':
            numberOfHashtags = raw_input('\nEnter number of hashtags to display:\n')
            numberOfHashtags = int(numberOfHashtags)
            sentencesTable = PrettyTable()
            sentencesTable.hrules = ALL
            sentencesTable.field_names = ['Word','Documents','Sentences']
            sentencesTable.align = 'l'


        " -------ORDER HASHTAGS BY PREVALENCE AND PRINT USER'S CHOSEN TABLE------- "
        a = 0
        for word in sorted(hashtags, key = lambda word: len(hashtags[word]), reverse = True):
            sortedDocString = ', '.join(sorted(docsOfHashtags[word]))


            " -------FORMAT SENTENCES TO CONTROL COLUMN WIDTH------- "
            wrappedLines = []
            for sentence in hashtags[word]:
                wrappedLines.append(textwrap.fill(sentence, 100))
            stringOfSentences = '\n\n'.join(wrappedLines)
            
            
            " -------FILL OCCURRENCES TABLE------- "
            if displayType.lower() == 'occurrences':
                if len(hashtags[word]) >= minimumOccurences :
                    occurrencesTable.add_row([word, textwrap.fill(sortedDocString, 30), len(hashtags[word])])
            
            
            " -------FILL SENTENCES TABLE------- "
            if displayType.lower() == 'sentences':
                sentencesTable.add_row([word, textwrap.fill(sortedDocString, 30), stringOfSentences])
                a += 1
                if a == numberOfHashtags:
                    break
                
                
        " -------PRINT CHOSEN TABLE------- "
        if displayType.lower() == 'sentences':
            print sentencesTable
        if displayType.lower() == 'occurrences':
            print occurrencesTable


    " -------LOOKUP SPECIFIC WORDS------- "
    if tableOrLookup.lower() == 'lookup':
        while True:
            lookupWord = raw_input('\nEnter a word to see all sentences containing the word. Type "Go Back" to go back to the previous options.\n')
            lookupWord = lookupWord.lower()
            print '---------------------------------------------------------------'
            if lookupWord.lower() == 'go back':
                break
            try:
                print '\n' + '\n\n'.join(hashtags[lookupWord])
                print '---------------------'
            except KeyError:
                print '\n' + 'No occurences of ' + lookupWord
                print '\n---------------------------------------------------------------'
    
    
    " -------ALLOW EXIT------- "            
    if tableOrLookup.lower() == 'exit':
        break
    
    
    