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
dict = {1:1,2:1,3:1,4:2,5:2,6:1}
dict2 ={}
t = {v: k for k, v in dict.items()}
result = []

for key in dict.keys():
    result.append(key)
l = ['a','b','c']

for w in sorted(dict, key=dict.get, reverse=True):
  print (w,dict[w])