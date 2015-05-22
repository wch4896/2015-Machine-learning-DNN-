import numpy as np


def Svm_pre(fbankFilename, labelFilename, mapFilename):
	# load file
	fbank = open(fbankFilename, 'r')
	label = open(labelFilename, 'r')
	mapidx = open(mapFilename, 'r')
	t = open('test.csv', 'a')
	# split content_feature
	f = fbank.read()
	list_f = []
	batch_1 = f.split('\n')
	
	for i in range(len(batch_1)):
		list_f.append(batch_1[i].split(' '))
	# split content_label
	l = label.read()
	list_l = []
	batch_2 = l.split('\n')

	for i in range(len(batch_2)):
		list_l.append(batch_2[i].split(','))

	# split content_mapsheet
	m = mapidx.read()
	mapSheet = []
	batch_3 = m.split('\n')
	big_list = []
	mid_array = np.zeros((48,48))

	for i in range(len(batch_3)):
		mapSheet.append(batch_3[i].split('\t'))

	# added feature value in same label; transition counting
	for i in range(len(mapSheet)):
		# list 69*48
		feature_sum = np.zeros(shape = (69,))
		for k in range(len(list_l)):
			if mapSheet[i][0] == list_l[k][1]:
				feature_sum = feature_sum + np.array(map(float,list_f[k][1:70]))
		big_list.append(feature_sum)
		
		# array 48*48
		for j in range(len(mapSheet)):
			counts = 0
			for k in range(len(list_l) - 1):
				if list_l[k][1] == mapSheet[i][0] and list_l[k + 1][1] == mapSheet[j][0]:
					counts = counts + 1
			mid_array[i][j] = counts

	# resize array & list before ouput file 
	array_6948_1 = np.zeros((48,69))

	for i in range(48):
		for j in range(69):
			# pass
			array_6948_1[i][j] = big_list[i][j]

	array_6948_1.resize(1,3312)
	mid_array.resize(1,2304)

	# output file
	for i in range(3312):
		t.write('faem0_si1392_' + str(i) + ',' + str(array_6948_1[0][i]) + '\n')
	for i in range(3312,5616):
		t.write('faem0_si1392_' + str(i) + ',' + str(mid_array[0][i-3312]) + '\n')
		
	# close file	
	fbank.close()
	label.close()
	mapidx.close()

Svm_pre('train_fbank_474.ark', 'train_474.lab', '48_idx_chr.map')