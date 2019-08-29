from utils.util import *
from gen_existence_proof import gen_existence_proof
import sys, datetime


def verify_existence_proof(proof):
    (block_header, tx_hash, trie_proof, trie_keys, v, r, s) = proof
    digest = keccak(
        encode_abi(
            ['bytes', 'bytes32', 'bytes[]', 'uint[]'],
            (block_header, tx_hash, trie_proof, trie_keys)
        )
    )
    if verify_sig(digest, v, r, s) not in [addr_rfn_1, addr_rfn_2]:
        return False
    node_hash = rlp.decode(block_header)[4]
    i = 0
    while i < len(trie_proof) - 1:
        if node_hash != keccak(trie_proof[i]):
            return False
        node = rlp.decode(trie_proof[i])
        node_hash = node[trie_keys[i]]
        i += 1
    if node_hash != keccak(trie_proof[i]):
        return False
    node = rlp.decode(trie_proof[i])
    tx_rlp = node[trie_keys[i]]
    if tx_hash != keccak(tx_rlp):
        return False
    return True


def verify_sig(digest, v, r, s):
    addr = w3.eth.account.recoverHash(digest, vrs=(v, r, s))
    return w3.toInt(hexstr=addr)


# Test case 1: 0x14198912703598b497ffbe17e6a90ffa85de276418ae41d217c0e3d2c76290d7
# Test case 2: 0x0661d6e95ab1320e93165c37b0e666c96c97b49a8819c02a8cda05c38ff5a97d
# Test case 3: 0x949ae094deb031cbcfb1aaf36ca62b49d5e1d34affbbda16f7323568d8ac2689
# Test case 4: 0x1e39d5b4b46d420e960e12ba2544988bc11c4d4e8c12ceca4871d306afd73d44
# Test case 5: 0xfe28a4dffb8ece2337863fba8dfd2686e9a9c995b50fe7911acbb2589f80b315
if __name__ == "__main__":

    test_tx_vector = [
        0xfe28a4dffb8ece2337863fba8dfd2686e9a9c995b50fe7911acbb2589f80b315,
        0x14198912703598b497ffbe17e6a90ffa85de276418ae41d217c0e3d2c76290d7,
        0x0661d6e95ab1320e93165c37b0e666c96c97b49a8819c02a8cda05c38ff5a97d,
        0x949ae094deb031cbcfb1aaf36ca62b49d5e1d34affbbda16f7323568d8ac2689,
        0x1e39d5b4b46d420e960e12ba2544988bc11c4d4e8c12ceca4871d306afd73d44
    ]

    for tx in test_tx_vector:

        print("tx to query: ", w3.toHex(tx))

        existence_proof_1 = gen_existence_proof(tx)
        print("communication with rfn1 in bytes: ", sys.getsizeof(rlp.encode(existence_proof_1)))

        existence_proof_2 = gen_existence_proof(tx)
        print("communication with rfn2 in bytes: ", sys.getsizeof(rlp.encode(existence_proof_2)))

        t_start = datetime.datetime.now()
        flag1 = verify_existence_proof(existence_proof_1)
        t_end = datetime.datetime.now()
        delta = t_end - t_start
        print("time to verify proof from rfn1: ", delta.total_seconds() * 1000)
        print(flag1)

        t_start = datetime.datetime.now()
        flag2 = verify_existence_proof(existence_proof_2)
        t_end = datetime.datetime.now()
        delta = t_end - t_start
        print("time to verify proof from rfn2: ", delta.total_seconds() * 1000)
        print(flag2)

        print('\n')
