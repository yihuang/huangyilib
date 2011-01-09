#!/usr/bin/python
# coding: utf-8
from decimal import Decimal
from jjc2 import adjustfund

TEST_CONFIG = {
    u'成长型': {
        u'股票': 100,
        u'债券': 0,
        u'保本': 0,
        u'货币': 0,
        u'指数': 0,
    },
    u'稳健型': {
        u'股票': 80,
        u'债券': 20,
        u'保本': 0,
        u'货币': 0,
        u'指数': 0,
    },
    u'防御型': {
        u'股票': 60,
        u'债券': 20,
        u'保本': 0,
        u'货币': 20,
        u'指数': 0,
    },
    u'保本型': {
        u'股票': 0,
        u'债券': 40,
        u'保本': 30,
        u'货币': 30,
        u'指数': 0,
    },
}
def test():
    holdlist = [
        ('450008', u'股票', Decimal('25.6900')),
        ('519690', u'股票', Decimal('25.5000')),
        ('481010', u'股票', Decimal('16.8000')),
        ('519087', u'股票', Decimal('16.3000')),
        ('481009', u'股票', Decimal('8.8100')),
        ('460005', u'股票', Decimal('6.9000')),
    ]
    config = TEST_CONFIG[u'稳健型']
    suggest = {
        '450008': u'赎回',
        '519690': u'赎回',
        '481009': u'赎回',
    }
    pool = {
        u'股票': [
            ('350005', 0),
            ('210003', 0),
            ('000031', 0),
            ('000021', 0),
            ('630002', 0),
        ],
        u'债券': [
            ('080003', 0),
            ('100035', 0),
            ('630003', 0),
            ('410004', 0),
        ],
        u'保本': [],
        u'货币': [],
        u'指数': [],
    }
    newfundlist = adjustfund(holdlist, config, suggest, pool)
    for f,t,p,(oper,diff) in newfundlist:
        print u'\t'.join(map(unicode, [f,t,p,oper,diff]))

if __name__ == '__main__':
    test()
