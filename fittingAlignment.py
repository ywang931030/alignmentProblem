#!/usr/bin/env python

'''
Find out the alignment with highest score between v', the substring of v, and w.
Use condition free taxi ride(LocalAlignment) algorithm.
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
	score = max(s[len(w)])
	scoreindex = []
	for j in range(len(v)):
		if s[len(w)][j] == score:
			scoreindex.append(j)
	index = max(scoreindex)
	# index = s[len(w)].index(score)
	return [backtrack, score, [len(w), index], s]


def wbacktrack(graph, w, n, m, output):
	'''
	backtrack the graph, from node with the highest score which is denoted as scoremax
	'''
	if graph[m][n] == 'source' or m == 0:
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
	if graph[m][n] == 'source' or m == 0:
		return ''
	if graph[m][n] == 'down':
		output = vbacktrack(graph, v, n, m - 1, output) + '-'
	elif graph[m][n] == 'right':
		output = vbacktrack(graph, v, n - 1, m, output) + v[n - 1]
	else:
		output = vbacktrack(graph, v, n - 1, m - 1, output) + v[n - 1]
	return output


sigma = 1
v = 'GTTGGATTACGAATCGATATCTGTTTG'
w = 'ACGTCG'
n = len(v)
m = len(w)
graph = DAGbuilt(v, w, sigma)
woutput = ''
voutput = ''
n = graph[2][1]
woutput = wbacktrack(graph[0], w, n, m, woutput)
voutput = vbacktrack(graph[0], v, n, m, voutput)
print graph[1]
print voutput
print woutput
# print graph[3][len(w)]
