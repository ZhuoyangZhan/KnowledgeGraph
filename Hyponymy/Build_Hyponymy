import pymysql
import opencc
from time import time
import pickle
dataset = []
synset = {}
start = time()
for idx, item in enumerate(data):
    try:
        upper = opencc.convert(item[1].decode().replace('\n','').replace('*',''))
        lower = opencc.convert(item[2].decode().replace('\n','').replace('*',''))
        category = item[-1].decode()
        if  category == 'page':
            if upper not in synset:
                synset[upper] = [lower]
            else:
                synset[upper].append(lower)
    except:
        upper = 'invalid'
        lower = 'invalid'
        category = 'invalid'
        print('invalid:', idx, item)
    dataset.append([upper, lower, category])
    if idx % 100000 == 0:
        print(idx, time()-start,'s')
        pickle.dump(dataset, open('relations','wb'))

def search_lower(terms):
    words = []

    def searcher(batch, words):
        new_add = []
        for w in batch:
            if w in u_d:
                cache = [word for word in u_d[w] if word not in words]
                words += cache
                new_add += cache
        return new_add, words
    
    new_add, words = searcher(terms, words)
    count = 0
    while len(new_add) != 0 and count <= 3:
        new_add, words = searcher(new_add, words)
        count += 1
        
    return words
    
def search_upper(terms):
    words = []

    def searcher(batch, words):
        new_add = []
        for w in batch:
            if w in d_u:
                cache = [word for word in d_u[w] if word not in words]
                words += cache
                new_add += cache
        return new_add, words
    
    new_add, words = searcher(terms, words)
    count = 0 
    while len(new_add) != 0 and count <= 2:
        new_add, words = searcher(new_add, words)
        count += 1
        
    return words

relations = {}
for idx, i in enumerate(dataset):
    if i[-1] == 'subcat':
        for term in i[:2]:
            if term not in relations:
                relations[term] = {'upper':[], 'lower':[]}
                try:
                    relations[term]['lower'] = search_lower([term])
                except:
                    print(i)
                try:
                    relations[term]['upper'] = search_upper([term])
                except:
                    print(i)    
                    
    if idx % 10000 == 0:
        print(idx)
