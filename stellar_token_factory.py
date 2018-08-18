import io
import json
import ipfsapi
import time
from stellar_base.builder import Builder
from stellar_base.keypair import Keypair


class TokenFactory(object):

    def __init__(self, issuer_secret, network='TESTNET'):
        self.issuer_secret = issuer_secret
        self.issuer_keypair = Keypair.from_seed(issuer_secret)
        self.network = network
        # For now we default to a local running node
        self.ipfs_api = ipfsapi.connect('127.0.0.1', 5001)

    def generate_non_fungible_token(self, initial_owner_secret, code, metadata=None):
        owner_keypair = Keypair.from_seed(initial_owner_secret)
        # First we generate the token trustline on the network
        self.create_trustline(initial_owner_secret, code)
        # Next we send exactly 0.0000001 to the initial owner
        return self.create_token_and_lock_account(
           code,
           owner_keypair.address().decode(),
           metadata
        )

    def create_ipfs_hash(self, data):
        # TODO: Don't generate an actual file
        with io.open(
            'token' + str(int(time.time())) + '.json', 'w', encoding='utf-8'
        ) as f:
            numbytes = f.write(json.dumps(data))
        res = self.ipfs_api.add('token.json')
        return res.get('Hash')

    def create_trustline(self, secret, code):
        builder = Builder(secret=secret, network=self.network)
        builder.append_trust_op(
            self.issuer_keypair.address().decode(),
            code,
            limit='0.0000001'
        )
        builder.sign()
        return builder.submit()

    def create_token_and_lock_account(self, code, owner_address, metadata):
        # Setup the base transaction
        builder = Builder(
            secret=self.issuer_secret,
            network=self.network
        )
        # Append relevant payment ops
        ipfs_hash = self.create_ipfs_hash(metadata)
        builder.append_manage_data_op('token_ipfs_hash', ipfs_hash)
        builder.append_payment_op(
            owner_address,
            '0.0000001',
            code,
            self.issuer_keypair.address().decode()
        )
        builder.append_set_options_op(master_weight=0)
        builder.sign()
        return builder.submit()
