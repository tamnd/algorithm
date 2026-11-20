---
tag: RZZ6FP
kind: algorithm
slug: demange-gale-sotomayor-auction
name: Demange-Gale-Sotomayor auction
aliases:
- DGS auction
- exact auction for unit-demand bidders
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: An ascending auction for unit-demand bidders that raises the prices of a minimal overdemanded set of items by one unit per round. It stops at the minimum Walrasian prices, the VCG payments.
solves: [assignment-problem]
model: word-ram
complexity:
  vars: {n: the number of bidders, m: the number of items, V: the largest value}
  time: {worst: O(V n^2 m^3)}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1986
  people: [Gabrielle Demange, David Gale, Marilda Sotomayor]
  note: Demange, Gale and Sotomayor gave the exact auction and an approximate auction in 1986, building on the assignment game of Shapley and Shubik (1971) and the result of Leonard (1983) that the minimum equilibrium prices are the VCG payments.
prereqs: [assignment-problem, bipartite-matching, hall-theorem]
see_also: [assignment-game, auction-algorithm, hungarian-algorithm, kelso-crawford-process, gross-substitutes, competitive-equilibrium, vcg-mechanism, english-auction]
sources:
  - paper: doi:10.1086/261411
    title: Gabrielle Demange, David Gale and Marilda Sotomayor, Multi-item auctions, Journal of Political Economy 94(4), 863 to 872 (1986)
    locator: the whole paper (the exact auction and the approximate auction)
  - paper: doi:10.1007/BF01753437
    title: Lloyd S. Shapley and Martin Shubik, The assignment game I, the core, International Journal of Game Theory 1(1), 111 to 130 (1971)
    locator: the whole paper (existence of competitive prices and the lattice of core payoffs)
  - paper: doi:10.1086/261158
    title: Herman B. Leonard, Elicitation of honest preferences for the assignment of individuals to positions, Journal of Political Economy 91(3), 461 to 479 (1983)
    locator: the whole paper (the minimum competitive prices are the VCG payments, so the minimum-price rule is truthful)
  - paper: doi:10.1006/jeth.1999.2580
    title: Faruk Gul and Ennio Stacchetti, The English auction with differentiated commodities, Journal of Economic Theory 92(1), 66 to 95 (2000)
    locator: the whole paper (the ascending auction for gross substitutes valuations)
  - book: isbn:9780521437882
    title: Alvin E. Roth and Marilda A. Oliveira Sotomayor, Two-Sided Matching, a Study in Game-Theoretic Modeling and Analysis, Cambridge University Press (1990)
    locator: the part on one-to-one matching with money (the assignment game and its auctions)
---

The Demange-Gale-Sotomayor auction (DGS auction) sells $m$ different items to $n$ bidders who each want at most one item. It is an ascending auction: all prices start at zero, and in each round the auctioneer raises by one unit the price of every item in a minimal overdemanded set, a set of items that too many bidders want and nothing else. It stops at the minimum Walrasian prices, and these are the VCG payments, so the auction is a dynamic form of the [VCG mechanism](/vcg-mechanism/) for unit-demand bidders. It solves the same optimization as the [Hungarian algorithm](/hungarian-algorithm/), which computes an optimal assignment with dual prices but has no rule that picks the minimum prices, and it is close to the [auction algorithm](/auction-algorithm/) of Bertsekas, an optimization method in which one bidder at a time raises one price by its bid increment plus $\varepsilon$ and which ends only near an optimum. The [Kelso-Crawford process](/kelso-crawford-process/) extends the ascending idea from unit demand to [gross substitutes](/gross-substitutes/) valuations.

## In plain words

Each bidder wants one item at most and knows what each item is worth to her. The auctioneer calls out prices, at first all zero. Each bidder names the items that give her the best deal at these prices. If some group of items is wanted by more bidders than there are items in the group, and those bidders want nothing outside it, the auctioneer raises the price of each item in the smallest such group by one. Prices only go up. When no group is overwanted, each bidder can get one of her favorite items, and the auctioneer hands them out. The final prices are the lowest prices at which supply meets demand, and no bidder gains by lying about her values.

## The problem

There are $n$ bidders and $m$ items. Bidder $i$ has a nonnegative integer value $v_{ij}$ for item $j$ and is unit-demand: she buys at most one item, and her utility for item $j$ at prices $p$ is $v_{ij} - p_j$, with utility $0$ for buying nothing (the null option $\varnothing$). Her demand set $D_i(p)$ is the set of options of maximum utility. A *Walrasian equilibrium* (competitive equilibrium) is a price vector $p \ge 0$ with an assignment $\mu$ that gives each bidder an option in her demand set, no item twice, and leaves only items of price $0$ unsold. Shapley and Shubik (1971) proved that equilibria exist, that every equilibrium assignment maximizes the total value $\sum_i v_{i \mu(i)}$ (the [assignment problem](/assignment-problem/)), and that the equilibrium price vectors form a lattice with a smallest element $p^*$. The task is to find $p^*$ and an equilibrium assignment. This is the market of the [assignment game](/assignment-game/) with buyers who hold no items and items whose sellers value them at $0$.

A set $S$ of items is *overdemanded* at $p$ when more than $|S|$ bidders have $D_i(p) \subseteq S$. By [Hall's theorem](/hall-theorem/), no set is overdemanded exactly when the bidders who strictly want some item can all get distinct demanded items. It is *minimal* when no proper subset is overdemanded.

## The algorithm

```pseudo id=main
DGS-AUCTION(values v)
L1  p_j ← 0 for every item j
L2  loop
L3      D_i ← the demand set of bidder i at p, for every i
L4      M ← a maximum matching of the bidders with ∅ ∉ D_i to distinct items of their demand sets
L5      if M matches every such bidder then exit the loop
L6      T ← the items reachable by alternating paths from a bidder that M leaves unmatched
L7      S ← T;  for each j ∈ T do if S \ {j} contains an overdemanded set then S ← S \ {j}
L8      p_j ← p_j + 1 for every j ∈ S
L9  for each unsold item j with p_j > 0 do flip an alternating path from j to an unmatched bidder or to an item of price 0
L10 return p and the assignment given by M
```

Lines L6 and L7 find a minimal overdemanded set. The items reached from an unmatched bidder form an overdemanded set, and line L7 shrinks it one item at a time, using the test of Hall's theorem to see whether a smaller set still contains an overdemanded set. Line L9 is needed because the matching of line L4 may leave an item with a positive price unsold; the flip moves a sale from an item of price $0$, or to a bidder who is happy with nothing, onto that item. The implementation keeps all prices as exact integers in `Fraction`.

## Example

Three bidders and three items $x_1, x_2, x_3$, with values

| | $x_1$ | $x_2$ | $x_3$ |
|---|---|---|---|
| bidder 1 | 4 | 6 | 2 |
| bidder 2 | 5 | 6 | 1 |
| bidder 3 | 3 | 7 | 4 |

| round | prices $(x_1, x_2, x_3)$ | demand sets of bidders 1, 2, 3 | minimal overdemanded set |
|---|---|---|---|
| 1 | $(0, 0, 0)$ | $\{x_2\}$, $\{x_2\}$, $\{x_2\}$ | $\{x_2\}$, wanted alone by 3 bidders |
| 2 | $(0, 1, 0)$ | $\{x_2\}$, $\{x_1, x_2\}$, $\{x_2\}$ | $\{x_2\}$, wanted alone by bidders 1 and 3 |
| 3 | $(0, 2, 0)$ | $\{x_1, x_2\}$, $\{x_1\}$, $\{x_2\}$ | $\{x_1, x_2\}$, wanted alone by all 3 bidders |
| 4 | $(1, 3, 0)$ | $\{x_1, x_2\}$, $\{x_1\}$, $\{x_2, x_3\}$ | none |

In round 3, neither $\{x_1\}$ (wanted alone only by bidder 2) nor $\{x_2\}$ (only by bidder 3) is overdemanded, so the minimal set is $\{x_1, x_2\}$. In round 4, bidder 2 gets $x_1$, bidder 1 gets $x_2$ and bidder 3 gets $x_3$. The final prices are $(1, 3, 0)$, and the utilities are $6 - 3 = 3$, $5 - 1 = 4$ and $4 - 0 = 4$. The assignment has total value $15$, the optimum. The prices are the VCG payments: without bidder 1 the best total value is $12$ and the others get $9$ with her, so she pays $3$; without bidder 2 it is $11$ against $10$, so he pays $1$; without bidder 3 it is $11$ against $11$, so she pays $0$.

With one item and values $(10, 7, 3)$, the price rises by one per round while at least two bidders strictly want the item, and the auction stops at $7$: the bidder with value $10$ wins and pays $7$, as in the [Vickrey auction](/vickrey-auction/). The tests reproduce both examples.

## Correctness

The proof is in `proofs/correctness.md`. It has four steps.

1. Lines L6 and L7 return an overdemanded set with no overdemanded proper subset. The reachable set of an unmatched bidder is overdemanded because every reachable item is matched (else the matching could grow), and the shrinking step keeps exactly what is needed.
2. Prices never pass $p^*$. If $p \le p^*$ and $S$ is minimal overdemanded at $p$, then every item of $S$ has $p_j < p^*_j$. Otherwise the items of $S$ already at their minimum price would absorb at most as many bidders as they number, and the rest of $S$ would be a smaller overdemanded set.
3. Prices do not stop below $p^*$. If $p \le p^*$ and $p \ne p^*$, the set $\{j : p_j < p^*_j\}$ is overdemanded. Otherwise, lowering these prices slightly from $p^*$ would give a Walrasian price vector below $p^*$, against its minimality.
4. At $p = p^*$, line L9 can always repair the matching. The symmetric difference with a Walrasian assignment gives the alternating path it needs.

The proof uses that $p^*$ is an integer vector, which holds because $p^*$ equals the VCG payments (Leonard 1983) and these are differences of optimal assignment values.

## Complexity

Each round raises the integer $\sum_j p_j$ by at least one, and the prices end at $p^*$, so there are at most $\sum_j p^*_j \le mV$ rounds, where $V$ is the largest value. In a round, line L3 takes $O(nm)$ time. A maximum matching by augmenting paths takes $O(n \cdot nm)$ time. Line L7 calls a matching up to $m$ times, so a round costs $O(n^2 m^2)$ and the whole auction $O(V n^2 m^3)$. Line L9 runs at most $m$ breadth-first searches of $O(nm)$ each. The space is $O(nm)$ for the values and demand sets.

The bound is pseudo-polynomial: it grows with the values, not with their bit length. The Hungarian algorithm finds an optimal assignment, with dual prices, in $O(n^3)$ time for $n = m$, and the minimum prices can then be computed from it, so the auction is not the fastest way to compute $p^*$. Its point is that it is an auction: bidders only report demand sets at posted prices.

## Properties

- **Truthful.** As a direct mechanism (bidders report values, the auctioneer simulates the auction), it charges the VCG payments, so truthful bidding is a dominant strategy (Leonard 1983; Demange, Gale and Sotomayor 1986). In the live auction, reporting true demand sets is an ex post equilibrium.
- **Efficient.** The final assignment maximizes the total value, by the first welfare theorem for this market.
- **Bidder-optimal.** Among all Walrasian equilibria, $p^*$ gives every bidder her highest utility at once. It is the best point of the core of the assignment game for the buyers.
- **Monotone prices.** Prices never go down, and the auction uses only demand information at posted prices.
- **Ties.** Ties among items in a demand set are allowed. The minimal overdemanded set may not be unique; the final prices do not depend on which one is raised, because they always equal $p^*$.

## Variants and improvements

- **The approximate auction.** In the same 1986 paper, bidders bid one at a time and raise a price by a fixed increment, much as in Bertsekas's auction algorithm. The final prices are close to $p^*$ when the increment is small.
- **Gross substitutes.** Kelso and Crawford (1982) gave an ascending process for bidders who want bundles with [gross substitutes](/gross-substitutes/) valuations, and Gul and Stacchetti (2000) gave an exact ascending auction for that class that ends at the minimum Walrasian prices; see [Kelso-Crawford process](/kelso-crawford-process/).
- **Sellers with reserve values.** In the assignment game, each item has a seller with a reservation value; start each price at that value instead of $0$.
- **Simultaneous ascending auctions** in spectrum sales use the same idea of rising prices on many items at once; see [simultaneous ascending auction](/simultaneous-ascending-auction/).

## When to use it

Use it to explain or to run an ascending auction for many different items when each bidder wants one item (housing units, time slots, jobs). It gives the VCG outcome without asking bidders to report all their values. To compute an optimal assignment or $p^*$ offline, use the Hungarian algorithm or a min-cost flow instead; they are strongly polynomial.

## Pitfalls

- Raising the prices of any overdemanded set, not a minimal one, can overshoot $p^*$. Let bidders 1 and 2 value the first item at $10$ and $7$ and the second at $0$, and let bidder 3 value only the second item, at $1$. At prices $(0, 0)$ the set of both items is overdemanded, but raising the second price is wrong: only bidder 3 wants that item, so its minimum price is $0$.
- A bidder whose maximum utility is $0$ also demands the null option. She is not counted in any overdemanded set, and treating her as required makes prices rise too far.
- The matching of line L4 can leave a positive-price item unsold even at $p^*$; skipping line L9 can return an assignment that is not an equilibrium.
- Non-integer values need a price step smaller than the value gaps, or a scaled problem; with step 1 and real values the auction ends only near $p^*$.
- The auction is not truthful for bidders who want more than one item; see the [Kelso-Crawford process](/kelso-crawford-process/) and [combinatorial auction](/combinatorial-auction/) for that case.

## Implementations

## History

Shapley and Shubik (1971) introduced the assignment game and proved that its core, which is the set of Walrasian outcomes, is a nonempty lattice. Crawford and Knoer (1981) and Kelso and Crawford (1982) studied salary adjustment processes for job markets. Leonard (1983) showed that the minimum equilibrium prices are the VCG payments, so the minimum-price rule is truthful. Demange, Gale and Sotomayor (1986) gave the exact auction with minimal overdemanded sets and proved that it stops at the minimum prices, and an approximate auction with bid increments. Gul and Stacchetti (2000) extended the exact auction to gross substitutes.

## References
