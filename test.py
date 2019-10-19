import re


def intersecting_lists(l, dict):
    ele = l[0]
    result = []
    for i in dict[ele]:
        count = 1
        for j in l[1:]:
            if i in dict[j]:
                count += 1
        if count == len(l):
            result.append(i)
    return result


#main.getFileText("textFile")
#a = doc[doc.index("<body>")+6:doc.index("</body>")]
dict = {'a':[1,2,3,4,5],'b':[2,3,4,5,6],'c':[1,3,4,5,6,7]}
l = ['a','b','c']

print(intersecting_lists(l,dict))