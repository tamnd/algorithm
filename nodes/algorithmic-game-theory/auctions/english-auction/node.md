---
tag: 6F235Y
kind: algorithm
slug: english-auction
name: English auction
aliases:
- ascending price auction
- open outcry auction
- ascending clock auction
area: algorithmic-game-theory/auctions
level: intro
summary: The price rises step by step while bidders drop out, and the last bidder left wins at the current price. With private values, staying in until the price reaches one's value is dominant.
model: word-ram
complexity:
  vars: {n: the number of bidders, k: the number of clock steps}
  time: {worst: O(n k)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1961
  people: [William Vickrey, Paul Milgrom, Robert J. Weber]
  note: Open ascending auctions are very old. Vickrey showed in 1961 that with private values the English auction has the same outcome as the second-price sealed-bid auction, and Milgrom and Weber in 1982 studied the clock form with interdependent values.
prereqs: [quasilinear-utility, dominant-strategy, vickrey-auction]
see_also: [vickrey-auction, dutch-auction, linkage-principle, common-value-auction, simultaneous-ascending-auction, demange-gale-sotomayor-auction, kelso-crawford-process, market-based-task-allocation]
sources:
  - paper: doi:10.1111/j.1540-6261.1961.tb02789.x
    title: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    locator: the equivalence of the English auction and the second-price sealed-bid auction with private values
  - paper: doi:10.2307/1911865
    title: "Paul R. Milgrom and Robert J. Weber, A theory of auctions and competitive bidding, Econometrica 50(5) (1982), 1089-1122"
    locator: the English auction as a clock auction in which bidders press a button while they stay in and see who leaves, its symmetric equilibrium with affiliated signals, and the result that it earns at least as much as the second-price auction
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 1 (the common auction forms) and Chapter 6, Section 6.3 (English auctions with interdependent values) and Section 6.5.1 (English versus second-price auctions)
  - paper: doi:10.1257/aer.20160425
    title: "Shengwu Li, Obviously strategy-proof mechanisms, American Economic Review 107(11) (2017), 3257-3287"
    locator: the ascending clock auction is obviously strategy-proof and the second-price sealed-bid auction is not, with laboratory evidence that subjects play the dominant strategy more often in the clock form
  - paper: doi:10.1257/00028280260344632
    title: "Alvin E. Roth and Axel Ockenfels, Last-minute bidding and the rules for ending second-price auctions, evidence from eBay and Amazon auctions on the Internet, American Economic Review 92(4) (2002), 1093-1103"
    locator: proxy bidding in online auctions, which turns the open auction into a second-price rule, and late bidding under a fixed end time
  - paper: doi:10.1257/0002828043052330
    title: "Lawrence M. Ausubel, An efficient ascending-bid auction for multiple objects, American Economic Review 94(5) (2004), 1452-1475"
    locator: the clinching auction, an ascending clock auction for many identical units that gives the Vickrey outcome
---

The English auction sells one item by a price that rises in public. The bidders who still want the item at the current price stay in, the others drop out, and the last bidder left wins at the price where the second-to-last one dropped out. With private values, a bidder's best plan is to stay in until the price reaches its value, so the English auction has the same outcome as the [Vickrey auction](/vickrey-auction/), the sealed-bid auction in which the winner pays the second-highest bid. It is the mirror of the [Dutch auction](/dutch-auction/), whose price falls. With interdependent values the two ascending and sealed forms differ, because the drop-out prices reveal information ([linkage principle](/linkage-principle/)).

## In plain words

An auctioneer calls a low price and raises it a little at a time. Everyone who still wants the item at the called price keeps a hand up. When a hand goes down, it stays down. When only one hand is left, that person buys the item at the last price called. Your best plan is simple: keep your hand up while the price is below what the item is worth to you, and drop it when the price passes that worth. Dropping early can lose you a good deal, and staying longer can make you pay too much. The winner pays about what the second most eager person was willing to pay, as in the sealed second-price auction.

## The problem

One item is for sale to $n$ bidders with private values $v_i$ and [quasilinear utility](/quasilinear-utility/). The seller runs a clock: the price starts at a reserve $p_0$ and rises by a fixed increment $\delta > 0$. At each price every active bidder says whether it stays in, and a bidder who leaves cannot return. The auction must stop with one winner and a price, or with no sale if no bidder accepts $p_0$. In the model on this page, each bidder $i$ acts by a *threshold* $d_i$, the highest price it accepts. The truthful threshold is $d_i = v_i$. A bidder may also use any strategy that depends on what it has seen, and the analysis covers that too.

## The algorithm

$A$ is the set of active bidders and $p$ is the clock price.

```pseudo id=main
CLOCK(d_1, ..., d_n, δ, p_0)
L1  A ← {i : d_i ≥ p_0}; p ← p_0
L2  if A is empty: return NIL, 0                  ▷ no sale
L3  while |A| ≥ 2:
L4      A' ← {i in A : d_i ≥ p + δ}               ▷ who accepts the next price
L5      if A' is empty: return min A, p          ▷ all left at once: the tie rule
L6      A ← A'; p ← p + δ
L7  return the bidder in A, p
```

Line L5 handles the case where all remaining bidders leave at the same step. The item then goes to the smallest index among them, at the last price they all accepted. Real auctions handle this case by the order in which the bids were called.

Let $d_{(1)} \ge d_{(2)}$ be the two largest thresholds, and let $g$ be the largest clock price $p_0 + k\delta$ that is at most $d_{(2)}$. The clock stops at $g$ or at $g + \delta$: at $g + \delta$ if the top bidder accepts it, and at $g$ with the tie rule otherwise. So the price is within $\delta$ of $d_{(2)}$, which is the Vickrey price.

## Example

Three bidders with values $(10, 7, 3)$ use the truthful thresholds, with $\delta = 1$ and $p_0 = 0$.

| clock $p$ | next price | who accepts it | active after the step |
|---|---|---|---|
| 0 | 1 | 1, 2, 3 | {1, 2, 3} |
| 3 | 4 | 1, 2 | {1, 2} |
| 7 | 8 | 1 | {1} |

Bidder 1 wins at 8, one increment above the Vickrey price 7. With $\delta = 1/2$ the price is $7.5$. With values $(7, 7, 3)$, bidders 1 and 2 both leave after 7, and the tie rule gives the item to bidder 1 at 7.

Other strategies do not help bidder 2, of value 7. With threshold 9 it stays to 9, and bidder 1 wins at 10: bidder 2 only raised the price for bidder 1. With threshold 11 it wins at 11 and has utility $7 - 11 = -4$.

The increment can help a bidder who leaves early. With values $(10, 9.5)$ and $\delta = 1$, truthful bidding gives bidder 1 the item at 10, with utility 0. If bidder 1 leaves after 9, both bidders leave at the same step, bidder 1 wins the tie at 9, and its utility is 1. The gain is exactly one increment, the most that a deviation can gain.

## Correctness

The proof is in `proofs/correctness.md`. It shows three facts.

- **The outcome.** With $A_k$ the set of bidders whose threshold is at least $p_0 + k\delta$, the loop keeps $A = A_k$ at step $k$. It stops at the last step $a$ with $|A_a| \ge 2$, with the price $g = p_0 + a\delta$ or $g + \delta$ as described above.
- **Price and efficiency.** With truthful thresholds, the price is within $\delta$ of the second-highest value and at most the winner's value, and the winner's value is more than the highest value minus $\delta$.
- **Truthful dropping is dominant up to one increment.** Fix any strategies of the others, which may depend on the price and on who has left. Up to the moment bidder $i$ leaves, the run does not depend on $i$'s plan, so $i$ chooses only the price at which it leaves. There are three outcomes: lose, win a tie at the last price $g$ at which another bidder is active, or win alone at $g + \delta$. The truthful threshold picks the best of these up to a loss of at most $\delta$, and it never gives a negative utility.

As $\delta \to 0$ the price tends to the second-highest value and the gain from any deviation tends to 0, which is the [Vickrey auction](/vickrey-auction/) with its exact dominance.

## Complexity

The loop runs $k \le \lfloor (d_{(2)} - p_0)/\delta \rfloor + 1$ times, and each pass scans the active set, so the time is $O(nk)$ and the extra space is $O(n)$. The number of steps $k$ depends on the values and the increment, not only on $n$: halving $\delta$ doubles the number of steps. In a real auction a step is a round of communication, so $k$ is the measure that matters. A computer simulation can jump the clock: sort the thresholds, or find the two largest in $O(n)$, and compute the stopping price from the closed form above.

## Properties

- **Dominance with private values.** Staying in up to one's value is weakly dominant in the continuous clock, and dominant up to $\delta$ with an increment. This needs no prior, and it holds against any strategies of the others.
- **Obviously strategy-proof.** At every point where the bidder must act, the worst outcome of staying in (when the price is below its value) is at least as good as the best outcome of leaving. A bidder does not need to reason about the others to see this. The sealed second-price auction lacks this property, and in experiments bidders play the dominant strategy more often in the clock form (Li 2017).
- **Efficient up to $\delta$.** The winner's value is within $\delta$ of the highest value.
- **Privacy of the winner.** The auction stops near the second-highest value, so the winner never reveals its own value.
- **Revenue.** In the [independent private values](/independent-private-values/) model the expected revenue is that of the Vickrey auction, up to $\delta$. With affiliated values the English auction earns at least as much as the second-price auction, because the prices at which the others leave tell the remaining bidders about the value ([linkage principle](/linkage-principle/)).

## Variants and improvements

- **Open outcry.** Bidders call out their own bids, and each new bid must beat the last one by a minimum increment. Bidders can jump bid, raising the price by more than the increment to signal strength. With private values the outcome is still close to the second-highest value.
- **Japanese button auction.** The clock form above, with all bidders' exits visible. This is the model of Milgrom and Weber (1982) and of most theory.
- **Proxy bidding.** Online auctions ask each bidder for a maximum, and a program raises its bid by one increment when it is outbid. The result is a second-price rule with an increment. With a fixed end time, bidders often bid only in the last seconds (Roth and Ockenfels 2002).
- **Many items.** The [simultaneous ascending auction](/simultaneous-ascending-auction/) runs one clock per item at the same time, and it is used for spectrum licenses. The [Demange-Gale-Sotomayor auction](/demange-gale-sotomayor-auction/) and the [Kelso-Crawford process](/kelso-crawford-process/) raise prices on over-demanded items and reach a Walrasian equilibrium. The clinching auction of Ausubel (2004) sells many identical units by one clock and gives the Vickrey outcome.
- **Task allocation.** Robot teams use auctions of the same shape to assign tasks, with costs in place of values ([market-based task allocation](/market-based-task-allocation/)).

## When to use it

Use the English auction when the bidders should see clearly that honest bidding is safe, when the item's value depends on information that other bidders have, or when the seller wants a transparent price that all bidders observe. Art and antiques houses, livestock markets and spectrum sales use ascending forms. It is a poor choice when the bidders cannot meet at one time, when the number of steps is too costly, or when the bidders can use the open bids to collude or to punish a rival.

## Pitfalls

- **The increment is a source of error.** The price is the second value plus up to one increment, and a bidder can gain up to one increment by an early exit that wins a tie. Choose $\delta$ small compared with the spread of values.
- **Ties at the end.** If all remaining bidders leave at the same step, the rule must say who wins and at which price. Line L5 sells at the last accepted price to the smallest index. A rule that sells at the next price can charge a bidder more than its threshold.
- **Collusion is easier in public.** Bidders see each other's exits, so a ring can detect and punish a bidder who breaks an agreement.
- **Equivalence with the Vickrey auction needs private values.** With common values, a bidder learns from the exits of the others, and its best exit price depends on that history. Then the English and second-price auctions differ in equilibrium and in revenue.
- **Reserve.** Without a reserve, a single bidder wins at the start price. The start price $p_0$ acts as the seller's reserve.

## Implementations

## History

Ascending auctions are very old. The Romans sold goods by open ascending bids, and the London auction houses founded in the eighteenth century use the same form. Vickrey (1961) was the first to analyse it as a game and showed that with private values it has the same outcome as his second-price sealed-bid auction. Milgrom and Weber (1982) wrote the clock form, in which each bidder presses a button while it stays in and all exits are seen, and proved that with affiliated values the English auction earns at least as much as the second-price auction. Ascending clock auctions for many items became the standard design for spectrum sales from 1994 on.

## References
