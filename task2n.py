import os

def findall(text,s):
	res = []
	index = 0
	while ((text.find(s,index)) != -1):
		pos = text.find(s,index);
		res.append(pos)
		index = pos + 1
	return res

def judgefellow(text,s):
	pos = findall(text,'fellow')
	for p in pos:
		if s in text[p-15:p+15]:
			return True
	return False

dir = './data'
result=[]
for school in os.listdir(dir):
	if(school.find('.') != -1):
		continue
	schoolDir = os.path.join(dir,school)
	for professor in os.listdir(schoolDir):
		if(professor.find('.') != -1):
			continue
		isAcmfellow = 0
		isIeeefellow = 0
		isGranted = 0
		professorDir = os.path.join(schoolDir,professor)
		for info in os.listdir(professorDir):
			infopath = os.path.join(professorDir,info);
			if(os.path.isfile(infopath) == False):
				continue;
			webpage = open(infopath)
			text = webpage.read().lower()
			isAcmfellow += judgefellow(text,'acm')
			isIeeefellow += judgefellow(text,'ieee')
			isGranted += (text.find('nsf') or text.find('grant'))
			webpage.close()
		professorInfo = '|'.join([school,professor,str(isAcmfellow>=1),str(isIeeefellow>=1),str(isGranted>=1)])
		result.append(professorInfo+'\n')
op = open('index.txt','w')
op.writelines(result)
op.close()
