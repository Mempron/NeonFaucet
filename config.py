from environs import Env

from dataclasses import dataclass


@dataclass
class Driver:
    extension_path: str
    delay: int


@dataclass
class Wallet:
    phrase: list[str]
    private_key: str
    public_key: str
    password: str


@dataclass
class Network:
    name: str
    rpc_url: str
    chain_id: str
    currency_symbol: str
    block_explorer_url: str


@dataclass
class Faucet:
    url: str
    token: str
    amount: str


@dataclass
class Config:
    driver: Driver
    wallet: Wallet
    network: Network
    faucet: Faucet
    proxies: dict


env = Env()
env.read_env()

proxies = {}

try:
    with open(env('PROXIES_PATH'), 'r') as file:
        for line in file:
            key, value = line.rstrip().split(':')
            proxies[key] = value
except FileNotFoundError:
    print("Proxies file doesn't exist.")


config = Config(
    driver=Driver(
        extension_path=env('DRIVER_EXTENSION_PATH'),
        delay=env.int('DRIVER_DELAY')
    ),
    wallet=Wallet(
        phrase=env.list('WALLET_PHRASE'),
        private_key=env('WALLET_PRIVATE_KEY'),
        public_key=env('WALLET_PUBLIC_KEY'),
        password=env('WALLET_PASSWORD')
    ),
    network=Network(
        name=env('NETWORK_NAME'),
        rpc_url=env('NETWORK_RPC_URL'),
        chain_id=env('NETWORK_CHAIN_ID'),
        currency_symbol=env('NETWORK_CURRENCY_SYMBOL'),
        block_explorer_url=env('NETWORK_BLOCK_EXPLORER_URL')
    ),
    faucet=Faucet(
        url=env('FAUCET_URL'),
        token=env('FAUCET_TOKEN'),
        amount=env('FAUCET_AMOUNT')
    ),
    proxies=proxies
)
