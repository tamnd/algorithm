---
tag: 4XRAFH
kind: algorithm
slug: earliest-finish-time-first
name: Earliest finish time first
aliases:
- Earliest finish time greedy
- Greedy activity selection
- Greedy interval scheduling
- earliest finish time greedy
- greedy interval scheduling
area: techniques/greedy
level: intro
summary: Sort intervals by finish time and repeatedly take the first compatible one.
solves: [activity-selection]
model: comparison-model
complexity:
  vars: {n: the number of activities}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [activity-selection, greedy-algorithm, sorting-problem]
see_also: [greedy-stays-ahead, greedy-choice-property, exchange-argument, interval-partitioning, weighted-interval-scheduling, k-machine-interval-scheduling, online-interval-scheduling]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.1, An activity-selection problem (RECURSIVE-ACTIVITY-SELECTOR and GREEDY-ACTIVITY-SELECTOR)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling, The Greedy Algorithm Stays Ahead
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 4, Greedy Algorithms (the class scheduling example)
---

Earliest finish time first is the [greedy algorithm](/greedy-algorithm/) for [activity selection](/activity-selection/): sort the activities by finish time, then scan them and take each activity that starts at or after the finish of the last one taken. It returns a largest set of pairwise compatible activities. It runs in $\Theta(n \log n)$ time for the sort and $\Theta(n)$ time for the scan, so it takes linear time when the input is already sorted by finish time. Its proof of optimality is the standard example of the [greedy stays ahead](/greedy-stays-ahead/) method.

## In plain words

You have one room and many requests to use it, each with a start time and an end time. You want to accept as many requests as you can, and two accepted requests must not overlap.

Take the request that ends first. It leaves the room free as early as possible, so it blocks the fewest later requests. Throw away every request that overlaps it. Then do the same with what is left: take the one that ends first, and so on.

In practice you sort the requests by end time once. Then you walk through the list and keep a request when it starts no earlier than the end of the last request you kept. Other rules that sound good, such as the shortest request first or the earliest start first, can accept fewer requests.

## The problem

The input is a finite set $S$ of $n$ activities. Activity $a$ has a start time $s(a)$ and a finish time $f(a)$ with $s(a) < f(a)$, and it occupies the half-open interval $[s(a), f(a))$. Two activities $a \ne b$ are *compatible* when their intervals are disjoint, that is, when $f(a) \le s(b)$ or $f(b) \le s(a)$. So an activity that ends at time 7 and an activity that starts at time 7 are compatible. The output is a set $A \subseteq S$ of pairwise compatible activities with $|A|$ as large as possible. This is the [activity-selection problem](/activity-selection/), also called interval scheduling.

## The algorithm

```pseudo id=main
EARLIEST-FINISH-TIME-FIRST(S)              ▷ S: n activities, each with s(a) < f(a)
L1  sort S by finish time into a1, a2, ..., an    ▷ f(a1) ≤ f(a2) ≤ ... ≤ f(an)
L2  A ← empty list
L3  last ← −∞                               ▷ finish time of the last activity in A
L4  for i ← 1 to n do
L5      if s(ai) ≥ last then                 ▷ ai is compatible with all of A
L6          append ai to A
L7          last ← f(ai)
L8  return A
```

Line L1 is the only step that costs more than linear time. Any order of activities with equal finish times is correct. The variable $last$ is the finish time of the activity added most recently. Because the activities arrive in order of finish time, $last$ is also the largest finish time in $A$, so one comparison in line L5 decides whether $a_i$ is compatible with all of $A$. The test is $\ge$ and not $>$, because the intervals are half-open.

## Example

Take the eight activities $a = [0, 6)$, $b = [1, 4)$, $c = [3, 5)$, $d = [4, 7)$, $e = [5, 9)$, $f = [6, 9)$, $g = [7, 8)$ and $h = [8, 11)$. Line L1 sorts them by finish time: $b, c, a, d, g, e, f, h$ (the tie between $e$ and $f$ at time 9 is kept in input order).

| $i$ | activity | interval | $last$ before | test $s \ge last$ | taken? | $last$ after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | $b$ | $[1, 4)$ | $-\infty$ | $1 \ge -\infty$ | yes | 4 |
| 2 | $c$ | $[3, 5)$ | 4 | $3 \ge 4$ | no | 4 |
| 3 | $a$ | $[0, 6)$ | 4 | $0 \ge 4$ | no | 4 |
| 4 | $d$ | $[4, 7)$ | 4 | $4 \ge 4$ | yes | 7 |
| 5 | $g$ | $[7, 8)$ | 7 | $7 \ge 7$ | yes | 8 |
| 6 | $e$ | $[5, 9)$ | 8 | $5 \ge 8$ | no | 8 |
| 7 | $f$ | $[6, 9)$ | 8 | $6 \ge 8$ | no | 8 |
| 8 | $h$ | $[8, 11)$ | 8 | $8 \ge 8$ | yes | 11 |

The output is $A = \{b, d, g, h\}$, with 4 activities. No compatible set of 5 exists, and $\{b, d, g, h\}$ is the only compatible set of 4 for this input. Three of the four choices use the half-open rule: $d$ starts when $b$ ends, $g$ starts when $d$ ends, and $h$ starts when $g$ ends. If the intervals were closed, a common end point would be a conflict, the test would be $s(a_i) > last$, and the same input would give only $\{b, g\}$, which is optimal for closed intervals. So the convention changes the answer.

For contrast, the rule "earliest start first" takes $a = [0, 6)$ first and then $f = [6, 9)$, and stops with 2 activities.

## Correctness

Let $i_1, \ldots, i_k$ be the activities that the algorithm takes, in the order it takes them, and let $j_1, \ldots, j_m$ be any compatible set, sorted by finish time. Two facts prove the algorithm correct.

- **Compatibility.** The [loop invariant](/loop-invariant/) of line L4 is: $A$ is pairwise compatible, and $last$ is the largest finish time in $A$ ($-\infty$ if $A$ is empty). An activity that passes line L5 starts at or after every finish time in $A$, so it is compatible with all of $A$.
- **The greedy stays ahead.** For each $r \le \min(k, m)$, $f(i_r) \le f(j_r)$. This follows by induction on $r$: if $j_r$ finished before $i_r$, then $j_r$ comes after $i_{r-1}$ and before $i_r$ in the sorted order, it passes the test of line L5, and the algorithm would have taken it.

If $m > k$, then $j_{k+1}$ starts at or after $f(j_k) \ge f(i_k)$, so the algorithm would have taken it after $i_k$. This contradicts the fact that $i_k$ is the last activity taken. So $k \ge m$ for every compatible set, and $A$ is maximum. The full proof is below.

## Complexity

- **Time.** Line L1 sorts $n$ keys with a [comparison sort](/comparison-sort/) such as [merge sort](/merge-sort/), in $\Theta(n \log n)$ time in the worst case. Lines L4 to L7 do $O(1)$ work for each of the $n$ activities, so the scan takes $\Theta(n)$ time. The total is $\Theta(n \log n)$. If the input is already sorted by finish time, line L1 is not necessary and the total is $\Theta(n)$.
- **Comparisons.** The scan does exactly $n$ comparisons in line L5. The sort does $O(n \log n)$.
- **Space.** The sorted order and the output take $\Theta(n)$ extra space. If the input array may be sorted in place and the output is a list of marks, the extra space is $O(1)$ apart from the sort.

The sort cannot be avoided when the output must be listed in time order. For distinct integers $x_1, \ldots, x_n$, the intervals $[2x_i, 2x_i + 1)$ are pairwise compatible, so the output holds all of them, and listing it in time order sorts the $x_i$. In the [comparison model](/comparison-model/) this needs at least $\lg(n!) = n \lg n - O(n)$ comparisons in the worst case. When only the set is required, this argument does not apply, and this page makes no claim about a lower bound for that version.

## Properties

- **Deterministic and comparison-based.** The algorithm compares only start and finish times. It works for any totally ordered time domain, such as integers, rationals or timestamps.
- **The output is in time order.** The activities in $A$ are sorted by finish time, and also by start time, because they are pairwise disjoint.
- **The output is the set with the earliest finishes.** By the stays-ahead lemma, the $r$-th activity of the greedy set finishes no later than the $r$-th activity of any compatible set. So the greedy set leaves the resource free as early as possible after each step.
- **Not online in the strict sense.** The algorithm needs all finish times before it starts. When the activities arrive sorted by finish time, it decides each one at once and never changes a decision.

## Variants and improvements

- **Recursive form.** CLRS first gives RECURSIVE-ACTIVITY-SELECTOR, which takes the first activity of the sorted list and calls itself on the activities that start at or after its finish. The iterative form above, which CLRS calls GREEDY-ACTIVITY-SELECTOR, is the same algorithm without the recursion.
- **Latest start time first.** Sort by start time, scan from the latest start to the earliest, and take each activity that finishes at or before the earliest start taken so far. This is the same algorithm with time reversed, and it is also optimal.
- **Minimum number of removals.** To make a set of intervals pairwise disjoint by deleting the fewest intervals, delete the $n - |A|$ intervals that the algorithm does not take.
- **Weighted activities.** When each activity has a value and the goal is the largest total value, this greedy rule fails. Use the dynamic program of [weighted interval scheduling](/weighted-interval-scheduling/).
- **Several resources.** To select the most activities that fit on $k$ identical rooms, see [k-machine interval scheduling](/k-machine-interval-scheduling/). To place all activities on the fewest rooms, see [interval partitioning](/interval-partitioning/).

## When to use it

Use it whenever the task is to fit the largest number of non-overlapping intervals on one resource and all intervals have the same value. It is optimal, it needs one sort and one pass, and it uses only comparisons. If the intervals have different values, use the dynamic program for weighted interval scheduling, which costs the same $O(n \log n)$ time but more code. If the intervals arrive one by one and each decision is final, the problem is an [online interval scheduling](/online-interval-scheduling/) problem, and no rule is optimal on every input.

## Pitfalls

- **Sort by the wrong key.** Sorting by start time in line L1 is wrong: for $[0, 10)$, $[1, 2)$ and $[3, 4)$ it takes $[0, 10)$ and stops with 1 activity, while the optimum is 2. Sorting by length is wrong too: for $[0, 5)$, $[4, 7)$ and $[6, 10)$ it takes $[4, 7)$ and stops with 1, while $[0, 5)$ and $[6, 10)$ give 2. Sort by finish time.
- **A strict test with half-open intervals.** The test $s(a_i) > last$ in line L5 rejects an activity that starts exactly when the last one ends. On the example above it returns only $\{b, g\}$, 2 activities instead of 4. Use $s(a_i) \ge last$ for half-open intervals. Use $>$ only when the intervals are closed and a common end point is a conflict.
- **Compare with the previous activity in the list.** Line L5 must compare with the finish of the last activity *taken*, not with the finish of $a_{i-1}$. The second test accepts activities that overlap the set.
- **Overflow of the sentinel.** In a typed language, use a flag for "no activity taken yet" or the smallest value of the type for $-\infty$, not a value such as $-1$ that a real start time can take.

## Implementations

## History

The activity-selection problem and this algorithm open the greedy chapter of CLRS, where they are used to show the greedy-choice property and optimal substructure. Kleinberg and Tardos use the same algorithm, under the name interval scheduling, to introduce the argument that the greedy algorithm stays ahead. The problem is the [maximum independent set](/maximum-independent-set/) problem restricted to interval graphs, which are [chordal graphs](/chordal-graph/). That problem is NP-hard on general graphs, and this algorithm solves the interval case in $O(n \log n)$ time.

## References
