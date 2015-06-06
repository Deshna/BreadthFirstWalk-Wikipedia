import wikipedia
from bs4 import BeautifulSoup
import pandas as pd
from nltk.tag import pos_tag
import re, Queue
counter = 1

q = Queue.Queue()
title_list = []

def find_links():
    global counter, title
    global q
    print "Enter while"
    
    
    while (not q.empty()):
        string = q.get()
        print "Head of the queue: ",string
        switch = False
        if string is not None:
            if string not in title_list:
                title_list.append(string)
            else:
                print "Node already traversed."
                switch = True
        else:
            print "String value was null."
            switch = True

        if switch:
            continue

        try:
            page = wikipedia.page(string)
        except:
            continue
        html_doc = page.html()
        soup = BeautifulSoup(html_doc)
        text = soup.find('table')
        born = str(text).find('Born')
        if born == -1:
            continue
        title = string
        matches = re.findall(r'title=\"(.+?)\"',str(text))
    
        match_list = []
        for match in matches:
            try:
                match = match.encode('utf-8')
                tag_tuples = pos_tag(match.split())
                count = 0
                for (string,tag) in tag_tuples:
                    if tag == 'NNP':
                            count = count+1
                if count==len(tag_tuples) and count>=2:
                    match_list.append(match)
                    q.put(match)
            except:
                print "Skipped value:",match
                pass
        
        print match_list
    
        if len(match_list)>0:
            data = pd.DataFrame({'title':[title],'related':[match_list[0]]})
            for i in range(1,len(match_list)):
                data.loc[counter] = [match_list[i],title]
                counter = counter + 1
        
            print data
            data.to_csv('gephi_ip.csv', mode = 'a')


title = 'Barack Obama'
q.put(title)
print "sent to run."
find_links()
