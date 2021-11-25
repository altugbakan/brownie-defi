from brownie import network, config, interface

from scripts.uniswap_swap import swap
from scripts.token_scripts import get_weth, approve_token
from scripts.helpful_scripts import get_account

WETH_LEND_AMOUNT = 0.1 * 10 ** 18
WETH_SWAP_AMOUNT = 0.01 * 10 ** 18


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def get_borrowable_data(account):
    lending_pool = get_lending_pool()
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        _,
        _,
        _,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth /= 10 ** 18
    total_collateral_eth /= 10 ** 18
    total_debt_eth /= 10 ** 18
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} ETH worth of tokens.")
    return float(available_borrow_eth)


def get_asset_price(price_feed_address):
    price_feed = interface.IAggregatorV3(price_feed_address)
    decimals = price_feed.decimals()
    latest_price = price_feed.latestRoundData()[1] / 10 ** decimals
    return float(latest_price)


def deposit(amount, token_address, account):
    lending_pool = get_lending_pool()
    approve_token(amount, lending_pool.address, token_address, account)
    tx = lending_pool.deposit(
        token_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    return tx


def borrow(amount, token_address, account):
    lending_pool = get_lending_pool()
    tx = lending_pool.borrow(
        token_address,
        amount,
        1,
        0,
        account.address,
        {"from": account},
    )
    tx.wait(1)
    return tx


def repay(amount, token_address, account):
    lending_pool = get_lending_pool()
    approve_token(amount, lending_pool.address, token_address, account)
    tx = lending_pool.repay(
        token_address, amount, 1, account.address, {"from": account}
    )
    tx.wait(1)


def main():
    account = get_account()

    # Convert ETH to WETH
    print("Converting ETH to WETH...")
    get_weth(WETH_LEND_AMOUNT + WETH_SWAP_AMOUNT, account)
    print("Converted.")

    # Deposit WETH
    print("Depositing WETH...")
    weth_address = config["networks"][network.show_active()]["weth_token"]
    deposit(WETH_LEND_AMOUNT, weth_address, account)
    print("Deposited.")

    # Find out how much we can borrow
    borrowable_eth = get_borrowable_data(account)
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    print(f"DAI/ETH price ratio is {dai_eth_price}")
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")

    # Borrow DAI
    print("Borrowing DAI...")
    dai_address = config["networks"][network.show_active()]["dai_token"]
    tx = borrow(amount_dai_to_borrow * 10 ** 18, dai_address, account)
    tx.wait(1)
    print("Borrowed")
    get_borrowable_data(account)

    # Swap WETH to DAI to repay all debt
    print("Swapping WETH for DAI...")
    swap(weth_address, dai_address, amount_in=WETH_SWAP_AMOUNT, account=account)
    print("Swapped")

    # Repay DAI
    print("Repaying DAI...")
    repay(
        amount_dai_to_borrow * 1.01 * 10 ** 18,  # including the fee
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    print("Repaid.")
    get_borrowable_data(account)
