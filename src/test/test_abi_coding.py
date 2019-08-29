from utils.util import *

proof_abi = encode_abi(
    ['bytes', 'bytes32', 'bytes[]', 'uint[]'],
    (b'', b'', [], [])
)

digest = keccak(proof_abi)

sig_1 = w3.eth.account.signHash(digest, private_key=sk_rfn_1)
sig_2 = w3.eth.account.signHash(digest, private_key=sk_rfn_2)

print(sig_1.v, w3.toHex(sig_1.r), w3.toHex(sig_1.s))
print(sig_2.v, w3.toHex(sig_2.r), w3.toHex(sig_2.s))
