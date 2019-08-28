from eth_typing import (
    Hash32
)
from typing import (
    Dict, Sequence, Tuple
)
from rlp.sedes import (
    Binary,
    big_endian_int,
    binary
)
import rlp
from eth_utils import (
    keccak,
)
from trie import HexaryTrie
from web3.auto.infura import w3

address = Binary.fixed_length(20, allow_empty=True)


class _Transaction(rlp.Serializable):
    fields = [
        ('nonce', big_endian_int),
        ('gas_price', big_endian_int),
        ('gas', big_endian_int),
        ('to', address),
        ('value', big_endian_int),
        ('data', binary),
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int)
    ]


BLANK_ROOT_HASH = Hash32(b'V\xe8\x1f\x17\x1b\xccU\xa6\xff\x83E\xe6\x92\xc0\xf8n\x5bH\xe0\x1b\x99l\xad\xc0\x01b/\xb5\xe3c\xb4!')
Transactions = Sequence[_Transaction]
TrieRootAndData = Tuple[Hash32, Dict[Hash32, bytes]]

block = w3.eth.getBlock(8290728)
trie = HexaryTrie(db={})
assert trie.root_hash == BLANK_ROOT_HASH
print(w3.toHex(trie.root_hash))

txs = []
B = len(block.transactions)
for key in range(B):
    tx = w3.eth.getTransaction(block.transactions[key])
    raw_tx = _Transaction(
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
    txs.append(raw_tx)
    trie.set(rlp.encode(key), rlp_tx)
assert block.transactionsRoot == trie.root_hash


# Generate Merkle tree proof for per each node
proofs = []
for key in range(B):
    proof = trie.get_proof(rlp.encode(key))
    proofs.append(proof)

# Verify Merkle tree proof for per each node
nodes = []
for key in range(B):
    node = HexaryTrie.get_from_proof(trie.root_hash, rlp.encode(key), proofs[key])
    nodes.append(node)
    assert nodes[key] == rlp.encode(txs[key])
    print(key, proofs[key], nodes[key])

print(True)
