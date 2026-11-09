---
tag: S8AASR
kind: algorithm
slug: ellipsoid-method
name: Ellipsoid method
aliases:
- Khachiyan's algorithm
- Shor-Khachiyan ellipsoid method
- central-cut ellipsoid method
area: optimization/linear-programming
level: advanced
summary: Shrink ellipsoids around the feasible region; the first polynomial-time LP algorithm.
solves: [linear-feasibility, linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of constraints, L: the bit length of the input}
  time: {worst: O(n^3 (m+n) L)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1979
  people: [Leonid Khachiyan, Naum Z. Shor, David B. Yudin, Arkadi Nemirovski]
  note: Shor and Yudin and Nemirovski developed the method for convex optimization in the 1970s; Khachiyan used it in 1979 to show that linear programming is in P.
prereqs: [linear-feasibility, positive-definite-matrix, separating-hyperplane-theorem]
see_also: [lp-in-p, separation-oracle, cutting-plane-method, karmarkar-algorithm, interior-point-method, simplex-method, minimum-volume-enclosing-ellipsoid, semidefinite-programming]
sources:
  - paper: doi:10.1016/0041-5553(80)90061-0
    title: L. G. Khachiyan, Polynomial algorithms in linear programming, USSR Computational Mathematics and Mathematical Physics 20(1), 1980
    locator: pages 53 to 72, the full version of the 1979 announcement
  - paper: doi:10.1007/bf01071394
    title: N. Z. Shor, Cut-off method with space extension in convex programming problems, Cybernetics 13(1), 1977
    locator: pages 94 to 96
  - paper: doi:10.1287/opre.29.6.1039
    title: Robert G. Bland, Donald Goldfarb and Michael J. Todd, The ellipsoid method, a survey, Operations Research 29(6), 1981
    locator: pages 1039 to 1091
  - paper: doi:10.1007/BF02579273
    title: Martin Grötschel, László Lovász and Alexander Schrijver, The ellipsoid method and its consequences in combinatorial optimization, Combinatorica 1(2), 1981
    locator: pages 169 to 197
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Chapter 8, Sections 8.2 to 8.5 (the key geometric result, the ellipsoid method for feasibility and for optimization, problems with exponentially many constraints)
  - book: isbn:9783642782428
    title: Martin Grötschel, László Lovász and Alexander Schrijver, Geometric Algorithms and Combinatorial Optimization, second edition, Springer, 1993
    locator: Chapter 3, The ellipsoid method
---

The ellipsoid method decides whether a convex set, such as the feasible region $\{x : Ax \le b\}$ of a [linear program](/linear-programming-problem/), contains a point. It keeps an ellipsoid that is sure to contain the set. At each step it tests the center; if the center is not in the set, a violated constraint cuts the ellipsoid in half through the center, and the method replaces the half by the smallest ellipsoid that contains it, which has a fixed fraction less volume. When the volume becomes smaller than the set can be, the set is empty. Khachiyan used it in 1979 to prove that [linear programming is in P](/lp-in-p/), and it needs only a [separation oracle](/separation-oracle/), not a list of the constraints.

## In plain words

Suppose that a treasure is somewhere inside a large egg-shaped region. Look at the middle of the egg. If the treasure is not at the middle, a hint tells you on which side of a flat cut through the middle it lies. Draw a new, smaller egg around that half, and repeat.

Each new egg has less volume than the last one by a fixed factor, so after a known number of steps the egg is smaller than any region that could still hold the treasure. Then you can say with certainty that the treasure does not exist. The method never needs the full list of constraints; at each step it only needs one constraint that the middle point breaks. This makes it a strong tool of theory, even though it is slow in practice.

## The problem

The input is a separation oracle for a convex set $K \subseteq \mathbb{R}^n$, and two radii $R > r > 0$, with the promise that $K$ lies in the ball $B(0, R)$, and that $K$ either is empty or contains some ball of radius $r$. The oracle, given a point $x$, says that $x \in K$, or returns a vector $g \ne 0$ with $g^\top z \le g^\top x$ for every $z \in K$. For $K = \{z : Az \le b\}$ the oracle returns a violated row $a_i$: then $a_i^\top z \le b_i < a_i^\top x$ for all $z \in K$.

The output is a point of $K$, or EMPTY. An ellipsoid is written $E(x, P) = \{z : (z - x)^\top P^{-1} (z - x) \le 1\}$, with center $x$ and a symmetric [positive definite](/positive-definite-matrix/) matrix $P$.

## The algorithm

```pseudo id=main
ELLIPSOID(oracle, n, R, r)
L1  x ← 0;  P ← R² I                                   ▷ E(x, P) is the ball B(0, R) ⊇ K
L2  for k = 0, 1, ..., N where N = ⌈2n(n + 1) ln(R / r)⌉
L3      if the oracle says x ∈ K then return x
L4      g ← the vector of the oracle                    ▷ K ⊆ {z : gᵀz ≤ gᵀx}
L5      b̃ ← P g / √(gᵀ P g)
L6      x ← x − b̃ / (n + 1)
L7      P ← n²/(n² − 1) · (P − 2/(n + 1) · b̃ b̃ᵀ)
L8  return EMPTY
```

Lines L5 to L7 compute the *Löwner-John ellipsoid* of the half-ellipsoid $E(x, P) \cap \{z : g^\top z \le g^\top x\}$, the ellipsoid of least volume that contains it. In the coordinates where $E(x, P)$ is the unit ball and $g$ points along the first axis, the new ellipsoid has center $-e_1/(n + 1)$, the semi-axis $n/(n + 1)$ along $e_1$ and the semi-axes $n/\sqrt{n^2 - 1}$ along the other axes. Its volume is

$$\frac{\operatorname{vol} E'}{\operatorname{vol} E} = \frac{n}{n + 1} \left(\frac{n^2}{n^2 - 1}\right)^{(n - 1)/2} < e^{-1/(2(n + 1))}.$$

For $n = 1$ the ellipsoid is an interval, and the cut keeps half of it.

*Linear programming.* To minimize $c^\top x$ over $K$, add *objective cuts*: if the center $x$ is feasible, use $g = c$, which keeps only the points with $c^\top z \le c^\top x$, and remember the best feasible center. Another way is binary search on the value $t$, with a feasibility test for $K \cap \{c^\top z \le t\}$ at each step. For a polyhedron $\{x : Ax \le b\}$ with integer data of bit length $L$, the radius $R = 2^{O(L)}$ is enough, and a small change of $b$ makes the set either empty or full-dimensional with $r = 2^{-O(L)}$. The [LP in P](/lp-in-p/) page gives these steps.

## Example

Find a point with $x_1 \ge 2$, $x_2 \ge 2$ and $x_1 + x_2 \le 5$, a triangle with corners $(2, 2)$, $(3, 2)$ and $(2, 3)$, starting from the disk of radius $4$ around the origin. Here $n = 2$, so each step multiplies the area by $\frac{2}{3}\sqrt{4/3} \approx 0.770$. The area is $\pi \sqrt{\det P}$.

| step | center $x$ | $\sqrt{\det P}$ | violated constraint |
|---|---|---|---|
| 0 | $(0, 0)$ | $16$ | $x_1 \ge 2$ |
| 1 | $(1.333, 0)$ | $12.317$ | $x_1 \ge 2$ |
| 2 | $(2.222, 0)$ | $9.481$ | $x_2 \ge 2$ |
| 3 | $(2.222, 1.778)$ | $7.299$ | $x_2 \ge 2$ |
| 4 | $(2.222, 2.963)$ | $5.619$ | $x_1 + x_2 \le 5$ |
| 5 | $(1.664, 2.404)$ | $4.325$ | $x_1 \ge 2$ |
| 6 | $(2.408, 2.032)$ | $3.330$ | none: the center is in the triangle |

At step 0 the cut $x_1 \ge 2$ keeps the right half of the disk; the new center is $(4/3, 0)$, and the new ellipse has the semi-axes $4 \cdot 2/3 = 8/3$ across the cut and $4 \cdot 2/\sqrt 3 \approx 4.62$ along it. The triangle has area $1/2$, so it fits only in an ellipse with $\sqrt{\det P} \ge 1/(2\pi) \approx 0.16$; if the triangle were empty, after about 12 more steps the method could report EMPTY.

## Correctness

Each new ellipsoid contains the half of the old one that the cut keeps, and $K$ lies in that half, so $K$ stays inside every ellipsoid. If the method returns a center, the oracle has accepted it. If it returns EMPTY, then after $N$ cuts the volume is less than $e^{-N/(2(n+1))} \operatorname{vol} B(0, R) \le \operatorname{vol} B(0, r)$, so $K$ cannot contain a ball of radius $r$, and by the promise $K$ is empty. The proof file proves the containment and the volume bound.

## Complexity

Model: arithmetic operations on reals have unit cost (the [real RAM](/real-ram/)), with a separate count of bits below.

- **Iterations.** $N = \lceil 2n(n + 1) \ln(R/r) \rceil = O(n^2 \log(R/r))$. For an LP with bit length $L$, $\log(R/r) = O(L)$, so $O(n^2 L)$ iterations decide feasibility. Optimization by binary search or by objective cuts needs only a constant factor more for this precision.
- **One iteration.** The update of lines L5 to L7 takes $O(n^2)$ operations. A check of all rows costs $O(mn)$. So the total is $O(n^2 L \cdot (mn + n^2)) = O(n^3 (m + n) L)$ operations, the bound of the front matter.
- **Bits.** The exact centers have huge bit lengths. Khachiyan showed that rounding to $O(nL)$ bits after the point, with the matrix $P$ blown up by a factor slightly above $1$ at each step, keeps the method correct. This gives a polynomial bound on the bit complexity as well.
- **Space.** $O(n^2)$ for $P$, besides the oracle.

The bound does not depend on $m$ except through the oracle. This is the key to its use for programs with exponentially many constraints.

## Properties

- **Polynomial, but slow.** The bound is polynomial, but the number of iterations is close to the bound in practice too, so the method is far slower than the simplex method and [interior-point methods](/interior-point-method/) on real programs.
- **Needs only separation.** It works with a [separation oracle](/separation-oracle/), so it solves programs with exponentially many constraints, such as the matching polytope or the subtour LP, in polynomial time if separation is polynomial.
- **Not exact in floating point.** It returns an approximate point; an exact optimal vertex needs a rounding step at the end.
- **General convex sets.** The same method works for any convex set with an oracle, for example for [semidefinite programs](/semidefinite-programming/).

## Variants and improvements

- **Deep cuts.** Cut with $g^\top z \le b_i$ instead of $g^\top z \le g^\top x$; the kept part is smaller, and the new ellipsoid is smaller too.
- **Shallow cuts and parallel cuts.** Variants for cuts that do not pass through the center, and for two parallel cuts at once.
- **Factored form.** Keep $P = J J^\top$ and update $J$; then $P$ stays positive definite in floating point. The implementation on this page does this.
- **Other cutting-plane methods.** The center of gravity method shrinks the volume by a constant factor $1 - 1/e$ per cut, but the center is hard to compute. The volumetric center and analytic center methods ([cutting-plane method](/cutting-plane-method/)) give better bounds in theory.
- **[Karmarkar's algorithm](/karmarkar-algorithm/) and interior-point methods.** They gave polynomial methods that are also fast in practice.

## When to use it

Use the ellipsoid method in proofs: to show that a problem with a polynomial-time separation oracle can be optimized in polynomial time, as in the equivalence of separation and optimization of Grötschel, Lovász and Schrijver. It is a good choice in practice only for small $n$ with a costly or implicit set of constraints, where its simple steps and low memory help. For explicit linear programs, use the [simplex method](/simplex-method/) or an [interior-point method](/interior-point-method/).

## Pitfalls

- **Loss of positive definiteness.** In floating point, the update of line L7 can give a matrix $P$ with a tiny negative eigenvalue after many steps, and then $g^\top P g$ is negative. Use the factored form, or blow up $P$ a little at each step.
- **Forgetting the volume promise.** An answer of EMPTY is correct only if the set either is empty or contains a ball of radius $r$. A feasible set of zero volume, for example an equality constraint, is never found; the LP version perturbs $b$ to make the set full-dimensional.
- **$n = 1$.** The factor $n^2/(n^2 - 1)$ is not defined; the method is then bisection of an interval.
- **Expecting early success.** The iteration count is close to the bound, even on easy problems.

## Implementations

The Python version keeps a factor $J$ with $P = JJ^\top$ in floats. `feasible_point(oracle, n, radius, inner)` is the method of this page, `rows_oracle(a, b)` builds the oracle for $Az \le b$, and `minimize` adds objective cuts. The tests check the volume ratio of each cut against the formula above with a determinant, that points of the kept half stay in the new ellipsoid, that a known feasible point stays in every ellipsoid of a run, the answers on 500 random feasible and infeasible systems, and that `minimize` comes within $10^{-6}$ of the optimum found by vertex enumeration in the plane.

## History

Shor (1977) and Yudin and Nemirovski (1976) developed the method of space dilation along a cut, as a method for convex optimization. In 1979 Khachiyan showed that it decides the feasibility of a system of linear inequalities in polynomial time, which proved that [linear programming is in P](/lp-in-p/); the result appeared on the front page of the New York Times. Grötschel, Lovász and Schrijver (1981), Karp and Papadimitriou, and Padberg and Rao showed that the method needs only a separation oracle, which made it a main tool of polyhedral combinatorics.

## References
