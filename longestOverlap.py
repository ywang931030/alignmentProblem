#!/usr/bin/env python
'''
find all pairs of reads with an exat suffix/prefix match of length at least 30.
mismatch is not permissioned
'''

from itertools import permutations
import time


def seedOverlap(seeds, k):
	'''
	Run overlap in seedIndex rather than permutations
	for each key in seeds, seeds[key][0] is b, seeds[key][1:]is a
	'''
	olap = {}
	for keys in seedIndex.keys():
		for each in seedIndex[keys][1:]:
			suffixId = each.index(keys)
			if each[suffixId:] == seedIndex[keys][0][0:len(each[suffixId:])]:
				olap[each, seedIndex[keys][0]] = 'miu'
	return olap


def indexBuild(reads, k):
	'''
	Preprocess reads file:
	Build seed index: term 'seed' indicates the potential allignment between subsequent of reads and prefix
	for each reads:
		if exist subsequent of reads == prefix: # prefix is the key value
			index[prefix] = reads
	'''
	seedIndex = {}
	for each in reads:
		seedIndex[each[: k]] = [each]

	for keys in seedIndex.keys():
		for each in reads:
			if keys in each and keys != each[: k]:
				seedIndex[keys].append(each)
			else:
				continue

	return seedIndex


def naiveOverlap(reads, k):
	olaps = {}
	for a, b in permutations(reads, 2):
		if b[: k] in a and a != b:
			olen = overlap(a, b, min=k)
			if olen > 0:
				olaps[(a, b)] = olen
	return olaps


def overlap(a, b, min):
	'''
	Return length of longest suffix of a matching a prefix of b that is at least min length.
	If NULL, returns 0.
	'''
	# start all the way from left
	start = 0
	while True:
		start = a.find(b[: min], start)
		# no more occurences to right
		if start == -1:
			return 0
		# if exist, check for full suffix-prefix match
		if b.startswith(a[start:]):
			return len(a) - start
		start += 1


def readGenomeFile(filename):
	'''
	Read FASTQ file.
	'''
	reads = []
	with open(filename, 'r') as fh:
		while True:
			# skip name line
			fh.readline()
			# read base sequence
			seq = fh.readline().rstrip()
			# skip placeholder line
			fh.readline()
			# skip the base quality line
			fh.readline()
			if len(seq) == 0:
				break
			reads.append(seq)
	return reads


reads = readGenomeFile('ERR266411_1.for_asm.fastq')
starttime = time.clock()
k = 30
# seedIndex = indexBuild(reads, k)
# seedOlap = {}
# seedOlap = seedOverlap(seedIndex, k)
olap = {}
olap = naiveOverlap(reads, k)
counts = []
# seedOverlap
# for a, b in seedOlap.keys():
# 	if a not in counts:
# 		counts.append(a)
for a, b in olap.keys():
	if a not in counts:
		counts.append(a)
endtime = time.clock()
print endtime - starttime
print len(counts)
print len(olap.keys())
