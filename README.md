## Deal or No Deal CLI game

This is a CLI-version of the popular game show `Deal or No Deal`.

To play Deal or No Deal, run `deal_or_no_deal.exe` in the `dist` folder.

Alternatively, if you have a Python environment setup on your machine, you could also run `deal_or_no_deal.py`. 

I wrote this in python, and there are some interesting mathematics behind the game. If you don't know about the game, read the rules here: https://www.rookieroad.com/game-shows/what-is-deal-or-no-4617305/ or watch any of the episodes on Youtube. 

In particular, I reverse engineered the math of the banker's offer. The banker's offer is based on the expected value of the current cases in play. I wrote a dynamic offer calculation algorithm which makes the game exciting, and borrows concepts from game theory and probability.

For the player, the ideal strategy is to determine their current equity, and compare with the banker's offer. If the banker's offer is higher than the player's equity, make the deal.