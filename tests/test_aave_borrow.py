from brownie import config, network

from scripts.aave_borrow import (
    get_asset_price,
    get_lending_pool,
    deposit,
)
from scripts.token_scripts import get_weth
from scripts.helpful_scripts import get_account


def test_get_asset_price():
    # Arrange / Act
    asset_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )

    # Assert
    assert asset_price > 0


def test_get_lending_pool():
    # Arrange / Act
    lending_pool = get_lending_pool()

    # Assert
    assert lending_pool != None


def test_deposit():
    # Arrange
    deposit_amount = 0.01 * 10 ** 18
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]
    get_weth(deposit_amount, account)

    # Act
    tx = deposit(deposit_amount, weth_address, account)

    # Assert
    assert tx.status == 1
