import rlp

root = [b' \x01', b'\x83ONE']
print(rlp.encode(root[0]))
print(rlp.encode(root[1]))
x = rlp.encode([rlp.encode(root[0]), rlp.encode(root[1])])
y = rlp.encode(root)
print(x)
print(y)
print(rlp.decode(x))
print(rlp.decode(y))
