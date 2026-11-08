---
tag: 9RN5KZ
kind: algorithm
slug: chan-algorithm
name: Chan's algorithm
aliases:
- Chan's output-sensitive convex hull
- optimal output-sensitive hull
- shatter and wrap
area: geometry/convex-hulls
level: advanced
summary: Splits the points into groups, hulls each group, then wraps around the groups with binary-search tangents; O(n log h).
solves: [convex-hull-problem]
model: real-ram
complexity:
  vars: {n: the number of input points, h: the number of hull vertices}
  time: {worst: O(n log h)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1996
  people: [Timothy M. Chan]
  note: Chan published the method, with a three-dimensional version, in Discrete and Computational Geometry in 1996.
prereqs: [convex-hull-problem, andrew-monotone-chain, jarvis-march, binary-search, orientation-test]
see_also: [kirkpatrick-seidel, convex-hull-output-sensitive-lower-bound, graham-scan, upper-and-lower-hull, quickhull, convex-hull-3d, convex-hull-lower-bound]
sources:
  - paper: doi:10.1007/BF02712873
    title: Timothy M. Chan, Optimal output-sensitive convex hull algorithms in two and three dimensions, Discrete and Computational Geometry 16(4), 1996
    locator: the planar algorithm (groups of size m, tangent queries by binary search, the squaring of the guess m) and the three-dimensional version
  - paper: doi:10.1137/0215021
    title: David G. Kirkpatrick and Raimund Seidel, The ultimate planar convex hull algorithm?, SIAM Journal on Computing 15(1), 1986
    locator: the first O(n log h) algorithm and the matching lower bound
  - paper: doi:10.1016/0020-0190(73)90020-3
    title: R. A. Jarvis, On the identification of the convex hull of a finite set of points in the plane, Information Processing Letters 2(1), 1973
    locator: the whole paper (the wrapping step that Chan's algorithm runs on groups)
---

Chan's algorithm computes the [convex hull](/convex-hull/) of $n$ points in the plane in $O(n \log h)$ time, where $h$ is the number of hull vertices. It splits the points into groups of $m$ points, computes the hull of each group with an $O(m \log m)$ method such as [Andrew's monotone chain](/andrew-monotone-chain/), and then runs the wrapping step of the [Jarvis march](/jarvis-march/) on the groups: from each hull vertex it finds the next one with one [binary search](/binary-search/) per group. When $m$ is at least $h$ the wrap closes in $h$ steps. The algorithm does not know $h$, so it tries $m = 2^2, 2^4, 2^8, \ldots$ and stops at the first success. The bound $O(n \log h)$ is optimal by the [output-sensitive lower bound](/convex-hull-output-sensitive-lower-bound/).

## In plain words

Gift wrapping finds the hull one corner at a time, and each corner costs a look at every point. That is fast when the hull has few corners and slow when it has many. Sorting-based methods cost the same no matter how many corners there are.

Chan's idea is to mix the two. Cut the points into small groups and wrap each small group once, which is cheap. Then walk around the whole set as in gift wrapping, but ask each group for its best point instead of asking each point. A group can answer fast because its own hull is already in order.

The walk may take only a fixed number of steps. If it does not close, the guess for the number of corners was too small, so square the guess and try again. The failed tries cost less than the last one, so the total stays small.

## The problem

The input is a finite list $P$ of points with exact coordinates, repeats allowed. The output is the list of the vertices of $\mathrm{conv}(P)$ in counterclockwise order, starting at the lexicographically smallest point, with no point in the middle of an edge, as in the [convex hull problem](/convex-hull-problem/). With one distinct point the output is that point, and with all points on one line it is the two end points.

Notation: $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive for a left turn. Points are compared lexicographically, by $x$ and then by $y$. The minimum $a$ and the maximum $b$ of $P$ are hull vertices. The *upper hull* is the part of the hull boundary from $a$ to $b$ in clockwise order, and the *lower hull* is the part from $a$ to $b$ in counterclockwise order (see [upper and lower hull](/upper-and-lower-hull/)). This page computes the upper hull with the wrap and gets the lower hull as the upper hull of the reflected set $-P = \{-p : p \in P\}$. Each group then needs only its upper chain, and the tangent query is a binary search on a chain that turns one way.

## The algorithm

```pseudo id=main
CHAN-HULL(P)
L1  if P is empty then return the empty list
L2  a ← min P, b ← max P;  if a = b then return [a]
L3  U ← CHAN-UPPER(P, a, b)                       ▷ upper hull from a to b
L4  L ← reflect(CHAN-UPPER(−P, −b, −a))           ▷ lower hull from b to a
L5  return reverse(L) without its last point, then reverse(U) without its last point

CHAN-UPPER(P, a, b)
L6  for t ← 1, 2, 3, … do
L7      m ← min(2^(2^t), n)
L8      cut P into groups of m points; U_j ← the upper chain of group j
L9      H ← [a]
L10     repeat m times
L11         p ← the last point of H; best ← none
L12         for each group j do
L13             c ← TANGENT(U_j, p)
L14             if c ≠ none and (best = none or orient(p, best, c) > 0 or (orient(p, best, c) = 0 and |c − p| > |best − p|)) then best ← c
L15         append best to H
L16         if best = b then return H
```

The upper chain of a group (line L8) is the output of the upper scan of [Andrew's monotone chain](/andrew-monotone-chain/), reversed: its points $u_0 < u_1 < \cdots < u_k$ go from the smallest to the largest point of the group, it turns strictly right at each inner point, and every point of the group is on or to the right of each edge. TANGENT returns the point of the chain that the wrap should take from $p$:

```pseudo id=tangent
TANGENT(U, p)                                    ▷ U = u_0 < u_1 < … < u_k
T1  lo ← the first index with u_lo > p           ▷ binary search on the order
T2  if there is no such index then return none
T3  i ← lo, j ← k
T4  while i < j do                               ▷ first index i ≥ lo with orient(p, u_i, u_{i+1}) < 0, or k
T5      mid ← ⌊(i + j)/2⌋
T6      if orient(p, u_mid, u_{mid+1}) < 0 then j ← mid else i ← mid + 1
T7  return u_i
```

Line L14 keeps the candidate that is most counterclockwise as seen from $p$, and on a tie the farther one. All candidates are larger than $p$, so they lie in one half-plane around $p$ and this comparison is a total order on directions. The next upper hull vertex after $p$ is the unique point that wins this comparison against all of $P$. Line L4 runs the same procedure on $-P$, whose smallest point is $-b$ and largest point is $-a$. The determinant of the orientation test has degree 2, so the reflection does not change any orientation, and reflecting the upper hull of $-P$ back gives the lower hull of $P$ from $b$ to $a$.

The algorithm never sorts all of $P$: line L2 takes a minimum and a maximum, and the sorts of line L8 are on groups of $m$ points.

## Example

Take the twelve points, in input order,

$$(0,0),\ (6,9),\ (3,2),\ (11,5),\ (1,5),\ (9,8),\ (5,4),\ (12,0),\ (3,8),\ (8,3),\ (6,-2),\ (10,2).$$

Here $a = (0,0)$ and $b = (12,0)$. The hull has $h = 8$ vertices: six edges on the upper hull and two on the lower hull.

**Upper hull, round $t = 1$, $m = 4$.** The groups are the input in blocks of four, and their upper chains are

| group | points | upper chain |
| --- | --- | --- |
| 1 | (0,0) (6,9) (3,2) (11,5) | (0,0) (6,9) (11,5) |
| 2 | (1,5) (9,8) (5,4) (12,0) | (1,5) (9,8) (12,0) |
| 3 | (3,8) (8,3) (6,−2) (10,2) | (3,8) (10,2) |

The wrap may take at most 4 steps.

| step | $p$ | tangent in group 1 | group 2 | group 3 | best |
| --- | --- | --- | --- | --- | --- |
| 1 | (0,0) | (6,9) | (1,5) | (3,8) | (1,5) |
| 2 | (1,5) | (6,9) | (9,8) | (3,8) | (3,8) |
| 3 | (3,8) | (6,9) | (9,8) | (10,2) | (6,9) |
| 4 | (6,9) | (11,5) | (9,8) | (10,2) | (9,8) |

The wrap does not reach $b$ in 4 steps, so the round fails. Its four steps were correct: they are the first four upper hull vertices after $a$.

**Upper hull, round $t = 2$.** Now $2^{2^2} = 16 > 12$, so $m = 12$ and there is one group. Its upper chain is the whole upper hull, and six steps give

$$H = (0,0),\ (1,5),\ (3,8),\ (6,9),\ (9,8),\ (11,5),\ (12,0).$$

**Lower hull.** On $-P$ the first round already succeeds: the lower hull of $P$ from $b$ to $a$ is $(12,0), (6,-2), (0,0)$, and it needs only two steps.

**Output.** Line L5 joins the two chains:

$$(0,0),\ (6,-2),\ (12,0),\ (11,5),\ (9,8),\ (6,9),\ (3,8),\ (1,5).$$

## Correctness

The proof has four parts. First, the next upper hull vertex after a vertex $p$ is the unique point $q > p$ of $P$ that is most counterclockwise as seen from $p$, and the farthest among the points in that direction. Second, along an upper chain the sign of $\mathrm{orient}(p, u_i, u_{i+1})$ is nonnegative and then negative after the index $lo$, so the binary search of TANGENT is valid. Third, for each group TANGENT returns a point that beats or ties every point of the group that is larger than $p$. This step uses the fact that a vertex of the upper hull of $P$ lies on or above every chord of $P$ that spans it. Fourth, the group that contains the true next vertex returns it, so line L14 selects it. By induction each round appends correct upper hull vertices, and a round with $m$ at least the number of upper edges reaches $b$. The output is then the same list that Andrew's algorithm returns, so it is the hull. The full proof is in the correctness proof below.

## Complexity

- **One round.** In round $t$ there are $\lceil n/m \rceil$ groups. Line L8 sorts each group and scans it, $O(m \log m)$ per group and $O(n \log m)$ in total. Each of the at most $m$ wrap steps makes one tangent query per group, each a binary search of $O(\log m)$ orientation tests, so the wrap costs $O(m \cdot (n/m) \cdot \log m) = O(n \log m)$. With $m \le 2^{2^t}$, the round costs $O(n \, 2^t)$.
- **Number of rounds.** Let $u$ be the number of edges of the upper hull, so $u \le h$. Round $t$ succeeds when $2^{2^t} \ge u$ or $m = n$. So the last round $t^*$ satisfies $2^{t^*} \le \max(2, 2 \lg u)$.
- **Total.** The round costs grow geometrically, so the sum over $t = 1, \ldots, t^*$ is $O(n \, 2^{t^*}) = O(n (1 + \log h))$. The same holds for the lower hull. Lines L1 and L2 cost $O(n)$. So the time is $O(n \log h)$ in the worst case on the [real RAM](/real-ram/), for $h \ge 2$.
- **Space.** $\Theta(n)$ for the groups, the chains and the reflected copy.

Squaring $m$ is what makes the sum geometric. With doubling, $m = 2^t$, there would be $\Theta(\log h)$ rounds of cost $\Theta(n \log h)$ each in the worst case, which gives $O(n \log^2 h)$. The bound $O(n \log h)$ is optimal in the algebraic decision tree model, by the [output-sensitive lower bound](/convex-hull-output-sensitive-lower-bound/). For $h = \Theta(n)$ it is $O(n \log n)$, the bound of [Graham's scan](/graham-scan/) and Andrew's algorithm.

## Properties

- **Output-sensitive.** The time depends on $h$, not only on $n$. For hulls with $O(1)$ vertices the time is $O(n)$.
- **Exact with integer input.** The predicates are the orientation test and the comparison of squared distances, both polynomials of degree 2.
- **Deterministic.** No randomness is used.
- **Failed rounds are safe.** A failed round costs time only. The steps that it makes are correct upper hull vertices, so an implementation can stop at any point and keep a correct prefix of the hull.

## Variants and improvements

- **Full group hulls.** Chan's paper computes the whole hull of each group with Graham's scan, wraps around the whole hull, and finds each tangent by binary search on a convex polygon. That search must handle the two chains of the polygon. Splitting into upper and lower hulls, as on this page, makes each search a search on a chain that turns one way.
- **Reuse between rounds.** An implementation can start round $t + 1$ from the vertices found in round $t$, or keep the guess $h$ from an earlier run. This changes only the constant.
- **Kirkpatrick-Seidel.** The [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/) reaches $O(n \log h)$ by prune and search: it finds the upper hull edge that crosses the median $x$-coordinate in linear time and recurses on both sides. It came first, in 1986, but it is longer to implement.
- **Three dimensions.** Chan's paper applies the same scheme in $\mathbb{R}^3$. The groups are hulled in $O(m \log m)$ time, each group hull is stored in a Dobkin-Kirkpatrick hierarchy for $O(\log m)$ extreme-point queries, and gift wrapping runs over the groups. The time is $O(n \log h)$ for $h$ hull facets. See the [3D convex hull problem](/convex-hull-3d/).
- **Other output-sensitive problems.** The same "guess and square" method applies when an $O(n \log m)$ procedure can detect that the answer is larger than $m$.

## When to use it

Use it when the input is large and the hull is known to be small, for example points from a smooth distribution inside a polygon, where the expected hull size is $O(\log n)$. In practice [Andrew's monotone chain](/andrew-monotone-chain/) is often as fast, because a sort of $n$ numbers is cheap and Chan's constant is larger. [Quickhull](/quickhull/) is also fast on such inputs but has an $O(n^2)$ worst case. Chan's algorithm is the simplest method with the optimal worst-case bound in terms of both $n$ and $h$.

## Pitfalls

- **Doubling instead of squaring.** With $m = 2^t$ the bound becomes $O(n \log^2 h)$.
- **A global sort.** Sorting all of $P$ first, for example to remove duplicates, costs $\Theta(n \log n)$ and loses the output-sensitive bound. Take only the minimum and the maximum, and let each group remove its own duplicates.
- **Ties in line L14.** Two candidates in the same direction from $p$ must be ranked by distance, the farther first. Otherwise the wrap stops at a point in the middle of an edge and the next step from it is wrong.
- **Tangent on the wrong part of the chain.** The binary search is valid only on the part of the chain that is larger than $p$. Points of the chain at or before $p$ can make the sign sequence non-monotone. Line T1 skips them.
- **Floating-point orientation.** An inconsistent sign breaks the monotonicity of the tangent search and the transitivity of line L14. Use exact arithmetic.

## Implementations

## History

Kirkpatrick and Seidel gave the first planar hull algorithm with $O(n \log h)$ time in 1986, together with a matching lower bound, and asked in the title of their paper whether it was the ultimate one. Timothy Chan published his simpler method in 1996. It combines a sort-based hull on small groups with Jarvis's gift wrapping from 1973 and guesses the output size by repeated squaring. The same paper gives a simple $O(n \log h)$ algorithm in three dimensions. Before it, the optimal three-dimensional bound came from the randomized method of Clarkson and Shor and its derandomization by Chazelle and Matoušek. Chan's technique of guessing an output parameter by squaring is now a standard tool in output-sensitive geometry.

## References
