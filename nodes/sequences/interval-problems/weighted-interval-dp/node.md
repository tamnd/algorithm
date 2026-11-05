---
tag: YZT11N
kind: algorithm
slug: weighted-interval-dp
name: Weighted interval scheduling dynamic programming
aliases:
- Weighted interval DP with binary search predecessors
area: sequences/interval-problems
level: core
summary: Sort by finish time, compute predecessors, and use the recurrence OPT(j)=max(OPT(j-1), w_j+OPT(p(j))).
solves: [weighted-interval-scheduling]
model: comparison-model
complexity:
  vars: {n: the number of intervals}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [weighted-interval-scheduling, binary-search, optimal-substructure, tabulation]
see_also: [activity-selection, earliest-finish-time-first, memoization, traceback, dag-dynamic-programming, k-machine-interval-scheduling, segmented-least-squares, knapsack-problem]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 6.1, Weighted Interval Scheduling, A Recursive Procedure (the recurrence, p(j), memoization and Find-Solution), and Section 6.2 (the iterative version)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.1, An activity-selection problem (the unit weight case and its dynamic programming formulation)
---

The weighted interval DP solves [weighted interval scheduling](/weighted-interval-scheduling/): it sorts the intervals by right end, finds for each interval $j$ the number $p(j)$ of intervals that end in time for it, and fills the table $\mathrm{OPT}(j) = \max(\mathrm{OPT}(j - 1), w_j + \mathrm{OPT}(p(j)))$. The sort and the binary searches for $p(j)$ take $\Theta(n \log n)$ time, the table takes $\Theta(n)$, and a backward walk over the table recovers an optimal set. The recurrence is correct because, in this order, the intervals compatible with $j$ among the earlier ones are exactly the first $p(j)$, a prefix. The end point type enters only in $p(j)$: an interval that ends at $l_j$ counts for half-open and open intervals and not for closed ones.

## In plain words

Line the intervals up by where they end. Walk through them in that order and write down, for each one, the best total weight you can get using only the intervals seen so far.

For the next interval there are two choices. Skip it, and the best total stays as it was. Or take it, and add its weight to the best total among the intervals that end before it starts. All those intervals come at the front of the line, so one quick search finds how many there are. Keep the larger of the two choices.

At the end, walk back through the table to see which choice was made at each step.

## The problem

The input is a list of $n$ intervals $\langle l_j, r_j \rangle$ of one type with weights $w_j > 0$. The output is a set of pairwise disjoint intervals of largest total weight. Closed intervals that share an end point meet, so they cannot both be chosen; half-open and open intervals that share an end point are disjoint, as shown on the [problem page](/weighted-interval-scheduling/).

## The algorithm

```pseudo id=main
WEIGHTED-INTERVAL(I[1 .. n])               ▷ half-open [l, r): r_i ≤ l_j means "ends in time"
L1  sort I by r ascending
L2  for j ← 1 to n do p[j] ← |{ i : I[i].r ≤ I[j].l }|   ▷ binary search; closed: I[i].r < I[j].l
L3  M[0] ← 0
L4  for j ← 1 to n do
L5      M[j] ← max(M[j − 1], w_j + M[p[j]])
L6  S ← ∅, j ← n
L7  while j > 0 do
L8      if w_j + M[p[j]] ≥ M[j − 1] then S ← S ∪ {j}, j ← p[j]
L9      else j ← j − 1
L10 return (M[n], S)
```

Line L2 counts, in the sorted array of right ends, the entries that are at most $l_j$, an upper bound search, or less than $l_j$ for closed intervals, a lower bound search. These intervals all come before $j$ in the order, as the correctness section shows. $M[j]$ is the best weight using only the first $j$ intervals. Lines L6 to L9 retrace the choices: if taking $j$ is at least as good as skipping it, take it and jump to $p[j]$, else skip it.

## Example

The six intervals of the [problem page](/weighted-interval-scheduling/), sorted by right end by line L1:

| $j$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| interval | $a$ $(0, 3)$ | $c$ $(1, 5)$ | $b$ $(3, 6)$ | $d$ $(5, 8)$ | $e$ $(6, 9)$ | $f$ $(8, 10)$ |
| $w_j$ | 2 | 5 | 4 | 3 | 4 | 2 |
| $p[j]$, closed | 0 | 0 | 0 | 1 | 2 | 3 |
| $M[j]$, closed | 2 | 5 | 5 | 5 | 9 | 9 |
| $p[j]$, half-open | 0 | 0 | 1 | 2 | 3 | 4 |
| $M[j]$, half-open | 2 | 5 | 6 | 8 | 10 | 10 |

The touches change $p$: $b$ starts at 3 where $a$ ends, so $p[3] = 1$ for half-open intervals and 0 for closed ones, and in the same way $d$, $e$ and $f$ each gain one predecessor.

*Closed, traceback.* At $j = 6$, $2 + M[3] = 7 < M[5] = 9$, skip $f$. At $j = 5$, $4 + M[2] = 9 \ge M[4] = 5$, take $e$ and jump to $j = 2$. At $j = 2$, $5 + M[0] = 5 \ge M[1] = 2$, take $c$. The result is $\{c, e\}$, weight 9.

*Half-open, traceback.* At $j = 6$, $2 + M[4] = 10 \ge M[5] = 10$, take $f$, jump to 4. Take $d$, since $3 + M[2] = 8 \ge M[3] = 6$, jump to 2, and take $c$. The result is $\{c, d, f\}$, weight 10. The other optimum $\{a, b, e\}$ is found if line L8 prefers skipping on ties.

## Correctness

Two facts make the recurrence right. First, in the order of line L1 the intervals before $j$ that are disjoint from $I_j$ are exactly the first $p[j]$: an earlier interval ends no later than $I_j$, so it is disjoint from $I_j$ only if it ends before $I_j$ starts, and those intervals form a prefix of the order. Second, an optimal set for the first $j$ intervals either skips $j$, and then it is optimal for the first $j - 1$, or takes $j$, and then the rest lies in that prefix of length $p[j]$ and is optimal there. The traceback keeps the invariant that $w(S) + M[j] = M[n]$ and every chosen interval is disjoint from the first $j$ intervals. The [proof](proofs/correctness.md) gives the details.

## Complexity

- **Time.** The sort of line L1 takes $\Theta(n \log n)$ comparisons. Line L2 does $n$ binary searches, $O(n \log n)$. Lines L3 to L9 take $\Theta(n)$, since each pass of the loop of line L7 lowers $j$ by at least one. The total is $\Theta(n \log n)$ in every case, because of the sort.
- **Space.** $\Theta(n)$ for the sorted order and the arrays $p$ and $M$.
- **Lower bound.** $\Omega(n \log n)$ in the algebraic decision tree model, even with unit weights, as shown on the [problem page](/weighted-interval-scheduling/). So the algorithm is optimal there.

## Properties

- **Exact and deterministic.** It returns an optimal set for any positive weights, real or integer.
- **Two cases per step.** Each entry depends on two earlier entries, so the subproblem graph has $2n$ edges, which is why the table costs only $O(n)$ after the $p[j]$ are known.
- **Order of right ends.** Any order of intervals with equal right ends works, because $p[j]$ counts only intervals that end strictly before $r_j$.
- **The whole table is needed.** $M[p[j]]$ can reach far back, so the table cannot be cut to a few entries, unlike recurrences that look only one or two steps back.

## Variants and improvements

- **Memoized recursion.** Compute $\mathrm{OPT}(n)$ by recursion with a table of known values, as in Kleinberg and Tardos. Without the table the recursion can take exponential time, for example when $p(j) = j - 2$ for all $j$, where the number of calls grows like the Fibonacci numbers.
- **Linear time on sorted input.** If the intervals come sorted by right end and also by left end, compute all $p[j]$ by one merge of the two sorted lists, so the algorithm runs in $O(n)$ time.
- **Counting optimal sets.** Keep with each $M[j]$ the number of optimal sets, adding the counts of both branches on a tie.
- **Several machines.** For $k$ machines the table approach does not extend directly; [k-machine interval scheduling](/k-machine-interval-scheduling/) uses a minimum cost flow.
- **Unit weights.** Then $M[n]$ is the size of a largest set of disjoint intervals, which the [earliest finish time](/earliest-finish-time-first/) greedy finds with no table.

## When to use it

Use it whenever intervals have different values and one resource must hold them, such as bookings, bids or candidate regions of a sequence. For unit weights the greedy is simpler. For a fixed number of resources larger than one, use the flow formulation, and if intervals arrive online with immediate decisions, this offline algorithm does not apply.

## Pitfalls

- **The wrong search for the type.** An upper bound search for closed intervals counts an interval that ends exactly at $l_j$ as compatible, and the result can contain two intervals that share a point, such as $[0, 3]$ and $[3, 6]$.
- **Sorting by left end.** The prefix property needs the order by right end. In the order by left end, the intervals compatible with $j$ are not a prefix: in $[0, 10), [1, 2), [3, 4)$ the interval $[3, 4)$ is compatible with $[1, 2)$ but not with $[0, 10)$.
- **Off by one in $p$.** $p[j]$ is a count, the index of the last compatible interval in a 1-based table. Mixing 0-based and 1-based indices makes $M[p[j]]$ read the wrong entry.
- **Linear search for $p$.** Scanning back from $j$ to find $p[j]$ takes $\Theta(n^2)$ time in the worst case, for example when every interval is compatible with all earlier ones. The binary search of line L2 keeps the total at $O(n \log n)$.
- **Weights that are not positive.** An interval with $w_j < 0$ is never taken, since $w_j + M[p[j]] < M[p[j]] \le M[j - 1]$. An interval with $w_j = 0$ can be taken by line L8, which tests $\ge$. Remove such intervals first if they are not wanted.

## Implementations

## History

Kleinberg and Tardos use weighted interval scheduling to open their chapter on dynamic programming, with the recurrence, the function $p(j)$, memoization, and the procedure that recovers the solution. CLRS treat the unit weight case, activity selection, first by a dynamic program and then by the greedy.

## References
