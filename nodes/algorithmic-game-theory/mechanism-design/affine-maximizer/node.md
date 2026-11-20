---
tag: P44K0N
kind: definition
slug: affine-maximizer
name: Affine maximizer
aliases:
- weighted VCG mechanism
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: "A mechanism that maximizes a weighted sum of reported values, with positive weights per agent, plus a constant per outcome over a fixed range. Weighted VCG payments make it DSIC."
prereqs: [vcg-mechanism, groves-mechanisms]
see_also: [roberts-theorem, maximal-in-range-mechanism, vcg-mechanism, green-laffont-theorem, reserve-price, myerson-optimal-auction, cycle-monotonicity, combinatorial-auction]
sources:
  - paper: "Kevin Roberts, The characterization of implementable choice rules, in Jean-Jacques Laffont (ed.), Aggregation and Revelation of Preferences, North-Holland, 1979, 321-348"
    locator: affine maximizers as the only dominant-strategy implementable rules on unrestricted domains with at least three outcomes
  - paper: doi:10.1007/s00355-008-0331-y
    title: "Ron Lavi, Ahuva Mu'alem and Noam Nisan, Two simplified proofs for Roberts' theorem, Social Choice and Welfare 32(3) (2009), 407-423"
    locator: the definition of affine maximizers and their weighted VCG payments
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), the part on affine maximizers and Roberts' theorem; Chapter 12, Ron Lavi, Computationally efficient approximation mechanisms
  - paper: doi:10.1613/jair.2046
    title: "Noam Nisan and Amir Ronen, Computationally feasible VCG mechanisms, Journal of Artificial Intelligence Research 29 (2007), 19-47"
    locator: VCG-based mechanisms and the result that truthful VCG-based allocation rules are maximal in range
---

An affine maximizer chooses, from a fixed range of outcomes, one that maximizes a weighted sum of the agents' reported values plus a fixed bonus for each outcome. The weights are positive and the bonuses do not depend on the reports, so payments in the style of [VCG](/vcg-mechanism/) make it [DSIC](/dominant-strategy-incentive-compatibility/). VCG itself is the affine maximizer with all weights 1, no bonuses and the full range, and a [maximal-in-range mechanism](/maximal-in-range-mechanism/) is the case with weights 1 and a restricted range. [Roberts' theorem](/roberts-theorem/) says that on the unrestricted domain with at least three outcomes in the range, affine maximizers are the only deterministic DSIC rules.

## Definition

Let $O$ be a finite set of outcomes and let there be $n$ agents with [quasilinear](/quasilinear-utility/) utilities, each reporting a valuation $b_i : O \to \mathbb{R}$. Fix

- a nonempty *range* $R \subseteq O$,
- a *weight* $w_i > 0$ for each agent $i$,
- a *constant* $c(o) \in \mathbb{R}$ for each $o \in R$.

The **affine maximizer** with these parameters picks
$$x(b) \in \arg\max_{o \in R} \Bigl( \sum_{i=1}^{n} w_i \, b_i(o) + c(o) \Bigr),$$
with a fixed tie-breaking order on $R$. Its payments are
$$p_i(b) = h_i(b_{-i}) - \frac{1}{w_i} \Bigl( \sum_{j \ne i} w_j \, b_j(x(b)) + c(x(b)) \Bigr),$$
where $h_i$ is any function that does not depend on $b_i$. The Clarke-style choice is $h_i(b_{-i}) = \frac{1}{w_i} \max_{o \in R} \bigl( \sum_{j \ne i} w_j b_j(o) + c(o) \bigr)$, the best score that the others and the constants can reach alone.

**Why it is DSIC.** An agent with true valuation $v_i$ who reports $b_i$ gets the utility
$$v_i(x(b)) - p_i(b) = \frac{1}{w_i} \Bigl( w_i \, v_i(x(b)) + \sum_{j \ne i} w_j \, b_j(x(b)) + c(x(b)) \Bigr) - h_i(b_{-i}).$$
The term $h_i(b_{-i})$ does not depend on the report, and $w_i > 0$. The bracket is the objective of the mechanism evaluated with $v_i$ in place of $b_i$, at the outcome $x(b)$. The truthful report makes $x$ maximize exactly this bracket over $R$, so no report does better.

With the Clarke-style $h_i$ and nonnegative valuations, every payment is nonnegative and every truthful agent has utility at least 0. The utility of agent $i$ is $\frac{1}{w_i}$ times the best total score minus the best score without $i$, which is at least 0.

The procedure, with the Clarke-style payments:

```pseudo id=main
AFFINE-MAXIMIZER(R, w, c, b_1, ..., b_n)
L1  for each o in R: S(o) ← c(o) + w_1 b_1(o) + ... + w_n b_n(o)
L2  x ← the first o in R with the largest S(o)
L3  for i ← 1 to n:
L4      H_i ← max over o in R of (S(o) - w_i b_i(o))    ▷ best score without agent i
L5      p_i ← (H_i - (S(x) - w_i b_i(x))) / w_i
L6  return x, (p_1, ..., p_n)
```

With the valuations given as tables over $R$, the procedure takes $O(n \, |R|)$ arithmetic operations. Roberts' theorem allows some weights to be 0, as long as not all are. An agent with weight 0 has no influence on the outcome, and its payment must then be a function $h_i(b_{-i})$ alone.

## Examples and non-examples

A small example. One item, two bidders with values $10$ and $7$, weights $w = (1, 2)$, no constants. The outcomes are "bidder 1 wins", "bidder 2 wins" and "nobody wins". The scores are $10$, $14$ and $0$, so bidder 2 wins. Its payment is $\frac{1}{2}(10 - 0) = 5$. Check: bidder 2 wins exactly when $2 b_2 > 10$, so its threshold bid is $5$, which is the payment that [Myerson's lemma](/myerson-lemma/) gives. Bidder 2 has utility $7 - 5 = 2$, and bidder 1 pays nothing.

More affine maximizers:

- **VCG.** All $w_i = 1$, all $c(o) = 0$, $R = O$.
- **Vickrey auction with an anonymous reserve.** One item, outcomes "bidder $i$ wins" for each $i$ and "nobody", with $c(\text{nobody}) = r$ and $c = 0$ otherwise, and all weights 1. The item goes to the highest bidder if its bid is at least $r$, and the winner pays $\max(\text{second-highest bid}, r)$. See [reserve price](/reserve-price/).
- **Bidder-specific reserves, in affine form.** With $c(\text{bidder } i \text{ wins}) = -r_i$ and $c(\text{nobody}) = 0$, the item goes to the bidder with the largest $b_i - r_i$, if that is positive. This is not the same rule as "highest bidder among those above their own reserve". With reserves $r = (0, 5)$ and bids $(6, 10)$, the affine scores are $6 - 0 = 6$ and $10 - 5 = 5$, so bidder 1 wins. The other rule gives the item to bidder 2, the highest bidder, since both bids are above their reserves.
- **Maximal-in-range mechanisms.** Weights 1, constants 0, and a range $R$ that is smaller than $O$ so that the maximization is fast. See [maximal-in-range mechanism](/maximal-in-range-mechanism/).
- **Weighted welfare.** Weights that express the priority of agents, for example in a public decision where some agents represent more people.

Non-examples:

- **The optimal auction for different value distributions.** [Myerson's optimal auction](/myerson-optimal-auction/) with bidders of different distributions gives the item to the bidder with the largest virtual value, which is not an affine function of the bids. It is DSIC because the domain is single-parameter, which is far from unrestricted, so Roberts' theorem does not apply to it.
- **The greedy knapsack rule.** The rule on the page [monotone allocation rule](/monotone-allocation-rule/) is DSIC in its single-parameter domain, but it does not maximize any fixed affine function over a fixed range.
- **Makespan minimization.** A scheduling rule that minimizes the largest load is a min-max rule, not the maximization of a weighted sum. This is why VCG, the natural affine maximizer for scheduling, only gets ratio $n$; see [truthful scheduling on unrelated machines](/truthful-scheduling-unrelated-machines/).
- **Weights that depend on the bids.** If $w_i$ changes with $b_i$, the argument above fails, and the rule is not DSIC in general.

## Related definitions

- **[Groves mechanisms](/groves-mechanisms/).** The payments of an affine maximizer are the Groves payments for the weighted objective, divided by $w_i$. With weights 1 and constants 0, they are exactly the Groves payments.
- **[Roberts' theorem](/roberts-theorem/).** On the unrestricted domain with a range of at least three outcomes, every deterministic DSIC rule is an affine maximizer, with weights $w_i \ge 0$ not all 0.
- **[Green-Laffont theorem](/green-laffont-theorem/).** For the efficient rule, the payments are fixed up to $h_i$. Roberts' theorem fixes the rule, and Green-Laffont fixes the payments.
- **[Maximal-in-range mechanism](/maximal-in-range-mechanism/).** The special case used to build truthful approximation mechanisms. Maximal-in-distributional-range mechanisms are the randomized version, which is [truthful in expectation](/truthful-in-expectation/).
- **[Cycle monotonicity](/cycle-monotonicity/).** Affine maximizers satisfy it, as every DSIC rule must.

## References
