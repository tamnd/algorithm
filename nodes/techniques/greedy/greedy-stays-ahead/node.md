---
tag: MN7NGT
kind: technique
slug: greedy-stays-ahead
name: Greedy stays ahead
aliases:
- Greedy stays-ahead proof
- Stays-ahead argument
- stays ahead argument
area: techniques/greedy
level: intro
summary: Proof method showing that after each step the greedy partial solution is at least as good as any other.
prereqs: [greedy-algorithm, loop-invariant]
see_also: [exchange-argument, greedy-choice-property, earliest-finish-time-first, activity-selection, dijkstra, matroid-greedy-theorem, interval-partitioning, loop-invariant]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling, The Greedy Algorithm Stays Ahead
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.1, An activity-selection problem
  - paper: doi:10.1016/S0021-9800(68)80039-0
    title: David Gale, Optimal assignments in an ordered set, an application of matroid theory, Journal of Combinatorial Theory 4(2), 1968
    locator: pages 176 to 180
---

Greedy stays ahead is a method to prove a greedy algorithm optimal by comparing it, step by step, with an arbitrary other solution. One defines a measure of progress for partial solutions and proves by induction that after $r$ steps the greedy solution is at least as far along as the first $r$ pieces of the other solution. At the end, being ahead at every step implies that the greedy solution is at least as good. Kleinberg and Tardos introduced the name and use it for interval scheduling, where the measure is the finish time of the $r$-th chosen interval.

## In plain words

Picture a race between the greedy algorithm and any other plan, including the best one. Both build their answer one piece at a time. After each piece, compare them with a score that tells how well placed each one is for what comes next.

The proof shows that the greedy algorithm is never behind. It is ahead after the first piece, and if it is ahead after some piece, it is still ahead after the next one, because whatever the other plan did next was also open to the greedy algorithm, and the greedy algorithm took something at least as good.

Since the greedy algorithm is never behind, it cannot end with a worse answer. In particular, the other plan cannot fit in more pieces than the greedy one.

## When it applies

- Solutions are built as sequences: intervals by finish time, stops along a road, vertices in order of distance, elements by weight.
- There is a natural measure of a partial solution that the greedy rule optimizes at each step: an earliest finish, a farthest reach, a largest weight.
- If the other solution's next piece is compatible with its own earlier pieces, it is also compatible with the greedy algorithm's earlier pieces, because the greedy algorithm is ahead. This availability step is the heart of the method.

It fits well when the greedy solution and the optimum may have different sizes, because the comparison runs over positions, not over shared elements. When a local swap with a simple cost change exists, an [exchange argument](/exchange-argument/) is often shorter.

## The template

```pseudo id=main
STAYS-AHEAD-PROOF(G, O)          ▷ G = g1, ..., gk greedy; O = o1, ..., om any solution
L1  order O in the same way the greedy algorithm orders its pieces   ▷ hole: the order
L2  define a measure f(x1, ..., xr) of a partial solution            ▷ hole: the measure
L3  base: f(g1) is at least as good as f(o1)
L4  for r ← 2 to min(k, m) do
L5      assume f(g1..g(r-1)) is at least as good as f(o1..o(r-1))
L6      show o_r was a feasible choice for greedy at step r         ▷ hole: availability
L7      conclude f(g1..gr) is at least as good as f(o1..or)          ▷ greedy picked the best
L8  convert: being ahead at every r implies k ≥ m, or cost(G) ≤ cost(O) ▷ hole: the end game
```

**The holes.** Line L1 sorts the other solution so that the comparison is fair, usually by the same key the greedy algorithm uses. Line L2 must be the quantity the greedy rule optimizes, or something it controls. Line L6 uses the induction hypothesis: because the greedy algorithm is ahead, every choice that is open to the other solution is open to it too. Line L8 turns the per-step inequality into a statement about the objective, usually by contradiction: if $m > k$, the piece $o_{k+1}$ would still have been available to the greedy algorithm, which stopped only when nothing was available.

## Classic examples

- **[Earliest finish time first](/earliest-finish-time-first/) for [activity selection](/activity-selection/).** Order both solutions by finish time; the measure is the finish time of the $r$-th activity, smaller is better. Base: the greedy algorithm takes the activity that finishes first. Step: $o_r$ starts after $o_{r-1}$ finishes, which is no earlier than when $g_{r-1}$ finishes, so $o_r$ was available and $f(g_r) \le f(o_r)$. End: if $m > k$, the activity $o_{k+1}$ starts after $g_k$ finishes and would have been taken.
- **Refueling along a road.** Stopping at the farthest reachable station keeps the greedy algorithm's reach after $r$ stops at least that of any other plan after $r$ stops, so it needs no more stops.
- **Covering points with unit intervals.** Repeatedly placing an interval that starts at the leftmost uncovered point keeps the covered prefix after $r$ intervals at least as long as that of any other cover with $r$ intervals.
- **[Dijkstra's algorithm](/dijkstra/).** The settled set grows in order of distance, and the invariant that every settled vertex has its true distance is a stays-ahead statement about the tentative distances.
- **Matroid greedy.** The $r$-th element chosen by the greedy algorithm weighs at least as much as the $r$-th heaviest element of any independent set (Gale, 1968). This element-wise domination is a stays-ahead statement, and it proves the [matroid greedy theorem](/matroid-greedy-theorem/).

## Variations

- **Counting form.** Measure the number of pieces placed by some time or position, and show that greedy has at least as many at every point.
- **Element-wise domination.** Sort both solutions and compare the $r$-th elements. This form also proves optimality for every objective that is increasing in each element, not only for the sum.
- **Bounds instead of opponents.** Some proofs compare the greedy algorithm with a lower bound rather than with another solution. For [interval partitioning](/interval-partitioning/), greedy never uses more resources than the depth, which every solution needs.
- **Loop invariants.** A stays-ahead claim is a [loop invariant](/loop-invariant/) quantified over all other solutions: "after iteration $r$, no solution's first $r$ pieces beat the greedy prefix."

## Pitfalls

- **A measure the greedy rule does not control.** If the measure is not what the rule optimizes, line L7 does not follow. For activity selection, "start time of the $r$-th activity" is the wrong measure.
- **Forgetting the order of the other solution.** The comparison of $g_r$ with $o_r$ only makes sense when $O$ is ordered like the greedy output.
- **Skipping the end game.** Being ahead at each step is not yet optimality. Line L8 must use the stopping rule of the algorithm to compare the final values.
- **Availability without the hypothesis.** Line L6 must use the induction hypothesis. If $o_r$ is available to the greedy algorithm for some other reason, check that reason carefully; with closed intervals, for example, touching end points change compatibility.

## Exercises

1. Points $x_1 < \cdots < x_n$ on a line must be covered by closed intervals of length 1. Prove by stays ahead that placing an interval at the leftmost uncovered point uses the fewest intervals.
2. A car with range $R$ drives past stations at $x_1 < \cdots < x_n$. State the measure and the availability step of a stays-ahead proof that "go to the farthest reachable station" minimizes the number of stops.
3. Show that "earliest start time first" is not optimal for activity selection, and point out the line of the template where a stays-ahead proof for it breaks.

## References
