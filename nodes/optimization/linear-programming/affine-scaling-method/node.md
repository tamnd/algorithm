---
tag: CWE5Y6
kind: algorithm
slug: affine-scaling-method
name: Affine scaling method
aliases:
- Dikin affine scaling
- Dikin's method
- primal affine scaling
area: optimization/linear-programming
level: advanced
summary: Interior-point method that rescales variables at each step to move toward the optimum.
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of constraints}
  time: {per_step: O(m^2 n)}
  space: {extra: O(m n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1967
  people: [I. I. Dikin, Earl R. Barnes, Robert J. Vanderbei, Marc S. Meketon, Barry A. Freedman]
  note: Dikin published the method in 1967; it was found again in 1986 as a simple form of Karmarkar's algorithm.
prereqs: [lp-standard-form, least-squares-problem, reduced-cost]
see_also: [karmarkar-algorithm, interior-point-method, central-path, barrier-method, simplex-method, dual-linear-program, klee-minty-cube, ellipsoid-method]
sources:
  - paper: "I. I. Dikin, Iterative solution of problems of linear and quadratic programming, Soviet Mathematics Doklady 8, 1967"
    locator: pages 674 to 675, the method with the step in the inscribed ellipsoid
  - paper: doi:10.1007/BF02592024
    title: Earl R. Barnes, A variation on Karmarkar's algorithm for solving linear programming problems, Mathematical Programming 36(2), 1986
    locator: pages 174 to 182
  - paper: doi:10.1007/BF01840454
    title: Robert J. Vanderbei, Marc S. Meketon and Barry A. Freedman, A modification of Karmarkar's linear programming algorithm, Algorithmica 1, 1986
    locator: pages 395 to 407, the step to a fraction of the boundary and the convergence for nondegenerate programs
  - paper: doi:10.1137/0805027
    title: Takashi Tsuchiya and Masakazu Muramatsu, Global convergence of a long-step affine scaling algorithm for degenerate linear programming problems, SIAM Journal on Optimization 5(3), 1995
    locator: pages 525 to 551, convergence of the primal and the dual iterates for step fractions up to 2/3
  - paper: doi:10.1016/0167-6377(93)90040-N
    title: Leslie A. Hall and Robert J. Vanderbei, Two-thirds is sharp for affine scaling, Operations Research Letters 13(4), 1993
    locator: pages 197 to 201
  - paper: doi:10.1137/S1052623493258404
    title: Walter F. Mascarenhas, The affine scaling algorithm fails for stepsize 0.999, SIAM Journal on Optimization 7(1), 1997
    locator: pages 34 to 46
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Chapter 9, Sections 9.1 (the affine scaling algorithm) and 9.2 (its convergence)
---

The affine scaling method solves a [linear program](/linear-programming-problem/) in [standard form](/lp-standard-form/) by a walk through the interior of the feasible region. At each step it rescales every variable by its current value, so that the current point becomes the all-ones vector, far from every wall $x_j = 0$. In the new scale it goes in the steepest direction down the cost, then it scales back. It is the simplest interior-point method: one weighted [least squares problem](/least-squares-problem/) per step, no barrier parameter and no projective map. Dikin found it in 1967, and it was found again in 1986 as a simpler form of [Karmarkar's algorithm](/karmarkar-algorithm/).

## In plain words

The method starts at a point strictly inside the feasible region. If it went straight downhill, it would soon hit a wall and have to stop. So before each step it stretches the space: a variable with a small value, close to its wall, is stretched a lot, and a variable with a large value is stretched a little. After the stretch, every wall is equally far away, and the method can safely go far in the downhill direction. Then it undoes the stretch.

The step stops at a fixed fraction of the way to the nearest wall, so the point always stays inside. The cost falls at every step. The numbers that the method computes on the way also give an estimate of the dual solution, and the gap between the two values tells when to stop.

## The problem

Minimize $c^\top x$ subject to $Ax = b$, $x \ge 0$, with $A \in \mathbb{R}^{m \times n}$. The input also has a strictly feasible point $x^0$: $Ax^0 = b$ and $x^0 > 0$. (If none is known, a phase one with an artificial variable, as in the [big-M method](/big-m-method/), gives one.) The output is an approximately optimal $x > 0$ with a dual estimate $y$, or UNBOUNDED with a ray $d \ge 0$, $Ad = 0$, $c^\top d < 0$.

## The algorithm

Let $X = \operatorname{diag}(x)$. In the scaled variables $u = X^{-1} x$, the current point is $u = e$, the constraints are $AXu = b$, and the cost is $(Xc)^\top u$. The steepest descent direction in the null space of $AX$ is $-X r$, where $r = c - A^\top y$ and $y$ solves the least squares problem $\min_y \|X(c - A^\top y)\|$. Back in $x$, the direction is $d = -X^2 r$.

```pseudo id=main
AFFINE-SCALING(A, c, x⁰, γ = 2/3, ε)
L1  x ← x⁰                                  ▷ Ax = b and x > 0
L2  loop
L3      X ← diag(x);  y ← (A X² Aᵀ)⁻¹ A X² c    ▷ the dual estimate
L4      r ← c − Aᵀ y                           ▷ the reduced costs at y
L5      if r ≥ 0 and xᵀ r ≤ ε then return OPTIMAL(x, y)
L6      d ← −X² r                              ▷ Ad = 0 and cᵀd = −‖X r‖²
L7      if d ≥ 0 then return UNBOUNDED(d)
L8      x ← x + γ / max_j(x_j r_j) · d          ▷ a fraction γ of the way to the wall
```

The step of line L8 sends the coordinate $j$ with the largest $x_j r_j$ to the value $(1 - \gamma) x_j$, and every other coordinate $j$ to at least $(1 - \gamma) x_j$. The *short step* version uses $x \leftarrow x + \beta d / \|Xr\|$ with $\beta < 1$ instead; then $x$ stays in Dikin's ellipsoid $\{z : \|X^{-1}(z - x)\| \le \beta\}$, which lies in the region $z \ge 0$.

The stop test of line L5 is a duality gap. If $r \ge 0$, then $y$ is feasible for the [dual program](/dual-linear-program/), and $c^\top x - b^\top y = x^\top r$, so the value $c^\top x$ is within $x^\top r$ of the optimum.

## Example

Maximize $x_1 + x_2$ subject to $x_1 + 2x_2 \le 4$ and $3x_1 + x_2 \le 6$. In standard form, minimize $-x_1 - x_2$ with the slacks $x_3$ and $x_4$:

$$A = \begin{pmatrix} 1 & 2 & 1 & 0 \\ 3 & 1 & 0 & 1 \end{pmatrix}, \quad b = \begin{pmatrix} 4 \\ 6 \end{pmatrix}, \quad c = (-1, -1, 0, 0).$$

The optimum is $x = (1.6, 1.2, 0, 0)$ with value $-2.8$, and the dual optimum is $y = (-0.4, -0.2)$. Start at $x^0 = (1, 1, 1, 2)$ with $\gamma = 2/3$.

| step | $x$ | $c^\top x$ | $y$ |
|---|---|---|---|
| 0 | $(1, 1, 1, 2)$ | $-2$ | $(-0.3729, -0.1525)$ |
| 1 | $(1.3030, 1.1818, 0.3333, 0.9091)$ | $-2.4848$ | $(-0.4078, -0.1870)$ |
| 2 | $(1.5099, 1.1672, 0.1557, 0.3030)$ | $-2.6771$ | $(-0.3995, -0.1994)$ |
| 3 | $(1.5677, 1.1902, 0.0519, 0.1068)$ | $-2.7579$ | $(-0.4000, -0.1999)$ |

At step 0, $r = (-0.1695, -0.1017, 0.3729, 0.1525)$, so $Xr = (-0.1695, -0.1017, 0.3729, 0.3051)$ and $d = -X^2 r = (0.1695, 0.1017, -0.3729, -0.6102)$. The largest $x_j r_j$ is $0.3729$ at the slack $x_3$, so the step length is $(2/3)/0.3729 = 1.788$, and $x_3$ goes from $1$ to $1/3$. The slacks of the two tight constraints shrink toward $0$ at each step, and $y$ converges to the dual optimum. With $\varepsilon = 10^{-9}$ the method stops after 19 steps; with $\gamma = 0.99$ it needs 8, and with $\gamma = 0.5$ it needs 28.

## Correctness

Each step keeps $Ax = b$ (since $Ad = 0$ by the normal equations of line L3) and $x > 0$ (since every coordinate keeps at least the fraction $1 - \gamma$ of its value). The cost falls by $t\|Xr\|^2$ for the step length $t$, so it falls strictly unless $Xr = 0$, and then $x^\top r = 0$ and the method stops. An answer OPTIMAL comes with a dual feasible $y$ and the gap $x^\top r \le \varepsilon$. An answer UNBOUNDED comes with a ray $d \ge 0$, $Ad = 0$, $c^\top d < 0$. The proof file proves these facts.

That the method reaches the stop test is a deeper result. For programs whose primal is not degenerate, Dikin (1974) and Vanderbei, Meketon and Freedman (1986) proved convergence. For all programs, Tsuchiya and Muramatsu (1995) proved that with $\gamma \le 2/3$ the iterates converge to an optimal point of the interior of the optimal face, and the dual estimates converge to an optimal dual point. Hall and Vanderbei (1993) showed that $2/3$ is the largest fraction for which the dual estimates always converge, and Mascarenhas (1997) gave a program on which $\gamma = 0.999$ makes the primal iterates converge to a point that is not optimal.

## Complexity

Model: arithmetic operations on reals have unit cost (the [real RAM](/real-ram/)).

- **One step.** Forming $AX^2A^\top$ costs $O(m^2 n)$, its Cholesky factorization $O(m^3)$, and the rest $O(mn)$. With $m \le n$ this is $O(m^2 n)$, the bound of the front matter. Sparse programs use sparse factorizations.
- **Number of steps.** No polynomial bound is known for the method. Near an optimal vertex of a program that is not degenerate, the cost converges linearly. Megiddo and Shub (1989) showed that the continuous paths of the method can pass close to every vertex of a [Klee-Minty cube](/klee-minty-cube/), which suggests that the short step version can need an exponential number of steps.
- **Space.** $O(mn)$ for the scaled matrix $AX$ and $O(m^2)$ for its normal matrix.

## Properties

- **Interior and monotone.** Every point is strictly feasible, and the cost falls at every step.
- **Dual estimates for free.** The vector $y$ of line L3 converges to a dual optimum under the conditions above, and $x^\top r$ is a computable duality gap.
- **Invariant under scaling of the variables.** The direction does not change if a column of $A$ and the matching $c_j$ are multiplied by a positive number.
- **Not polynomial in theory, fast in practice.** In the 1980s, codes based on affine scaling were among the first interior-point codes that beat the simplex method on large programs.

## Variants and improvements

- **Dual affine scaling.** Apply the same idea to the dual program, $\max b^\top y$ subject to $A^\top y \le c$, with the scaling by the dual slacks. Adler, Karmarkar, Resende and Veiga built an early fast code on it.
- **Primal-dual affine scaling.** Scale by $X$ and the dual slacks together; this is the predictor step of Mehrotra's predictor-corrector method, the core of modern [interior-point solvers](/interior-point-method/).
- **Centering.** Adding a pull toward the [central path](/central-path/) gives the [barrier method](/barrier-method/) and path-following methods, which have polynomial bounds.
- **[Karmarkar's algorithm](/karmarkar-algorithm/).** Adds a projective map and a potential function, and gets a polynomial bound.

## When to use it

Use it to learn interior-point methods, or for a quick solver that needs only least squares. For real programs, prefer a primal-dual interior-point method with centering, or the [simplex method](/simplex-method/) when a vertex solution, warm starts or sensitivity data are needed.

## Pitfalls

- **Steps too long.** A fraction $\gamma$ near $1$ is faster, but the method can then fail on degenerate programs (Mascarenhas, $\gamma = 0.999$). Use $\gamma \le 2/3$ when convergence must be sure.
- **Ill-conditioned normal equations.** As coordinates go to $0$, the matrix $AX^2A^\top$ becomes nearly singular, especially on degenerate programs. Solve the least squares problem with an orthogonal factorization or with care in the Cholesky factorization. The implementation uses Gram-Schmidt with dependent rows skipped.
- **Detecting unboundedness in floats.** In exact arithmetic the test is $d \ge 0$. In floats, the coordinates that go to $0$ keep tiny negative entries of $d$ forever, and the other coordinates grow without bound. Test whether the positive entries of $Xr$ are tiny next to $\|Xr\|$ instead.
- **No start point.** The method needs $x^0 > 0$ with $Ax^0 = b$. A vertex is not a valid start.

## Implementations

The Python version uses floats. The least squares problem of line L3 is solved by a two-pass Gram-Schmidt process on the rows of $AX$, which gives $Xr$ and $y$ together. The tests build 600 random programs with integer data and a rational interior point. Three in four have a bounded optimum, which a brute force over all bases finds exactly in fractions; the method must match it within $10^{-6}$, and $b^\top y$ must match it too. The other programs have a known ray, and the method must report UNBOUNDED with a valid ray. The tests also check that the cost never rises and that every point is feasible and positive.

## History

I. I. Dikin published the method in 1967, and proved its convergence for nondegenerate programs in 1974, but his work was little known outside the Soviet Union. After Karmarkar's paper of 1984, Barnes (1986) and Vanderbei, Meketon and Freedman (1986) proposed the method again, as a form of Karmarkar's algorithm without the projective map. Its convergence on degenerate programs stayed open until Tsuchiya and Muramatsu (1995).

## References
