---
tag: 3J25VA
kind: data-structure
slug: active-edge-table
name: Active edge table
aliases:
- AET
area: graphics-and-signals/rasterization
level: advanced
summary: The list of polygon edges that cross the current pixel row, sorted by the x of the crossing and updated from row to row, with an edge table of new edges per row.
model: real-ram
prereqs: [scanline-polygon-fill, insertion-sort]
see_also: [polygon-scan-conversion, sweep-line-technique, bentley-ottmann-algorithm, watkins-scanline-algorithm, bucket-sort, linked-list, digital-differential-analyzer, even-odd-fill-rule]
sources:
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Section 3.6, Filling Polygons (the global edge table in buckets by the first scan line, and the active edge table sorted by x)
  - book: "William M. Newman and Robert F. Sproull, Principles of Interactive Computer Graphics, second edition, McGraw-Hill, 1979"
    locator: the scan conversion of polygons with a sorted edge list
  - paper: "Gregory Ackland and Neil H. Weste, The edge flag algorithm, a fill method for raster scan displays, IEEE Transactions on Computers C-30(1), 41 to 48 (1981)"
    locator: the description of the sorted edge list method that the edge flag method replaces
---

The active edge table is the list of polygon edges that cross the center line of the current pixel row, each with the $x$ of its crossing, kept sorted by $x$. A second structure, the edge table, holds each edge in a bucket for the first row that it crosses. When the sweep moves down one row, each crossing moves by a fixed step, the edges that end leave, the list is sorted again by insertion sort, and the edges of the new bucket are merged in. It is the sweep status of [scanline polygon fill](/scanline-polygon-fill/), and over the whole image its re-sorts make at most one move for each pair of edges that intersect.

## In plain words

Picture a horizontal line that moves down the image one row at a time. The outline of a shape meets the line at a few points. The table is the list of the edges that meet the line now, in order from left to right, with the place where each one meets it.

When the line moves down one row, each meeting point slides left or right by a fixed amount that depends on the slope of its edge. Some edges end and leave the list. Some edges start and join it. A second table, sorted by the row where each edge starts, tells you which edges join.

Two meeting points change their order only where two edges cross. So the list is almost always still in order, and a simple sort that fixes small faults is fast.

## The abstract type

The table supports a sweep from row 0 to row $H - 1$ over a set of $n$ segments in the plane. It is built once from the rings of a polygon and the height $H$. Then it supports two operations:

- **NEXT-ROW** moves the sweep to the next row $j$.
- **CROSSINGS** returns the edges that are active on row $j$ as pairs $(x, d)$, sorted by $x$. Here $x$ is the exact crossing of the edge with the center line $y = j + 1/2$, and $d$ is $+1$ for an edge that runs down and $-1$ for an edge that runs up.

An edge is **active** on row $j$ when $y_{\text{top}} \le j + 1/2 < y_{\text{bot}}$. The pixel model is the one of [polygon scan conversion](/polygon-scan-conversion/): pixel $(i, j)$ is a point sample at $(i + 1/2, j + 1/2)$, as in OpenGL and Direct3D 10, not a little square, and $y$ grows downward. The half-open rule counts a vertex on a center line once where the boundary passes through it, and it makes no horizontal edge active. From the sorted crossings, a fill computes the spans of the row under the [even-odd fill rule](/even-odd-fill-rule/) or the [nonzero winding rule](/nonzero-winding-rule/).

## Representation

Each edge is a record of four fields:

| Field | Meaning |
|---|---|
| $j_1$ | the first row on which the edge is no longer active, $\lceil y_{\text{bot}} - 1/2 \rceil$ |
| $x$ | the $x$ of the edge on the center line of the current row |
| $\Delta$ | the change of $x$ from one row to the next, $(x_{\text{bot}} - x_{\text{top}}) / (y_{\text{bot}} - y_{\text{top}})$ |
| $d$ | the direction, $+1$ down and $-1$ up |

The **edge table** is an array of $H$ buckets. Bucket $j$ holds the records of the edges whose first active row is $j$, sorted by $x$ and then by $\Delta$. The **active edge table** is a list of the records of the active edges, sorted by $x$. Textbooks often use a linked list, so that a record can leave or join in constant time once its place is known. An array that is rebuilt on each row, as in the implementation here, has the same cost bound.

The model is the [real RAM](/real-ram/) with exact rational arithmetic, and the implementation keeps $x$ and $\Delta$ as Python fractions. With integer vertices, $x$ is an integer plus a fraction with denominator $y_{\text{bot}} - y_{\text{top}}$, so a program can also keep an integer numerator as an error term.

## Operations

```pseudo id=main
BUILD(rings, H)
L1  for each edge with ytop ≠ ybot, put the record (j1, x on the line of row j0, Δ, d) in bucket ET[j0],
    where j0 ← max(⌈ytop − 1/2⌉, 0) and j1 ← ⌈ybot − 1/2⌉, when j0 < min(j1, H)
L2  sort each bucket by x, then by Δ; A ← empty list; row ← −1

NEXT-ROW()
L3  if row ≥ 0 then for each record e in A do e.x ← e.x + e.Δ
    row ← row + 1; j ← row
L4  remove from A each record with j1 ≤ j
L5  sort A by x with insertion sort
L6  merge the sorted bucket ET[j] into A, by x, then by Δ
    return j

CROSSINGS()
L7  return the list of (e.x, e.d) for the records e of A, in order
```

The order of lines L3 to L6 matters. The step on line L3 moves the old records to the new center line, so line L5 compares values on the same line. The merge on line L6 comes after the sort, so new records go straight to their place and do not pay for moves.

## Example

Take the bow tie with the vertices $(0, 0)$, $(4, 4)$, $(4, 0)$, $(0, 4)$ on a grid of 4 rows. Its four edges all start in bucket 0: the diagonal $a$ from $(0, 0)$ to $(4, 4)$ with $\Delta = 1$, the right side from $(4, 4)$ to $(4, 0)$, the diagonal $c$ from $(4, 0)$ to $(0, 4)$ with $\Delta = -1$, and the left side from $(0, 4)$ to $(0, 0)$.

| Row $j$ | CROSSINGS after NEXT-ROW | Moves on line L5 | Even-odd spans |
|---|---|---|---|
| 0 | $(0, -1)$, $(1/2, +1)_a$, $(7/2, +1)_c$, $(4, -1)$ | 0 | $[3, 4)$ |
| 1 | $(0, -1)$, $(3/2, +1)_a$, $(5/2, +1)_c$, $(4, -1)$ | 0 | $[0, 1)$, $[2, 4)$ |
| 2 | $(0, -1)$, $(3/2, +1)_c$, $(5/2, +1)_a$, $(4, -1)$ | 1 | $[0, 1)$, $[2, 4)$ |
| 3 | $(0, -1)$, $(1/2, +1)_c$, $(7/2, +1)_a$, $(4, -1)$ | 0 | $[3, 4)$ |

The diagonals cross at $(2, 2)$, between the center lines $y = 1.5$ and $y = 2.5$. On row 2, line L3 gives $a$ the value $5/2$ and $c$ the value $3/2$, so the list is out of order, and line L5 makes one move. This is the only move of the whole sweep, and the bow tie has one pair of edges that cross inside it. The other pairs that meet do so at the corners, where each pair shares a vertex and is never out of order. On row 0 the span $[0, 1/2)$ holds no pixel center, so the left triangle starts only on row 1, while the right one starts on row 0: the tie rule takes a center on a left edge and not one on a right edge.

## Correctness

After NEXT-ROW returns row $j$, the list holds each edge that is active on row $j$ exactly once, with the exact $x$ of its crossing with $y = j + 1/2$, in sorted order. The proof is by induction on $j$. An edge is active on the rows $j_0 \le j < j_1$. Line L3 adds $\Delta$, which moves $x$ by one row along the edge. Line L4 removes the edges with $j_1 \le j$, line L5 sorts what is left, and line L6 merges in the edges with first row $j$, which were sorted by line L2. For the cost, two active edges change their order between two rows only if they meet at a height in between, and after the move their order is right for all later rows, because the difference of their $x$ values is linear in $y$. The full proof is below.

## Complexity

Let $n$ be the number of edges, $H$ the number of rows, $I$ the number of pairs of an edge and a row on which it is active, and $K$ the number of pairs of edges that intersect.

| Operation | Time |
|---|---|
| BUILD | $O(n \log n + H)$ |
| NEXT-ROW on row $j$ | $O(1 + A_j + A_{j-1} + m_j)$, with $A_j$ the active edges and $m_j$ the moves |
| all $H$ calls of NEXT-ROW | $O(H + I + K)$ |
| CROSSINGS | $O(A_j)$ |

The sum of $A_j$ over all rows is $I$, and the sum of $m_j$ is at most $K$, by the proof. For a simple polygon two edges meet only at a shared vertex, so $K \le n$. For a polygon that crosses itself, $K$ can be as large as $\Theta(n^2)$. The term $I$ can reach $nH$ and does not depend on the number of filled pixels. The space is $O(n + H)$.

Without the merge on line L6, new edges appended at the end of the list cost up to $A_j$ moves each in the insertion sort. Without the step before the sort, the sort compares values on different lines and the bound fails.

## Variants

- **A balanced tree.** The [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) keeps the sweep status in a [balanced binary search tree](/balanced-binary-search-tree/) and handles each crossing as an event at its exact height. The active edge table does not track crossings as events: it samples the order only on center lines and repairs it there, which is simpler when the rows are fixed.
- **Integer error terms.** With integer vertices, each record holds the integer part of $x$, a numerator and the denominator $y_{\text{bot}} - y_{\text{top}}$, and the step is done as in Bresenham's line method.
- **Polygons with depth.** The [Watkins scanline algorithm](/watkins-scanline-algorithm/) keeps the edges of many polygons in one active edge table and records for each edge the polygon it bounds, to resolve depth along each span.
- **Convex polygons.** A convex polygon has two active edges on each row, one in each chain, and needs no table.
- **Edge flags.** The edge flag method of Ackland and Weste marks the crossings in a buffer of flags and needs no sorted list.

## When to use it

Use it inside a scanline fill of general polygons on a CPU: concave shapes, holes, many rings and self-intersections. It is also the core of scanline hidden surface methods, which sweep many polygons at once. For a polygon with few edges, or for triangles, the edge function tests of [triangle rasterization](/triangle-rasterization/) need no shared state. For a sweep that needs the exact order between any two heights, use the tree of the Bentley-Ottmann algorithm.

## Pitfalls

- **Counting a vertex twice.** If an edge is active on the closed interval $y_{\text{top}} \le y \le y_{\text{bot}}$, a vertex on a center line counts once for each of its two edges, and the parity breaks for the rest of the row. Use the half-open rule.
- **Horizontal edges in the table.** They have no $\Delta$, and they must not enter.
- **Rounding of $j_0$ and $j_1$.** Rounding $y_{\text{top}}$ to the nearest integer, in place of $\lceil y_{\text{top}} - 1/2 \rceil$, puts edges on the wrong first row, so they miss or add a row.
- **Floating-point drift.** In [IEEE 754](/ieee-754/) arithmetic, adding a rounded $\Delta$ on each row lets $x$ drift, as in the [digital differential analyzer](/digital-differential-analyzer/). Two edges that meet at a vertex can then cross in the wrong order, or a crossing can move past a pixel center. Use exact fractions, integer error terms, or compute $x$ from the end points on each row.
- **The wrong sort.** A full sort of the list on each row costs $O(A_j \log A_j)$ per row even when nothing changed. Insertion sort costs $O(A_j)$ plus the moves, and the moves are bounded by the pairs that cross.
- **Ties between new edges.** Two edges that start at one vertex have the same $x$ on their first row. Sort a bucket by $x$ and then by $\Delta$, so that the edge that moves left comes first and the next row needs no move.

## Implementations

## History

The edge list that is sorted by $y$ and swept row by row comes from the scan line hidden surface methods of the late 1960s, such as the work of Wylie, Romney, Evans and Erdahl at the University of Utah in 1967 and the method of Watkins in 1970. The names edge table and active edge table are the ones that textbooks such as Foley and his coauthors use for the fill of polygons.

## References
