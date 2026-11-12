---
tag: QEVP9Z
kind: problem
slug: view-selection
name: View selection problem
aliases:
- materialized view selection
- data cube view selection
area: systems/database-algorithms
level: advanced
summary: "Choose which views to materialize so that a query workload runs fastest within a budget. In the data cube lattice, greedy gets at least 1 - 1/e of the best benefit."
prereqs: [materialized-view]
see_also: [index-selection, materialized-view, view-maintenance, group-by-aggregation, query-optimization, cost-model, hash-aggregation, selinger-join-enumeration]
sources:
  - paper: doi:10.1145/233269.233333
    title: Venky Harinarayan, Anand Rajaraman and Jeffrey D. Ullman, Implementing data cubes efficiently, Proceedings of ACM SIGMOD 1996, 205 to 216
    locator: the lattice framework and the linear cost model, the greedy algorithm, the bound of 1 - (1 - 1/k)^k (at least 63 percent) on its benefit, and the space-constrained variant
  - paper: "George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14 (1978), 265 to 294"
    title: An analysis of approximations for maximizing submodular set functions I
    locator: the greedy algorithm reaches 1 - (1 - 1/k)^k of the maximum of a monotone submodular function over sets of size k
  - paper: "Himanshu Gupta, Selection of views to materialize in a data warehouse, Proceedings of ICDT 1997, LNCS 1186, 98 to 112"
    title: Selection of views to materialize in a data warehouse
    locator: AND-OR view graphs that generalize the lattice, and greedy algorithms with performance guarantees for them
  - paper: "Himanshu Gupta, Venky Harinarayan, Anand Rajaraman and Jeffrey D. Ullman, Index selection for OLAP, Proceedings of ICDE 1997, 208 to 219"
    title: Index selection for OLAP
    locator: the joint selection of views and indexes on the data cube with greedy algorithms
  - paper: "Surajit Chaudhuri and Vivek Narasayya, An efficient, cost-driven index selection tool for Microsoft SQL Server, Proceedings of VLDB 1997, 146 to 155"
    title: An efficient, cost-driven index selection tool for Microsoft SQL Server
    locator: the use of the optimizer's cost estimates for hypothetical physical structures in a greedy search
---

The view selection problem asks which [materialized views](/materialized-view/) to store so that a workload of queries runs as fast as possible, subject to a budget: a number of views, a space limit, or a limit on the cost of [maintaining](/view-maintenance/) them. Its best known form is for the data cube, where Harinarayan, Rajaraman and Ullman (1996) organized the possible GROUP BY views in a lattice, charged each query the size of the smallest stored view that can answer it, and showed that a simple greedy algorithm gets at least $1 - (1 - 1/k)^k > 1 - 1/e \approx 0.63$ of the best possible benefit with $k$ views. It is the sister problem of [index selection](/index-selection/): both choose physical structures for a workload under a budget, using cost estimates from the optimizer.

## In plain words

A sales table can be summed by product, by store, by customer, or by any group of these. Each summary is a possible stored view. Storing all of them would take too much space, and storing none makes each question read the whole table.

A small summary can be computed from a bigger one that groups by more columns. So a stored summary helps every question whose grouping it covers. The task is to pick a few summaries that help the most questions the most. A simple method works well: pick the summary that saves the most work now, add it, and repeat. This method always gets at least about two thirds of the best possible saving.

## Definition

**The lattice model** (Harinarayan, Rajaraman and Ullman 1996).

- A finite set of views with a *dependency* order: $w \preceq v$ if a query on $w$ can be answered from $v$. For the data cube, the views are the subsets of the dimensions (the GROUP BY attributes), and $w \preceq v$ if $w \subseteq v$. A top view answers everything (the base data, or the full GROUP BY) and is always materialized.
- Each view $v$ has a size $|v|$ (its number of rows), and each view $w$ is queried with a frequency $f(w) \ge 0$.
- **Linear cost model.** For a set $S$ of materialized views (with the top), a query on $w$ costs $C_S(w) = \min\{|v| : v \in S,\ w \preceq v\}$: it scans the smallest stored view that can answer it.
- The *benefit* of $S$ is $B(S) = \sum_w f(w)\,(C_{\emptyset}(w) - C_S(w))$, the saving against storing only the top view.

**Problem.** Given $k$, find a set $S$ of at most $k$ views (besides the top) with the largest benefit $B(S)$.

## Variants

- **Space budget.** Replace "at most $k$ views" by $\sum_{v \in S} |v| \le$ a space limit; the greedy algorithm then picks the largest benefit per unit of space.
- **Maintenance budget.** Limit the total cost of maintaining the chosen views under the update stream; the benefit is then no longer submodular, and greedy loses its guarantee.
- **General view graphs.** AND-OR graphs (Gupta 1997) allow a view to be computed from several views together, for example a join view from its inputs, not only from one ancestor.
- **Views and indexes together.** Choose views and indexes on them in one budget (Gupta et al. 1997).
- **Workload-driven design tools.** Commercial tuning advisors choose views and [indexes](/index-selection/) for a recorded workload, with the optimizer's cost model in place of the linear model.

## Examples

**A three-dimensional cube.** The dimensions are part ($p$), supplier ($s$) and customer ($c$). The eight views and their sizes in rows are $psc$: 6M (the top), $pc$: 6M, $ps$: 0.8M, $sc$: 6M, $p$: 0.2M, $s$: 0.01M, $c$: 0.1M, and the empty grouping (none): 1. Each view is queried once. With only the top view, each query reads 6M rows, so the total cost is 48M.

| round | chosen view | queries that benefit | benefit | total cost after |
|---|---|---|---|---|
| 1 | $ps$ | $ps$, $p$, $s$, none: $4 \cdot (6\text{M} - 0.8\text{M})$ | 20.8M | 27.2M |
| 2 | $c$ | $c$: $6\text{M} - 0.1\text{M}$; none: $0.8\text{M} - 0.1\text{M}$ | 6.6M | 20.6M |
| 3 | $s$ | $s$: $0.8\text{M} - 0.01\text{M}$; none: $0.1\text{M} - 0.01\text{M}$ | 0.88M | 19.72M |

The views $pc$ and $sc$ have benefit 0, because they are as large as the top. Here greedy is optimal for $k = 1, 2, 3$; a brute force search over all sets confirms it.

**Greedy is not always optimal.** Take a top $T$ of size 100, a view $M$ of size 50 that can answer four views $L_1, \ldots, L_4$, and two views $A$ and $B$ of size 40, where $A$ answers $L_1, L_2$ and $B$ answers $L_3, L_4$. Each $L_i$ has size 40 and each view is queried once. With $k = 2$, greedy first takes $M$ (benefit $5 \cdot 50 = 250$, against $3 \cdot 60 = 180$ for $A$), then $A$ (benefit $60 + 2 \cdot 10 = 80$), for a total of 330. The best pair is $\{A, B\}$, with $6 \cdot 60 = 360$. The ratio $330/360 = 11/12$ is above the guarantee $1 - (1/2)^2 = 3/4$.

## Known algorithms

- **Greedy** (Harinarayan, Rajaraman and Ullman 1996). Start with the top view; $k$ times, add the view $v$ with the largest marginal benefit $\sum_{w \preceq v} f(w) \max(0,\ C_S(w) - |v|)$. With $m$ views and the dependency relation given, each round takes $O(m^2)$ time, so $O(k m^2)$ in all.

```pseudo id=main
GREEDY-VIEWS(views, sizes, frequencies, top, k)
L1  S ← {top}
L2  repeat k times
L3      for each view v not in S do
L4          B(v) ← Σ over w ⪯ v of f(w) · max(0, C_S(w) − |v|)
L5      v* ← the view with the largest B(v)
L6      S ← S ∪ {v*}
L7  return S
```

- **Greedy by benefit per unit space** for a space budget.
- **Exhaustive search** over all sets of $k$ views, $O(\binom{m}{k} m^2)$, for small lattices; for a cube with $d$ dimensions there are $m = 2^d$ views.
- **AND-OR graph greedy** (Gupta 1997) and **A* search** or randomized search when the benefit is not submodular, as under a maintenance budget.
- **What-if optimization.** Physical design tools ask the optimizer for the cost of each query under hypothetical views and indexes, and run a greedy or a search over the candidates, as in index selection (Chaudhuri and Narasayya 1997).

## Bounds

**Greedy guarantee.** In the lattice model with the linear cost, the greedy benefit with $k$ views is at least $1 - (1 - 1/k)^k$ times the optimum, and this is more than $1 - 1/e \approx 0.632$ for every $k$. Proof: for one query $w$, the saving $C_{\emptyset}(w) - C_S(w)$ is the largest of the savings of the chosen views that can answer $w$, and a maximum of nonnegative weights over a growing set is monotone and *submodular* (adding a view to a larger set gains no more than adding it to a smaller set). So $B$ is monotone submodular. Let $O$ be an optimal set of $k$ views and $G_i$ the greedy set after $i$ rounds. Then $B(O) \le B(G_i \cup O) \le B(G_i) + \sum_{o \in O} (B(G_i \cup \{o\}) - B(G_i)) \le B(G_i) + k\,(B(G_{i+1}) - B(G_i))$, since greedy takes the largest marginal gain. So the gap $B(O) - B(G_i)$ shrinks by a factor $1 - 1/k$ each round, and after $k$ rounds it is at most $(1 - 1/k)^k B(O)$. This is the theorem of Nemhauser, Wolsey and Fisher (1978) for monotone submodular functions.

**Hardness.** The problem is NP-hard, so no polynomial algorithm is expected to find the optimum in general. For the general class of monotone submodular maximization with a cardinality constraint, $1 - 1/e$ is the best ratio that a polynomial number of value queries can guarantee (Nemhauser and Wolsey 1978).

**Space budget.** With a space limit in place of a count, greedy by benefit per unit space is close to the same guarantee when every view is small compared with the space limit; Harinarayan, Rajaraman and Ullman give a bound that degrades with the ratio of the largest view size to the space limit.

## Reductions

- **Facility location.** The lattice problem is a maximum-coverage type facility location problem: views are facilities, queries are clients, and each client is served by the cheapest open facility that can serve it. The greedy guarantee for such problems applies.
- **Index selection** has the same shape: choose structures within a budget to minimize workload cost, with costs from the optimizer. Interactions between indexes (one index makes another useless, or two indexes are only useful together) can break submodularity, which is why its tools use heuristics with fewer guarantees.
- **Query answering using views** is the inner step: to compute the benefit of a candidate view, the system must know which queries can be rewritten to use it; see [materialized view](/materialized-view/).

## Applications

OLAP servers and data warehouses precompute selected aggregates of the data cube so that roll-up queries read small tables. Database tuning advisors recommend materialized views and indexes for a recorded workload. The same greedy method selects precomputed results in caches and in big data systems that reuse intermediate results across jobs.

## References
