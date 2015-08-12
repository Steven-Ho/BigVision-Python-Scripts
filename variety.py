import pickle as p
import re

f = open('/media/DATA/BigVision/NLTK/wikidata/tags_statsX','rb')
dc = p.load(f)
f.close()

filt = ['www','com','square','iphoneography','app','flickr','instagram','500px','facebook','photo','foto','nikon','canon','nikkor']

ratio = 0.5
com = dict()
for it in dc:
	ls = dc[it]
	lt = list()
	for i in range(len(ls)):
		flag = False
		for j in range(len(filt)):
			if ls[i][0].find(filt[j])!=-1:
				flag = True
				break
		if re.search('[0-9]+d$',ls[i][0]):
			flag = True
		if re.search('^[daf][0-9]+',ls[i][0]):
			flag = True
		if not flag:
			lt.append(ls[i])
	ls = lt
		
	if len(ls)==0:
		com[it]=1.0
	else:
		sum_tg = 0
		for i in range(len(ls)):
			sum_tg += (ls[i][1])

		info = 0.0
		for i in range(len(ls)):
			info += ls[i][1]*1.0/sum_tg
			if info>ratio:
				break

		var = ((i+1)*1.0/sum_tg)/ratio
		com[it] = var

f = open('/media/DATA/BigVision/NLTK/wikidata/tags_comp','wb')
p.dump(com,f)
f.close()