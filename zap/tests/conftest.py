import pytest
from brownie import config, Wei, Contract, chain

@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture
def user(accounts):
    return accounts.at("0xfd875403b4338a1fa9dcb03AE4d49ED43a9290Bb", force=True)


@pytest.fixture
def crv():
    return Contract("0xD533a949740bb3306d119CC777fa900bA034cd52")


@pytest.fixture
def lp_3crv():
    return Contract("0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490")

@pytest.fixture
def y3crv():
    return Contract("0x84E13785B5a27879921D6F685f041421C7F482dA")


@pytest.fixture
def vault():
    return Contract("0xc5bDdf9843308380375a611c18B50Fb9341f502A")


@pytest.fixture
def vesting():
    return Contract("0x575CCD8e2D300e2377B43478339E364000318E2c")

@pytest.fixture
def minter(interface):
    return Contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0")


@pytest.fixture
def gauges(interface, user):
    ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
    registry = Contract("0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c")
    pools = [registry.pool_list(i) for i in range(registry.pool_count())]
    gauges = set(chain.from_iterable([registry.get_gauges(pool)[0] for pool in pools]))
    gauges.discard(ZERO_ADDRESS)
    user_gauges = [
        gauge
        for gauge in gauges
        if interface.CurveGauge(gauge).claimable_tokens.call(user) > 0
    ]
    user_gauges += [ZERO_ADDRESS for _ in range(20 - len(user_gauges))]
    return user_gauges[:20]


@pytest.fixture
def backzapper(accounts, CurveBackzapper):
    return CurveBackzapper.deploy({"from": accounts[0]})


@pytest.fixture
def zap_3crv(accounts, y3CrvZapper):
    return y3CrvZapper.deploy({"from": accounts[0]})
