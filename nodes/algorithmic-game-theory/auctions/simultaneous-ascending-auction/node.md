---
tag: 427AF8
kind: algorithm
slug: simultaneous-ascending-auction
name: Simultaneous ascending auction
aliases:
- SAA
- simultaneous multiple round auction
area: algorithmic-game-theory/auctions
level: advanced
summary: "Sells many items at once in rounds: bidders bid on the items they want at rising prices until a round has no new bid. Near-efficient with substitutes; complements cause exposure."
model: word-ram
complexity:
  vars: {n: the number of bidders, m: the number of items, r: the largest value of a bundle divided by the price increment}
  time: {worst: O(n m^2 2^m r)}
  space: {extra: O(m 2^m)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1994
  people: [Paul Milgrom, Robert Wilson, R. Preston McAfee]
  note: Milgrom, Wilson and McAfee proposed the format for the US spectrum auctions, and the Federal Communications Commission first used it in 1994.
prereqs: [combinatorial-auction, english-auction, demand-query]
see_also: [gross-substitutes, kelso-crawford-process, demange-gale-sotomayor-auction, competitive-equilibrium, vcg-mechanism, uniform-price-auction, bidding-languages, winner-determination-problem]
sources:
  - paper: doi:10.1086/262118
    title: "Paul Milgrom, Putting auction theory to work: the simultaneous ascending auction, Journal of Political Economy 108(2) (2000), 245-272"
    locator: the rules of the auction, the convergence to a competitive equilibrium with substitutes and straightforward bidding, and the problems with complements
  - book: isbn:9780262033428
    title: "Peter Cramton, Yoav Shoham and Richard Steinberg (eds.), Combinatorial Auctions, MIT Press, 2006"
    locator: Chapter 4 (Cramton, Simultaneous ascending auctions)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 8 (spectrum auctions, the exposure problem and demand reduction)
  - book: isbn:9780521536721
    title: Paul Milgrom, Putting Auction Theory to Work, Cambridge University Press, 2004
    locator: the chapters on the simultaneous ascending auction and on substitutes
---

The simultaneous ascending auction (SAA) sells many different items at once. Every item has its own price, all prices start low, and the auction runs in rounds. In each round every bidder may bid on any item at its current price plus an increment, and the highest bidder on an item becomes its standing winner. The auction closes when a round passes with no new bid on any item, and each item goes to its standing winner at its price. When the bidders see items as [substitutes](/gross-substitutes/) and bid straightforwardly, SAA ends close to a [Walrasian equilibrium](/competitive-equilibrium/), and its welfare is within $m\epsilon$ of the optimum for $m$ items and increment $\epsilon$. When some bidder needs several items together, it can be stuck with part of a package it no longer wants. This is the *exposure problem*. Governments have used SAA to sell radio spectrum licenses since 1994.

## In plain words

Many items are for sale at the same time, each with its own price. Prices start at zero. In each round, every buyer looks at the prices and decides which items it would most like to own, then bids a little more on those it does not already hold. Items with new bids get a new leader and a higher price. When a round passes with no new bid anywhere, the auction ends. Because all items close together, a buyer can switch from one item to another as prices change. This works well when items can replace each other. A buyer that needs two items together can be left holding one of them at a price it regrets.

## The problem

There are $m$ items and $n$ bidders. Bidder $i$ has a valuation $v_i$ on sets of items, with $v_i(\emptyset) = 0$, monotone, and [quasilinear utility](/quasilinear-utility/). The auction learns about the valuations only through bids, and it must give each item to at most one bidder and set a price for each item. The goal is high welfare $\sum_i v_i(H_i)$ for the final holdings $H_i$, with prices at which each bidder is happy with what it holds. We model the bidders as *straightforward*: in each round, a bidder asks for a bundle it most prefers at the current prices, which is a [demand query](/demand-query/), and bids on the items of that bundle that it does not hold.

## The algorithm

```pseudo id=main
SAA(v_1, ..., v_n, m, ε)
L1  for each item j: p_j ← 0, holder_j ← NIL
L2  repeat
L3      for each bidder i
L4          H_i ← the items with holder i; q_j ← p_j for j in H_i and q_j ← p_j + ε otherwise
L5          T_i ← a bundle that maximizes v_i(T) - Σ_{j ∈ T} q_j, preferring one that contains H_i
L6          bid on each item of T_i \ H_i
L7      if there was no new bid: stop
L8      for each item j with new bids
L9          holder_j ← the new bidder with the smallest index; p_j ← p_j + ε
L10 return the holdings H_1, ..., H_n and the prices p
```

A bid cannot be withdrawn. The standing winner of an item keeps it until someone bids more. The code computes line L5 by trying all $2^m$ bundles, which stands for the bidder's own decision.

## Example

**Two unit-demand bidders.** Bidder 1 values item A at 5 and item B at 4 and wants one item. Bidder 2 values A at 3 and B at 4. With $\epsilon = 1$: in round 1 both want an item at prices $(1, 1)$; bidder 1 bids on A and bidder 2 on B. In round 2 each holds its best item and nobody bids. Bidder 1 gets A at 1 and bidder 2 gets B at 1, the optimal allocation.

**The exposure problem.** Bidder 1 values the pair $\{A, B\}$ at 10 and each single item at 0. Bidder 2 values A at 9 and bidder 3 values B at 3. With $\epsilon = 1$:

| rounds | what happens | prices of A, B |
|---|---|---|
| 1 | all bid; bidder 1 leads on both | $1, 1$ |
| 2 | bidder 2 takes A, bidder 3 takes B | $2, 2$ |
| 3 | bidder 1 takes both back | $3, 3$ |
| 4 to 8 | bidder 3 stops at 3; bidders 1 and 2 raise A in turns | $8, 3$ |
| 9 | the pair would cost at least $12 > 10$, so bidder 1 stops | $8, 3$ |

Bidder 2 wins A at 8, and bidder 1 is left with B at 3, worth 0 to it alone, so its utility is $-3$. The welfare is 9, while giving A to bidder 2 and B to bidder 3 gives 12.

## Correctness

The proof is in `proofs/correctness.md`. It shows these facts.

- **Termination.** No price exceeds the largest value $V$, every round that does not stop raises the sum of the prices by at least $\epsilon$, so there are at most $mV/\epsilon + 1$ rounds. Unsold items keep the price 0.
- **Holdings stay wanted under gross substitutes.** If every valuation has [gross substitutes](/gross-substitutes/), then in each round each bidder demands a bundle that contains what it holds. The proof is an induction on the rounds: the personal prices of held items do not change and the others do not fall.
- **Near equilibrium at the end.** When no bidder bids, each holds a bundle it demands at its personal prices and has utility at least 0. Summing the demand inequalities gives welfare at least $\mathrm{OPT} - m\epsilon$. As $\epsilon \to 0$ this is the [Kelso-Crawford process](/kelso-crawford-process/) with simultaneous bids.
- **The exposure problem.** The example shows that with complements a straightforward bidder can end with negative utility and the welfare can be far from the optimum.

## Complexity

There are at most $mV/\epsilon + 1$ rounds. Each round asks $n$ demand queries; answering one by trying all $2^m$ bundles takes $O(m 2^m)$ time, and the bookkeeping takes $O(nm)$. With $r = V/\epsilon$, the total is $O(n m^2 2^m r)$ time. For valuations with a fast demand oracle, such as unit-demand or additive ones, the $2^m$ factor is replaced by the cost of the oracle. The number of rounds grows with $1/\epsilon$, so real auctions use increments of a few percent of the price.

## Properties

- **Price discovery.** Bidders see the prices of all items during the auction and can move between substitutes.
- **Near-efficient with substitutes.** Under gross substitutes and straightforward bidding, welfare is within $m\epsilon$ of the optimum, and the final prices are an approximate [competitive equilibrium](/competitive-equilibrium/).
- **Not truthful.** Straightforward bidding is not an equilibrium in general. A bidder that wants several units can reduce its demand to keep prices low, as in the [uniform price auction](/uniform-price-auction/).
- **Exposure.** With complements, a bidder that bids for a package risks winning only part of it.
- **No package bids.** A bidder cannot say that it wants items only together.

## Variants and improvements

- **Activity rules.** Real SAAs require each bidder to bid on enough items in each round to keep its eligibility, so that bidders cannot wait until the end and hide their demand.
- **Bid withdrawal.** Some versions allow a bidder to withdraw a standing bid for a penalty, which softens the exposure problem.
- **Combinatorial clock auction.** Clock prices rise on items with excess demand, bidders report bundles, and a final sealed round with package bids decides the allocation and payments. This removes exposure at the cost of solving the [winner determination problem](/winner-determination-problem/).
- **Ascending proxy auction.** Proxy agents bid on packages for the bidders and end in a core outcome.
- **Item-price auctions in theory.** With unit-demand bidders the process is close to the [Demange-Gale-Sotomayor auction](/demange-gale-sotomayor-auction/), which raises prices on overdemanded sets of items and ends near the minimum Walrasian prices.

## When to use it

Use SAA to sell many related items when the bidders see them mostly as substitutes, value the price information that an open auction gives, and the seller wants a simple format without package bids. When bidders have strong complements, such as licenses that are only useful together, use a format with package bids instead.

## Pitfalls

- **Straightforward bidding is an assumption.** The welfare bound holds for straightforward bidders with gross substitutes, not for strategic bidders.
- **Exposure.** A bidder that needs a package can lose money; risk-averse bidders then bid less, which also lowers welfare.
- **Ties in line L5.** The tie rule matters. Preferring a bundle that contains the held items keeps the gross substitutes argument valid; another rule can make bidders drop and retake items.
- **Increment size.** A large $\epsilon$ ends quickly but loses up to $m\epsilon$ welfare; a small one takes many rounds.

## Implementations

## History

The US Federal Communications Commission received authority to auction spectrum licenses in 1993. Paul Milgrom, Robert Wilson and R. Preston McAfee proposed the simultaneous ascending auction for it, and the first such auction ran in July 1994. The format raised large revenue and was copied by many countries. Milgrom (2000) explained its theory: with substitutes and straightforward bidding it reaches a competitive equilibrium, and with complements it suffers from exposure. The later move to package bidding, such as combinatorial clock auctions, came from these limits.

## References
