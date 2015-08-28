#!/usr/bin/env python

'''
input a source node and a sink node of a graph, followed by a list of edges and their weight in the graph
output the longest path from source to sink in the graph followed by its length
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
		predecessors[int(each[0][1])] = []
	# build the graph, more than one edges may be exist to one node
	for each in edges:
		predecessors[int(each[0][1])].append([int(each[0][0]), int(each[1])])
	return predecessors


def longestPath(predecessors, source, sink):
	'''
	find the longest path in the graph
	input a dict with edges
	output the length of longest path in the graph
	'''
	s = {}
	keys = predecessors.keys()
	keys.sort()
	for key in keys:
		s[key] = 0
		s[source] = 0
	for key in predecessors.keys():
		preWeight = []
		for each in predecessors[key]:
			preWeight.append(s[each[0]] + each[1])
		s[key] = max(preWeight)
	return s


def tracePath(predecessors, s, source, sink):
	'''
	input the dict of s, backtrace the full path
	'''
	path = []
	id = sink
	path.append(str(id))
	length = s[id]
	while length > 0:
		for each in predecessors[id]:
			if length - each[1] == s[each[0]]:
				path.append(str(each[0]))
				length = length - each[1]
				id = each[0]
			else:
				continue
	return path


def main():
	source = 12
	sink = 19
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
	fromSink = []
	currentNode = []
	for each in edges:
		if each[0][0] == str(source):
			fromSink.append(each)
			currentNode.append(each[0][1])
	currentSink = source
	while currentSink <= sink:
		for each in edges:
			if each[0][0] in currentNode:
				fromSink.append(each)
				currentNode.append(each[0][1])
				currentSink = max(currentNode)
	predecessors = {}
	predecessors = buildGraph(fromSink)
	# print predecessors
	s = longestPath(predecessors, source, sink)
	print s[sink]
	path = tracePath(predecessors, s, source, sink)
	print '->'.join(path[::-1])


if __name__ == '__main__':
	main()
