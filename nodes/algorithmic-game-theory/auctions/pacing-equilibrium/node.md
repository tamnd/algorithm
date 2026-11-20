---
tag: W1M0KT
kind: definition
slug: pacing-equilibrium
name: Pacing equilibrium
aliases:
- budget pacing equilibrium
- multiplicative pacing
area: algorithmic-game-theory/auctions
level: research
summary: "Budget-limited bidders in many auctions scale all their bids by one multiplier each, so that every bidder either spends exactly its budget or bids its full values."
prereqs: [vickrey-auction, first-price-auction, quasilinear-utility]
see_also: [fisher-market, eisenberg-gale-program, competitive-equilibrium, ppad, position-auction, generalized-second-price-auction, online-adwords-problem, nash-equilibrium]
sources:
  - paper: doi:10.1287/opre.2021.2167
    title: "Vincent Conitzer, Christian Kroer, Eric Sodomka and Nicolas E. Stier-Moses, Multiplicative pacing equilibria in auction markets, Operations Research 70(2) (2022), 963-989"
    locator: Definition 3.6 (pacing equilibrium for second-price auctions) and Theorem 4.1 (existence), with examples of multiple equilibria and the hardness of finding the best one
  - paper: doi:10.1287/mnsc.2022.4310
    title: "Vincent Conitzer, Christian Kroer, Debmalya Panigrahi, Okke Schrijvers, Nicolas E. Stier-Moses, Eric Sodomka and Christopher A. Wilkens, Pacing equilibrium in first price auction markets, Management Science 68(12) (2022), 8515-8535"
    locator: the first-price pacing equilibrium, its uniqueness, its equivalence with a quasilinear Fisher market equilibrium, and the convex program that computes it
  - paper: doi:10.1145/3465456.3467578
    title: "Xi Chen, Christian Kroer and Rachitesh Kumar, The complexity of pacing for second-price auctions, Proceedings of the 22nd ACM Conference on Economics and Computation (EC 2021)"
    locator: PPAD-completeness of finding a pacing equilibrium for second-price auctions
---

A pacing equilibrium is a steady state of an ad market in which each advertiser has a budget and takes part in many auctions at once. Each bidder $i$ picks one number $\alpha_i \in [0, 1]$, its *pacing multiplier*, and bids $\alpha_i v_{ij}$ in every auction $j$ instead of its value $v_{ij}$. In equilibrium, every bidder either spends exactly its budget or does not pace at all ($\alpha_i = 1$), and each good goes to the highest paced bids. Ad platforms pace bids in this way to spread budgets over many auctions. Conitzer, Kroer, Sodomka and Stier-Moses (2022) defined the equilibrium for second-price auctions and proved that it always exists; for first-price auctions the equilibrium is unique and equals the equilibrium of a quasilinear [Fisher market](/fisher-market/).

## Definition

There are $n$ bidders and $m$ goods, each sold in its own single-item auction. Bidder $i$ has values $v_{ij} \ge 0$ and a budget $B_i > 0$, and [quasilinear utility](/quasilinear-utility/) up to its budget. Allocations may be fractional, which models ties and a continuum of identical impressions.

A **second-price pacing equilibrium** (Conitzer, Kroer, Sodomka and Stier-Moses 2022, Definition 3.6) is a list of pacing multipliers $\alpha_i \in [0, 1]$, allocations $x_{ij} \in [0, 1]$ and prices $p_j \ge 0$ with these properties:

1. **Prices are second prices.** $p_j$ is the second-highest paced bid $\alpha_i v_{ij}$ on good $j$.
2. **Only the highest bids win.** If $x_{ij} > 0$, then $\alpha_i v_{ij} = \max_k \alpha_k v_{kj}$.
3. **Goods with a positive price are sold.** $\sum_i x_{ij} \le 1$, with equality if $p_j > 0$.
4. **Budgets hold.** $\sum_j x_{ij} p_j \le B_i$ for every bidder.
5. **No unnecessary pacing.** If $\sum_j x_{ij} p_j < B_i$, then $\alpha_i = 1$.

A **first-price pacing equilibrium** is the same with $p_j$ the highest paced bid, so that each winner pays its own paced bid.

Known facts:

- **Existence.** A second-price pacing equilibrium always exists (Conitzer, Kroer, Sodomka and Stier-Moses 2022, Theorem 4.1). The proof uses a fixed point theorem.
- **Many equilibria.** There can be several second-price pacing equilibria with different revenue and welfare, and finding one with the most revenue or welfare is NP-hard (Conitzer, Kroer, Sodomka and Stier-Moses 2022).
- **Computing one is PPAD-complete** for second-price auctions (Chen, Kroer and Kumar 2021); see [PPAD](/ppad/).
- **First price is easy.** The first-price pacing equilibrium is unique, it is the competitive equilibrium of a Fisher market with quasilinear buyers, and a convex program in the style of the [Eisenberg-Gale program](/eisenberg-gale-program/) computes it in polynomial time (Conitzer, Kroer, Panigrahi et al. 2022).

## Examples and non-examples

**A budget that binds.** One good, bidder 1 with value 10 and budget 2, bidder 2 with value 4 and budget 100, second-price auction.

| $\alpha_1$ | paced bids | result | condition broken |
|---|---|---|---|
| $1$ | $10, 4$ | bidder 1 wins and pays 4 | budget 2 of bidder 1 |
| $1/5$ | $2, 4$ | bidder 2 wins and pays 2 | bidder 1 spends 0 but paces |
| $2/5$ | $4, 4$ | tie at price 4, $x = (1/2, 1/2)$ | none |

With $\alpha = (2/5, 1)$ bidder 1 spends $4 \cdot 1/2 = 2$, its whole budget, and bidder 2 spends $2 < 100$ with $\alpha_2 = 1$. Any $\alpha_1 > 2/5$ makes bidder 1 win the whole good at 4, above its budget, and any $\alpha_1 < 2/5$ makes it spend nothing while it paces, so this equilibrium is unique. The first-price version gives the same outcome.

**No budget binds.** If every budget is larger than the sum of the bidder's values, no bidder can spend its whole budget, because each price is at most the winner's paced bid. Condition 5 then forces $\alpha_i = 1$ for all $i$, and the equilibrium is the outcome of truthful bidding in each auction.

**Non-example: pacing each auction separately.** A bidder that shades its bid by a different factor in each auction is not pacing in this sense. The model allows one multiplier per bidder across all auctions, which is what makes the equilibrium a market equilibrium in the first-price case.

**Non-example: overspending.** Multipliers under which some bidder pays more than its budget are not an equilibrium, even if every good goes to its highest paced bid.

## Related definitions

- **Fisher market equilibrium.** In a [Fisher market](/fisher-market/) buyers with budgets buy divisible goods at prices that clear the market. A first-price pacing equilibrium is a [competitive equilibrium](/competitive-equilibrium/) of such a market with quasilinear buyers, where $1/\alpha_i$ plays the role of the bang-per-buck of bidder $i$.
- **Budget-constrained auctions.** The [online AdWords problem](/online-adwords-problem/) allocates queries to budget-limited advertisers online, without strategic bids. Pacing equilibria study the steady state with strategic platforms or bidders.
- **Position auctions.** With ad slots, each auction can be a [position auction](/position-auction/) run by [GSP](/generalized-second-price-auction/) with paced bids.
- **Nash equilibrium.** A pacing equilibrium is defined by the budget and market conditions above, not by best responses, so it is not a [Nash equilibrium](/nash-equilibrium/) by definition. Whether bidders gain by reporting other values or budgets to the pacing system is a separate question.

## References
