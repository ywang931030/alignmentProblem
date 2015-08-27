#!/usr/bin/env python
'''
Global Alignment with align affine gap penaltys, that is, gap extension penalty epsilon and gap opening penalty sigma
'''

import sys
sys.setrecursionlimit(1000000)


def wBacktrack(middle, w, n, m, woutput):
	'''
	backtrack and construct full length of w
	'''
	if n == 0 or m == 0:
		return ''
	if middle[n][m] == 'toLower':
		woutput = wBacktrack(middle, w, n - 1, m, woutput) + '-'
	elif middle[n][m] == 'toUpper':
		woutput = wBacktrack(middle, w, n, m - 1, woutput) + w[m - 1]
	else:
		woutput = wBacktrack(middle, w, n - 1, m - 1, woutput) + w[m - 1]
	return woutput


def vBacktrack(middle, v, n, m, voutput):
	'''
	backtrack and construct full length of v
	'''
	if n == 0 or m == 0:
		return ''
	if middle[n][m] == 'toLower':
		voutput = vBacktrack(middle, v, n - 1, m, voutput) + v[n - 1]
	elif middle[n][m] == 'toUpper':
		voutput = vBacktrack(middle, v, n, m - 1, voutput) + '-'
	else:
		voutput = vBacktrack(middle, v, n - 1, m - 1, voutput) + v[n - 1]
	return voutput


def backtrackBuilt(v, w, n, m, matrix, sigma, epsilon):
	'''
	Build the backtrack matrix, to mostly alleviate number of edges, we implement three backtrack matrix.
	upper for right, lower for down, and middle for main
	'''
	upperBacktrack = []
	lowerBacktrack = []
	middleBacktrack = []
	upper = []
	lower = []
	middle = []
	# initiation the rows of backtrack matrix and scoring matrix
	for i in range(n + 1):
		upper.append([0])
		lower.append([0])
		middle.append([0])
		upperBacktrack.append([' '])
		lowerBacktrack.append([' '])
		middleBacktrack.append([' '])
	# initialize the columns of backtrack matrix and scoring matrix
	for i in range(n + 1):
		for j in range(m):
			lowerBacktrack[i].append(' ')
			upperBacktrack[i].append(' ')
			middleBacktrack[i].append(' ')
			lower[i].append(0)
			upper[i].append(0)
			middle[i].append(0)
	# initialize the scoring matrix
	# assumed that penalty for beginning from other offset rather than head is needed
	for i in range(n):
		lower[i + 1][0] = lower[i][0] - sigma
		upper[i + 1][0] = upper[i][0] - sigma
		middle[i + 1][0] = middle[i][0] - sigma
	for j in range(m):
		lower[0][j + 1] = lower[0][j] - sigma
		upper[0][j + 1] = upper[0][j] - sigma
		middle[0][j + 1] = middle[0][j] - sigma
	lower[0][0] = 0
	upper[0][0] = 0
	middle[0][0] = 0
	for i in range(n):
		for j in range(m):
			lower[i + 1][j + 1] = max(lower[i][j + 1] - epsilon, middle[i][j + 1] - sigma)
			upper[i + 1][j + 1] = max(upper[i + 1][j] - epsilon, middle[i + 1][j] - sigma)
			middle[i + 1][j + 1] = max(lower[i + 1][j + 1], upper[i + 1][j + 1], middle[i][j] + matrix[v[i]][w[j]])
			if lower[i + 1][j + 1] == lower[i][j + 1] - epsilon:
				lowerBacktrack[i + 1][j + 1] = 'down'
			elif lower[i + 1][j + 1] == middle[i][j + 1] - sigma:
				lowerBacktrack[i + 1][j + 1] = 'lowerToMiddle'
			if upper[i + 1][j + 1] == upper[i + 1][j] - epsilon:
				upperBacktrack[i + 1][j + 1] = 'right'
			elif upper[i + 1][j + 1] == middle[i + 1][j] - sigma:
				upperBacktrack[i + 1][j + 1] = 'upperToMiddle'
			if middle[i + 1][j + 1] == lower[i + 1][j + 1]:
				middleBacktrack[i + 1][j + 1] = 'toLower'
			elif middle[i + 1][j + 1] == upper[i + 1][j + 1]:
				middleBacktrack[i + 1][j + 1] = 'toUpper'
			elif middle[i + 1][j + 1] == middle[i][j] + matrix[v[i]][w[j]]:
				middleBacktrack[i + 1][j + 1] == 'cornor'
	return [lowerBacktrack, middleBacktrack, upperBacktrack, middle[n][m]]


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


def main():
	matrix = loadMatrix('BLOSUM62.txt')
	sigma = 11
	epsilon = 1
	v = 'GTIMICCIHARSTDKIMTPCNGFQHILVKTLKRESPWSPCEQYMGSDCMRMVMVSEGLMEVDTVKHIWGACCCRGKTYESQL'
	w = 'CFIMICCIHARSTERIVTTHCNGFQHILVKTLKEVPDWKDPWSPCEQYFGSDCMPMVMVSEGLMEVDTVHHICGATYEPQL'
	n = len(v)
	m = len(w)
	backtrack = backtrackBuilt(v, w, n, m, matrix, sigma, epsilon)
	# print backtrack
	vOutput = ''
	wOutput = ''
	vOutput = vBacktrack(backtrack[1], v, n, m, vOutput)
	wOutput = wBacktrack(backtrack[1], w, n, m, wOutput)
	print backtrack[3]
	print vOutput
	print wOutput


if __name__ == '__main__':
	main()
