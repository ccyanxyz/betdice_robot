## EOS dice game robot

Requirements: cleos, keosd, nodeos, python3

Replace these fields with your own wallet and account info:
```python
wallet_name = 'YOUR WALLET NAME'
wallet_password = 'YOUR WALLET PASSWORD'
account = 'YOUR EOS ACCOUNT'
```

Run:
```shell
keosd > keosd.log 2>&1 &
python3 betdice.py
```

