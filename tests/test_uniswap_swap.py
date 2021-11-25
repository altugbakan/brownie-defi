from brownie import network, config

from scripts.uniswap_swap import swap
from scripts.token_scripts import get_weth
from scripts.helpful_scripts import get_account

WETH_AMOUNT = 0.01 * 10 ** 18


def test_swap():
    # Arrange
    account = get_account()
    get_weth(WETH_AMOUNT, account)
    weth_address = config["networks"][network.show_active()]["weth_token"]
    dai_address = config["networks"][network.show_active()]["dai_token"]

    # Act
    tx = swap(weth_address, dai_address, amount_in=WETH_AMOUNT, account=account)

    # Assert
    assert tx.status == 1
