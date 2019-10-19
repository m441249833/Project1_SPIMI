def intersecting_lists(l,dict):
    ele = l[0]
    result=[]
    for i in dict[ele]:
        count = 1
        for j in l[1:]:
            if i in dict[j]:
                count +=1
        if count == len(l):
            result.append(i)
    return result


def union_list(l,dict):
    result = dict[l[0]]
    for i in range(1,len(l)):
        result += dict[l[i]]
    return result

def single_list(word,dict):
    return dict[word]

