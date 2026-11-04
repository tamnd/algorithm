---
tag: 6FVPG6
kind: technique
slug: reduction-to-sorting
name: Reduction to sorting
aliases:
- sorting as a subroutine
area: techniques/reductions-and-transforms
level: intro
summary: Solving a problem by sorting its input first, then answering queries from the sorted order.
prereqs: [reduction, sorting-problem, presorting]
see_also: [transform-and-conquer, canonicalization, interval-merging, activity-selection, graham-scan, sweep-line-technique, closest-pair-of-points, reduction-lower-bound]
sources:
  - book: isbn:9780132316811
    title: Anany Levitin, Introduction to the Design and Analysis of Algorithms, third edition, Pearson, 2012
    locator: Section 6.1, Presorting; Section 6.6, Problem Reduction
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition, Springer, 2020
    locator: Chapter 4, Sorting (the applications of sorting)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.1, An activity-selection problem (sort by finish time)
  - paper: doi:10.1016/0020-0190(72)90045-2
    title: "Ronald L. Graham, An efficient algorithm for determining the convex hull of a finite planar set, Information Processing Letters 1(4) (1972), 132-133"
    locator: the whole note (sort the points by angle, then one scan)
---

A reduction to sorting solves a problem $P$ by mapping each instance of $P$ to an instance of the [sorting problem](/sorting-problem/), sorting it, and reading the answer of $P$ off the sorted order with a cheap pass. It is a [reduction](/reduction/) in which the target problem is sorting. The items that are sorted may be derived from the input (endpoints of intervals, angles of points, sorted strings as keys), and the order may be a key that is computed from each item. When the transform and the final pass take $O(n)$ time and the derived instance has $O(n)$ items, $P$ is solved in $O(n \log n)$ time with a comparison sort.

## In plain words

Some problems become easy once the right list is in the right order. The trick is to find which list to build and which order to use. Sometimes it is the input itself in its usual order. Often it is something else: the end times of meetings, the two endpoints of each interval as separate events, or the direction from one fixed point to each other point.

After the sort, one walk from left to right gives the answer, because the order puts the items that matter next to each other or in the sequence in which a greedy choice must look at them.

The plain case, where you sort the input as it is and then scan it, has its own page: presorting. Here the work is in the choice of what to sort and by what key.

## When it applies

- The answer depends only on how items relate in some total order, for example which items are neighbours, which come first, or in which order events happen.
- Each input item maps to a constant number of derived items with a key that is cheap to compute.
- A greedy rule is correct when the items are processed in a fixed order (by finish time, by left endpoint, by deadline).
- Items must be grouped by an equivalence, and each item has a [canonical form](/canonicalization/) that can serve as a sort key.
- No linear-time algorithm is known for the problem. If one is (selection, maximum gap with integer or floor operations), the reduction gives a slower bound than the best one.

## The template

The holes are ENCODE, which builds the derived items with their keys, KEY, which gives the order, and DECODE, a pass over the sorted items.

```pseudo id=main
SOLVE-BY-SORTING(x)
L1  B ← ENCODE(x)                ▷ m derived items, m = O(n), with their keys
L2  SORT(B by KEY)               ▷ ties broken by a fixed rule
L3  return DECODE(B)             ▷ one pass, O(m) time
```

Let ENCODE take $e(n)$ time and give $m(n)$ items, let a key comparison take $c$ time, and let DECODE take $d(m)$ time. With a comparison sort, the total time is

$$e(n) + O(c \cdot m \log m) + d(m).$$

With $e(n) = O(n)$, $m = O(n)$, $c = O(1)$ and $d(m) = O(m)$, this is $O(n \log n)$. With integer keys in a range of polynomial size, [radix sort](/radix-sort/) replaces the comparison sort and the total is $O(n)$.

The correctness proof always has the same shape. It shows that, in the sorted order of KEY, the answer depends only on a local property of the order: two items that are adjacent, or a prefix of the order processed by a greedy rule. DECODE then checks that property.

How it differs from [presorting](/presorting/): presorting sorts the input items by their own values and scans the result. A reduction to sorting may sort other objects than the input items, by a key that is not the natural order, and may sort more than once. Presorting is the special case in which ENCODE is the identity.

## Classic examples

### Closest pair on a line

Given $n$ reals, find two with the smallest difference. ENCODE is the identity, so this is also [presorting](/presorting/), but it shows the key fact on which DECODE rests: if $a < b < c$, then $c - a > b - a$, so a closest pair is always adjacent in the sorted order. For $(31, 4, 15, 92, 65, 35, 89)$ the sorted order is $(4, 15, 31, 35, 65, 89, 92)$, the six adjacent gaps are $11, 16, 4, 30, 24, 3$, and the closest pair is $89, 92$. The scan looks at $6$ gaps instead of all $21$ pairs. In the plane the same idea needs more work: see [closest pair of points](/closest-pair-of-points/).

### Merging intervals

[Interval merging](/interval-merging/) replaces a set of closed intervals by the disjoint intervals of their union. KEY is the left endpoint. DECODE keeps a current interval $[s, t]$; the next interval $[a, b]$ joins it when $a \le t$, and $t$ becomes $\max(t, b)$; else $[s, t]$ is output and $[a, b]$ starts a new one. After the sort, an interval that starts after $t$ cannot meet any earlier interval, since all earlier intervals end by $t$. For $\{[8, 10], [1, 3], [15, 18], [2, 6], [9, 12]\}$, the sorted order is $[1, 3], [2, 6], [8, 10], [9, 12], [15, 18]$, and the output is $[1, 6], [8, 12], [15, 18]$.

### Maximum overlap by sorting events

To find the largest number of half-open intervals $[a, b)$ that share a point, ENCODE makes $2n$ derived items: an event $(a, +1)$ and an event $(b, -1)$ for each interval. KEY is the coordinate, and at equal coordinates a $-1$ event comes before a $+1$ event, because an interval that ends at $x$ does not contain $x$. DECODE adds the $\pm 1$ values in order and returns the largest prefix sum. For $\{[1, 4), [2, 4), [4, 6), [4, 7), [5, 8)\}$ the answer is $3$ (the points of $[5, 6)$). If the tie rule puts starts first, the prefix sum at $4$ reaches $4$, which is wrong. This is the first step of the [sweep line technique](/sweep-line-technique/) ([maximum overlap by a sweep](/sweep-maximum-overlap/)).

### Greedy order: activity selection

In [activity selection](/activity-selection/), choose as many pairwise compatible activities $[s_i, f_i)$ as possible. KEY is the finish time $f_i$. DECODE takes each activity that starts at or after the finish time of the last chosen one. The exchange argument in CLRS Section 15.1 shows that an activity with the earliest finish time is in some optimal solution, so the greedy pass is optimal. For the eleven activities with $s = (1, 3, 0, 5, 3, 5, 6, 8, 8, 2, 12)$ and $f = (4, 5, 6, 7, 9, 9, 10, 11, 12, 14, 16)$, the pass chooses $[1, 4), [5, 7), [8, 11), [12, 16)$.

### Grouping by a canonical key

To group words that are anagrams of each other, ENCODE maps each word $w$ to the pair $(\mathrm{sort}(w), w)$, where $\mathrm{sort}(w)$ is the word with its letters in order. Two words are anagrams exactly when the keys are equal, a fact proved on the [canonicalization](/canonicalization/) page. After the sort by key, each group is a run. For (listen, silent, google, enlist, inlets, banana), the keys are eilnst (four times), eggloo and aaabnn, so the groups are {listen, silent, enlist, inlets}, {google} and {banana}. Here there are two levels of sorting: the letters inside each word, and then the pairs.

### Convex hull by angle

[Graham scan](/graham-scan/) finds the lowest point $p_0$, sorts the other points by the angle of $p_i - p_0$ ([angular sort](/angular-sort/)), and then makes one pass with a stack that removes each point at which the chain does not turn left. The scan pushes and pops each point at most once, so it takes $O(n)$ time, and the whole algorithm takes $O(n \log n)$. The angle is never computed: the comparison of two directions is the sign of a cross product. [Andrew's monotone chain](/andrew-monotone-chain/) sorts by $x$ instead.

## Variations

- **Several sorts.** Some algorithms sort the same items by two keys, for example the divide-and-conquer [closest pair](/closest-pair-divide-and-conquer/) algorithm, which keeps the points sorted by $x$ and by $y$.
- **Decorate, sort, undecorate.** When KEY is costly, compute it once for each item, sort the pairs (key, item), and drop the keys. This costs $n$ key computations instead of $\Theta(n \log n)$.
- **Integer keys.** When the keys are integers in a range of size $n^{O(1)}$, a [radix sort](/radix-sort/) makes the whole reduction linear.
- **Sorting as a lower bound.** The opposite direction, from sorting to a new problem, proves that the new problem needs $\Omega(n \log n)$ time in a given model. See [lower bounds by reduction](/reduction-lower-bound/).

## Pitfalls

- **Sorting when a linear algorithm exists.** The $k$th smallest item does not need a sort: [quickselect](/quickselect/) finds it in $O(n)$ expected time and [median of medians](/median-of-medians/) in $O(n)$ worst-case time. The largest gap between neighbours in the sorted order of $n$ reals takes $O(n)$ time with buckets on a RAM that has the floor function, although the obvious method sorts.
- **The tie rule.** The order of items with equal keys can change the answer, as in the maximum overlap example. Write the tie rule into KEY.
- **The wrong key.** Sorting intervals by length or by start time does not make the activity selection greedy correct; only the finish time does. Prove the local property for the key you use.
- **Costly comparisons.** If each key is a string of length $L$, a comparison takes up to $L$ steps, and the sort takes $O(L n \log n)$ time. A [string sort](/string-sorting/) or a hash of the keys can be faster.
- **Floating-point keys.** Angles computed with atan2 can tie or swap for nearly collinear points. Compare with exact cross products on integer coordinates.
- **The direction of the reduction.** Solving $P$ with a sort gives an upper bound for $P$. It says nothing about a lower bound for $P$.

## Exercises

1. Given $n$ points on a line and a length $L$, find the largest number of points that a closed segment of length $L$ can cover. Reduce the problem to one sort and one pass with two indices.
2. Prove that, among closed intervals sorted by left endpoint, the merge rule "join when $a \le t$" outputs the connected parts of the union.
3. Give $n$ jobs with processing times $p_1, \ldots, p_n$ on one machine. Show that the order of non-decreasing $p_i$ minimizes the sum of completion times, and compute the minimum for $p = (3, 1, 4, 1, 5)$.
4. Two strings are equal up to a permutation of letters when one is an anagram of the other. Decide this for two strings of length $L$ over an alphabet of size $\sigma$ in $O(L + \sigma)$ time, without a comparison sort.
5. Show an input of five intervals on which sorting by start time and taking each compatible interval gives fewer intervals than the optimum.

## References
