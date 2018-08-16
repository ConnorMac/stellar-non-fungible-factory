from stellar_base.builder import Builder
from stellar_base.keypair import Keypair


class TokenFactory(object):

    def __init__(self, issuer_secret, network='test'):
        self.issuer_secret = issuer_secret
        self.issuer_keypair = Keypair.from_seed(issuer_secret)
        self.network = network

    def generate_non_fungible_token(self, initial_owner_secret, code, metadata=None):
        owner_keypair = Keypair.from_seed(initial_owner_secret)
        # First we generate the token trustline on the network
        # TODO: Set limit to 0.0000001 as well
        self.create_trustline(initial_owner_secret, code)
        # Next we send exactly 0.0000001 to the initial owner
        return self.create_token_and_lock_account(
           code,
           owner_keypair.address().decode()
        )

    def create_trustline(self, secret, code):
        builder = Builder(secret=secret, network=self.network)
        builder.append_trust_op(
            self.issuer_keypair.address().decode(),
            code
        )
        builder.sign()
        return builder.submit()

    def create_token_and_lock_account(self, code, owner_address):
        builder = Builder(
            secret=self.issuer_secret,
            network=self.network
        )
        builder.append_payment_op(
            owner_address,
            0.0000001,
            code,
            self.issuer_keypair.address().decode()
        )
        builder.append_set_options_op(master_weight=0)
        builder.sign()
        return builder.submit()
