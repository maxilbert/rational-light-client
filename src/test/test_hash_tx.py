from web3.auto.infura import w3
from rlp.sedes import (
    Binary,
    big_endian_int,
    binary
)
import rlp
from eth_utils import (
    keccak,
)

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


tx = w3.eth.getTransaction(0x95604ade1cd64e12851e9626270fe1b61b3034293ae6d6d85fcf27b19d146c28)

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

print(True)
