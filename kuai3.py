import subprocess
import time
import sys
import re
import json
import random
import threading
import requests as req

CLEOS = 'cleos --wallet-url http://127.0.0.1:8900 -u http://mainnet.genereos.io '

def run(cmd):
    return subprocess.call(cmd, shell = True)

def run2(cmd):
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    ret = p.stdout.read()
    return ret

def get_price(token = 'city_eos'):
    url = 'https://api.newdex.io/v1/ticker/price'
    payload = { 'symbol': token }
    ret = json.loads(req.get(url, params = payload).text)
    current_price = ret['data']['price']
    # print(current_price)
    return current_price

def get_block_num():
    url = 'https://api.eosnewyork.io/v1/chain/get_info'
    ret = json.loads(req.get(url).text)

    head_block_num = ret['head_block_num']
    last_irreversible = ret['last_irreversible_block_num']
    
    # print('head:', head_block_num)
    # print('irreversible:', last_irreversible)

    return head_block_num, last_irreversible

def get_block_hash(block_num):
    url = 'https://api.eosnewyork.io/v1/chain/get_block'
    payload = { 'block_num_or_id': block_num }
    
    try:
        ret = json.loads(req.post(url, json = payload).text)
        block_hash = ret['id']
    except KeyboardInterrupt:
        exit()
    except:
        return block_num, None, None

    # print(block_num, block_hash)
    # get a num in 1-6
    num = None
    l = list(block_hash)
    for i in reversed(l):
        if i in ['1', '2', '3', '4', '5', '6']:
            num = i
            break

    return block_num, block_hash, num

if __name__ == '__main__':
    block_num, _ = get_block_num()
    nums = [0, 0, 0]
    cur = 0
    while True:
        # block_num, _ = get_block_num()
        block_num, block_hash, num = get_block_hash(block_num)
        if block_hash is None:
            continue
        else:
            nums[cur % 3] = int(num)
            cur += 1
            print(block_num, block_hash, num, sum(nums))
            block_num += 1
