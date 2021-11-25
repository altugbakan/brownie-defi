from brownie import interface, config, network

from scripts.helpful_scripts import get_account

WETH_AMOUNT = 0.01 * 10 ** 18


def get_weth(amount=WETH_AMOUNT, account=get_account()):
    """Mints WETH by depositing ETH."""
    weth = interface.IWETH(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": amount})
    tx.wait(1)
    return tx


def approve_token(amount, spender, token_address, account=get_account()):
    """Approves the token for the spender to spend."""
    token = interface.IERC20(token_address)
    tx = token.approve(spender, amount, {"from": account})
    tx.wait(1)
    return tx
