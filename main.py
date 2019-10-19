import re
import spimi_util
import query_utils as qu
import nltk
from nltk import PorterStemmer




def getDocId(line):
    return re.findall('NEWID="(.*?)"',line)[0]

def getToken(docID,text):
    '''
    Function that generates terms strea
    @:param: docID(int), text(string)
    @:return: a tuple consist of document id and terms of this document
    '''

    # canceling all digits, replace them to ""

    terms = re.sub('\d+','',text)
    # macthing all words, ignoring punctuations , put all terms in terms[] list
    terms = re.findall(r'\w+',terms)
    if 'reuter' in terms:
        terms.remove('reuter')
    #print("ID:",docID,"\n","text:\n",terms)
    return (docID,terms)

def extractText(text):
    '''
    Function extracts text content from tag <body> for current document
    @:param:reuter text with tags
    @:return: article text without tags
    '''
    temp = (text[text.index("<BODY>")+6:text.index("</BODY>")])
    temp = temp.lower()
    return temp


def tokenization(file,totalDict):
    '''

    :param file:
    :return:
    '''
    f = open(file,errors='ignore')
    line = f.readline()
    docList=[]
    while line:
        doc =""
        id =0
        while not re.search("</REUTERS>",line):
            doc += line
            if re.search("NEWID=",line):
                id = int(getDocId(line))
            line = f.readline()

        if re.search("<BODY>",doc) != None: # if the document has no content, also append empty term list to it for future convenience.
            doc = extractText(doc)
            docList.append(getToken(id,doc))
        else:
            docList.append((id,[]))

        line = f.readline()

    # once a reuter file is ready, invert it and split it to 2 block and write into disk.
    spimi_util.spimi_invert(docList,totalDict)

    f.close()
    return 0

def mergeBlocks(totalDict):
    i = 0
    fileNo = 1
    filePath = "merged_blocks/block"+str(fileNo)+".txt"
    f = open(filePath,"w+",errors='ignore')
    sorted_terms = sorted(totalDict)
    for item in sorted_terms:
        f.write(item+":"+str(totalDict[item])+"\n")
        i +=1
        if i == 25000:
            fileNo +=1
            f.close()
            filePath = "merged_blocks/block"+str(fileNo)+".txt"
            f = open(filePath,"w+",errors='ignore')
            i = 0
            continue


def process_query(str,dict):
    if re.search(" AND ",str):
        str = str.split(" AND ")
        for item in str:
            item.lower()
        return qu.intersecting_lists(str,totalDict)
    elif re.search(" OR ",str):
        for item in str:
            item.lower()
        str = str.split(" OR ")
        return qu.union_list(str,totalDict)
    else:
        return qu.single_list(str,totalDict)






if __name__ == '__main__':
    print("initializing......")
    totalDict = dict()
    #phase 1, creating disk block through spimi algorithm
    for i in range(2):
        if i <10 :
            filePath = "documents/reut2-00"+str(i)+".sgm"
        else:
            filePath = "documents/reut2-0"+str(i)+".sgm"
        # phase 1, spimi invert and write to blocks

        tokenization(filePath,totalDict)
    print("spimi blocks created.")

        #phase 2, merging blocks
    mergeBlocks(totalDict)

        #phase 3, retrieve
    str = ""
    while True:
        str = input("Please enter a string(enter -1 to exit):")
        if str == '-1':
            break
        answer = process_query(str,totalDict)
        print("query result:")
        print(answer)









