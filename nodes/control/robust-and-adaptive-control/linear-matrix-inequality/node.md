---
tag: 7J5JP2
kind: definition
slug: linear-matrix-inequality
name: Linear matrix inequality
aliases:
- LMI
area: control/robust-and-adaptive-control
level: core
summary: "A constraint F(x) = F_0 + x_1 F_1 + ... + x_k F_k > 0 with symmetric F_i. Its feasible set is convex, so stability and norm tests in this form are solved as semidefinite programs."
prereqs: [positive-definite-matrix, semidefinite-programming]
see_also: [semidefinite-programming, schur-complement, lyapunov-theorem-for-linear-systems, bounded-real-lemma, s-procedure, quadratic-stability, kalman-yakubovich-popov-lemma, lmi-h-infinity-synthesis]
sources:
  - book: isbn:089871334X
    title: Stephen Boyd, Laurent El Ghaoui, Eric Feron and Venkataramanan Balakrishnan, Linear Matrix Inequalities in System and Control Theory, SIAM Studies in Applied Mathematics 15, SIAM, 1994
    locator: Section 1.2 (a brief history of LMIs in control theory), Sections 2.1 and 2.2 (LMIs and the standard problems LMIP, EVP and GEVP), Section 2.4 (interior-point methods) and Section 2.5 (strict and nonstrict LMIs)
  - paper: "Jan C. Willems, Least squares stationary optimal control and the algebraic Riccati equation, IEEE Transactions on Automatic Control 16(6), 621-634, 1971"
    locator: the link between the Riccati equation, the frequency domain inequality and the linear matrix inequality
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Chapter 12, Linear Matrix Inequalities
---

A linear matrix inequality (LMI) is a constraint that a symmetric matrix, whose entries depend affinely on unknown real numbers, be positive definite (or, in the other sign convention, negative definite). The set of unknowns that satisfy it is convex, so the search for a feasible point, or for the best point under a linear cost, is a [semidefinite program](/semidefinite-programming/) and can be solved to any accuracy by interior point methods. Many tests in control take this form: Lyapunov stability, the H-infinity norm bound of the [bounded real lemma](/bounded-real-lemma/), [quadratic stability](/quadratic-stability/) of uncertain systems, and state feedback design after a change of variables. The first LMI in control is Lyapunov's: $A^T P + P A < 0$ with $P > 0$.

## Definition

**Standard form.** Let $F_0, F_1, \dots, F_k$ be real symmetric $N \times N$ matrices. A linear matrix inequality in $x \in \mathbb{R}^k$ is

$$F(x) = F_0 + x_1 F_1 + \dots + x_k F_k > 0,$$

where $> 0$ means [positive definite](/positive-definite-matrix/). The nonstrict LMI is $F(x) \ge 0$ (positive semidefinite). In this area, an LMI written with $< 0$ means negative definite, which is the same as $-F(x) > 0$.

**Matrix variables.** In control the unknowns are usually matrices. For example, with $A \in \mathbb{R}^{n \times n}$ given,

$$P > 0, \qquad A^T P + P A < 0$$

is an LMI in the symmetric matrix $P$. It fits the standard form: write $P = \sum_i x_i E_i$ for a basis $E_1, \dots, E_k$ of the symmetric $n \times n$ matrices, $k = n(n+1)/2$, and put the two conditions in one block diagonal matrix $\operatorname{diag}(P, -(A^T P + P A)) > 0$ of size $N = 2n$. Any finite set of LMIs is one LMI in this way.

**Convexity.** If $F(x) > 0$ and $F(y) > 0$, then $F(\theta x + (1 - \theta) y) = \theta F(x) + (1 - \theta) F(y) > 0$ for $\theta \in [0, 1]$, because $F$ is affine and the positive definite matrices form a convex cone. So the feasible set is convex. It is open for a strict LMI and closed for a nonstrict one. It is in general not a polyhedron: its boundary is curved.

**Schur complements.** Many convex but nonlinear constraints become LMIs by the [Schur complement](/schur-complement/) lemma: for symmetric $Q$, $R$ and any $S$,

$$\begin{bmatrix} Q & S \\ S^T & R \end{bmatrix} > 0 \iff R > 0 \text{ and } Q - S R^{-1} S^T > 0 .$$

For example, the Riccati inequality $A^T P + P A + P B R^{-1} B^T P + C^T C < 0$ with $R > 0$ is not affine in $P$, but it is equivalent to the LMI $\begin{bmatrix} A^T P + P A + C^T C & P B \\ B^T P & -R \end{bmatrix} < 0$.

**Standard problems.** Three problems recur (Boyd, El Ghaoui, Feron and Balakrishnan 1994, Section 2.2):

- **Feasibility (LMIP).** Find $x$ with $F(x) > 0$, or show that none exists.
- **Linear objective (EVP).** Minimize $c^T x$ subject to $F(x) \ge 0$. This is a semidefinite program. The smallest $\gamma$ with $\|G\|_\infty < \gamma$ by the bounded real lemma is of this kind.
- **Generalized eigenvalue problem (GEVP).** Minimize $\lambda$ subject to $\lambda B(x) - A(x) > 0$, $B(x) > 0$ and $C(x) > 0$, with $A$, $B$, $C$ affine. It is quasiconvex, and it is solved by bisection on $\lambda$ or by special interior point methods. The best decay rate certified by a quadratic Lyapunov function is of this kind.

**Solving.** An LMI problem with $k$ scalar variables and an $N \times N$ matrix is a semidefinite program of that size. A primal-dual [interior point method](/interior-point-method/) finds a point within $\varepsilon$ of optimal in $O(\sqrt{N} \log(1/\varepsilon))$ iterations, each a Newton step of cost about $O(k^2 N^2 + k N^3)$ flops for dense data, when the problem is strictly feasible and a starting point is known; see the semidefinite programming page for the exact assumptions. The [ellipsoid method](/ellipsoid-method/) is also polynomial in $k$ and $\log(1/\varepsilon)$, but slower in practice. For the Lyapunov LMI, $k = n(n+1)/2$, so the cost per iteration grows like $n^6$: LMIs are practical for tens of states, while the [Lyapunov equation](/lyapunov-equation/) itself costs $O(n^3)$.

**Strict and nonstrict.** A strict LMI that is feasible has a feasible set with an interior, and small errors in the data do not destroy feasibility. Solvers return points of the nonstrict problem, so a strict LMI is usually checked with a margin: $F(x) \ge \epsilon I$. The certificate of a feasible point is a Cholesky factorization of $F(x) - \epsilon I$. A certificate of infeasibility is a dual matrix $Z \ge 0$, $Z \ne 0$, with $\operatorname{trace}(F_i Z) = 0$ for $i \ge 1$ and $\operatorname{trace}(F_0 Z) \le 0$ ([Lagrangian duality](/lagrangian-duality/) for semidefinite programs).

**Riccati equations and LMIs.** Willems (1971) related the algebraic Riccati equation to the LMI

$$\begin{bmatrix} A^T P + P A + Q & P B + S \\ B^T P + S^T & R \end{bmatrix} \ge 0, \qquad R > 0 .$$

For $(A, B)$ controllable, this LMI is feasible exactly when a frequency domain inequality holds and exactly when the Riccati equation $A^T P + P A + Q - (P B + S) R^{-1} (B^T P + S^T) = 0$ has a real symmetric solution. The Riccati equation then has a largest solution, which is also the largest solution of the LMI. The [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) is the general form of this link.

## Examples and non-examples

- **Lyapunov stability, the check value.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ (eigenvalues $-1$ and $-2$). The matrix $P = \begin{bmatrix} 5/4 & 1/4 \\ 1/4 & 1/4 \end{bmatrix}$ has $\det P = 1/4 > 0$ and trace $3/2 > 0$, so $P > 0$, and $A^T P + P A = -I < 0$ exactly. So $P$ satisfies the LMI and proves that $A$ is [Hurwitz](/hurwitz-matrix/) (by the [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/)). Here $k = 3$ and $N = 4$.
- **Non-example of feasibility: an imaginary eigenvalue.** For $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, with eigenvalue $j$ and eigenvector $v$, every symmetric $P$ gives $v^H (A^T P + P A) v = (\bar\lambda + \lambda)\, v^H P v = 0$. So $A^T P + P A$ is never negative definite, and the LMI is infeasible. The nonstrict LMI $A^T P + P A \le 0$ is feasible, with $P = I$: strict and nonstrict LMIs can differ.
- **A curved feasible set.** $\begin{bmatrix} x_1 & 1 \\ 1 & x_2 \end{bmatrix} \ge 0$ holds exactly when $x_1 \ge 0$, $x_2 \ge 0$ and $x_1 x_2 \ge 1$: the region above a branch of a hyperbola. It is convex but not a polyhedron, so it is not a set of linear inequalities.
- **State feedback, after a change of variables.** The closed-loop Lyapunov condition $(A + B K)^T P + P (A + B K) < 0$ is bilinear in $(K, P)$, so it is not an LMI. Multiply by $Q = P^{-1}$ on both sides and set $Y = K Q$. The condition becomes $A Q + Q A^T + B Y + Y^T B^T < 0$ with $Q > 0$, an LMI in $(Q, Y)$, and $K = Y Q^{-1}$. For the double integrator $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, the point $Q = \begin{bmatrix} 1 & -1 \\ -1 & 5 \end{bmatrix}$, $Y = \begin{bmatrix} 1 & -13 \end{bmatrix}$ gives $A Q + Q A^T + B Y + Y^T B^T = \begin{bmatrix} -2 & 6 \\ 6 & -26 \end{bmatrix} < 0$ (determinant 16, trace $-28$), and $K = Y Q^{-1} = \begin{bmatrix} -2 & -3 \end{bmatrix}$: the closed loop is the matrix of the first example. See [state feedback](/state-feedback/).
- **Non-example: a rank constraint.** The set of $P \ge 0$ with $\operatorname{rank} P \le 1$ is not convex (the average of $\operatorname{diag}(1, 0)$ and $\operatorname{diag}(0, 1)$ has rank 2), so it is not the feasible set of any LMI. Output feedback and reduced order controller design lead to such constraints, and they are not LMI problems in general.

## Related definitions

- [Semidefinite programming](/semidefinite-programming/): the optimization problem behind every LMI problem, with its duality and solvers.
- [Schur complement](/schur-complement/): the lemma that turns many convex matrix inequalities into LMIs.
- [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/): the first LMI test, $P > 0$ and $A^T P + P A < 0$.
- [Bounded real lemma](/bounded-real-lemma/) and [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/): LMIs equivalent to frequency domain inequalities.
- [S-procedure](/s-procedure/): turns a quadratic inequality on a set into an LMI with a multiplier.
- [Quadratic stability](/quadratic-stability/) and [common Lyapunov function](/common-lyapunov-function/): one Lyapunov matrix for many systems, found by LMIs at the vertices.
- [LMI H-infinity synthesis](/lmi-h-infinity-synthesis/): the controller design by LMIs.
- [Sum of squares programming](/sum-of-squares-programming/): LMIs on the coefficients of polynomials, for nonlinear systems.

## References
