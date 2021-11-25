# Brownie DeFi
Brownie scripts interacting with DeFi smart contracts.

## Uniswap
1. Converts ETH to WETH.
2. Swaps WETH for DAI.

## Aave
1. Converts ETH to WETH.
2. Deposits WETH
3. Calculates how much DAI you can borrow using Chainlink Price Feeds.
4. Borrows DAI.
5. Swaps WETH to DAI using Uniswap.
6. Repays DAI debt with interest.