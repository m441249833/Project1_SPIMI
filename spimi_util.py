global blockID
blockID = 1

def spimi_invert(token_stream):
    dictionary = dict()


    for token in token_stream:
        id = token[0]
        terms = token[1]
        for term in terms: # invert each term
            if dictionary.get(term) != None:
                if id not in dictionary[term]:
                    dictionary[term].append(id)
            else:
                dictionary[term] = [id]
        if (id % 500 == 0):
            # for every 500 articles, write into disk block.
            sorted_terms = sorted(dictionary)
            writeTermsToBlock(sorted_terms,dictionary)
            dictionary=dict()
            sorted_terms=[]
    if len(dictionary.keys()) != 0:
        # if there are terms left in the dictionary (esspecially for the last document case, there are 500+78 documents, so need to store the remaining 78 docments)
        sorted_terms = sorted(dictionary)
        writeTermsToBlock(sorted_terms, dictionary)


    return sorted_terms

def writeTermsToBlock(sorted_terms,dict):
    global blockID
    path = "blocks/block" + str(blockID) + ".txt"
    f = open(path, 'w+')
    print("creating block",blockID,"......")
    for term in sorted_terms:
        f.write(term+":"+str(dict.get(term))+"\n")
    f.close()
    blockID +=1






