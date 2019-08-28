from trie import HexaryTrie
from web3.auto import w3
import rlp
from eth_utils import (
    keccak,
)


trie = HexaryTrie(db={})
print(w3.toHex(trie.root_hash))
print(w3.toHex(keccak(trie.root_node)))
print(w3.toHex(keccak(rlp.encode(trie.root_node))))

print("1", w3.toHex(rlp.encode(1)))
print("ONE", w3.toHex(rlp.encode("ONE")))
print("2", w3.toHex(rlp.encode(2)))
print("TWO", w3.toHex(rlp.encode("TWO")))

trie.set(rlp.encode(1), rlp.encode("ONE"))
print(w3.toHex(trie.root_hash))
print(w3.toHex(keccak(rlp.encode(trie.get_node(trie.root_hash)))))
assert trie.root_hash == keccak(rlp.encode(trie.get_node(trie.root_hash)))
print(trie.get_node(trie.root_hash))


trie.set(rlp.encode(2), rlp.encode("TWO"))
print(w3.toHex(trie.root_hash))
print(w3.toHex(keccak(rlp.encode(trie.get_node(trie.root_hash)))))
assert trie.root_hash == keccak(rlp.encode(trie.get_node(trie.root_hash)))
print(trie.get_node(trie.root_hash))


trie.set(rlp.encode(3), rlp.encode("THREE"))
print(w3.toHex(trie.root_hash))
print(w3.toHex(keccak(rlp.encode(trie.get_node(trie.root_hash)))))
assert trie.root_hash == keccak(rlp.encode(trie.get_node(trie.root_hash)))
print(trie.get_node(trie.root_hash))

proof = trie.get_proof(rlp.encode(1))
assert HexaryTrie.get_from_proof(trie.root_hash, rlp.encode(1), proof) == rlp.encode("ONE")
print(proof)

proof = trie.get_proof(rlp.encode(2))
assert HexaryTrie.get_from_proof(trie.root_hash, rlp.encode(2), proof) == rlp.encode("TWO")
print(proof)

proof = trie.get_proof(rlp.encode(3))
assert HexaryTrie.get_from_proof(trie.root_hash, rlp.encode(3), proof) == rlp.encode("THREE")
print(proof)
#([b'\x10', b'\xae\xa5\xd0\x99\xdd\xe25gVx\xdcu\xd5\xecAC]w\xa7E\xcd=\xb20)\xb3\xaa\xf6Jy~\xdd'],
# [b'', [b' ', b'\x83ONE'], [b' ', b'\x83TWO'], [b' ', b'\x85THREE'], b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
# [b' ', b'\x85THREE'])

print(proof[0])
print(w3.toHex(rlp.encode(proof[0])))
print(proof[1])
print(keccak(rlp.encode(proof[1])))

