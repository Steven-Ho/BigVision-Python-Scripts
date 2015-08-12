import nltk
import re
import pickle as p
from nltk.corpus import stopwords

f = open('/media/DATA/BigVision/NLTK/wikidata/tags_wordlist.txt','rb')
tg_ls = p.load(f)
f.close()
tg_dc = dict()
for ln in tg_ls:
	tg_dc[ln[0]] = ln[1]


sw_dc = dict()
#1.extract stopwords
sw = stopwords.words('english')
sw += stopwords.words('spanish')
sw += stopwords.words('german')
for it in sw:
	if tg_dc.get(it)!=None:
		sw_dc[it] = tg_dc[it]
		tg_dc.pop(it)
#2.extract empty strings
#sw_dc[''] = tg_dc['']
#tg_dc.pop('')
#3.extract years
yr = [w[0] for w in tg_ls if re.search('^[0-9]+$',w[0])]
for it in yr:
	if tg_dc.get(it)!=None:
		sw_dc[it] = tg_dc[it]
		tg_dc.pop(it)
#4.extract single alnum
for ln in tg_ls:
	if len(ln[0])==1:
		if tg_dc.get(ln[0])!=None:
			sw_dc[ln[0]] = ln[1]
			tg_dc.pop(ln[0])

tg_ls = sorted(tg_dc.iteritems(), key=lambda d:d[1], reverse=True)
f = open('/media/DATA/BigVision/NLTK/wikidata/tags_nsw.wordlist','wb')
p.dump(tg_ls,f)
f.close()
print sw_dc