---
tag: AYJGGA
kind: algorithm
slug: kelso-crawford-process
name: Kelso-Crawford salary adjustment process
aliases:
- Kelso-Crawford ascending auction
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: An ascending auction in which bidders take items at the price plus a fixed step and items go to the last bidder. With gross substitutes valuations it ends at an approximate Walrasian equilibrium.
model: word-ram
complexity:
  vars: {n: the number of bidders, m: the number of items, V: the largest value of a bundle, k: the number of price steps per unit of value}
  time: {worst: O(k V n m^2 2^m)}
  space: {extra: O(2^m + n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1982
  people: [Alexander S. Kelso, Vincent P. Crawford]
  note: Kelso and Crawford introduced the gross substitutes condition and the salary adjustment process in 1982, extending the job matching model of Crawford and Knoer (1981); Gul and Stacchetti (1999, 2000) and Paes Leme (2017) restated it as an ascending auction.
prereqs: [gross-substitutes, gale-shapley]
see_also: [demange-gale-sotomayor-auction, gross-substitutes, combinatorial-auction, demand-query, english-auction, simultaneous-ascending-auction, competitive-equilibrium, tatonnement]
sources:
  - paper: doi:10.2307/1913392
    title: Alexander S. Kelso and Vincent P. Crawford, Job matching, coalition formation, and gross substitutes, Econometrica 50(6), 1483 to 1504 (1982)
    locator: the whole paper (the salary adjustment process and the gross substitutes condition)
  - paper: doi:10.1006/jeth.1999.2531
    title: Faruk Gul and Ennio Stacchetti, Walrasian equilibrium with gross substitutes, Journal of Economic Theory 87(1), 95 to 124 (1999)
    locator: the whole paper (existence of Walrasian equilibrium and the maximal class that contains unit demand)
  - paper: doi:10.1006/jeth.1999.2580
    title: Faruk Gul and Ennio Stacchetti, The English auction with differentiated commodities, Journal of Economic Theory 92(1), 66 to 95 (2000)
    locator: the whole paper (an exact ascending auction for gross substitutes)
  - paper: doi:10.1016/j.geb.2017.10.016
    title: Renato Paes Leme, Gross substitutability, an algorithmic survey, Games and Economic Behavior 106, 294 to 316 (2017)
    locator: Section 1 (the Walrasian tatonnement with personalized prices and Theorem 1.4)
  - paper: doi:10.1257/0002828054825466
    title: John William Hatfield and Paul R. Milgrom, Matching with contracts, American Economic Review 95(4), 913 to 935 (2005)
    locator: the whole paper (a common frame for deferred acceptance and the Kelso-Crawford process)
---

The Kelso-Crawford process is an ascending auction for many items in which each bidder may want a bundle. A bidder sees the current price for each item she holds and the price plus a fixed step $\delta$ for every other item; she takes the new items of her best bundle, and their prices rise by $\delta$. When every bidder has [gross substitutes](/gross-substitutes/) valuations, she never needs to give back an item, and the process ends at an allocation that is optimal up to $m\delta$ and supported by prices. The [Demange-Gale-Sotomayor auction](/demange-gale-sotomayor-auction/) is the exact, round-based version for unit-demand bidders; this process allows bundles but ends only near an equilibrium. The [tatonnement](/tatonnement/) of general equilibrium theory adjusts prices of divisible goods in both directions, while here prices only rise and goods are indivisible.

## In plain words

Several firms want to hire workers, and each worker goes to the firm that offers the highest salary. A firm can want many workers. Each firm in turn looks at the salaries and asks: which group of workers gives me the most profit? For workers it already has, it pays the current salary. For others, it must offer a bit more. It makes offers to the new workers it wants, and those workers leave their old firms. Salaries only go up. When no firm wants to make a new offer, the process stops. If no firm ever drops a worker just because other workers got more expensive, every firm keeps the workers it has, and the final hiring is almost the best for all firms together.

## The problem

There are $n$ bidders and $m$ items. Bidder $i$ has a valuation $v_i$ that gives a value to each bundle of items, with $v_i(\varnothing) = 0$. Utility is quasilinear: bidder $i$ with bundle $S$ at prices $p$ gets $v_i(S) - p(S)$, where $p(S) = \sum_{j \in S} p_j$. Items have no preferences except for money; in the job market reading, the bidders are firms, the items are workers and prices are salaries. The demand set $D_i(p)$ is the set of bundles of maximum utility, and asking for one of them is a [demand query](/demand-query/).

The goal is a Walrasian ([competitive](/competitive-equilibrium/)) equilibrium: prices $p$ and an allocation of disjoint bundles $X_1, \ldots, X_n$ with $X_i \in D_i(p)$ for every bidder and price $0$ on unsold items. Such an allocation maximizes the total value $\sum_i v_i(X_i)$. This is the welfare problem of a [combinatorial auction](/combinatorial-auction/). For general valuations an equilibrium may not exist; Kelso and Crawford (1982) proved that it exists when every valuation has gross substitutes.

## The algorithm

```pseudo id=main
KELSO-CRAWFORD(valuations v_1, ..., v_n, step δ)
L1  p_j ← 0 and owner_j ← none for every item j
L2  repeat
L3      changed ← false
L4      for each bidder i do
L5          X ← {j : owner_j = i}
L6          q_j ← p_j for j ∈ X;  q_j ← p_j + δ for j ∉ X
L7          S ← a bundle of D_i(q) with X ⊆ S
L8          for each j ∈ S \ X do p_j ← p_j + δ;  owner_j ← i;  changed ← true
L9  until not changed
L10 return p and the bundles {j : owner_j = i}
```

The vector $q$ of line L6 holds the *personalized prices* of bidder $i$: to take an item she must outbid its owner by $\delta$. Line L7 asks for a demanded bundle that keeps all her items; gross substitutes is exactly what makes such a bundle exist. Items she loses leave her bundle only when another bidder takes them at line L8. The implementation picks the smallest such bundle, enumerates all $2^m$ bundles to find the demand set, keeps prices in `Fraction`, uses $\delta = 1/(m+1)$ by default, and raises `ValueError` when line L7 finds no bundle.

## Example

Two items $a$ and $b$ and step $\delta = 1/3$. Bidder 1 is additive with $v_1(a) = 2$ and $v_1(b) = 1$. Bidder 2 wants one item at most and values each at $2$. The best allocation gives $a$ to bidder 1 and $b$ to bidder 2, for a total of $4$.

| turn | bidder | holds | personalized prices $(a, b)$ | bundle chosen | prices after $(a, b)$ |
|---|---|---|---|---|---|
| 1 | 1 | nothing | $(1/3, 1/3)$ | $\{a, b\}$ | $(1/3, 1/3)$ |
| 2 | 2 | nothing | $(2/3, 2/3)$ | $\{a\}$ (tie with $\{b\}$) | $(2/3, 1/3)$ |
| 3 | 1 | $\{b\}$ | $(1, 1/3)$ | $\{a, b\}$ | $(1, 1/3)$ |
| 4 | 2 | nothing | $(4/3, 2/3)$ | $\{b\}$ | $(1, 2/3)$ |
| 5 | 1 | $\{a\}$ | $(1, 1)$ | $\{a\}$ (tie with $\{a, b\}$) | no change |
| 6 | 2 | $\{b\}$ | $(4/3, 2/3)$ | $\{b\}$ | no change |

Bidder 1 gets $a$ for $1$ and bidder 2 gets $b$ for $2/3$, the optimal allocation. Bidder 1 loses $b$ in turn 4 without asking to; that is the mechanism by which bundles shrink. The test file reproduces this trace.

## Correctness

The proof is in `proofs/correctness.md`. Its key steps:

1. Right after a turn of bidder $i$, her bundle is demanded at her personalized prices.
2. Until her next turn, her personalized prices only rise, and the prices of the items she still holds do not change. By gross substitutes she still demands a bundle that contains those items, so line L7 never fails.
3. A bidder takes item $j$ only if its marginal value in her bundle is at least its new price, so every price stays at most $V$, and there are at most $mV/\delta$ bids.
4. At the end, for every bidder $i$ and every bundle $T$, $v_i(X_i) - p(X_i) \ge v_i(T) - p(T) - \delta |T \setminus X_i|$, and every unsold item has price $0$. So the outcome is a Walrasian equilibrium up to $\delta$ per item.
5. Summing step 4 over an optimal allocation gives total value at least $\mathrm{OPT} - m\delta$. With integer values and $\delta < 1/m$, the allocation is optimal.

## Complexity

Let $k = 1/\delta$. There are at most $mVk$ bids, so at most $mVk + 1$ passes of lines L2 to L9 and $n(mVk + 1)$ turns. With demand found by enumeration, a turn costs $O(m 2^m)$ time, so the total is $O(k V n m^2 2^m)$. With a demand oracle instead, the process makes $O(kVnm)$ demand queries; for gross substitutes valuations a demand query can be answered with $O(m^2)$ value queries by a greedy algorithm (Paes Leme 2017). The extra space is $O(2^m)$ for the enumerated demand set and $O(n + m)$ for the holdings.

The time is pseudo-polynomial in the values and grows as $1/\delta$. To find an exact equilibrium, prices can also be computed from the dual of a linear program, which has integral solutions for gross substitutes.

## Properties

- **Monotone prices.** Prices never go down, and each bid raises one price by $\delta$.
- **No item is given back.** Under gross substitutes a bidder never drops an item by choice; she loses items only when outbid.
- **Approximate equilibrium.** The final prices and bundles satisfy the equilibrium conditions up to $\delta$ per item.
- **Optimal for small steps.** With integer values and $\delta < 1/m$, the final allocation maximizes the total value.
- **Not exactly truthful.** The final prices are not the VCG payments in general, and a bidder with many items can gain by demand reduction.
- **Order dependent.** The outcome depends on the order of bidders and on how ties are broken.

## Variants and improvements

- **The original job market.** In Kelso and Crawford (1982) workers have preferences over firms and salaries. Firms make salary offers, each worker holds her best offer and rejects the others, and a firm raises a rejected offer by a fixed step in the next round. With salaries held fixed, the process is the many-to-one [Gale-Shapley](/gale-shapley/) deferred acceptance with firms proposing.
- **Exact auctions.** Gul and Stacchetti (2000) gave an ascending auction for gross substitutes that raises the prices of a minimal set in excess demand and ends at the minimum Walrasian prices. For unit demand it is the [DGS auction](/demange-gale-sotomayor-auction/).
- **Matching with contracts.** Hatfield and Milgrom (2005) put deferred acceptance and this process into one frame, with a substitutes condition on the choice of contracts.
- **Spectrum auctions.** The [simultaneous ascending auction](/simultaneous-ascending-auction/) uses the same rising prices on many items with an activity rule, but bidders there often see items as complements, and then the guarantees here do not hold.
- **Single item.** With one item, the process is an [English auction](/english-auction/) with step $\delta$: the bidder with the highest value wins at about the second highest value.

## When to use it

Use it as a model of decentralized price formation in labor or goods markets where buyers want bundles of substitutes, or to run an ascending auction when bidders can answer demand queries but should not report whole valuations. It is the simplest algorithm that shows why gross substitutes makes Walrasian equilibrium exist.

## Pitfalls

- With complements, line L7 can fail. If bidder 1 values only the pair $\{a, b\}$ at $3$ and bidder 2 values $b$ at $3$, bidder 1 can end up holding $a$ while $b$ gets too expensive, and then no demanded bundle keeps $a$. The implementation raises `ValueError` here; a market version would leave her with an item she does not want (the exposure problem).
- A large $\delta$ can end far from the optimum: the guarantee is only $\mathrm{OPT} - m\delta$.
- A plain demand query can return a demanded bundle that drops a held item when there are ties. Line L7 needs a demanded bundle that keeps all held items; break ties in favor of held items, or take the whole demand set.
- Gross substitutes is a property of the whole valuation. Checking it from samples of bundles is not enough; see [gross substitutes](/gross-substitutes/) for exact tests.

## Implementations

## History

Crawford and Knoer (1981) studied a salary adjustment process for one-to-one job matching. Kelso and Crawford (1982) let firms hire many workers, introduced the gross substitutes condition and showed that the process reaches a core allocation, which gives the existence of equilibrium. Gul and Stacchetti (1999) showed that gross substitutes is the largest class that contains unit-demand valuations and always has an equilibrium, and in 2000 gave an exact English auction for it. Hatfield and Milgrom (2005) joined this process and deferred acceptance in matching with contracts. Paes Leme (2017) surveyed the algorithmic side of gross substitutes and wrote the process in the form used here.

## References
