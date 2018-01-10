#-*- coding: utf-8 -*-
#%% import
from steem.blog import Blog
from steem import Steem
from steem.account import Account
from steem.post import Post
import io
import os.path
import json
import time
from functools import reduce
from pprint import pprint
from tinydb import TinyDB, Query
#%% db connect
db = TinyDB('db.json')
#%% config
b = 18850709
U = ['leesunmoo','jsg','ioc','sonamoo','kakaotalk','skt','krexchange','holic7', 'corn113', 'kwak']
#%% block num json

def BlockNumSave(L):
    with io.open('block.json','w') as fp:
        json.dump(L, fp)

if(os.path.exists('block.json') == False):
    L = dict(map(lambda u:(u,b), U))
    BlockNumSave(L)
else:
    with io.open('block.json','r') as fp:
        L = json.load(fp)
for u in U:
    if u not in L:
        L[u] = b
        BlockNumSave(L)
#%% crawl downvote
while True:
    try:
        ML = L.copy()
        R = []
        for u in U:
            for V in Account(u).history_reverse(filter_by="vote"):
                if V['weight'] < 0: #case downvote
                    if V['block'] <= L[u]:
                        break
                    print("[%s] %s -> %s (%s) : %s" % (V['timestamp'], V['voter'], V['author'], V['weight'], V['permlink']))
                    p = Post('@%s/%s' % (V['author'], V['permlink']))
                    V['title'] = p['title']
                    R.append(V)
                    ML[u] = max([V['block'], ML[u]])
        L = ML.copy()
        BlockNumSave(L)
        for r in R:
            db.insert(r)
        print("COOLDOWN 1 min")
        time.sleep(60)
    except Exception as e:
        print("failed with error code: {}".format(e))
