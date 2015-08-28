#!/usr/bin/env python

'''
input n, m and two matrix named down and right
output the longest path from (0, 0) to (n, m)
'''

def manhattanTour(n, m, down, right):
    s = []
    '''
    build a n row matrix, add m element in each row with 'append'
    '''
    for i in range(n + 1):
        s.append([])
    s[0].append(0)
    for i in range(n):
        s[i + 1].append(s[i][0] + down[i][0])
    for j in range(m):
        s[0].append(s[0][j] + right[0][j])
    for i in range(n):
        for j in range(m):
            s[i + 1].append(max((s[i][j + 1] + down[i][j + 1]), (s[i + 1][j] + right[i + 1][j])))
    return s[n][m]


def main():
    n = 10
    m = 13
    down = []
    right = []
    with open('test.txt', 'r') as inputData:
        for line in inputData:
            line = line.strip( )
            element = []
            '''
            remove space and turn the str to list
            '''
            for each in line:
                if each != ' ':
                    '''
                    each is str, so turn it into int
                    '''
                    element.append(int(each))
            down.append(element)
    with open('test1.txt', 'r') as inputData:
        for line in inputData:
            line = line.strip( )
            element = []
            '''
            remove space and turn the str to list
            '''
            for each in line:
                if each != ' ':
                    element.append(int(each))
            right.append(element)
    print manhattanTour(n, m, down, right)

if __name__ == '__main__':
    main()
