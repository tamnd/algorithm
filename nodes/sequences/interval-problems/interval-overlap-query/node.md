---
tag: CMEPZF
kind: problem
slug: interval-overlap-query
name: Interval overlap query
aliases:
- Interval intersection query
- Range overlap reporting
area: sequences/interval-problems
level: core
summary: Report all stored intervals that intersect a query interval.
prereqs: [interval-stabbing-query, binary-search]
see_also: [interval-tree-search, interval-tree, priority-search-tree, segment-tree, interval-list-intersection, allens-interval-algebra, sweep-line-technique, range-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 17.3, Interval trees (the overlap test for closed intervals and INTERVAL-SEARCH), and Exercise 17.3-4 (listing all overlapping intervals)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 10, More Geometric Data Structures, Sections 10.1 Interval Trees and 10.2 Priority Search Trees (windowing queries)
  - paper: doi:10.1137/0214021
    title: "Edward M. McCreight, Priority search trees, SIAM Journal on Computing 14(2) (1985), pages 257 to 276"
    locator: the structure for 3-sided range queries, which answers overlap queries on the points (l, r)
---

An interval overlap query stores a set of $n$ intervals and, for a query interval $Q$, reports the stored intervals that share at least one point with $Q$. For closed intervals, $[l, r]$ meets $[a, b]$ exactly when $l \le b$ and $a \le r$; for half-open and open intervals both inequalities are strict, so intervals that only touch at an end point overlap in the first case and not in the others. Every overlapping interval either contains the left end of $Q$ or starts inside $Q$, which splits the problem into a [stabbing query](/interval-stabbing-query/) and a search on sorted left ends. Interval trees and priority search trees answer it in $O(\log n + k)$ or $O((k + 1) \log n)$ time for $k$ reported intervals, and counting alone takes $O(\log n)$ with two sorted arrays.

## In plain words

You keep a list of booked time slots. Someone asks for a new slot, and you want all bookings that clash with it. A booking clashes if it starts before the new slot ends and ends after the new slot starts.

The question is what to do when a booking ends exactly when the new slot starts. If times include their end moment, the two share that moment and they clash. If a slot from 9 to 10 means "up to but not including 10", a slot that starts at 10 does not clash.

A good data structure answers this without looking at every booking. It finds the clashes in about as many steps as there are clashes, plus a few more to find where to look.

## Definition

**Input.** A set $S = \{I_1, \ldots, I_n\}$ of nonempty intervals of $\mathbb{R}$, $I_j = \langle l_j, r_j \rangle$, and query intervals $Q = \langle a, b \rangle$, all of one type. Closed intervals have $l \le r$; half-open intervals $[l, r)$ and open intervals $(l, r)$ have $l < r$, so that they are nonempty.

**Output.** For each query, the set $\{\, j : I_j \cap Q \ne \emptyset \,\}$. The set $S$ is given in advance and can be preprocessed. In the dynamic form, insertions and deletions of intervals are mixed with the queries.

**The overlap test.** For intervals of one type,

| type | $I_j \cap Q \ne \emptyset$ if and only if |
|---|---|
| closed $[l, r]$, $[a, b]$ | $l \le b$ and $a \le r$ |
| half-open $[l, r)$, $[a, b)$ | $l < b$ and $a < r$ |
| open $(l, r)$, $(a, b)$ | $l < b$ and $a < r$ |

*Proof.* Let $L = \max(l, a)$ and $R = \min(r, b)$. The intersection is the interval from $L$ to $R$, which contains its left end only if both intervals contain their left ends, and its right end only if both contain their right ends. For closed intervals it is $[L, R]$, nonempty if and only if $L \le R$. For half-open intervals it is $[L, R)$, and for open ones $(L, R)$; both are nonempty if and only if $L < R$, using the density of $\mathbb{R}$ for the open case. Since $l \le r$ (or $l < r$) and $a \le b$ (or $a < b$) hold already, $L \le R$ (or $L < R$) reduces to the two cross conditions on $l, b$ and $a, r$. $\square$

**Mixed types.** The same argument gives the rule for a closed query on half-open intervals, and for any other mix: each of the two cross conditions is $\le$ when both of its ends are closed, and $<$ otherwise. For example $[1, 3)$ meets $[3, 5]$ in no point, and $[1, 3]$ meets $[3, 5)$ in the point 3.

**Decomposition.** For closed intervals, $I_j$ meets $[a, b]$ if and only if exactly one of these holds: (i) $l_j \le a \le r_j$, so $I_j$ contains $a$, or (ii) $a < l_j \le b$, so $I_j$ starts inside $Q$ after $a$. For half-open intervals the cases are (i) $l_j \le a < r_j$ and (ii) $a < l_j < b$. *Proof for closed intervals:* if $l_j \le a$, the test $l_j \le b$ holds and the overlap is $a \le r_j$, case (i); if $l_j > a$, then $a < l_j \le r_j$ holds and the overlap is $l_j \le b$, case (ii). The half-open case is the same with $<$ at $b$ and $r_j$. The two cases split on $l_j \le a$, so no interval is counted twice.

## Variants

- **Existence.** Decide whether some interval meets $Q$, or return one. The augmented interval tree does this in $O(\log n)$ time.
- **Counting.** Return the number of overlapping intervals. For closed intervals, $I_j$ misses $[a, b]$ if and only if $r_j < a$ or $l_j > b$, and both cannot hold, since then $l_j > b \ge a > r_j$. So the count is $n - |\{ j : r_j < a \}| - |\{ j : l_j > b \}|$, found by [binary search](/binary-search/) in the sorted left ends and the sorted right ends in $O(\log n)$ time. For half-open intervals use $r_j \le a$ and $l_j \ge b$.
- **Stabbing.** The query is a point, $Q = [p, p]$: this is the [interval stabbing query](/interval-stabbing-query/). For half-open intervals a point is not a half-open interval, so the stabbing test $l \le p < r$ is stated separately.
- **Offline queries.** All $q$ queries are known in advance. A [sweep](/sweep-line-technique/) over the sorted end points of intervals and queries answers them in $O((n + q) \log (n + q) + k)$ time with no tree.
- **Joins.** Report all overlapping pairs between two sets of intervals. For two sorted lists of disjoint intervals this is [interval list intersection](/interval-list-intersection/), in linear time.
- **Higher dimensions.** For axis-parallel boxes, two boxes overlap if and only if they overlap in every coordinate. Windowing queries in the plane combine interval trees, segment trees and range trees, as in de Berg et al., Chapter 10.

## Examples

Store the seven intervals with end points $(1, 3), (2, 5), (3, 4), (5, 8), (6, 7), (8, 9), (7, 10)$ and query with the end points $(4, 6)$.

| stored | closed: $l \le 6$ and $4 \le r$ | half-open: $l < 6$ and $4 < r$ |
|---|---|---|
| $(1, 3)$ | no, $3 < 4$ | no |
| $(2, 5)$ | yes | yes |
| $(3, 4)$ | yes, touches at 4 | no, $4 < 4$ fails |
| $(5, 8)$ | yes | yes |
| $(6, 7)$ | yes, touches at 6 | no, $6 < 6$ fails |
| $(8, 9)$ | no, $8 > 6$ | no |
| $(7, 10)$ | no, $7 > 6$ | no |

So the closed query reports 4 intervals and the half-open query reports 2. The open intervals give the same answer as the half-open ones. The counting formula agrees: for closed intervals one interval ends before 4 and two start after 6, so $7 - 1 - 2 = 4$; for half-open intervals two end at or before 4 and three start at or after 6, so $7 - 2 - 3 = 2$.

By the decomposition, for the closed query, $[2, 5]$ and $[3, 4]$ contain the point 4, case (i), and $[5, 8]$ and $[6, 7]$ start in $(4, 6]$, case (ii).

**Edge cases.** An empty set reports nothing. A query that lies inside one stored interval reports that interval, though no end point of it lies in $Q$. A degenerate closed query $[p, p]$ is a stabbing query.

## Known algorithms

- **Linear scan.** Test every interval: $O(n)$ per query, no preprocessing. Best when there are few queries.
- **[Interval tree search](/interval-tree-search/).** A balanced search tree by left end in which each node stores the largest right end of its subtree, as in the [interval tree](/interval-tree/) of CLRS. One overlapping interval in $O(\log n)$ time, all of them in $O(\min(n, (k + 1) \log n))$ time, with $O(\log n)$ insertion and deletion.
- **Centered interval tree.** The static tree of Edelsbrunner and McCreight, built around median end points, answers stabbing queries in $O(\log n + k)$ time with $O(n)$ space. With the decomposition above and a sorted array of left ends for case (ii), it answers overlap queries in $O(\log n + k)$ time.
- **[Priority search tree](/priority-search-tree/).** Map $I_j$ to the point $(l_j, r_j)$. For closed intervals the query is the quadrant $l \le b$, $r \ge a$, a special 3-sided range query, which McCreight's structure answers in $O(\log n + k)$ time with $O(n)$ space and $O(\log n)$ updates.
- **[Segment tree](/segment-tree/).** Over the sorted end points, each interval is stored at $O(\log n)$ canonical nodes; with the decomposition it gives $O(\log n + k)$ queries in $O(n \log n)$ space, and it extends to counting and to higher dimensions.

## Bounds

**Upper bounds.** $O(n)$ space and $O(\log n + k)$ query time, by a priority search tree or a centered interval tree with a sorted array, after $O(n \log n)$ preprocessing. Counting takes $O(\log n)$ with two sorted arrays.

**Lower bound for a query.** Consider a comparison tree that answers point queries by comparing the query against stored values. With the $n$ disjoint closed intervals $[2j, 2j + 1]$, $j = 1, \ldots, n$, the queries $[2j, 2j]$ and a query $[0, 0]$ have $n + 1$ different answers, so the tree has at least $n + 1$ leaves and depth at least $\lceil \log_2 (n + 1) \rceil$. Writing the output takes $k$ steps. So $\Omega(\log n + k)$ per query is optimal in this model, and the structures above reach it.

**Preprocessing.** The $O(\log n + k)$ structures are built in $O(n \log n)$ time, the cost of sorting the end points.

## Reductions

- **To stabbing plus a range search.** By the decomposition, one overlap query is a stabbing query at $a$ and a one-dimensional range query on left ends in $(a, b]$, closed case, or $(a, b)$, half-open case. The answers are disjoint, so the output cost stays $O(k)$.
- **To 3-sided range reporting.** By the map $I_j \mapsto (l_j, r_j)$ and the overlap test, as for the priority search tree.
- **From stabbing.** A stabbing query at $p$ is the closed overlap query $[p, p]$, so overlap queries are at least as hard as stabbing queries.
- **Relation names.** In [Allen's interval algebra](/allens-interval-algebra/), a half-open interval overlaps $Q$ when the relation is anything except before, meets, met by and after. For closed intervals, meets and met by also count as overlap.

## Applications

- **Calendars and booking.** Find the reservations that clash with a requested time slot, where the end point convention decides whether back-to-back bookings clash.
- **Genome annotation.** Find the genes or features that overlap a region of a chromosome. Genome coordinates are often half-open, zero-based, or closed, one-based, and mixing the two is a common source of off-by-one errors.
- **Temporal databases.** Select the rows whose validity period overlaps a query period.
- **Memory and address ranges.** Find the mapped regions that overlap a requested range of addresses.
- **Windowing.** In two dimensions, find the segments or boxes that meet a query window.

## References
