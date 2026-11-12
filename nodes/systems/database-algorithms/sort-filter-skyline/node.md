---
tag: 6QMS6V
kind: algorithm
slug: sort-filter-skyline
name: Sort-filter-skyline
aliases:
- SFS
- SFS skyline algorithm
- skyline with presorting
area: systems/database-algorithms
level: advanced
summary: "Skyline by presorting on a monotone score such as entropy, then one window filter: a tuple that no window tuple dominates is in the skyline and is output at once."
solves: [pareto-front-computation]
model: comparison-model
complexity:
  vars: {n: the number of tuples, d: the number of dimensions, w: the window size in tuples}
  time: {best: O(n log n + d n), worst: O(n log n + d n^2)}
  space: {extra: O(w + n)}
properties: {deterministic: true, recursive: false, online: false, external-memory: true}
prereqs: [pareto-dominance, bnl-skyline, external-merge-sort]
see_also: [kung-algorithm, non-dominated-sorting, pareto-front-computation, skyline-problem, top-k-query, topological-sort]
sources:
  - paper: doi:10.1109/ICDE.2003.1260846
    title: Jan Chomicki, Parke Godfrey, Jarek Gryz and Dongming Liang, Skyline with presorting, Proceedings of the 19th International Conference on Data Engineering (ICDE 2003), 717 to 719
    locator: the SFS algorithm, the presort by a monotone function, the entropy score, and the comparison with BNL
  - paper: "Jan Chomicki, Parke Godfrey, Jarek Gryz and Dongming Liang, Skyline with presorting: Theory and optimizations, Intelligent Information Processing and Web Mining (IIS 2005), Advances in Soft Computing, Springer, 595 to 604"
    locator: the proofs that a topological presort makes every window tuple a skyline tuple, and the optimizations of the window
  - paper: "Parke Godfrey, Ryan Shipley and Jarek Gryz, Maximal vector computation in large data sets, Proceedings of the 31st International Conference on Very Large Data Bases (VLDB 2005)"
    locator: the analysis of BNL, SFS and LESS, and the average case under independent attributes
  - paper: doi:10.1109/ICDE.2001.914855
    title: Stephan Börzsönyi, Donald Kossmann and Konrad Stocker, The skyline operator, Proceedings of the 17th International Conference on Data Engineering (ICDE 2001), 421 to 430
    locator: the block-nested-loops algorithm that SFS improves
---

Sort-filter-skyline (SFS) computes the skyline of a relation, the tuples that no other tuple dominates, by first sorting the tuples by a monotone score and then running one window filter like [BNL](/bnl-skyline/). Chomicki, Godfrey, Gryz and Liang (2003) observed that after such a sort, no tuple is dominated by a later one. So a tuple that survives the window is in the skyline for certain: it is output at once and never leaves the window. This makes SFS *progressive*, removes the timestamps of BNL, and makes the number of passes exactly $\lceil |S| / w \rceil$ for a skyline $S$ and a window of $w$ tuples. As for BNL, this is the database skyline, the [Pareto front](/pareto-front-computation/) of the tuples, not the building outline of the [skyline problem](/skyline-problem/).

## In plain words

You look for a hotel that is cheap and near the beach. A hotel is out if another one is no worse on both and better on one.

First, sort the hotels by a single number that mixes price and distance, such as their sum, with the best numbers first. Now a hotel that beats another one always comes before it in the list.

Go down the sorted list with a short card. If a hotel on the card beats the new hotel, throw the new one away. If not, the new hotel is a winner for sure: nothing later can beat it. Write it on the card and announce it.

When the card is full, put the hotels that are still in on a scrap sheet, and start again with an empty card.

## The problem

The input is a relation of $n$ tuples and $d$ skyline attributes, each to be minimized. Tuple $p$ *dominates* $q$, written $p \prec q$, if $p_i \le q_i$ for all $i$ and $p_i < q_i$ for some $i$ ([Pareto dominance](/pareto-dominance/)). The output is the skyline $S$: every tuple that no tuple dominates, with all copies of equal tuples. Memory holds a window of $w$ tuples.

## The algorithm

A score $s$ is *monotone* if $p \prec q$ implies $s(p) \le s(q)$. Sorting by such a score gives a [topological order](/topological-sort/) of the dominance relation, once ties are broken in a way that agrees with dominance (for example by comparing the tuples in lexicographic order). Chomicki and coauthors recommend the *entropy* score $E(p) = \sum_i \ln(1 + p_i)$ for attributes scaled to $[0, 1]$; the sum also works.

```pseudo id=main
SFS(input, w, s)
L1  T ← the input sorted by (s(p), p), smallest first          ▷ a topological order of ≺
L2  while T is not empty do
L3      F ← T; T ← an empty temporary file; W ← ∅
L4      for each p in F, in order do
L5          if some q ∈ W dominates p then drop p and go to the next p
L6          if |W| < w then put p in W and output p          ▷ p is in the skyline
L7          else append p to T
L8  return the tuples in the order they were output
```

The window is emptied between passes. This is safe: every tuple in $T$ was compared with the whole window when it was written, because the window does not change once it is full.

## Example

Hotels as (price, distance), both to be minimized, with a window of $w = 2$ and $s = $ sum:

| hotel | a | b | c | d | e | f | g | h |
|---|---|---|---|---|---|---|---|---|
| (price, distance) | (5, 5) | (4, 6) | (6, 2) | (3, 7) | (5, 4) | (2, 9) | (7, 1) | (6, 6) |
| sum | 10 | 10 | 8 | 10 | 9 | 11 | 8 | 12 |

The sorted order is c, g, e, d, b, a, f, h (ties by the tuple: (6, 2) before (7, 1), and (3, 7) before (4, 6) before (5, 5)).

| pass | scanned | action | window |
|---|---|---|---|
| 1 | c, g | enter: **output c, g** | c, g |
| 1 | e, d, b, a, f | window full: written | c, g |
| 1 | h | dominated by c: dropped | c, g |
| 2 | e, d | enter: **output e, d** | e, d |
| 2 | b | window full: written | e, d |
| 2 | a | dominated by e: dropped | e, d |
| 2 | f | window full: written | e, d |
| 3 | b, f | enter: **output b, f** | b, f |

The skyline is c, g, e, d, b and f, found in $\lceil 6 / 2 \rceil = 3$ passes. Each tuple is output the moment it enters the window. BNL needs timestamps for the same data, and outputs nothing before the end of its first pass.

## Correctness

If $p \prec q$, then $p$ comes before $q$ in the sorted order. Suppose a tuple $p$ enters the window but some tuple dominates it; take a dominator $r$ that is itself in the skyline. Then $r$ comes before $p$. Either $r$ entered the window earlier in this pass or an earlier one, and then $p$ was compared with it and dropped; or $r$ was written to the temporary file because the window was full, and then the window was still full when $p$ came. Both are impossible, so each window tuple is in the skyline. Skyline tuples are never dropped, and each pass moves at least one tuple into the window, so every skyline tuple is output exactly once. The full proof is in the proof file.

## Complexity

- **Sort.** $O(n \log n)$ comparisons in memory, or an [external merge sort](/external-merge-sort/) on disk; the sort can be free if the data already comes in a suitable order.
- **Dominance tests.** Each pair is tested at most once, so at most $n(n - 1)/2$ tests of $O(d)$ time: $O(d n^2)$ in the worst case, when the skyline is large.
- **Passes.** Exactly $\lceil |S| / w \rceil$ filter passes. In particular, if the skyline fits in the window, one pass suffices, unlike BNL, whose window can fill with tuples that later turn out to be dominated.
- **Average case.** For $n$ tuples with independent, continuous attributes, the expected skyline size is $\Theta((\ln n)^{d-1} / (d - 1)!)$, so for fixed $d$ the filter does $O(n (\ln n)^{d-1})$ tests on average. Godfrey, Shipley and Gryz showed that the sort then dominates, and that LESS reduces the total to $O(d n)$ on average.

## Properties

- **Progressive.** Skyline tuples are output as the scan reaches them, so the first results come right after the sort.
- **No window replacement.** A window tuple is never dominated, so the window only grows within a pass and needs no timestamps.
- **Good window contents.** A score like entropy puts tuples that dominate a large region early, so the window holds strong filters and drops most tuples quickly.
- **Generic.** Any monotone score and any number of dimensions work. Attributes to maximize are negated or reversed.

## Variants and improvements

- **[BNL](/bnl-skyline/).** The same filter without the presort; it needs timestamps and can waste window space.
- **LESS.** Godfrey, Shipley and Gryz (2005) keep an elimination-filter window of strong tuples during the first pass of the external sort, so dominated tuples are dropped before they are sorted.
- **SaLSa.** Bartolini, Ciaccia and Patella sort by a score that also allows stopping before the end of the input, once a tuple seen so far dominates every tuple that is still to come.
- **Projection.** Keep only the skyline attributes and a pointer in the window, so that more tuples fit.
- **[Kung's algorithm](/kung-algorithm/) and [non-dominated sorting](/non-dominated-sorting/)** are main-memory methods for the same problem; sort-based sweeps are the best choice for two or three dimensions.

## When to use it

Use SFS when the skyline must be computed by a query engine over data that does not fit in memory and no index helps. The presort is a normal sort operator, and the filter is a simple scan with a buffer, so SFS fits a pipelined plan, and it can feed tuples to the next operator early. It beats BNL when the skyline is large compared with the window or when the input order is bad for BNL. When an R-tree exists, index-based skyline algorithms can avoid reading most of the data.

## Pitfalls

- **Non-monotone scores.** A score such as the product of the attributes fails for negative values; a score that is not monotone breaks the presort, and SFS then outputs dominated tuples.
- **Ties in the score.** Tuples with the same score must be ordered so that a dominating tuple comes first, for example by the tuple itself. With rounded floating-point scores, two tuples where one dominates the other can get the same score.
- **Entropy domain.** $\ln(1 + x)$ needs $x > -1$; scale the attributes to $[0, 1]$ first.
- **Clearing the window.** The window must be emptied between passes. If the full window is kept, no tuple of the next pass can enter it, and the loop never ends. The old window tuples are of no use there, because every tuple of the temporary file was already compared with them.

## Implementations

## History

Chomicki, Godfrey, Gryz and Liang presented SFS at ICDE 2003 as an answer to the order sensitivity of BNL, with the entropy score. An extended version with proofs and optimizations followed in 2005, the same year in which Godfrey, Shipley and Gryz analyzed BNL, SFS and their new LESS algorithm. Later sort-based algorithms, such as SaLSa, keep the SFS idea and add early stopping.

## References
