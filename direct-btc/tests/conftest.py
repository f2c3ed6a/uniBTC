import pytest
from web3 import Web3
from pathlib import Path
from brownie import accounts, project, config

# Web3 client
@pytest.fixture(scope="session", autouse=True)
def w3():
    return Web3(Web3.HTTPProvider('http://localhost:8545'))

# Roles
@pytest.fixture(scope="session", autouse=True)
def roles(w3):
    pauser_role = w3.keccak(text='PAUSER_ROLE')  # index = 0
    minter_role = w3.keccak(text='MINTER_ROLE')  # index = 1
    manager_role = w3.keccak(text='MANAGER_ROLE')  # index = 2
    default_admin_role = w3.to_bytes(hexstr="0x00")  # index = 5
    return [pauser_role, minter_role, manager_role, default_admin_role]

# Predefined Accounts
@pytest.fixture(scope="session", autouse=True)
def owner():
    return accounts[0]

@pytest.fixture(scope="session", autouse=True)
def deployer():
    return accounts[1]

@pytest.fixture(scope="session", autouse=True)
def alice():
    return accounts[2]

@pytest.fixture(scope="session", autouse=True)
def bob():
    return accounts[3]

@pytest.fixture(scope="session", autouse=True)
def executor():
    return accounts[3]

@pytest.fixture(scope="session", autouse=True)
def zero_address():
    return accounts.at("0x0000000000000000000000000000000000000000", True)

@pytest.fixture(scope="session", autouse=True)
def chain_id(w3):
    return w3.eth.chain_id

@pytest.fixture(scope="session", autouse=True)
def deps():
    # Reference: https://docs.openzeppelin.com/contracts/4.x/api/proxy#TransparentUpgradeableProxy
    deps = project.load(  Path.home() / ".brownie" / "packages" / config["dependencies"][0])
    return deps

def pytest_addoption(parser):
    parser.addoption("--case", action="store", default="default_slippage", help="case for the test")