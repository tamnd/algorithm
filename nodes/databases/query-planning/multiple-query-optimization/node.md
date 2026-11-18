---
tag: MJSBSF
kind: problem
slug: multiple-query-optimization
name: Multiple-query optimization
aliases:
- multi-query optimization
- MQO
area: databases/query-planning
level: advanced
summary: "Optimize a batch of queries together, so that a subexpression common to several queries is computed once and shared. The problem is NP-hard; practical methods are heuristics."
prereqs: [query-optimization, materialized-view]
see_also: [common-subexpression-elimination, view-selection, hru-greedy-view-selection, cascades-framework, set-cover, a-star-search, greedy-algorithm, np-hard]
sources:
  - paper: "Timos K. Sellis, Multiple-query optimization, ACM Transactions on Database Systems 13(1) (1988), 23 to 52"
    title: Multiple-query optimization
    locator: the problem of choosing one plan for each query of a batch so that the tasks the plans have in common are done once, and exact and heuristic search methods for it
  - paper: "Timos K. Sellis and Subrata Ghosh, On the multiple-query optimization problem, IEEE Transactions on Knowledge and Data Engineering 2(2) (1990), 262 to 266"
    title: On the multiple-query optimization problem
    locator: the complexity of the problem
  - paper: "Prasan Roy, S. Seshadri, S. Sudarshan and Siddhesh Bhobe, Efficient and extensible algorithms for multi query optimization, Proceedings of ACM SIGMOD 2000, 249 to 260"
    title: Efficient and extensible algorithms for multi query optimization
    locator: the AND-OR DAG of the plans of all queries, the cost of materializing and reusing a shared node, and the heuristics Volcano-SH, Volcano-RU and a greedy choice of nodes to materialize, with measurements
---

Multiple-query optimization takes a batch of queries that run together and looks for the plans with the least total cost, where a result that several plans need is computed once and shared. A normal [query optimizer](/query-optimization/) handles one query at a time, so it cannot see that two queries join the same filtered tables. Timos K. Sellis stated the problem in 1988 as the choice of one plan for each query, where the cost of a set of plans counts each shared task once. The problem is [NP-hard](/np-hard/): this page proves it by a reduction from [set cover](/set-cover/), and Sellis and Ghosh (1990) studied its complexity. Prasan Roy, S. Seshadri, S. Sudarshan and Siddhesh Bhobe (2000) put the plans of all queries in one AND-OR DAG, as in the [Cascades](/cascades-framework/) and Volcano optimizers, and chose the shared nodes greedily. Their methods are heuristics with measured gains.

## In plain words

Suppose a report runs ten queries at night, and several of them join this year's orders with the customers. Each query alone would do this join again. It is cheaper to do the join once, keep the result, and let every query read it.

But the best plan for one query alone may not create a result that the others can use. Sometimes each query must take a plan that is a little worse for itself, so that all of them can share one piece of work. Multiple-query optimization looks for the choice of plans for all queries that costs the least in total.

Keeping a shared result also costs something, because it must be written and read again. So sharing pays only when the work saved is larger than this cost.

## Definition

**Input (the model of Sellis).** Queries $Q_1, \ldots, Q_n$. A set $T$ of tasks, each with a cost $c(t) \ge 0$; a task is a subexpression, such as a selection or a join of some relations. For each query $Q_i$, a set $\mathcal{A}_i$ of alternative plans, where each plan is a set of tasks $p \subseteq T$.

**Question.** Choose one plan $p_i \in \mathcal{A}_i$ for each query to minimize the total cost $c(p_1 \cup \cdots \cup p_n) = \sum_{t \in p_1 \cup \cdots \cup p_n} c(t)$. The decision form asks whether there is a choice with total cost at most $K$.

**The DAG model (Roy et al.).** The plans of all queries form one AND-OR DAG: an OR node is a subexpression with its alternative ways to compute it, and an AND node is an operator with its inputs. The answer chooses a plan for each query and a set $M$ of nodes to materialize. A node in $M$ costs its computation plus the cost to write it once, and each use of it costs a read. The first model is the case where sharing is free.

## Variants

- **Batch MQO.** All queries are known at once, as in a nightly report.
- **Shared pipelines.** Share a scan or an operator between queries that run at the same time, without writing the shared result, which saves the write cost but makes the queries wait for each other.
- **Continuous queries.** In a stream system, many standing queries run for a long time, and new ones are added to a shared plan as they arrive.
- **View maintenance.** Several [materialized views](/materialized-view/) are updated from the same changes, and the update expressions share subexpressions.
- **Queries with nested subqueries.** A subquery that is run many times with different values is a batch of similar queries.

## Examples

**Sharing beats the best plan of each query.** Two queries both need the year's orders joined with the customers, $E = \sigma_{\text{year}=2024}(\text{Orders}) \bowtie \text{Customers}$, which costs 100 to compute and 10 more to write and read for sharing.

| query | plan | cost alone |
|---|---|---|
| $Q_1$ | $A$: $E \bowtie \text{Nation}$ | $100 + 20 = 120$ |
| $Q_1$ | $B$: $\sigma(\text{Orders}) \bowtie (\text{Customers} \bowtie \text{Nation})$ | 90 |
| $Q_2$ | $C$: $E \bowtie \text{Lineitem}$ | $100 + 200 = 300$ |
| $Q_2$ | $D$: $(\sigma(\text{Orders}) \bowtie \text{Lineitem}) \bowtie \text{Customers}$ | 280 |

Optimized one at a time, the queries take $B$ and $D$, for $90 + 280 = 370$. The pairs $A, D$ and $B, C$ share nothing and cost 400 and 390. The pair $A, C$ computes $E$ once: $100 + 10 + 20 + 200 = 330$. So the best batch plan uses a plan that is not the best alone for each of the two queries.

**Sharing that does not pay.** If $E$ cost 30 to compute and 40 to write and read, the pair $A, C$ would cost less if each query computed $E$ again on its own, because $2 \cdot 30 < 30 + 40$. A DAG optimizer must compare the two.

## Known algorithms

- **One query at a time, then share.** Optimize each query alone and then share the subexpressions that the chosen plans happen to have in common, as [common subexpression elimination](/common-subexpression-elimination/) does in a compiler. This is fast, but it misses the plans in the example. Roy et al. call their version of this Volcano-SH.
- **Exact search.** Sellis (1988) gave exact methods that search the combinations of plans, with [A* search](/a-star-search/) guided by a lower bound on the cost of the plans still to be chosen, and faster heuristic methods. Exact search takes time exponential in the number of queries in the worst case.
- **Greedy materialization.** Roy et al. (2000) start with no shared nodes and repeatedly add to $M$ the node of the DAG that lowers the total cost most, until no node helps. This is a [greedy algorithm](/greedy-algorithm/) with no proved bound in general; they made it fast with incremental cost updates and report good plans at a small cost in optimization time.
- **Volcano-RU.** Optimize the queries in sequence, and let each one reuse the nodes that earlier queries in the sequence chose to keep.

## Bounds

**MQO is NP-hard (proved).** The decision form is in NP, because a choice of plans can be checked in polynomial time. For hardness, reduce from set cover. Given a universe $U$ and a family $\mathcal{F}$ of subsets of $U$, make a task $t_S$ of cost 1 for each $S \in \mathcal{F}$ and a query $Q_e$ for each $e \in U$, whose plans are the one-task sets $\{t_S\}$ for the sets $S \ni e$.

*Proof that the optimal costs are equal.* A choice of plans picks, for each element $e$, a set that contains $e$, so the chosen sets cover $U$ and their number is the total cost. Conversely, a cover $\mathcal{C}$ gives a choice of plans: for each $e$, pick any set of $\mathcal{C}$ that contains $e$; the union of the tasks has at most $|\mathcal{C}|$ tasks. So the least total cost equals the size of the smallest cover. $\square$

The reduction keeps the cost exactly, and the number of queries is $|U|$. So the hardness of approximating set cover carries over: unless P = NP, no polynomial algorithm approximates MQO in this model within $(1 - \epsilon) \ln n$ for $n$ queries. When each element is in two sets, the same construction is [vertex cover](/vertex-cover/).

**Easy cases.** With no task shared by two queries, the total cost is a sum of separate terms, and optimizing each query alone is optimal. If every plan has one task, as in the reduction, the problem is set cover, and the greedy set cover algorithm is within a factor $H_n \le \ln n + 1$.

## Reductions

- **From set cover and vertex cover.** As above.
- **To view selection.** Choosing nodes to materialize for a batch is close to the [view selection problem](/view-selection/), in which the views are kept for a whole workload and limited by space; the greedy algorithm of Roy et al. has the same form as the [HRU greedy algorithm](/hru-greedy-view-selection/), but the bound $1 - 1/e$ of HRU needs a benefit function with diminishing returns, which MQO costs do not have in general.
- **From single-query optimization.** With $n = 1$, MQO is normal query optimization.

## Applications

- **Batch reports and dashboards.** Many queries over the same fact tables run at the same time.
- **Stream systems.** Shared plans for many standing queries.
- **View maintenance and data loading.** The expressions that update several views share their inputs.
- **Query rewriting inside one query.** A query with a common table expression or a repeated subquery is a small batch, and the same choice of what to materialize applies.

## References
