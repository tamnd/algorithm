---
tag: NGK04Z
kind: model
slug: combinatorial-auction
name: Combinatorial auction
aliases:
- package auction
area: algorithmic-game-theory/auctions
level: core
summary: "An auction of many different items in which each bidder values bundles of items, so that a bidder can want items only together (complements) or only one of several (substitutes)."
prereqs: [quasilinear-utility, vcg-mechanism]
see_also: [winner-determination-problem, bidding-languages, demand-query, single-minded-bidder-mechanism, simultaneous-ascending-auction, gross-substitutes, competitive-equilibrium, communication-complexity]
sources:
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: Chapter 11 (Blumrosen and Nisan, Combinatorial auctions), Sections 11.1 to 11.5
  - book: isbn:9780262033428
    title: "Peter Cramton, Yoav Shoham and Richard Steinberg (eds.), Combinatorial Auctions, MIT Press, 2006"
    locator: the introduction and the parts on mechanisms, bidding and efficiency, and complexity and algorithmic considerations
  - paper: "Michael H. Rothkopf, Aleksandar Pekec and Ronald M. Harstad, Computationally manageable combinational auctions, Management Science 44(8) (1998), 1131-1147"
    locator: the hardness of choosing the winners for general package bids and the bid structures that make it tractable
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 4 (algorithmic mechanism design and the single-minded case) and Lecture 8 (spectrum auctions)
---

A combinatorial auction sells $m$ different items to $n$ bidders at once, and lets each bidder value whole bundles of items rather than single items. This matters when items are *complements*, such as two neighboring radio licenses that are worth more together, or *substitutes*, such as two flights of which a traveler needs only one. Selling items one at a time forces a bidder to guess what it will win later, so a combinatorial auction lets it bid on packages. The model raises three questions that single-item auctions do not: choosing the best allocation is [NP-hard](/np-hard/) (the [winner determination problem](/winner-determination-problem/)), a valuation has $2^m$ numbers and needs a [bidding language](/bidding-languages/) or [queries](/demand-query/) to be described, and truthful mechanisms such as [VCG](/vcg-mechanism/) need the exact optimum, which is hard to compute.

## The machine

There is a set $M$ of $m$ items, one unit of each, and a set of $n$ bidders.

- **Valuations.** Bidder $i$ has a private valuation $v_i : 2^M \to \mathbb{R}_{\ge 0}$ with $v_i(\emptyset) = 0$. It is usually *monotone*: $S \subseteq T$ implies $v_i(S) \le v_i(T)$.
- **Allocations.** An allocation is a list of pairwise disjoint bundles $S_1, \ldots, S_n \subseteq M$. Items can stay unsold.
- **Payments and utility.** The mechanism also sets payments $p_i$, and bidder $i$ has [quasilinear utility](/quasilinear-utility/) $v_i(S_i) - p_i$.
- **Access to valuations.** A bidder can report its valuation in a bidding language, such as a list of package bids with OR and XOR rules, or the mechanism can ask it queries: a *value query* asks for $v_i(S)$, and a [demand query](/demand-query/) gives item prices and asks for a bundle that maximizes $v_i(S) - \sum_{j \in S} p_j$.

Common classes of valuations, from the most restricted:

| class | rule | example |
|---|---|---|
| single-minded | value $v$ for every superset of one bundle $S^*$, else 0 | a firm that needs one route |
| unit demand | $v(S) = \max_{j \in S} v(\{j\})$ | a buyer who wants one house |
| additive | $v(S) = \sum_{j \in S} v(\{j\})$ | no interaction between items |
| [gross substitutes](/gross-substitutes/) | a demanded item stays demanded when other prices rise | unit demand, additive |
| [submodular](/submodular-function/) | decreasing marginal values | coverage of customers |
| general | any monotone function | complements, such as a pair of licenses |

## What it counts

- **Social welfare** $\sum_i v_i(S_i)$, the main goal in algorithmic mechanism design, and the [approximation ratio](/approximation-ratio/) of a mechanism against the best welfare.
- **Revenue** $\sum_i p_i$, the goal of the seller.
- **Computation**, as time polynomial in $n$, $m$ and the size of the bids, or as the number of queries.
- **Communication**, the number of bits the bidders must send, which counts the cost of describing a valuation of $2^m$ numbers; see [communication complexity](/communication-complexity/).
- **Incentives**: whether truthful bidding is a dominant strategy ([DSIC](/dominant-strategy-incentive-compatibility/)), and the welfare of equilibria when it is not.

## Relation to other models

- With $m = 1$ it is a single-item auction, such as the [Vickrey auction](/vickrey-auction/).
- With unit-demand bidders it is the [assignment game](/assignment-game/), solved by the [assignment problem](/assignment-problem/) and by ascending auctions such as the [Demange-Gale-Sotomayor auction](/demange-gale-sotomayor-auction/).
- With identical items it is a multi-unit auction, such as the [uniform price auction](/uniform-price-auction/).
- The [position auction](/position-auction/) is a special case with ranked slots and one value per click.
- With buyers and sellers on both sides it becomes a combinatorial exchange, the many-item form of a [double auction](/double-auction/).
- Markets with prices and divisible goods, such as the [Fisher market](/fisher-market/), are the continuous relatives; their equilibria are the [competitive equilibria](/competitive-equilibrium/) of this model when items are indivisible.

## Known results in the model

- **Winner determination is hard.** Maximizing welfare over general package bids is [weighted set packing](/set-packing/). It is NP-hard, and for single-minded bids no polynomial algorithm approximates it within $m^{1/2 - \epsilon}$ unless $\mathrm{P} = \mathrm{NP}$ (Lehmann, O'Callaghan and Shoham 2002; Sandholm 2002). Some bid structures, such as intervals of a line, make it polynomial (Rothkopf, Pekec and Harstad 1998). See the [winner determination problem](/winner-determination-problem/).
- **VCG needs the optimum.** The [VCG mechanism](/vcg-mechanism/) is truthful and efficient for any valuations, but only when it computes an exact optimum; with an approximate allocation it is not truthful in general. This is why polynomial truthful mechanisms use other designs, such as [maximal-in-range mechanisms](/maximal-in-range-mechanism/) or greedy rules with critical prices.
- **Single-minded bidders.** The [Lehmann-O'Callaghan-Shoham mechanism](/single-minded-bidder-mechanism/) is truthful, polynomial and a $\sqrt m$ approximation, which is close to the best possible.
- **Walrasian equilibrium.** Prices for single items that clear the market exist exactly when the linear programming relaxation of winner determination has an integral optimum. With [gross substitutes](/gross-substitutes/) valuations they always exist, and ascending item-price auctions find them (Kelso and Crawford 1982; Gul and Stacchetti 1999). With complements they may not exist.
- **Communication.** For general valuations, finding an efficient allocation needs communication exponential in $m$, even with any type of query, and so does any approximation better than $m^{1/2 - \epsilon}$ (Nisan and Segal 2006). With demand queries, the linear programming relaxation can be solved in polynomial time, and with item prices an approximation of $\min(n, O(\sqrt m))$ is possible (Blumrosen and Nisan, Chapter 11 of Nisan, Roughgarden, Tardos and Vazirani 2007).
- **Practice.** The [simultaneous ascending auction](/simultaneous-ascending-auction/) sells spectrum without package bids and suffers from the exposure problem with complements; combinatorial clock auctions add package bids.

## References
