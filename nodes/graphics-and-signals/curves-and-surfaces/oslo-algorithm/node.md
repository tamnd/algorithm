---
tag: MGGW0D
kind: algorithm
slug: oslo-algorithm
name: Oslo algorithm
aliases:
- Cohen-Lyche-Riesenfeld algorithm
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Refines the knot vector of a B-spline curve in one pass. Each new control point is computed directly, as a combination of at most p + 1 old ones with weights from a triangle of p rounds.
solves: [knot-refinement]
model: real-ram
complexity:
  vars: {p: the degree, d: the dimension of the points, n: the index of the last old control point, N: the index of the last new control point}
  time: {worst: Θ(N (log n + p^2 + p d))}
  space: {extra: Θ(p)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1980
  people: [Elaine Cohen, Tom Lyche, Richard Riesenfeld]
  note: Cohen, Lyche and Riesenfeld derived the algorithm from discrete B-splines in Computer Graphics and Image Processing 14 (1980). Lyche and Mørken made it more efficient in 1986.
prereqs: [knot-refinement, boehm-knot-insertion]
see_also: [de-boor-algorithm, cox-de-boor-recursion, curry-schoenberg-theorem, lane-riesenfeld-algorithm, chaikin-corner-cutting, nurbs, tensor-product-surface, partition-of-unity]
sources:
  - paper: "Elaine Cohen, Tom Lyche and Richard Riesenfeld, Discrete B-splines and subdivision techniques in computer-aided geometric design and computer graphics, Computer Graphics and Image Processing 14(2) (1980), 87 to 111"
    locator: the discrete B-splines, their recurrence, and the two refinement algorithms
  - paper: doi:10.1137/0723042
    title: Tom Lyche and Knut Mørken, Making the Oslo algorithm more efficient, SIAM Journal on Numerical Analysis 23(3) (1986), 663 to 675
    locator: improved versions of the two algorithms of the 1980 paper
  - paper: doi:10.1016/0167-8396(89)90032-0
    title: Lyle Ramshaw, Blossoms are polar forms, Computer Aided Geometric Design 6(4) (1989), 323 to 358
    locator: control points as values of the polar form at consecutive knots
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 5.3, Knot refinement
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XI, The B-spline series, control points, and knot insertion
---

The Oslo algorithm solves [knot refinement](/knot-refinement/): given a [B-spline](/b-spline/) curve of degree $p$ on knots $\tau$ and a finer knot vector $t$ that contains $\tau$, it computes the control points of the same curve on $t$. It does not insert the new knots one at a time. For each new control point $d_j$ it finds the old span that holds the knot $t_j$, runs a triangle of $p$ rounds that has the shape of the [Cox-de Boor recursion](/cox-de-boor-recursion/), with the fine knots $t_{j+1}, \ldots, t_{j+p}$ in place of the parameter, and gets the weights $\alpha_{i,p}(j)$ of at most $p + 1$ old control points. These weights are the discrete B-splines of Cohen, Lyche and Riesenfeld. Each new point costs $O(p^2 + p d)$, and the points can be computed independently, in any order.

## In plain words

You have a B-spline curve and you want to describe it with more knots, so that it has more control points, but the curve must stay the same. One way is to add the knots one by one. This algorithm instead computes each new control point directly from the old ones.

For one new point, it first finds where its knot lies among the old knots. Then only a few old points matter, one more than the degree. It mixes them in a fixed number of rounds. Each round uses one of the next knots of the new list and gives one more weight. At the end it has one weight for each of the few old points, and the new point is the weighted average.

Every new point is found on its own, so the work can be split among processors.

## The problem

The input is a degree $p \ge 1$, an old knot vector $\tau_0 \le \cdots \le \tau_{n+p+1}$ with $n \ge p$, control points $c_0, \ldots, c_n \in \mathbb{R}^d$, and a fine knot vector $t_0 \le \cdots \le t_{N+p+1}$ that contains $\tau$ as a multiset. As in the implementation, the new knots lie in the open interval $(\tau_p, \tau_{n+1})$, the end spans are nonempty ($\tau_p < \tau_{p+1}$ and $\tau_n < \tau_{n+1}$), and no knot of $t$ has multiplicity above $p + 1$. The output is $d_0, \ldots, d_N$ with $\sum_j d_j N^t_{j,p} = \sum_i c_i N^\tau_{i,p}$ on the domain $[\tau_p, \tau_{n+1}]$. The model is the [real RAM](/real-ram/), with exact rational arithmetic in the implementation.

## The algorithm

```pseudo id=main
OSLO-REFINE(τ, t, p, c)                     ▷ t contains τ; N = |t| − p − 2
L1  for j ← 0 to N
L2      μ ← the index with τ[μ] ≤ t[j] < τ[μ+1], clamped to p ≤ μ ≤ n
L3      α ← (1, 0, …, 0)                     ▷ p + 1 entries; α[s] weighs c[μ−r+s]
L4      for r ← 1 to p
L5          x ← t[j+r]
L6          for s ← r−1 downto 0
L7              a ← (x − τ[μ−r+1+s]) / (τ[μ+1+s] − τ[μ−r+1+s])
L8              α[s+1] ← α[s+1] + a · α[s];  α[s] ← (1 − a) · α[s]
L9      d[j] ← Σ_{s=0}^{p} α[s] · c[μ−p+s]
L10 return d
```

Lines L3 to L8 are the [Cox-de Boor recursion](/cox-de-boor-recursion/) for the $p + 1$ B-splines on the span $\mu$, with one change: round $r$ uses the fine knot $t_{j+r}$ where the recursion uses the parameter. After round $r$, the entry $\alpha[s]$ belongs to the old index $\mu - r + s$. The denominator of line L7 is at least $\tau_{\mu+1} - \tau_\mu > 0$. Line L6 runs downward, so that line L8 reads $\alpha[s]$ of the last round before it overwrites it; the implementation writes each round into a new row, which gives the same numbers. After line L8 the entries are the discrete B-splines $\alpha_{\mu-p+s,p}(j)$, the row $j$ of the knot insertion matrix, and line L9 applies the row.

## Example

Take $p = 2$, $\tau = (0, 0, 0, 1, 2, 3, 3, 3)$, the control points $c_0 = (0, 0)$, $c_1 = (1, 2)$, $c_2 = (3, 3)$, $c_3 = (5, 1)$, $c_4 = (6, 0)$, and insert the midpoints of all spans: $t = (0, 0, 0, 1/2, 1, 3/2, 2, 5/2, 3, 3, 3)$, so $N = 7$. The trace for $j = 2$ and $j = 4$, with $\alpha$ written as weights of old indices:

| $j$ | $t_j$, $\mu$ (L2) | round $r$ | $x = t_{j+r}$ (L5) | $a$ for $s = r-1, \ldots, 0$ (L7) | $\alpha$ after L8 |
|---|---|---|---|---|---|
| 2 | $0$, $2$ | 1 | $1/2$ | $1/2$ | $c_1{:}\ \tfrac12$, $c_2{:}\ \tfrac12$ |
| 2 | | 2 | $1$ | $1/2$, $1$ | $c_0{:}\ 0$, $c_1{:}\ \tfrac34$, $c_2{:}\ \tfrac14$ |
| 4 | $1$, $3$ | 1 | $3/2$ | $1/2$ | $c_2{:}\ \tfrac12$, $c_3{:}\ \tfrac12$ |
| 4 | | 2 | $2$ | $1/2$, $1$ | $c_1{:}\ 0$, $c_2{:}\ \tfrac34$, $c_3{:}\ \tfrac14$ |

So $d_2 = \tfrac34 (1, 2) + \tfrac14 (3, 3) = (3/2, 9/4)$ and $d_4 = \tfrac34 (3, 3) + \tfrac14 (5, 1) = (7/2, 5/2)$. All eight new points are

$$(0, 0),\ (1/2, 1),\ (3/2, 9/4),\ (5/2, 11/4),\ (7/2, 5/2),\ (9/2, 3/2),\ (11/2, 1/2),\ (6, 0),$$

the same as the result of three insertions by [Boehm knot insertion](/boehm-knot-insertion/). The full matrix is on the [knot refinement](/knot-refinement/) page.

For a cubic, take $\tau = (0, 0, 0, 0, 1, 2, 3, 3, 3, 3)$ with the control points $(0, 0), (1, 3), (3, 4), (5, 4), (7, 1), (8, 0)$, and $t = (0, 0, 0, 0, 1, 3/2, 2, 5/2, 3, 3, 3, 3)$. Row $j = 4$ is $\tfrac18 c_2 + \tfrac{11}{16} c_3 + \tfrac{3}{16} c_4$, with three nonzero weights, and the new points are $(0, 0), (1, 3), (5/2, 15/4), (4, 4), (41/8, 55/16), (13/2, 7/4), (15/2, 1/2), (8, 0)$.

## Correctness

The cleanest proof uses blossoms. Every polynomial $\pi$ of degree at most $p$ has a unique symmetric function $B[\pi](x_1, \ldots, x_p)$, affine in each argument, with $B[\pi](x, \ldots, x) = \pi(x)$. Three facts give the result. First, the triangle of lines L3 to L8 with the arguments $x_1, \ldots, x_p$ computes $B[\pi_\mu](x_1, \ldots, x_p)$, where $\pi_\mu$ is the piece of the curve on the span $\mu$; this follows from Marsden's identity, because for the curve $(y - x)^p$ the triangle gives $\prod_k (y - x_k)$. Second, on each span of $t$, the B-spline series with the coefficients $B[\pi](t_{j+1}, \ldots, t_{j+p})$ is $\pi$, again by Marsden's identity. Third, two pieces of the curve have the same blossom value when the arguments contain the knots between them, because the pieces join with the smoothness that the knot multiplicities give. The proof below checks that the knots between the span of line L2 and the span where $N^t_j$ is used are always among $t_{j+1}, \ldots, t_{j+p}$.

## Complexity

For each of the $N + 1$ new points, line L2 costs $O(\log n)$ by [binary search](/binary-search/), lines L4 to L8 cost $p(p + 1)/2$ steps, and line L9 costs $O(p d)$. The total is $\Theta(N (\log n + p^2 + p d))$ in the worst case, with $O(p)$ extra space for the row besides the output. When the new points are computed in order of $j$, line L2 can move forward from the last $\mu$, and the search costs $O(n + N)$ in total.

## Properties

- **Each point on its own.** The row for $d_j$ depends only on $j$, $\tau$ and $t$, not on other rows. Rows can be computed in parallel, or only for the points that are needed.
- **Convex rows.** Each row sums to 1, and its final entries are nonnegative. So each new point is a convex combination of at most $p + 1$ consecutive old points, and the refined polygon lies in the [convex hull](/convex-hull-property/) of the old one.
- **The matrix is reusable.** The rows depend on the knots only. For a surface or a family of curves with the same knots, the matrix is computed once and applied to every row of control points, or to every coordinate.
- **The same answer as Boehm.** The refined control points are unique, by the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/), so the Oslo algorithm and repeated Boehm insertion give the same points, in exact arithmetic.
- **Identity rows.** If no new knot lies near $t_j$, the row is a unit row: $d_j$ is an old point.
- **Evaluation as a special case.** If $t_{j+1} = \cdots = t_{j+p} = u$, the triangle computes $B[\pi_\mu](u, \ldots, u) = \pi_\mu(u)$. If $u$ lies in the span $\mu$, the row is the list of the basis values $N^\tau_{i,p}(u)$ of the Cox-de Boor recursion, and $d_j = C(u)$, the point that the [de Boor algorithm](/de-boor-algorithm/) computes.

## Variants and improvements

- **The triangle on the points.** The same rounds can run on the control points instead of the weights, as in the [de Boor algorithm](/de-boor-algorithm/) with a different parameter in each round. This saves the separate sum of line L9 but does not give the matrix, and it costs $O(p^2 d)$ per point instead of $O(p^2 + p d)$. The 1980 paper has two algorithms of the Oslo kind.
- **Lyche and Mørken (1986).** They showed that the discrete B-splines that are nonzero at one index are discrete B-splines of lower degree on fewer knots, which shortens the triangle, and they improved both algorithms of the 1980 paper.
- **Uniform subdivision.** For uniform knots and midpoint insertion, all rows in the middle are equal, and the method is the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/); for $p = 2$ it is [Chaikin corner cutting](/chaikin-corner-cutting/).
- **Rational curves and surfaces.** For [NURBS](/nurbs/), apply the rows to the homogeneous points $(w_i c_i, w_i)$. For a [tensor product surface](/tensor-product-surface/), compute the matrix for $u$ and the matrix for $v$, and apply them to the rows and the columns of the control net.

## When to use it

Use it when many knots are added at once, when the same refinement is applied to many curves or to a surface, when the knot insertion matrix itself is needed, for example for a least squares fit on the fine knots, or when only some of the new points are needed. For one or a few new knots, [Boehm knot insertion](/boehm-knot-insertion/) is shorter and needs fewer operations. For uniform subdivision, the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/) is simpler.

## Pitfalls

- **The clamp in line L2.** For $t_j < \tau_p$, which happens at the left end of an unclamped knot vector, there is no span of the domain that holds $t_j$, and line L2 must take $\mu = p$. Without the clamp, line L9 reads $c$ at negative indices. With the clamp, the intermediate entries of $\alpha$ can be negative: for $\tau = (0, 1, 2, 3, 4, 5)$, $p = 2$ and the new knot $5/2$, round 1 of row 0 gives $a = -1$ and the entries $2$ and $-1$, and round 2 gives the correct row $(1, 0, 0)$. The final rows are right, and they are nonnegative.
- **Empty end spans.** The clamp needs a nonempty span, so the algorithm needs $\tau_p < \tau_{p+1}$ and $\tau_n < \tau_{n+1}$. The implementation rejects other input.
- **The knot in line L5.** Round $r$ uses $t_{j+r}$, the knot $r$ places after $t_j$ in the fine vector. Using $t_{j+r-1}$, or the old knots, gives rows that do not reproduce the curve.
- **The old knots in line L7.** The weights use the old knots $\tau$, with an interval that grows with the round, as in the Cox-de Boor recursion. Using the fine knots here gives wrong rows.
- **The direction of line L6.** Running $s$ upward overwrites $\alpha[s]$ before line L8 reads it for $\alpha[s+1]$.
- **New knots at the ends of the domain.** On a clamped knot vector, a new knot at $\tau_p$ or $\tau_{n+1}$ would raise the multiplicity to $p + 2$. The implementation accepts only new knots strictly inside the domain.

## Implementations

## History

Elaine Cohen, Tom Lyche and Richard Riesenfeld introduced the algorithm in "Discrete B-splines and subdivision techniques in computer-aided geometric design and computer graphics", Computer Graphics and Image Processing, 1980. They showed that refinement of a knot vector, by any knots and with repeated knots, gives the new control points as values of the discrete B-splines, and that earlier subdivision schemes are special cases. The paper has two algorithms of this kind. In the same year, Wolfgang Boehm published the insertion of a single knot. Tom Lyche and Knut Mørken, at the University of Oslo, gave faster versions of both algorithms in 1986. Lyle Ramshaw's blossoms (1989) gave the short description $d_j = B[\pi](t_{j+1}, \ldots, t_{j+p})$.

## References
