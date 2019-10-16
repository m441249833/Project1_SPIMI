import re
import main



#main.getFileText("textFile")
#a = doc[doc.index("<body>")+6:doc.index("</body>")]
doc = ""
a = re.search("<BODY>",doc)
print(a)