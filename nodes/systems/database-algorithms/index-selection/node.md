---
tag: BFQ09A
kind: problem
slug: index-selection
name: Index selection problem
aliases:
- index selection problem
area: systems/database-algorithms
level: advanced
summary: "Choose a set of indexes that fits in a space budget and minimizes the estimated cost of a workload, updates included. NP-hard; tools use greedy search over optimizer estimates."
prereqs: [cost-model, knapsack-problem, np-hard]
see_also: [view-selection, query-optimization, max-coverage, set-cover, submodular-function, greedy-algorithm, clustered-index, covering-index]
sources:
  - paper: doi:10.1145/320289.320296
    title: "Douglas Comer, The difficulty of optimum index selection, ACM Transactions on Database Systems 3(4) (1978)"
    locator: pp. 440 to 445; optimum index selection for a file is NP-complete, by a reduction from 3-satisfiability
  - url: http://www.vldb.org/conf/1997/P146.PDF
    title: "Surajit Chaudhuri and Vivek Narasayya, An efficient, cost-driven index selection tool for Microsoft SQL Server, Proceedings of VLDB 1997"
    locator: pp. 146 to 155; Section 2 (the problem with a bound k on the number of indexes, costs from the optimizer), Section 3 (atomic configurations), Section 4 (candidate selection per query) and Section 5 (the Greedy(m, k) enumeration)
  - paper: doi:10.1145/276304.276337
    title: "Surajit Chaudhuri and Vivek Narasayya, AutoAdmin what-if index analysis utility, SIGMOD 1998"
    locator: pp. 367 to 378; hypothetical indexes and the optimizer's cost estimates for them
  - paper: doi:10.1007/BF01588971
    title: "George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14 (1978)"
    locator: the bound 1 - 1/e for the greedy maximization of a monotone submodular function under a cardinality constraint
---

The index selection problem asks which indexes to build on a database for a given workload. Each candidate index makes some queries cheaper, costs space, and makes the updates of the workload more expensive. The goal is a set of indexes, the *configuration*, that fits in a space budget and minimizes the total estimated cost of the workload. The problem is NP-hard, as Comer showed in 1978. Physical design tools solve it with a greedy search over candidate indexes, and they get the cost of each query under each configuration from the query optimizer, by "what-if" calls that pretend the indexes exist (Chaudhuri and Narasayya, 1997 and 1998). It is the sister problem of [view selection](/view-selection/), which chooses materialized views instead of indexes.

## In plain words

A kitchen has room for a few gadgets. A garlic press saves time on some recipes, a food processor on others, and a stand mixer on still others. Each gadget takes counter space and must be cleaned after use. You know the meals you cook in a usual week. Which gadgets should you keep so that the week's work is smallest?

Two gadgets that do the same job do not help twice. A big gadget that saves a lot can block two small ones that together save more. Because of this, there is no fast method that always finds the best choice, and real tools use good guesses that they check with the database's own cost estimates.

## Definition

**Input.**

- A workload: queries and updates $q_1, \ldots, q_r$, with weights $w_q$ (how often each runs).
- Candidate indexes $I_1, \ldots, I_n$, each with a size $s_i > 0$ and a maintenance cost $m_i \ge 0$, the extra cost of the workload's updates when $I_i$ exists.
- A cost function $\mathrm{Cost}(q, S)$, the cost of query $q$ when the indexes $S$ exist. In practice the query optimizer computes it.
- A space budget $b$.

**Output.** A configuration $S \subseteq \{I_1, \ldots, I_n\}$ with $\sum_{i \in S} s_i \le b$ that minimizes

$$\mathrm{Total}(S) = \sum_q w_q\, \mathrm{Cost}(q, S) + \sum_{i \in S} m_i .$$

The *benefit* of $S$ is $\mathrm{Total}(\emptyset) - \mathrm{Total}(S)$; minimizing the total is the same as maximizing the benefit.

**The single-index model.** If each query uses at most one index, then $\mathrm{Cost}(q, S) = \min(c_q, \min_{i \in S} c_{q,i})$, where $c_q$ is the cost with no index and $c_{q,i}$ the cost with index $I_i$ alone. Chaudhuri and Narasayya call the sets of indexes that one query can use together *atomic configurations*; for a query that uses one index, the cost under $S$ is the minimum over its atomic configurations in $S$. The implementation on this page uses this model, with the optimizer's estimates given as a table.

## Variants

- **Bound on the number of indexes.** Choose at most $k$ indexes, as in Chaudhuri and Narasayya (1997). This is the budget with $s_i = 1$.
- **Index interactions.** A query can use two indexes together (index intersection, or an index on each side of a join). Then $\mathrm{Cost}(q, S)$ is a minimum over subsets of $S$, and the benefit is no longer a sum over single indexes.
- **Clustered index choice.** At most one index per table can be [clustered](/clustered-index/), which adds a matroid constraint per table.
- **Online and adaptive tuning.** The workload changes over time, and indexes are created and dropped as it changes. [Database cracking](/database-cracking/) avoids the choice by building indexes as a side effect of queries.
- **Views and indexes together.** Choose materialized views and indexes in one search, since an index on a view competes for the same space. [View selection](/view-selection/) is the version for views alone.

## Examples

**Greedy by benefit per space is not optimal.** Three queries, each run once, cost 10, 8 and 8 with no index. Index A (size 6) makes the first cost 1, index B (size 5) the second, index C (size 5) the third. The budget is 10.

| configuration | size | total cost | benefit | benefit per unit of size |
|---|---|---|---|---|
| none | 0 | 26 | 0 | |
| {A} | 6 | 17 | 9 | 1.5 |
| {B} or {C} | 5 | 19 | 7 | 1.4 |
| {B, C} | 10 | 12 | 14 | |

Greedy takes A first, since its ratio 1.5 is the largest. Then neither B nor C fits in the remaining 4 units, so greedy stops at a total of 17. The optimum is {B, C}, with total 12. This is the [knapsack](/knapsack-problem/) trap: one large item blocks two smaller items worth more.

**A database case.** A table $T(a, b, c)$ and a workload of three queries, each with cost 100 by a full scan. Every index costs 10 per unit of workload in maintenance, and the budget is 10.

| query | weight | with index on $a$ (size 4) | with index on $(a, b)$ (size 6) | with index on $c$ (size 4) |
|---|---|---|---|---|
| $a = ?$ | 50 | 3 | 3 | 100 |
| $a = ?$ and $b = ?$ | 30 | 10 | 2 | 100 |
| $c$ in a range | 20 | 100 | 100 | 20 |

With no index the total is $50 \cdot 100 + 30 \cdot 100 + 20 \cdot 100 = 10{,}000$. Alone, the indexes give 2,460 for $a$, 2,220 for $(a, b)$ and 8,410 for $c$. Benefit per unit of size: $7540/4 = 1885$ for $a$, $7780/6 \approx 1297$ for $(a, b)$, $1590/4 = 397.5$ for $c$. Greedy takes $a$, then $c$ (its gain is still 1,590, while $(a, b)$ now gains only 230), and stops at $\{a, c\}$ with total $150 + 300 + 400 + 20 = 870$. The optimum is $\{(a, b), c\}$: $150 + 60 + 400 + 20 = 630$. The index on $(a, b)$ serves the first query as well as the index on $a$ does, so it is the better first choice, but its ratio is lower. Even with a budget of 14, which fits all three, the optimum leaves out $a$: it would save nothing next to $(a, b)$ and cost 10 to maintain.

## Known algorithms

**Exhaustive search.** Try every configuration within the budget, $O(2^n)$ calls of the cost function. It is exact and is used for small candidate sets, and inside Greedy$(m, k)$ for the first $m$ indexes.

**Greedy by benefit per space.**

```pseudo id=main
GREEDY(W, b)
L1  S ← ∅
L2  loop
L3      for each candidate index i ∉ S do
L4          if size(S) + s_i > b then skip i
L5          gain_i ← Total(S) − Total(S ∪ {i});  ratio_i ← gain_i / s_i
L6          keep the i with the largest ratio among those with gain_i > 0
L7      if no i was kept then return S
L8      S ← S ∪ {i}
```

It makes $O(n^2)$ calls of the cost function. Chaudhuri and Narasayya's Greedy$(m, k)$ starts from the best configuration of $m$ indexes, found by exhaustive search, and then adds one index at a time while the cost falls, up to $k$ indexes. Since a call of the cost function is a call of the optimizer, the tool also reduces the candidates first: for each query it picks the best indexes for that query alone, and only those enter the search. Multi-column indexes are built up step by step, from the best single-column ones.

**What-if optimization.** The optimizer is asked for the plan and cost of a query as if a hypothetical index existed. Only the statistics and the metadata of the index are created, not the index itself, so the tool can evaluate thousands of configurations without building any of them.

**Integer programming.** In the single-index model, the problem is a facility location problem with a knapsack constraint: variables $x_i$ for the chosen indexes and $y_{q,i}$ for the index that query $q$ uses, with $\sum_i y_{q,i} \le 1$ and $y_{q,i} \le x_i$. Solvers find exact optima for moderate sizes.

## Bounds

- **NP-hardness.** Comer (1978) proved a form of optimum index selection NP-complete by a reduction from [3-SAT](/3-sat/). The reductions below show it again in the model of this page: the problem is NP-hard even with no interactions between indexes, and NP-hard in the strong sense even with unit sizes.
- **Approximation, unit sizes.** With no maintenance costs, the benefit in the single-index model is $B(S) = \sum_q w_q \max(0, \max_{i \in S}(c_q - c_{q,i}))$, a facility location function. It is monotone and [submodular](/submodular-function/): adding an index to a larger set saves less, because the larger set already serves some queries well. So greedy with a bound $k$ on the number of indexes has benefit at least $(1 - 1/e)$ times the optimum, by the theorem of Nemhauser, Wolsey and Fisher (1978). Since max coverage is a special case, no polynomial algorithm does better unless P = NP (Feige, 1998).
- **Approximation, sizes.** With sizes, greedy by ratio alone can be arbitrarily bad: with one index of size 1 and benefit 2, one of size $b$ and benefit $b$, and budget $b$, greedy takes the first and then has no room for the second, a benefit of 2 against $b$. Taking the better of greedy and the best single index gives at least half of the optimum benefit when benefits add up (the knapsack case); for submodular benefits with sizes, partial enumeration plus greedy gives $1 - 1/e$ (Sviridenko, 2004).
- **No guarantee with maintenance.** With maintenance costs, the benefit can drop when an index is added, as in the example with budget 14, and the guarantees above do not hold. The guarantees are also for the benefit, not for the total cost, which can be far from optimal in ratio even when the benefit is close.

## Reductions

- **From knapsack.** Given items with values $v_j$ and sizes $s_j$ and a capacity $b$, make query $j$ with weight 1 and cost $v_j$ without an index, and index $I_j$ of size $s_j$ that makes query $j$ cost 0 and helps no other. The benefit of a configuration is the value of the items chosen, so an optimal configuration is an optimal knapsack packing. Knapsack is NP-hard, so index selection is.
- **From max coverage.** Given a universe of $r$ elements, sets $T_1, \ldots, T_n$ and a number $k$, make a query of cost 1 for each element and an index of size 1 for each set, which makes the queries of its elements cost 0. The benefit of a configuration of $k$ indexes is the number of elements covered by the $k$ sets. [Max coverage](/max-coverage/) is NP-hard in the strong sense, since it contains [set cover](/set-cover/) as a decision problem, so index selection is strongly NP-hard even with unit sizes.
- **To view selection.** An index is a materialized view of a table, sorted on its key, so index selection is a special case of the selection of views and indexes together.

## Applications

- Physical design tools of commercial systems, which recommend indexes and materialized views from a recorded workload, starting with the AutoAdmin index tuning tool for Microsoft SQL Server.
- Automatic and continuous tuning in cloud databases, which add and drop indexes as the workload changes, and validate each change against the measured costs.
- Manual physical design: textbooks such as Ramakrishnan and Gehrke give rules of thumb for the choice of indexes, of the clustered index and of composite keys that make [covering indexes](/covering-index/), and the problem on this page is the formal version of that choice.

## References
