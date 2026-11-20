---
tag: SH7M6B
kind: algorithm
slug: vcg-mechanism
name: Vickrey-Clarke-Groves mechanism
aliases:
- VCG mechanism
area: algorithmic-game-theory/mechanism-design
level: intro
summary: Picks the outcome of maximum reported welfare and charges each agent the welfare loss it causes the others. Truth telling is a dominant strategy for any valuations.
model: word-ram
complexity:
  vars: {n: the number of agents, k: "the number of outcomes, with each valuation given as a table of k numbers"}
  time: {worst: O(n k)}
  space: {extra: O(k)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1973
  people: [William Vickrey, Edward H. Clarke, Theodore Groves]
  note: Vickrey analysed the second-price auction in 1961, Clarke proposed the pivot payment for public projects in 1971, and Groves gave the general family of truthful welfare-maximizing payments in 1973.
prereqs: [quasilinear-utility, direct-revelation-mechanism, dominant-strategy-incentive-compatibility]
see_also: [groves-mechanisms, clarke-pivot-rule, vickrey-auction, combinatorial-auction, winner-determination-problem, green-laffont-theorem, affine-maximizer, maximal-in-range-mechanism]
sources:
  - paper: doi:10.1111/j.1540-6261.1961.tb02789.x
    title: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    locator: the second-price sealed-bid auction and the proof that bidding the true value is a dominant strategy
  - paper: doi:10.1007/BF01726210
    title: "Edward H. Clarke, Multipart pricing of public goods, Public Choice 11 (1971), 17-33"
    locator: the pivot payment for a public project, which charges an agent only when its report changes the decision
  - paper: doi:10.2307/1914085
    title: "Theodore Groves, Incentives in teams, Econometrica 41(4) (1973), 617-631"
    locator: the general payment scheme that makes truth telling dominant for any welfare-maximizing decision
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), Sections 9.3.3 to 9.3.5 (VCG mechanisms, the Clarke pivot rule with its individual rationality and no positive transfers, and the examples)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 7 (multi-parameter mechanism design, the VCG mechanism and its practical problems)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Sections 10.4.1 to 10.4.4 (Groves mechanisms, the VCG mechanism, VCG and individual rationality, VCG and weak budget balance)
  - paper: "Lawrence M. Ausubel and Paul Milgrom, The lovely but lonely Vickrey auction, in Peter Cramton, Yoav Shoham and Richard Steinberg (eds.), Combinatorial Auctions, MIT Press, 2006, Chapter 1, 17-40"
    locator: low or zero revenue with complements, outcomes outside the core, collusion of losing bidders and shill bids
  - paper: doi:10.1613/jair.2046
    title: "Noam Nisan and Amir Ronen, Computationally feasible VCG mechanisms, Journal of Artificial Intelligence Research 29 (2007), 19-47"
    locator: VCG payments with an approximate welfare optimizer are not truthful in general
---

The Vickrey-Clarke-Groves (VCG) mechanism is a [direct revelation mechanism](/direct-revelation-mechanism/) for agents with [quasilinear utility](/quasilinear-utility/). It asks each agent for its valuation of every outcome, chooses an outcome that maximizes the sum of the reported values, and charges each agent the loss of welfare that its presence causes to the other agents. Truth telling is a dominant strategy for every agent, for any set of outcomes and any valuations ([DSIC](/dominant-strategy-incentive-compatibility/)), and the chosen outcome maximizes the true welfare. The [Vickrey auction](/vickrey-auction/) is the case of one item. VCG is the member of the [Groves mechanisms](/groves-mechanisms/) with the [Clarke pivot rule](/clarke-pivot-rule/) as payment.

## In plain words

A group must make one choice, for example who gets which items or whether to build a bridge. Each person says how much each possible choice is worth to them in money. The mechanism takes the choice with the largest total worth. Then it asks of each person: how much better off would the others be if this person had stayed at home? The answer is what the person pays. A person who changes nothing for the others pays nothing. A person who pushes the choice away from what the others would have taken pays for the harm. With these prices, each person gains most by telling the truth. A false report can change the choice only to one with a smaller total worth, counted with the person's true worth, and the payment follows the others' loss exactly, so a lie never pays.

## The problem

There are $n$ agents and a finite set $O$ of $k$ outcomes. Agent $i$ has a private valuation $v_i : O \to \mathbb{R}$, and each valuation in $\mathbb{R}^O$ is possible. The mechanism receives reports $b_1, \ldots, b_n$, chooses an outcome $x(b) \in O$, and charges payments $p_1(b), \ldots, p_n(b)$. The payment $p_i$ goes from agent $i$ to the mechanism, and a negative $p_i$ is a transfer to the agent. Agent $i$ has the quasilinear utility $u_i = v_i(x(b)) - p_i(b)$. The goal is a mechanism that is DSIC and whose outcome maximizes the welfare $\sum_i v_i(x)$ when the agents tell the truth.

## The algorithm

Write $T(o) = \sum_{j} b_j(o)$ for the reported welfare of outcome $o$. Then $T(o) - b_i(o)$ is the welfare of the agents other than $i$.

```pseudo id=main
VCG(O, b_1, ..., b_n)
L1  for each o in O: T(o) ← b_1(o) + ... + b_n(o)
L2  x ← the first o in O with the largest T(o)
L3  for i ← 1 to n:
L4      W_-i ← max over o in O of (T(o) - b_i(o))    ▷ best welfare of the others if i were absent
L5      p_i ← W_-i - (T(x) - b_i(x))                 ▷ minus the welfare the others get at x
L6  return x, (p_1, ..., p_n)
```

Line L4 is the best welfare the others could reach without agent $i$, and line L5 subtracts the welfare they actually get. So $p_i$ is the *externality* of agent $i$. In the form of a Groves mechanism, $p_i(b) = h_i(b_{-i}) - \sum_{j \ne i} b_j(x(b))$ with $h_i(b_{-i}) = W_{-i}$, and $W_{-i}$ does not depend on $b_i$. Line L2 breaks ties by the fixed order of $O$. Any rule that picks some welfare-maximizing outcome gives the same guarantees.

## Example

Two items $A$ and $B$ and three bidders. Bidder 1 wants both items together and values $\{A, B\}$ at 10, and each single item at 0. Bidder 2 values $A$ at 6, and bidder 3 values $B$ at 7, and neither wants the other item. An outcome gives each item to one bidder or keeps it, so there are $4^2 = 16$ outcomes. The best one gives $A$ to bidder 2 and $B$ to bidder 3, with welfare 13. Giving both items to bidder 1 has welfare 10.

| agent $i$ | $W_{-i}$ (best without $i$) | others' welfare at $x$ | $p_i$ | utility |
|---|---|---|---|---|
| 1 | 13 ($A$ to 2, $B$ to 3) | 13 | 0 | 0 |
| 2 | 10 (both to 1) | 7 | 3 | 6 - 3 = 3 |
| 3 | 10 (both to 1) | 6 | 4 | 7 - 4 = 3 |

Bidder 2 pays 3, the least bid for $A$ that still wins it against the threat of bidder 1: with a bid below 3 for $A$, the pair of bidders 2 and 3 would bid less than 10 in total. The revenue is 7, less than the bid 10 of bidder 1. So bidder 1 and the seller would both prefer a deal at a price between 7 and 10: the VCG outcome is not in the core here.

With one item and values $(10, 7, 3)$, the outcomes are "bidder $i$ wins". Bidder 1 wins. Without bidder 1 the others reach 7, and at $x$ they get 0, so bidder 1 pays 7. The losers pay 0. This is the Vickrey auction.

## Correctness

Three facts hold for every input, and the proof is in `proofs/correctness.md`.

- **Welfare.** Line L2 returns an outcome with the largest reported welfare. When the agents tell the truth, it maximizes the true welfare.
- **Dominant strategies.** For every agent $i$, true valuation $v_i$, report $b_i$ and reports $b_{-i}$ of the others, $v_i(x(v_i, b_{-i})) - p_i(v_i, b_{-i}) \ge v_i(x(b_i, b_{-i})) - p_i(b_i, b_{-i})$. The utility of agent $i$ equals the reported welfare of the chosen outcome, with $v_i$ in place of $b_i$, minus $W_{-i}$, which agent $i$ cannot change. The truthful report makes the mechanism maximize exactly this welfare.
- **Payments.** $p_i \ge 0$ for every input, because $W_{-i}$ is a maximum over all outcomes. If every valuation is nonnegative, then $u_i \ge 0$ for a truthful agent ([individual rationality](/individual-rationality/)).

## Complexity

With each valuation given as a table of $k$ numbers, the input has $n k$ numbers. Line L1 takes $O(nk)$ additions, line L2 takes $O(k)$ comparisons, and each pass of lines L4 and L5 takes $O(k)$. The total time is $O(nk)$, linear in the input, and the extra space is $O(k)$ for the table $T$. This assumes word-ram arithmetic on numbers of bounded size; the implementation uses exact fractions.

In most uses $O$ is not a list. It is a set of allocations of $m$ items, of paths in a graph or of schedules, and it has exponential size. Then VCG needs one welfare maximization for $x$ and one more for each $W_{-i}$, so $n + 1$ calls to an exact optimizer in total. For a [combinatorial auction](/combinatorial-auction/) the optimization is the [winner determination problem](/winner-determination-problem/), which is NP-hard. VCG with an approximate optimizer is not truthful in general (Nisan and Ronen 2007). The ways around this are [maximal-in-range mechanisms](/maximal-in-range-mechanism/), which optimize exactly over a smaller range, and the single-parameter methods of [Myerson's lemma](/myerson-lemma/).

## Properties

- **DSIC and efficient.** Truth telling is a dominant strategy, and the outcome maximizes welfare. This holds with no prior on the valuations.
- **No positive transfers.** No agent is ever paid: $p_i \ge 0$.
- **Ex post individually rational for nonnegative valuations.** It can fail when an agent has a negative value for some outcome. With outcomes "no" and "yes" for a project, agent 1 values "yes" at 5 and agent 2 values it at $-2$. VCG builds, agent 2 pays 0 and ends at utility $-2$.
- **Weakly budget balanced, not budget balanced.** The payments sum to at least 0, but in general not to 0, and the surplus cannot be returned without loss of DSIC or efficiency ([budget balance](/budget-balance/), [Green-Laffont theorem](/green-laffont-theorem/)).
- **Payments depend on others only through $W_{-i}$ and the outcome.** Agent $i$ influences its payment only through the choice of $x$.

## Variants and improvements

- **Groves mechanisms.** Replace $W_{-i}$ by any function $h_i(b_{-i})$. Every choice is DSIC and efficient. On the unrestricted domain these are the only DSIC efficient mechanisms ([Groves mechanisms](/groves-mechanisms/)).
- **Weighted VCG and affine maximizers.** Maximize $\sum_i w_i b_i(o) + c_o$ with fixed weights $w_i > 0$ and constants $c_o$, with the matching payments ([affine maximizer](/affine-maximizer/)). Roberts' theorem says that on unrestricted domains with at least 3 outcomes these are the only truthful mechanisms onto their range ([Roberts' theorem](/roberts-theorem/)).
- **Reverse auctions and procurement.** The agents have costs, so their values are negative or zero. For a path in a graph whose edges are owned by agents, VCG picks the [shortest path](/shortest-path/) and pays each edge on it the length of the shortest path without that edge minus the length of the chosen path without that edge (Nisan, Section 9.3.5).
- **Public projects.** Add the planner as one more agent with the value $-C$ for building. The payments of the citizens then do not cover $C$ in general: with values 150, 120 and 60 and $C = 300$, the project is built and the citizens pay 120, 90 and 30, in total 240.
- **Redistribution.** Rebates that depend only on the others' reports return part of the surplus and keep DSIC ([Groves mechanisms](/groves-mechanisms/) gives an example).

## When to use it

Use VCG when the goal is welfare, the agents' values are private and can take any form, and an exact optimizer for the outcome is affordable. It needs no prior and no assumption on the valuations. It is a poor choice when revenue matters (use [Myerson's optimal auction](/myerson-optimal-auction/) in single-parameter settings), when the budget must balance (use the [AGV mechanism](/agv-mechanism/), which is only Bayesian incentive compatible), or when the optimization is too hard to solve exactly.

## Pitfalls

- **An approximate optimizer.** Lines L2 and L4 must solve the optimization exactly. With a heuristic, an agent can gain by a lie that steers the heuristic to a better outcome for it.
- **Low or zero revenue.** With complements, revenue can be 0. Let bidder 1 value $\{A, B\}$ at 2, bidder 2 value $A$ at 2 and bidder 3 value $B$ at 2. VCG gives $A$ to bidder 2 and $B$ to bidder 3, and both pay $2 - 2 = 0$. Adding bidders 2 and 3 lowered the revenue from 2 to 0, so revenue is not monotone in the set of bidders.
- **Collusion of losers.** In the same auction, let the true values of bidders 2 and 3 be $1/2$ each. Truthful bids give both items to bidder 1 at price 1. If bidders 2 and 3 both bid 2, they win, pay 0, and each gains $1/2$. DSIC is about one agent at a time, not about groups.
- **False-name bids.** A bidder can gain by bidding under several names in a combinatorial auction (Yokoo, Sakurai and Matsubara 2004); in the example above one bidder with two names plays the part of bidders 2 and 3.
- **Negative values and IR.** The Clarke pivot rule gives IR only when all valuations are nonnegative.
- **Ties.** A truthful agent can be indifferent between reports. The guarantees hold for any fixed tie rule, but a test of DSIC must compare utilities with $\ge$, not $>$, and must use exact arithmetic.

## Implementations

## History

Vickrey (1961) studied the sealed-bid auction in which the highest bidder pays the second-highest bid, and showed that bidding the true value is dominant. Clarke (1971) proposed, for a public project, to charge each citizen only when its report changes the decision, by the amount of the change for the others. Groves (1973) gave the general scheme for a team: pay each member the reported value of the others, plus any term that does not depend on its own report. The name "VCG" for the combination with the pivot term became standard in the computer science literature, where Nisan and Ronen began the study of its computational side.

## References
