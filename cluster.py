import lmdb
import re
from yfcc import YFCC 
import pickle as p 

def bifind(str, ls, h, t):
	m = (h+t)/2
	if ls[m][0]==str:
		return m
	elif ls[m][0]<str:
		return bifind(str, ls, m+1, t)
	else:
		return bifind(str, ls, h, m)

def tokenize(str, dc, ls):
	rs = list()
	h = 0
	t = 0
	b = 0
	while h<len(str):
		if t==len(str):
			substr = str[h:t]
			if dc.get(substr)==None:
				if b>h:
					substr = str[h:b]
					rs.append(substr)
					t = b
					h = t
				else:
					break
			else:
				rs.append(substr)
				break
		elif str[t].isalnum():
			t = t + 1
		elif not(str[h].isalnum()):
			t = t + 1
			h = t
		else:
			substr = str[h:t]
			if dc.get(substr)==None:
				if b <= h:
					t = t + 1
					h = t
				else:
					substr = str[h:b]
					rs.append(substr)
					t = b
					h = t
			else:
				b = t
				mat1 = bifind(substr, ls, 0, len(ls))
				mat2 = mat1
				while ls[mat2][0].find(substr)!=-1:
					mat2 = mat2 + 1
				if mat1 == mat2:
					rs.append(substr)
					t = t + 1
					h = t
				else:
					t = t + 1
		#print h, b, t
	return rs

def translate(str):
	ret = ''
	n = 0
	tmp = str.lower()
	while n < len(tmp):
		if tmp[n] == '+':
			ret = ret + ' '
			n = n + 1
		if tmp[n] == '%':
			asc = tmp[n+1:n+3]
			nasc = int(asc,16)
			ch = chr(nasc)
			ret = ret + ch
			n = n + 3
		else:
			ret = ret + tmp[n]
			n = n + 1
	return ret

ccpt = open('confident2_idx.list','r')
ccpt_dc = dict()
ccpt_ls = list()
for ln in ccpt.readlines():
	cp = ln.split()
	ccpt_ls.append((cp[0],cp[1]))
for it in ccpt_ls:
	ccpt_dc[it[0]] = it[1]
ccpt.close()

rslt = dict()
tgls = open('/media/DATA/BigVision/NLTK/wikidata/tags_nsw.wordlist','rb')
tg_ls = p.load(tgls)
tg_lsx = [w for w in tg_ls if w[1]>5]
tg_dc = dict()
for it in tg_lsx:
	tg_dc[it[0]] = it[1]
tgls.close()

f1 = open("""/media/DATA/BigVision/NLTK/wikidata/entry.txt""",'rb')
f2 = open("""/media/DATA/BigVision/NLTK/wikidata/diction.txt""",'rb')
dc0 = p.load(f2)
print "f2 loaded"
ls0 = p.load(f1)
print "f1 loaded"
f1.close()
f2.close()

db = YFCC()
for idx in range(50):
	db.open('/media/DATA/BigVision/YFCC_100K_sample_images/images_files/part-'+str(idx).zfill(5))
	print 'part-'+str(idx).zfill(5)+' processing...'
	for item in db.iterItem():
		if ccpt_dc.get(item.id)!=None:
			cplb = ccpt_dc[item.id]
			if rslt.get(cplb)==None:
				rslt[cplb] = dict()
			tagsls = item.user_tags
			tags = list()
			for ln in tagsls:
				wr = translate(ln)
				tags += tokenize(wr, dc0, ls0)
			dc = rslt[cplb]
			for it in tags:
				if tg_dc.get(it)!=None:
					if dc.get(it)==None:
						dc[it] = 1
					else:
						dc[it] += 1
	db.close()

print 'sorting...'
rsltx = dict()
for it in rslt:
	rsltx[it]=sorted(rslt[it].iteritems(), key=lambda d:d[1], reverse=True)
print 'sorted'
f = open('/media/DATA/BigVision/NLTK/wikidata/tags_stats','wb')
p.dump(rsltx,f)
f.close()
print 'done.'
#print rslt