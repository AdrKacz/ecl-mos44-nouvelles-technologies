# For color see: https://stackoverflow.com/questions/9781218/how-to-change-node-jss-console-font-color

import time
import hashlib
import random
import rsa

class Transaction:
    def __init__(self, amount : float, payer : rsa.PublicKey, payee : rsa.PublicKey) -> None:
        self.amount : float = amount
        self.payer : rsa.PublicKey = payer # public key
        self.payee : rsa.PublicKey = payee # public key

    def __str__(self) -> str:
        s : str = '\x1b[1mTransaction\x1b[0m\n'
        for attr, value in self.__dict__.items():
            s += f'{attr:<20}:\t{value}\n'
        return s

    def display(self, indent : str = '\t') -> str:
        s : str = '\n'
        for attr, value in self.__dict__.items():
            if isinstance(value, rsa.PublicKey):
                s += f'{indent}{attr:<20}:\t{value.n}\n'
            else:
                s += f'{indent}{attr:<20}:\t{value}\n'
        return s

class Block:
    def __init__(self, prev_block_hash : str, transaction : Transaction) -> None:
        self.prev_block_hash : str = prev_block_hash
        self.transaction : Transaction = transaction
        self.ts : float = time.time()
        self.nonce : int = round(random.random() * 999999999) # Used to mine the block
    
    @property
    def hash(self) -> str:
        hash_256 = hashlib.new('sha256')
        hash_256.update(str(self).encode('utf-8'))
        return hash_256.hexdigest()


    def __str__(self) -> str:
        s : str = '\x1b[1mBlock\x1b[0m\n'
        for attr, value in self.__dict__.items():
            if isinstance(value, Transaction):
              s += f'\x1b[4m{attr}\x1b[0m\t{value.display()}\n'
            else:  
                s += f'{attr:<20}:\t{value}\n'
        return s


class Chain:
    # Initialiase chain with Genesis block
    genesis : tuple[rsa.PublicKey, rsa.PrivateKey] = rsa.newkeys(512);
    satoshi : tuple[rsa.PublicKey, rsa.PrivateKey] = rsa.newkeys(512)
    chain : list[Block] = [Block(None, Transaction(100, genesis[0], satoshi[0]))]
    def __init__(self) -> None:
        # Only one chain, use singleton and duplication
        pass

    def mine(nonce : int) -> None:
        """
        Find a value that starts with 4 0's
        """
        solution = 1
        print('\x1b[1mMining ...\x1b[0m')
        while True:
            hash = hashlib.new('md5') # faster to compute than SHA-256 (128 bytes long)
            hash.update((str(nonce + solution)).encode('utf-8'))
            attempt : str = hash.hexdigest()
            if attempt[:4] == '0000':
                print(f'\tSolved: {solution}')
                return solution
            solution += 1

    def add_block(transaction : Transaction, sender_public_key : rsa.PublicKey, signature : bytes) -> None:
        is_valid : str = rsa.verify(str(transaction).encode('utf-8'), signature, sender_public_key)
        if is_valid == 'SHA-256':
            new_block = Block(Chain.chain[-1].hash, transaction)
            Chain.mine(new_block.nonce)
            Chain.chain.append(new_block)


class Wallet:
    def __init__(self) -> None:
        keypair : tuple[rsa.PublicKey, rsa.PrivateKey] = rsa.newkeys(512) # (pub, priv)
        self.public_key : rsa.PublicKey = keypair[0]
        self.private_key : rsa.PrivateKey = keypair[1]

    def send_money(self, amount : float, payee_public_key : rsa.PublicKey) -> None:
        transaction : Transaction = Transaction(amount, self.public_key, payee_public_key)

        signature : bytes = rsa.sign(str(transaction).encode('utf-8'), self.private_key, 'SHA-256')
        Chain.add_block(transaction, self.public_key, signature)
    
    def __str__(self) -> str:
        s : str = '\x1b[1mWallet\x1b[0m\n'
        for attr, value in self.__dict__.items():
            s += f'{attr:<20}:\t{value}\n'
        return s

        

if __name__ == '__main__':
    print('Hello Crypto!')
    alice = Wallet()
    bob = Wallet()
    marc = Wallet()
    sam = Wallet()

    marc.send_money(50, alice.public_key)
    bob.send_money(23, alice.public_key)
    alice.send_money(5, bob.public_key)

    for i, b in enumerate(Chain.chain):
        print(f'\n\x1b[2m-- {i:^3} --\x1b[0m')
        print(b)

    
