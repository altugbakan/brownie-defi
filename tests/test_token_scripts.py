from brownie import config, network

from scripts.token_scripts import approve_token, get_weth
from scripts.helpful_scripts import get_account

WETH_AMOUNT = 0.01 * 10 ** 18


def test_get_weth():
    # Arrange
    account = get_account()

    # Act
    tx = get_weth(WETH_AMOUNT, account)

    # Assert
    assert tx.status == 1


def test_approve_token():
    # Arrange
    account = get_account()
    spender = config["networks"][network.show_active()]["swap_router"]
    amount = 1 * 10 ** 18  # 1
    weth_address = config["networks"][network.show_active()]["weth_token"]

    # Act
    tx = approve_token(amount, spender, weth_address, account)

    # Assert
    assert tx.status == 1
