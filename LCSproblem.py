#!/usr/bin/env python

'''
input two strings v,w
ouput longest common subsequences between two strings
To avoid maximum recursion depth exceedition, recursion depth should be set
'''

import sys
sys.setrecursionlimit(1000000)


def LCSBacktrack(v, w):
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
	for i in range(len(v)):
		for j in range(len(w)):
			if v[i] == w[j]:
				s[i + 1][j + 1] = max(s[i][j + 1], s[i + 1][j], (s[i][j] + 1))
			else:
				s[i + 1][j + 1] = max(s[i][j + 1], s[i + 1][j])
			if s[i + 1][j + 1] == s[i][j + 1]:
				backtrack[i + 1][j + 1] = 'down'
			elif s[i + 1][j + 1] == s[i + 1][j]:
				backtrack[i + 1][j + 1] = 'right'
			elif s[i + 1][j + 1] == s[i][j] + 1 and v[i] == w[j]:
				backtrack[i + 1][j + 1] = 'cornor'
	return backtrack


def OutputLCS(backtrack, v, i, j, output):
	'''
	backtrack is the matrix returned by function LCSBacktrack
	v is a str
	i, j is the length of v and w
	'''
	if i == 0 or j == 0:
		return ''
	if backtrack[i][j] == 'down':
		output = OutputLCS(backtrack, v, i - 1, j, output)
	elif backtrack[i][j] == 'right':
		output = OutputLCS(backtrack, v, i, j - 1, output)
	else:
		output = OutputLCS(backtrack, v, i - 1, j - 1, output) + v[i - 1]
	return output


def main():
	v = 'AGACTG'
	w = 'GTACGA'
	backtrack = LCSBacktrack(v, w)
	n = len(v)
	m = len(w)
	output = ''
	output = OutputLCS(backtrack, v, n, m, output)
	print output


if __name__ == '__main__':
	main()
