---
tag: PNCJ41
kind: problem
slug: skyline-problem
name: Skyline problem
aliases:
- building skyline
- city skyline
area: techniques/sweep-line
level: core
summary: Compute the outline of the union of rectangles standing on a common baseline.
prereqs: [sweep-line-technique, divide-and-conquer-paradigm]
see_also: [skyline-sweep, lower-envelope-of-segments, area-of-union-of-rectangles, rectangle-union-sweep, element-distinctness-lower-bound, merge-sort, hidden-surface-removal, pareto-front]
sources:
  - book: isbn:9780201120370
    title: Udi Manber, Introduction to Algorithms, A Creative Approach, Addison-Wesley, 1989
    locator: Chapter 5, Section 5.6, A divide-and-conquer algorithm, the skyline problem
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the main theorem and its application to element distinctness
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 8, The geometry of rectangles (measure and contour of a union of rectangles)
---

The skyline problem asks for the outline of $n$ axis-parallel rectangles, the *buildings*, that stand on a common horizontal baseline: the list of points where the height of the upper boundary of their union changes. The outline is the upper [envelope](/lower-envelope-of-segments/) of the tops of the buildings, so it is a step function with at most $2n$ steps. The [skyline sweep](/skyline-sweep/) and a [divide-and-conquer](/divide-and-conquer-paradigm/) merge both solve it in $O(n \log n)$ time, and a reduction from [element distinctness](/element-distinctness/) shows that this is optimal in the algebraic computation tree model.

## In plain words

You look at a city from far away at sunset. Each building is a dark rectangle that stands on the ground, and the buildings hide each other. You want to draw only the line where the dark area meets the sky. This line goes up and down in steps.

To describe the line, list the places where its height changes, from left to right, with the new height at each place. A gap between buildings is a part of the line at ground level. Two buildings of the same height that touch make one flat step, with no point between them. A small building in front of a taller one changes nothing. The question is how to find this list fast when there are many buildings.

## Definition

**Input.** A list of $n \ge 0$ buildings $(L_i, R_i, H_i)$, $1 \le i \le n$, with real numbers $L_i < R_i$ and $H_i > 0$. Building $i$ is the rectangle $[L_i, R_i] \times [0, H_i]$.

**The height function.** For each real $x$ let

$$f(x) = \max\{H_i : L_i \le x < R_i\}, \qquad f(x) = 0 \text{ if no } i \text{ has } L_i \le x < R_i.$$

The half-open intervals $[L_i, R_i)$ make $f$ continuous from the right, so each step of $f$ has a well-defined start.

**Output.** The *skyline* is the list of key points $(x_1, h_1), \ldots, (x_m, h_m)$ with

- $x_1 < x_2 < \cdots < x_m$,
- $f(x) = h_j$ for all $x \in [x_j, x_{j+1})$ and $1 \le j < m$, and $f(x) = 0$ for $x < x_1$ and for $x \ge x_m$ (so $h_m = 0$),
- $h_j \ne h_{j+1}$ for $1 \le j < m$, and $h_1 \ne 0$.

The last two conditions make the list unique: it is the shortest list that describes $f$, and its points are exactly the $x$ where $f$ changes value. For $n = 0$ the list is empty. Each $x_j$ is one of the $L_i$ or $R_i$, because $f$ is constant between two consecutive endpoints. So $m \le 2n$.

## Variants

- **Polygon vertices.** Output the boundary of the union as a rectilinear polygon. Each key point $(x_j, h_j)$ gives the two vertices $(x_j, h_{j-1})$ and $(x_j, h_j)$, with $h_0 = 0$, and a gap at height 0 splits the boundary into several polygons. This is the contour of the union, a special case of the contour of a union of rectangles in Preparata and Shamos, Chapter 8.
- **Closed buildings.** With closed intervals $[L_i, R_i]$ in the definition of $f$, the value of $f$ at an endpoint can change, but the outline as a set of points in the plane is the same. Two closed buildings of equal height that touch still give one step.
- **Merging two skylines.** Given the skylines of two sets of buildings, with $m_1$ and $m_2$ points, compute the skyline of the union. This takes $O(m_1 + m_2)$ time, and it is the step of the divide-and-conquer algorithm below.
- **Sorted input.** The buildings come sorted by $L_i$. This does not lower the bound: the reduction below with all $L_i$ equal still needs $\Omega(n \log n)$ time. If the buildings are sorted by $L_i$ and also by $R_i$ in the same order, so that no building starts later and ends earlier than another, the active buildings form a queue and a [monotonic deque](/monotonic-deque/) gives the skyline in $O(n)$ time.
- **Area under the skyline.** Compute $\int f(x)\,dx = \sum_{j < m} h_j (x_{j+1} - x_j)$, the area of the union of the buildings. This is a special case of the [area of a union of rectangles](/area-of-union-of-rectangles/).
- **Not the database skyline.** In databases, a "skyline query" asks for the points of a set that no other point dominates in all coordinates, the [Pareto front](/pareto-front/). That is a different problem, solved for example by the [block-nested-loop skyline](/bnl-skyline/).

## Examples

**Five buildings.** For $(2, 9, 10)$, $(3, 7, 15)$, $(5, 12, 12)$, $(15, 20, 10)$ and $(19, 24, 8)$ the skyline is

$$[(2, 10), (3, 15), (7, 12), (12, 0), (15, 10), (20, 8), (24, 0)].$$

The point $(12, 0)$ marks the gap from 12 to 15. The building $(2, 9, 10)$ ends at 9 under the taller $(5, 12, 12)$, so 9 is not a key point. The [skyline sweep](/skyline-sweep/) page traces this input step by step.

**Eight buildings.** For $(1, 5, 11)$, $(2, 7, 6)$, $(3, 9, 13)$, $(12, 16, 7)$, $(14, 25, 3)$, $(19, 22, 18)$, $(23, 29, 13)$ and $(24, 28, 4)$ the skyline is

$$[(1, 11), (3, 13), (9, 0), (12, 7), (16, 3), (19, 18), (22, 3), (23, 13), (29, 0)].$$

The building $(2, 7, 6)$ is hidden and does not appear. The building $(14, 25, 3)$ shows in two places, from 16 to 19 and from 22 to 23.

**Nested buildings.** For $(0, 10, 3)$, $(2, 4, 7)$ and $(5, 6, 7)$ the skyline is $[(0, 3), (2, 7), (4, 3), (5, 7), (6, 3), (10, 0)]$.

**Touching buildings.** For $(0, 2, 5)$ and $(2, 4, 5)$ the skyline is $[(0, 5), (4, 0)]$: there is no point at 2. For $(0, 2, 5)$ and $(2, 4, 3)$ it is $[(0, 5), (2, 3), (4, 0)]$, with no point $(2, 0)$.

**The largest output.** For the $n$ disjoint buildings $(2i, 2i + 1, 1)$, $0 \le i < n$, the skyline has $2n$ points, so the bound $m \le 2n$ is tight.

## Known algorithms

- **[Skyline sweep](/skyline-sweep/).** Sweep a vertical line over the $2n$ endpoints and keep the active heights in a max-heap with lazy deletion. $O(n \log n)$ time and $O(n)$ space.
- **Divide and conquer.** Split the buildings into two halves of sizes $\lceil n/2 \rceil$ and $\lfloor n/2 \rfloor$, solve both, and merge the two skylines $A$ and $B$. The merge walks both lists from left to right like the merge of [merge sort](/merge-sort/). It keeps the current height $h_A$ of $A$ and $h_B$ of $B$. At the next coordinate $x$, the smaller of the next $x$ values of the two lists, it updates $h_A$ if $A$ has a point at $x$ and $h_B$ if $B$ has a point at $x$, and outputs $(x, \max(h_A, h_B))$ if this value differs from the last output height. A single building $(L, R, H)$ is the skyline $[(L, H), (R, 0)]$. Each skyline of $k$ buildings has at most $2k$ points, so the merge costs $O(n)$, and $T(n) = 2T(n/2) + O(n)$ gives $O(n \log n)$ by the [master theorem](/master-theorem/). This is the algorithm of Manber, Section 5.6.
- **Incremental insertion.** Add the buildings one at a time, and merge each one into the current skyline with the merge above. The current skyline of $i$ buildings has up to $2i$ points, so the total is $O(n^2)$ time, and $\Theta(n^2)$ for $n$ disjoint buildings given from left to right with a merge that walks the whole list.
- **Brute force.** Evaluate $f$ at each of the at most $2n$ endpoints by a scan of all buildings, and keep the points where the value changes. $O(n^2)$ time.

## Bounds

**Upper bound.** $O(n \log n)$ time in the worst case, by the sweep or by divide and conquer. Both algorithms only compare coordinates and heights.

**Output size.** $m \le 2n$, and $m = 2n$ for disjoint buildings (see the examples). So no algorithm that lists the output can beat $\Omega(n)$, and the lower bound below is the stronger one.

**Lower bound.** In the [algebraic computation tree](/algebraic-computation-tree/) model, each algorithm for the skyline problem needs $\Omega(n \log n)$ operations in the worst case. Every comparison-based algorithm is such a tree, so the bound holds for them too. The proof is the reduction from element distinctness below, together with the theorem of Ben-Or (1983) that [element distinctness](/element-distinctness-lower-bound/) needs $\Omega(n \log n)$ operations in this model. So the sweep and the divide-and-conquer algorithm are optimal.

## Reductions

**From element distinctness, in $O(n)$ time.** Given real numbers $a_1, \ldots, a_n$ with $n \ge 1$, let $\mu = \min_i a_i$ and $M = \max_i a_i$, and make the buildings $(a_i, M + 1, a_i - \mu + 1)$. Each has $a_i < M + 1$ and height $a_i - \mu + 1 \ge 1$. For $x < M + 1$, the active buildings are those with $a_i \le x$, so $f(x) = \max\{a_i : a_i \le x\} - \mu + 1$ when some $a_i \le x$, and $f(x) = 0$ otherwise. This $f$ is a nondecreasing step function that rises exactly at each distinct value of the $a_i$, and it drops to 0 at $M + 1$. So the skyline has exactly $d + 1$ points, where $d$ is the number of distinct values, and its $x$ coordinates are the distinct values in increasing order, followed by $M + 1$. The numbers are distinct if and only if the skyline has $n + 1$ points. The transformation and the count take $O(n)$ operations. For $(4, 1, 3, 1)$ the buildings are $(4, 5, 4)$, $(1, 5, 1)$, $(3, 5, 3)$, $(1, 5, 1)$, and the skyline $[(1, 1), (3, 3), (4, 4), (5, 0)]$ has 4 points, not 5, so the numbers are not distinct.

**With all left ends equal.** The buildings $(0, a_i - \mu + 1, M - a_i + 1)$ all start at 0. A building with a smaller $a_i$ is taller and ends earlier, so $f$ drops at each distinct value of $a_i - \mu + 1$, and the skyline again has $d + 1$ points. For $(4, 1, 3, 2)$ the skyline is $[(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]$. So input sorted by left end does not make the problem easier.

**Sorting.** The first reduction also sorts: when the $a_i$ are distinct, the $x$ coordinates of the first $n$ key points are $a_1, \ldots, a_n$ in increasing order.

**To the upper envelope of segments.** The skyline is the upper envelope of the $n$ horizontal segments $[L_i, R_i) \times \{H_i\}$ and the baseline. Two horizontal segments at different heights do not cross, so the envelope is much simpler than the general [envelope of segments](/lower-envelope-of-segments/), where crossings give $\Theta(n \alpha(n))$ pieces.

**To the area of a union of rectangles.** The area of the union of the buildings is $\sum_{j < m} h_j (x_{j+1} - x_j)$, so it follows from the skyline in $O(m)$ time. The general [area of a union of rectangles](/area-of-union-of-rectangles/) has rectangles that do not share a baseline, and it needs a [segment tree](/segment-tree/) in the sweep instead of a heap.

## Applications

- **Hidden lines in two dimensions.** The skyline is the part of the boundary of a set of rectangles on a baseline that a viewer far above, looking down, can see, a small case of [hidden-surface removal](/hidden-surface-removal/).
- **Maximum over intervals.** Many tasks assign a value to each of $n$ intervals and ask, at each point, for the largest value of the intervals that cover it: the peak demand of overlapping reservations, the highest priority of active jobs over time, or the tallest obstacle along a line. The skyline is the answer as a step function.
- **Teaching.** The problem is a standard exercise for both the [sweep line technique](/sweep-line-technique/) and the [divide-and-conquer paradigm](/divide-and-conquer-paradigm/), because the merge of two skylines mirrors the merge of two sorted lists.

## References
