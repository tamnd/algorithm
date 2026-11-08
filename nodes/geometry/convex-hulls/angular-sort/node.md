---
tag: AX2YCH
kind: concept
slug: angular-sort
name: Angular sort
aliases:
- polar angle sort
- sorting by polar angle
- radial sort
area: geometry/convex-hulls
level: intro
summary: Sorting points by their angle around a pivot point, used by Graham's scan.
prereqs: [cross-product, orientation-test, sorting-problem]
see_also: [graham-scan, rotational-sweep, minkowski-sum-convex-polygons, half-plane-intersection, star-shaped-polygon, comparison-sort-lower-bound, floating-point-arithmetic, andrew-monotone-chain]
sources:
  - paper: doi:10.1016/0020-0190(72)90045-2
    title: Ronald L. Graham, An efficient algorithm for determining the convex hull of a finite planar set, Information Processing Letters 1(4), 1972
    locator: the sort of the points by angle around an interior point before the scan
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, 2nd edition, Cambridge University Press, 1998
    locator: Chapter 3, Convex hulls in two dimensions (Graham's algorithm, sorting by angle with a left-turn comparison and the handling of collinear ties)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, the section on Graham's scan (polar sorting without trigonometric functions)
---

An angular sort puts points in the order of their direction as seen from a fixed pivot, like the hand of a clock that sweeps counterclockwise around the pivot. [Graham's scan](/graham-scan/) starts with this sort, and so do [rotational sweeps](/rotational-sweep/), the merge step of [Minkowski sums of convex polygons](/minkowski-sum-convex-polygons/) and many visibility algorithms. The sort can be done exactly with integer arithmetic, without computing any angle: a half-plane test and a [cross product](/cross-product/) give a correct comparison function.

## In plain words

Stand at one point and look at all the others. Start facing east and turn slowly to your left, all the way around. Write down each point at the moment you face it. That list is the angular sort.

A computer does not need to measure the angles to do this. To decide which of two points comes first, it is enough to know whether the second one is to the left or to the right of the first, as seen from where you stand. Two multiplications and one subtraction answer that question exactly. The only care needed is at the start of the turn: a point just past east and a point just before east look close together but belong at opposite ends of the list.

## The idea

Fix a pivot $o$ and replace each other point $p$ by the vector $v = p - o \ne 0$. The task is to sort the vectors by the angle $\theta(v) \in [0, 2\pi)$ measured counterclockwise from the positive $x$-axis, and by length when two angles are equal.

**The obvious way and its problem.** Sorting by `atan2(v.y, v.x)` rounds each angle to a floating-point number, and two different directions can get the same rounded angle. For $u = (10^9, 10^9 + 1)$ and $w = (10^9 + 1, 10^9 + 2)$ the cross product is $u_x w_y - u_y w_x = -1$, so $w$ has the smaller angle, but Python's `math.atan2` returns the same value for both. A tie rule by length then puts $u$ first, the wrong order. In Graham's scan such an error can keep a point that is not a hull vertex. See [floating-point arithmetic](/floating-point-arithmetic/).

**The exact comparison.** Split the directions into two half-open halves:

$$\mathrm{half}(v) = \begin{cases} 0 & \text{if } v_y > 0, \text{ or } v_y = 0 \text{ and } v_x > 0, \\ 1 & \text{otherwise}. \end{cases}$$

Half 0 holds the angles in $[0, \pi)$ and half 1 the angles in $[\pi, 2\pi)$. Inside one half, two angles differ by less than $\pi$, so the sign of the cross product $u \times v = u_x v_y - u_y v_x = |u||v|\sin(\theta(v) - \theta(u))$ tells their order: $u \times v > 0$ exactly when $\theta(u) < \theta(v)$, and $u \times v = 0$ exactly when the angles are equal. The comparison is:

1. If $\mathrm{half}(u) \ne \mathrm{half}(v)$, the vector in half 0 comes first.
2. Otherwise, if $u \times v > 0$, $u$ comes first; if $u \times v < 0$, $v$ comes first.
3. Otherwise the directions are equal, and the shorter vector comes first, compared by $u \cdot u$ against $v \cdot v$.

```python
from functools import cmp_to_key

def half(v):
    return 0 if v[1] > 0 or (v[1] == 0 and v[0] > 0) else 1

def angle_cmp(u, v):
    if half(u) != half(v):
        return half(u) - half(v)
    c = u[0] * v[1] - u[1] * v[0]
    if c != 0:
        return -1 if c > 0 else 1
    du, dv = u[0] ** 2 + u[1] ** 2, v[0] ** 2 + v[1] ** 2
    return (du > dv) - (du < dv)

order = sorted(vectors, key=cmp_to_key(angle_cmp))
```

If the input coordinates have absolute value at most $M$, the vectors $p - o$ have coordinates of absolute value at most $2M$, and the cross products and squared lengths have absolute value at most $8M^2$. In a language with fixed-width integers this tells you the word size you need; Python integers do not overflow.

The comparison is a strict weak order, because it is the lexicographic order on the key $(\mathrm{half}(v), \theta(v), |v|)$, so any correct comparison sort can use it. Sorting takes $O(n \log n)$ comparisons. An angular sort can also sort any list of distinct numbers (map each number to a point on the upper half of a circle around the pivot, in the same order), so the [comparison-sort lower bound](/comparison-sort-lower-bound/) of $\Omega(n \log n)$ comparisons applies when the only operations are such comparisons.

**Why the half test matters.** The cross product alone is not a valid comparison over the full circle. For $a = (2, 0)$, $b = (-1, 2)$ and $c = (-1, -2)$, about $120°$ apart, $a \times b = 4$, $b \times c = 4$ and $c \times a = 4$ are all positive. A cross-product-only rule would say $a$ before $b$, $b$ before $c$ and $c$ before $a$, a cycle, and a sort that uses it can return any order.

**The Graham special case.** Graham's scan in its common form picks the pivot $o$ as the lowest point, and among the lowest the leftmost. Then every other point has $v_y > 0$, or $v_y = 0$ and $v_x > 0$, so all vectors lie in half 0, and the cross product alone is a correct comparison. Graham's 1972 paper used a point inside the hull as the pivot and a full turn instead.

**Ties.** Points in the same direction need a rule that suits the algorithm. Sorting them by distance, as above, is the usual choice. For Graham's scan with the lowest pivot, the points on the last ray (the largest angle) must be visited from far to near if collinear hull points are to be kept, and only the farthest one matters if they are to be dropped.

## Examples

**A full turn around the origin.** The vectors $(3,0)$, $(-2,-2)$, $(0,-1)$, $(1,1)$, $(2,2)$, $(-1,0)$, $(0,4)$, $(-3,1)$, $(2,-3)$ sort to

$$(3,0),\ (1,1),\ (2,2),\ (0,4),\ (-3,1),\ (-1,0),\ (-2,-2),\ (0,-1),\ (2,-3).$$

The first five are in half 0 and the last four in half 1. $(1,1)$ and $(2,2)$ have the same direction ($1 \cdot 2 - 1 \cdot 2 = 0$), and the shorter comes first. $(-1, 0)$ has angle exactly $\pi$ and opens half 1. A script compared this exact order with an `atan2` sort on 3000 random sets of small integer vectors and found no difference; on small inputs `atan2` is accurate enough, but the exact comparison does not depend on that.

**A Graham pivot.** For the points $(4,1)$, $(1,3)$, $(6,4)$, $(2,0)$, $(5,6)$, $(0,2)$, $(3,3)$, $(4,4)$, the lowest point is $o = (2, 0)$. The sorted order around it is

$$(4,1),\ (6,4),\ (4,4),\ (5,6),\ (3,3),\ (1,3),\ (0,2).$$

Here $(4,4) - o = (2, 4)$ and $(5,6) - o = (3, 6)$ point the same way ($2 \cdot 6 - 4 \cdot 3 = 0$), so the nearer point $(4, 4)$ comes first.

## Where it is used

- [Graham's scan](/graham-scan/) sorts the points by angle around the lowest point and then removes right turns with a stack. [Andrew's monotone chain](/andrew-monotone-chain/) replaces the angular sort by a sort on coordinates, which avoids the special pivot and the tie rule.
- A [rotational sweep](/rotational-sweep/) around a point processes events in angular order, for example to compute the visibility polygon of a point or the visibility graph of obstacles.
- The [Minkowski sum of two convex polygons](/minkowski-sum-convex-polygons/) merges the edge vectors of both polygons by angle, and the same half test and cross product compare them.
- [Half-plane intersection](/half-plane-intersection/) by the sort-and-deque method sorts the boundary lines by the angle of their direction vectors.
- A [star-shaped polygon](/star-shaped-polygon/) through a point set: sorting the points around a pivot inside their hull and joining them in that order gives a simple polygon, provided no two points share a direction from the pivot.

## References
