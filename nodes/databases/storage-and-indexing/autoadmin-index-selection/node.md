---
tag: Q7Z4FQ
kind: algorithm
slug: autoadmin-index-selection
name: AutoAdmin index selection
aliases:
- Chaudhuri-Narasayya index tuning
area: databases/storage-and-indexing
level: advanced
summary: "Pick indexes for a workload by finding the best ones for each query, then growing a configuration greedily with what-if costs."
model: word-ram
complexity:
  vars: {q: the number of statements in the workload, n: the number of candidate indexes, m: the size of the exhaustive start, k: the largest number of indexes, P: the number of admissible indexes}
  time: {worst: "O((n^m + k n) q k)", average: "O((n^m + k n) q k)", best: "O(n^m q)"}
  space: {extra: "O(q P)"}
properties: {deterministic: true, exact: false, external: false, online: false, in_place: false, recursive: false}
history:
  year: 1997
  people: [Surajit Chaudhuri, Vivek Narasayya]
  note: "Chaudhuri and Narasayya of Microsoft Research presented the tool at VLDB 1997, as part of the AutoAdmin project. It became the Index Tuning Wizard of Microsoft SQL Server 7.0."
prereqs: [index-selection, what-if-index-analysis, greedy-algorithm]
see_also: [cost-model, query-optimization, covering-index, view-selection, access-path-selection, np-hard, submodular-function, partial-index]
sources:
  - url: http://www.vldb.org/conf/1997/P146.PDF
    title: "Surajit Chaudhuri and Vivek Narasayya, An efficient, cost-driven index selection tool for Microsoft SQL Server, Proceedings of the 23rd International Conference on Very Large Data Bases (VLDB 1997)"
    locator: "pp. 146 to 155: Section 3 (atomic configurations and the reduction of optimizer calls), Section 4 (candidate index selection per query), Section 5 (the Greedy(m, k) enumeration), Section 6 (multi-column indexes and MC-LEAD), Section 7 (experiments with SQL Server 7.0)"
  - paper: doi:10.1145/276304.276337
    title: "Surajit Chaudhuri and Vivek Narasayya, AutoAdmin what-if index analysis utility, Proceedings of ACM SIGMOD 1998"
    locator: pp. 367 to 378, the hypothetical indexes and the optimizer interface that the tool uses for its costs
  - paper: doi:10.1145/984523.984530
    title: "Gregory Piatetsky-Shapiro, The optimal selection of secondary indices is NP-complete, ACM SIGMOD Record 13(2) (1983)"
    locator: pp. 72 to 75, the NP-completeness of optimal index selection
---

AutoAdmin index selection is the algorithm of the index tuning tool that Chaudhuri and Narasayya built for Microsoft SQL Server. Given a workload of queries and updates and a limit $k$ on the number of indexes, it returns a configuration of indexes with a low estimated cost. The [index selection problem](/index-selection/) is NP-hard, so the tool is a heuristic made of three parts. *Candidate selection* treats each query alone as a workload and keeps the indexes of its best configuration. *Configuration enumeration*, Greedy$(m, k)$, searches all configurations of $m$ candidates exhaustively and then adds one index at a time. *Multi-column index generation* builds wider indexes step by step from the narrower ones that were chosen. All costs come from the query optimizer by [what-if calls](/what-if-index-analysis/), and *atomic configurations* let the tool derive most costs without a call.

## In plain words

Suppose you can afford three indexes for a database, and you have a list of the queries that people run. Trying every set of three indexes would take far too many questions to the optimizer. So you first ask, for each query alone, "which indexes would help this query most?" Only those indexes stay in the game.

Then you build the set. You try all pairs of the remaining indexes and keep the best pair. You then add the single index that helps the most, as long as it helps at all and the set is not full. Wide indexes on two columns are tried only if their first column was a good index on its own. Each "how much would this cost?" goes to the optimizer as if the indexes existed, and answers that can be worked out from earlier answers are not asked again.

## The problem

The input is a workload $W$ of $q$ weighted statements, a limit $k$ on the number of indexes, and an optimizer that, for a statement $Q$ and a configuration $C$ of hypothetical indexes, returns the estimated cost $\mathrm{opt}(Q, C)$. The goal is a configuration $C$ with $|C| \le k$ and a small total cost $\mathrm{Cost}(W, C) = \sum_{Q} w_Q \, \mathrm{opt}(Q, C)$. Updates are in the workload, so an index can raise the total cost.

Each optimizer call is expensive, so the tool must make few of them. The problem itself, with its NP-hardness and its known bounds, is on the page on [index selection](/index-selection/). This page is about the AutoAdmin algorithm.

## The algorithm

```pseudo id=main
TUNE(W, k, m, width)
L1  chosen ← ∅; pool ← ∅
L2  for j ← 1 to width do
L3      pool ← pool ∪ the admissible indexes of width j     ▷ width 1: the indexable columns; width j > 1: MC-LEAD
L4      candidates ← chosen; for each statement Q in W do
L5          candidates ← candidates ∪ ENUMERATE({Q}, the indexes of pool that Q can use, k, m)
L6      chosen ← ENUMERATE(W, candidates ∪ chosen, k, m)
```

```pseudo id=enumerate
ENUMERATE(W, S, k, m)                                     ▷ Greedy(m, k)
L7  C ← the configuration of at most m indexes of S with the least Cost(W, C), by exhaustive search
L8  while |C| < k do
L9      i ← the index of S \ C with the least Cost(W, C ∪ {i})
L10     if Cost(W, C ∪ {i}) ≥ Cost(W, C) then stop
L11     C ← C ∪ {i}
L12 return C
```

```pseudo id=cost
L13 opt(Q, C) ← the least opt(Q, A) over the atomic configurations A ⊆ C, each a cached what-if call
```

- **Admissible indexes.** In the first iteration they are the single-column indexes on the indexable columns, those that appear in the predicates of the workload. In iteration $j$, the MC-LEAD rule of the paper forms an index of width $j$ from a chosen index of width $j - 1$ by adding one more column of the workload. So $(a, d)$ is considered only if $(a)$ was chosen.
- **Candidate selection.** A query alone is a workload of one, and the tool runs its own enumeration on it. The indexes of the best configuration for that query become candidates. This prunes the search to indexes that are best for at least one query.
- **Greedy$(m, k)$.** With $m = 0$ it is plain greedy, and with $m = k$ it is exhaustive search over the candidates. The paper reports: "We found that m=2 produced very good solutions" (a measurement on its workloads).
- **Atomic configurations.** An atomic configuration of a query is a set of indexes that one plan of the query can use together. The paper derives the cost of a query in a large configuration as the least cost over its atomic subsets, and limits these subsets (for example, by the number of indexes per table that they may hold) so that few what-if calls are needed. In the optimizer model on this page, a plan uses one index, so the atomic configurations are the single indexes, and the cost of an update is the sum of the maintenance costs of the indexes it changes.

## Example

A table $T$ has 100,000 rows and the columns $a$, $b$, $c$ and $d$ with 1,000, 100, 10 and 50,000 distinct values. A full scan costs 5,000. The workload has three queries and one update, and $k = 2$, $m = 2$, width 2:

| statement | weight | the best single index for it | cost |
|---|---|---|---|
| $Q_1$: $a = ?$, reads $d$ | 50 | $(a, d)$, covering | 8 |
| $Q_2$: $a = ?$ and $b = ?$ | 30 | $(a, b)$, covering | 3.05 |
| $Q_3$: $d$ in a range of 0.1%, reads $c$ | 20 | $(d, c)$, covering | 8 |
| $U$: update of $b$ | 10 | none; 4 more per index that holds $b$ | 1 |

With no index, the total is $100 \cdot 5000 + 10 = 500{,}010$.

1. **Width 1.** The admissible indexes are $(a)$, $(b)$ and $(d)$. Alone, $Q_1$ and $Q_2$ choose $(a)$ (cost 103 each, since about 100 rows match), and $Q_3$ chooses $(d)$ (cost 103). The candidates are $\{(a), (d)\}$, and the enumeration chooses both, with a total of $100 \cdot 103 + 10 = 10{,}310$.
2. **Width 2.** MC-LEAD extends $(a)$ to $(a, b)$, $(a, c)$ and $(a, d)$, and $(d)$ to $(d, a)$, $(d, b)$ and $(d, c)$. Alone, $Q_1$ chooses $(a, d)$, $Q_2$ chooses $(a, b)$, and $Q_3$ chooses $(d, c)$. With the earlier choice, the candidates are $(a)$, $(d)$, $(a, b)$, $(a, d)$ and $(d, c)$.
3. **Enumeration.** With $m = 2 = k$, L7 tries every pair. The best is $\{(a, d), (d, c)\}$, with $50 \cdot 8 + 30 \cdot 103 + 20 \cdot 8 + 10 \cdot 1 = 3{,}660$. The pair $\{(a, b), (d, c)\}$ serves $Q_2$ almost for free but costs $50 \cdot 103$ for $Q_1$ and 5 for each update, a total of 5,451.5.

An exhaustive search over every configuration of at most two indexes of width at most 2 also gives 3,660, so here the tool finds the optimum. It made 21 what-if calls. The search costed 84 distinct pairs of a statement and a configuration, so without atomic configurations it would have needed 84 calls.

**Measurement.** On 200 random instances with two tables and 3 to 7 statements (seeds 0 to 199, $k = 3$, $m = 2$, width 2), the tool found the optimum of the exhaustive search on 94 instances. The median ratio of its cost to the optimum was 1.008, and the worst was 16.6. On average it made 25.6 what-if calls against 168.3 distinct statement and configuration pairs. With $m = 0$ it found the optimum on 93 instances and with $m = 3$ on 95.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). The main points:

- **Exact costs (theorem).** In a model where a plan uses the indexes of one atomic configuration, the cost of a query in any configuration is the least cost over its atomic subsets. So the derived costs equal the optimizer's costs, and the cache changes no value.
- **Bounded calls (theorem).** With single-index atomic configurations, the tool makes at most $q (P + 1)$ what-if calls.
- **Greedy$(m, k)$ (theorem).** The result has at most $k$ indexes, is at least as good as every configuration of at most $m$ candidates, and, if it has fewer than $k$ indexes, no single candidate lowers its cost. With $m \ge k$ it is the optimum over the candidates.
- **No optimality (heuristic).** The tool can miss the optimum. An index that is second best for two queries but serves both is never a candidate, and MC-LEAD never forms $(e, c)$ if $(e)$ was not chosen. Both cases occur in the measurement above: the worst instance needed $(e, c)$ for two queries whose best single indexes were $(c)$ and $(b)$.

## Complexity

- **Enumeration.** L7 costs $\sum_{r \le m} \binom{n}{r} = O(n^m)$ configurations, and the loop at most $k n$ more. Each configuration is costed over $q$ statements, with up to $k$ cached look-ups each.
- **Candidate selection** runs the enumeration once per statement, on the few indexes that the statement can use.
- **What-if calls** are the real cost, since each is an optimizer call. They are at most $q (P + 1)$ with single-index atomic configurations, and the paper's limits on atomic configurations keep them small in general.
- **Space.** The cache of what-if costs, $O(q P)$ entries.

## Properties

- **Deterministic.** Ties are broken by a fixed order of the indexes.
- **Not exact.** It is a heuristic for an NP-hard problem; its results are at least as good as no index and locally best for one added index.
- **Optimizer-driven.** It uses the optimizer's own cost estimates, so it chooses indexes that the optimizer will in fact use. Errors in the estimates become errors in the choice.
- **Offline.** It needs the workload in advance, as a trace or a sample.

## Variants and improvements

- **Database Engine Tuning Advisor.** The successor tool in later versions of SQL Server also chooses materialized views and partitionings, with the same candidate selection and enumeration ideas ([view selection](/view-selection/)).
- **Space limit.** A limit on storage instead of on the number of indexes; the greedy step then compares benefit per unit of space, as on the [index selection](/index-selection/) page.
- **Workload compression.** Large traces are reduced to a sample of representative statements before tuning.
- **Integer programming.** Later tools solve the enumeration exactly over the candidates, with the same what-if costs.

## When to use it

Use this approach to recommend indexes for a known workload, when the optimizer can cost hypothetical indexes and when the number of indexable columns is too large for exhaustive search. It is the pattern of most commercial and open-source index advisors. If the workload is not known in advance, adaptive methods such as [database cracking](/database-cracking/) build indexes as queries arrive. If the workload is small, an exhaustive search or an integer program over the candidates is affordable and exact.

## Pitfalls

- **Pruned candidates.** Candidate selection keeps only the best indexes of each query. A shared index that is second best for many queries is lost. Widening the per-query search to the best few configurations reduces this.
- **The leading column.** MC-LEAD builds wide indexes only on chosen narrow ones. If the useful leading column was not chosen at width 1, the wide index is never tried.
- **Bad estimates.** The tool trusts the optimizer's [cardinality estimates](/cardinality-estimation/). If they are wrong, it can choose indexes that are useless at run time. Check a recommendation on real runs.
- **Updates.** A workload without its updates makes every index look free. Include the inserts, updates and deletes, with their real weights.
- **Many what-if calls.** Without atomic configurations and a cache, the number of optimizer calls grows with the number of configurations, not with the number of indexes, and the tool becomes too slow.

## Implementations

## History

Surajit Chaudhuri and Vivek Narasayya of the AutoAdmin project at Microsoft Research presented the tool at VLDB 1997, and it shipped as the Index Tuning Wizard of SQL Server 7.0. Their SIGMOD 1998 paper described the what-if interface that lets the optimizer cost indexes that do not exist. Earlier work had shown that optimal index selection is NP-complete (Comer, 1978; Piatetsky-Shapiro, 1983), and had often used cost models apart from the optimizer. The AutoAdmin tool made the optimizer itself the cost model, which most later index advisors do too.

## References
