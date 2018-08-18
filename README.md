# Stellar NFT

The NFT library creates a non-fungible token on the Stellar network. The resulting token
is a 0.0000001 supply limited token from a locked Issuer account that has an IPFS hash attached to it's account data. (Although it is not pinned so will be lost if your node goes
offline)

Currently the library is not opinionated about the data expected in the metadata.

## Basic usage

Before running the script you will need a funded Issuer account (1.5XLM) and a funded initial owner account (1 XLM). NOTE: that the Issuer account will be locked so it will not be usable after this.

The machine running the script will also need an IPFS daemon running on localhost.

```
from stellar_token_factory import TokenFactory

issuer_secret = 'SBLVL4PBIGHTCPEAWEWNZ2BSW2OU4KEUYHARWSL2AICCVNKQ6FQSP2OF'
owner_secret = 'SAAXGVL7A56BS2CP5OWLREAVTVSFB2NAMIPZWC5ETMDCZ54A6UNTVUCZ'
tf = TokenFactory(issuer_secret)
metadata = {
    'img': 'testing.jpg',
    'description': 'This is my first collectable!',
    'ref_url': 'This is a url for more context'
}
tx = tf.generate_non_fungible_token(owner_secret, 'FUNGI', metadata=metadata)
```