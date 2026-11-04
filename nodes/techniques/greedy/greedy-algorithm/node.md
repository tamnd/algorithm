---
tag: M75C3A
kind: technique
slug: greedy-algorithm
name: Greedy algorithm
aliases:
- greedy method
- greedy strategy
area: techniques/greedy
level: intro
summary: Build a solution by repeatedly making the locally best choice without reconsidering it.
prereqs: [optimal-substructure]
see_also: [greedy-choice-property, exchange-argument, greedy-stays-ahead, matroid-greedy-theorem, activity-selection, huffman-coding, greedy-set-cover, local-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 15, Greedy Algorithms
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 4, Greedy Algorithms
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Sections 16.4 and 16.5, Matroids and greedy methods, A task-scheduling problem as a matroid
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 4, The Greedy Method
---

A greedy algorithm builds a solution one piece at a time, and at each step adds the piece that looks best by a simple local rule, without ever undoing a choice. It is fast, usually one sort or one priority queue, and for many problems it is exactly optimal: interval scheduling, minimum spanning trees, Huffman codes, fractional knapsack and single-machine scheduling rules. For other problems the same idea fails, so a greedy algorithm needs a proof. The standard proofs are the [exchange argument](/exchange-argument/), [greedy stays ahead](/greedy-stays-ahead/), and the [matroid greedy theorem](/matroid-greedy-theorem/), which explains exactly when the "take the best item that still fits" rule works.

## In plain words

A greedy algorithm makes a series of choices. At each step it takes what looks best right now, by one fixed rule, and it never goes back to change an earlier choice.

This is often how people solve everyday problems. A cashier gives change with the largest coin that fits. A student with many short tasks does the one that is due first. Sometimes this is the best possible plan, and sometimes it is not.

The hard part of a greedy algorithm is not the code, which is usually short. The hard part is to choose the right rule and to prove that it gives the best answer. For many rules that seem natural, a small example shows that they fail.

## When it applies

A greedy algorithm is exact when the problem has two properties.

- **Greedy choice.** Some optimal solution contains the choice that the greedy rule makes first. This is the [greedy choice property](/greedy-choice-property/). It lets the algorithm commit to the choice without checking other options.
- **Optimal substructure.** After the first choice, what remains is a smaller instance of the same problem, and an optimal solution of it, together with the first choice, is optimal for the whole instance. See [optimal substructure](/optimal-substructure/).

Dynamic programming also needs optimal substructure, but it tries all choices and keeps the best. A greedy algorithm tries one. So when both apply, greedy is faster, and when the greedy choice property fails, dynamic programming is the usual fallback.

Signs that a greedy algorithm may work: the objective is a sum or a maximum of independent contributions; a swap of two adjacent pieces changes the cost in a simple local way; or the feasible sets have the exchange property of a [matroid](/matroid/). Signs that it may fail: a choice can block several later choices at once, as in the 0-1 [knapsack problem](/knapsack-problem/).

## The template

```pseudo id=main
GREEDY(I)
L1  C ← the candidates of instance I                        ▷ hole: what a candidate is
L2  S ← the empty partial solution
L3  while C is not empty and S is not complete do
L4      x ← a candidate of C that is best by the greedy key   ▷ hole: the key
L5      remove x from C
L6      if S ∪ {x} is feasible then                         ▷ hole: the feasibility test
L7          S ← S ∪ {x}
L8          update the keys of C that depend on S           ▷ hole: dynamic keys, often none
L9  return S
```

**Filling the holes.** If the keys do not change, line L4 is a scan of the candidates sorted once by the key, and the algorithm costs one sort plus $n$ feasibility tests. If the keys change when $S$ grows, as in Prim's and Dijkstra's algorithms or in Huffman's construction, line L8 is a priority queue update, and the cost is $O(n \log n)$ heap operations. Line L6 can be an expensive test (independence in a matroid) or a trivial one (always true for Huffman's merges).

**Proving the result optimal.** The template does not prove anything. Pick one of these routes.

1. *Exchange argument.* Take any optimal solution and change it, one swap at a time, into the greedy solution without making it worse. See [exchange argument](/exchange-argument/).
2. *Greedy stays ahead.* Show by induction that after each step the greedy partial solution is at least as good as the first steps of any other solution, by a suitable measure. See [greedy stays ahead](/greedy-stays-ahead/).
3. *Matroid structure.* Show that the feasible sets form a matroid and the objective is a sum of element weights; then the greedy algorithm by weight is optimal by the [matroid greedy theorem](/matroid-greedy-theorem/).
4. *Bound by a certificate.* Find a lower or upper bound that every solution obeys, and show that the greedy solution reaches it. For [interval partitioning](/interval-partitioning/), the depth of the intervals is such a bound.

## Classic examples

| problem | greedy key | proof route |
| --- | --- | --- |
| [activity selection](/activity-selection/) | [earliest finish time](/earliest-finish-time-first/) | stays ahead |
| [interval partitioning](/interval-partitioning/) | earliest start, any free resource | bound by the depth |
| [fractional knapsack](/fractional-knapsack/) | largest value per weight | exchange |
| [Huffman coding](/huffman-coding/), [optimal merge pattern](/optimal-merge-pattern/) | merge the two smallest | exchange and induction |
| [minimum spanning tree](/minimum-spanning-tree/) by [Kruskal](/kruskal/) | lightest edge without a cycle | matroid, or the [cut property](/cut-property/) |
| [shortest paths](/dijkstra/) with nonnegative weights | nearest unsettled vertex | stays ahead |
| [Smith's rule](/smith-rule/) for $\sum w_j C_j$ | largest $w_j / p_j$ | adjacent exchange |
| [minimizing maximum lateness](/minimizing-maximum-lateness/) | earliest due date | adjacent exchange |
| [minimizing the number of late jobs](/minimizing-number-of-late-jobs/) | due date, drop the longest | induction with a stronger invariant |
| [job sequencing with deadlines](/job-sequencing-with-deadlines/) | largest profit that still fits | matroid |
| change-making with a [canonical coin system](/canonical-coin-system/) | largest coin that fits | depends on the coins |
| [optimal tape storage](/optimal-tape-storage/) | shortest file first | adjacent exchange |

## Variations

- **Sort once or keep a heap.** Static keys need one sort. Keys that change with the partial solution need a priority queue.
- **Best-in and worst-out.** Instead of adding the best candidate, start with everything and remove the worst one that can be removed. For minimum spanning trees this is the [reverse-delete](/reverse-delete/) algorithm; on matroids both forms are optimal.
- **Greedy as an approximation.** When the greedy rule is not exact, it often has a provable ratio. Greedy [set cover](/greedy-set-cover/) is within a factor of about $\ln n$, and the better of the greedy integer part and the single most valuable item is within a factor 2 for the 0-1 knapsack problem.
- **Online greedy.** In an [online algorithm](/online-algorithm/), each choice must be made when the input arrives, and a greedy rule is often the natural choice. Its quality is then measured by a competitive ratio.
- **Greedy then improve.** A greedy solution is a good start for [local search](/local-search/), which then makes improving changes.

## Pitfalls

- **No proof.** A natural rule can fail. For activity selection, "shortest interval first", "earliest start first" and "fewest conflicts first" all fail on small examples. Always test against brute force on small random inputs, and then prove.
- **The wrong key.** For $\sum w_j C_j$, sorting by $p_j$ or by $w_j$ is wrong; the key is the ratio $w_j / p_j$. For the 0-1 knapsack problem, sorting by value per weight is not optimal at all.
- **A close relative is not greedy.** The fractional knapsack is greedy and the 0-1 knapsack is not. Coins $1, 5, 10, 25$ are greedy and coins $1, 3, 4$ are not. Change one detail of a problem and check the proof again.
- **Ties.** A proof that assumes distinct keys can break when keys are equal. Either handle ties in the proof or show that all tie orders give the same value.
- **Feasibility only checked locally.** Line L6 must test the whole set $S \cup \{x\}$, not only $x$ against the last element added, unless the problem guarantees that this is enough, as for intervals sorted by finish time.

## Exercises

1. Coins $1, 3, 4$: find the smallest amount for which the greedy rule (largest coin first) does not use the fewest coins, and show that the greedy choice property fails for it.
2. A car with a tank range $R$ drives along a road with gas stations at positions $x_1 < x_2 < \cdots < x_n$, starting full at position 0, with consecutive stations at most $R$ apart. Show that stopping at the farthest station reachable on the current tank minimizes the number of stops. Which proof route fits?
3. Give an independence system and nonnegative weights for which "take the heaviest element that still fits" is not optimal. Then explain how your example violates the exchange property of a matroid.
4. For 0-1 knapsack, show that the greedy rule by value per weight can be arbitrarily bad, but that, when every item fits alone, the better of its result and the most valuable single item is at least half of the optimum.

## References
