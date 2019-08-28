from utils.util import *
from gen_existence_proof import gen_existence_proof


def verify_existence_proof(proof):
    (block_header, tx_hash, trie_proof, trie_keys, v, r, s) = proof
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


if __name__ == "__main__":
    # Test case 1: 0x14198912703598b497ffbe17e6a90ffa85de276418ae41d217c0e3d2c76290d7
    # Test case 2: 0x0661d6e95ab1320e93165c37b0e666c96c97b49a8819c02a8cda05c38ff5a97d
    # Test case 3: 0x949ae094deb031cbcfb1aaf36ca62b49d5e1d34affbbda16f7323568d8ac2689
    # Test case 4: 0x1e39d5b4b46d420e960e12ba2544988bc11c4d4e8c12ceca4871d306afd73d44
    existence_proof = gen_existence_proof(0x14198912703598b497ffbe17e6a90ffa85de276418ae41d217c0e3d2c76290d7)
    print(verify_existence_proof(existence_proof))

    existence_proof = gen_existence_proof(0x0661d6e95ab1320e93165c37b0e666c96c97b49a8819c02a8cda05c38ff5a97d)
    print(verify_existence_proof(existence_proof))

    existence_proof = gen_existence_proof(0x949ae094deb031cbcfb1aaf36ca62b49d5e1d34affbbda16f7323568d8ac2689)
    print(verify_existence_proof(existence_proof))

    existence_proof = gen_existence_proof(0x1e39d5b4b46d420e960e12ba2544988bc11c4d4e8c12ceca4871d306afd73d44)
    print(verify_existence_proof(existence_proof))
