import jieba

str = '很好看的电影'
ret = jieba.cut(str, cut_all=True)
print(ret)

for factor in ret:
    print(factor)
