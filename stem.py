import pickle as p 
import nltk

f = open('/media/DATA/BigVision/NLTK/wikidata/tags_stats','rb')
ccpt_dc = p.load(f)
f.close()
xccpt_dc = dict()
#porter = nltk.PorterStemmer()
wnl = nltk.WordNetLemmatizer()
for it in ccpt_dc:
	xccpt_dc[it] = dict()
	ls = ccpt_dc[it]
	dc = xccpt_dc[it]
	for tp in ls:
		#key = porter.stem(tp[0])
		key = wnl.lemmatize(tp[0])
		if dc.get(key)==None:
			dc[key] = tp[1]
		else:
			dc[key] += tp[1]

print 'sorting...'
rslt = dict()
for it in xccpt_dc:
	rslt[it]=sorted(xccpt_dc[it].iteritems(), key=lambda d:d[1], reverse=True)
print 'sorted'
f = open('/media/DATA/BigVision/NLTK/wikidata/tags_statsX','wb')
p.dump(rslt,f)
f.close()
print 'done.'