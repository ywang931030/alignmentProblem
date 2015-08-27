#!/usr/bin/env python

'''
An overlap alignment of strings v = v1 ... vn and w = w1 ... wm is a global alignment of a suffix of v with a prefix of w.
An optimal overlap alignment of strings v and w maximizes the global alignment score between an i-suffix of v and a j-prefix of w (i.e., between vi ... vn and w1 ... wj) among all i and j.
Overlap Alignment Problem: Construct a highest-scoring overlap alignment between two strings.
Input: Two strings and a matrix score.
Output: A highest-scoring overlap alignment between the two strings as defined by the scoring matrix
score.
'''

import sys
sys.setrecursionlimit(1000000)


def DAGbuilt(v, w, sigma):
	'''
	v, w are two str containing separated characters
	dimension of s is (|v| + 1) * (|w| + 1)
	'''
	backtrack = []
	s = []
	for i in range(len(w) + 1):
		s.append([0])
		backtrack.append([' '])
	'''
	s[0][0] has already been given a value, so next we begin from s[0][1]
	'''
	for i in range(len(w) + 1):
		for j in range(len(v)):
			s[i].append(0)
			backtrack[i].append(' ')
			# initialize
	for i in range(len(w)):
		s[i + 1][0] = s[i][0] - sigma
	# source node is the w[0]
	for j in range(len(v)):
		s[0][j + 1] = 0
		backtrack[0][j] = 'source'
	for i in range(len(w)):
		for j in range(len(v)):
			if w[i] == v[j]:
				s[i + 1][j + 1] = max((s[i][j + 1] - sigma), (s[i + 1][j] - sigma), (s[i][j] + 1))
			else:
				s[i + 1][j + 1] = max((s[i][j + 1] - sigma), (s[i + 1][j] - sigma), (s[i][j] - sigma))
			if s[i + 1][j + 1] == s[i][j + 1] - sigma:
				backtrack[i + 1][j + 1] = 'down'
			elif s[i + 1][j + 1] == s[i + 1][j] - sigma:
				backtrack[i + 1][j + 1] = 'right'
			elif s[i + 1][j + 1] == s[i][j] + 1 and w[i] == v[j]:
				backtrack[i + 1][j + 1] = 'cornor'
			elif s[i + 1][j + 1] == s[i][j] - sigma and w[i] != v[j]:
				backtrack[i + 1][j + 1] = 'mismatch'
	score = []
	for i in range(len(w) + 1):
		score.append(s[i][len(v)])
	index = score.index(max(score))
	maxscore = max(score)
	return [backtrack, maxscore, [index, len(v)]]


def wbacktrack(graph, w, n, m, output):
	'''
	backtrack the graph, from node with the highest score which is denoted as scoremax
	'''
	if m == 0:
		return ''
	if graph[m][n] == 'down':
		output = wbacktrack(graph, w, n, m - 1, output) + w[m - 1]
	elif graph[m][n] == 'right':
		output = wbacktrack(graph, w, n - 1, m, output) + '-'
	else:
		output = wbacktrack(graph, w, n - 1, m - 1, output) + w[m - 1]
	return output


def vbacktrack(graph, v, n, m, output):
	'''
	backtrack the graph, from node with the highest score which is denoted as scoremax
	'''
	if graph[m][n] == 'source':
		return ''
	if graph[m][n] == 'down':
		output = vbacktrack(graph, v, n, m - 1, output) + '-'
	elif graph[m][n] == 'right':
		output = vbacktrack(graph, v, n - 1, m, output) + v[n - 1]
	else:
		output = vbacktrack(graph, v, n - 1, m - 1, output) + v[n - 1]
	return output


sigma = 2
v = 'ATTCTTATGGTGACCGAGGAAGAGGCCCGCACTAAGTCGTCTCACCGCCGTCTTCAATCCAGAGGATTAGCGCTGGGATCGATTTTTTCATGGATCCTACGTTACGAAGCTGACAGTAGCATTGACCCAAATTTAGGACTGTCAAGTACGAGAATTTGATGAATTCCATCGAACAACGCATGCTACATTCCACAAAACCCTCTTCAAAGTGGACCTCACAGGAGATGCGATACCGCGAAGCCGTAAGTTCCCTCTTTAAACCACGTGGAGTAAAATACCCCAAATTAGCCGTTATGACGGTGCAGGTCGGGTGCAGAGACTTCGTAGGGTGCAGCTTAGATCTCAGCTCTCTAATGTGACGCTCTCGGCTTTTCGGGGAGGGCCCCCATCACGCTTTTCCAATCCTTCCATTTGCCGTCGGTCGACCGGCTCACAATCTGGGAGTAAATTAATTGCAGGGGCCTTTTTAGAGATGAACAATCAGTCACGGACCACAGCCTCGGTGCGAGGGCCTAGTGCGTATTTGCAACCTTTCAGCGCTCGTGTCGTTAATTCATGCTCCTCATTCCAACCGAATAAATCCTACCCTTCCGCCGGCCCGGTAACTTCCTGCCTAAAGGTGGATCGTAGATAATACCGAGCTTTTTGTTTCCGGCTCGTTTGGAGTCTTACGTCCTATCACCTACAAAACGCGAACTAGCCGTGTCTAAGAGCTACGTTTGAGATATTGATGTTACGAGCTTATCCGCTGTAAGCTTCGGATCCGGGCAAAGCATGCCCCTATTGGGACTCTAGATTCCGTCGCTGGGTATCTTACAGGCCCGCAATTGCGGTGTTAGATGTGTACGGGTGGGCCGTACTGAGCTCGCGAAATCGTCTTTAATCCCATTAGAAAGGGGCGAAGATGAGCAGCAGGGGTGCACGGGGCCACACTCCACCGGCCATGTGGTCCTTCCATAGCCGTTC'
w = 'ATTTGATCCGGACGATCGCATGCCTACTGGGACCTAGATTCCGTCCCTGGGATCTTTTATGGCCGCGCAATTGCGGAGGTTGGATGTGTGCGGGCGTTGCTGTACTGAGTTGCGAAATGGTCTTTAAATCCCATGGTAGAGGTGGTTGAGGACAGGCCTCAAGGGGCTGCAAGGGCATCAATCACCACACCATGAGGCCTCTCATACCGTGTCTCAGCAAACAAATCCAACCCTCGCCTTAGGTGTTACTCGCGTCCAAGTTTAACGTAGGCCTGCGATAGGCCAGCCTCCGCGCTTCCGGTGACCTGACTGTCCACATACGCCTAGCATACTCTGATAGCTACGCCGCTATGGCACTAACCGGTTGTTCTCTGGGATCGTTATTCAAAGGGCAGCTTAGTCTAAACACTCTAGCTCCCTCCTGGTGTCGTTATGCGGAACTCGTCGTTTCTCTAGCTCTGGACTTCACCCTACAATACACGATCTATGGAGGCGAATAGCGTTCGGTGAATAGCCATACTGTTATCAAATTGTCTCGGCGCGCGAACTAGTACCCCGCGCAAAGAACAAGTCAGTAGGGGGGTGGCGTTAAACAGTGTACAGCCGCTCAAATTTTAATGCCGGAATCTGACCGTGGGTTCACTGATAACGCAGGGTGAGTCGGTGACAGGTCAAACTCTTCGGGTTTATTGGAAGTCTCAAACGAACCATTCTCAAACGAGAATACCTCATCGCTCTGACTCCCGCCAGACGGCAGCCATGCATGTCTTCCATATATCGTGTATGCTACTGCTCCGTAATTTGTCGAGCCTACATTCTAGAGGGAAAAGTTTCGGCCAATTCCCTAGTCCCCTCGCTAGT'
n = len(v)
m = len(w)
graph = DAGbuilt(v, w, sigma)
# print graph
n = graph[2][1]
m = graph[2][0]
woutput = ''
woutput = wbacktrack(graph[0], w, n, m, woutput)
voutput = ''
voutput = vbacktrack(graph[0], v, n, m, voutput)
print graph[1]
print voutput
print woutput
