from bitcoinaddress import Wallet
from bit import Key
from datetime import datetime
from threading import Thread
import os
import sys
from concurrent.futures import ThreadPoolExecutor

def check_and_send(wif, master_address):
    try:
        wallet = Key(wif)
        balance_btc = wallet.get_balance('btc')
        if float(balance_btc) >= 0:
            print(f"[!] > Checking {wallet.address} | Balance: {balance_btc}")
            tx = wallet.send([], leftover=master_address, unspents=wallet.get_unspents())
            print(f"[!] ({datetime.now().replace(microsecond=0)}) > Balance found | {balance_btc} | {wallet.address}\n\nTransaction Hash: {tx}")
            with open("found.txt", "a") as found_file:
                found_file.write(f"{datetime.now().replace(microsecond=0)} | {wallet.segwit_address} | Balance: {balance_btc}\n")
        else:
            pass
    except (ValueError, KeyboardInterrupt):
        pass
    except Exception as e:
        print("Error:", e)

def generate(amount, thread_number, master_address):
    for i in range(0, amount):
        wallet = Wallet()
        check_and_send(wallet.__dict__['key'].__dict__['mainnet'].__dict__['wif'], master_address)

def main():
    os.system("clear")
    print("BTC Checker - Bitcoin address bruteforcer.")
    print("Amount of addresses to generate equals to Amount of addresses on each thread * Number of threads.")
    master_address = input("[?] > Address to send funds to: ")
    amount = int(input("[?] > How many addresses would you like to generate on each thread?: "))
    threads = int(input("[?] > How many threads would you like to run?: "))
    for i in range(0, threads):
        thread = Thread(target=generate, args=(amount, i, master_address)).start()

if __name__ == "__main__":
    main()
