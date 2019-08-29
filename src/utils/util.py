from eth_typing import (
    Hash32
)
from typing import (
    Dict, Sequence, Tuple
)
from rlp.sedes import (
    Binary,
    BigEndianInt,
    big_endian_int,
    binary
)
import rlp
from eth_utils import (
    keccak,
)
from trie import HexaryTrie
from web3.auto.infura import w3
from eth_abi import encode_abi
from eth_account import Account

address = Binary.fixed_length(20, allow_empty=True)
hash32 = Binary.fixed_length(32)
uint256 = BigEndianInt(256)
trie_root = Binary.fixed_length(32, allow_empty=True)


class Transaction(rlp.Serializable):
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


class BlockHeader(rlp.Serializable):
    fields = [
        ('parent_hash', hash32),
        ('uncles_hash', hash32),
        ('coinbase', address),
        ('state_root', trie_root),
        ('transaction_root', trie_root),
        ('receipt_root', trie_root),
        ('bloom', uint256),
        ('difficulty', big_endian_int),
        ('block_number', big_endian_int),
        ('gas_limit', big_endian_int),
        ('gas_used', big_endian_int),
        ('timestamp', big_endian_int),
        ('extra_data', binary),
        ('mix_hash', binary),
        ('nonce', Binary(8, allow_empty=True))
    ]


BLANK_ROOT_HASH = Hash32(b'V\xe8\x1f\x17\x1b\xccU\xa6\xff\x83E\xe6\x92\xc0\xf8n\x5bH\xe0\x1b\x99l\xad\xc0\x01b/\xb5\xe3c\xb4!')
Transactions = Sequence[Transaction]
TrieRootAndData = Tuple[Hash32, Dict[Hash32, bytes]]

sk_lwn = 0xfe62bb0b8578e1bf32bc9265fac5e6f24b9aff1e0d115cc4a41a3a6728abf1f1
sk_rfn_1 = 0xe3991216c1ad171842100dfa62fa711d3aa81fbcae1088d9fb3574b4eedc92d6
sk_rfn_2 = 0x1afd61c96e70bac6b9f75f0f0fee247a2f76ee5ef86cfdb660c081ba84c5e96e

addr_lwn = 0x802Fd9c8369AF656196547d3619aEF222bE56777
addr_rfn_1 = 0x3ca68896d4111E26847100C5328fF4F3F3b31B84
addr_rfn_2 = 0xd5F4538211bf0F6cCb3c7a7934768E7E2B5703f2
