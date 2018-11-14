import subprocess
import time
import re
import json
import random
import threading

CLEOS = 'cleos --wallet-url http://127.0.0.1:8900 -u http://mainnet.genereos.io '

def run(cmd):
    return subprocess.call(cmd, shell = True)

def run2(cmd):
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    ret = p.stdout.read()
    return ret

def unlock_wallet(wallet_name, wellet_password):
    cmd = CLEOS + 'wallet unlock -n ' + wallet_name + ' --password ' + wallet_password
    run(cmd)

def watch_wallet(wallet_name, wallet_password):
    counter = 0
    while True:
        if counter % 30 == 0:
            unlock_wallet(wallet_name, wallet_password)
        counter += 1
        time.sleep(1)

def bid():
    cmd = CLEOS + 'get table funcityturbo funcityturbo gamepool'
    r = re.compile('^[1-9]\\d*\\.\\d*|0\\.\\d*[1-9]\\d*$')
    while True:
        ret = json.loads(str(run2(cmd).decode()))
        # print(ret)
        current = ret['rows'][0]['price']
        current = r.match(current).group(0)
        idx = str(current).index('.')
        print(current)
        if float(current) <= 500:
            bid_cmd = CLEOS + f'push action funcitytoken transfer \'["11111to55555","funcityturbo","{current} CITY", "W#+PY81Ux2~q;otG:&dcVgd^uG"]\' -p 11111to55555@active' 
            print(bid_cmd)
            run(bid_cmd)

if __name__ == '__main__':
    wallet_name = 'YOUR WALLET NAME'
    wallet_password = 'YOUR WALLET PASSWORD'
    # unlock wallet
    unlock_wallet(wallet_name, wallet_password)

    threads = []
    for i in range(10):
        thread = threading.Thread(target = bid)
        threads.append(thread)

    wallet_t = threading.Thread(target = watch_wallet, args = (wallet_name, wallet_password))
    wallet_t.start()

    for t in threads:
        t.start()
