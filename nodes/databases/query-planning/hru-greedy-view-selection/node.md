---
tag: TY6PHM
kind: algorithm
slug: hru-greedy-view-selection
name: HRU greedy view selection
aliases:
- Harinarayan-Rajaraman-Ullman algorithm
- greedy cube materialization
area: databases/query-planning
level: advanced
summary: "Choose views of a data cube lattice one at a time by largest benefit. The greedy benefit is at least (e - 1)/e, about 63 percent, of the optimal benefit, for a fixed number k of views."
solves: [view-selection]
model: word-ram
complexity:
  vars: {n: the number of views in the lattice, k: the number of views to choose}
  time: {worst: "O(k n^2)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, greedy: true, recursive: false}
history:
  year: 1996
  people: [Venky Harinarayan, Anand Rajaraman, Jeffrey D. Ullman]
  note: Given at SIGMOD 1996 with the lattice framework for data cubes and the bound 1 - (1 - 1/k)^k.
prereqs: [view-selection, submodular-function]
see_also: [nemhauser-wolsey-fisher-theorem, data-cube, materialized-view, greedy-algorithm, max-coverage, set-cover, index-selection, group-by-aggregation]
sources:
  - paper: doi:10.1145/233269.233333
    title: Venky Harinarayan, Anand Rajaraman and Jeffrey D. Ullman, Implementing data cubes efficiently, Proceedings of ACM SIGMOD 1996, 205 to 216
    locator: "Section 3.2 (the linear cost model and the reduction from set cover), Section 4.1 and Fig. 6 (the benefit and the greedy algorithm), Examples 4.1 and 4.2 (Figs. 7 and 9), Section 4.3 (Theorem 4.1, the bound 1 - (1 - 1/k)^k, and Theorem 4.2 for benefit per unit space), Section 4.5 (query frequencies)"
  - paper: "George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14 (1978), 265 to 294"
    title: An analysis of approximations for maximizing submodular set functions I
    locator: the greedy algorithm reaches 1 - (1 - 1/k)^k of the maximum of a monotone submodular function over sets of size k
  - paper: "Himanshu Gupta, Selection of views to materialize in a data warehouse, Proceedings of ICDT 1997"
    title: Selection of views to materialize in a data warehouse
    locator: the extension of the greedy method and its guarantee from the cube lattice to AND-OR view graphs
---

The HRU greedy algorithm chooses which views of a data cube to store. Harinarayan, Rajaraman and Ullman gave it in 1996. The possible GROUP BY views form a lattice: a view can answer every view that groups by fewer attributes. A query costs the size of the smallest stored view that can answer it. The algorithm stores the top view, then adds $k$ more views. Each time it takes the view that lowers the total cost the most. The greedy benefit is at least $1 - (1 - 1/k)^k$ times the optimal benefit, and this is more than $(e - 1)/e \approx 0.63$. The [view selection](/view-selection/) page states the general problem, its budgets and its relation to [index selection](/index-selection/). This page holds the algorithm itself, the full proof of both bounds of the paper, the examples of the paper, and code.

## In plain words

A sales table can be summed by part, by supplier, by customer, or by any group of these. Each of these summaries is a view, and a summary by more columns can produce a summary by fewer columns. The full table can produce all of them. If a summary is not stored, a question about it reads the smallest stored summary that can produce it.

The algorithm starts with only the full table stored. In each round, it looks at each summary that is not stored. It adds up how much work that summary would save, over all the questions it could answer. It stores the one that saves the most, and repeats. Each choice is good now but may not be best for all rounds. Even so, the total saving is always at least about 63 percent of the best possible saving with the same number of summaries.

## The problem

The input is a set of views with a top view $t$, a relation $w \preceq v$ (view $w$ can be answered from view $v$), a size $|v|$ for each view, and a number $k$. In the cube on attribute set $A$, the views are the subsets of $A$, $w \preceq v$ means $w \subseteq v$, and $t = A$. In the linear cost model of the paper, answering $w$ from a stored set $S$ costs

$$C_S(w) = \min\{|u| : u \in S,\ w \preceq u\},$$

the number of rows of the smallest stored view that can answer it. The top view is always stored. The goal is a set of $k$ views besides $t$ that minimizes $\sum_w C_S(w)$, or with query frequencies $q_w$, $\sum_w q_w C_S(w)$. The paper shows that this problem is NP-complete even in this simple model, by a reduction from [set cover](/set-cover/).

## The algorithm

The benefit of a view $v$ for the current set $S$ is the drop in total cost when $v$ is added:

$$B(v, S) = \sum_{w \preceq v} q_w \max\big(0,\ C_S(w) - |v|\big).$$

```pseudo id=main
GREEDY(views V with top t, sizes |v|, weights q_w, number k)
L1  S ← {t}
L2  for i ← 1 to k do
L3      for each view v not in S, compute B(v, S) = the sum over w ⪯ v of q_w · max(0, C_S(w) - |v|)
L4      choose a view v not in S with the largest B(v, S)
L5      S ← S ∪ {v}
L6  return S - {t}, in the order of choice
```

The code keeps $C_S(w)$ for every view $w$ and lowers it after each choice, so line L3 never recomputes the minimum over $S$. For a space limit instead of a count, the variant picks the view with the largest $B(v, S)/|v|$ in line L4.

## Example

This is Example 4.1 of the paper. The lattice has eight views with these sizes: $a = 100$ (the top), $b = 50$, $c = 75$, $d = 20$, $e = 30$, $f = 40$, $g = 1$, $h = 10$. View $a$ answers $b$ and $c$; $b$ answers $d$ and $e$; $c$ answers $e$ and $f$; $d$ answers $g$; $e$ answers $g$ and $h$; $f$ answers $h$; and the relation is transitive. With only $a$ stored, each of the eight views costs 100, a total of 800. Take $k = 3$.

| view | round 1 | round 2 | round 3 |
|---|---|---|---|
| b | **250** | | |
| c | 125 | 50 | 25 |
| d | 160 | 60 | **60** |
| e | 210 | 60 | 50 |
| f | 120 | **70** | |
| g | 99 | 49 | 49 |
| h | 90 | 40 | 30 |

In round 1, $b$ improves itself and the four views below it ($d$, $e$, $g$, $h$) from 100 to 50 each, a benefit of 250. In round 2, $f$ lowers its own cost from 100 to 40 and the cost of $h$ from 50 (through $b$) to 40, a benefit of $60 + 10 = 70$. In round 3, $d$ improves itself and $g$ from 50 to 20, a benefit of 60. The greedy choice is $b$, $f$ and $d$, with benefit $250 + 70 + 60 = 380$ and total cost 420. A search over all 35 sets of three views shows that 380 is the best possible, so greedy is optimal here.

Greedy is not always optimal. In Example 4.2 of the paper, the top view has size 200, and three views $b$, $c$ and $d$ below it have sizes 100, 99 and 100. Four chains of 20 views of size 100 hang below them: $b$ answers chains 1 and 2, $c$ chains 2 and 3, $d$ chains 3 and 4. With $k = 2$, greedy first takes $c$, with benefit $41 \cdot 101 = 4141$, and then $b$ or $d$, with benefit 2100, for a total of 6241. The set $\{b, d\}$ has benefit $82 \cdot 100 = 8200$. The ratio is about 0.761, close to the bound $3/4$ for $k = 2$.

## Correctness

The proof file proves both results of the paper. The core fact is that the total benefit $f(X)$ of a set $X$ of views is a monotone [submodular function](/submodular-function/): adding other views can only lower $C_S(w)$, so it can only lower the benefit of a view. Then the argument of [Nemhauser, Wolsey and Fisher](/nemhauser-wolsey-fisher-theorem/) applies. If $O$ is an optimal set of $k$ views and $G_i$ the greedy set after $i$ rounds, the views of $O$ together add at most $k$ times the best single benefit, so the gap to the optimum shrinks by a factor of at least $1 - 1/k$ in each round. After $k$ rounds the gap is at most $(1 - 1/k)^k$ of the optimum.

**Theorem 1 (Theorem 4.1 of the paper).** With $k$ views, $B_{greedy} \ge (1 - (1 - 1/k)^k)\, B_{opt}$, and the bound is tight. For $k = 2$ it is $3/4$, and it decreases toward $(e - 1)/e$ as $k$ grows.

**Theorem 2 (Theorem 4.2 of the paper, as proved here).** If greedy picks by benefit per unit space and has used space $s$, its benefit is at least $1 - 1/e$ of the best benefit of any set of views with total size at most $s$. The same proof works with any query weights.

## Complexity

Let $n$ be the number of views. The sets of views below each view take $O(n^2)$ space. Line L3 costs $O(n)$ per view, so $O(n^2)$ per round, and the update of $C_S$ after line L5 costs $O(n)$. The total is $O(k n^2)$ time. For the cube on $d$ attributes, $n = 2^d$ and the view on a set $A$ has $2^{|A|}$ views below it, so one round costs $3^d$ steps. The sizes of the views are inputs; in practice they are estimated, for example by sampling or by a sketch for the number of distinct groups, which can cost more than the greedy search.

## Properties

- **Approximation, proved.** At least $1 - (1 - 1/k)^k > 0.63$ of the optimal benefit, for every lattice and every $k$. This is about the benefit (the saving over storing only the top view), not about the total cost.
- **Tight.** The paper shows lattices with ratio arbitrarily close to the bound; for $k = 2$, close to $3/4$.
- **Exact for $k = 1$.** The first choice is the best single view.
- **Nonincreasing gains.** By submodularity, each round gains no more than the round before.
- **Deterministic.** With a fixed tie rule, the same input gives the same choice.

## Variants and improvements

- **Query frequencies.** With a weight $q_w$ per query, the benefit sums $q_w \max(0, C_S(w) - |v|)$, and the bound stays the same (Section 4.5 of the paper).
- **Space limit.** Pick by benefit per unit space. The bound $1 - 1/e$ holds against the best use of the space that greedy has used. Against a fixed limit, a view that does not fit can make plain greedy arbitrarily bad, so a practical version also compares with the best single view that fits.
- **Views and indexes.** Gupta, Harinarayan, Rajaraman and Ullman (1997) extended the greedy method to choose indexes on the views together with the views.
- **AND-OR view graphs.** Gupta (1997) generalized the lattice to graphs in which a view can be computed from several others, with greedy algorithms that keep a guarantee.
- **Maintenance cost.** When the budget is the time to [maintain](/view-maintenance/) the views, the constraint is not a count or a space limit, and the proofs of this page do not carry over.

## When to use it

Use it to choose which aggregates of a star schema or a [data cube](/data-cube/) to precompute, when query costs are roughly proportional to the size of the view read. It is easy to implement, and the guarantee holds for any sizes. When the cost model has indexes, joins or maintenance costs, use it as a heuristic inside a cost-based tool that uses the optimizer's estimates, as in index selection.

## Pitfalls

- **Reading the bound as a bound on the cost.** The 63 percent is about the benefit, the saving over the top view alone. When the best saving is small compared with the cost of the top view, 63 percent of it says little about the total cost.
- **Forgetting the top view.** The top view must always be stored, or some queries cannot be answered. It is not one of the $k$ views.
- **Stale costs.** After each choice, $C_S(w)$ must be lowered for every view below the new view. Using the costs of the first round makes greedy pick overlapping views, such as $b$ and $e$ in the example.
- **Bad size estimates.** The algorithm is only as good as the sizes. The size of a view grouped by several attributes is often much smaller than the product of the numbers of values, and estimating it is a [distinct values](/distinct-elements-problem/) problem.
- **A fixed space limit.** See the variant above: picking by benefit per unit space and skipping what does not fit has no guarantee.

## Implementations

## History

Gray et al. proposed the data cube operator in 1996, and it raised the question of which parts of the cube to precompute. In the same year Venky Harinarayan, Anand Rajaraman and Jeffrey D. Ullman organized the views as a lattice, used the TPC-D benchmark as a running example, and gave the greedy algorithm with its bounds; the paper refers to a full version of 1995 for the proofs. Their analysis is a case of the bound of Nemhauser, Wolsey and Fisher (1978) for monotone submodular functions. Later work by Gupta and by Gupta, Harinarayan, Rajaraman and Ullman extended the method to indexes and to general view graphs.

## References
