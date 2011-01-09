# coding: utf-8
from decimal import Decimal
from collections import defaultdict
TYPES = [u'股票', u'债券', u'保本', u'指数', u'货币']
def adjustfund(holdlist, config, suggest, pool):
    '''
    基金类型： 股票 债券 保本 指数 货币
    依赖 holdlist 用户基金持仓比例： [(基金代码，基金类型，比例)]
         suggest 基金评级建议：{基金代码：建议}
         config 符合用户偏好的配置比例：{基金类型：比例}
         pool 符合用户偏好的基金池：{基金类型：[(基金代码, 评分)]}
    返回：新的持仓比例 [(基金代码，基金类型，比例，操作)]
    '''
    assert sum(p for _,_,p in holdlist) == 100, sum(p for _,_,p in holdlist)
    # 根据评级建议，该赎回的全部赎回
    holdlist = [
        (fundcode, type, 0) if suggest.get(fundcode, u'持有')==u'赎回' else (fundcode, type, percent)
        for fundcode, type, percent in holdlist
        ]

    remainder = 100 - sum(p for _,_,p in holdlist)

    fundpercent = defaultdict(Decimal)
    fundpercent.update((f, p) for f,_,p in holdlist)
    fundoper = {}

    fundtype = dict( (f, t) for f,t,_ in holdlist )
    fundscore = dict( (f,s) for l in pool.values() for (f,s) in l )

    typepercent = defaultdict(Decimal)
    typefund = defaultdict(list)
    for f,t,p in holdlist:
        typefund[t].append(f)
        typepercent[t] += p

    typediff = {}
    for type in TYPES:
        # 按照资产配置要求，计算每种类型基金的调整比例
        diff = typediff[type] = config.get(type, 0) - typepercent.get(type, 0)
        if diff==0:
            continue
        # 按照调整比例，从每种类型基金中挑选基金进行调整，
        # 加仓：挑选分数最高的，
        #       如果不持有该类型基金，则挑选基金池中分数最高的
        #       如果持有基金中没有基金池评分的
        # 赎回：优先挑选分数低的，循环进行

        l = typefund[type][:]
        if diff>0:
            holdpoolfund = filter(lambda (f,s): f in l, pool[type])
            if holdpoolfund:
                f,_ = max(holdpoolfund, key=lambda (_,s):s)
                fundoper[f] = (u'加仓', diff)
            else:
                f,_ = max(pool[type], key=lambda (_,s):s)
                fundoper[f] = (u'申购', diff)

            fundpercent[f] += diff
            # f 可能是新增基金，补充基金类型映射
            fundtype[f] = type
        else:
            assert l
            l.sort(key=lambda f:fundscore.get(f, 0))
            count = abs(diff)
            while l and count:
                f = l.pop(0)
                if fundpercent[f]>=count:
                    fundpercent[f] -= count
                    count = 0
                    fundoper[f] = (u'赎回', count)
                else:
                    count -= fundpercent[f]
                    fundoper[f] = (u'赎回', fundpercent[f])
                    fundpercent[f] = 0
            assert count==0

    newholdlist = [(f, fundtype[f], p, fundoper.get(f, (u'持有',0))) for f,p in fundpercent.items()]

    # 验证数据一致性
    assert sum(p for _,_,p,_ in newholdlist) == 100, sum(p for _,_,p in newholdlist)
    newtypepercent = defaultdict(Decimal)
    for _,t,p,_ in newholdlist:
        newtypepercent[t] += p
    assert all(newtypepercent[t]==config[t] for t in TYPES)

    return newholdlist
