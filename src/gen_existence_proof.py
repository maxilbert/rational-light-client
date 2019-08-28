from utils.util import *


def gen_existence_proof(tx_hash):
    tx = w3.eth.getTransaction(tx_hash)
    block_number = tx.blockNumber
    block = w3.eth.getBlock(block_number)
    # print(block_number)
    print(tx_hash)

    # Genenate rlp Block header
    block_raw = BlockHeader(
        w3.toBytes(hexstr=w3.toHex(block.parentHash)),
        w3.toBytes(hexstr=w3.toHex(block.sha3Uncles)),
        w3.toBytes(hexstr=block.miner),
        w3.toBytes(hexstr=w3.toHex(block.stateRoot)),
        w3.toBytes(hexstr=w3.toHex(block.transactionsRoot)),
        w3.toBytes(hexstr=w3.toHex(block.receiptsRoot)),
        w3.toInt(block.logsBloom),
        block.difficulty,
        block.number,
        block.gasLimit,
        block.gasUsed,
        block.timestamp,
        block.extraData,
        block.mixHash,
        block.nonce
    )
    block_rlp = rlp.encode(block_raw)

    # Generate Merkle trie of transactions
    tx_index = 0
    tx_rlp = b''
    trie = HexaryTrie(db={})
    txs = []
    for key in range(len(block.transactions)):
        tx = w3.eth.getTransaction(block.transactions[key])
        raw_tx = Transaction(
            tx.nonce,
            tx.gasPrice,
            tx.gas,
            w3.toBytes(hexstr=tx.to),
            tx.value,
            w3.toBytes(hexstr=w3.toHex(hexstr=tx.input)),
            tx.v,
            w3.toInt(tx.r),
            w3.toInt(tx.s)
        )
        rlp_tx = rlp.encode(raw_tx)
        assert tx.hash == keccak(rlp_tx)
        if int.from_bytes(tx.hash, "big") == tx_hash:
            tx_index = key
            tx_rlp = rlp_tx
        txs.append(raw_tx)
        trie.set(rlp.encode(key), rlp_tx)
    assert block.transactionsRoot == trie.root_hash

    # Generate Merkle trie proof for per each node
    trie_proof = trie.get_proof(rlp.encode(tx_index))
    trie_proof_rlp = [rlp.encode(node) for node in trie_proof]

    # Get keys for verifying proof
    trie_keys = [None] * len(trie_proof)
    for i in range(len(trie_proof) - 1):
        child_hash = keccak(rlp.encode(trie_proof[i+1]))
        for j in range(len(trie_proof[i])):
            if trie_proof[i][j] == child_hash:
                trie_keys[i] = j
    for j in range(len(trie_proof[-1])):
        if trie_proof[-1][j] == tx_rlp:
            trie_keys[-1] = j

    # Generate Signature for the existence proof
    digest = keccak(
        encode_abi(
            ['bytes', 'bytes32', 'bytes[]', 'uint[]'],
            (block_rlp, w3.toBytes(tx_hash), trie_proof_rlp, trie_keys)
        )
    )
    sig = w3.eth.account.signHash(digest, private_key=sk_rfn_1)
    addr_1 = w3.eth.account.recoverHash(digest, signature=sig.signature)
    addr_2 = w3.eth.account.recoverHash(digest, vrs=(sig.v, sig.r, sig.s))
    addr_3 = w3.eth.account.from_key(sk_rfn_1)
    assert(addr_1 == addr_3.address)
    assert(addr_2 == addr_3.address)

    return block_rlp, w3.toBytes(tx_hash), trie_proof_rlp, trie_keys, sig.v, w3.toBytes(sig.r), w3.toBytes(sig.s)


if __name__ == "__main__":
    # Test case 1: 0x14198912703598b497ffbe17e6a90ffa85de276418ae41d217c0e3d2c76290d7
    # Test case 2: 0x0661d6e95ab1320e93165c37b0e666c96c97b49a8819c02a8cda05c38ff5a97d
    # Test case 3: 0x949ae094deb031cbcfb1aaf36ca62b49d5e1d34affbbda16f7323568d8ac2689
    # Test case 4: 0x1e39d5b4b46d420e960e12ba2544988bc11c4d4e8c12ceca4871d306afd73d44
    existence_proof = gen_existence_proof(0x14198912703598b497ffbe17e6a90ffa85de276418ae41d217c0e3d2c76290d7)
    (block_header, tx_hash, trie_proof, trie_keys, v, r, s) = existence_proof
    print(
        w3.toHex(block_header), '\n',
        w3.toHex(tx_hash), '\n',
        [w3.toHex(node) for node in trie_proof], '\n',
        trie_keys, '\n',
        v, w3.toHex(r), w3.toHex(s)
    )
