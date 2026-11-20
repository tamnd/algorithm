---
tag: 2ZMN7N
kind: model
slug: double-auction
name: Double auction
aliases:
- two-sided auction
area: algorithmic-game-theory/auctions
level: core
summary: "A market in which buyers submit bids and sellers submit asks for units of one good, and a mechanism decides who trades and at which prices, as in a call market or a stock exchange."
prereqs: [quasilinear-utility, individual-rationality, budget-balance]
see_also: [mcafee-trade-reduction, myerson-satterthwaite-theorem, vcg-mechanism, uniform-price-auction, independent-private-values, bayes-nash-equilibrium, competitive-equilibrium, combinatorial-auction]
sources:
  - paper: "R. Preston McAfee, A dominant strategy double auction, Journal of Economic Theory 56(2) (1992), 434-450"
    locator: the model of a double auction with unit demand and unit supply, the efficient trades and the trade reduction mechanism
  - paper: "Roger B. Myerson and Mark A. Satterthwaite, Efficient mechanisms for bilateral trading, Journal of Economic Theory 29(2) (1983), 265-281"
    locator: bilateral trade with independent private values, and the impossibility of an efficient, incentive compatible, individually rational and budget balanced mechanism
---

A double auction is a market with traders on both sides. Buyers submit *bids*, the most they will pay for a unit, and sellers submit *asks*, the least they will accept. A mechanism matches them and sets prices. Call markets that clear once, such as the opening auction of a stock exchange, and continuous order books are double auctions. Unlike a one-sided auction, the auctioneer must balance two groups whose reports both affect the price, and the [Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/) shows that no mechanism is efficient, incentive compatible, individually rational and budget balanced at once, even for one buyer and one seller. [McAfee's trade reduction mechanism](/mcafee-trade-reduction/) gives up at most one trade to get the other properties.

## The machine

- **Traders.** There are buyers and sellers of one kind of good, $n$ traders in all. In the basic model each buyer wants one unit and has a private value $v$ for it, and each seller has one unit and a private cost $c$.
- **Reports.** Each buyer reports a bid $b$ and each seller an ask $s$. In the Bayesian version, values and costs are drawn independently from known distributions, as in the [independent private values](/independent-private-values/) model.
- **Outcomes.** A mechanism chooses which buyers and sellers trade, with as many trading buyers as trading sellers, and a payment for each trading buyer and a receipt for each trading seller.
- **Utility.** [Quasilinear](/quasilinear-utility/): a buyer that trades at price $p$ gets $v - p$, a seller that trades at price $p$ gets $p - c$, and others get 0.
- **Multi-unit traders.** In general, a trader may submit a schedule of bids or asks for several units, and a call market clears all orders at one price.

## What it counts

- **Gains from trade**, $\sum (v - c)$ over the trading pairs, against the maximum.
- **Incentives**: [DSIC](/dominant-strategy-incentive-compatibility/) or Bayesian incentive compatibility, and the equilibria of formats that are not truthful.
- **[Individual rationality](/individual-rationality/)**: no trader that reports truthfully loses.
- **[Budget balance](/budget-balance/)**: *weak* if the buyers pay at least what the sellers receive, *strong* if they pay exactly that, so the market maker neither adds nor keeps money.
- **Computation** is easy: sorting the two sides takes $O(n \log n)$ time.

## Relation to other models

- With one seller and many buyers, it is a one-sided auction, such as the [Vickrey auction](/vickrey-auction/) or the [uniform price auction](/uniform-price-auction/) for many units.
- With one buyer and one seller it is *bilateral trade*, the setting of the [Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/).
- With many different goods and bundles it is a combinatorial exchange, the two-sided form of a [combinatorial auction](/combinatorial-auction/).
- A price at which the number of bids above it equals the number of asks below it is a [competitive equilibrium](/competitive-equilibrium/) price of the market.

## Known results in the model

- **Efficient trades.** Sort the bids $b_{(1)} \ge b_{(2)} \ge \cdots$ and the asks $s_{(1)} \le s_{(2)} \le \cdots$, and let $k$ be the largest $t$ with $b_{(t)} \ge s_{(t)}$. The first $k$ buyers and sellers trade in every efficient outcome, and every price in $[\max(s_{(k)}, b_{(k+1)}), \min(b_{(k)}, s_{(k+1)})]$ clears the market.
- **Impossibility.** Myerson and Satterthwaite (1983) showed that with one buyer and one seller, independent values with overlapping supports and positive densities, no mechanism is efficient, Bayesian incentive compatible, interim individually rational and weakly budget balanced.
- **VCG runs a deficit.** The [VCG mechanism](/vcg-mechanism/) for the double auction makes all $k$ efficient trades; each buyer pays $\max(s_{(k)}, b_{(k+1)})$ and each seller receives $\min(b_{(k)}, s_{(k+1)})$. It is DSIC and individually rational, but the sellers receive at least what the buyers pay, so the market maker must pay the difference.
- **Trade reduction.** [McAfee's mechanism](/mcafee-trade-reduction/) (1992) is DSIC, individually rational and weakly budget balanced, and loses at most the least valuable efficient trade, so it gets at least a $1 - 1/k$ fraction of the gains from trade.
- **The $k$-double auction.** The pair trades when $b \ge s$, at the price $\lambda b + (1 - \lambda) s$ for a fixed weight $\lambda \in [0, 1]$ (the literature calls the weight $k$). This simple format is not truthful. Chatterjee and Samuelson (1983) found its equilibria for bilateral trade, and in large markets its equilibria approach efficiency, as the impossibility theorem allows.
- **Experiments.** Vernon Smith's laboratory markets in the early 1960s showed that continuous double auctions reach prices and quantities near the competitive equilibrium quickly, even with few traders.

## References
