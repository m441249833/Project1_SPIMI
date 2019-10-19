def intersecting_list(l,dict):
    ll = []
    for item in l :
        if dict.get(item.lower()) != None:
            ll.append(item.lower())
        else:
            print("word \'"+item+"\' is no in the database")

    if len(ll) == 0:
        return []
    ele = ll[0]
    result=[]
    for i in dict[ele.lower()]:
        count = 1
        for j in ll[1:]:
            if i in dict[j.lower()]:
                count +=1
        if count == len(ll):
            result.append(i)
    return result


def union_list(l,dict):
    if dict.get(l[0].lower()) != None:
        result = dict[l[0].lower()]
    else:
        print("word \'" + l[0] + "\' is no in the database")
        result = []
    for i in range(1,len(l)):
        if dict.get(l[i].lower()) != None:
            result += dict[l[i].lower()]
        else:
            result +=[]
            print("word \'" + l[i] + "\' is no in the database")
    return result

def single_list(word,dict):
    if dict.get(word.lower()) == None:
        print("word \'" + word + "\' is no in the database")
        return []
    else:
        return dict[word.lower()]

