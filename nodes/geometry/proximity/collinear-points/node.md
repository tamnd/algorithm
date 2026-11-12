---
tag: 9DGH9D
kind: problem
slug: collinear-points
name: Collinear points
aliases:
- collinear points detection
- points on a common line
- three collinear points
area: geometry/proximity
level: core
summary: Problem of finding the lines that hold k or more points of a set, for a given k ≥ 3, solved by sorting points by slope.
prereqs: [orientation-test, cross-product, general-position]
see_also: [3sum-hardness, line-arrangement, hough-transform, angular-sort, hash-table, line-arrangement-construction, proximity-problems]
sources:
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry, Theory and Applications 5(3), 1995, 165-185
    locator: the definition of 3SUM-hardness and the proof that deciding whether three of n points are collinear is 3SUM-hard
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 8, Arrangements and duality (point-line duality, the O(n^2) construction of an arrangement, and degeneracy testing)
  - paper: "Herbert Edelsbrunner and Leonidas J. Guibas, Topologically sweeping an arrangement, Journal of Computer and System Sciences 38(1), 1989, 165-194"
    locator: the topological sweep of an arrangement of n lines in O(n^2) time and O(n) space, with application to finding collinear triples
---

The collinear points problem asks which points of a set lie on a common line: find every line that contains at least $k$ of the $n$ input points, usually $k = 3$ or $k = 4$, or decide whether any three points are collinear. The standard method fixes each point $p$ in turn, sorts the other points by the slope of the line through $p$, and reads off runs of equal slopes; it takes $O(n^2 \log n)$ time, and $O(n^2)$ with hashing or with the dual [line arrangement](/line-arrangement/). Deciding whether any three points are collinear is the founding example of [3SUM-hardness](/3sum-hardness/), so no algorithm with time $O(n^{2 - \varepsilon})$ is expected. Slopes must be compared exactly: two different slopes can round to the same float.

## In plain words

You have a set of dots and want to find every straight line that passes through many of them, say four or more.

Checking every group of four dots works, but the number of groups grows very fast. A better idea: stand on one dot and look at all the others. Dots that lie on one line through your dot are seen in exactly the same direction. So sort the other dots by direction, and the dots that share a direction come out next to each other. Do this from every dot, and every line with many dots is found.

Directions must be compared with exact whole-number arithmetic. Two directions can differ so slightly that a computer working with rounded decimals sees them as equal.

## Definition

**Input.** A set $P$ of $n$ distinct points $p = (x, y)$ with integer coordinates (rational input is scaled to integers), and an integer $k \ge 3$.

**Output.** Every maximal subset of $P$ of size at least $k$ whose points lie on one line, each reported once, for example as the two extreme points of the subset in $(x, y)$-order.

**Collinearity.** Three points $p, q, r$ are collinear exactly when the [orientation test](/orientation-test/) is zero:

$$\mathrm{orient}(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x) = 0 .$$

With integer coordinates this is an exact integer test. Points $q$ and $r$ lie on one line through $p$ exactly when the reduced directions $(q - p)/g$ and $(r - p)/g'$ are equal up to sign, where $g$ and $g'$ are the gcds of the components; normalizing the sign (first nonzero component positive) turns the direction into an exact key for sorting or hashing.

**Duplicates.** If points may repeat, a copy of $p$ lies on every line through $p$. The usual convention removes duplicates first and adds their multiplicity to each line through the point afterwards.

**Decision version.** *Three collinear points*: is there a triple $p, q, r \in P$ with $\mathrm{orient}(p, q, r) = 0$? A "no" answer means $P$ is in [general position](/general-position/) with respect to lines.

## Variants

- **Any three collinear.** The decision version above, the standard test for general position, which many geometric algorithms assume.
- **Maximum number of collinear points.** Find a line containing the most points. The same slope grouping solves it in $O(n^2 \log n)$ time, or $O(n^2)$ expected with hashing.
- **Lines with at least $k$ points for large $k$.** If $k$ is a constant fraction of $n$, random sampling finds such lines much faster: two random points lie on a fixed heavy line with constant probability.
- **Approximate collinearity.** For real data, points within distance $\varepsilon$ of a line; this is line detection, as in the [Hough transform](/hough-transform/), and it is no longer exact.
- **Higher dimensions.** Are any $d + 1$ points of $\mathbb{R}^d$ on a common hyperplane? This is the $d$-dimensional degeneracy test, solved in $O(n^d)$ time with the dual arrangement of hyperplanes.

## Examples

**Two lines of four.** For the eleven points

$$P = \{(0,0), (1,1), (2,2), (3,3), (5,0), (5,1), (5,4), (5,7), (6,3), (1,6), (4,6)\},$$

the lines with at least three points are

| line | points | count |
| --- | --- | --- |
| $y = x$ | $(0,0), (1,1), (2,2), (3,3)$ | 4 |
| $x = 5$ | $(5,0), (5,1), (5,4), (5,7)$ | 4 |
| $3x + 2y = 15$ | $(1,6), (3,3), (5,0)$ | 3 |

For $k = 4$ the output is the first two lines. Around $p = (5,4)$ the normalized directions of the other points are $(5,4)$, $(4,3)$, $(3,2)$, $(2,1)$ for the four points on $y = x$, $(0,1)$ for $(5,0)$, $(5,1)$ and $(5,7)$, $(1,-1)$ for $(6,3)$, $(2,-1)$ for $(1,6)$ and $(1,-2)$ for $(4,6)$. The only direction shared by three points is $(0,1)$, which together with $p$ gives the vertical line of four. The points of $y = x$ have four different directions from $p$, as they should, since $p$ is not on that line.

**Float slopes fail.** The points $(0,0)$, $(3,1)$ and $(3 \cdot 10^{16} + 1, 10^{16})$ are not collinear: the orientation is $3 \cdot 10^{16} - (3 \cdot 10^{16} + 1) = -1$. But in double precision $3 \cdot 10^{16} + 1$ rounds to $3 \cdot 10^{16}$, and the two float slopes $1/3$ and $10^{16} / (3 \cdot 10^{16} + 1)$ compare equal.

**Reduction from 3SUM.** The numbers $-3, 1, 2$ sum to $0$, and the points $(-3, -27)$, $(1, 1)$, $(2, 8)$ are collinear: the slope from the first to the second is $28/4 = 7$ and from the second to the third is $7/1 = 7$.

## Known algorithms

| algorithm | time | space | idea |
| --- | --- | --- | --- |
| brute force over triples | $\Theta(n^3)$ | $O(1)$ | test $\mathrm{orient}(p, q, r)$ for every triple |
| brute force over 4-subsets | $\Theta(n^4)$ | $O(1)$ | the naive method for $k = 4$ |
| sort by slope around each point | $O(n^2 \log n)$ | $O(n)$ | [angular sort](/angular-sort/) around $p$, scan runs of equal direction |
| hash the reduced direction | $O(n^2)$ expected | $O(n)$ | group by the normalized direction in a [hash table](/hash-table/) |
| dual [line arrangement](/line-arrangement/) | $O(n^2)$ | $O(n^2)$ | three collinear points become three lines through one vertex |
| topological sweep (Edelsbrunner and Guibas, 1989) | $O(n^2)$ | $O(n)$ | sweep the arrangement without storing it |

The slope sort is the standard textbook method: for each point $p$, sort the other $n - 1$ points by their direction from $p$ with an exact comparator (the sign of a cross product within a half-plane, or the normalized integer direction), then report each run of at least $k - 1$ equal directions together with $p$. Each line with $m$ points is seen from each of its $m$ points; reporting it only from its smallest point in $(x, y)$-order avoids duplicates.

## Bounds

- **Upper bound.** $O(n^2)$ deterministic time for the decision version and for listing all lines with at least three points, by the arrangement or the topological sweep.
- **3SUM-hardness.** Gajentaan and Overmars (1995) showed that 3SUM reduces to "three collinear points" in linear time: map each number $a$ to the point $(a, a^3)$. For distinct $a, b, c$, the points $(a, a^3)$, $(b, b^3)$, $(c, c^3)$ are collinear exactly when $a + b + c = 0$, because the slope between $(a, a^3)$ and $(b, b^3)$ is $a^2 + ab + b^2$, and equal slopes from $a$ to $b$ and from $a$ to $c$ give $(b - c)(a + b + c) = 0$. So an $O(n^{2 - \varepsilon})$ algorithm for collinearity would refute the [3SUM conjecture](/3sum-conjecture/).
- **Output size.** Listing all lines with at least $k$ points can have large output: a $\sqrt{n} \times \sqrt{n}$ grid has $\Theta(n)$ lines with $\sqrt{n}$ points each, and with $k = 3$ there can be $\Theta(n^2)$ lines.
- **Where the evidence comes from.** No quadratic lower bound is known in the general algebraic models; quadratic bounds are proved only in restricted decision tree models, and the belief that quadratic time is needed rests on the 3SUM reduction.

## Reductions

- **3SUM reduces to three collinear points**, by $a \mapsto (a, a^3)$, as above.
- **Three collinear points reduces to line arrangements.** Under the duality $(a, b) \mapsto \{y = ax - b\}$, three points are collinear exactly when their three dual lines meet in one point, so building the [arrangement](/line-arrangement-construction/) of the dual lines and checking vertex degrees decides it.
- **Collinear points and the Hough transform.** The Hough transform votes for lines in a discretized dual space, an approximate version of the same duality.

## Applications

- **Degeneracy checks.** Many algorithms assume general position; testing it before running them is this problem.
- **Computer vision and pattern recognition.** Finding lines through many feature points, approximately, as in the [Hough transform](/hough-transform/).
- **Teaching.** The slope sort is a classic exercise in exact comparators, sorting with a custom order, and handling degenerate input.
- **Fine-grained complexity.** The problem is the first geometric member of the 3SUM-hard class, used as a source for reductions to other geometric problems.

## References
