from nltk.corpus import wordnet as wn
import pickle as p

f = open('/media/DATA/BigVision/NLTK/wikidata/tags_nsw.wordlist','rb')
tg_ls = p.load(f)
f.close()
wn_ls = list()
wk_ls = list()
cl_ls = list()
for i in range(len(tg_ls)):
	wd = tg_ls[i][0]
	ss_ls = wn.synsets(wd)
	if len(ss_ls)!=0:
		ss = ss_ls[0]
		paths = ss.hypernym_paths()
		pt = [synset.name() for synset in paths[0]]
		wn_ls.append(tg_ls[i])
		cl_ls.append((wd,pt))
	else:
		wk_ls.append(tg_ls[i])

f = open('/media/DATA/BigVision/NLTK/wikidata/tags_wn.wordlist','wb')
p.dump(wn_ls,f)
f.close()
f = open('/media/DATA/BigVision/NLTK/wikidata/tags_wk.wordlist','wb')
p.dump(wk_ls,f)
f.close()
f = open('/media/DATA/BigVision/NLTK/wikidata/tags_cl.wordlist','wb')
p.dump(cl_ls,f)
f.close()