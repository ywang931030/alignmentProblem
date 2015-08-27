#!/usr/bin/env python
'''
Find a highest-scoring alignment of two strings as defined by a scoring matrix named 'BLSOUM62'
Input two protein strings written in the single-letter amino acid alphabet.
Output the maximum alignment score of these strings followed by an alignment achieving this score.
The BLOSUM62 is the scoring matrix, and indel penalty theta = -5
'''

__author__ = 'Yue Wang'


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


def alignBacktrack(v, w, matrix, theta):
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
		s[i + 1][0] = s[i][0] + theta
	for j in range(len(w)):
		s[0][j + 1] = s[0][j] + theta
	s[0][0] = 0
	for i in range(len(v)):
		for j in range(len(w)):
			s[i + 1][j + 1] = max((s[i][j + 1] + theta), (s[i + 1][j] + theta), (s[i][j] + matrix[v[i]][w[j]]))
			if s[i + 1][j + 1] == s[i][j + 1] + theta:
				backtrack[i + 1][j + 1] = 'down'
			elif s[i + 1][j + 1] == s[i + 1][j] + theta:
				backtrack[i + 1][j + 1] = 'right'
			elif s[i + 1][j + 1] == s[i][j] + matrix[v[i]][w[j]]:
				backtrack[i + 1][j + 1] = 'cornor'
	return [backtrack, s[len(v)][len(w)]]


def vOutputLCS(backtrack, v, i, j, output):
	'''
	backtrack is the matrix returned by function LCSBacktrack
	v is a str
	i, j is the length of v and w
	'''
	if i == 0 or j == 0:
		return ''
	if backtrack[i][j] == 'down':
		output = vOutputLCS(backtrack, v, i - 1, j, output) + v[i - 1]
	elif backtrack[i][j] == 'right':
		output = vOutputLCS(backtrack, v, i, j - 1, output) + '-'
	else:
		output = vOutputLCS(backtrack, v, i - 1, j - 1, output) + v[i - 1]
	return output


def wOutputLCS(backtrack, v, i, j, output):
	'''
	backtrack is the matrix returned by function LCSBacktrack
	v is a str
	i, j is the length of v and w
	'''
	if i == 0 or j == 0:
		return ''
	if backtrack[i][j] == 'down':
		output = wOutputLCS(backtrack, v, i - 1, j, output) + '-'
	elif backtrack[i][j] == 'right':
		output = wOutputLCS(backtrack, v, i, j - 1, output) + w[j - 1]
	else:
		output = wOutputLCS(backtrack, v, i - 1, j - 1, output) + w[j - 1]
	return output


# print loadMatrix('BLOSUM62.txt')
matrix = loadMatrix('BLOSUM62.txt')
# print matrix
theta = -5
v = 'PLEASANTLY'
w = 'MEANLY'
n = len(v)
m = len(w)
backtrack = alignBacktrack(v, w, matrix, theta)
print backtrack[1]
voutput = ''
voutput = vOutputLCS(backtrack[0], v, n, m, voutput)
woutput = ''
woutput = wOutputLCS(backtrack[0], w, n, m, woutput)

print voutput
print woutput
