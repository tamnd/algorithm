---
tag: 994S1T
kind: problem
slug: chore-division
name: Chore division
aliases:
- fair division of bads
area: algorithmic-game-theory/fair-division
level: advanced
summary: "Fair division of a burden or of items with negative value, where each agent wants as little as possible by its own measure."
model: robertson-webb-query-model
complexity:
  vars: {n: the number of agents}
  time: {worst: Θ(n log n)}
see_also: [cake-cutting-problem, rental-harmony, divide-and-choose, even-paz-algorithm, edmonds-pruhs-lower-bound, su-rental-harmony-algorithm, indivisible-goods-allocation, round-robin-allocation]
sources:
  - paper: "Francis Edward Su, Rental harmony: Sperner's lemma in fair division, American Mathematical Monthly 106(10) (1999), 930-942"
    locator: Section 6, Chores and Rent-partitioning (envy-free chore division with Sperner labels), and the procedures of Oskui and of Peterson and Su that Su reports
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: pp. 153-155 (moving-knife procedures for chores, as cited by Su)
  - paper: "Sina Dehghani, Alireza Farhadi, MohammadTaghi Hajiaghayi and Hadi Yami, Envy-free chore division for an arbitrary number of agents, SODA 2018, pp. 2564-2583"
    locator: the first bounded envy-free chore protocol for any number of agents
  - paper: "Alireza Farhadi and MohammadTaghi Hajiaghayi, On the complexity of chore division, arXiv:1710.00271 (2017)"
    locator: the abstract (a link between chore division and cake cutting, and the lower bound of n log n queries for proportional chore division)
---

Chore division is the [cake cutting problem](/cake-cutting-problem/) for a bad resource: a burden such as a set of tasks, a period of duty or a shared cost, which each agent wants to receive as little of as possible by its own measure. The fairness goals are the mirror images of those for goods: a proportional division gives each of $n$ agents at most $1/n$ of the burden by its own measure, and an envy-free division gives each agent a part that it finds no worse than any other part. The difference from cake cutting is the direction of preferences, and it matters because protocols for goods cannot simply be reversed: trimming a piece makes it worse for goods but better for chores. The difference from [rental harmony](/rental-harmony/) is that there the burden, the rent, is attached to rooms that are goods, while here everything is bad.

## In plain words

Some housemates must share the housework. Each has its own view: one hates washing dishes, another hates cleaning the bathroom. The work can be split in many ways, and each housemate wants as little as possible by its own view.

A fair split can mean that each housemate thinks it does at most its share of all the work. A stronger meaning is that no housemate would rather swap its tasks with the tasks of another housemate. These are the same ideas as for sharing a cake, turned around: here a bigger piece is a worse piece.

The methods for cakes do not always carry over. Cutting a little off a piece helps the person who gets it, not hurts, so the steps of a good method for cakes can do the wrong thing for chores.

## Definition

The burden is the interval $[0, 1]$. Agent $i$ has a cost measure $C_i$ that is nonnegative, additive and nonatomic, with $C_i([0, 1]) = 1$. A division is a list of pieces $X_1, \dots, X_n$, each a finite union of intervals, that are disjoint up to end points and cover $[0, 1]$. It is

- **proportional** if $C_i(X_i) \le 1/n$ for every $i$;
- **envy-free** if $C_i(X_i) \le C_i(X_j)$ for every $i$ and $j$.

An envy-free division of the whole burden is proportional, since $n C_i(X_i) \le \sum_j C_i(X_j) = 1$. The input is given by queries, as in the [Robertson-Webb model](/robertson-webb-query-model/): $\mathrm{Eval}_i(x, y)$ returns $C_i([x, y])$ and $\mathrm{Cut}_i(x, t)$ returns a point $y$ with $C_i([x, y]) = t$. The measure is the number of queries in the worst case.

For indivisible chores there is a finite set of items, agent $i$ has an additive cost $c_i(e) \ge 0$ for each item $e$, and each item goes to one agent.

## Variants

- **Divisible or indivisible.** A divisible burden is cut; indivisible chores are given out whole, and then envy-free divisions need not exist, so weaker goals such as envy-freeness up to one chore are used.
- **Connected pieces.** Each agent gets one interval, as when the burden is a period of time.
- **Proportional or envy-free.** As for goods.
- **Mixed resources.** Some parts are goods for some agents and bads for others.
- **Rent and chores.** Su treats rent as a chore to share: each tenant wants to pay as little as possible, which gives a chore division with the rooms as a second part of the problem.

## Examples

**Two agents.** Agent 1 has a uniform cost on $[0, 1]$. Agent 2 finds only $[0, 1/2]$ costly, with density 2 there. Agent 1 cuts the burden into two pieces of equal cost to it, at $1/2$. Agent 2 takes the piece that costs it less, $[1/2, 1]$, at cost 0. Agent 1 gets $[0, 1/2]$ at cost $1/2$, the same as the other piece in its eyes. The division is envy-free. This is [divide and choose](/divide-and-choose/), with the chooser taking the smaller piece instead of the larger one.

**Indivisible chores.** Two agents share three chores $A$, $B$ and $C$. Agent 1 has costs $(1, 2, 3)$ and agent 2 has costs $(3, 1, 2)$. With one chore and two agents, the agent that gets it always envies the other, so exact envy-freeness can fail. With [round-robin](/round-robin-allocation/) picking, each agent in turn takes the remaining chore that costs it least. Agent 1 takes $A$, agent 2 takes $B$, and agent 1 takes $C$. Agent 1 has cost $4$ and values the bundle of agent 2 at $2$, so it envies; but without $C$ its cost is $1 \le 2$. So the division is envy-free up to one chore.

## Known algorithms

| method | agents | goal | notes |
|---|---|---|---|
| divide and choose, chooser takes the smaller piece | 2 | envy-free | 2 queries |
| [Even-Paz](/even-paz-algorithm/) with the halving rule reversed | $n$ | proportional | $O(n \log n)$ queries |
| Oskui's procedure, as reported by Su (1999) | 3 | envy-free | discrete |
| moving-knife procedures for chores (Brams and Taylor) | small $n$ | envy-free | continuous knives |
| Su's method with Sperner labels | $n$ | approximately envy-free, connected | see [Su's algorithm](/su-rental-harmony-algorithm/) |
| Dehghani, Farhadi, Hajiaghayi and Yami (SODA 2018) | $n$ | envy-free | bounded number of queries |
| round-robin | $n$, indivisible | envy-free up to one chore | each agent picks its cheapest remaining chore |

**Even-Paz for chores.** Each agent marks the point $x_i$ with $C_i([0, x_i]) = 1/2$. Let $m$ be the median mark. The $n/2$ agents with the largest marks find $[0, m]$ worth at most $1/2$ of their cost, and the others find $[m, 1]$ worth at most $1/2$. Recursing on each half with half the agents gives each agent at most $1/n$ of its cost when $n$ is a power of 2, with the same query count as for goods. This is a theorem with the same proof as for the [Even-Paz algorithm](/even-paz-algorithm/), with the inequalities reversed.

**Round-robin for chores.** Fix two agents $i$ and $j$. If $i$ picks before $j$ in each round, each chore of $i$ costs $i$ no more than the chore $j$ takes in the same round. If $j$ picks first, the chore $i$ takes in round $r$ costs $i$ no more than the chore $j$ takes in round $r + 1$, which was still free. In both cases, removing the last chore of $i$ leaves a bundle that costs $i$ no more than the bundle of $j$. So round-robin is envy-free up to one chore for additive costs.

## Bounds

All entries are theorems in the Robertson-Webb model unless stated.

- **Two agents.** Envy-free with 2 queries.
- **Proportional, upper bound.** $O(n \log n)$ queries, by Even-Paz for chores.
- **Proportional, lower bound.** $\Omega(n \log n)$ queries (Farhadi and Hajiaghayi 2017), the chore version of the [Edmonds-Pruhs lower bound](/edmonds-pruhs-lower-bound/). So proportional chore division needs $\Theta(n \log n)$ queries.
- **Envy-free, upper bound.** A bounded protocol for every $n$ (Dehghani, Farhadi, Hajiaghayi and Yami 2018).
- **Envy-free with connected pieces.** Approximately envy-free divisions into intervals can be found with Sperner labels (Su 1999).
- **Indivisible chores.** Envy-free divisions need not exist, by the example with one chore; envy-freeness up to one chore is always possible for additive costs, by round-robin.

## Reductions

- **Goods to chores and back, by reversal.** Proportional protocols carry over directly when every comparison is reversed, as in Even-Paz. Envy-free protocols with trimming do not, because trimming changes value in the other direction.
- **Cake cutting to chore division.** Farhadi and Hajiaghayi relate the two problems closely and use this link to transfer the $\Omega(n \log n)$ lower bound to proportional chore division.
- **Rent division.** Su's treatment of rent as a chore makes [rental harmony](/rental-harmony/) a source of chore division problems, solved by the same Sperner labels.

## Applications

- Housework among housemates, and duty rosters, such as night shifts or on-call times.
- Sharing a cost, such as rent or the cost of a shared service, when the agents see the parts differently.
- Assigning unpleasant tasks in a team, as a problem with indivisible chores.

## References
