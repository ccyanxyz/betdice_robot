import subprocess
import time
import random

CLEOS = 'cleos --wallet-url http://127.0.0.1:8900 -u http://mainnet.genereos.io '

def getseed():
    charmap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    seed = ''
    for i in range(18):
        idx = random.randint(0, len(charmap) - 1)
        seed += charmap[idx]
    return seed

def create_memo(referal, rollUnder):
    memo = 'action:bet,seed:' + getseed() + ',rollUnder:' + str(rollUnder) + ',ref:' + referal
    return memo

def run(cmd):
    return subprocess.call(cmd, shell = True)

def run2(cmd):
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    ret = p.stdout.read()
    return ret

def bet(account, amount, memo):
    cmd = CLEOS + 'transfer ' + account + ' ' + betdice_account + ' ' +\
            "'" + str(amount) + " EOS' " + "'" + memo + "'"
    # print(cmd)
    # print("🎲 ", account, amount)
    run(cmd)

def unlock_wallet(wallet_name, wellet_password):
    cmd = CLEOS + 'wallet unlock -n ' + wallet_name + ' --password ' + wallet_password
    run(cmd)

def get_balance(account):
    cmd = CLEOS + 'get currency balance eosio.token ' + account +\
            " | awk '{print $1}'"

    ret = float(run2(cmd))
    return ret

def get_cpu(account):
    cmd = CLEOS + "get account " + account + " | grep available | awk 'NR==2 {print $2}'"
    # print(cmd)
    cpu_available = float(run2(cmd))
    return cpu_available

def get_ram(account):
    cmd = CLEOS + "get account " + account + " | grep available | awk 'NR==1 {print $2}'"
    ram_available = float(run2(cmd))
    return ram_available

if __name__ == '__main__':
    wallet_name = 'YOUR WALLET NAME'
    wallet_password = 'YOUR WALLET PASSWORD'
    account = 'YOUR EOS ACCOUNT'
    # I'll appreciate it if you don't change this
    referal = '11111to55555'
    betdice_account = 'betdiceadmin'
    # 0.95 probility to win
    rollUnder = 96
    # bet 0.1 EOS one time
    amount = 0.1
    
    # unlock wallet
    unlock_wallet(wallet_name, wallet_password)

    '''
    # test
    print('memo: ', create_memo(referal, rollUnder))
    print('balance: ', get_balance(account))
    print('cpu: ', get_cpu(account))
    print('ram: ', get_ram(account))
    '''

    while True:
        cpu = get_cpu(account)
        if cpu == 0:
            print('No cpu available, waiting...')
            time.sleep(1)
            continue

        balance1 = get_balance(account)
        memo = create_memo(referal, rollUnder)
        bet(account, amount, memo)
        print("🎲 ", account, amount, rollUnder)
        time.sleep(3)
        balance2 = get_balance(account)

        profit = balance2 - balance1
        print('profit: ', profit)
