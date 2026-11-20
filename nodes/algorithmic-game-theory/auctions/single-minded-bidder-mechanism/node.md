---
tag: Z6TN8C
kind: algorithm
slug: single-minded-bidder-mechanism
name: "Lehmann-O'Callaghan-Shoham mechanism"
aliases:
- LOS mechanism
- greedy mechanism for single-minded bidders
area: algorithmic-game-theory/auctions
level: advanced
summary: "A greedy mechanism for single-minded bidders: sort by value over the square root of bundle size, accept disjoint bundles, charge critical values. Truthful and a sqrt(m) approximation."
model: word-ram
complexity:
  vars: {n: the number of bidders, m: the number of items}
  time: {worst: O(n^2 m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 2002
  people: [Daniel Lehmann, Liadan Ita O'Callaghan, Yoav Shoham]
  note: Lehmann, O'Callaghan and Shoham (conference version 1999, journal version 2002) showed that a greedy allocation with critical-value payments is truthful for single-minded bidders, and that ranking by value over the square root of the bundle size gives a sqrt(m) approximation.
prereqs: [combinatorial-auction, winner-determination-problem, myerson-lemma, greedy-algorithm, approximation-ratio]
see_also: [vcg-mechanism, set-packing, maximal-in-range-mechanism, monotone-allocation-rule, single-parameter-environment, independent-set, truthful-in-expectation, dominant-strategy-incentive-compatibility]
sources:
  - paper: "Daniel Lehmann, Liadan Ita O'Callaghan and Yoav Shoham, Truth revelation in approximately efficient combinatorial auctions, Journal of the ACM 49(5) (2002), 577-602"
    locator: the greedy mechanism for single-minded bidders, the sufficient conditions for truthfulness (exactness and monotonicity with critical payments), and the sqrt(m) approximation bound
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: Chapter 11 (Blumrosen and Nisan, Combinatorial auctions), Section 11.2 (single-minded bidders)
---

The Lehmann-O'Callaghan-Shoham mechanism (LOS) is a truthful [combinatorial auction](/combinatorial-auction/) for *single-minded* bidders. Each such bidder wants one fixed bundle of items and values every set that contains it at the same amount, and every other set at 0. Even for these bidders, choosing the best allocation is the [weighted set packing](/set-packing/) problem, which is [NP-hard](/np-hard/), so the [VCG mechanism](/vcg-mechanism/) cannot run in polynomial time. LOS replaces the optimum with a [greedy](/greedy-algorithm/) choice: rank the bids by value over the square root of the bundle size, and accept each bid whose bundle does not meet an accepted one. Each winner pays its *critical value*, the smallest bid that would still win. The result is [DSIC](/dominant-strategy-incentive-compatibility/), and the welfare is at least $1/\sqrt{m}$ of the optimum, for $m$ items.

## In plain words

Each bidder wants one particular group of items and says how much the group is worth to it. Groups that share an item cannot both be sold. The auction ranks the bids by worth per item, but measured gently: it divides by the square root of the group size, so that one big group does not beat many small ones too easily. Then it walks down the ranking and accepts every group that does not clash with groups it has already accepted. A winner does not pay its bid. It pays the lowest bid that would still have won, given the other bids. So bidding the truth is always best, and the result is never too far from the best possible.

## The problem

There are $m$ items and $n$ bidders. Bidder $i$ is single-minded: it has a bundle $S_i$ and a value $v_i \ge 0$, and its value for a set $X$ is $v_i$ if $S_i \subseteq X$ and 0 otherwise. Its utility is [quasilinear](/quasilinear-utility/). Each bidder reports a bundle and a value. The mechanism picks a set $W$ of winners whose bundles are pairwise disjoint, and a payment for each winner. The aims are: truthful reporting of both the bundle and the value is a dominant strategy, the mechanism runs in polynomial time, and the welfare $\sum_{i \in W} v_i$ is close to the optimum.

## The algorithm

```pseudo id=main
LOS((S_1, v_1), ..., (S_n, v_n))
L1  order the bidders by v_i / sqrt(|S_i|), highest first; ties go to the smaller index
L2  W ← GREEDY(order), where GREEDY keeps a set of used items and:
L3      for each bidder i in the order
L4          if S_i does not meet the used items: accept i and add S_i to the used items
L5  for each winner i in W
L6      run GREEDY on the order without i; let j be the first accepted bidder whose bundle meets S_i
L7      p_i ← v_j · sqrt(|S_i|) / sqrt(|S_j|) if j exists, else 0
L8  return W and the payments p
```

Losers pay 0. The payment of line L7 is the bid at which the key of $i$ equals the key of $j$: $p_i / \sqrt{|S_i|} = v_j / \sqrt{|S_j|}$. It is usually irrational, so the code returns it exactly as $c\sqrt{r}$ with a rational $c$ and a square-free integer $r$.

## Example

Four bidders bid for the items $\{0, 1, 2, 3\}$.

| bidder | bundle | value | key $v / \sqrt{\lvert S \rvert}$ |
|---|---|---|---|
| 0 | $\{0, 1\}$ | 6 | $6 / \sqrt 2 \approx 4.24$ |
| 1 | $\{1, 2\}$ | 5 | $5 / \sqrt 2 \approx 3.54$ |
| 2 | $\{2, 3\}$ | 4 | $4 / \sqrt 2 \approx 2.83$ |
| 3 | $\{0, 1, 2, 3\}$ | 9 | $9 / 2 = 4.5$ |

The order is $3, 0, 1, 2$. Bidder 3 takes all four items, and every other bundle meets it. Without bidder 3, the greedy run accepts bidder 0 first, and $\{0, 1\}$ meets $\{0, 1, 2, 3\}$, so $j = 0$ and $p_3 = 6 \cdot \sqrt 4 / \sqrt 2 = 6\sqrt 2 \approx 8.49$. This is at most the bid 9, and bidder 3 would lose with any bid below $6\sqrt 2$. The welfare is 9, while bidders 0 and 2 together give 10.

## Correctness

The proof is in `proofs/correctness.md`. It shows these facts.

- **Feasibility.** The accepted bundles are pairwise disjoint.
- **Approximation.** Every bundle of an optimal solution meets the bundle of a winner that comes before it in the order, or is a winner itself. Charging each optimal bundle to such a winner and using the Cauchy-Schwarz inequality gives $\mathrm{OPT} \le \sqrt{m} \cdot \sum_{i \in W} v_i$.
- **Monotonicity.** If $i$ wins with $(S_i, v_i)$, it also wins with a higher value or a smaller bundle, because both raise its key and can only remove bidders that come before it.
- **Critical value.** For a fixed bundle, $i$ wins exactly when its value is at least the payment of line L7, with ties broken as in line L1.
- **Truthfulness.** A [monotone allocation rule](/monotone-allocation-rule/) with critical-value payments is truthful for single-minded bidders: lying about the value is handled as in [Myerson's lemma](/myerson-lemma/), and asking for a larger bundle cannot lower the critical value, while a bundle that misses an item of $S_i$ is worth 0. Truthful bidders never pay more than their value.
- **Tightness.** One bidder that wants all $m$ items with value $\sqrt m + \delta$ beats $m$ bidders that each want one item with value 1, so the ratio $\sqrt m$ cannot be improved for this order.

## Complexity

Line L1 takes $O(n \log n)$ time. One greedy run with a table of used items takes $O(\sum_i |S_i|) = O(nm)$ time, and lines L5 to L7 make one run per winner. So the total time is $O(n^2 m)$ and the extra space is $O(n + m)$. With $m$ large and bundles small, the bound is $O(n \sum_i |S_i|)$.

## Properties

- **DSIC and individually rational** for single-minded bidders, for misreports of both the value and the bundle.
- **A $\sqrt{m}$ approximation** of the optimal welfare. For general single-minded bids, no polynomial algorithm does better than $m^{1/2 - \epsilon}$ unless $\mathrm{P} = \mathrm{NP}$, by the hardness of [independent set](/independent-set/), so the bound is close to the best possible.
- **Deterministic and polynomial.**
- **Not VCG payments.** Its truthfulness comes from a monotone allocation with critical prices, not from the VCG payment rule, which is a different route from [maximal-in-range mechanisms](/maximal-in-range-mechanism/).

## Variants and improvements

- **Other ranking keys.** Any key that increases in the value and decreases in the bundle size gives a truthful mechanism with critical payments. Ranking by $v_i$ gives an $m$ approximation, and ranking by $v_i / |S_i|$ also gives $m$; the square root balances the two failure modes.
- **Known single-minded bidders.** If the bundles are public, only the values are private. This is a [single-parameter environment](/single-parameter-environment/), and any monotone algorithm with threshold payments is truthful.
- **Small bundles.** If every bundle has at most $d$ items, greedy by value gives a $d$ approximation.
- **Multi-unit and general bidders.** For bidders with general valuations, truthful polynomial mechanisms use maximal-in-range or randomized ([truthful in expectation](/truthful-in-expectation/)) designs, and the best known ratios are weaker.

## When to use it

Use it for a combinatorial auction where each bidder wants one specific package, the instance is too large for exact winner determination, and the bidders must not need to strategize. If exact winner determination is feasible, VCG gives the optimal welfare and is also truthful.

## Pitfalls

- **Payments with a greedy rule that is not monotone.** Critical-value payments are only truthful when the allocation is monotone. Adding a local improvement step after the greedy pass can break monotonicity.
- **VCG payments with greedy allocation.** Charging VCG-style payments computed with the greedy allocation is not truthful.
- **Exact arithmetic.** The keys and payments involve square roots. Floating point can change the order at ties and break truthfulness, so compare keys by $v_i^2 / |S_i|$ in exact arithmetic.
- **Bidders who are not single-minded.** If a bidder values two different bundles, the mechanism cannot express it, and truthfulness may fail.

## Implementations

## History

Lehmann, O'Callaghan and Shoham presented the mechanism at the ACM Conference on Electronic Commerce in 1999, and the journal version appeared in 2002. They identified the conditions under which a greedy allocation with critical payments is truthful for single-minded bidders, and they proved the $\sqrt m$ bound for the square root key. Their work was one of the first to combine a polynomial approximation algorithm with dominant-strategy incentives for a hard allocation problem.

## References
