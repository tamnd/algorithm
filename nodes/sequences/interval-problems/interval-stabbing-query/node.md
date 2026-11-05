---
tag: V7ERVH
kind: problem
slug: interval-stabbing-query
name: Interval stabbing query
aliases:
- Point enclosure query
- point enclosure query
- stabbing query
area: sequences/interval-problems
level: core
summary: Report all stored intervals that contain a given point.
prereqs: [binary-search, total-order]
see_also: [interval-overlap-query, interval-tree-search, interval-tree, priority-search-tree, segment-tree, maximum-overlap, interval-piercing, sweep-line-technique]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 10, More Geometric Data Structures, Section 10.1 Interval Trees (stabbing queries in O(log n + k) time) and Section 10.3 Segment Trees
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 17.3, Interval trees (the dynamic structure; a stabbing query is the overlap query with a point)
  - paper: doi:10.1137/0214021
    title: "Edward M. McCreight, Priority search trees, SIAM Journal on Computing 14(2) (1985), pages 257 to 276"
    locator: the structure for 3-sided range queries, which answers stabbing queries on the points (l, r)
---

An interval stabbing query stores a set of $n$ intervals and, for a query point $p$, reports the intervals that contain $p$. Whether a point at an end of an interval counts depends on the type: $p$ stabs $[l, r]$ when $l \le p \le r$, $[l, r)$ when $l \le p < r$, and $(l, r)$ when $l < p < r$, so the same point and intervals give different answers under the three readings. Interval trees, segment trees and priority search trees report the $k$ answers in $O(\log n + k)$ time, and the count alone takes $O(\log n)$ time with two sorted arrays. Stabbing is the basic case of the [interval overlap query](/interval-overlap-query/), and it is how the [depth](/maximum-overlap/) of a family is defined.

## In plain words

You have a list of events, each with a start and an end time. Someone asks: what was going on at 5 o'clock? You want every event that had started by then and had not yet ended.

The hard part is the exact moment. An event that ends at 5 and an event that starts at 5 may or may not count, and the answer depends on whether an event includes its end moments. An event from 2 to 5 that means "up to but not including 5" is already over at 5.

A good data structure answers each question in time close to the number of events it reports, instead of checking every event.

## Definition

**Input.** A set $S = \{I_1, \ldots, I_n\}$ of nonempty intervals of $\mathbb{R}$ or of a [total order](/total-order/), $I_j = \langle l_j, r_j \rangle$, all of one type, and query points $p$.

**Output.** For each query, the set $\{\, j : p \in I_j \,\}$. The set $S$ can be preprocessed. In the dynamic form, insertions and deletions are mixed with the queries.

**The stabbing test.**

| type | $p \in I_j$ if and only if | end points that count |
|---|---|---|
| closed $[l, r]$ | $l \le p \le r$ | both |
| half-open $[l, r)$ | $l \le p < r$ | left only |
| open $(l, r)$ | $l < p < r$ | none |

**As a range query.** Map $I_j$ to the point $(l_j, r_j)$ of the plane. For closed intervals, $p$ stabs $I_j$ if and only if the point lies in the quadrant $l \le p$, $r \ge p$. So stabbing is a two-sided range query on the points, and every structure for 2-sided or 3-sided range reporting answers it.

## Variants

- **Counting.** For closed intervals, $p \notin I_j$ if and only if $l_j > p$ or $r_j < p$, and both cannot hold since $l_j \le r_j$. So the count is $n - |\{ j : l_j > p \}| - |\{ j : r_j < p \}|$, or equally $|\{ j : l_j \le p \}| - |\{ j : r_j < p \}|$, since every interval with $r_j < p$ has $l_j \le p$. Two [binary searches](/binary-search/) in the sorted left ends and the sorted right ends give it in $O(\log n)$ time. For half-open intervals, count $l_j \le p$ minus $r_j \le p$; for open intervals, $l_j < p$ minus $r_j \le p$.
- **Existence or one witness.** Return one interval that contains $p$, in $O(\log n)$ time with an [interval tree](/interval-tree/).
- **Best interval.** Return the shortest interval, or the one of largest weight, among those that contain $p$. When the intervals are laminar, nested or disjoint, the shortest one is the innermost, as in longest prefix match for network addresses.
- **Offline.** All $q$ points are known. Sort the points and the end points together and sweep, keeping the current intervals in a set: $O((n + q) \log (n + q) + k)$ time, or only the counts in $O((n + q) \log (n + q))$.
- **The deepest point.** The largest answer over all $p$ is the depth, the [maximum overlap](/maximum-overlap/) problem.
- **Covering by stabs.** The fewest points that together stab every interval is [interval piercing](/interval-piercing/).
- **Higher dimensions.** For axis-parallel boxes, $p$ stabs a box when it lies in its interval on every axis. Multi-level segment trees answer this.

## Examples

Store the seven intervals with end points $(1, 3), (2, 5), (3, 4), (5, 8), (6, 7), (8, 9), (7, 10)$.

**Query $p = 5$.** The point 5 is the right end of $(2, 5)$ and the left end of $(5, 8)$, and no interval has it inside.

| type | reported | count |
|---|---|---|
| closed | $[2, 5]$, $[5, 8]$ | 2 |
| half-open | $[5, 8)$ | 1 |
| open | none | 0 |

The counting formula agrees. Four intervals have $l \le 5$ and two have $r < 5$, so the closed count is $4 - 2 = 2$. Three intervals have $r \le 5$, so the half-open count is $4 - 3 = 1$. Three intervals have $l < 5$, so the open count is $3 - 3 = 0$.

**Query $p = 7$.** The point 7 is the right end of $(6, 7)$, the left end of $(7, 10)$, and inside $(5, 8)$. The closed query reports $[5, 8], [6, 7], [7, 10]$; the half-open query reports $[5, 8), [7, 10)$; the open query reports $(5, 8)$.

**Edge cases.** A point left of all intervals, such as $p = 0$, stabs nothing. A closed point interval $[3, 3]$ is stabbed only by $p = 3$. A half-open interval $[3, 3)$ or an open interval $(3, 3)$ is empty and is never stabbed, so the input requires $l < r$ for these types.

## Known algorithms

- **Linear scan.** Test each interval, $O(n)$ per query.
- **Centered interval tree.** The static tree of Edelsbrunner and McCreight stores the intervals that contain a median end point at the root, in two lists sorted by left end and by right end, and recurses on the intervals left and right of it. A query walks one path and scans each list only as far as it reports. $O(n)$ space, $O(n \log n)$ preprocessing, $O(\log n + k)$ query time, as in de Berg et al., Section 10.1.
- **[Segment tree](/segment-tree/).** Over the elementary segments between sorted end points, each interval is stored at $O(\log n)$ canonical nodes, and a query reports the lists on one root-to-leaf path: $O(\log n + k)$ time and $O(n \log n)$ space, de Berg et al., Section 10.3. Open and closed ends are handled by making each end point an elementary segment of its own.
- **[Priority search tree](/priority-search-tree/).** On the points $(l_j, r_j)$, a 3-sided query $l \le p$, $r \ge p$ in $O(\log n + k)$ time, $O(n)$ space, and $O(\log n)$ insertion and deletion.
- **[Interval tree search](/interval-tree-search/).** The augmented search tree by left end, with the largest right end of each subtree, as in CLRS. One answer in $O(\log n)$ time, all in $O(\min(n, (k + 1) \log n))$, with $O(\log n)$ updates.
- **Precomputed lists.** Store the answer for each of the $O(n)$ elementary segments and end points, and find the segment of $p$ by binary search: $O(\log n + k)$ time, but $\Theta(n^2)$ space for $n$ nested intervals.

## Bounds

**Upper bound.** $O(n)$ space and $O(\log n + k)$ query time, by the centered interval tree or the priority search tree, after $O(n \log n)$ preprocessing. The priority search tree also supports updates in $O(\log n)$ time. Counting takes $O(\log n)$ time.

**Lower bound.** Consider a comparison tree that answers queries by comparing $p$ with stored values. For the $n$ disjoint closed intervals $[2j, 2j + 1]$, $j = 1, \ldots, n$, the points $0, 2, 4, \ldots, 2n$ have $n + 1$ different answers, so the tree has at least $n + 1$ leaves and depth at least $\lceil \log_2 (n + 1) \rceil$. With $k$ steps to write the output, $\Omega(\log n + k)$ per query is needed in this model, so the structures above are optimal.

## Reductions

- **To overlap queries.** For closed intervals, $p$ stabs $I_j$ if and only if $I_j$ overlaps $[p, p]$, so any [overlap query](/interval-overlap-query/) structure answers stabbing.
- **From overlap queries.** Conversely, an overlap query with $[a, b]$ is a stabbing query at $a$ plus a search of the left ends in $(a, b]$, as shown on the overlap query page. So the two problems have the same cost up to a sorted array.
- **To 2-sided range reporting.** By the map $I_j \mapsto (l_j, r_j)$ above.
- **To counting by prefix sums.** For integer end points in a range of size $U$, add $+1$ at $l_j$ and $-1$ after the last stabbing point of $I_j$, and take prefix sums: all $U$ counts in $O(n + U)$ time, with the end point type deciding where the $-1$ goes.

## Applications

- **Timelines.** List the sessions, jobs or reservations that were active at a given moment, for example in logs or monitoring.
- **Genome positions.** List the genes or features that cover a given base of a chromosome.
- **Network addresses.** Each routing prefix is an interval of addresses, and the prefixes are laminar. The prefixes that match an address are the intervals that it stabs, and longest prefix match picks the shortest one.
- **Geometry.** In two dimensions, find the rectangles that contain a query point, for example in hit testing of a user interface.
- **Sweep algorithms.** Many sweeps keep the set of intervals stabbed by the sweep line, as in [maximum overlap](/maximum-overlap/).

## References
