from brownie import interface, network, config, chain

from scripts.token_scripts import approve_token, get_weth
from scripts.helpful_scripts import get_account

SWAP_FEE = 3000  # 0.3%
WETH_AMOUNT = 0.01 * 10 ** 18


def swap(
    token_in,
    token_out,
    fee=SWAP_FEE,
    account=get_account(),
    deadline=chain.time() + 600,
    amount_in=0,
    amount_out_minimum=0,
    sqrt_price_limit_x96=0,
):
    swap_router = interface.ISwapRouter(
        config["networks"][network.show_active()]["swap_router"]
    )
    approve_token(amount_in, swap_router.address, token_in, account)
    tx = swap_router.exactInputSingle(
        [
            token_in,
            token_out,
            fee,
            account,
            deadline,
            amount_in,
            amount_out_minimum,
            sqrt_price_limit_x96,
        ],
        {"from": account},
    )
    tx.wait(1)
    return tx


def main():
    account = get_account()

    # Convert ETH to WETH
    print("Converting ETH to WETH...")
    weth_address = config["networks"][network.show_active()]["weth_token"]
    get_weth(WETH_AMOUNT, account)
    print("Converted.")

    # Swap WETH for DAI
    print("Swapping WETH for DAI...")
    dai_address = config["networks"][network.show_active()]["dai_token"]
    swap(
        token_in=weth_address,
        token_out=dai_address,
        amount_in=WETH_AMOUNT,
        account=account,
    )
    print("Swapped.")
