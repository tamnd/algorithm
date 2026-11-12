---
tag: Z8FKJW
kind: algorithm
slug: watkins-scanline-algorithm
name: Watkins' scanline algorithm
aliases:
- Watkins' algorithm
area: graphics-and-signals/visibility
level: advanced
summary: Hidden surface removal one scanline at a time, with a sorted list of edge crossings that changes little from line to line, and a split of each span only where the front surface changes.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: the number of triangles, W: the image width in pixels, H: the image height in pixels, k: "the number of pairs of an edge and a scanline that it crosses", I: the number of moves of the insertion sort over all scanlines, s: "the number of span pieces popped, over all scanlines", c: the largest number of triangles over one span}
  time: {worst: O(n + W H + k + I + s c)}
  space: {extra: O(n + W)}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1970
  people: [Gary S. Watkins]
  note: Watkins described the algorithm in his 1970 University of Utah PhD thesis, as a visible surface method fast enough for real-time hardware.
prereqs: [hidden-surface-removal, scanline-polygon-fill, active-edge-table]
see_also: [z-buffer, warnock-algorithm, object-space-vs-image-space, visibility-coherence, sweep-line-technique, insertion-sort, polygon-scan-conversion, painters-algorithm]
sources:
  - paper: "Gary Scott Watkins, A Real-Time Visible Surface Algorithm, PhD thesis, University of Utah, Computer Science Department, report UTEC-CSc-70-101, June 1970"
    locator: the whole thesis (the sorted edge list per scanline, the spans between crossings, and the subdivision of spans)
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the sections on the scan-line algorithms and on the coherence they use
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 15, the section on scan-line algorithms (the edge table, the active edge table and the spans)
---

Watkins' scanline algorithm solves [hidden surface removal](/hidden-surface-removal/) one row of pixels at a time. On each scanline, the edges of the polygons cross the line at points that a sorted list holds; between two neighbor crossings the set of polygons over the line does not change, and this interval is a *span*. In each span the algorithm compares the depths of these polygons only at the ends of the span. If one polygon is in front at both ends, it is in front on the whole span; if not, the span is split where the two depth lines cross. The list of crossings changes little from one scanline to the next, so it is kept with the [active edge table](/active-edge-table/) of [scanline polygon fill](/scanline-polygon-fill/).

## In plain words

Draw the picture one row at a time, from the top. On a row, the outlines of the shapes cut the row into pieces. Inside one piece, the same shapes are over the row all the way across.

For each piece, look at its two ends. If the same shape is nearest at both ends, it is nearest on the whole piece, because flat shapes cannot cross twice. Paint the piece with it at once. If the nearest shape is different at the two ends, the two shapes cross somewhere in the piece. Cut the piece at the crossing, and look at both halves in the same way.

The next row is almost the same as this one, so the list of cut points only moves a little. That makes each row cheap.

## The problem

The input is a list of $n$ triangles in screen space and an image of $W \times H$ pixels. A vertex is $(x, y, z)$ with $x$ to the right and $y$ down in pixel units, and $z$ the depth, smaller nearer, affine in $x$ and $y$ on each triangle. Scanline $j$ is the line $y = j + \tfrac12$ through the pixel centers $(i + \tfrac12, j + \tfrac12)$ of row $j$. The output at each pixel is the covering triangle with the least depth at the center, the one with the smaller index on a tie, or the background.

To keep the edge cases simple, no vertex has $y = j + \tfrac12$, so a scanline never passes through a vertex or along an edge; a renderer gets this by a fill rule for vertices, or by moving the vertices by a tiny amount. Then a triangle meets scanline $j$ in an interval $[x_l, x_r)$, closed at the left, which is the [top-left fill rule](/top-left-fill-rule/) on that line. With rational coordinates every step is exact.

## The algorithm

The *edge table* ET holds each edge in the bucket of the first scanline that it crosses, with its triangle, its $x$ on that scanline, its step $\delta = \Delta x / \Delta y$ per scanline and its last scanline. The *active edge list* AEL holds the edges that cross the current scanline, sorted by $x$.

```pseudo id=main
WATKINS(W, H, T)
L1  put each edge that crosses a scanline in ET[its first scanline], as (triangle, x, δ, last)
L2  for j ← the first nonempty bucket to H − 1 do
L3      add the edges of ET[j] to the AEL
L4      sort the AEL by x with insertion sort           ▷ it is almost sorted
L5      for each crossing e of the AEL, left to right: toggle e.triangle in the set S
L6          the span is [e.x, the next x); let i_0 .. i_1 be the pixel centers in it
L7          push (i_0, i_1); while the stack is not empty: pop (lo, hi)
L8              p ← the nearest of S at center lo; q ← at center hi; if p = q then give pixels lo..hi to p
L9              else cut where the depths of p and q are equal; push (cut, hi) and (lo, cut − 1)
L10     for each edge of the AEL: x ← x + δ; drop it if j is its last scanline
```

Line L5 works because each triangle has exactly two crossings on a scanline it meets: entering it and leaving it. The set $S$ holds the triangles that cover the open span. Line L9 sets $x^*$ to the point where $z_p(x) = z_q(x)$ on the scanline, and the cut to the first pixel center at or right of $x^*$; when a center is exactly at $x^*$, it goes to the half of the triangle with the smaller index. The cut is strictly inside $[lo, hi]$, so each split makes the pieces smaller.

## Example

Width 8, height 2. Triangle $A = ((0,0,0), (8,0,8), (0,2,0))$ has depth $z = x$. Triangle $B = ((0,0,4), (8,0,4), (8,2,4))$ has depth 4.

On scanline 0 ($y = \tfrac12$), $A$ covers $[0, 6)$ and $B$ covers $[2, 8)$, so the AEL is $0, 2, 6, 8$, and there are three spans.

| span | $S$ | ends | result |
|---|---|---|---|
| $[0, 2)$, pixels 0 to 1 | $\{A\}$ | $A$, $A$ | fill with $A$ |
| $[2, 6)$, pixels 2 to 5 | $\{A, B\}$ | $A$ at 2.5 (depth 2.5 < 4), $B$ at 5.5 (4 < 5.5) | split at $x^* = 4$: pixels 2 to 3 get $A$, pixels 4 to 5 get $B$ |
| $[6, 8)$, pixels 6 to 7 | $\{B\}$ | $B$, $B$ | fill with $B$ |

On scanline 1 ($y = \tfrac32$), $A$ covers $[0, 2)$ and $B$ covers $[6, 8)$, with nothing between. The image is

```
AAAABBBB
AA....BB
```

and the algorithm made one split. A z-buffer does 12 depth tests on row 0, one for each of the 12 fragments; here row 0 pops 5 pieces: the 3 spans and the 2 halves of the split.

## Correctness

The AEL after line L4 holds exactly the edges that cross scanline $j$, at their exact $x$, sorted: line L1 starts each edge at its first scanline, line L10 steps it by $\delta$ and drops it after its last one, and insertion sort sorts. Each triangle over the scanline contributes two crossings, so after the toggle at a crossing $S$ is the set of triangles that cover the span to its right. On a span the depth of each triangle of $S$ is affine in $x$. If $p$ wins at both ends against $m$, the difference $z_p - z_m$ is at most 0 at both ends, so by convexity it is at most 0 in between, and where it is 0 the index of $p$ is smaller: $p$ wins at every center. If the winners differ, the cut at $x^*$ is correct for $p$ against $q$, and the two halves are handled by the same argument. The proof file gives the details, including the termination.

## Complexity

The edge table costs $O(n + H)$ to build with buckets. Over all scanlines, the AEL holds $k$ entries, and the steps of line L10 cost $O(k)$. Insertion sort costs $O(k + I)$, where $I$ is the number of moves. Two edges that were in the list on the scanline before swap places only if they cross between the two scanlines, and a new edge moves at most past the whole list. So $I$ is at most the number of pairs of edges that cross in the image, plus $O(n)$ moves for each new edge. Each popped piece costs $O(c)$ for the two nearest choices, so $O(s c)$ in all, and the fills cost $O(W)$ per scanline. The total is $O(n + W H + k + I + s c)$.

The number of pieces $s$ is at most the number of spans plus twice the number of splits, and a split happens only when the front triangles at the two ends of a piece differ, so that two triangles cross in depth inside the span. For scenes without such crossings, $s$ is the number of spans. The extra space is the edge table, the AEL and a stack of at most $O(W)$ pieces per scanline.

## Properties

- **Scanline coherence.** The AEL changes little from one scanline to the next, so it is updated, not rebuilt.
- **Span coherence.** A whole span is decided by two choices at its ends, not one per pixel. This is the main saving over a per-pixel depth test.
- **One row at a time.** The output comes out in the order of the display, row by row, with memory for one scanline, not a depth buffer. This is what made the method fit the real-time hardware of its time.
- **Exact.** With rational coordinates the output equals the brute-force answer at each pixel center.
- **Image space, with object-space spans.** The spans and cuts are exact geometry on each scanline, and the answers are per pixel. See [object space and image space](/object-space-vs-image-space/).

## Variants and improvements

- **Scanline z-buffer.** Replace the span logic by a depth buffer of one row. It is simpler, needs $O(W)$ memory, and gives the same output, but compares depths at each covered pixel.
- **Intersections in advance.** Find the lines where triangles cut through each other before the sweep, and add them as edges, so that no span needs a split.
- **Coverage.** Keep the exact $x$ of the crossings and give each edge pixel the fraction of each span in it, for antialiasing along $x$.
- **Plane sweep.** The same sweep of a line over the image with a sorted list of crossings is the [sweep line technique](/sweep-line-technique/) of computational geometry.

## When to use it

Use it where the output must be produced in scan order with memory for one row, as in early display hardware and in printers and plotters that work by bands, or to study scanline and span coherence. Use a [z-buffer](/z-buffer/) for real-time rendering on modern hardware, where memory is cheap and per-pixel tests are fast.

## Pitfalls

- **Vertices on scanlines.** A scanline through a vertex or along a horizontal edge makes the counts of crossings odd or double. Use a half-open rule for the $y$ range of each edge, or move the vertices off the scanlines.
- **Depth at one point only.** Deciding a span by the depths at its left end, or at its middle, is wrong where two triangles cross inside it. Compare at both ends, and split.
- **The cut.** The cut must be strictly between the two end centers; a cut that can land on $lo$ or past $hi$ makes the loop run forever.
- **Sorting.** Re-sort the AEL after the step of line L10, not before; edges that cross between scanlines swap places there. Insertion sort is right because the list is almost sorted.

## Implementations

## History

Watkins described the algorithm in 1970 in his PhD thesis at the University of Utah, as a visible surface method fast enough to run in real-time hardware. It continued the scanline methods of Wylie, Romney, Evans and Erdahl (1967) and of Bouknight (1970), and added the subdivision of spans where the front surface changes. Sutherland, Sproull and Schumacker included it among the ten algorithms of their 1974 survey.

## References
