# -*- coding:utf-8 -*-

from numpy import random
K = [1,2,3,4,5] # 设总的要比数为5个
R = {1:2,2:3,3:5,4:1,5:9}  # 各个摇臂对应的奖赏
prob = {1:0.6,2:0.5,3:0.2,4:0.7,5:0.05} # 各个摇臂对应的概率吐币的概率
T =10000
epsion = 0.1
count = dict(zip(list(range(1,6)),[0]*5))  # 计算每个摇臂的摇到的次数

r = 0
for i in range(T):
    Q = dict(zip(list(range(1,6)),[0]*5))

    if random.random() < epsion:
        k = random.choice(K)
    else:
        k = max(Q,key=Q.get)

    v = random.choice([R[k],0],p = [prob[k],1-prob[k]])
    r += v
    Q[k] = (Q[k]*count[k] + v)/(count[k]+1)

    count[k] = count[k] + 1
print("end the reward is {0}".format(r))