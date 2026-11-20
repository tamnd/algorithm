---
tag: 3GCYFC
kind: algorithm
slug: vickrey-auction
name: Vickrey auction
aliases:
- second-price sealed-bid auction
- second-price auction
area: algorithmic-game-theory/auctions
level: intro
summary: Each bidder submits one sealed bid. The highest bidder wins and pays the second highest bid, so bidding one's true value is a weakly dominant strategy.
model: word-ram
complexity:
  vars: {n: the number of bidders}
  time: {worst: O(n)}
  space: {extra: O(1)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1961
  people: [William Vickrey]
  note: Vickrey defined the second-price sealed-bid auction in 1961, showed that truthful bidding is dominant, and found that it earns the same expected revenue as the first-price auction in his symmetric examples.
prereqs: [quasilinear-utility, dominant-strategy, direct-revelation-mechanism, dominant-strategy-incentive-compatibility, individual-rationality]
see_also: [english-auction, first-price-auction, vcg-mechanism, revenue-equivalence-theorem, reserve-price, myerson-optimal-auction, bulow-klemperer-theorem, generalized-second-price-auction]
sources:
  - paper: doi:10.1111/j.1540-6261.1961.tb02789.x
    title: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    locator: the second-price sealed-bid auction, the proof that bidding the true value is dominant, and its relation to the English auction
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 2, Section 2.2 (second-price auctions, the weakly dominant strategy and the expected payment) and the section on reserve prices in the same chapter
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 2, Section 2.4 (second-price auctions and dominant strategies)
  - paper: doi:10.1257/jep.14.3.183
    title: "David Lucking-Reiley, Vickrey auctions in practice, from nineteenth-century philately to twenty-first-century e-commerce, Journal of Economic Perspectives 14(3) (2000), 183-192"
    locator: the use of second-price rules in stamp auctions by mail before 1961 and the proxy bidding of online auctions
  - paper: doi:10.1086/261670
    title: "Michael H. Rothkopf, Thomas J. Teisberg and Edward P. Kahn, Why are Vickrey auctions rare?, Journal of Political Economy 98(1) (1990), 94-109"
    locator: the reasons why real auctioneers avoid the sealed second-price rule, with the fear that bids reveal values to later negotiations and a cheating auctioneer
---

The Vickrey auction, also called the second-price sealed-bid auction, sells one item. Each bidder submits one sealed bid, the highest bid wins, and the winner pays the highest of the other bids, not its own. Because the price does not depend on the winner's own bid, bidding the true value is a weakly [dominant strategy](/dominant-strategy/), so the auction is [DSIC](/dominant-strategy-incentive-compatibility/) and gives the item to the bidder who values it most. With private values it has the same outcome as the [English auction](/english-auction/), in which the price rises until one bidder is left, and it is the one-item case of the [VCG mechanism](/vcg-mechanism/).

## In plain words

Everyone writes a price in an envelope. The person with the highest price gets the item, but pays only the second highest price written by someone else. This rule takes away the reason to lie. If you write less than the item is worth to you, you do not lower what you pay when you win, you only risk losing an item you wanted at a good price. If you write more, you only add the risk of winning at a price above your worth. So the best thing to write is exactly what the item is worth to you, whatever the others write.

## The problem

One item is for sale to $n$ bidders. Bidder $i$ has a private value $v_i \ge 0$ and [quasilinear utility](/quasilinear-utility/): $v_i - p$ if it wins and pays $p$, and $0$ if it loses. The seller sets a reserve $r \ge 0$, the lowest price at which it sells. The auction is a [direct revelation mechanism](/direct-revelation-mechanism/): it receives bids $b_1, \ldots, b_n$ and must choose a winner (or no sale) and a price. The goal is a rule under which truthful bidding is dominant, the item goes to the highest value at least $r$, and losers pay nothing.

## The algorithm

A bid is *eligible* if it is at least $r$. The variable $s$ holds the highest bid seen so far other than that of the current leader $w$, and never less than $r$.

```pseudo id=main
VICKREY(b_1, ..., b_n, r)
L1  w ← NIL; s ← r
L2  for i ← 1 to n:
L3      if b_i ≥ r and (w = NIL or b_i > b_w):        ▷ i is the new leader
L4          if w ≠ NIL: s ← b_w                       ▷ the old leader's bid is now the best other bid
L5          w ← i
L6      else: s ← max(s, b_i)
L7  if w = NIL: return NIL, 0                         ▷ no bid reaches the reserve
L8  return w, s                                       ▷ w wins and pays s; all others pay 0
```

The winner $w$ is the smallest index among the highest eligible bids, because line L3 replaces the leader only on a strictly larger bid. The price is $s = \max(r, \max_{j \ne w} b_j)$. This is the *critical bid* of the winner: the smallest bid with which it would still win against the same $b_{-w}$.

## Example

Three bidders bid their values $(10, 7, 3)$ and $r = 0$.

| step | $b_i$ | leader $w$ | $s$ |
|---|---|---|---|
| start | | NIL | 0 |
| $i = 1$ | 10 | 1 | 0 |
| $i = 2$ | 7 | 1 | 7 |
| $i = 3$ | 3 | 1 | 7 |

Bidder 1 wins and pays 7, so its utility is $10 - 7 = 3$. With $r = 8$ bidder 1 pays 8. With $r = 12$ the item is not sold. With bids $(7, 7, 3)$ the tie goes to bidder 1, which pays 7.

Lies do not help. If bidder 1 bids 6 instead of 10, it loses and gets 0 instead of 3. If it bids 20, it still pays 7. If bidder 2 bids 11 instead of 7, it wins, pays 10, and gets $7 - 10 = -3$.

With $n$ values drawn independently and uniformly from $[0, 1]$ ([independent private values](/independent-private-values/)), the price is the second-highest value, whose expected value is $(n-1)/(n+1)$: $1/3$ for two bidders and $1/2$ for three. With two bidders and the reserve $r = 1/2$, the expected revenue rises to $5/12$, the most that any auction can earn here ([Myerson's optimal auction](/myerson-optimal-auction/)). The tests check these numbers by simulation.

## Correctness

The proof is in `proofs/correctness.md`. It shows three facts.

- **The output.** The loop keeps the invariant that $w$ is the first highest eligible bid among the bids seen and $s$ is the largest of $r$ and the other bids seen. So line L8 returns the first highest eligible bidder and the price $\max(r, \max_{j \ne w} b_j)$.
- **Truthful bidding is weakly dominant.** Fix the bids $b_{-i}$ of the others and let $m_i = \max(r, \max_{j \ne i} b_j)$, which bidder $i$ cannot change. A bid above $m_i$ wins and pays $m_i$, and a bid below $m_i$ loses. So the truthful bid gets $\max(0, v_i - m_i)$, the best of the two outcomes. A bid that changes the outcome either gives up a gain $v_i - m_i > 0$ or buys a loss $v_i - m_i < 0$.
- **Individual rationality and efficiency.** A truthful bidder never gets a negative utility ([individual rationality](/individual-rationality/)), and with truthful bids the item goes to a highest value that is at least $r$.

The dominance holds for every $b_{-i}$, with no prior on the values and no assumption that the others are truthful.

## Complexity

One pass over the bids, with at most two comparisons in line L3 and one in line L6 per bid, so the time is $\Theta(n)$ and the extra space is $O(1)$. This is optimal up to the constant, since each bid must be read. The fewest comparisons that find the largest and the second-largest of $n$ numbers is $n + \lceil \log_2 n \rceil - 2$, with a knockout tournament ([selection problem](/selection-problem/)). The implementation uses exact comparisons, so it works with integers, fractions or floats.

## Properties

- **DSIC.** Truthful bidding is a weakly dominant strategy for every bidder.
- **Efficient.** With truthful bids and $r = 0$, the item goes to the highest value.
- **Ex post individually rational and no positive transfers.** A truthful bidder has utility at least 0, and no bidder is ever paid.
- **Prior-free.** The rule and the bidders' strategies need no distribution of values.
- **Revenue.** In the symmetric [independent private values](/independent-private-values/) model, the expected revenue is the expected second-highest value. By the [revenue equivalence theorem](/revenue-equivalence-theorem/) it equals the revenue of the first-price, Dutch, English and all-pay auctions.
- **Not strictly dominant.** For a fixed $b_{-i}$ many bids are as good as the truth, for example any bid above $m_i$ when $v_i > m_i$. Dominance is weak.

## Variants and improvements

- **Reserve price.** The parameter $r$ above. With $n$ symmetric bidders whose values have a regular distribution, the Vickrey auction with the reserve $\phi^{-1}(0)$, where $\phi$ is the [virtual valuation](/virtual-valuation/), is optimal for revenue ([reserve price](/reserve-price/)). For asymmetric bidders the optimal auction is no longer a Vickrey auction with one reserve.
- **$k$ identical items.** The $k$ highest bids win and each pays the $(k+1)$-th highest bid. This is the VCG mechanism for $k$ units and unit demand, and it is DSIC.
- **VCG.** For many items and general valuations, the [VCG mechanism](/vcg-mechanism/) charges each bidder the welfare loss it causes the others. The Vickrey auction is its one-item case.
- **English auction and proxy bidding.** The [English auction](/english-auction/) reaches the same outcome by an open, rising price. Online auctions use proxy bidding: the bidder states a maximum, and a program raises its bid by one increment at a time, which is close to a second-price rule.
- **Generalized second-price auction.** For ranked ad slots, each bidder pays the next bid below. This is not DSIC for more than one slot ([generalized second-price auction](/generalized-second-price-auction/)).

## When to use it

Use it when the goal is to give the item to the bidder who values it most and the bidders should not have to guess what the others will bid. It suits automated bidders, since the best strategy is simple and the same for every belief about the others. It is a poor choice when the seller cannot be trusted to report the second bid honestly, when bidders fear that their bid reveals their value to a later negotiation, or when the bidders can collude (Rothkopf, Teisberg and Kahn 1990). Many display advertising exchanges used second-price rules for years and moved to first-price rules around 2019.

## Pitfalls

- **Weak dominance does not exclude other equilibria.** With two bidders of values 10 and 3, the bids $(0, 100)$ form a Nash equilibrium: the low-value bidder wins and pays 0. The truthful equilibrium is the one in dominant strategies, but it is not the only one.
- **A cheating seller.** The seller sees the bids and can add a fake bid just below the winning bid (a shill bid). The winner then pays nearly its full value, and it cannot detect the change from the outcome alone.
- **Collusion.** If the second and third bidders agree that only one of them bids, the price drops. DSIC holds for each bidder alone, not for groups.
- **Ties.** A tie at the top must go to one bidder by a fixed rule, and the winner then pays its own bid. Tests of DSIC must compare utilities with $\ge$, not $>$, and must use exact arithmetic.
- **The reserve is a bid of the seller.** The price is $\max(r, \cdot)$, not the second bid alone. Forgetting $r$ in line L1 makes the winner pay less than the reserve.
- **Values must be private.** If a bidder's value depends on what the others know, as in a [common value auction](/common-value-auction/), the truthful bid is no longer dominant and the winner's curse appears.

## Implementations

## History

Vickrey (1961) studied auctions as games of incomplete information. He defined the sealed-bid auction in which the winner pays the second-highest bid, proved that bidding the true value is dominant, and noted that it gives the same result as the English auction with private values. He also computed, for uniform values, that the first-price auction earns the same expected revenue, which is an early case of [revenue equivalence](/revenue-equivalence-theorem/). Second-price rules were in use earlier: stamp dealers who ran auctions by mail in the nineteenth century charged the winner the second-highest mailed bid, plus one increment (Lucking-Reiley 2000). Vickrey received the Nobel Memorial Prize in Economic Sciences in 1996, together with James Mirrlees. Clarke (1971) and Groves (1973) extended the idea of charging the externality to general decisions, which led to the VCG mechanism.

## References
