import subprocess
import time
import random
import threading

CLEOS = 'cleos --wallet-url http://127.0.0.1:8900 -u http://mainnet.genereos.io '

def getseed():
    charmap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    seed = ''
    for i in range(64):
        idx = random.randint(0, len(charmap) - 1)
        # idx = len(charmap) - 1
        seed += charmap[idx]
    return seed

def create_memo(referal, rollUnder):
    # memo = 'action:bet,seed:' + getseed() + ',rollUnder:' + str(rollUnder) + ',ref:' + referal
    memo = str(rollUnder) + '-' + getseed() + '-' + referal
    return memo

def run(cmd):
    return subprocess.call(cmd, shell = True)

def run2(cmd):
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    ret = p.stdout.read()
    return ret

def onebet(account, amount, memo):
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
    print('cpu: ', cpu_available)
    return cpu_available

def get_ram(account):
    cmd = CLEOS + "get account " + account + " | grep available | awk 'NR==1 {print $2}'"
    ram_available = float(run2(cmd))
    return ram_available

def bet(account, amount, rollUnder, referal, betdice_account):
    while True:
        cpu = get_cpu(account)
        if cpu == 0:
            print('No cpu available, waiting...')
            continue

        memo = create_memo(referal, rollUnder)
        onebet(account, amount, memo)
        print(account, amount, rollUnder)
        time.sleep(3)

def watch_wallet(wallet_name, wallet_password):
    counter = 0
    while True:
        if counter % 30 == 0:
            unlock_wallet(wallet_name, wallet_password)
        counter += 1
        time.sleep(10)

if __name__ == '__main__':
    wallet_name = 'YOUR WALLET NAME'
    wallet_password = 'YOUR WALLET PASSWORD'
    account = 'YOUR EOS ACCOUNT'
    # I'll appreciate it if you don't change this
    referal = '11111to55555'
    betdice_account = 'funcity1main'
    # 0.95 probility to win
    rollUnder = 96
    # bet 0.1 EOS one time
    amount = 0.1

    # unlock wallet
    unlock_wallet(wallet_name, wallet_password)

    # bet(account, amount, rollUnder, referal, betdice_account)

    # multi threading
    threads = []
    for i in range(5):
        thread = threading.Thread(target = bet, args = (account, amount, rollUnder, referal, betdice_account))
        threads.append(thread)

    wallet_thread = threading.Thread(target = watch_wallet, args = (wallet_name, wallet_password))
    wallet_thread.start()

    print('starting...')
    for t in threads:
        t.start()
