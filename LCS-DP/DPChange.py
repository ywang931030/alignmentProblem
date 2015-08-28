#!/usr/bin/env python

'''
input a number MONEY and an array COINS(COINi,...), calculate the mininum number of coins needed to changes MONEY
output this number
'''


def DPChange(money, coins):
    '''
    money is an integer, while coins represent an array of coins in type of list
    '''
    minNumCoins = []
    minNumCoins.append(0)
    Inf = float('Inf')
    '''
    float() ensure the type is int but not str.
    '''
    for m in range(money):
    	'''
        range(money) is from 0, however, we need money count from 1, so we should add 1 to m.
        '''
        minNumCoins.append(Inf)
        '''
        we set every minNumCoins[m] is Infinite
        '''
        for i in xrange(len(coins)):
            if m + 1 >= coins[i]:
                if minNumCoins[m - coins[i] + 1] + 1 < minNumCoins[m + 1]:
                    minNumCoins[m + 1] = minNumCoins[m - coins[i] + 1] + 1
    return minNumCoins[money]


def main():
    money = 16876
    coins = [21, 14, 11, 7, 5, 3, 1]
    mininum = DPChange(money, coins)
    print mininum


if __name__ == '__main__':
    main()
