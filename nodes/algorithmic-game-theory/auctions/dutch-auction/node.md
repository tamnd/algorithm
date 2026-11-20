---
tag: 6N55V9
kind: algorithm
slug: dutch-auction
name: Dutch auction
aliases:
- descending price auction
- descending clock auction
area: algorithmic-game-theory/auctions
level: intro
summary: The price starts high and falls step by step, and the first bidder to accept wins at the current price. It is strategically the same game as the first-price sealed-bid auction.
model: word-ram
complexity:
  vars: {n: the number of bidders, k: the number of clock steps}
  time: {worst: O(n k)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1961
  people: [William Vickrey]
  note: Descending clock auctions sell flowers and fish in the Netherlands and elsewhere. Vickrey noted in 1961 that the Dutch auction is strategically the same game as the first-price sealed-bid auction.
prereqs: [quasilinear-utility, first-price-auction]
see_also: [first-price-auction, first-price-auction-equilibrium, english-auction, vickrey-auction, revenue-equivalence-theorem, independent-private-values, uniform-price-auction, bayes-nash-equilibrium]
sources:
  - paper: doi:10.1111/j.1540-6261.1961.tb02789.x
    title: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    locator: the descending auction and its equivalence with the first-price sealed-bid auction
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 1 (the common auction forms and the strategic equivalence of the Dutch and first-price auctions) and Chapter 2, Section 2.3 (the first-price equilibrium, which is also the Dutch equilibrium)
  - paper: doi:10.2307/1911865
    title: "Paul R. Milgrom and Robert J. Weber, A theory of auctions and competitive bidding, Econometrica 50(5) (1982), 1089-1122"
    locator: the strategic equivalence of the Dutch and first-price auctions, which holds also with interdependent values
  - paper: doi:10.1257/aer.89.5.1063
    title: "David Lucking-Reiley, Using field experiments to test equivalence between auction formats, magic on the Internet, American Economic Review 89(5) (1999), 1063-1080"
    locator: a field test in which Dutch auctions of trading cards earned more than first-price sealed-bid auctions of the same cards
  - paper: "James C. Cox, Bruce Roberson and Vernon L. Smith, Theory and behavior of single object auctions, in Vernon L. Smith (ed.), Research in Experimental Economics, Volume 2, JAI Press, 1982, 1-43"
    locator: laboratory tests in which Dutch auctions earned less than first-price sealed-bid auctions
---

The Dutch auction sells one item by a price that falls in public. A clock starts at a high price and goes down step by step, and the first bidder who accepts the current price wins and pays it. Before the clock stops, a bidder learns nothing except that no one has accepted yet, so its plan is just a price at which to accept. That makes the Dutch auction strategically the same game as the [first-price auction](/first-price-auction/), where each bidder writes one sealed bid and the highest bid pays itself. It is the mirror of the [English auction](/english-auction/), whose price rises, and it has the same equilibrium as the first-price auction ([equilibrium of the symmetric first-price auction](/first-price-auction-equilibrium/)).

## In plain words

An auctioneer starts at a price that is too high for everyone and lowers it a little at a time. The first person who shouts "mine" buys the item at the price on the clock. If you wait, the price gets better for you, but someone else may shout first. So you must decide in advance the price at which you will shout, and nothing you see before that changes your mind, because all you see is that nobody has shouted. Choosing that price is the same problem as choosing a sealed bid in an auction where the highest bid wins and pays itself. So the two auctions give the same result.

## The problem

One item is for sale to $n$ bidders with private values $v_i$ and [quasilinear utility](/quasilinear-utility/). The clock starts at a price $T$ above every value that matters and falls by a fixed decrement $\delta > 0$. The seller does not sell below a reserve $r$. At each level the bidders may accept, and the auction stops at the first acceptance. In the model on this page, bidder $i$ acts by a *stop price* $s_i$: it accepts at the first level $p$ with $p \le s_i$. The goal is to run the clock and find the winner and the price.

## The algorithm

$p$ is the clock price, computed as $T - k\delta$ at step $k$.

```pseudo id=main
DUTCH(s_1, ..., s_n, T, δ, r)
L1  p ← T
L2  while p ≥ r:
L3      S ← {i : s_i ≥ p}                       ▷ the bidders who accept at this level
L4      if S is not empty: return min S, p     ▷ the first to accept wins and pays p
L5      p ← p - δ                              ▷ computed as T - kδ after k steps
L6  return NIL, 0                              ▷ the clock passed the reserve
```

If several bidders accept at the same level, line L4 gives the item to the smallest index. A real clock settles this by who pressed first. If a stop price is at least $T$, that bidder accepts at once.

The output is the outcome of the first-price auction on the stop prices rounded down to the clock levels. So the price is at most the highest stop price and more than the highest stop price minus $\delta$.

## Example

Three bidders have values $(9, 6, 3)$, drawn independently and uniformly from $[0, 12]$. In the symmetric equilibrium each bidder accepts at $\frac{n-1}{n} v = \frac{2}{3} v$, the first-price equilibrium bid, so the stop prices are $(6, 4, 2)$. The clock starts at $T = 12$ with $\delta = 1$.

| clock $p$ | 12 | 11 | 10 | 9 | 8 | 7 | 6 |
|---|---|---|---|---|---|---|---|
| bidders who accept | none | none | none | none | none | none | 1 |

Bidder 1 stops the clock at 6 and pays 6, with utility 3. With stop prices $(6.5, 4, 2)$ the result is the same, because the clock has no level between 7 and 6. With a reserve of 7, the clock stops at 7 with no acceptance, and the item is not sold. With stop prices $(6, 6, 2)$ both bidders accept at 6 and bidder 1 wins the tie.

## Correctness

The proof is in `proofs/correctness.md`. It shows two facts.

- **The outcome.** For a clock level $g$, $s_i \ge g$ holds exactly when the rounded stop price $\rho(s_i)$, the largest level at most $s_i$, is at least $g$. The clock goes down level by level and stops at the first level that some rounded stop price reaches, which is the largest rounded stop price. So DUTCH returns the first-price outcome on the rounded stop prices.
- **Strategic equivalence.** A bidder's information while the clock runs is only the current level and the fact that no one has accepted. A plan is therefore fixed by the first level at which it accepts, which is a stop price. So the strategies, the outcomes and the payoffs of the Dutch auction are those of the first-price auction on the clock levels, and the two have the same Bayes-Nash equilibria.

The equivalence holds for any values, private or interdependent, because it uses only what the bidders can see (Milgrom and Weber 1982). This is a stronger link than the one between the English and Vickrey auctions, which needs private values.

## Complexity

The clock visits at most $k = \lfloor (T - \max(p^*, r))/\delta \rfloor + 1$ levels, where $p^*$ is the highest rounded stop price, and each visit scans the $n$ stop prices. So the time is $O(nk)$ and the extra space is $O(n)$. As with the English auction, $k$ is the number of rounds and depends on $T$ and $\delta$. A simulation can find the result in $O(n)$ time by rounding the largest stop price. In practice the clock moves fast and a lot is sold in seconds, which is why the form is used for large numbers of perishable lots.

## Properties

- **Same as the first-price auction.** The Dutch auction with a fine clock has the outcome of the first-price auction on the same bids, so it has the same equilibria, the same expected revenue and the same efficiency. In the symmetric [independent private values](/independent-private-values/) model with uniform values, the expected revenue is $(n-1)/(n+1)$, up to the rounding of the clock.
- **Not DSIC.** A bidder who accepts at its value gains nothing. The best stop price depends on the others.
- **Revenue equivalence.** With symmetric, independent, risk-neutral bidders, the Dutch, first-price, English and Vickrey auctions earn the same expected revenue ([revenue equivalence theorem](/revenue-equivalence-theorem/)).
- **One message.** Only the winner sends a message, so the auction is fast and reveals only the winning price.
- **The clock lowers the price a little.** With decrement $\delta$, the winner pays the largest level at most its stop price, so the seller loses less than $\delta$ compared with the sealed first-price auction on the same bids.

## Variants and improvements

- **Many units.** For a lot of several units, the winner at a level chooses how many units to buy at that price, and the clock goes on for the rest. Flower auctions work this way.
- **Restart with a reserve.** If the clock passes the reserve without acceptance, the item is held back or offered again later.
- **Procurement.** A rising clock with costs in place of values: the price offered for a contract rises until one supplier accepts. This is the same game as a first-price procurement auction.
- **Continuous time.** With $\delta \to 0$ the Dutch auction is exactly the first-price auction.

## When to use it

Use the Dutch auction to sell many lots quickly, one after another, with bidders who are present at the same time, as in the flower, fish and produce markets of the Netherlands and other countries. It reveals only the winning price, needs one message per lot and ends as soon as a bidder accepts. It is a poor choice when the bidders are not all present at the same moment, or when the seller wants the bidders to learn from each other, as in an [English auction](/english-auction/) with common values.

## Pitfalls

- **Dutch is not English.** The English auction rises and has the outcome of the second-price auction with private values; the Dutch auction falls and has the outcome of the first-price auction. Their expected revenues are equal only under the conditions of revenue equivalence.
- **The name is used for another auction.** In finance, a "Dutch auction" of shares often means a [uniform-price auction](/uniform-price-auction/), in which all winners pay the same clearing price. That is a different mechanism with different incentives.
- **Behaviour differs from theory.** The strategic equivalence is a theorem, but people do not always bid the same way. Laboratory subjects earned the seller less in Dutch auctions than in sealed first-price auctions (Cox, Roberson and Smith 1982), while a field test with trading cards found the opposite (Lucking-Reiley 1999).
- **Rounding of the clock.** A test that compares the Dutch and first-price auctions must round the bids down to the clock levels, or use bids on the levels. With floats, compute the level as $T - k\delta$ and not by repeated subtraction.
- **Ties at a level.** Two bidders can accept at the same level. The rule must say who wins, and a real system needs a fair way to decide who pressed first.

## Implementations

## History

Descending clock auctions are used in the Netherlands for flowers, fruit and vegetables, and in many fish markets, and the name comes from the Dutch flower auctions. Vickrey (1961) noted that the Dutch auction and the first-price sealed-bid auction are strategically the same, and used this to analyse both at once. Milgrom and Weber (1982) showed that the equivalence holds with any values, while the equivalence of the English and second-price auctions needs private values. Experiments then tested whether real bidders treat the two forms the same, with mixed results.

## References
