---
tag: E97Y5D
kind: algorithm
slug: bnl-skyline
name: Block-nested-loop skyline
aliases:
- BNL skyline
- block-nested-loops skyline algorithm
- BNL skyline operator
area: systems/database-algorithms
level: advanced
summary: "Skyline by scanning: keep a window of incomparable tuples in memory, spill the overflow to a temporary file, and use timestamps to output tuples once they have met all others."
solves: [pareto-front-computation]
model: comparison-model
complexity:
  vars: {n: the number of tuples, d: the number of dimensions, w: the window size in tuples}
  time: {best: O(d n), worst: O(d n^2)}
  space: {extra: O(w + n)}
properties: {deterministic: true, recursive: false, online: false, external-memory: true}
prereqs: [pareto-dominance, pareto-front-computation, nested-loop-join]
see_also: [sort-filter-skyline, kung-algorithm, non-dominated-sorting, skyline-problem, top-k-query, external-merge-sort]
sources:
  - paper: doi:10.1109/ICDE.2001.914855
    title: Stephan Börzsönyi, Donald Kossmann and Konrad Stocker, The skyline operator, Proceedings of the 17th International Conference on Data Engineering (ICDE 2001), 421 to 430
    locator: the SKYLINE OF clause, the block-nested-loops algorithm (window, temporary file, timestamps, self-organizing window and replacement variants), the divide-and-conquer algorithm and the experiments
  - paper: doi:10.1109/ICDE.2003.1260846
    title: Jan Chomicki, Parke Godfrey, Jarek Gryz and Dongming Liang, Skyline with presorting, Proceedings of the 19th International Conference on Data Engineering (ICDE 2003), 717 to 719
    locator: the comparison of SFS with BNL
  - paper: doi:10.1145/321906.321910
    title: H. T. Kung, F. Luccio and F. P. Preparata, On finding the maxima of a set of vectors, Journal of the ACM 22(4), 469 to 476 (1975)
    locator: the maxima problem in main memory, which the skyline operator extends to large data sets
---

The block-nested-loop (BNL) algorithm computes the *skyline* of a relation: the tuples that no other tuple dominates, where a tuple dominates another if it is at least as good in every chosen attribute and better in at least one. Börzsönyi, Kossmann and Stocker (2001) introduced it with the `SKYLINE OF` clause for SQL. BNL scans the input and keeps a *window* of incomparable candidates in memory. A tuple that a window tuple dominates is dropped; a tuple that dominates window tuples replaces them; and a tuple that does not fit is written to a temporary file for the next pass. Timestamps tell when a window tuple has met every other tuple and can be output. BNL runs in one pass when the skyline fits in memory, and in $O(d n^2)$ time in the worst case. This is the database skyline, the [Pareto front](/pareto-front-computation/) of a set of tuples; it is a different problem from the [skyline problem](/skyline-problem/) of computational geometry, which asks for the outline of a set of buildings.

## In plain words

You look for a hotel that is cheap and near the beach. A hotel is not worth a look if another hotel is both cheaper (or the same price) and nearer (or the same distance), and better in at least one of the two. The skyline is the list of hotels that are left.

Go through the hotels one by one, and keep a short list on a card. If a hotel on the card beats the new one, throw the new one away. If the new one beats hotels on the card, cross them out. If the new hotel is still in, write it on the card, or, if the card is full, on a scrap sheet.

When you are done, start again with the scrap sheet. A hotel on the card is sure once it has been checked against every other hotel.

## The problem

The input is a relation of $n$ tuples and $d$ skyline attributes, each to be minimized. (Negate an attribute to maximize it.) Tuple $p$ *dominates* $q$, written $p \prec q$, if $p_i \le q_i$ for all $i$ and $p_i < q_i$ for some $i$ ([Pareto dominance](/pareto-dominance/)). The output is the skyline: every tuple that no tuple dominates. Equal tuples do not dominate each other, so all copies of a skyline tuple are output. Memory holds a window of $w$ tuples, and the input may be much larger.

## The algorithm

Each tuple in the window or in the temporary file carries a timestamp $ts$, taken from a counter. A window tuple $q$ has met every tuple scanned after it entered. It has not met the tuples written to the temporary file before it entered; it meets them in the next pass, which reads the file in timestamp order.

```pseudo id=main
BNL(input, w)
L1  W ← ∅; T ← the input, each tuple with ts = −1; clock ← 0
L2  while T is not empty do
L3      F ← T; T ← an empty temporary file
L4      for each p in F, in order do
L5          output and remove each q ∈ W with ts(q) < ts(p)          ▷ q has met all tuples
L6          if some q ∈ W dominates p then drop p and go to the next p
L7          remove from W each q that p dominates
L8          if |W| < w then put p in W else append p to T; ts(p) ← clock; clock ← clock + 1
L9      output and remove each q ∈ W that entered before the first write to T in this pass
L10 return the tuples in the order they were output
```

Lines L6 and L7 are one loop over the window. If $p$ is dominated, the loop can stop early, because the window is an antichain: a window tuple that $p$ dominates would then be dominated by another window tuple.

## Example

Hotels as (price, distance), both to be minimized, with a window of $w = 2$:

| hotel | a | b | c | d | e | f | g | h |
|---|---|---|---|---|---|---|---|---|
| (price, distance) | (5, 5) | (4, 6) | (6, 2) | (3, 7) | (5, 4) | (2, 9) | (7, 1) | (6, 6) |

| pass | scanned | action | window after | temporary file |
|---|---|---|---|---|
| 1 | a | enters, ts 0 | a0 | |
| 1 | b | enters, ts 1 | a0, b1 | |
| 1 | c, d | window full: written, ts 2 and 3 | a0, b1 | c2, d3 |
| 1 | e | dominates a, removes it, enters, ts 4 | b1, e4 | c2, d3 |
| 1 | f, g | window full: written, ts 5 and 6 | b1, e4 | c2, d3, f5, g6 |
| 1 | h | dominated by b: dropped | b1, e4 | |
| 1 | end | first write was at 2: **output b** | e4 | |
| 2 | c2 | enters, ts 7 | e4, c7 | |
| 2 | d3 | written, ts 8 | e4, c7 | d8 |
| 2 | f5 | 4 < 5: **output e**; f enters, ts 9 | c7, f9 | d8 |
| 2 | g6 | written, ts 10 | c7, f9 | d8, g10 |
| 2 | end | first write was at 8: **output c** | f9 | |
| 3 | d8 | enters, ts 11 | f9, d11 | |
| 3 | g10 | 9 < 10: **output f**; g enters | d11, g12 | |
| 3 | end | no writes: **output d, g** | | |

The skyline is b, c, d, e, f and g, output in the order b, e, c, f, d, g. Tuple e is output in the middle of pass 2: it entered the window after c and d were written, and once the scan reaches f, which was written after e entered, e has met everything.

## Correctness

A tuple is dropped or removed only when another tuple dominates it, so each skyline tuple survives. The window stays an antichain. The timestamps ensure that two output tuples have always met: one was scanned while the other was in the window, and then neither can dominate the other. If an output tuple $q$ were dominated, a minimal tuple $s$ that dominates $q$ would be in the skyline and would be output, and it would have met $q$, a contradiction. Each pass removes at least one tuple for good, so BNL stops. The full proof is in the proof file.

## Complexity

- **Dominance tests.** Each unordered pair of tuples is tested at most once, so at most $n(n - 1)/2$ tests of $O(d)$ time each: $O(d n^2)$ in the worst case.
- **Best case.** If the window never fills, BNL makes one pass and at most $w$ tests per tuple: $O(d w n)$ time and one scan of the input.
- **Passes and I/O.** Each pass reads its source and writes at most as many tuples. When the skyline is much larger than the window, the number of passes grows to about the skyline size divided by $w$; on anti-correlated data where every tuple is in the skyline, BNL makes $\lceil n / w \rceil$ passes.
- **Space.** $w$ tuples in memory, plus the temporary file.

## Properties

- **Generic.** It needs only a dominance test, so it handles any number of dimensions, `MIN`, `MAX` and `DIFF` attributes, and it works on any input, without indexes or sorting.
- **Not progressive.** No tuple is output before the end of the first pass, because a tuple that enters the window may later be dominated.
- **Order-sensitive.** The cost depends on the input order. If dominating tuples come first, the window holds good tuples and drops most others; if they come last, the window fills with tuples that are later removed. [SFS](/sort-filter-skyline/) fixes this by presorting.
- **Duplicates.** Equal tuples are all kept. Remove duplicates first if the query asks for distinct tuples.

## Variants and improvements

- **Self-organizing window.** Move a window tuple that dominates a scanned tuple to the front of the window, so that strong tuples are tested first.
- **Replacement policy.** When the window is full, replace a window tuple with a new tuple that dominates a larger region, and write the old one to the temporary file instead.
- **[Sort-filter-skyline (SFS)](/sort-filter-skyline/).** Sort the input by a monotone score first; then a window tuple is never dominated, and it can be output at once.
- **LESS.** Godfrey, Shipley and Gryz (2005) combine SFS with an elimination filter in the first pass of the external sort.
- **Divide and conquer.** The same paper gives a divide-and-conquer algorithm on the lines of [Kung, Luccio and Preparata](/kung-algorithm/), better when the skyline is large.
- **Index-based.** With an R-tree, nearest-neighbor and branch-and-bound skyline algorithms output tuples progressively and read only part of the data.

## When to use it

Use BNL when the skyline is small, when no index exists, and when the dimensions are few. It is simple to add to a query engine because it is a scan with a buffer, and it was the first skyline method implemented in database systems. When the skyline is large, use SFS or LESS, which avoid wasted window work, or divide and conquer. For in-memory data in two or three dimensions, sort-based maxima algorithms are much faster.

## Pitfalls

- **Outputting too early.** A window tuple is not final at the moment it enters; it can still be dominated by a later tuple, or by a tuple written to the temporary file before it entered. Use the timestamps.
- **Dominance with ties.** Use "no worse in all and better in one". With "better in all", tuples that tie in one attribute are kept wrongly; with "no worse in all", equal tuples remove each other.
- **Stopping the window loop.** It is safe to stop at the first window tuple that dominates $p$; it is not safe to insert $p$ before every window tuple has been checked.
- **Window size.** The window must hold at least one tuple, and too small a window gives many passes on large skylines.

## Implementations

## History

Kung, Luccio and Preparata studied the maxima of a set of vectors in 1975, in main memory. Börzsönyi, Kossmann and Stocker brought the problem to databases at ICDE 2001 under the name *skyline*, with the `SKYLINE OF` clause, BNL and a divide-and-conquer algorithm for large data. Chomicki, Godfrey, Gryz and Liang added presorting with SFS in 2003, and many index-based and parallel skyline algorithms followed.

## References
