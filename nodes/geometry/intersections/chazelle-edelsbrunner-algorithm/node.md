---
tag: VR6X2D
kind: algorithm
slug: chazelle-edelsbrunner-algorithm
name: Chazelle-Edelsbrunner segment intersection algorithm
aliases:
- chazelle-edelsbrunner
area: geometry/intersections
level: research
summary: The first optimal deterministic algorithm for reporting all k intersections of n segments in the plane, in O(n log n + k) time and O(n + k) space.
solves: [all-segment-intersections]
model: real-ram
complexity:
  vars: {n: the number of segments, k: the number of intersections}
  time: {worst: O(n log n + k)}
  space: {extra: O(n + k)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Bernard Chazelle, Herbert Edelsbrunner]
  note: "Chazelle and Edelsbrunner presented the algorithm at FOCS 1988 and published the full version, An optimal algorithm for intersecting line segments in the plane, in the Journal of the ACM in 1992."
prereqs: [all-segment-intersections, bentley-ottmann-algorithm, segment-tree, trapezoidal-map]
see_also: [segment-intersection-lower-bound, red-blue-intersection, shamos-hoey-algorithm, line-arrangement, randomized-incremental-construction, segment-intersection-point, merge-sort]
sources:
  - paper: doi:10.1145/147508.147511
    title: Bernard Chazelle and Herbert Edelsbrunner, An optimal algorithm for intersecting line segments in the plane, Journal of the ACM 39(1), 1992, 1-54
    locator: the O(n log n + k) time algorithm, the construction of the subdivision with vertical visibility, the O(n + k) storage, and the amortization by a combinatorial theorem on line arrangements
  - paper: doi:10.1109/sfcs.1988.21975
    title: Bernard Chazelle and Herbert Edelsbrunner, An optimal algorithm for intersecting line segments in the plane, 29th Annual Symposium on Foundations of Computer Science (FOCS 1988)
    locator: the conference version of the algorithm
  - paper: doi:10.1145/220279.220302
    title: Ivan J. Balaban, An optimal algorithm for finding segments intersections, Proceedings of the 11th Annual Symposium on Computational Geometry (SoCG 1995), 211-219
    locator: the strip, staircase and tree search procedures, the simpler O(n log^2 n + k) version, and the optimal O(n log n + k) time algorithm in O(n) space
  - paper: doi:10.1016/0022-0000(86)90025-5
    title: Bernard Chazelle, Reporting and counting segment intersections, Journal of Computer and System Sciences 32(2), 1986, 156-182
    locator: the earlier O(n log^2 n / log log n + k) reporting algorithm
  - paper: doi:10.1007/BF02187740
    title: Kenneth L. Clarkson and Peter W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4(5), 1989, 387-421
    locator: the randomized incremental trapezoidal decomposition in O(n log n + k) expected time
  - paper: doi:10.1016/s0747-7171(08)80064-8
    title: Ketan Mulmuley, A fast planar partition algorithm, I, Journal of Symbolic Computation 10(3-4), 1990, 253-280
    locator: the randomized construction of the partition induced by segments in O(n log n + k) expected time
---

The Chazelle-Edelsbrunner algorithm reports all $k$ intersection points of $n$ line segments in the plane in $O(n \log n + k)$ time. This matches the lower bound $\Omega(n \log n + k)$, so it was the first optimal deterministic answer to the question that the [Bentley-Ottmann sweep](/bentley-ottmann-algorithm/) left open, since the sweep pays $O(\log n)$ for each crossing. Within the same time the algorithm builds the planar subdivision formed by the segments, together with the segment directly above and below every end point and crossing, which is the [trapezoidal map](/trapezoidal-map/) of the arrangement; that output is why it needs $O(n + k)$ space. The code on this page is a simpler exact method with the same main idea, labelled as such below.

## In plain words

Picture many sticks thrown on a table, and the task of listing every place where two sticks cross. A sweep that moves a ruler across the table and stops at every crossing does a small search at each stop. When there are millions of crossings, those searches add up.

The better methods cut the table into strips. A stick that runs across a whole strip is a "long" stick there. Long sticks that do not cross each other inside the strip are already sorted from bottom to top, so a short stick can find all the long sticks it crosses with one search followed by a walk. The trick is to pay for every extra step with a crossing that gets reported, so the work is the cost of sorting plus a constant per crossing.

## The problem

The input is a list of $n$ closed segments with rational coordinates. The output is every pair of segments that share a point, or every intersection point with the segments through it; see [all segment intersections](/all-segment-intersections/). The Chazelle-Edelsbrunner algorithm counts $k$ as the number of intersection points and also returns the vertical visibility map. The code below returns the pairs, with $k$ the number of intersecting pairs, and accepts every degenerate input: shared end points, collinear overlaps, vertical segments and segments of length zero.

## The algorithm

**The optimal algorithm.** Chazelle and Edelsbrunner sweep the plane, but they do not process crossings in the order of their $x$-coordinates, which is what forces a priority queue and the $\log n$ per crossing on Bentley-Ottmann. Instead they build the vertical decomposition of the segments: every end point and every crossing shoots a vertical ray up and down to the next segment, and the plane is cut into trapezoids. The segments are organized by a hierarchy of vertical slabs in the style of a [segment tree](/segment-tree/), so that a segment is "long" in a few slabs and "short" in the others. The trapezoids are discovered in an order that follows the structure of the arrangement, so that each crossing and each trapezoid costs $O(1)$ amortized, and only the end points pay $O(\log n)$. The amortization rests on a combinatorial theorem about arrangements of lines proved in the paper. The construction is long and the paper runs to 54 pages, so this page does not implement it.

**The implemented method.** The code uses a simpler slab tree of staircases, close to the simple version of Balaban's algorithm. A *staircase* of a strip is a set of segments that cross the whole strip and do not meet inside it, so they are sorted from bottom to top at every $x$ in the strip.

```pseudo id=main
STAIR-TREE(S)
L1  shear the plane by x ← x + λy, λ small and exact, so that distinct end points get distinct x
L2  report every pair of segments with a common end point
L3  X ← the sorted x of the end points; on the slab tree over X give each segment its canonical nodes Long(v) and the nodes Inner(v) where it has an end inside
L4  SEARCH(root, empty list)
SEARCH(v, P)                     ▷ v has the strip [x_b, x_e]; P spans it and is sorted at x_b
L5  L ← the merge of P and Long(v), in the order at x_b
L6  (Q, rest) ← SPLIT(L): scan L and put s on top of the staircase Q if it misses the top stair in the strip, else in rest
L7  for each s in rest: walk up and down Q from the place of s and report every stair that s meets
L8  for each t in Inner(v): binary search the place of its left end in Q, then walk and report
L9  if v is a leaf then report the points at x_b against L, and R ← STRIP(rest)
L10 else R ← SEARCH(right child, SEARCH(left child, rest))
L11 return the members of P, in the order at x_e of the merge of Q and R
STRIP(L)                         ▷ every segment of L crosses the whole leaf strip
L12 while |L| ≥ 2
L13   (Q, L) ← SPLIT(L) and report as in line L7, keeping each Q
L14 merge the staircases and the last L in the order at x_e and return the result
```

Line L1 is an exact linear map, so it changes no answer, and after it no segment of positive length is vertical and each end point coordinate $x = X_i$ belongs to one end point. Line L3 is the segment tree of the $x$-ranges: $\mathrm{Long}(v)$ holds the segments for which $v$ is a canonical node, and $\mathrm{Inner}(v)$ holds the segments that end inside the strip of $v$, and the points that lie in it. Lines L6 and L7 are the staircase step: a segment that is not put on the staircase meets the top stair, so it pays for itself with a reported pair. Because the stairs are sorted everywhere in the strip, the stairs that a segment meets form one block next to its place, and a walk from that place finds them (Lemma 3 of the proof). Line L10 passes the non-stairs to both children, and the left child returns them in the order at the middle line, so the right child needs no sorting. Line L9 handles a leaf strip, where all present segments cross the strip and STRIP repeats the staircase step until nothing is left.

## Example

$s_0 = (0, 0)(8, 8)$, $s_1 = (1, 7)(9, 1)$, $s_2 = (2, 4)(10, 4)$, $s_3 = (3, 1)(7, 3)$. All end points have distinct $x$, so line L1 does nothing, and $X = 0, 1, 2, 3, 7, 8, 9, 10$ gives $7$ leaf strips. The table lists the nodes where something happens; at the other nodes $L$ has at most one segment and nothing is reported.

| strip | $P$ | Long | Inner | stairs $Q$ | rest | reported |
| --- | --- | --- | --- | --- | --- | --- |
| $[0, 10]$ | | | $s_0, s_1, s_2, s_3$ | | | |
| $[0, 3]$ | | $s_0$ | $s_1, s_2$ | $s_0$ | | none: $s_1$ and $s_2$ meet $s_0$ only right of $x = 3$ |
| $[3, 10]$ | | $s_2$ | $s_0, s_1, s_3$ | $s_2$ | | $(s_2, s_0)$ at $(4, 4)$, $(s_2, s_1)$ at $(5, 4)$ |
| $[3, 8]$ | | $s_0, s_1$ | $s_3$ | $s_0$ | $s_1$ | $(s_0, s_1)$ at $(31/7, 31/7)$ |
| $[3, 7]$ (leaf) | $s_1$ | $s_3$ | | $s_3$ | $s_1$ | $(s_3, s_1)$ at $(33/5, 14/5)$ |
| $[7, 8]$ (leaf) | $s_1$ | | | $s_1$ | | |

In the strip $[3, 8]$ both $s_0$ and $s_1$ are long; at $x = 3$, $s_0$ is lower, so it is the first stair, and $s_1$ meets it inside the strip, so $s_1$ goes to rest, is reported against $s_0$, and is passed to both children. In the leaf $[3, 7]$ it meets the long segment $s_3$, and in the leaf $[7, 8]$ it is alone. The output is the $4$ pairs $(0, 1), (0, 2), (1, 2), (1, 3)$, each reported once.

## Correctness

The proof for the implemented method is in [proofs/correctness.md](proofs/correctness.md). Two facts carry it. First, a staircase is sorted on the whole strip, so the stairs that a segment or a point meets form one block next to its place at the left end, and the walks of lines L7 and L8 find exactly that block. Second, every meeting pair without a common end point is *alive* at some node: its common point lies in the strip, one segment is in $L$ and the other is in $L$ or is inner. At that node the pair is reported, or it stays alive at a child, so it is reported by the time the search reaches a leaf. Pairs with a common end point are the only ones that can fall between two strips, and line L2 reports them.

For the optimal algorithm, Chazelle and Edelsbrunner prove that the trapezoids found by their sweep are exactly the trapezoids of the vertical decomposition, so every crossing appears as a vertex of the map.

## Complexity

**The optimal algorithm.** $O(n \log n + k)$ time, which is optimal: $\Omega(n \log n)$ holds already for $k = 0$ by the [segment intersection lower bound](/segment-intersection-lower-bound/), and $\Omega(k)$ is the output. The space is $O(n + k)$, because the vertical map is built.

**The implemented method.** Each segment is in $O(\log n)$ sets $\mathrm{Long}(v)$ and $\mathrm{Inner}(v)$, at most two of each per level, so the binary searches of line L8 cost $O(n \log^2 n)$ in total and the presorting of the long lists $O(n \log^2 n)$. A segment of rest meets the top stair, so $|\mathit{rest}_v|$ is at most the number of pairs reported at $v$. Passing to two children doubles this, which gives $O(n \log^2 n + K)$ time, where $K$ is the number of reports with repetition. When no two segments overlap in more than a point, each pair is reported only a constant number of times, so $K = O(k)$ and the time is $O(n \log^2 n + k)$, the bound of Balaban's simple version. Collinear overlaps can be reported more often, and the set of found pairs removes the repeats. The space is $O(n \log n + k)$ for the tree and the output. The tests count the work and check it against $4 (n \log_2^2 n + k)$.

## Properties

- **Output.** The optimal algorithm returns the vertical decomposition, with every crossing and the segments above and below every vertex; the implemented method returns only the pairs.
- **Exact.** The implemented method uses only orientation tests, comparisons of heights at end point coordinates, and an exact shear, with `Fraction` coordinates.
- **Deterministic.** Both are deterministic, unlike the randomized algorithms of Clarkson and Shor and of Mulmuley with the same expected bound.
- **Practical.** Chazelle and Edelsbrunner report that their algorithm was implemented and that it uses much less space in practice than the worst case.

## Variants and improvements

- **Balaban (1995).** A deterministic algorithm with the same time $O(n \log n + k)$ and only $O(n)$ space, built from strips and staircases as above. Its simpler version takes $O(n \log^2 n + k)$; the optimal one speeds up the location of inner segments in the staircases, which costs $O(\log n)$ per segment and level here.
- **Randomized incremental construction.** Clarkson and Shor (1989) and Mulmuley (1988, 1990) insert the segments in random order into a [trapezoidal map](/trapezoidal-map/) and report all crossings in $O(n \log n + k)$ expected time with $O(n + k)$ space; these are much simpler to implement. See [randomized incremental construction](/randomized-incremental-construction/).
- **Chazelle (1986).** An earlier deterministic algorithm with $O(n \log^2 n / \log \log n + k)$ time, the first with a linear term in $k$.
- **Red-blue intersection.** When the segments come in two colour classes without crossings inside a class, simpler methods reach the same bounds; see [red-blue intersection](/red-blue-intersection/).
- **Bentley-Ottmann.** The plane sweep with $O((n + k) \log n)$ time and $O(n)$ space is the usual choice in practice.

## When to use it

The optimal deterministic algorithm matters in theory and when $k$ is large compared with $n$, so that the factor $\log n$ on the crossings of Bentley-Ottmann dominates. In practice the randomized trapezoidal map is the usual way to reach the same expected bound, and Bentley-Ottmann is the usual way when $k$ is small. The staircase method of this page is a reasonable exact choice when many crossings are expected and simple code is wanted: it has no priority queue and never computes a crossing point to order events.

## Pitfalls

- **Pairs on a strip boundary.** Two segments that only touch at a common end point on a line $x = X_i$ may never be long in a common strip; without line L2 they are missed. A crossing of two segments exactly on $x = X_i$ is not a problem, since both run on into the next strip.
- **Vertical segments and equal $x$.** The slab tree needs the strips between distinct end point coordinates, and a vertical segment crosses no strip. Line L1 removes both problems with an exact shear; a shear with a float slope can change which segments meet.
- **Staircases in the closed strip.** SPLIT at line L6 must test meeting in the closed strip, including touching at $x_b$ or $x_e$. Testing only proper crossings lets two stairs touch, so the stairs are no longer strictly ordered, and the block property behind the walks of lines L7 and L8 no longer holds.
- **Order at the middle line.** At line L10 the right child needs rest sorted at the middle line, which the left child returns. Reusing the order at $x_b$ is wrong, since non-stairs cross each other inside the left half.
- **Points.** A segment of length zero is never long. Line L3 must make it inner on the half-open strips that hold it, and line L9 must test it against all of $L$ at a leaf, or a point on the boundary of two canonical strips of a segment is missed.

## Implementations

## History

Bentley and Ottmann's sweep of 1979 reported intersections in $O((n + k) \log n)$ time, and Chazelle (1986) gave the first method with a term linear in $k$. Chazelle and Edelsbrunner presented the optimal $O(n \log n + k)$ algorithm at FOCS 1988; the journal version appeared in the Journal of the ACM in 1992. In the same years, Clarkson and Shor and Mulmuley reached the same bound in expectation with randomized incremental methods, which became the standard practical route. Balaban (1995) gave a second optimal deterministic algorithm that also uses only linear space.

## References
