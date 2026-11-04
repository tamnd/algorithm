---
tag: E3PVVE
kind: data-structure
slug: li-chao-tree
name: Li Chao tree
aliases:
- Li Chao Tree
- Li Chao segment tree
area: data-structures/range-query-structures
level: advanced
summary: A segment tree over x coordinates storing a line per node, supporting line insertion and minimum or maximum queries at a point.
implements: [range-query-structure]
model: word-ram
complexity:
  vars: {C: the number of possible query abscissas, n: the number of inserted lines}
  time: {worst: O(log C)}
  space: {extra: "O(min(n, C))"}
prereqs: [segment-tree, convex-hull-trick]
see_also: [dynamic-segment-tree, lazy-propagation, sweep-line-technique, point-update-range-min-query, binary-search, divide-and-conquer-paradigm, monotonic-stack]
sources:
  - url: https://cp-algorithms.com/geometry/convex_hull_trick.html
    title: cp-algorithms, Convex hull trick and Li Chao tree
    locator: the section Li Chao tree (functions that cross at most once, the line kept at each node, add_line and get, and the cost O(log C))
  - url: https://oi-wiki.org/ds/li-chao-tree/
    title: OI Wiki, 李超线段树 (Li Chao segment tree)
    locator: the sections 过程 (insertion of a segment over its O(log n) nodes, in O(log^2 n) time) and 合并 (merging two trees)
---

A Li Chao tree keeps a set of lines $y = a x + b$ and answers, for a query abscissa $x$, the smallest value $\min_i (a_i x + b_i)$ of any line at $x$. It is a [segment tree](/segment-tree/) over the possible abscissas, $C$ of them, in which each node stores at most one line: the line that is lowest at the middle of the node's range among those that reached the node. Inserting a line walks down one path and swaps lines on the way, and a query takes the minimum over the lines on the path to $x$; both take $O(\log C)$ time. It solves the same problem as the dynamic [convex hull trick](/convex-hull-trick/), with shorter code, any order of slopes, and no division, and it works for any family of functions in which two functions cross at most once.

## In plain words

You have many straight roads drawn on a chart, each going up or down at its own steady slope, and someone asks "at this point of the chart, which road is lowest?". Checking every road is slow when there are many.

The tree splits the chart into halves, quarters, and so on. Each piece keeps the one road that is lowest at the middle of that piece. When a new road comes, compare it with the kept road at the middle. Keep the lower one there. The other one can still win only on one side of the middle, because two straight roads cross at most once, so send it down to that side and repeat. To answer a question, walk from the top to the piece of the point and take the lowest kept road you met.

## The abstract type

A set $L$ of lines, empty at the start, over a fixed domain $X = \{x_0 < x_1 < \cdots < x_{C-1}\}$ of query abscissas, often the integers in $[X_0, X_1)$. The operations are:

- $\textsc{insert}(f)$: add the line $f(x) = a x + b$ to $L$;
- $\textsc{query}(x)$ with $x \in X$: return $\min_{f \in L} f(x)$, or $+\infty$ if $L$ is empty.

The maximum version negates the lines. The structure never deletes lines. The same code works for any functions in which each two cross at most once on $X$, such as segments of parabolas $y = (x - c)^2 + d$ with equal leading coefficients.

## Representation

A segment tree over the index range $[0, C)$ of $X$, as an array of $4C$ slots or as a [dynamic segment tree](/dynamic-segment-tree/) that creates nodes on demand. A node $v$ over $[lo, hi)$ with $hi - lo \ge 2$ has the middle $mid = \lfloor (lo + hi) / 2 \rfloor$, the left child over $[lo, mid)$ and the right child over $[mid, hi)$, and it stores one line $\mathit{line}[v]$ or nil. The invariant is:

> **(LC)** For every inserted line $f$ and every $x \in X$, some line $g$ stored on the path from the root to the leaf of $x$ has $g(x) \le f(x)$.

So the minimum over the path is the minimum over all lines, and the query only reads the path.

## Operations

```pseudo id=main
INSERT(f)                                  ▷ add the line f to the set
L1  v ← root, lo ← 0, hi ← C
L2  loop
L3      if line[v] = nil then line[v] ← f, return
L4      mid ← ⌊(lo + hi) / 2⌋
L5      if f(mid) < line[v](mid) then swap f and line[v]    ▷ the node keeps the line lowest at mid
L6      if hi − lo = 1 then return
L7      if f(lo) < line[v](lo) then v ← left(v), hi ← mid
L8      else if f(hi − 1) < line[v](hi − 1) then v ← right(v), lo ← mid
L9      else return                        ▷ f is nowhere better on [lo, hi)
```

Here $f(i)$ means $f(x_i)$ for an index $i$. After line L5 the node line $g$ has $g(mid) \le f(mid)$. Since $f - g$ is linear, the sign change, if any, is on one side of $mid$: if $f(lo) < g(lo)$, then $f$ can win only on $[lo, mid)$, and if $f(hi - 1) < g(hi - 1)$, only on $(mid, hi)$.

```pseudo id=query
QUERY(x)                                   ▷ x is an index in [0, C)
L10 v ← root, lo ← 0, hi ← C, best ← +∞
L11 while v exists and line[v] ≠ nil do
L12     best ← min(best, line[v](x))
L13     if hi − lo = 1 then break
L14     mid ← ⌊(lo + hi) / 2⌋
L15     if x < mid then v ← left(v), hi ← mid else v ← right(v), lo ← mid
L16 return best
```

A node is filled before any of its children, because INSERT fills the first empty node on its path and stops, so the query may stop at the first empty node.

## Example

Take the integer domain $[0, 8)$ and insert, in this order, $A: y = 5$, $B: y = x$, $C: y = 7 - x$ and $D: y = 12 - 2x$.

| insert | at the root $[0, 8)$, mid 4 | below | stored after |
|---|---|---|---|
| $A$ | empty, place $A$ | | root $A$ |
| $B$ | $B(4) = 4 < A(4) = 5$: swap, carry $A$ | $A(0) = 5 \ge B(0) = 0$, $A(7) = 5 < B(7) = 7$: go right, place $A$ at $[4, 8)$ | root $B$, $[4,8)$: $A$ |
| $C$ | $C(4) = 3 < B(4) = 4$: swap, carry $B$ | $B(0) = 0 < C(0) = 7$: go left, place $B$ at $[0, 4)$ | root $C$, $[0,4)$: $B$, $[4,8)$: $A$ |
| $D$ | $D(4) = 4 \ge C(4) = 3$: keep $C$; $D(7) = -2 < C(7) = 0$: go right | at $[4, 8)$, mid 6: $D(6) = 0 < A(6) = 5$, swap, carry $A$; $A(4) = 5 \ge 4$ and $A(7) = 5 \ge -2$: drop $A$ | root $C$, $[0,4)$: $B$, $[4,8)$: $D$ |

The line $A$ is dropped, which is right: on $[4, 8)$ it is above $D$ everywhere. The queries give $\textsc{query}(2) = \min(C(2), B(2)) = \min(5, 2) = 2$, $\textsc{query}(5) = \min(C(5), D(5)) = \min(2, 2) = 2$ and $\textsc{query}(7) = \min(0, -2) = -2$, which are the true minima over the four lines.

## Correctness

INSERT keeps (LC). Follow the carried line $f$ and the node line $g$ at a node over $[lo, hi)$. After line L5, $g(mid) \le f(mid)$, and the node keeps $g$; the line that was swapped down is the carried one from now on, so it is enough to show that the carried line keeps (LC) on $[lo, hi)$. If the walk stops at line L9, then $f \ge g$ at $lo$ and at $hi - 1$, hence on all of $[lo, hi)$ because $f - g$ is linear. If it goes left at line L7, then $f - g$ is negative at $lo$ and non-negative at $mid$, so it is non-negative on $[mid, hi)$, where $g$ covers $f$; the left part is handled further down. If it goes right at line L8, then $f \ge g$ at $lo$ and at $mid$, so on $[lo, mid]$, and the right part is handled further down. A line placed at line L3 is on the path of every $x$ in its node. Lines already stored deeper do not move. QUERY returns the minimum over the path, which by (LC) is the minimum over all lines. The [proof](proofs/correctness.md) writes this out.

## Complexity

The tree has $\lceil \lg C \rceil + 1$ levels. INSERT does $O(1)$ work per level on one path, and so does QUERY, so both take $O(\log C)$ time with $O(1)$ evaluations of lines per level. Each insertion fills at most one empty node, so at most $\min(n, 2C - 1)$ nodes hold lines; an array tree has $4C$ slots, and a dynamic tree that creates a node only when it places a line there has at most $n$ nodes.

For real abscissas, the domain is the sorted set of query points, known in advance, or an interval of reals cut down to a precision $\varepsilon$, with $C = (X_1 - X_0) / \varepsilon$.

## Variants

- **Segments instead of lines.** To insert a line that is valid only on $[x_l, x_r]$, cut the range into the $O(\log C)$ canonical nodes of the segment tree and run INSERT from each of them, for $O(\log^2 C)$ time per segment; this is the form described on OI Wiki.
- **Maximum.** Insert $(-a, -b)$ and negate the answer, or flip the comparisons.
- **Functions that cross once.** Any family in which two members cross at most once works unchanged, for example $y = a x^2 + b x + c$ with a common $a$.
- **Merging Li Chao trees.** Two trees over the same domain can be merged by inserting the lines of one node into the other recursively; OI Wiki shows that merges over $n$ nodes in total cost $O(n \log C)$, because each move of a line either takes it one level deeper or drops it.
- **Persistent Li Chao tree.** Path copying on INSERT keeps every version, for queries on the lines added up to a time $t$.

## When to use it

Use a Li Chao tree for dynamic programming of the form $dp_i = \min_j (m_j \cdot x_i + c_j) + w_i$ when the slopes $m_j$ or the query points $x_i$ are not monotone, so that the monotone [convex hull trick](/convex-hull-trick/) with a deque does not apply. It needs no fractions or intersection points, so it avoids the precision and overflow problems of hull code, and it adds lines in any order. If both the slopes and the queries are sorted, the deque version is $O(1)$ amortized and faster. If lines must be deleted, use the hull with offline [divide and conquer](/divide-and-conquer-paradigm/) over time, or a segment tree on time of Li Chao trees.

## Pitfalls

- **Comparing at the wrong points.** The test at line L8 must use $hi - 1$, the last point of the range, not $hi$, which belongs to the next node; with real domains use the closed interval and a midpoint that both children share.
- **Overflow.** $a x + b$ can exceed 64 bits for slopes and abscissas near $10^9$ and offsets near $10^{18}$; check the ranges or use wider arithmetic.
- **Empty answer.** With no lines, the query must return $+\infty$ or a flag, not the value of a default line $0 x + 0$.
- **Query points outside the domain.** The tree answers only for $x \in X$. A query at a new point needs the domain to be known in advance, or a domain over all integers in a range.
- **Ties.** With $\le$ in place of $<$ at line L5, equal lines are swapped forever without harm, but a strict test avoids needless work.

## Implementations

## History

The structure is named after Li Chao (李超), and it spread through Chinese competitive programming in the early 2010s, where it is called 李超线段树, the Li Chao segment tree. English-language teaching material, such as the cp-algorithms page, presents it next to the convex hull trick as the simpler alternative for adding lines in any order.

## References
