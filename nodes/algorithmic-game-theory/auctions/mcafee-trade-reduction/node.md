---
tag: AMA27A
kind: algorithm
slug: mcafee-trade-reduction
name: "McAfee's trade reduction mechanism"
aliases:
- McAfee double auction
area: algorithmic-game-theory/auctions
level: advanced
summary: "A double auction for one good that drops the least valuable efficient trade when needed, so that it is truthful, individually rational and never runs a deficit."
model: word-ram
complexity:
  vars: {n: the number of buyers and sellers}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1992
  people: [R. Preston McAfee]
  note: McAfee (1992) gave the first double auction in which truthful reporting is a dominant strategy for both sides, at the cost of at most one trade, escaping the Myerson-Satterthwaite impossibility.
prereqs: [double-auction, dominant-strategy-incentive-compatibility, individual-rationality, budget-balance]
see_also: [myerson-satterthwaite-theorem, myerson-lemma, vickrey-auction, vcg-mechanism, uniform-price-auction, single-parameter-environment]
sources:
  - paper: "R. Preston McAfee, A dominant strategy double auction, Journal of Economic Theory 56(2) (1992), 434-450"
    locator: the mechanism with the price (b(k+1) + s(k+1))/2 and the reduction to k - 1 trades, the proof that truthful reporting is dominant, and the bound on the lost gains from trade
  - paper: "Roger B. Myerson and Mark A. Satterthwaite, Efficient mechanisms for bilateral trading, Journal of Economic Theory 29(2) (1983), 265-281"
    locator: the impossibility of an efficient, incentive compatible, individually rational and budget balanced mechanism for bilateral trade
---

McAfee's trade reduction mechanism is a double auction for one kind of good. Each buyer wants one unit and each seller has one unit. The mechanism finds the $k$ trades that an efficient market would make, and then either lets all $k$ pairs trade at one price taken from the first pair that does not trade, or, when that price does not fit, drops the $k$-th pair and charges the others prices set by that dropped pair. Truthful reporting is a dominant strategy for every buyer and every seller, nobody trades at a loss, and the auctioneer never adds money. The cost is at most one trade, the least valuable one, so the mechanism gets at least a $1 - 1/k$ fraction of the possible gains from trade. The [Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/) says that no mechanism can have all of these properties and also be fully efficient.

## In plain words

Buyers say the most they would pay, and sellers say the least they would accept. Line the buyers up from the highest offer down and the sellers from the lowest ask up, and pair them until a buyer offers less than its seller asks. Those pairs could all trade. Now look at the first pair that cannot trade, and take the midpoint of their two numbers as a price. If every paired trader is happy at that price, they all trade at it. If not, the last pair is sent home, and the other buyers pay the offer of the sent-home buyer while the other sellers get the ask of the sent-home seller. Nobody can change their own price by lying, so the truth is the best report.

## The problem

There are buyers with values $v_1, v_2, \ldots$ for one unit, and sellers with costs $c_1, c_2, \ldots$ for their unit, $n$ traders in all. Every trader has [quasilinear utility](/quasilinear-utility/): a buyer that trades at price $p$ gets $v - p$, a seller that trades at price $p$ gets $p - c$, and a trader that does not trade gets 0. The traders report bids and asks, and the mechanism chooses which buyers and sellers trade and their prices. The aims are: truthful reporting is a dominant strategy ([DSIC](/dominant-strategy-incentive-compatibility/)), no truthful trader loses ([individual rationality](/individual-rationality/)), the buyers pay at least what the sellers receive ([weak budget balance](/budget-balance/)), and the gains from trade, the sum of $v - c$ over the trading pairs, are close to the maximum.

## The algorithm

```pseudo id=main
MCAFEE(b_1, ..., b_B, s_1, ..., s_S)
L1  rank buyers b_(1) ≥ b_(2) ≥ ... and sellers s_(1) ≤ s_(2) ≤ ...; ties go to the smaller index
L2  k ← the largest t with b_(t) ≥ s_(t), or 0 if there is none
L3  if k = 0: return no trade
L4  if buyer k + 1 and seller k + 1 exist: p0 ← (b_(k+1) + s_(k+1)) / 2
L5      if s_(k) ≤ p0 ≤ b_(k):
L6          return buyers and sellers of ranks 1..k, all trading at the price p0
L7  return buyers and sellers of ranks 1..k-1; each buyer pays b_(k), each seller receives s_(k)
```

The bids do not increase and the asks do not decrease along the ranks, so the pairs with $b_{(t)} \ge s_{(t)}$ are exactly the first $k$. In line L7 the auctioneer keeps $(k - 1)(b_{(k)} - s_{(k)}) \ge 0$.

## Example

**All efficient trades happen.** Buyers bid $10, 8, 2$ and sellers ask $1, 3, 9$. The pairs are $(10, 1)$, $(8, 3)$ and $(2, 9)$, so $k = 2$. The price is $p_0 = (2 + 9)/2 = 5.5$, which lies in $[s_{(2)}, b_{(2)}] = [3, 8]$. Both pairs trade at 5.5. The buyers get $4.5$ and $2.5$, and the sellers get $4.5$ and $2.5$. The gains from trade are $9 + 5 = 14$, the maximum.

**One trade is dropped.** Buyers bid $10, 5, 4$ and sellers ask $1, 3, 9$. Again $k = 2$, but $p_0 = (4 + 9)/2 = 6.5$ is above $b_{(2)} = 5$. Line L7 runs: the buyer with 10 pays 5 and the seller with 1 receives 3, and the auctioneer keeps 2. The gains from trade are 9, against the maximum $9 + 2 = 11$. The lost trade is worth 2, the smaller of the two.

## Correctness

The proof is in `proofs/correctness.md`. It shows these facts.

- **Efficient trades.** With truthful reports, the largest possible gains from trade are $\sum_{t \le k} (b_{(t)} - s_{(t)})$, made by the first $k$ pairs.
- **Budget balance and the loss.** The buyer price is at least the seller price. Line L6 makes all $k$ trades, and line L7 drops only the pair with the smallest gain, so the gains are at least $(1 - 1/k)$ of the maximum.
- **A threshold for each trader.** Fix the reports of everyone except one buyer. There is a number $\theta$, which depends only on the others, such that the buyer trades when its bid is above $\theta$, does not trade when its bid is below $\theta$, and pays exactly $\theta$ when it trades. The proof finds $\theta$ by a case analysis on the number $h$ of efficient trades without this buyer. The value is the midpoint price of the first pair that does not trade, or the bid of the last trading buyer, depending on the case. Sellers are symmetric.
- **Truthful and individually rational.** A threshold with a payment equal to it is the condition of [Myerson's lemma](/myerson-lemma/) for this [single-parameter](/single-parameter-environment/) setting, so the truth is a dominant strategy and a truthful trader never loses.

## Complexity

Ranking the two sides takes $O(n \log n)$ time and $O(n)$ space, and lines L2 to L7 take $O(n)$ time. With bids that arrive already sorted, the whole mechanism takes $O(n)$ time.

## Properties

- **DSIC** for buyers and sellers.
- **Ex post individually rational.** Every trading buyer pays at most its bid and every trading seller receives at least its ask.
- **Weakly budget balanced.** In line L6 the budget balances exactly; in line L7 the auctioneer keeps a surplus.
- **Loses at most one trade.** The gains are at least the maximum minus $b_{(k)} - s_{(k)}$, which is at least $(1 - 1/k)$ of the maximum. As markets grow, the share of lost gains tends to 0.
- **Deterministic and prior-free.** It needs no distribution of values.

## Variants and improvements

- **Plain trade reduction.** Always use line L7. It keeps the same properties and is simpler, but it drops a trade even when the midpoint price would work.
- **Vickrey double auction.** All $k$ efficient pairs trade; each buyer pays $\max(s_{(k)}, b_{(k+1)})$ and each seller receives $\min(b_{(k)}, s_{(k+1)})$. This is the [VCG mechanism](/vcg-mechanism/) for the double auction. It is efficient and DSIC, but the sellers receive more than the buyers pay, so the auctioneer must cover a deficit.
- **Strong budget balance.** Later mechanisms keep truthfulness and lose few trades while sending all money from buyers to sellers, with no surplus for the auctioneer, for example by letting a randomly chosen trader set the price.
- **Bayesian mechanisms.** If the auctioneer knows the distributions, the mechanism can be tuned for expected gains, but by the [Myerson-Satterthwaite theorem](/myerson-satterthwaite-theorem/) some loss remains.

## When to use it

Use it for a market of one good with many buyers and sellers who each trade one unit, when the market maker must not lose money and when the traders should not need to guess the others' reports. It suits markets with many traders, where losing one trade costs little. In a market with one buyer and one seller it never trades, so use a posted price or a bargaining rule there.

## Pitfalls

- **Small markets.** With $k = 1$ and no pair at rank 2, line L7 drops the only trade. The guarantee $1 - 1/k$ is 0 for $k = 1$.
- **Missing traders at rank $k + 1$.** If there is no buyer or no seller of rank $k + 1$, the price $p_0$ does not exist and line L7 runs. Some write-ups add a dummy trader with a bound on the values instead; this changes the outcome, so state the rule.
- **Unit demand and unit supply.** The proof uses one unit per trader. With multi-unit traders, a trader's own bids can set its price, as in the [uniform price auction](/uniform-price-auction/), and the mechanism is no longer truthful.
- **Exact arithmetic.** The price $p_0$ is a midpoint, and the test of line L5 compares it with the bids. Use exact fractions so that the boundary cases do not change the outcome.

## Implementations

## History

Myerson and Satterthwaite (1983) proved that even with one buyer and one seller, no mechanism is efficient, Bayesian incentive compatible, individually rational and budget balanced when the supports of the values overlap. McAfee (1992) showed that in a large market this obstacle costs little. He gave a double auction that is dominant-strategy truthful for both sides, individually rational and weakly budget balanced, and that loses at most the least valuable efficient trade.

## References
