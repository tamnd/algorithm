---
tag: FSTB0X
kind: problem
slug: coalition-structure-generation
name: Coalition structure generation
aliases:
- optimal coalition structure
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: Partition the players into coalitions so that the sum of coalition values is maximum. Dynamic programming solves it in O(3^n) time.
prereqs: [transferable-utility-game, set-partitions, submask-enumeration]
see_also: [bell-numbers, set-packing, winner-determination-problem, combinatorial-auction, marginal-contribution-nets, hedonic-game, bitmask-dp, np-hard]
sources:
  - paper: doi:10.1016/S0004-3702(99)00036-3
    title: "Tuomas Sandholm, Kate Larson, Martin Andersson, Onn Shehory and Fernando Tohme, Coalition structure generation with worst case guarantees, Artificial Intelligence 111(1-2) (1999), 209-238"
    locator: the NP-hardness of the problem, the search of the two lowest levels of the coalition structure graph as the least search that gives a bound, and the anytime algorithm that lowers the bound
  - paper: doi:10.1007/BF01935053
    title: "D. Y. Yeh, A dynamic programming approach to the complete set partitioning problem, BIT 26(4) (1986), 467-474"
    locator: the dynamic program over subsets in O(3^n) time for complete set partitioning
  - paper: doi:10.1016/j.artint.2015.08.004
    title: "Talal Rahwan, Tomasz P. Michalak, Michael Wooldridge and Nicholas R. Jennings, Coalition structure generation: a survey, Artificial Intelligence 229 (2015), 139-174"
    locator: the survey of exact, anytime and heuristic algorithms, compact representations, and the variants with externalities and constraints
---

Coalition structure generation asks how to split a set of agents into teams so that the teams together produce the most value. Each team, or coalition, has a value given by a characteristic function, and the value of a split is the sum of the values of its coalitions. The problem is the first step of coalition formation in multiagent systems: before the agents divide the payoff of a coalition, they must decide which coalitions to form. The number of splits grows faster than any exponential function, but a dynamic program over subsets finds the best one in $O(3^n)$ time. In terms of the size of the input, which lists $2^n$ values, the problem is in polynomial time, but it is NP-hard when the values are given compactly.

## In plain words

A company has a group of workers and many possible teams. For each possible team, it knows how much that team would earn. Every worker must be in exactly one team, and a worker may also work alone. The company wants the split into teams that earns the most in total. Trying every split is hopeless, because the number of splits explodes as the group grows. A smarter method works one group of workers at a time: the best split of a group is found by choosing the team of its first worker and adding the best split of the rest. Remembering the best split for every group makes this fast enough for about twenty workers. If the earnings are given only for a short list of teams, the input is small, and no method is known that is fast compared with it: the problem is hard.

## Definition

The input is a set $N = \{1, \ldots, n\}$ of agents and a characteristic function $v : 2^N \to \mathbb{R}$ with $v(\emptyset) = 0$, given as a table of $2^n - 1$ numbers. A **coalition structure** is a partition $CS = \{C_1, \ldots, C_k\}$ of $N$ into nonempty, pairwise disjoint coalitions. Its value is

$$V(CS) = \sum_{j = 1}^{k} v(C_j).$$

The task is to find a coalition structure $CS^*$ with the largest value. There is no transfer of payoff between coalitions here; the question of how to divide $v(C)$ among the members of $C$ is separate, and is answered by solutions such as the [core](/core-of-a-cooperative-game/) or the [Shapley value](/shapley-value/).

The number of coalition structures is the Bell number $B_n$, the number of [set partitions](/set-partitions/) of an $n$-element set. $B_n$ grows faster than $c^n$ for every constant $c$, so enumeration is out of the question beyond about 15 agents.

## Variants

- **Anytime with a guarantee.** The algorithm must report, at any time, a structure and a bound $\beta$ such that $V(CS^*) \le \beta\, V(CS)$. This is the setting of Sandholm et al. (1999).
- **Sparse input.** Only some coalitions are listed with a value, and every other coalition is not allowed or has value 0. The input is then small, and the problem is NP-hard.
- **Compact representations.** The function $v$ is given by a short description, such as [marginal contribution nets](/marginal-contribution-nets/), a graph, or skills and tasks. The complexity depends on the representation.
- **Externalities.** In a partition function game, the value of a coalition depends on how the other agents are partitioned.
- **Constraints.** Some coalitions are forbidden, or coalition sizes are bounded.

## Examples

Four agents have the values below.

| coalition | value | coalition | value | coalition | value |
|---|---|---|---|---|---|
| {1} | 3 | {1, 2} | 6 | {1, 2, 3} | 8 |
| {2} | 2 | {1, 3} | 5 | {1, 2, 4} | 7 |
| {3} | 2 | {1, 4} | 4 | {1, 3, 4} | 7 |
| {4} | 1 | {2, 3} | 6 | {2, 3, 4} | 9 |
| | | {2, 4} | 5 | {1, 2, 3, 4} | 10 |
| | | {3, 4} | 4 | | |

There are $B_4 = 15$ coalition structures. Let $f(S)$ be the best value of a partition of $S$. The dynamic program gives $f(\{1, 2\}) = 6$, $f(\{2, 3\}) = 6$, $f(\{2, 4\}) = 5$, $f(\{3, 4\}) = 4$, and $f(\{2, 3, 4\}) = \max(9, 2 + 4, 6 + 1, 5 + 2) = 9$. For the full set, the coalition that contains agent 1 is tried in all 8 ways:

| coalition of agent 1 | value of the rest | total |
|---|---|---|
| {1} | $f(\{2, 3, 4\}) = 9$ | 12 |
| {1, 2} | $f(\{3, 4\}) = 4$ | 10 |
| {1, 3} | $f(\{2, 4\}) = 5$ | 10 |
| {1, 4} | $f(\{2, 3\}) = 6$ | 10 |
| {1, 2, 3}, {1, 2, 4}, {1, 3, 4} | 1, 2, 2 | 9, 9, 9 |
| {1, 2, 3, 4} | 0 | 10 |

The optimum is $\{\{1\}, \{2, 3, 4\}\}$ with value 12, more than the grand coalition with value 10.

## Known algorithms

- **Dynamic programming.** For every nonempty $S \subseteq N$, let $m$ be the smallest agent in $S$ and

  $$f(S) = \max_{m \in C \subseteq S} \big( v(C) + f(S \setminus C) \big), \qquad f(\emptyset) = 0.$$

  Fixing the coalition of the smallest agent counts each partition once. Every pair $C \subseteq S$ is visited at most once, and there are $3^n$ such pairs, because each agent is in $C$, in $S \setminus C$, or outside $S$. So the time is $O(3^n)$ with [submask enumeration](/submask-enumeration/) over bitmasks, and the space is $O(2^n)$. Yeh (1986) gave this algorithm for complete set partitioning, and it was found again for the [winner determination problem](/winner-determination-problem/) of combinatorial auctions.
- **Anytime search with a bound (Sandholm et al. 1999).** Arrange the structures by their number of coalitions. Level 1 is the grand coalition and level 2 has the $2^{n - 1} - 1$ splits into two coalitions. If all values are nonnegative, the best structure in levels 1 and 2 is within a factor $n$ of the optimum. Sandholm et al. showed that searching these $2^{n-1}$ structures is the least search that gives any bound, and gave a schedule of further search that lowers the bound.
- **Search over integer partitions.** Later exact algorithms split the search space by the multiset of coalition sizes and use upper bounds to prune whole subspaces. They are often much faster than dynamic programming in practice; the survey of Rahwan et al. (2015) compares them.
- **Integer programming.** The problem is a set partitioning integer program with one binary variable for each coalition and one equality constraint for each agent.

## Bounds

- **Search space.** There are $B_n$ coalition structures, which is more than exponential in $n$. The dynamic program avoids this by sharing the solutions of subsets.
- **Input size.** With a full table the input has $2^n - 1$ numbers, so $3^n = (2^n)^{\log_2 3}$ is about the input size to the power 1.585. In this sense the full-table problem is in polynomial time.
- **Hardness.** With a sparse or compact input, the problem is [NP-hard](/np-hard/) (Sandholm et al. 1999).
- **The factor $n$ of levels 1 and 2.** Let $CS^*$ have $k \le n$ coalitions, and let $C$ be the one with the largest value, so $v(C) \ge V(CS^*)/k \ge V(CS^*)/n$. The structure $\{C, N \setminus C\}$, or $\{N\}$ if $C = N$, is in level 1 or 2, and with nonnegative values its value is at least $v(C)$. So the best structure in these levels is within a factor $n$.

## Reductions

- **From weighted set packing.** Given sets $T_1, \ldots, T_m$ over a ground set with weights, let the ground elements be the agents, let $v(T_j) = w_j$, and let every other coalition have value 0. A coalition structure of value $W$ gives a packing of the listed sets of weight $W$, and a packing becomes a structure by putting each uncovered element alone. So [weighted set packing](/set-packing/), which is NP-hard, reduces to the sparse problem.
- **Winner determination.** In a combinatorial auction, the items are the agents and the value of a bundle is the highest bid on it. The best allocation of the items is the best coalition structure. So the two problems are the same, and their algorithms transfer.
- **Hedonic games.** In a [hedonic game](/hedonic-game/) each agent has its own utility for each coalition that contains it. A partition that maximizes the sum of the agents' utilities is an optimal coalition structure for $v(C) = \sum_{i \in C} u_i(C)$.

## Applications

Coalition structure generation is used to form teams of agents or robots for tasks, to group sensors, vehicles or ride-sharing customers, and to clear combinatorial auctions. It also appears in clustering, where the value of a cluster replaces the value of a coalition.

## References
