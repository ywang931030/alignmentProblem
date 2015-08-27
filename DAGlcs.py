#!/usr/bin/env python

'''
input a source node and a sink node of a graph, followed by a list of edges and their weight in the graph
output the longest path in the graph followed by its length
'''


def buildGraph(edges):
	'''
	input a list contain edges and weights,
	output a dict contain edges and its predecessors together with weights
	In the dict predecessors: key is the node, first element of the value is the predecessor, second element is the weight of the edge
	'''
	predecessors = {}
	# initiation of the graph
	for each in edges:
		predecessors[each[0][1]] = []
	# build the graph, more than one edges may be exist to one node
	for each in edges:
		predecessors[each[0][1]].append([int(each[0][0]), int(each[1])])
	return predecessors


def longestPath(predecessors, source, sink):
	'''
	find the longest path in the graph
	input a dict with edges
	output the length of longest path in the graph
	'''
	s = [0 for i in range(sink - source + 1)]
	for i in range(sink - source):
		if str(i + 1 + source) in predecessors.keys():
			preWeight = {}
			for each in predecessors[str(i + 1 + source)]:
				preWeight[s[each[0]] + each[1]] = each[0]
			s[i + 1 + source] = max(preWeight.keys())
	return s


def tracePath(predecessors, s, source, sink):
	'''
	input the list of s, backtrace the full path
	'''
	path = []
	id = s.index(max(s))
	path.append(str(id))
	length = max(s)
	while length > 0:
		for each in predecessors[str(id)]:
			if length - each[1] == s[each[0]]:
				path.append(str(each[0]))
				length = length - each[1]
				id = each[0]
			else:
				continue
	return path


def main():
	source = 0
	sink = 44
	edges = []
	with open('test.txt', 'r') as inputData:
		for line in inputData:
			line = line.strip()
			# split the input with ':'
			edges.append(line.split(':'))
	for each in edges:
		# split the 'n->m' with '->'
		each[0] = each[0].split('->')
	# for each in edges, each[0][0] is the predecessor of each[0][1], each[1] is the weight of the edge
	predecessors = {}
	predecessors = buildGraph(edges)
	# print predecessors
	s = longestPath(predecessors, source, sink)
	print max(s)
	path = tracePath(predecessors, s, source, sink)
	print '->'.join(path[::-1])


if __name__ == '__main__':
	main()
