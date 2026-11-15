---
tag: 501R5E
kind: technique
slug: sum-of-squares-programming
name: Sum-of-squares programming
aliases:
- SOS programming
- SOS optimization
area: control/stability
level: advanced
summary: Proves that a polynomial is nonnegative by writing it as a sum of squares, checked by a semidefinite program, and so finds polynomial Lyapunov functions.
prereqs: [semidefinite-programming, lyapunov-function]
see_also: [semidefinite-programming, lyapunov-function, region-of-attraction-estimation, s-procedure, linear-matrix-inequality, barrier-certificate, converse-lyapunov-theorem, hilbert-nullstellensatz]
sources:
  - paper: doi:10.1007/s10107-003-0387-5
    title: "P. A. Parrilo, Semidefinite programming relaxations for semialgebraic problems, Mathematical Programming 96(2), 293-320, 2003"
    locator: the Gram matrix form of the sum-of-squares condition and its use with Positivstellensatz certificates
  - paper: "P. A. Parrilo, Structured semidefinite programs and semialgebraic geometry methods in robustness and optimization, PhD thesis, California Institute of Technology, 2000"
    locator: the search for polynomial Lyapunov functions by sum-of-squares programs
  - paper: doi:10.1007/BF01443605
    title: "D. Hilbert, Über die Darstellung definiter Formen als Summe von Formenquadraten, Mathematische Annalen 32, 342-350, 1888"
    locator: the cases in which every nonnegative form is a sum of squares of forms
  - paper: doi:10.1512/iumj.1993.42.42045
    title: "M. Putinar, Positive polynomials on compact semi-algebraic sets, Indiana University Mathematics Journal 42(3), 969-984, 1993"
    locator: the representation of polynomials that are positive on a compact set with an archimedean description
  - paper: doi:10.1109/CDC.2011.6161499
    title: "A. A. Ahmadi, M. Krstic and P. A. Parrilo, A globally asymptotically stable polynomial vector field with no polynomial Lyapunov function, 50th IEEE Conference on Decision and Control, 2011"
    locator: the example of a quadratic vector field that is globally asymptotically stable and has no polynomial Lyapunov function
---

Sum-of-squares programming proves that a polynomial is nonnegative by writing it as a sum of squares of other polynomials. A sum of squares can never be negative, so the decomposition is a certificate that anyone can check by expanding it. The search for the squares is a [semidefinite program](/semidefinite-programming/): the polynomial must equal $z(x)^T Q z(x)$ for a vector $z(x)$ of monomials and a positive semidefinite matrix $Q$, and matching coefficients gives linear equations on $Q$. The coefficients of the polynomial can themselves be unknowns, provided that they enter linearly. This turns the search for a polynomial [Lyapunov function](/lyapunov-function/) $V$ into a convex problem: ask that $V$ and $-\dot V$ both be sums of squares, up to a small positive definite margin. Hilbert (1888) showed that most nonnegative polynomials are not sums of squares, so the method is a sufficient test, not an exact one. Parrilo (2000, 2003) gave the semidefinite formulation and its use for Lyapunov functions, [regions of attraction](/region-of-attraction-estimation/) and other questions in control.

## In plain words

A polynomial such as $2x^4 + 2x^3 y - x^2 y^2 + 5y^4$ is hard to check for negative values by looking at it. If one can write it as $\tfrac12 (2x^2 - 3y^2 + xy)^2 + \tfrac12 (y^2 + 3xy)^2$, the question is closed: squares are never negative. To find such squares, list the monomials that can appear inside them, here $x^2$, $y^2$ and $xy$. Any sum of squares of combinations of these monomials is $z^T Q z$ with $z = (x^2, y^2, xy)$ and $Q$ positive semidefinite, and any positive semidefinite $Q$ gives such a sum. So the task is to find a positive semidefinite matrix whose entries satisfy a few linear equations. That is a semidefinite program, and convex optimization solves it.

## When it applies

- The question is that a polynomial, or a family of polynomials with unknown coefficients that enter linearly, is nonnegative on $\mathbb{R}^n$ or on a set described by polynomial inequalities. Rational data can be cleared of denominators first.
- The number of variables $n$ and the degree $2d$ are small. With all monomials of degree at most $d$, the Gram matrix has size $\binom{n+d}{d}$ and there is one linear equation for each of the $\binom{n+2d}{2d}$ monomials of degree at most $2d$. For $n = 2$ and $2d = 4$ this is a $6 \times 6$ matrix and $15$ equations; for $n = 6$ and $2d = 8$ it is $210 \times 210$ with $3003$ equations.
- In control, the polynomials are a Lyapunov candidate $V$ and its derivative $\dot V = \nabla V \cdot f$ along a polynomial vector field $f$, a [barrier certificate](/barrier-certificate/), or the conditions of an [S-procedure](/s-procedure/) on a semialgebraic set. For a quadratic $V$ and a linear $f$ it reduces to a [linear matrix inequality](/linear-matrix-inequality/).

Deciding whether a polynomial of degree $4$ is nonnegative is [NP-hard](/np-hard/), so no fast exact test is expected. A semidefinite program is solved by an [interior point method](/interior-point-method/) to accuracy $\epsilon$ in time polynomial in the size of the matrices, the number of equations and $\log(1/\epsilon)$, under assumptions such as a strictly feasible point and a known bound on the solution. This is a statement about approximate solutions, not about an exact decision.

## The template

1. **Choose the degree and the monomials.** For a polynomial $p$ of degree $2d$, take $z(x)$ as the monomials of degree at most $d$. Remove every monomial whose exponent is not in half the Newton polytope of $p$, the convex hull of the exponents of $p$; such monomials cannot appear in any decomposition.
2. **Match coefficients.** Write $p(x) = z(x)^T Q z(x)$ with $Q$ symmetric. For each monomial $x^\alpha$, the sum of the entries $Q_{ij}$ with $z_i z_j = x^\alpha$ must equal the coefficient of $x^\alpha$ in $p$. This is a linear system $A u = b$ in the entries of $Q$ and in the free coefficients $c$ of $p$, if there are some.
3. **Solve the semidefinite program.** Find $u$ with $A u = b$ and every Gram block $Q_j \succeq 0$, or optimize a linear objective over this set, for example the largest $\gamma$ such that $p - \gamma$ is a sum of squares.
4. **Extract the squares.** Factor $Q = L D L^T$ with $D \ge 0$ diagonal; then $p = \sum_i d_i (\ell_i^T z)^2$, where $\ell_i$ is column $i$ of $L$. A [Cholesky decomposition](/cholesky-decomposition/) does the same for a positive definite $Q$.
5. **Make it a proof.** A numerical solver returns a $Q$ that satisfies the equations and the cone condition only up to a tolerance. If the computed $Q$ is positive definite with some margin, round it to rationals, project it back onto $A u = b$ in exact arithmetic, and check that it is still positive semidefinite.

For the search for a Lyapunov function of $\dot x = f(x)$ with $f(0) = 0$, the unknown is $V(x) = \sum_k c_k m_k(x)$ for chosen monomials $m_k$ with no constant or linear term, and the program has two constraints for a small $\epsilon > 0$: $V(x) - \epsilon \|x\|^2$ is a sum of squares, and $-\nabla V(x) \cdot f(x) - \epsilon \|x\|^2$ is a sum of squares. Both are linear in $c$. A solution gives $V(x) \ge \epsilon \|x\|^2$ and $\dot V(x) \le -\epsilon \|x\|^2$ on all of $\mathbb{R}^n$, so the origin is globally asymptotically stable.

The implementation solves the feasibility problem with a short method that needs no external solver, and it returns only exact certificates:

```pseudo id=main
SOS-FEASIBLE(constraints p_j(c) = z_j^T Q_j z_j for j = 1..k, margin ε)
L1  match coefficients: build the linear equations A u = b in u = (c, Q_1, ..., Q_k)
L2  u ← 0
L3  repeat at most T times
L4      u ← the orthogonal projection of u onto {u : A u = b}
L5      if λ_min(Q_j) ≥ ε/2 for every j then exit the loop
L6      for each j: write Q_j = V Λ V^T and set Q_j ← V max(Λ, ε) V^T     ▷ projection onto {Q ⪰ ε I}
L7  if the loop did not exit then return FAIL                          ▷ not a proof that no certificate exists
L8  round every entry of u to a fraction with a small denominator
L9  u ← the orthogonal projection of u onto {u : A u = b}, in exact rational arithmetic
L10 factor each Q_j = L D L^T exactly; if a pivot is negative then return FAIL
L11 return (c, Q_1, ..., Q_k)                                          ▷ an exact certificate
```

Lines L3 to L6 are alternating projections between the affine set and the closed convex set where every block satisfies $Q_j \succeq \epsilon I$. When the two sets intersect, alternating projections converge to a point of the intersection, often slowly. The off-diagonal entries are scaled by $\sqrt 2$ in $u$, so that the Euclidean distance on $u$ is the Frobenius distance on the matrices and line L6 is the true projection. Line L5 stops at a point that has a margin of $\epsilon/2$. The rounding in L8 and the exact projection in L9 move the matrices only a little, so the margin keeps them positive semidefinite in practice, and line L10 confirms it exactly. A returned result is therefore a proof: the equations hold exactly, and $L D L^T$ with $D \ge 0$ shows that every $Q_j$ is positive semidefinite. A FAIL means only that this search did not succeed. A production code uses an interior point solver in step 3 and keeps steps 4 and 5.

## Classic examples

**A Gram matrix family.** For $p = 2x^4 + 2x^3 y - x^2 y^2 + 5y^4$ and $z = (x^2, y^2, xy)$, matching coefficients gives $Q_{11} = 2$ from $x^4$, $Q_{22} = 5$ from $y^4$, $2Q_{13} = 2$ from $x^3 y$, $2Q_{23} = 0$ from $x y^3$, and $Q_{33} + 2Q_{12} = -1$ from $x^2 y^2$. One parameter is free:

$$Q(\lambda) = \begin{bmatrix} 2 & \lambda & 1 \\ \lambda & 5 & 0 \\ 1 & 0 & -1 - 2\lambda \end{bmatrix}.$$

Every $\lambda$ gives a matrix with $z^T Q(\lambda) z = p$, and $p$ is a sum of squares exactly when some $Q(\lambda)$ is positive semidefinite. For $\lambda = 0$ the last diagonal entry is $-1$, so that choice fails. For $\lambda = -3$ the exact factorization gives $D = (2, \tfrac12, 0)$, rank $2$, and the decomposition $p = \tfrac12 (2x^2 - 3y^2 + xy)^2 + \tfrac12 (y^2 + 3xy)^2$. For $\lambda = -2$ it gives $D = (2, 3, \tfrac{13}{6})$, a positive definite matrix and a sum of three squares. The determinant is $(\lambda + 3)(2\lambda^2 - 5\lambda - 5)$, and $Q(\lambda) \succeq 0$ exactly for $-3 \le \lambda \le (5 - \sqrt{65})/4 \approx -0.766$. The implementation finds a positive definite member of this interval and returns its exact factorization.

**The Motzkin polynomial.** $M(x, y) = x^4 y^2 + x^2 y^4 - 3x^2 y^2 + 1$ is nonnegative: the arithmetic mean of $x^4 y^2$, $x^2 y^4$ and $1$ is at least their geometric mean $x^2 y^2$. It is not a sum of squares. The Newton polytope of $M$ is the triangle with corners $(0,0)$, $(4,2)$ and $(2,4)$, so a square in a decomposition can only use the monomials $1$, $xy$, $x^2 y$ and $x y^2$. Of all products of two of these, only $xy \cdot xy$ equals $x^2 y^2$. So the coefficient $-3$ of $x^2 y^2$ must equal the diagonal entry $Q_{xy,xy}$, which cannot be negative in a positive semidefinite matrix. This is the standard example of a nonnegative polynomial that the method cannot certify; Motzkin published it in 1967.

**A Lyapunov function for a damped Duffing oscillator.** Take $\dot x_1 = x_2$, $\dot x_2 = -x_1 - x_2 - x_1^3$. A quadratic $V = a x_1^2 + b x_1 x_2 + c x_2^2$ cannot prove global asymptotic stability by this program: the quartic part of $-\dot V$ is $b x_1^4 + 2c x_1^3 x_2$, which takes both signs unless $c = 0$, and $c = 0$ makes $V$ indefinite or degenerate. With $V$ in the span of $x_1^2$, $x_1 x_2$, $x_2^2$ and $x_1^4$, and the Gram basis $(x_1, x_2, x_1^2)$ for both constraints, the program is feasible. One solution is

$$V = \tfrac34 x_1^2 + \tfrac12 x_1 x_2 + \tfrac12 x_2^2 + \tfrac14 x_1^4, \qquad \dot V = -\tfrac12 \left(x_1^2 + x_2^2 + x_1^4\right).$$

The quadratic part of $V$ has the matrix $\begin{bmatrix} 3/4 & 1/4 \\ 1/4 & 1/2 \end{bmatrix}$, with pivots $\tfrac34$ and $\tfrac{5}{12}$, so $V$ is positive definite and radially unbounded. The implementation finds a certificate of this form with $\epsilon = 1/100$ in a few milliseconds, and the tests check along a simulated solution that $V$ decreases at every step.

## Variations

- **Global lower bounds.** The largest $\gamma$ such that $p - \gamma$ is a sum of squares is a lower bound on $\min_x p(x)$, and it is exact when $p - p_{\min}$ is a sum of squares, for example for every univariate $p$. The dual of this program is a moment relaxation; Lasserre's hierarchy raises the degree step by step.
- **Nonnegativity on a set.** To show $p \ge 0$ where $g_1(x) \ge 0, \dots, g_m(x) \ge 0$, find sums of squares $s_0, \dots, s_m$ with $p = s_0 + \sum_i s_i g_i$. This is a polynomial [S-procedure](/s-procedure/). Putinar (1993) showed that every polynomial that is strictly positive on such a set has this form when the description of the set is archimedean, for example when one of the $g_i$ is $R^2 - \|x\|^2$. The degrees needed are not bounded in advance. The Positivstellensatz gives certificates of infeasibility in the same spirit, much as the [Nullstellensatz](/hilbert-nullstellensatz/) does for equations.
- **Regions of attraction.** For a local result, ask that $-\dot V - s(x)(\beta - V)$ is a sum of squares with $s$ a sum of squares. Then $\dot V < 0$ on the sublevel set $V \le \beta$. The product $s \cdot \beta$ is bilinear, so one fixes one factor, solves, and alternates, as described in [region-of-attraction estimation](/region-of-attraction-estimation/).
- **Smaller programs.** Newton polytope reduction, symmetry and sparsity cut the Gram matrix. Diagonally dominant and scaled diagonally dominant sums of squares (Ahmadi and Majumdar) replace the semidefinite constraint by linear or second-order cone constraints, with more conservatism.
- **Matrix sums of squares.** A polynomial matrix $P(x)$ is a sum of squares if $y^T P(x) y$ is one in $(x, y)$. This certifies state-dependent metrics for contraction and other matrix inequalities.

## Pitfalls

- A sum of squares is nonnegative, but a nonnegative polynomial need not be a sum of squares. Hilbert proved that the two sets are equal only for univariate polynomials, for quadratic polynomials and for bivariate quartics (in homogeneous form: binary forms, quadratic forms and ternary quartics). The Motzkin polynomial is a counterexample in two variables of degree $6$.
- $V$ a sum of squares gives only $V \ge 0$, not a positive definite $V$. Add the margin $\epsilon \|x\|^2$ or another positive definite term. This margin also excludes some correct Lyapunov functions: $V = \tfrac12 x_1^4 + x_2^2$ is not above $\epsilon (x_1^2 + x_2^2)$ near the origin.
- A polynomial vector field can be globally asymptotically stable and have no polynomial Lyapunov function of any degree. Ahmadi, Krstic and Parrilo (2011) gave the example $\dot x = -x + x y$, $\dot y = -y$. So a failed search at every degree tried does not show that the origin is not asymptotically stable; see the [converse Lyapunov theorem](/converse-lyapunov-theorem/).
- Numerical solvers accept small violations of the equations and of the cone. A solver message "feasible" is not a proof. Round and check exactly, as in step 5. Peyrl and Parrilo (2008) studied this rounding and projection.
- The rounding step needs a margin, so it needs a strictly feasible point. If the basis contains a monomial that the Newton polytope rules out, every positive semidefinite $Q$ that satisfies the equations has a zero row and column for it, and no positive definite $Q$ exists. In the Lyapunov search, the constant monomial $1$ in the basis for $V - \epsilon\|x\|^2$ has this problem, because $V(0) = 0$ forces $Q_{11} = 0$. With such a basis the method of this page fails, and interior point solvers become inaccurate. Remove the monomials first.
- The size grows as $\binom{n+d}{d}$. Ten variables with a quartic $V$ already need several matrices of size $66$, and degree $8$ in ten variables needs size $1001$.

## Exercises

1. Show that $x^4 + 1$ is a sum of squares, and find all Gram matrices for $z = (1, x, x^2)$. Which of them have rank $2$?
2. For the family $Q(\lambda)$ above, verify the determinant $(\lambda + 3)(2\lambda^2 - 5\lambda - 5)$ and show that $Q(\lambda) \succeq 0$ exactly for $-3 \le \lambda \le (5 - \sqrt{65})/4$.
3. Show that for a univariate polynomial $p$ of even degree, the largest $\gamma$ such that $p - \gamma$ is a sum of squares equals $\min_x p(x)$.
4. For $\dot x_1 = -x_1 + x_2$, $\dot x_2 = -x_1^3 - x_2$, show that $V = \tfrac12 x_1^4 + x_2^2$ gives $\dot V = -2x_1^4 - 2x_2^2$. Explain why the two constraints with the margin $\epsilon \|x\|^2$ reject this $V$, and propose a margin that accepts it.
5. Write the program for the Duffing example with $V$ in the span of $x_1^2$, $x_1 x_2$ and $x_2^2$ only, and prove by hand that it is infeasible for every $\epsilon > 0$.

## References
