import hashlib
import time
from bitcoinlib.keys import HDKey, Signature, Key, verify
from bitcoinlib.mnemonic import Mnemonic


pub = HDKey('03d48968ebe658b586913837b58dc2f21ca825eda8c0f819985d84435353b7a18f')
# Get the current timestamp
timestamp = str(time.time())
mnemonic = Mnemonic()
words = mnemonic.generate()
print(words)

master_key = HDKey.from_passphrase(words)
print(master_key)

# Generate the SHA-256 hash
sha256_hash = hashlib.sha256(timestamp.encode()).hexdigest()

# Print the SHA-256 hash
print("SHA-256 Hash:", sha256_hash)
print()

tr1=sha256_hash

child_private_key = master_key.child_private(10)
print(child_private_key)
child_private_key = master_key.child_private(11)
print(child_private_key)
child_public_key  = child_private_key.public()
txid = '0d12fdc4aac9eaaab9730999e0ce84c3bd5bb38dfd1f4c90c613ee177987429c'
pub_key = master_key.public()
print(tr1)
print(master_key)
signature2 = '9aea4ec4d8695a3ed097329bc7fa9e2e036f1a8c312fd6ab61dd7e71f3d5533c34c6c27c3f9ffde545501656afebda198e325803b7bf99f8da368b3a2d81e591'

print(signature2)
signature = Signature.create(txid=tr1, private=child_private_key)
print(signature)

print(signature.verify(tr1, child_public_key))

txid = '4010fc4391fe909f3f5e38f41581be5fc7c931083958a9541f46a3508da4e39f'
sign = '429788c475c3791e21e1e0fa7b4209e16053e61409646df8a4aba095f1d9fe275e6debca0ea81dbfd091f427b49acdea6206130cae494ad95db98a4327afe88e'
k = HDKey('03d48968ebe658b586913837b58dc2f21ca825eda8c0f819985d84435353b7a18f')
print(verify(txid, sign, k))