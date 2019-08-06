#from web3.auto.infura.ropsten import w3
from web3.auto.infura import w3
from eth_utils import (
    keccak,
)
import rlp
from rlp.sedes import (
    Binary,
    big_endian_int,
)
from trie import (
    HexaryTrie,
)


def format_proof_nodes(proof):
    trie_proof = []
    for rlp_node in proof:
        trie_proof.append(rlp.decode(w3.toBytes(hexstr=w3.toHex(rlp_node))))
    return trie_proof


def verify_eth_get_proof(proof, root):
    trie_root = Binary.fixed_length(32, allow_empty=True)
    hash32 = Binary.fixed_length(32)

    class _Account(rlp.Serializable):
        fields = [
                    ('nonce', big_endian_int),
                    ('balance', big_endian_int),
                    ('storage', trie_root),
                    ('code_hash', hash32)
                ]
    acc = _Account(
        proof.nonce,
        proof.balance,
        w3.toBytes(hexstr=w3.toHex(proof.storageHash)),
        w3.toBytes(hexstr=w3.toHex(proof.codeHash))
    )
    rlp_account = rlp.encode(acc)
    trie_key = keccak(w3.toBytes(hexstr=proof.address))
    trie_proof = format_proof_nodes(proof.accountProof)

    leaf = HexaryTrie.get_from_proof(
        root, trie_key, trie_proof
    )

    if acc == b'':
        print("Verify that the account does not exist")
    else:
        assert rlp_account == leaf, "Failed to verify account proof {}".format(proof.address)
        print("Succeed to verify account proof {}".format(proof.address))
    return True


block = w3.eth.getBlock(8287420)
print(block)
proof = w3.eth.getProof('0xd525245432B71c2589a51aCB5ae56B439E57357E', [0], 8287420)
print(proof)
assert verify_eth_get_proof(proof, block.stateRoot)
