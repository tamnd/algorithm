---
tag: FXBG7P
kind: problem
slug: interval-containment
name: Interval containment
aliases:
- Nested intervals
- Interval inclusion detection
area: sequences/interval-problems
level: intro
summary: Find pairs of intervals where one lies inside another.
prereqs: [sorting-problem, total-order]
see_also: [interval-containment-sort, interval-merging, dominance-counting, fenwick-tree, longest-increasing-subsequence, element-distinctness-lower-bound, allens-interval-algebra, interval-overlap-query]
sources:
  - url: https://leetcode.com/problems/remove-covered-intervals/
    title: LeetCode 1288, Remove Covered Intervals
    locator: the problem statement ([a, b) is covered by [c, d) when c <= a and b <= d)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 5, Orthogonal Range Searching (a query on the end point pairs as points in the plane)
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983), pages 80 to 86"
    locator: the element distinctness lower bound used in the Bounds section
---

Interval containment asks, for a family of $n$ intervals, which intervals lie inside other intervals of the family. The basic forms are to decide whether some interval contains another, to find for each interval one interval that contains it, and to keep only the maximal intervals. An interval $[l, r]$ lies inside $[l', r']$ exactly when $l' \le l$ and $r \le r'$, so containment is a dominance relation between the points $(l, r)$, and a sort by left end with ties broken by right end solves the basic forms in $O(n \log n)$ time. Two intervals that share an end point can still be nested, so the tests use $\le$, never $<$.

## In plain words

You have a list of time slots, and you want to throw away every slot that sits completely inside a longer slot, because the longer one already covers it. A slot sits inside another one when it starts no earlier and ends no later.

The tricky cases are slots that share an end. A slot from 9:00 to 10:00 sits inside a slot from 9:00 to 12:00, even though both start at 9:00. Two copies of one slot each sit inside the other, so you must decide which copy to keep. A slot from 10:00 to 12:00 that only touches another slot at 10:00 does not sit inside it.

## Definition

**Input.** A family of $n$ nonempty intervals $I_1, \ldots, I_n$ of $\mathbb{R}$ (or of a [total order](/total-order/)), with $I_j = \langle l_j, r_j \rangle$ and $l_j \le r_j$, all of one type: closed, half-open or open.

**Containment.** $I_i \subseteq I_j$ is set inclusion. For intervals of one type,

$$ I_i \subseteq I_j \iff l_j \le l_i \text{ and } r_i \le r_j. $$

For closed intervals this is direct. For half-open intervals $[l, r)$ with $l < r$: if $l_j \le l_i$ and $r_i \le r_j$, each $x$ with $l_i \le x < r_i$ has $l_j \le x < r_j$; conversely, $l_i \in I_i \subseteq I_j$ gives $l_j \le l_i$, and the points of $I_i$ just left of $r_i$ lie in $I_j$, which gives $r_i \le r_j$. Open intervals are the same with both ends handled like the right end. So the test does not depend on the type, as long as all intervals have the same type. $I_i$ is *properly* contained in $I_j$ when $I_i \subseteq I_j$ and $I_i \ne I_j$.

**Mixed types.** If the types differ, compare end points as keys: a left end $x$ gets the key $(x, 0)$ if it is closed and $(x, 1)$ if it is open, and a right end $x$ gets $(x, 1)$ if it is closed and $(x, 0)$ if it is open. Then $I_i \subseteq I_j$ if and only if the left key of $I_j$ is at most that of $I_i$ and the right key of $I_i$ is at most that of $I_j$, in lexicographic order. For example $[1, 3) \subseteq [1, 3]$, but $[1, 3] \not\subseteq [1, 3)$.

**Tasks.**

1. **Decide.** Is there a pair $i \ne j$ with $I_i \subseteq I_j$?
2. **Maximal intervals.** Return the intervals that are not properly contained in any other, keeping one copy of each, together with a container for every other interval. This is "remove covered intervals".
3. **Count.** For each $i$, the number of $j \ne i$ with $I_i \subseteq I_j$, or with $I_j \subseteq I_i$.
4. **Report.** List all pairs $(i, j)$, $i \ne j$, with $I_i \subseteq I_j$.

**As dominance.** Map $I_j$ to the point $p_j = (-l_j, r_j)$ of the plane. Then $I_i \subseteq I_j$ if and only if $p_j$ is at least $p_i$ in both coordinates. So task 3 is [dominance counting](/dominance-counting/), and task 2 asks for the maximal points, the Pareto front of the $p_j$.

## Variants

- **Longest nested chain.** The longest sequence $J_1 \supsetneq J_2 \supsetneq \cdots$ of intervals of the family. After removing duplicates and sorting by left end ascending and right end descending, a chain is exactly a non-increasing subsequence of the right ends, so it is a [longest increasing subsequence](/longest-increasing-subsequence/) problem, solved in $O(n \log n)$ time.
- **Containment queries.** Store the family and answer, for a query interval $Q$, the intervals that contain $Q$ or lie inside $Q$. Both are 2-sided or 3-sided range queries on the points $p_j$, answered by a [range tree](/range-tree/) or a [priority search tree](/priority-search-tree/).
- **Proper families.** A family in which no interval properly contains another. Sorted by left end, such a family is also sorted by right end. Its interval graphs are the proper interval graphs.
- **Containment between two families.** For each interval of $A$, decide whether some interval of $B$ contains it. The same sort works on the merged list, with the $B$ intervals placed first at ties.

## Examples

**A family with all the touching cases.** Take the closed intervals

$$ [1, 4], \; [2, 3], \; [3, 6], \; [1, 2], \; [5, 6], \; [3, 6], \; [6, 8], \; [7, 8]. $$

- $[1, 2] \subseteq [1, 4]$, with a shared left end, and $[2, 3] \subseteq [1, 4]$.
- $[5, 6] \subseteq [3, 6]$, with a shared right end. It lies in both copies of $[3, 6]$.
- The two copies of $[3, 6]$ each contain the other.
- $[7, 8] \subseteq [6, 8]$, with a shared right end.
- $[6, 8]$ touches $[3, 6]$ at 6 but is not contained in it, and $[3, 6]$ only overlaps $[1, 4]$.

The maximal intervals, one copy each, are $[1, 4], [3, 6], [6, 8]$. There are 7 ordered pairs $(i, j)$ with $I_i \subseteq I_j$: the 5 proper ones, $[1, 2]$ and $[2, 3]$ in $[1, 4]$, $[5, 6]$ in each copy of $[3, 6]$, and $[7, 8]$ in $[6, 8]$, plus each copy of $[3, 6]$ in the other.

**The same numbers as half-open intervals.** The answer is the same, because the test is the same for every type. $[5, 6) \subseteq [3, 6)$ still holds, and $[6, 8)$ is still not inside $[3, 6)$.

**Edge cases.** One interval contains nothing else. A proper family, such as $[1, 3], [2, 4], [3, 5]$, has no contained pair: each pair only overlaps or touches. $n$ copies of one interval give $n(n - 1)$ ordered pairs.

## Known algorithms

- **[Interval containment by sorting](/interval-containment-sort/).** Sort by left end ascending and right end descending, then scan with the largest right end so far. An interval is contained in an earlier one exactly when its right end is at most that maximum. This solves tasks 1 and 2 in $O(n \log n)$ time.
- **Sort and a [Fenwick tree](/fenwick-tree/).** In the same order, count for each interval the earlier right ends that are at least its own. $O(n \log n)$ time for task 3, as in [dominance counting](/dominance-counting/).
- **Sort and scan for reporting.** In the same order, the intervals that $I_i$ contains are among the later intervals that start at or before $r_i$. One query per interval to a [priority search tree](/priority-search-tree/) on the points $p_j$ gives task 4 in $O(n \log n + k)$ time for $k$ pairs.
- **Brute force.** Test all $n(n - 1)$ ordered pairs in $O(n^2)$ time.

## Bounds

**Upper bound.** $O(n \log n)$ time for tasks 1, 2 and 3 in the [comparison model](/comparison-model/), and $O(n \log n + k)$ for task 4, where $k$ can be as large as $n(n - 1)$.

**Lower bound.** Task 1 needs $\Omega(n \log n)$ operations in the [algebraic decision tree](/algebraic-decision-tree/) model. Given numbers $x_1, \ldots, x_n$, form the point intervals $[x_j, x_j]$. Then $[x_i, x_i] \subseteq [x_j, x_j]$ if and only if $x_i = x_j$, so there is a contained pair if and only if two numbers are equal. This decides [element distinctness](/element-distinctness/) with $O(n)$ extra work, and Ben-Or's bound ([lower bound page](/element-distinctness-lower-bound/)) applies. Tasks 2 and 3 answer task 1, so the bound holds for them too. For half-open intervals use $[x_j, x_j + 1)$: two of them are nested if and only if they are equal.

## Reductions

- **To two-dimensional dominance.** The map $I_j \mapsto (-l_j, r_j)$ turns containment into dominance, so maxima and dominance counting algorithms apply directly.
- **From element distinctness.** As in the Bounds section.
- **To longest increasing subsequence.** The longest nested chain, as in the Variants section.
- **Merging is not containment.** [Interval merging](/interval-merging/) joins intervals that overlap or touch; containment asks for the stronger relation. Every contained interval disappears into the component of its container, but a component can also absorb intervals that are not contained in any single other interval.

## Applications

- **Removing redundant data.** Drop time ranges, genomic regions or address ranges that a larger range already covers.
- **Nesting structure.** Tags of a document, scopes of a program, or calls in a trace form intervals that are either nested or disjoint; the containment relation gives the tree.
- **Proper interval models.** Checking that a family is proper, no interval inside another, is a step in recognizing proper interval graphs from an interval model.
- **Temporal reasoning.** The relations "during", "starts" and "finishes" of [Allen's interval algebra](/allens-interval-algebra/) together make up proper containment.

## References
