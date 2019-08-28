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

# Generate Merkle tree
txs = []
B = len(block.transactions)
print("The block has %d transactions" % B)
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
    # print(rlp_tx)
assert block.transactionsRoot == trie.root_hash
print(w3.toHex(trie.root_hash))

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
    print("proof of key %d:" % key, proofs[key], nodes[key])


print(True)

proof = proofs[3]
print(proof)
print(proof[0])
print(w3.toHex(rlp.encode(proof[0])))
print(w3.toHex(keccak(rlp.encode(proof[0]))))


print(proof[1])
print(w3.toHex(rlp.encode(proof[1])))
print(keccak(rlp.encode(proof[1])))

print(proof[2])
print(w3.toHex(rlp.encode(proof[2])))
print(keccak(rlp.encode(proof[2])))



#([b'\xa5b\xf8\xad\xe1\xbd\xb4\x9e8\x02F\x16*\xc1\x00/3b\x1a\xceg\xbc\x06*\xfa\xf9R\x15B3F7', b'', b'', b'', b'', b'', b'', b'', b'Q\xb7[\xd5\xa9^X.\x974\x18\xe8xG:|\xc2\xce*\x98\xc9I_\n\x03?\x83\xa5\x7f\r\xed\x03', b'', b'', b'', b'', b'', b'', b'', b''],
# [b'', b'\xe9\xaf\xd1\xa6v\x94I\x17\x86>\xdc\x8b\xef\x03_]0\xab\xbaq\x14\xa1\x08l\x94J\xafP5\x06\x17\xfe', b"\x11K\x92\xdfR\xbd5\xe7\x9e\xc7\x02\xf0\xc4\xc1|\x1b\xa0'>\x98\xc9\xa5\xb8\x10\x03\xfb!\xbd\xb0\x9f\xfc\xd8", b'\x84\x8f\x1f]FR.\xf26Ee\xdf3\xa0\x90\xb4-\x7fB(-\xf0\x87\xf9}x\xea\xe3\x84\xe2\x8c\x01', b'SU\x92M\r\xf1\xce\xa2~\x89f\xa9\xee\x96\xd1\xc41\xa2\rW\t\xac\xc7:w\x85+1*4\x0f\xa0', b'X\x80P\xf1I]\xb6\xcb\xafM`\xb4\x0c\x1dD\xb2\xca\r|\x87x\x84z\xcd\xf0\x02\xc5\xe9\xbe4\x1b;', b'\x92\x05\xad\xaf \xcc\xd4\xe4\x95X\x0b\x1a\n\xd9`\x07\xf5\x9f\xffN\x16\xe0\x85\x8faD\xf9\x1c\xda\x9du6', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
# [b' ', b'\xf8l\x02\x85\x02T\x0b\xe4\x00\x82R\x08\x94\x1b\x9c\x9cU\x03\x98\x98A}\xf7I\x98\xe0\x04t\xaeb\xa2@[\x88\x0fD\xbb*tU \x00\x80&\xa0\x91Bl\xf2R\x9cVS\xd2\xddp\x85W\x1a\xa4[\xe7\xdd%\xe3[l\xc7\x0f\xec\x86_]T\x96c0\xa0Z%w\xd3\xb9<\xd6\xa4\xcd\xe58_\xc3\xcd\xb3\x16\x0e\x04\xeb\x8e\xbcp;\xd0\xfb\xd9i\xc8!k!6'])

# ["0xf851a0a562f8ade1bdb49e380246162ac1002f33621ace67bc062afaf952154233463780808080808080a051b75bd5a95e582e973418e878473a7cc2ce2a98c9495f0a033f83a57f0ded038080808080808080","0xf8d180a0e9afd1a676944917863edc8bef035f5d30abba7114a1086c944aaf50350617fea0114b92df52bd35e79ec702f0c4c17c1ba0273e98c9a5b81003fb21bdb09ffcd8a0848f1f5d46522ef2364565df33a090b42d7f42282df087f97d78eae384e28c01a05355924d0df1cea27e8966a9ee96d1c431a20d5709acc73a77852b312a340fa0a0588050f1495db6cbaf4d60b40c1d44b2ca0d7c8778847acdf002c5e9be341b3ba09205adaf20ccd4e495580b1a0ad96007f59fff4e16e0858f6144f91cda9d753680808080808080808080", "0xf87120b86ef86c028502540be400825208941b9c9c55039898417df74998e00474ae62a2405b880f44bb2a745520008026a091426cf2529c5653d2dd7085571aa45be7dd25e35b6cc70fec865f5d54966330a05a2577d3b93cd6a4cde5385fc3cdb3160e04eb8ebc703bd0fbd969c8216b2136"]
# [0, 3]

# 0xa562f8ade1bdb49e380246162ac1002f33621ace67bc062afaf9521542334637,0x,0x,0x,0x,0x,0x,0x,0x51b75bd5a95e582e973418e878473a7cc2ce2a98c9495f0a033f83a57f0ded03,0x,0x,0x,0x,0x,0x,0x,0x