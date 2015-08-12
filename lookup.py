import string
from yfcc import YFCC
import lmdb
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

def stats(ls, dc):
	for s in ls:
		if dc.get(s)==None:
			dc[s] = 1
		else:
			dc[s] = dc[s] + 1

sample_str = "the green camp had no choice but to end the fight after the perth-born 38-year-old headed back to the wrong corner at the conclusion of the ninth round, which left the australian wobbly after 15 unanswered blows by traver"
f1 = open("""/media/DATA/BigVision/NLTK/wikidata/entry.txt""",'rb')
f2 = open("""/media/DATA/BigVision/NLTK/wikidata/diction.txt""",'rb')
dc = p.load(f2)
print "f2 loaded"
ls = p.load(f1)
print "f1 loaded"
f1.close()
f2.close()

#rslt = tokenize(sample_str, dc, ls)
#print rslt

db = YFCC()
#tl_dc = dict()
tg_dc = dict()
#ds_dc = dict()
for idx in range(50):
	db.open('/media/DATA/BigVision/YFCC_100K_sample_images/images_files/part-'+str(idx).zfill(5))
	print 'part-'+str(idx).zfill(5)+' processing...'
	for item in db.iterItem():
		tagsls = item.user_tags
		tags = list()
		for ln in tagsls:
			wr = translate(ln)
			tags += tokenize(wr, dc, ls)
			#tags += wr.split(' ')
#		title = item.title
#		title = translate(title)
#		desc = item.description
#		desc = translate(desc)
		tg_ls = tags
#		ds_ls = tokenize(desc, dc, ls)
#		tl_ls = tokenize(title, dc, ls)
		stats(tg_ls, tg_dc)
#		stats(ds_ls, ds_dc)
#		stats(tl_ls, tl_dc)
	db.close()
#print 'Writing into title_wordlist.txt'
#f = open("""/media/DATA/BigVision/NLTK/corpora/wikidata/title_wordlist.txt""",'wb')
#tmp = sorted(tl_dc.iteritems(), key=lambda d:d[1], reverse=True)
#p.dump(tmp, f)
#f.close()
print 'Writing into tags_wordlist.txt'
f = open("""/media/DATA/BigVision/NLTK/wikidata/tags_wordlist.txt""",'wb')
tmp = sorted(tg_dc.iteritems(), key=lambda d:d[1], reverse=True)
p.dump(tmp, f)
f.close()
#print 'Writing into desc_wordlist.txt'
#f = open("""/media/DATA/BigVision/NLTK/corpora/wikidata/desc_wordlist.txt""",'wb')
#tmp = sorted(ds_dc.iteritems(), key=lambda d:d[1], reverse=True)
#p.dump(tmp, f)
#f.close()
print 'Done.'