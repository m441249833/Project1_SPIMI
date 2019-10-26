import re
import string
import nltk
#nltk.download()
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
ps = PorterStemmer()

def remove_num(dict):
    for key in tuple(dict.keys()):
        if key.isdigit():
            del dict[key]

def case_folding(unfiltered_list):
    dict_non_pos_temp = {}
    dict_pos_temp = {}
    for item in unfiltered_list:
        for term in item[1]:
            if dict_pos_temp.get(term.lower()) != None:
                dict_pos_temp[term.lower()].append(item[0])
            else:
                dict_pos_temp[term.lower()] = [item[0]]

    for item in unfiltered_list:
        for term in item[1]:
            if dict_non_pos_temp.get(term.lower()) != None:
                if item[0] not in dict_non_pos_temp[term.lower()]:
                    dict_non_pos_temp[term.lower()].append(item[0])
            else:
                dict_non_pos_temp[term.lower()] = [item[0]]

    return dict_non_pos_temp,dict_pos_temp

def remove_stopwords(dict,num):
    words = []
    for sample in set(stopwords.words('english')):
        words.append(sample)
        if len(words) >= num :
            break
    for word in words:
        if dict.get(word) != None:
            del dict[word]

def stemming(unfilterd_list):
    dict_non_pos_temp = {}

    for item in unfiltered_list:
        for term in item[1]:
            if dict_non_pos_temp.get(ps.stem(term.lower())) != None:
                if item[0] not in dict_non_pos_temp[ps.stem(term.lower())]:
                    dict_non_pos_temp[ps.stem(term.lower())].append(item[0])
            else:
                dict_non_pos_temp[ps.stem(term.lower())] = [item[0]]

    return dict_non_pos_temp



def remove_punc(str):
    for char in str:
        if char in string.punctuation:
            str = str.replace(char,'')
    return str

def collect_term(filePath):
    f = open(filePath,errors='ignore')
    line = f.readline()
    docList = []
    while line:
        doc = ""
        id = 0
        while not re.search("</REUTERS>", line):
            doc += line
            if re.search("NEWID=", line):
                id = int(re.findall('NEWID="(.*?)"',line)[0])
            line = f.readline()


        if re.search("<BODY>",doc) != None:  # if the document has no content, also append empty term list to it for future convenience.
            doc = doc[doc.index("<BODY>")+6:doc.index("</BODY>")]
            doc = remove_punc(doc)
            docList.append([id, doc.split()])
        else:
            docList.append([id, []])

        line = f.readline()
    return docList

def count_postings(dict):
    temp = 0
    for v in dict.values():
        temp += len(v)
    return temp

if __name__ == '__main__':
    unfiltered_list = []
    for i in range(22):
        if i < 10:
            filePath = "documents/reut2-00" + str(i) + ".sgm"
        else:
            filePath = "documents/reut2-0" + str(i) + ".sgm"
        unfiltered_list += collect_term(filePath)
    #print (unfiltered_list)
    dict_pos={}
    for item in unfiltered_list:
        for term in item[1]:
            if dict_pos.get(term) != None:
                dict_pos[term].append(item[0])
            else:
                dict_pos[term] = [item[0]]
    dict_non_pos={}

    for item in unfiltered_list:
        for term in item[1]:
            if dict_non_pos.get(term) != None:
                if item[0] not in dict_non_pos[term]:
                    dict_non_pos[term].append(item[0])
            else:
                dict_non_pos[term] = [item[0]]
    terms=[0,0,0,0,0,0]
    non_pos_posting=[0,0,0,0,0,0]
    pos_posting=[0,0,0,0,0,0]

    #title
    print("size","∆","cml","size","∆","cml","size","∆","cml")

    #unfiltered
    terms[0] = len(dict_non_pos)
    non_pos_posting[0] = count_postings(dict_non_pos)
    pos_posting[0] = count_postings(dict_pos)
    print (terms[0],0,0,
           "\t",non_pos_posting[0],0,0,
           "\t",pos_posting[0],0,0)

    # eliminate numbers
    for item in unfiltered_list:
        for term in item[1]:
            if term.isdigit():
                item[1].remove(term)
    remove_num(dict_pos)
    remove_num(dict_non_pos)

    terms[1] = len(dict_non_pos)
    non_pos_posting[1] = count_postings(dict_non_pos)
    pos_posting[1] = count_postings(dict_pos)
    print (terms[1],int(((terms[1]-terms[0])/float(terms[0]))*100),int(((terms[1]-terms[0])/float(terms[0]))*100),
           "\t",non_pos_posting[1],int(((non_pos_posting[1]-non_pos_posting[0])/float(non_pos_posting[0]))*100),int(((non_pos_posting[1]-non_pos_posting[0])/float(non_pos_posting[0]))*100),
           "\t",pos_posting[1],int(((pos_posting[1]-pos_posting[0])/float(pos_posting[0]))*100),int(((non_pos_posting[1]-non_pos_posting[0])/float(non_pos_posting[0]))*100))


    #case folding
    dict_non_pos,dict_pos = case_folding(unfiltered_list)
    terms[2] = len(dict_non_pos)
    non_pos_posting[2] = count_postings(dict_non_pos)
    pos_posting[2] = pos_posting[1]
    print (terms[2],int(((terms[2]-terms[1])/float(terms[1]))*100),int(((terms[2]-terms[0])/float(terms[0]))*100),
           "\t",non_pos_posting[2],int(((non_pos_posting[2]-non_pos_posting[1])/float(non_pos_posting[1]))*100),int(((non_pos_posting[2]-non_pos_posting[0])/float(non_pos_posting[0]))*100),
           "\t",pos_posting[2],int(((pos_posting[2]-pos_posting[1])/float(pos_posting[1]))*100),int(((pos_posting[2]-pos_posting[0])/float(pos_posting[0]))*100))

    # 30 stop words
    remove_stopwords(dict_non_pos,30)
    remove_stopwords(dict_pos,30)
    terms[3] = len(dict_non_pos)
    non_pos_posting[3] = count_postings(dict_non_pos)
    pos_posting[3] = count_postings(dict_pos)
    print (terms[3],int(((terms[3]-terms[2])/float(terms[2]))*100),int(((terms[3]-terms[0])/float(terms[0]))*100),
           "\t",non_pos_posting[3],int(((non_pos_posting[3]-non_pos_posting[2])/float(non_pos_posting[2]))*100),int(((non_pos_posting[3]-non_pos_posting[0])/float(non_pos_posting[0]))*100),
           "\t",pos_posting[3],int(((pos_posting[3]-pos_posting[2])/float(pos_posting[2]))*100),int(((pos_posting[3]-pos_posting[0])/float(pos_posting[0]))*100))

    #150 stop words
    remove_stopwords(dict_non_pos,150)
    remove_stopwords(dict_pos,150)
    terms[4] = len(dict_non_pos)
    non_pos_posting[4] = count_postings(dict_non_pos)
    pos_posting[4] = count_postings(dict_pos)
    print (terms[4],int(((terms[4]-terms[3])/float(terms[3]))*100),int(((terms[4]-terms[0])/float(terms[0]))*100),
           "\t",non_pos_posting[4],int(((non_pos_posting[4]-non_pos_posting[3])/float(non_pos_posting[3]))*100),int(((non_pos_posting[4]-non_pos_posting[0])/float(non_pos_posting[0]))*100),
           "\t",pos_posting[4],int(((pos_posting[4]-pos_posting[3])/float(pos_posting[3]))*100),int(((pos_posting[4]-pos_posting[0])/float(pos_posting[0]))*100))

    # stemming
    dict_non_pos = stemming(unfiltered_list)
    terms[5] = len(non_pos_posting)
    non_pos_posting[5] = count_postings(dict_non_pos)
    pos_posting[5] = pos_posting[4]
    print(terms[5], int(((terms[5] - terms[4]) / float(terms[4])) * 100),
          int(((terms[5] - terms[0]) / float(terms[0])) * 100),
          "\t", non_pos_posting[5], int(((non_pos_posting[5] - non_pos_posting[4]) / float(non_pos_posting[4])) * 100),
          int(((non_pos_posting[5] - non_pos_posting[0]) / float(non_pos_posting[0])) * 100),
          "\t", pos_posting[5], int(((pos_posting[5] - pos_posting[4]) / float(pos_posting[4])) * 100),
          int(((pos_posting[5] - pos_posting[0]) / float(pos_posting[0])) * 100))










