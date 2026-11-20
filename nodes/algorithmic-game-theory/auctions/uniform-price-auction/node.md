---
tag: 6TRC5Q
kind: algorithm
slug: uniform-price-auction
name: Uniform price auction
aliases:
- multi-unit uniform price auction
area: algorithmic-game-theory/auctions
level: core
summary: "Sells k identical units to the k highest marginal bids at one price, the highest losing bid or the lowest winning bid. Truthful for unit demand; bidders who want several units shade their bids."
model: word-ram
complexity:
  vars: {n: the number of bidders, d: the total number of marginal bids, k: the number of units}
  time: {worst: O(d log d)}
  space: {extra: O(d)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1960
  people: [Milton Friedman, Robert Wilson, Lawrence Ausubel, Peter Cramton]
  note: Friedman argued around 1960 that the US Treasury should sell its securities at one price. Wilson (1979) showed that share auctions at one price can have equilibria with very low prices, and Ausubel, Cramton, Pycia, Rostek and Weretka (2014) studied demand reduction in detail.
prereqs: [vickrey-auction, quasilinear-utility, dominant-strategy-incentive-compatibility]
see_also: [vcg-mechanism, simultaneous-ascending-auction, english-auction, myerson-lemma, double-auction, combinatorial-auction, nash-equilibrium, selection-problem]
sources:
  - paper: doi:10.1093/restud/rdu023
    title: "Lawrence M. Ausubel, Peter Cramton, Marek Pycia, Marzena Rostek and Marek Weretka, Demand reduction and inefficiency in multi-unit auctions, Review of Economic Studies 81(4) (2014), 1366-1400"
    locator: demand reduction in the uniform price auction, the inefficiency it causes, and the comparison with the pay-as-bid auction
  - paper: "Robert Wilson, Auctions of shares, Quarterly Journal of Economics 93(4) (1979), 675-689"
    locator: equilibria of the auction of a divisible good at one price, with prices far below the values
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: the chapters on multiple-unit auctions (the uniform price, discriminatory and Vickrey auctions of identical units, and demand reduction)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 9 (budget constraints and the uniform-price multi-unit auction)
---

The uniform price auction sells $k$ identical units of one good. Each bidder reports a list of *marginal bids*, one for each extra unit it wants, and the auction accepts the $k$ highest marginal bids. Every unit sold costs the same price: the highest losing bid in one version, the lowest winning bid in the other. With the highest losing bid and bidders who want one unit each, it is the $(k + 1)$-th price auction, which is [DSIC](/dominant-strategy-incentive-compatibility/) and a case of the [VCG mechanism](/vcg-mechanism/). When a bidder wants several units, its own losing bid can set the price of its winning units, so it gains by bidding less for its later units. This *demand reduction* makes the auction inefficient in equilibrium. Governments use the format for bonds and for some electricity and emission permit markets.

## In plain words

A seller has many copies of the same thing. Each buyer says how much it would pay for a first copy, for a second copy, and so on. The seller gives the copies to the highest offers, and then everyone pays the same price per copy, set by the offers that just missed or just made it. If every buyer wants only one copy, honest offers are best, exactly as in a sealed second-price auction. A buyer that wants many copies has a reason to lie. Its offer for the last copy can become the price that it pays on all its other copies. By asking for fewer copies, it can make the price fall a lot and gain more than it gives up. This is why such auctions can sell to the wrong buyers.

## The problem

There are $k$ identical units and $n$ bidders with [quasilinear utility](/quasilinear-utility/). Bidder $i$ has marginal values $v_{i,1} \ge v_{i,2} \ge \cdots$: it values $x$ units at $v_{i,1} + \cdots + v_{i,x}$. It reports marginal bids $b_{i,1} \ge b_{i,2} \ge \cdots \ge 0$, in total $d$ numbers. The auction must choose how many units $x_i$ each bidder gets, with $\sum_i x_i \le k$, and one price $p$ per unit, so that bidder $i$ pays $p\,x_i$. The aims are to give the units to the highest reported marginal bids, and to set a price at which no winning bid is below the price and no losing bid is above it.

## The algorithm

```pseudo id=main
UNIFORM-PRICE(b, k)
L1  E ← all triples (b_{i,j}, i, j) for every bidder i and unit j
L2  sort E by bid, highest first; ties go to the smaller i, then the smaller j
L3  q ← min(k, |E|)
L4  for each of the first q triples (·, i, ·): x_i ← x_i + 1
L5  if the rule is HIGHEST-LOSING: p ← the bid of triple k + 1, or 0 if |E| ≤ k
L6  else (LOWEST-WINNING): p ← the bid of triple q, or 0 if q = 0
L7  return x, p, and the payments p · x_i
```

The tie rule of line L2 puts a bidder's unit $j$ before its unit $j + 1$ when the bids are equal, so every bidder wins a prefix of its list. Sorting is the simplest way to write line L2; a [selection](/selection-problem/) of the $(k + 1)$-th largest bid does the same work in linear time.

## Example

**Unit demand.** Four bidders want one unit each and bid $7, 5, 3, 3$ for $k = 2$ units. The bids 7 and 5 win. Under the highest losing rule both winners pay 3, the best losing bid. Under the lowest winning rule both pay 5.

**Demand reduction.** Take $k = 2$, a bidder $A$ that values each of two units at 10, and a bidder $B$ that values one unit at 6. Use the highest losing rule.

| bids of $A$ | bid of $B$ | sorted triples | units of $A$, $B$ | price | utility of $A$ |
|---|---|---|---|---|---|
| $(10, 10)$ | $6$ | $10_A, 10_A, 6_B$ | $2, 0$ | 6 | $20 - 12 = 8$ |
| $(10, 0)$ | $6$ | $10_A, 6_B, 0_A$ | $1, 1$ | 0 | $10 - 0 = 10$ |

By giving up its second unit, $A$ makes its own bid 0 the highest losing bid, and the price falls from 6 to 0. The second profile is a Nash equilibrium. Its welfare is $10 + 6 = 16$, while the optimum gives both units to $A$ for 20.

## Correctness

The proof is in `proofs/correctness.md`. It shows these facts.

- **The allocation is the best for the reports.** Each bidder wins a prefix of its list, and the winning triples are the $q$ highest bids, so the allocation maximizes the sum of the accepted marginal bids.
- **The price clears the market.** Every winning bid is at least $p$ and every losing bid is at most $p$. So at the price $p$, each bidder's reported demand is the number of units it got, up to ties.
- **Unit demand is truthful.** If each bidder wants one unit, bidder $i$ wins when its bid is above the $k$-th highest other bid $\theta$ and loses when it is below, and a winner pays $\theta$ under the highest losing rule. This is the threshold form of [Myerson's lemma](/myerson-lemma/), and truthful bidding is a dominant strategy.
- **The lowest winning rule is not truthful**, even for unit demand: with one unit and bids 5 and 3, the winner pays its own bid and gains by bidding 4.
- **Multi-unit demand is not truthful** under either rule, by the demand reduction example.

## Complexity

Sorting $d$ triples takes $O(d \log d)$ time and $O(d)$ extra space, and lines L4 to L7 take $O(d + n)$ time. With a linear-time selection of the $k$-th and $(k + 1)$-th largest bids and a partition of the list around them, the time is $O(d + n)$. Ties at the boundary must still be broken by the rule of line L2.

## Properties

- **Clearing price.** Every winner pays the same price per unit, and the price lies between the best losing bid and the worst winning bid.
- **DSIC for unit demand** under the highest losing rule, with the same threshold argument as the [Vickrey auction](/vickrey-auction/).
- **Not DSIC for multi-unit demand.** A bidder's losing bids on later units can set the price of its winning units, so in equilibrium bidders shade their bids for later units (Ausubel, Cramton, Pycia, Rostek and Weretka 2014).
- **Inefficient in equilibrium** when bidders want several units, because demand reduction moves units from high to low marginal values.
- **Low-price equilibria.** In the model of a divisible good with bidders that submit demand curves, Wilson (1979) found equilibria in which the price is far below the values, because each bidder faces a steep supply from the others.

## Variants and improvements

- **Pay-as-bid (discriminatory) auction.** Each winner pays its own winning bids. Bidders then shade all their bids, not only the later ones. Neither format dominates the other in revenue or efficiency in general (Ausubel, Cramton, Pycia, Rostek and Weretka 2014).
- **Vickrey auction for identical units.** Each bidder pays, for its $x$-th unit, the $x$-th highest losing bid of the others. This is the [VCG mechanism](/vcg-mechanism/) for this setting and is DSIC for any nonincreasing marginal values, at the cost of different prices for the same good.
- **Ascending clock auction.** The price rises, and bidders report how many units they want at each price, until demand falls to $k$. With straightforward bidding it ends at the uniform price; Ausubel's clinching auction changes the payments so that sincere bidding becomes an equilibrium.
- **Reserve price.** The seller adds $k$ bids of its own at the reserve, which bounds the price from below.

## When to use it

Use it to sell many identical units when one public price matters, for example for government bonds, when buyers want a single price for fairness or for resale. With unit demand, use the highest losing rule, which is truthful. When large bidders want many units, expect demand reduction, and consider a clock auction with clinching or a Vickrey auction for identical units.

## Pitfalls

- **The price rule matters.** "Uniform price" can mean the highest losing bid or the lowest winning bid. Only the first is truthful for unit demand.
- **The bidder's own bids set the price.** With multi-unit demand the price can be a losing bid of a winner. Do not treat the auction as a $(k + 1)$-th price auction in that case.
- **Ties at the boundary.** When several bids equal the $k$-th bid, the tie rule decides who wins, but the price does not depend on who wins the tie.
- **Marginal bids must not increase.** A list with an increasing step does not describe a valuation with decreasing marginal values, and the prefix property of line L2 fails; the code rejects such a list.

## Implementations

## History

Milton Friedman argued around 1960 that the US Treasury should sell its securities at one price rather than at the bids, so that small bidders would not need to guess the market. Wilson (1979) modeled the sale of a divisible good to bidders who submit demand curves and found equilibria of the uniform price rule in which the price is far below the values. Theory and evidence on demand reduction followed in the 1990s and 2000s, and Ausubel, Cramton, Pycia, Rostek and Weretka (2014) compared the uniform price and pay-as-bid formats, showing that demand reduction makes both inefficient and that their ranking in revenue and efficiency depends on the setting.

## References
