---
tag: XYWQB6
kind: definition
slug: reserve-price
name: Reserve price
aliases:
- reservation price
- monopoly reserve
area: algorithmic-game-theory/auctions
level: core
summary: "A minimum price below which the seller keeps the item. For i.i.d. regular values the optimal reserve is the zero of the virtual valuation, whatever the number of bidders."
prereqs: [vickrey-auction, virtual-valuation]
see_also: [myerson-optimal-auction, regular-distribution, bulow-klemperer-theorem, ironing, sequential-posted-pricing, first-price-auction, generalized-second-price-auction]
sources:
  - paper: "John G. Riley and William F. Samuelson, Optimal auctions, American Economic Review 71(3) (1981), 381-392"
    locator: the optimal reserve price for symmetric bidders, which exceeds the seller's own value and does not depend on the number of bidders
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the optimal auction as an auction with bidder-specific reserves given by the zeros of the virtual valuations
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 5, Revenue-maximizing auctions, Section 5.2 (the Vickrey auction with the monopoly reserve) and Section 5.3 (reserve prices in sponsored search)
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 2 (reserve prices in first-price and second-price auctions with independent private values)
---

A reserve price is the lowest price at which the seller will sell: bids below it are ignored, and if no bid reaches it the seller keeps the item. In a [Vickrey auction](/vickrey-auction/) with reserve $r$, the highest bidder wins if its bid is at least $r$ and pays the larger of $r$ and the second-highest bid. A reserve is a tool for revenue. It trades a loss of sales for higher prices, and for bidders with independent regular values the best reserve is the zero of the [virtual valuation](/virtual-valuation/), the *monopoly reserve*. It differs from a posted price, which is the only price offered: a reserve is a floor, and competition can push the price above it.

## Definition

Fix an auction format, such as the second-price or the first-price auction, and a number $r \ge 0$. The auction **with reserve price $r$** treats every bid below $r$ as absent. If no bid is at least $r$, the item is not sold. In a second-price auction with reserve $r$, the winner pays $\max(r, b_{(2)})$, where $b_{(2)}$ is the second-highest bid. The auction stays truthful, since the winner's payment is still its threshold bid.

A reserve can be **anonymous**, the same $r$ for all bidders, or **bidder-specific**, a reserve $r_i$ for each bidder $i$.

**Monopoly reserve.** For a distribution $F$ with virtual valuation $\varphi$, a monopoly reserve is a price $r^*$ that maximizes $r(1 - F(r))$, the revenue from one bidder. If $F$ is [regular](/regular-distribution/), $r^* = \varphi^{-1}(0)$. When the seller has a value $v_0$ for the item, the optimal reserve solves $\varphi(r) = v_0$, so it lies strictly above $v_0$ when $1 - F(r) > 0$ (Riley and Samuelson 1981).

**Optimality.** For bidders with i.i.d. regular values and seller value $0$, the second-price auction with the anonymous reserve $\varphi^{-1}(0)$ is [Myerson's optimal auction](/myerson-optimal-auction/). The optimal reserve does not depend on the number of bidders. For independent regular values with different distributions, the optimal auction gives bidder $i$ the reserve $\varphi_i^{-1}(0)$, but in addition it ranks the bidders by virtual value, not by bid.

## Examples and non-examples

- **Uniform values.** For $U[0, 1]$, $\varphi(v) = 2v - 1$, so $r^* = 1/2$. One bidder facing the price $1/2$ pays with probability $1/2$, for revenue $1/4$. Two bidders: the Vickrey auction earns $1/3$, and with reserve $1/2$ it earns $5/12$, the optimal revenue.
- **Seller value.** For $U[0, 1]$ and seller value $v_0 = 1/4$, the optimal reserve solves $2r - 1 = 1/4$, so $r = 5/8$, which is above $1/4$. Selling to a bidder with value between $1/4$ and $5/8$ would gain the seller something, but it would lower the prices paid by bidders with higher values.
- **Exponential values.** For $F(v) = 1 - e^{-\lambda v}$, $\varphi(v) = v - 1/\lambda$, so $r^* = 1/\lambda$, the mean value.
- **Equal-revenue distribution.** For $F(v) = 1 - 1/v$ on $[1, \infty)$, every price $r \ge 1$ gives one bidder the revenue 1, so every such $r$ is a monopoly reserve.
- **Bidder-specific reserves.** With $v_1 \sim U[0, 1]$ and $v_2 \sim U[0, 2]$, $\varphi_1(v) = 2v - 1$ and $\varphi_2(v) = 2v - 2$, so the optimal reserves are $1/2$ and $1$. An anonymous reserve cannot match both.
- **Irregular values.** For values $2, 3, 5$ with probabilities $1/2, 1/6, 1/3$, the ironed virtual values are $1/2, 1/2, 5$, all positive, so the optimal reserve is $2$ and the seller always sells. The raw virtual value of 3 is $-1$, so a reserve from the raw $\varphi$ would be wrong.
- **Not an entry fee.** An entry fee is paid by every bidder who takes part, win or lose. A reserve is paid only by a winner, and only when the competition is weaker than the reserve.
- **Not a posted price.** With two bidders and reserve $1/2$, a sale at $0.7$ happens when the bids are $0.9$ and $0.7$. A posted price of $1/2$ would sell at $1/2$.

## Related definitions

- **Virtual valuation.** The reserve is where the virtual value becomes nonnegative ([virtual valuation](/virtual-valuation/)). For an irregular distribution, the zero of the ironed virtual value is used ([ironing](/ironing/)).
- **Bulow-Klemperer theorem.** With i.i.d. regular values, one more bidder in a Vickrey auction with no reserve earns at least as much as the optimal reserve ([Bulow-Klemperer theorem](/bulow-klemperer-theorem/)).
- **Posted prices.** [Sequential posted pricing](/sequential-posted-pricing/) offers a price to each bidder in turn, with no competition between bidders.
- **Reserves in other formats.** In a [first-price auction](/first-price-auction/) with i.i.d. values the same reserve is optimal, by revenue equivalence. In ad auctions such as the [generalized second-price auction](/generalized-second-price-auction/), reserve prices per click play the same role.

## References
