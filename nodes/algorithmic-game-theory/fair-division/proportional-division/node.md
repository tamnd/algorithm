---
tag: HTHT5J
kind: definition
slug: proportional-division
name: Proportional division
aliases:
- proportionality
area: algorithmic-game-theory/fair-division
level: intro
summary: An allocation in which each of the n agents gets a piece worth at least 1/n of the whole by its own measure.
prereqs: [cake-cutting-problem]
see_also: [envy-freeness, last-diminisher, dubins-spanier-moving-knife, even-paz-algorithm, edmonds-pruhs-lower-bound, divide-and-choose, indivisible-goods-allocation, proportional-fairness]
sources:
  - paper: "Hugo Steinhaus, The problem of fair division, Econometrica 16(1) (1948), 101-104"
    locator: the goal that each of n people gets at least 1/n by its own estimate, and the method of Banach and Knaster
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: Chapter 1, Proportionality for n = 2 (pp. 6-29), and Chapter 2, Proportionality for n > 2, the divisible case (from p. 30)
  - book: isbn:9781568810768
    title: Jack Robertson and William Webb, Cake-Cutting Algorithms, Be Fair If You Can, A K Peters, 1998
    locator: Chapter 1, Fairly Dividing a Cake; Chapter 3, Unequal Shares; Chapter 4, The Serendipity of Disagreement (more than 1/n when the valuations differ)
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms, Section 13.3, classic algorithms (from p. 313), and Section 13.4, complexity of cake cutting (from p. 316)
---

A proportional division of a [cake](/cake-cutting-problem/) among $n$ agents is an allocation in which each agent gets a piece that it values at least $1/n$ of the whole cake. Each agent measures with its own valuation, so the pieces need not be equal in size or in value to others. It is the weakest of the usual fairness goals: every [envy-free](/envy-freeness/) allocation of the whole cake is proportional, but not every proportional allocation is envy-free. A proportional allocation with connected pieces always exists and can be found with $\Theta(n \log n)$ queries in the [Robertson-Webb query model](/robertson-webb-query-model/).

## Definition

The cake is $[0, 1]$, and agent $i \in \{1, \dots, n\}$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. An allocation is a list of disjoint pieces $X_1, \dots, X_n$, each a finite union of intervals. The allocation is proportional when

$$V_i(X_i) \ge \frac{1}{n} \quad \text{for every agent } i.$$

The pieces do not have to cover the whole cake for this condition, but the usual protocols give all of it out. If the valuations are not normalized, the condition is $V_i(X_i) \ge V_i([0, 1]) / n$.

Related forms of the condition:

- **Weighted.** Agent $i$ has an entitlement $w_i \ge 0$ with $\sum_i w_i = 1$, and the condition is $V_i(X_i) \ge w_i$. The case $w_i = 1/n$ is the plain definition.
- **Strong.** The condition is $V_i(X_i) > 1/n$ for every $i$. Such an allocation exists exactly when at least two of the valuations differ. If all agents have the same valuation, the values of the pieces sum to at most 1 for each agent, so some agent gets at most $1/n$.
- **Approximate.** The condition is $V_i(X_i) \ge 1/(cn)$ for a factor $c \ge 1$. The [Edmonds-Pruhs lower bound](/edmonds-pruhs-lower-bound/) holds even for this weaker goal, for $c$ up to $n^{1 - \delta}$.

## Examples and non-examples

- **Identical valuations.** If all $n$ agents value the cake uniformly, an allocation is proportional exactly when each piece has length $1/n$ (when all the cake is given out). Each agent then gets exactly $1/n$, and no agent can get more without another agent getting less.
- **A non-example.** Three agents with uniform valuations get $[0, 1/2]$, $[1/2, 3/4]$ and $[3/4, 1]$. The second and the third agents get $1/4 < 1/3$, so the allocation is not proportional.
- **Different valuations.** Split $[0, 1]$ into four equal segments, and let agents 1, 2 and 3 have the densities $(1, 1, 1, 1)$, $(2, 1, 1, 0)$ and $(3, 1, 0, 0)$, scaled to total 1. The [last diminisher](/last-diminisher/) gives agent 3 the piece $[0, 1/9]$, agent 2 the piece $[1/9, 11/36]$ and agent 1 the piece $[11/36, 1]$, with values $1/3$, $1/3$ and $25/36$ for their owners. This is proportional. It is not envy-free, because agent 3 values the piece of agent 2 at $17/36$.
- **Two agents.** For $n = 2$ and an allocation of the whole cake, proportional and envy-free are the same, because $V_i(X_1) + V_i(X_2) = 1$. [Divide and choose](/divide-and-choose/) gives both.
- **Indivisible goods.** One good and two agents who both want it: no allocation is proportional, since one agent gets nothing. For [indivisible goods](/indivisible-goods-allocation/), weaker goals are used instead, such as proportional up to one good.

Protocols that find a proportional division for every $n$ are the last diminisher and the [Dubins-Spanier moving knife](/dubins-spanier-moving-knife/), with $O(n^2)$ queries, and the [Even-Paz algorithm](/even-paz-algorithm/), with $O(n \log n)$ queries. All three give connected pieces and guarantee $1/n$ to each agent that answers honestly, whatever the others answer.

## Related definitions

- [Envy-freeness](/envy-freeness/): no agent values another piece more than its own. It is stronger. If all the cake is given out, $n V_i(X_i) \ge \sum_j V_i(X_j) = 1$.
- Equitability: all agents get the same value by their own measures. A proportional allocation need not be equitable, and an equitable allocation need not be proportional (all agents can get the same small value).
- [Pareto optimality](/pareto-optimality/): no other allocation is at least as good for all agents and better for one. It is independent of proportional division. Giving the whole cake to one agent is Pareto optimal when no other agent values a part that the first agent does not value, but it is not proportional.
- Exact division: every agent values every piece at exactly $1/n$. It implies a proportional and envy-free division.
- [Proportional fairness](/proportional-fairness/) in networks is a different idea with a similar name: a rate allocation that maximizes the sum of the logarithms of the rates.

## References
