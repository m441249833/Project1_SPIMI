import re
import spimi_util



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


def tokenization(file):
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
    spimi_util.spimi_invert(docList)

    f.close()
    return 0

if __name__ == '__main__':
    print("initializing......")
    #phase 1, creating disk block through spimi algorithm
    for i in range(22):
        if i <10 :
            filePath = "documents/reut2-00"+str(i)+".sgm"
        else:
            filePath = "documents/reut2-0"+str(i)+".sgm"
        # phase 1, spimi invert and write to blocks

        tokenization(filePath)
    print("spimi blocks created.")

        #phase 2, merging blocks



