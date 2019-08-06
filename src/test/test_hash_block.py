#from web3.auto.infura.ropsten import w3
from web3.auto.infura import w3
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

print(w3.isConnected())

address = Binary.fixed_length(20, allow_empty=True)
hash32 = Binary.fixed_length(32)
uint256 = BigEndianInt(256)
trie_root = Binary.fixed_length(32, allow_empty=True)


class _BlockHeader(rlp.Serializable):
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


block = w3.eth.getBlock(8288380)

raw_block = _BlockHeader(
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

rlp_block = rlp.encode(raw_block)

assert keccak(rlp_block) == block.hash

print(True)
