#!/usr/bin/env python

'''
To solve local alignment problem, that is, to find out the maximum scores of the local alignment of the strings.
It is an improvement on global alignment problem, using DAG, which add edges weigh 0 from source to every nodes, and from every nodes to sink
'''

import sys
sys.setrecursionlimit(1000000)


def loadMatrix(filename):
	score = {}
	keys = []
	with open(filename, 'r') as f:
		for line in f:
			line = line.rstrip()
			if line[0] == ' ':
				# the first line
				line = line.split('  ')
				keys = line[1:]
				keys[0] = 'A'
				# print keys
			else:
				score[line[0]] = {}
				line = line.split('  ')
				# first element is the name of this row
				rowName = line[0]
				line = line[1:]
				for i in range(len(keys)):
					score[rowName][keys[i]] = int(line[i])
	return score


def DAGbuilt(v, w, matrix, sigma):
	'''
	v, w are two str containing separated characters
	dimension of s is (|v| + 1) * (|w| + 1)
	'''
	backtrack = []
	s = []
	for i in range(len(v) + 1):
		s.append([0])
		backtrack.append([' '])
	'''
	s[0][0] has already been given a value, so next we begin from s[0][1]
	'''
	for i in range(len(v) + 1):
		for j in range(len(w)):
			backtrack[i].append(' ')
			s[i].append(0)
			# initialize
	for i in range(len(v)):
		s[i + 1][0] = s[i][0] - sigma
	for j in range(len(w)):
		s[0][j + 1] = s[0][j] - sigma
	s[0][0] = 0
	for i in range(len(v)):
		for j in range(len(w)):
			s[i + 1][j + 1] = max((s[i][j + 1] - sigma), (s[i + 1][j] - sigma), (s[i][j] + matrix[v[i]][w[j]]), 0)
			if s[i + 1][j + 1] == s[i][j + 1] - sigma:
				backtrack[i + 1][j + 1] = 'down'
			elif s[i + 1][j + 1] == s[i + 1][j] - sigma:
				backtrack[i + 1][j + 1] = 'right'
			elif s[i + 1][j + 1] == s[i][j] + matrix[v[i]][w[j]]:
				backtrack[i + 1][j + 1] = 'cornor'
			elif s[i + 1][j + 1] == 0:
				backtrack[i + 1][j + 1] = 'source'
	score = []
	for each in s:
		score.append(max(each))
	scoremax = max(score)
	scoreindex = []
	scoreindex.append(score.index(scoremax))
	scoreindex.append(s[scoreindex[0]].index(scoremax))
	return [backtrack, scoremax, scoreindex]


def wbacktrack(graph, w, n, m, output):
	'''
	backtrack the graph, from node with the highest score which is denoted as scoremax
	'''
	if n == 0 or m == 0 or graph[n][m] == 'source':
		# output = output + w[m]
		return ''
	if graph[n][m] == 'down':
		output = wbacktrack(graph, w, n - 1, m, output) + '-'
	elif graph[n][m] == 'right':
		output = wbacktrack(graph, w, n, m - 1, output) + w[m - 1]
	else:
		output = wbacktrack(graph, w, n - 1, m - 1, output) + w[m - 1]
	return output


def vbacktrack(graph, v, n, m, output):
	'''
	backtrack the graph, from node with the highest score which is denoted as scoremax
	'''
	if n == 0 or m == 0 or graph[n][m] == 'source':
		# output = output + w[m]
		return ''
	if graph[n][m] == 'down':
		output = vbacktrack(graph, v, n - 1, m, output) + v[n - 1]
	elif graph[n][m] == 'right':
		output = vbacktrack(graph, v, n, m - 1, output) + '-'
	else:
		output = vbacktrack(graph, v, n - 1, m - 1, output) + v[n - 1]
	return output


matrix = loadMatrix('PAM250.txt')
# print matrix
sigma = 5
v = 'KNVMWNHVRNHPSPNWMECSRCWQHLMPPAWSAQSMMRCIECFEMPFDSDHNPEQKTAETLGNCELVDTQPFGPHMPSIRQSKCRVWWNNQWFGERHEREQQDSFPLEKMQVNFAVKALFGGQMAGKAIMWHCTFLMDYLWVNTMDACANDLLPTYCLDNLAPGLKHCHQSEWNYEGGLKTNLHQQYCDEFKAHIIPKEAPIVDILCPWTIKYELEQNEFAMAMESIAIAMQGANWRGFFCYDCIAYPHAIHMIARDGASCLWGGYANMERTSKSQRWIDQETWPKQHAMQMNDKGERVAYVNQTMPYATCGRDSIDELIWCNYLLSVCYPRHEEAWQCEWHNADDKPSTHDTFLQMSIKHFAMRFSNEVGIAQFAEEDNDSDQKPRKETLSNYNWWVWQQKPRHPVGFQLSVQWFHPFSALACSGYCVERGFEWYFEYPIYMLGLAKESSMTKRMSKGHFATARTFWRDLYEFFIPCCMRWILCYCEWDPIDFQKKPITRTAWDSNVKKLFYYPGSPWVLKKENLQQMMYVMLQRTHQATNTPLLRKYATREAHPTPQWEQPHFPEYTFMRFVAGYMHKEMMTNDHWVINKQPPNGHMLCGFTEVMFLYHTDCFEKQQFSHWVAGNLPQHKAKCYVKMCMQSEHSACDSQNWKYFDNHHVHHSWWHTLYIPNRIYTCVREHHGYFQGPAIFLMDPDPFCVENHNAYPGYVTERKTKLCKINPHVTMATKNPSKGRILITKFDQFVPNDRDKREVEWMLFAYRRYMRSFKTEHRTIPVYEPNALTIRLLYNRPAEPEYPMDFSVRNNDWIDCGANFAEVNFPKRNCGPDLRLLGPMGVWFSRWIGALLYPFKSSYSDRDFGRWAYPDVANWSDVIAVYLMNLYWKDQASSMGHHYRQTKG'
w = 'TSWMRGESQCKSVAKNMPMYFLKACNCCCGMRIFTYWTYRHLWLIKEKSTKGHETIYCRYSCRKNANEQMSCVVCCHQQGCDSREYYNARDFIATGLAGNWDHAVHIFCGQPGGAFHYTDFLVYYFGPASHDAKAAKNCLEWLCQHCVHRMNQDANGIRHPPLKCDGELDSMMKAGYNPHLVLNFCWHTSQQPTDIWYNFLRFDVMLSPMLDVACLHAKKHVADVHRMGMRYKFKLKDLKWRVLVYHMKGLTAYRQMGYRDCHTWNYGFCWRGFFNYDCIAYPALAPRQFCTDGASCLWQEKGVGHNGYANMERTIGCNWFVFKSSNWLFKETHDQVSKQHAMQPDYDKGERRQAEPKPNKGPGGDYAWCDELWCNYWASLSVVSKKNYAWQCEWHNMVAVIWKAVLRLTFLQMSIKHFAMRFSNEVGIAQFGEEDNDSDQADGNHPRKETGSNYNWWTWQQAPRHPVGFANLEKWPHSVFFKQWPHPNSGYYVERGFEIYMTLLICLAGGRDTKKMSKGHFAGARTTWRRFIPCHMMLPCSWILCYCEFQKRFPWCVMQSEITKTGWDDNVKKLFYYPRPIPYRRMLKENLQQMMYVMLRRFHHPNYPLHPERQWTWWCGRFVAGYMHKEYMTWDHWTINKQPKCSHIQQCESFEVWQALTPYTCHFDVWTLVVSPSGMAPIFWDDRHQPAGSAKFSWIIMHLLGSWVCNCFTVYDQMAILQQVCNIKPCEMFSSLNIKVMYGYLDEEMKIFRSQLIMIVKVQGHHIVEMDRQWSYRCNHTRWQVSRGRHCQFEKCEDWKHTPIYWEFVPVYMFIASELCGDIMENRWIKENFWWHTWVNKMTINKKWIPCCDILPKECWIIPQKYTVNRCWTSEGNLNRPPKRANRHWMMSAMPKSHRMPALLDRNLSTVDETLKRQTVWGCVDTLEPISPRNWFVTMRKCFVGFQIANNPENHKEDNCQNYMH'
graph = DAGbuilt(v, w, matrix, sigma)
# print graph
n = graph[2][0]
m = graph[2][1]
woutput = ''
woutput = wbacktrack(graph[0], w, n, m, woutput)
voutput = ''
voutput = vbacktrack(graph[0], v, n, m, voutput)
print graph[1]
print voutput
print woutput
