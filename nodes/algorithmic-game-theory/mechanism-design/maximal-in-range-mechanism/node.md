---
tag: HD9BNP
kind: technique
slug: maximal-in-range-mechanism
name: Maximal-in-range mechanism
aliases:
- MIR mechanism
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: "Fix a range of outcomes without looking at the bids, maximize reported welfare exactly over that range, and charge VCG payments on it. The result is deterministic and DSIC."
prereqs: [vcg-mechanism, affine-maximizer]
see_also: [truthful-in-expectation, roberts-theorem, combinatorial-auction, maximum-weight-matching, winner-determination-problem, approximation-ratio, submodular-function, single-minded-bidder-mechanism]
sources:
  - paper: doi:10.1613/jair.2046
    title: "Noam Nisan and Amir Ronen, Computationally feasible VCG mechanisms, Journal of Artificial Intelligence Research 29 (2007), 19-47"
    locator: VCG-based mechanisms with approximate allocation algorithms, and the result that they are truthful only when the algorithm is maximal in its range
  - paper: "Shahar Dobzinski and Noam Nisan, Mechanisms for multi-unit auctions, Journal of Artificial Intelligence Research 37 (2010), 85-98 (conference version in EC 2007)"
    locator: the maximal-in-range 2-approximation for multi-unit auctions that bundles the units into equal blocks and optimizes over blocks by dynamic programming
  - paper: "Shahar Dobzinski and Shaddin Dughmi, On the power of randomization in algorithmic mechanism design, Proceedings of the 50th IEEE Symposium on Foundations of Computer Science (FOCS 2009)"
    locator: maximal-in-distributional-range mechanisms and a truthful-in-expectation FPTAS for multi-unit auctions
  - paper: "Ron Lavi and Chaitanya Swamy, Truthful and near-optimal mechanism design via linear programming, Journal of the ACM 58(6) (2011), Article 25 (conference version in FOCS 2005)"
    locator: truthful-in-expectation mechanisms whose range is a scaled-down copy of the fractional relaxation
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 12, Ron Lavi, Computationally efficient approximation mechanisms
---

A maximal-in-range (MIR) mechanism fixes a set of outcomes, the *range*, before seeing any bids, finds the outcome of largest reported welfare inside the range exactly, and charges [VCG](/vcg-mechanism/) payments computed on the range. Because it is VCG on a smaller outcome set, it is deterministic and [DSIC](/dominant-strategy-incentive-compatibility/), and the designer only has to pick a range that is easy to optimize over and always contains a good outcome. Its close page, [truthful in expectation](/truthful-in-expectation/), is a weaker notion for randomized mechanisms. The randomized version of this technique, maximal in *distributional* range, optimizes over a fixed set of lotteries and gives mechanisms that are truthful in expectation but not DSIC in the deterministic sense. An MIR mechanism is the [affine maximizer](/affine-maximizer/) with weights 1 and no constants.

## In plain words

Finding the best way to split goods among bidders is often too slow to compute. A fast but inexact method usually breaks honesty, because a bidder may gain by lying to steer the method. The fix is to limit the choices in advance. Pick a list of allowed outcomes, chosen before anyone bids, so that the best outcome on the list is fast to find and never much worse than the true best. Then always choose the best outcome on the list, and charge each bidder the harm it does to the others, measured on the same list. This is the usual welfare-maximizing auction played on a smaller menu, so honesty is still the best plan for every bidder.

## When it applies

- The goal is social welfare, the sum of the agents' values, or something close to it.
- Agents have rich, multi-parameter valuations, so that by [Roberts' theorem](/roberts-theorem/) weighted welfare maximization is close to the only option for a deterministic DSIC rule.
- Exact welfare maximization over all outcomes is too hard, as for the [winner determination problem](/winner-determination-problem/) of a [combinatorial auction](/combinatorial-auction/).
- There is a range $R$ that depends only on public data, such as the numbers of agents and items, over which the maximum can be found exactly in polynomial time, and which contains an outcome within a factor $\alpha$ of the optimum for every valuation profile.

It does not fit objectives that are not sums of values, such as the makespan in [truthful scheduling](/truthful-scheduling-unrelated-machines/).

## The template

Let $O$ be the set of all outcomes and $R \subseteq O$ a nonempty range fixed in advance. On reports $b_1, \dots, b_n$:

```pseudo id=main
MAXIMAL-IN-RANGE(R, b_1, ..., b_n)
L1  for each o in R: T(o) ← b_1(o) + ... + b_n(o)
L2  x ← the first o in R with the largest T(o)
L3  for i ← 1 to n:
L4      W_-i ← max over o in R of (T(o) - b_i(o))    ▷ best welfare of the others, on the range
L5      p_i ← W_-i - (T(x) - b_i(x))
L6  return x, (p_1, ..., p_n)
```

In practice lines L1, L2 and L4 are not loops over $R$, which is usually exponentially large, but calls to a fast exact optimizer for the range, so the mechanism makes $n + 1$ optimizer calls.

**Truthfulness.** Agent $i$ with true valuation $v_i$ has utility $v_i(x) + \sum_{j \ne i} b_j(x) - W_{-i}$. The term $W_{-i}$ does not depend on $b_i$, and the truthful report makes $x$ maximize the first two terms over $R$. So truth telling is a dominant strategy. With nonnegative valuations the payments are nonnegative and truthful agents get nonnegative utility, as for VCG.

**Approximation.** The welfare of the outcome is $\max_{o \in R} \sum_i v_i(o)$, so the approximation ratio is
$$\alpha = \sup_{v} \frac{\max_{o \in O} \sum_i v_i(o)}{\max_{o \in R} \sum_i v_i(o)},$$
a property of the range alone. The design problem is to choose $R$ with a small $\alpha$ and a fast exact optimizer.

## Classic examples

**Grand bundle or one item each, worked by hand.** In a combinatorial auction with $m$ items, let $R$ contain the $n$ allocations that give all items to one bidder, and all allocations that give each bidder at most one item. The best grand bundle needs $n$ value queries, and the best one-item-each allocation is a [maximum-weight bipartite matching](/maximum-weight-matching/) between bidders and items with weights $b_i(\{j\})$. So the mechanism runs in polynomial time.

Take $m = 4$ items and two bidders with additive values: bidder 1 values each item at 3, and bidder 2 values item 1 at 5 and the others at 1. The optimum gives item 1 to bidder 2 and the rest to bidder 1, with welfare $5 + 9 = 14$. On the range, the grand bundles give $12$ and $8$, and the best matching gives $5 + 3 = 8$. The mechanism gives all items to bidder 1, with welfare 12. Bidder 1 pays $W_{-1} - 0 = \max(8, 5) - 0 = 8$, where $8$ is bidder 2's grand bundle and $5$ is its best single item, and has utility $12 - 8 = 4$. Bidder 2 pays $12 - 12 = 0$.

For subadditive valuations, $v(S \cup T) \le v(S) + v(T)$, this range has ratio at most $2\sqrt{m}$. Let $S_1, \dots, S_n$ be an optimal allocation. At most $\sqrt{m}$ bidders get more than $\sqrt{m}$ items, and each of them has value at most the best grand bundle, so together they have at most $\sqrt{m}$ times the best grand bundle. A bidder with $|S_i| \le \sqrt{m}$ has, by subadditivity, $v_i(S_i) \le \sqrt{m} \max_{j \in S_i} v_i(\{j\})$. Giving each such bidder its best item in $S_i$ is a matching, because the sets $S_i$ are disjoint, so these bidders together have at most $\sqrt{m}$ times the best matching. Adding, the optimum is at most $2\sqrt{m}$ times the better of the two parts of the range.

**Multi-unit auctions.** Dobzinski and Nisan (2007 conference, 2010 journal) studied $m$ identical units and $n$ bidders with general valuations for numbers of units. Their range splits the units into about $n^2$ equal blocks and allocates whole blocks only. The best allocation of blocks can be found by dynamic programming in time polynomial in $n$ and $\log m$, and the range always contains an allocation with at least half the optimal welfare. This gives a deterministic DSIC 2-approximation.

**VCG with an approximation algorithm.** Nisan and Ronen (2007) asked what happens when the exact optimizer inside VCG is replaced by an approximation algorithm. They showed that such a VCG-based mechanism is truthful only if the algorithm is maximal in its range. So the technique is the only way to keep VCG payments while giving up exact optimization.

**VCG itself** is the case $R = O$.

## Variations

- **Maximal in distributional range (MIDR).** The range is a fixed set of probability distributions over outcomes, and the mechanism picks the one with the largest expected reported welfare. With VCG payments in expectation, the mechanism is [truthful in expectation](/truthful-in-expectation/). Dobzinski and Dughmi (2009) used this to get an FPTAS for multi-unit auctions that is truthful in expectation, compared with the deterministic ratio 2 above.
- **Scaled LP ranges.** Lavi and Swamy (2005 conference, 2011 journal) take as range the fractional solutions of an LP relaxation scaled down by the integrality gap. Each scaled fractional solution is a lottery over integral solutions, so the mechanism is MIDR and truthful in expectation, with the ratio of the integrality gap.
- **Affine maximizers in range.** Adding weights and outcome constants keeps truthfulness by the same argument; see [affine maximizer](/affine-maximizer/).
- **Single-parameter alternatives.** When agents have one-number types, a designer can use any [monotone allocation rule](/monotone-allocation-rule/) instead, which is a much larger family; see [single-minded bidder mechanism](/single-minded-bidder-mechanism/).

## Pitfalls

- **The range must not depend on the bids.** Taking the better of two algorithms, where one of them is not optimal over a fixed range, gives a range that changes with the reports, and truthfulness fails in general.
- **The optimization over the range must be exact.** A near-optimal outcome inside the range is not enough: an agent can gain by lying to push the algorithm toward a better outcome for itself, the same failure as for VCG with an approximation algorithm.
- **Tie-breaking must be fixed.** Ties inside the range must be broken in a way that does not depend on the reports, for example by a fixed order of $R$.
- **The ratio is the worst case over all valuations.** A range that is good for typical inputs can still be very bad for some inputs, and the guarantee is only the worst case. For valuations with complements, the grand-bundle-or-one-item range above can lose a factor of about $m/2$.
- **Payments need $n + 1$ optimizations.** Each payment uses the best outcome in the range without one agent, so the running time is about $n + 1$ times that of the optimizer.

## Exercises

1. Show that the best one-item-each allocation in the worked example is a maximum-weight bipartite matching, and compute it for the two bidders above.
2. Give $m/2$ bidders, each of whom wants a different pair of items with value 1 and values every set without its pair at 0. Show that the grand-bundle-or-one-item range gets welfare 1 while the optimum is $m/2$.
3. Show that the Vickrey auction with an anonymous reserve price is an affine maximizer but not an MIR mechanism with constants 0 over the outcomes "bidder $i$ wins" and "nobody wins".
4. Assume valuations are monotone: a larger bundle is worth at least as much. Show that every MIR mechanism whose range contains the $n$ grand-bundle allocations gets at least a $1/n$ fraction of the optimal welfare.
5. Prove that the ratio of an MIR mechanism is exactly the worst case of the optimum over the best welfare in the range, as in the formula for $\alpha$.

## References
