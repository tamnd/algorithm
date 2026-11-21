---
tag: ATPJNQ
kind: algorithm
slug: generalized-second-price-auction
name: Generalized second-price auction
aliases:
- GSP auction
area: algorithmic-game-theory/auctions
level: core
summary: "Ranks ad bids, gives the s-th highest bidder slot s and charges it the next bid per click. Not truthful, but it has an envy-free equilibrium with the VCG outcome."
model: word-ram
complexity:
  vars: {n: the number of bidders, k: the number of slots}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 2002
  people: [Benjamin Edelman, Michael Ostrovsky, Michael Schwarz, Hal Varian]
  note: Google adopted the next-bid price for its ad auctions in 2002. Edelman, Ostrovsky and Schwarz (2007) and Varian (2007) showed that GSP is not truthful and studied its envy-free equilibria.
prereqs: [position-auction, vickrey-auction, nash-equilibrium]
see_also: [gsp-envy-free-equilibrium, vcg-mechanism, myerson-lemma, reserve-price, online-adwords-problem, price-of-anarchy, uniform-price-auction, pacing-equilibrium]
sources:
  - paper: doi:10.1257/aer.97.1.242
    title: "Benjamin Edelman, Michael Ostrovsky and Michael Schwarz, Internet advertising and the generalized second-price auction: selling billions of dollars worth of keywords, American Economic Review 97(1) (2007), 242-259"
    locator: Section II (the rules of GSP and the example in which truthful bidding is not dominant) and Remark 1 (for the same bids, GSP payments are at least the VCG payments)
  - paper: doi:10.1016/j.ijindorg.2006.10.002
    title: "Hal R. Varian, Position auctions, International Journal of Industrial Organization 25(6) (2007), 1163-1178"
    locator: the model of position auctions and the symmetric Nash equilibria of the next-bid price rule
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lectures 2 and 3 (sponsored search auctions and the GSP auction)
---

The generalized second-price auction (GSP) sells the ad slots next to the results of a web search. The slots are ranked, and a higher slot gets more clicks. Each advertiser bids one price per click. GSP sorts the bids, gives the highest bidder the top slot, the second highest the second slot, and so on, and each winner pays, for each click, the bid of the bidder just below it. With one slot this is the [Vickrey auction](/vickrey-auction/). With two or more slots it is not truthful: a bidder can gain by bidding less and taking a lower slot at a lower price. It is still the standard format of search advertising, because it has a [locally envy-free equilibrium](/gsp-envy-free-equilibrium/) with the same slots and payments as the [VCG mechanism](/vcg-mechanism/).

## In plain words

Advertisers bid for places on a page of search results, and a place near the top gets more clicks. The page sorts the advertisers by bid. The best bid gets the top place, the next bid the next place, and so on. Each advertiser pays for each click the bid of the advertiser right below it, not its own bid. This looks like the sealed second-price auction, where the honest bid is always best, but it is different. Here an advertiser can bid less, drop one place, lose a few clicks, and pay much less for every click it keeps. So advertisers do not simply bid their values.

## The problem

There are $k$ slots and $n$ bidders. Slot $s$ gets $\alpha_s$ clicks, with $\alpha_1 \ge \alpha_2 \ge \cdots \ge \alpha_k \ge 0$, the same for every bidder. Bidder $i$ has a private value $v_i$ per click and [quasilinear utility](/quasilinear-utility/): in slot $s$ at the price $\pi$ per click it gets $\alpha_s (v_i - \pi)$. This is the [position auction](/position-auction/) model. Each bidder reports a bid $b_i$ per click. The mechanism gives each slot to at most one bidder and sets a price per click for each winner. A reserve price $r \ge 0$ is optional: a bid below $r$ takes no part.

## The algorithm

```pseudo id=main
GSP(b_1, ..., b_n, α_1, ..., α_k, r)
L1  R ← the bidders with b_i ≥ r, sorted by bid, highest first; ties go to the smaller index
L2  q ← min(k, |R|)
L3  for s ← 1 to q
L4      give slot s to R_s
L5      if R_{s+1} exists: π_s ← b of R_{s+1}
L6      else: π_s ← r
L7  return the slots and the prices per click π_1, ..., π_q
```

Bidder $R_s$ pays $\alpha_s \pi_s$ in total. Slots after $q$ stay empty.

## Example

This is the example of Edelman, Ostrovsky and Schwarz (2007). Three bidders have values $10, 4, 2$ per click, and two slots get $\alpha_1 = 200$ and $\alpha_2 = 199$ clicks. There is no reserve.

| bids | slot of bidder 1 | its price per click | its utility |
|---|---|---|---|
| $10, 4, 2$ (truthful) | 1 | 4 | $200 \cdot (10 - 4) = 1200$ |
| $3, 4, 2$ | 2 | 2 | $199 \cdot (10 - 2) = 1592$ |

Bidder 1 gains by bidding 3: it loses one click and saves 2 on each of 199 clicks. So truthful bidding is not a dominant strategy.

The VCG payments are $398$ for slot 2 (the value 2 of the third bidder times the 199 clicks it would gain) and $402$ for slot 1, in total 800. With the bids $10, 2.01, 2$ in GSP, bidder 1 pays $200 \cdot 2.01 = 402$ and bidder 2 pays $199 \cdot 2 = 398$. These bids form an equilibrium with the VCG outcome, and the page on the [locally envy-free equilibrium](/gsp-envy-free-equilibrium/) explains how to find them.

## Correctness

The proof is in `proofs/correctness.md`. It shows these facts.

- **The output.** Slot $s$ goes to the $s$-th eligible bidder in sorted order and costs the next eligible bid per click, or $r$ if there is none. No bidder gets two slots.
- **Individual rationality.** The price per click is at most the bidder's own bid and at least $r$, so a bidder that bids its value never gets a negative utility.
- **One slot is Vickrey.** With $k = 1$ the winner pays the larger of $r$ and the highest other bid.
- **Not truthful for two or more slots**, by the example above.
- **GSP payments are at least VCG payments for the same bids.** The VCG payment of slot $s$ is $\sum_{t \ge s} (\alpha_t - \alpha_{t+1})\, b_{(t+1)}$, and each bid in the sum is at most $b_{(s+1)}$, so the sum is at most $\alpha_s b_{(s+1)}$.

## Complexity

Sorting the bids takes $O(n \log n)$ time and $O(n)$ space, and lines L2 to L7 take $O(k)$ time. Only the $k + 1$ highest bids matter, so a [selection](/selection-problem/) of them and a sort of those $k + 1$ bids give $O(n + k \log k)$ time.

## Properties

- **Not DSIC** when $k \ge 2$ and $\alpha_1 > \alpha_2 > 0$, whatever the rates; the gain from bidding for a lower slot is largest when the click-through rates differ by little.
- **Ex post individually rational** for truthful bids, and every winner pays at most its bid.
- **Efficient equilibrium.** Every envy-free equilibrium in the sense of Varian gives the slots in the order of the values and pays at least the VCG payments; the bidder-optimal one has exactly the VCG outcome (Edelman, Ostrovsky and Schwarz 2007; Varian 2007).
- **Same bids, more money.** For the same bids GSP charges each bidder at least the VCG payment. In the equilibrium with the VCG outcome the revenue is the same as VCG, because the bids are lower.
- **Simple prices.** The price of a slot depends only on the next bid, which is easy to explain to advertisers.

## Variants and improvements

- **Weighted GSP.** Real systems rank by bid times a quality score, an estimate of the click-through rate of the ad, and charge the smallest bid that keeps the slot: $\pi_s = b_{s+1} w_{s+1} / w_s$ for the weights $w$. The model and the equilibrium results carry over with values scaled by the weights.
- **Reserve prices.** A [reserve price](/reserve-price/), the same for all bidders or one per bidder, raises revenue in the same way as in [Myerson's optimal auction](/myerson-optimal-auction/).
- **VCG for slots.** The [VCG mechanism](/vcg-mechanism/) charges slot $s$ the sum $\sum_{t \ge s} (\alpha_t - \alpha_{t+1}) b_{(t+1)}$. It is truthful and gives the same outcome as the bidder-optimal envy-free equilibrium of GSP. Some ad platforms use it.
- **Generalized first-price auction.** The early format of Overture charged each winner its own bid. Bids then changed all the time in cycles, which led to GSP.
- **Budgets.** With daily budgets the bidders, or the platform for them, scale the bids down; see [pacing equilibrium](/pacing-equilibrium/).

## When to use it

Use GSP to sell ranked slots with click-through rates that fall from the top, when the bidders are sophisticated and bid repeatedly, so that they can find an equilibrium. Use VCG when you want truthful bidding to be a dominant strategy, and use a [Vickrey auction](/vickrey-auction/) when there is one slot, where the two agree.

## Pitfalls

- **"Second price" does not mean truthful.** With two or more slots, the truth is not a dominant strategy, and an analysis that assumes it is wrong.
- **Many equilibria.** GSP has many Nash equilibria, some inefficient. The envy-free refinement picks a set with the VCG outcome or more revenue, but the refinement is an assumption about how bidders behave.
- **Ties.** Line L1 breaks ties by index. Bidders with equal bids pay the same price per click but get different numbers of clicks.
- **Separable click-through rates.** The model assumes that the clicks of a slot do not depend on the ad. With quality scores, rank by weighted bid, not by bid.

## Implementations

## History

Overture (formerly GoTo.com) sold search ads from 1997 in a pay-per-click auction where each winner paid its own bid. Bids changed quickly in cycles, and in 2002 Google introduced the rule that each winner pays the next bid, and Overture then adopted it. Edelman, Ostrovsky and Schwarz (2007) named the format the generalized second-price auction, showed that it is not truthful, and found its locally envy-free equilibria; Varian (2007) studied the same equilibria as symmetric Nash equilibria and tested them on data.

## References
