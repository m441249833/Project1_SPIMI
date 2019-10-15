import re

def getDocId(line):
    return re.findall('NEWID="(.*?)"',line)[0]

def getToken(docID,text):
    """""
    Function that generates terms strea
    @:param docID(int), text(string)
    @:returns a tuple consist of document id and terms inside this document 
    """""

    # canceling all digits, replace them to " "(white spaces)
    terms = re.sub('\d+','',text)
    # macthing all words, ignoring punctuations , put all terms in terms[] list
    terms = re.findall(r'\w+',terms)
    #return (docID,terms)
    print("ID:",docID,"\n","text:\n",terms)
    #exit()
    return (docID,terms)

def extractText(text):
    """""
    Function extracts text content from tag <body> for current document
    @:param:

    """""
    return text[text.index("<BODY>")+6:text.index("</BODY>")]

def getFileText(file):
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
        if re.search("<BODY>",doc) != None:
            doc = extractText(doc)
        docList.append(getToken(id,doc))
        line = f.readline()

    f.close()
    return docList

def writeIntoBlock(block,blockID):
    path = "blocks/block"+str(blockID)+".txt"
    f = open(path,'w+')
    f.write(str(block))
    f.close()



if __name__ == '__main__':
    for i in range(22):
        if i <10 :
            filePath = "documents/reut2-00"+str(i)+".sgm"
        else:
            filePath = "documents/reut2-0"+str(i)+".sgm"
        block = getFileText(filePath)
        writeIntoBlock(block,i)

