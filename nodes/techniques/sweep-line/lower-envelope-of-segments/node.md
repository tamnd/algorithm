---
tag: RTEWXY
kind: problem
slug: lower-envelope-of-segments
name: Lower envelope of segments
aliases:
- lower envelope
area: techniques/sweep-line
level: advanced
summary: Compute the pointwise minimum of n line segments or functions as a piecewise description.
prereqs: [inverse-ackermann-function, convex-hull, divide-and-conquer-paradigm]
see_also: [skyline-problem, convex-hull-trick, li-chao-tree, line-arrangement, kinetic-heap, hidden-surface-removal, element-distinctness-lower-bound, sweep-line-technique]
sources:
  - book: isbn:9780521470254
    title: Micha Sharir and Pankaj K. Agarwal, Davenport-Schinzel Sequences and Their Geometric Applications, Cambridge University Press, 1995
    locator: Chapter 1 (lower envelopes and Davenport-Schinzel sequences), Chapter 2 (sequences of order 3), Chapter 4 (realization by lower envelopes of segments)
  - paper: doi:10.1007/BF02579170
    title: "Sergiu Hart and Micha Sharir, Nonlinearity of Davenport-Schinzel sequences and of generalized path compression schemes, Combinatorica 6(2) (1986), 151-177"
    locator: the main theorem, lambda_3(n) = Theta(n alpha(n))
  - paper: doi:10.1007/BF02187894
    title: "Ady Wiernik and Micha Sharir, Planar realizations of nonlinear Davenport-Schinzel sequences by segments, Discrete and Computational Geometry 3 (1988), 15-47"
    locator: the main theorem (n segments whose lower envelope has Omega(n alpha(n)) pieces)
  - paper: doi:10.1016/0020-0190(89)90136-1
    title: "John Hershberger, Finding the upper envelope of n line segments in O(n log n) time, Information Processing Letters 33(4) (1989), 169-174"
    locator: the main result (O(n log n) time; O(lambda_{k+1}(n) log n) for curves that cross pairwise at most k times)
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the main theorem and its application to element distinctness
---

The lower envelope of a set of $n$ line segments in the plane is the graph of their pointwise minimum: for each $x$, the lowest point where a segment meets the vertical line through $x$. The problem is to compute it as a list of pieces, each one a part of a single segment. Unlike the envelope of full lines, which has at most $n$ pieces, the envelope of segments can have $\Theta(n \alpha(n))$ pieces, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/), because the sequence of segments along it is a Davenport-Schinzel sequence of order 3. Hershberger (1989) computes it in $O(n \log n)$ time, which is optimal in the algebraic computation tree model.

## In plain words

Draw some straight sticks on a sheet of paper, some of them crossing. Now look at the sheet from the bottom edge, as if the sticks were walls and you stood far below. For each position from left to right, you see only the lowest stick there. The parts that you see form a broken path, the lower envelope.

The task is to list that path from left to right: which stick you see, and where the view changes from one stick to another. The view changes where two sticks cross, where a stick starts and hides the one behind it, and where a stick ends and shows the one behind it. One stick can appear many times, because shorter sticks can start and end in front of it. The surprise is that the average number of appearances per stick can grow without limit, though extremely slowly.

## Definition

**Input.** A set $S = \{s_1, \ldots, s_n\}$ of non-vertical closed line segments in the plane. Segment $s_i$ is the graph of an affine function $\ell_i(x) = m_i x + c_i$ over an interval $[a_i, b_i]$ with $a_i < b_i$. So each segment is a *partially defined function*: it has a value only for $x \in [a_i, b_i]$.

**The envelope.** For each real $x$ let

$$E(x) = \min\{\ell_i(x) : 1 \le i \le n,\ a_i \le x \le b_i\},$$

with $E(x) = +\infty$ when no segment is defined at $x$. The *lower envelope* is the graph of $E$ where $E$ is finite.

**Output.** The *minimization diagram*: the partition of the real line into maximal intervals $I_1, I_2, \ldots, I_k$, in order from left to right, such that on the interior of each $I_j$ either no segment is defined or one segment $s_{\sigma(j)}$ attains the minimum. The output lists the intervals and the labels $\sigma(j)$. The *combinatorial complexity* of the envelope is the number of labeled intervals. When two segments overlap on a common line, a fixed rule (for example the smaller index) picks the label, and the bounds below do not change.

**Upper envelope.** The upper envelope is the graph of the pointwise maximum. Replacing each segment by its mirror image in the $x$-axis turns one problem into the other, so every bound for one holds for the other.

## Variants

- **Full lines.** If each segment is a full non-vertical line, the envelope $E(x) = \min_i (m_i x + c_i)$ is a concave function. Its slope decreases from left to right, so each line gives at most one piece and there are at most $n$ pieces. A line $\ell_i$ attains the minimum at some $x$ exactly when the point $(m_i, c_i)$ minimizes $x \cdot m + c$ over the points $(m_j, c_j)$, that is, when $(m_i, c_i)$ is a vertex of the lower [convex hull](/convex-hull/) of these points that is extreme in the direction $(-x, -1)$. So the envelope of lines is the lower hull of the dual points, read in decreasing order of slope, and it takes $O(n \log n)$ time. This is the structure behind the [convex hull trick](/convex-hull-trick/).
- **Segments that do not cross.** If no two segments cross, the label sequence has no subsequence $a\,b\,a\,b$, so it is a Davenport-Schinzel sequence of order 2 and has at most $2n - 1$ pieces. The [skyline problem](/skyline-problem/) is the upper envelope of horizontal segments, which is a case of this.
- **Curves.** For partially defined continuous functions whose graphs cross pairwise at most $s$ times, the envelope has at most $\lambda_{s+2}(n)$ pieces. For totally defined functions with at most $s$ crossings pairwise, the bound is $\lambda_s(n)$. Sharir and Agarwal, Chapter 1, prove both.
- **Envelopes in three dimensions.** The lower envelope of triangles or surfaces in space is a planar map. It is the subject of the later chapters of Sharir and Agarwal, and it is outside this page.

## Examples

**Two segments, four pieces.** Let $a$ be the segment from $(0, 0)$ to $(10, 0)$ and $b$ the segment from $(2, -4)$ to $(12, 6)$. They cross at $x = 6$. The envelope is $a$ on $[0, 2]$, $b$ on $[2, 6]$, $a$ on $[6, 10]$ and $b$ on $[10, 12]$. The label sequence is $a\,b\,a\,b$: a segment can appear twice, which lines cannot do.

**Five segments.** Take

| segment | from | to |
|---|---|---|
| $s_1$ | $(0, 4)$ | $(6, 1)$ |
| $s_2$ | $(1, 0)$ | $(9, 8)$ |
| $s_3$ | $(3, 3)$ | $(12, 0)$ |
| $s_4$ | $(5, 6)$ | $(14, 6)$ |
| $s_5$ | $(8, 1)$ | $(11, -1)$ |

The lower envelope has 7 pieces:

| interval | $[0, 1]$ | $[1, 10/3]$ | $[10/3, 6]$ | $[6, 8]$ | $[8, 11]$ | $[11, 12]$ | $[12, 14]$ |
|---|---|---|---|---|---|---|---|
| segment | $s_1$ | $s_2$ | $s_1$ | $s_3$ | $s_5$ | $s_3$ | $s_4$ |

The breakpoints are of three kinds. At $x = 1$ the segment $s_2$ starts below $s_1$, and $E$ jumps down from $3.5$ to $0$. At $x = 10/3$ the segments $s_1$ and $s_2$ cross, at height $7/3$. At $x = 6$ the segment $s_1$ ends, and $E$ jumps up from 1 to 2, the height of $s_3$. The sequence $s_1\,s_2\,s_1\,s_3\,s_5\,s_3\,s_4$ has no subsequence of the form $x\,y\,x\,y\,x$.

**Lines tangent to a parabola.** The lines $y = -2a x + a^2$ for $a = 3, 1, 4$ are the tangents of $y = -x^2$ at $x = 3, 1, 4$. Their lower envelope is the line for $a = 1$ up to $x = 2$, then $a = 3$ up to $x = 3.5$, then $a = 4$: the lines appear in increasing order of $a$. The reduction below uses this.

## Known algorithms

- **Divide and conquer.** Split $S$ into two halves, compute both envelopes, and merge them by a sweep from left to right over the union of their breakpoints. On each interval between two consecutive breakpoints, each envelope is one segment or nothing, and two segments cross at most once, so the merge emits $O(1)$ pieces per interval and runs in time linear in the sizes of the two envelopes, that is $O(\lambda_3(n))$. The recurrence $T(n) = 2T(n/2) + O(\lambda_3(n))$ gives $O(\lambda_3(n) \log n) = O(n \alpha(n) \log n)$ time. See the [divide-and-conquer paradigm](/divide-and-conquer-paradigm/); the merge is the same walk as the merge of two [skylines](/skyline-problem/).
- **Hershberger's algorithm.** $O(n \log n)$ time, which is optimal. Hershberger groups the segments so that the segments of one group all meet a common vertical line. On each side of that line the group behaves like a set of functions that all start (or all end) at the same $x$, so by the argument in the Bounds section its envelope has only $O(m)$ pieces for $m$ segments. These smaller envelopes are cheap to merge. For curves that cross pairwise at most $k$ times, the same method takes $O(\lambda_{k+1}(n) \log n)$ time.
- **Lines.** For full lines, sort by slope and run [Andrew's monotone chain](/andrew-monotone-chain/) on the dual points, in $O(n \log n)$ time.

## Bounds

**The label sequence is a Davenport-Schinzel sequence of order 3.** A *Davenport-Schinzel sequence of order $s$* on $n$ symbols has no two equal adjacent symbols and no alternating subsequence $a\,b\,a\,b \ldots$ of length $s + 2$ for distinct $a, b$. Let $\lambda_s(n)$ be the largest length of such a sequence. The labels $\sigma(1), \sigma(2), \ldots$ of the envelope, with the empty intervals left out, form such a sequence for $s = 3$:

- Two adjacent labeled intervals have different labels by maximality. If two consecutive labeled intervals are separated by an empty interval, their labels differ too: a segment is defined on an interval, so a segment that appears on both sides of a gap would be defined in the gap.
- Suppose $a\,b\,a\,b\,a$ is a subsequence, at points $x_1 < x_2 < x_3 < x_4 < x_5$ inside the intervals of these labels. Segment $a$ is defined at $x_1$ and $x_5$, so on all of $[x_1, x_5]$; segment $b$ is defined on $[x_2, x_4]$. At $x_2$ and $x_4$ segment $b$ is strictly below $a$, and at $x_3$ segment $a$ is strictly below $b$. So $\ell_a - \ell_b$ changes sign on $(x_2, x_3)$ and again on $(x_3, x_4)$. Two distinct affine functions have at most one zero, so this is impossible.

So the envelope has at most $\lambda_3(n)$ pieces, plus at most $n + 1$ empty intervals.

**$\lambda_3(n) = \Theta(n \alpha(n))$.** Hart and Sharir (1986) proved this upper and lower bound.

**Segments that meet a common vertical line.** Let $m$ segments all meet the line $x = c$. On $[c, \infty)$ each of them is defined on an interval $[c, b_i]$. Suppose the labels to the right of $c$ contain $a\,b\,a\,b$ at points $c \le x_1 < x_2 < x_3 < x_4$. Segment $a$ is defined at $x_3$, so on $[c, x_3]$, and $b$ is defined on $[c, x_4]$. So both are defined on $[x_1, x_3]$, with $a$ below $b$ at $x_1$ and $x_3$ and $b$ below $a$ at $x_2$: two sign changes of $\ell_a - \ell_b$, which is impossible. So the labels on each side of $c$ form a Davenport-Schinzel sequence of order 2, and $\lambda_2(m) = 2m - 1$ gives $O(m)$ pieces in total.

**The bound is attained by segments.** A Davenport-Schinzel sequence is a combinatorial object, and not every one comes from segments. Wiernik and Sharir (1988) constructed, for each $n$, a set of $n$ segments whose lower envelope has $\Omega(n \alpha(n))$ pieces. So the worst-case complexity of the lower envelope of $n$ segments is $\Theta(n \alpha(n))$.

**Time.** $O(n \log n)$ by Hershberger's algorithm. The output has $O(n \alpha(n))$ pieces, which is $o(n \log n)$, so the time lower bound does not come from the size of the output. It comes from the reduction below: in the [algebraic computation tree](/algebraic-computation-tree/) model each algorithm needs $\Omega(n \log n)$ operations in the worst case, even for full lines, because [element distinctness](/element-distinctness-lower-bound/) needs $\Omega(n \log n)$ operations in this model (Ben-Or, 1983).

## Reductions

**From element distinctness, in $O(n)$ time.** Given reals $a_1, \ldots, a_n$, let $\mu = \min_i a_i$ and $M = \max_i a_i$. Make the segment $s_i$ of the line $y = -2a_i x + a_i^2$ over $[\mu - 1, M + 1]$. This line is the tangent of $y = -x^2$ at $x = a_i$, and $-2a_i x + a_i^2 = (x - a_i)^2 - x^2$. At a fixed $x$, the lowest segment is the one with $a_i$ closest to $x$. So if the $a_i$ are distinct and sorted as $a_{\pi(1)} < \cdots < a_{\pi(n)}$, the envelope has exactly $n$ pieces with labels $\pi(1), \ldots, \pi(n)$ in this order, with breakpoints at the midpoints $(a_{\pi(j)} + a_{\pi(j+1)})/2$, which all lie in $[\mu, M]$. Given the output, check in $O(n)$ time whether its labels are $n$ distinct indices $\pi(1), \ldots, \pi(n)$ with $a_{\pi(1)} < \cdots < a_{\pi(n)}$. If the $a_i$ are distinct, the check passes. If two are equal, no order of the indices is strictly increasing, so the check fails, whatever the envelope algorithm does with the two equal segments. The construction uses one multiplication per segment, which the algebraic computation tree model allows. The same construction with full lines gives the bound for envelopes of lines.

**Sorting.** For distinct inputs the reduction outputs the $a_i$ in sorted order, so an envelope algorithm also sorts.

**To the convex hull.** As in the variant for lines, the envelope of $n$ lines is the lower convex hull of the $n$ dual points $(m_i, c_i)$, and the converse also holds: the lower hull of points $(p_i, q_i)$ is read off the envelope of the lines $y = p_i x + q_i$. Both directions cost $O(n)$.

**To the skyline.** The [skyline problem](/skyline-problem/) is the upper envelope of $n$ horizontal segments.

## Applications

- **Visibility.** The parts of $n$ opaque segments that are visible from a point far below, at $y = -\infty$, are exactly the pieces of the lower envelope. This is the two-dimensional case of [hidden-surface removal](/hidden-surface-removal/).
- **Kinetic problems.** If $n$ points move on a line with constant speeds, each during its own time interval, the position of the leftmost point over time is the lower envelope of $n$ segments in the time-position plane. The [kinetic heap](/kinetic-heap/) maintains such a minimum online.
- **Dynamic programming.** The [convex hull trick](/convex-hull-trick/) and the [Li Chao tree](/li-chao-tree/) answer queries of the form $\min_i (m_i x + c_i)$, a point query on the envelope of lines. The Li Chao tree also handles segments.
- **Arrangements.** The envelope is the lowest face boundary of the [arrangement of lines](/line-arrangement/) or segments, and the bounds above are the first step to the bounds on a single face of an arrangement, in Sharir and Agarwal, Chapter 5.

## References
