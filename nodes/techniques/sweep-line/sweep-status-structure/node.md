---
tag: M4V0SH
kind: data-structure
slug: sweep-status-structure
name: Sweep status structure
aliases:
- status structure
- sweep status
area: techniques/sweep-line
level: core
summary: Balanced search tree that keeps the objects crossing the sweep line in their current geometric order.
prereqs: [sweep-line-technique, balanced-binary-search-tree, orientation-test]
see_also: [event-queue, bentley-ottmann-algorithm, segment-intersection-detection, red-black-tree, ordered-set, interval-tree, segment-tree, skyline-sweep]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 2, Section 2.1 (the status structure T, with the segments in the leaves, and the handling of an event point)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 33.2 (the total preorder of segments at x, the operations INSERT, DELETE, ABOVE and BELOW on a red-black tree, and ANY-SEGMENTS-INTERSECT)
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science, 1976
    locator: pp. 208 to 215
  - paper: doi:10.1109/TC.1979.1675432
    title: Jon L. Bentley and Thomas A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers C-28(9), 1979
    locator: pp. 643 to 647
---

The sweep status structure of a [sweep](/sweep-line-technique/) is the ordered set of the objects that cross the sweep line, ordered by their position along the line. For line segments it is a [balanced binary search tree](/balanced-binary-search-tree/) whose comparator evaluates each segment at the current position of the line, so the keys change as the line moves while the tree stays a valid search tree. It supports insert, delete, the neighbors above and below a segment or a point, and the swap of two neighbors at their crossing, each in $O(\log n)$ time for $n$ stored segments when no three of them pass through one point. It is the second half of each plane sweep, next to the [event queue](/event-queue/).

## In plain words

Picture a vertical ruler that slides from left to right over a drawing of line pieces. At each moment some pieces cross the ruler, and you can list them from the bottom of the ruler to the top. The status structure keeps that list.

The list changes only at a few places. A piece joins the list when the ruler reaches its left end, and leaves it at its right end. Two pieces exchange places where they cross. Between these places the heights on the ruler change, but the order does not, because no two pieces cross there. So a search tree that compares pieces by their height on the ruler stays sorted.

The sweep asks the list one main question: which pieces are directly above and below a given piece or point? Only neighbors in the list can meet first, so this question finds all crossings.

## The abstract type

Let $S$ be a set of segments in the plane, none vertical, and no two overlapping (sharing more than one point). For a segment $s$ from $(x_1, y_1)$ to $(x_2, y_2)$ with $x_1 < x_2$ and a value $x$ with $x_1 \le x \le x_2$, let

$$ y_s(x) = y_1 + \frac{y_2 - y_1}{x_2 - x_1} (x - x_1), \qquad m_s = \frac{y_2 - y_1}{x_2 - x_1}. $$

At a sweep position $x$, compare two segments that both cross the line by the key $(y_s(x), m_s)$, lexicographically. The first part is the order along the line. CLRS (Section 33.2) use it alone; for segments through one point of the line it gives a tie, so it is a total preorder, not a total order. The second part breaks the tie by the order just to the right of $x$: if $y_s(x) = y_t(x)$ and $m_s < m_t$, then $y_s(x') < y_t(x')$ for each $x' > x$ where both are defined. De Berg et al. sweep a horizontal line from top to bottom and order the segments from left to right along it; that is the same order after a quarter turn of the plane.

The status $T$ holds the set of active segments, those that cross the line at $T.x$, as a sequence from bottom to top. The operations are:

- SET-X$(T, x')$: move the line to $x' \ge T.x$. The precondition is that no two stored segments cross at an $x$ strictly between $T.x$ and $x'$, and that each stored segment still spans $x'$.
- INSERT$(T, s)$ and DELETE$(T, s)$.
- ABOVE$(T, s)$ and BELOW$(T, s)$: the segment directly above or below $s$, or NIL.
- SWAP$(T, s, t)$: $t$ is directly above $s$ and both pass through the same point of the line; exchange them.
- NEIGHBORS-OF-POINT$(T, y)$: the segments directly below and directly above the point $(T.x, y)$, not counting the segments through it.

Between two calls of SET-X the structure is an [ordered set](/ordered-set/) with predecessor and successor queries. It does not meet the laws of an ordered set or of a [dictionary](/dictionary/) over its whole life, because the order depends on $x$ and SWAP changes it without an insert or a delete. So this page names no abstract type that it implements.

## Representation

**In theory.** A balanced binary search tree, for example a [red-black tree](/red-black-tree/) as in CLRS or an [AVL tree](/avl-tree/), holds the active segments in the order at $T.x$. Each node stores a segment, not a number: the key is computed during each comparison from the segment and the current $x$. A precomputed $y$-value would go out of date as soon as the line moves. De Berg et al. store the segments in the leaves, and each internal node stores the segment of the rightmost leaf of its left subtree, to guide the search. A search with a point of the line then ends at a leaf next to the point, so the neighbors of an event point are found with one walk from the root and the leaf order.

**Exact comparisons.** With integer endpoints, the test "is the point $p$ above the segment $s = (a, b)$" is the sign of the [cross product](/cross-product/) $(b - a) \times (p - a)$, an [orientation test](/orientation-test/) with integers only. CLRS compare segments in this way. The implementation of this page uses rational numbers for $y_s(x)$ and $m_s$, which gives the same exact answers.

**The implementation.** It keeps the active segments in a Python list, sorted from bottom to top, and finds positions by [binary search](/binary-search/) with the key at the current $x$. A search costs $O(\log n)$ comparisons, as in a tree, but an insert or a delete moves $O(n)$ list entries. A balanced tree makes each update $O(\log n)$. The representation invariant at the current $x$ is:

1. the list holds each active segment once, and each of them spans $x$;
2. the values $y_s(x)$ do not decrease along the list;
3. after all the events at $x$ are handled, the list is sorted by the key $(y_s(x), m_s)$.

Part 2 makes the segments through one point of the line a contiguous block. Part 3 is the order just to the right of $x$, which is the order until the next event.

## Operations

```pseudo id=main
SET-X(T, x′)                       ▷ no two stored segments cross between T.x and x′
L1  T.x ← x′                       ▷ the stored order does not change

INSERT(T, s)                       ▷ x₁(s) ≤ T.x ≤ x₂(s)
L2  i ← the first position with key(T[i]) > key(s), where key(t) = (y_t(T.x), m_t)
L3  insert s at position i

LOCATE(T, s)                       ▷ the position of the stored segment s
L4  i ← the first position with y_T[i](T.x) ≥ y_s(T.x)
L5  while i < |T| and y_T[i](T.x) = y_s(T.x) do     ▷ the block through the point of s
L6      if T[i] = s then
L7          return i
L8      i ← i + 1
L9  error: s is not stored

DELETE(T, s)
L10 remove T[LOCATE(T, s)]

ABOVE(T, s)
L11 i ← LOCATE(T, s); return T[i + 1], or NIL if i is the last position

BELOW(T, s)
L12 i ← LOCATE(T, s); return T[i − 1], or NIL if i = 0

SWAP(T, s, t)                      ▷ t is directly above s, and y_s(T.x) = y_t(T.x)
L13 i ← LOCATE(T, s)
L14 exchange T[i] and T[i + 1]

NEIGHBORS-OF-POINT(T, y)           ▷ the point (T.x, y)
L15 lo ← the first position with y_T[i](T.x) ≥ y
L16 hi ← the first position with y_T[i](T.x) > y
L17 return (T[lo − 1], or NIL if lo = 0; T[hi], or NIL if hi = |T|)
```

**SET-X** changes only the comparator. Its precondition is what makes this safe; the correctness section explains why.

**INSERT** finds the place of the new segment by the full key. A new segment that starts on another segment, or at the start of other segments, gets a tie in $y$, and the slope puts it in the order just to the right of $x$. In a tree, line L2 is one search from the root, and line L3 is the tree insert with its rebalancing, $O(\log n)$ in total.

**LOCATE** finds a stored segment by its $y$-value at $x$ and then by identity inside its block. It does not use the slope, because a block can be in the order just to the left of $x$ (before a swap) or just to the right (after it). It costs $O(\log n + b)$, where $b$ is the size of the block, the number of stored segments through the point of $s$. In a sweep without three segments through one point, $b \le 2$.

**DELETE, ABOVE and BELOW** use LOCATE and then remove, or read a neighbor. In a tree, the neighbors are the predecessor and the successor of the node, $O(\log n)$.

**SWAP** handles a crossing of two segments. Just to the left of the crossing point, $s$ is below $t$; just to the right, $t$ is below $s$. The exchange of two adjacent entries keeps part 2 of the invariant, because the two have the same $y$ at $x$. In a tree, exchange the segments stored in the two nodes, after a search that costs $O(\log n)$.

**NEIGHBORS-OF-POINT** answers the question of an event point $p = (x, y)$ in Bentley-Ottmann: which segments are directly left and right of $p$ along the line (below and above here). Lines L15 and L16 are two binary searches by $y$ only. The stored segments in positions $lo$ to $hi - 1$ pass through $p$.

**An event.** A sweep with this structure handles all the event points with the same $x$ in this order: SET-X; DELETE each segment that ends at $x$; for each point where stored segments cross, reverse their block; INSERT each segment that starts at $x$. For two segments the reversal is a SWAP. For three or more segments through one point, de Berg et al. delete them all and insert them again, which reverses their order. After the event, the sweep tests the new pairs of neighbors for crossings to the right of $x$, and puts the crossings in the [event queue](/event-queue/).

## Example

Take $a$ from $(0, 0)$ to $(10, 10)$, $b$ from $(0, 10)$ to $(10, 0)$, $c$ from $(1, 5)$ to $(3, 5)$ and $d$ from $(2, 1)$ to $(6, 2)$. The only crossing is $a$ with $b$ at $(5, 5)$. The table shows the list from bottom to top after each operation, with $y_s(x)$ in parentheses.

| $x$ | operation | status after it | what the sweep learns |
|---|---|---|---|
| 0 | INSERT $a$ | $a(0)$ | |
| 0 | INSERT $b$ | $a(0)$, $b(10)$ | $a$ and $b$ are neighbors and cross at $(5, 5)$ |
| 1 | INSERT $c$ | $a(1)$, $c(5)$, $b(9)$ | BELOW $c = a$ and ABOVE $c = b$; no new crossing |
| 2 | INSERT $d$ | $d(1)$, $a(2)$, $c(5)$, $b(8)$ | ABOVE $d = a$; $d$ and $a$ do not cross |
| 3 | DELETE $c$ | $d(5/4)$, $a(3)$, $b(7)$ | $a$ and $b$ are neighbors again |
| 4 | NEIGHBORS-OF-POINT 5 | $d(3/2)$, $a(4)$, $b(6)$ | below is $a$, above is $b$ |
| 5 | before the event | $d(7/4)$, $a(5)$, $b(5)$ | a tie: $a$ and $b$ meet the line at one point |
| 5 | SWAP $a$, $b$ | $d(7/4)$, $b(5)$, $a(5)$ | new neighbors $d$ and $b$ do not cross |
| 6 | DELETE $d$ | $b(4)$, $a(6)$ | |
| 10 | DELETE $b$, DELETE $a$ | empty | |

The rows for $x = 1$ to $4$ show the main point: the $y$-values change at each step, but the list never needs to be rearranged. At $x = 5$ the list holds a tie, and the swap puts $b$ below $a$, which is the order for $x > 5$.

## Correctness

The structure is correct because the order of the active segments changes only at event points. If no two stored segments cross between $x$ and $x'$, then for any two of them the sign of $y_s - y_t$ is the same at each point of the open interval $(x, x')$: the difference is a linear function of $x$, and a zero would be a crossing. So the list that is sorted just to the right of $x$ is still sorted just to the left of $x'$, and at $x'$ itself its $y$-values do not decrease, by continuity. Segments that tie at $x'$ pass through a common point; just to the left of it they are in decreasing order of slope, so reversing each block gives increasing slope, the order just to the right. Deletes, inserts by the full key, and the reversal at each event then restore the invariant. The full proof, with each operation, is below.

## Complexity

Let $n$ be the number of stored segments, and $b$ the number of stored segments through the point that an operation looks at ($b \le 2$ in general position).

| operation | balanced search tree | sorted list with binary search |
|---|---|---|
| SET-X | $O(1)$ | $O(1)$ |
| INSERT | $O(\log n)$ worst case | $O(\log n)$ comparisons, $O(n)$ moves |
| DELETE | $O(\log n + b)$ worst case | $O(\log n + b)$ comparisons, $O(n)$ moves |
| ABOVE, BELOW | $O(\log n + b)$ worst case | $O(\log n + b)$ |
| SWAP | $O(\log n + b)$ worst case | $O(\log n + b)$ |
| NEIGHBORS-OF-POINT | $O(\log n)$ worst case | $O(\log n)$ |
| space | $O(n)$ | $O(n)$ |

Each comparison costs $O(1)$ arithmetic operations on the coordinates. With integer coordinates, the cross products need integers about twice as long as the coordinates.

In the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) on $n$ segments with $k$ intersection points, there are $O(n + k)$ operations on the status, each $O(\log n)$, so $O((n + k) \log n)$ time in the status. A block of $b$ segments through one intersection point costs $O(b \log n)$ to reverse; de Berg et al. bound the sum of these sizes by the number of edges of the planar subdivision that the segments form, $O(n + k)$ (Section 2.1).

**Lower bound.** In the [comparison model](/comparison-model/), $n$ inserts of segments that all cross one line, followed by a walk of ABOVE from the lowest one, sort the $n$ values $y_s(x)$. So a status structure cannot do both INSERT and ABOVE in $o(\log n)$ amortized comparisons.

## Variants

- **Detection only.** ANY-SEGMENTS-INTERSECT of CLRS (Section 33.2), after Shamos and Hoey, stops at the first crossing it finds. So it never needs SWAP, and it uses a static event queue of the $2n$ sorted endpoints. It decides in $O(n \log n)$ time whether any two of $n$ segments intersect.
- **Intervals instead of segments.** In the [rectangle intersection sweep](/rectangle-intersection-sweep/) the active objects are the $y$-intervals of the rectangles that the line crosses. Their order does not change, and the query is "which stored intervals overlap this one", so the status is an [interval tree](/interval-tree/) or a [segment tree](/segment-tree/).
- **Measure of the cross-section.** For the [area of a union of rectangles](/rectangle-union-sweep/), the status must report the total length of the union of the active $y$-intervals. A [segment tree](/segment-tree/) over the [compressed](/coordinate-compression/) $y$-values, with a cover count in each node, does this in $O(\log n)$ per update.
- **A counter array.** With $n$ rectangles, an array of cover counts over the $O(n)$ elementary $y$-intervals of the compressed coordinates is enough when $O(n)$ per update is acceptable. It gives an $O(n^2)$ sweep that is easy to write.
- **A max-heap of heights.** In the [skyline sweep](/skyline-sweep/), the status is the multiset of heights of the active buildings, and the only query is the largest one. A max-[heap](/binary-heap/) with lazy deletion of ended buildings, or a balanced tree with counts, does this in $O(\log n)$ per event.
- **Other balanced trees.** A [skip list](/skip-list/) or a [treap](/treap/) gives the same bounds in expectation. Exact comparisons matter more than the choice of tree.

## When to use it

Use a balanced search tree with a comparator at the current $x$ when the active objects are segments or curves whose order can change only at events that the sweep knows, as in [segment intersection](/segment-intersection-detection/), [Bentley-Ottmann](/bentley-ottmann-algorithm/) and the partition into [monotone pieces](/monotone-polygon-triangulation/). Use a sorted list when the number of active objects stays small, because its constants are small. When the active objects are intervals on a fixed axis and the queries are about coverage or overlap, use a segment tree, an interval tree or a counter array instead.

## Pitfalls

- **Floating-point keys.** With rounded values of $y_s(x)$, the comparator can say $s < t$, $t < u$ and $u < s$ for three segments near one point. The tree is then no longer a search tree, and searches miss stored segments. Compare with integer cross products or with rational numbers, as lines L2, L4 and L5 do.
- **Stored numbers as keys.** A tree that stores $y_s(x)$ as a number when $s$ is inserted is sorted by the old $x$ only. The key must be computed at the current $x$ in each comparison.
- **A missed swap.** If the sweep moves past a crossing point without reversing the block of line L14, the two segments are in the wrong order for the rest of the sweep, and SET-X breaks its precondition. Each crossing must be an event, or the sweep must stop at the first crossing, as in the detection variant.
- **The wrong side of a tie.** INSERT with the key $y_s(x)$ alone puts a segment that starts on another segment in an arbitrary position. The tie must be broken by the order just to the right of $x$, as the slope in line L2 does. LOCATE must not use the slope, because a block can still be in the order of the left side.
- **Wrong order of the work at an event.** If INSERT runs before the deletes and the reversals at the same $x$, it searches in a block that is not yet in slope order. Do the deletes first, then the reversals, then the inserts.
- **Vertical segments.** A vertical segment has no single $y$ at its $x$. De Berg et al. allow such segments (horizontal ones in their rotated setting) with conventions for the order at an event point (Section 2.1). A simple way is not to store it, and to handle it at its event as a range query: the stored segments whose $y$ at $x$ lies in its $y$-range are exactly the ones it meets. See [degeneracy in sweeps](/degeneracy-in-sweeps/).

## Implementations

## History

Shamos and Hoey (1976) decided whether $n$ segments intersect with a sweep that keeps the segments crossing the line in a balanced tree ordered along the line, in $O(n \log n)$ time. Bentley and Ottmann (1979) extended the sweep to report all $k$ intersections in $O((n + k) \log n)$ time, with an exchange of two segments in the status at each intersection point. CLRS present the detection algorithm with a red-black tree, and de Berg et al. present the reporting algorithm with the segments in the leaves of the tree.

## References
