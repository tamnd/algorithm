---
tag: 6C4KQA
kind: problem
slug: semidefinite-programming
name: Semidefinite programming
aliases:
- SDP
- semidefinite program
- linear matrix inequality optimization
area: optimization/convex-optimization
level: advanced
summary: Linear optimization over the cone of positive semidefinite matrices.
prereqs: [linear-programming-problem, positive-definite-matrix, convex-optimization-problem]
see_also: [convex-relaxation, lovasz-theta-function, maximum-cut, second-order-cone-programming, interior-point-method, minimum-volume-enclosing-ellipsoid, lyapunov-equation, eigenvalue]
sources:
  - paper: doi:10.1137/1038003
    title: Lieven Vandenberghe and Stephen Boyd, Semidefinite programming, SIAM Review 38(1), 1996
    locator: pages 49 to 95
  - paper: doi:10.1137/0805002
    title: Farid Alizadeh, Interior point methods in semidefinite programming with applications to combinatorial optimization, SIAM Journal on Optimization 5(1), 1995
    locator: pages 13 to 51
  - paper: doi:10.1017/S0962492901000071
    title: Michael J. Todd, Semidefinite optimization, Acta Numerica 10, 2001
    locator: pages 515 to 560
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.6.2 (semidefinite programming), Section 5.9 (generalized inequalities and SDP duality)
  - paper: doi:10.1137/0806020
    title: Christoph Helmberg, Franz Rendl, Robert J. Vanderbei and Henry Wolkowicz, An interior-point method for semidefinite programming, SIAM Journal on Optimization 6(2), 1996
    locator: pages 342 to 361
  - paper: doi:10.1007/BF02614433
    title: Motakuri V. Ramana, An exact duality theory for semidefinite programming and its complexity implications, Mathematical Programming 77, 1997
    locator: pages 129 to 162
  - paper: doi:10.1023/A:1008203903341
    title: Lorant Porkolab and Leonid Khachiyan, On the complexity of semidefinite programs, Journal of Global Optimization 10(4), 1997
    locator: pages 351 to 365
  - paper: doi:10.1287/moor.23.2.339
    title: Gábor Pataki, On the rank of extreme matrices in semidefinite programs and the multiplicity of optimal eigenvalues, Mathematics of Operations Research 23(2), 1998
    locator: pages 339 to 358
  - paper: doi:10.1007/s10107-002-0352-8
    title: Samuel Burer and Renato D. C. Monteiro, A nonlinear programming algorithm for solving semidefinite programs via low-rank factorization, Mathematical Programming 95(2), 2003
    locator: pages 329 to 357
  - paper: doi:10.1137/S1052623497328987
    title: Christoph Helmberg and Franz Rendl, A spectral bundle method for semidefinite programming, SIAM Journal on Optimization 10(3), 2000
    locator: pages 673 to 696
  - book: isbn:9780898713343
    title: Stephen Boyd, Laurent El Ghaoui, Eric Feron and Venkataramanan Balakrishnan, Linear Matrix Inequalities in System and Control Theory, SIAM, 1994
    locator: Chapter 2 (standard problems involving linear matrix inequalities)
---

A semidefinite program (SDP) minimizes a linear function of a symmetric matrix $X$ subject to linear equations and the constraint that $X$ is [positive semidefinite](/positive-definite-matrix/). Its dual has a linear matrix inequality: a matrix that depends affinely on the variables must be positive semidefinite. SDP contains [linear programming](/linear-programming-problem/) (diagonal matrices) and [second-order cone programming](/second-order-cone-programming/), and it can express eigenvalue bounds, norms of matrices, sums of squares of polynomials and many stability conditions of control theory. Interior-point methods solve it to accuracy $\varepsilon$ in $O(\sqrt{n}\log(1/\varepsilon))$ iterations for matrices of order $n$. SDP is the main tool for [convex relaxations](/convex-relaxation/) of hard problems, as in the [Goemans-Williamson max-cut algorithm](/maximum-cut/) and the [Lovász theta function](/lovasz-theta-function/).

## In plain words

A linear program picks numbers that must not be negative. A semidefinite program picks a whole table of numbers, a symmetric matrix, and the rule is that the matrix must be "not negative" in the matrix sense: it must never turn a direction into a negative amount. This one rule hides infinitely many simple rules, one for each direction, but together they still make a region in one piece with no dents. So the best point can be found fast, and a matching dual problem proves that it is the best. The extra power of a matrix makes it possible to write problems about eigenvalues, about distances and about polynomials that a linear program cannot write.

## Definition

**Notation.** $\mathbb{S}^n$ is the space of real symmetric $n \times n$ matrices with the inner product $\langle C, X\rangle = \operatorname{tr}(CX) = \sum_{ij}C_{ij}X_{ij}$. We write $X \succeq 0$ when $X$ is positive semidefinite, that is, $v^\top Xv \ge 0$ for all $v$, or equivalently all [eigenvalues](/eigenvalue/) of $X$ are nonnegative.

**Input.** Matrices $C, A_1, \dots, A_m \in \mathbb{S}^n$ and a vector $b \in \mathbb{R}^m$.

**Problem.** The primal and the dual SDP are

$$\text{(P)}\ \min_{X \in \mathbb{S}^n}\ \langle C, X\rangle \ \text{ s.t. } \langle A_i, X\rangle = b_i\ (i = 1, \dots, m),\ X \succeq 0,$$

$$\text{(D)}\ \max_{y \in \mathbb{R}^m}\ b^\top y \ \text{ s.t. } S = C - \sum_{i=1}^m y_iA_i \succeq 0.$$

The constraint of (D) is a linear matrix inequality (LMI) in $y$.

**Output.** An optimal pair $X^*$, $(y^*, S^*)$ to a given accuracy, or a certificate of infeasibility. Exact answers can be irrational, so the output is an approximation.

**Duality.** The cone of positive semidefinite matrices is self-dual: $\langle S, X\rangle = \operatorname{tr}(S^{1/2}XS^{1/2}) \ge 0$ when $S, X \succeq 0$. So for feasible $X$ and $(y, S)$, the gap is $\langle C, X\rangle - b^\top y = \langle S, X\rangle \ge 0$. If (P) has a positive definite feasible point and (D) is feasible, then (D) attains its optimum and the two values are equal, and the same holds with the roles exchanged. At an optimal pair with zero gap, $\langle S, X\rangle = 0$ with $S, X \succeq 0$ gives $SX = 0$: the ranges of $X$ and $S$ are orthogonal, so $\operatorname{rank}X + \operatorname{rank}S \le n$. Without strict feasibility, the optimum can fail to be attained, and the two optimal values can differ.

## Variants

- **LMI feasibility.** Find $y$ with $F_0 + \sum_iy_iF_i \succeq 0$, or prove that none exists. Many problems of control theory have this form.
- **Eigenvalue optimization.** Minimize the largest eigenvalue, or the sum of the $k$ largest eigenvalues, of an affine matrix function. Each is an SDP.
- **Block-diagonal SDP.** $X$ is block diagonal, as when several small SDP, LP and SOCP constraints are combined. Solvers use the block structure.
- **Complex SDP.** $X$ is Hermitian. It reduces to a real SDP of twice the order. It is common in quantum information and signal processing.
- **Rank-constrained SDP.** Add $\operatorname{rank}X \le r$. The problem is no longer convex, and with $r = 1$ it contains [max-cut](/maximum-cut/), so it is NP-hard.
- **Sum-of-squares programs.** Find polynomials that are sums of squares subject to linear constraints on their coefficients. Each such constraint is an SDP constraint on a Gram matrix.

## Examples

**The largest eigenvalue.** For a symmetric $C$, $\lambda_{\max}(C) = \max\{\langle C, X\rangle : \operatorname{tr}X = 1,\ X \succeq 0\}$, and the dual is $\min\{t : tI - C \succeq 0\}$. For $C = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$, the primal optimum is $X^* = \tfrac12\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$, the projection on the eigenvector $(1, 1)/\sqrt2$, with $\langle C, X^*\rangle = 3$. The dual optimum is $t^* = 3$, with $S = 3I - C = \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix} \succeq 0$. The gap is $\langle S, X^*\rangle = \tfrac12(1 - 1 - 1 + 1) = 0$, and $SX^* = 0$, with $\operatorname{rank}X^* + \operatorname{rank}S = 2$.

**An LP as an SDP.** Restrict $X$ and all $A_i$ and $C$ to diagonal matrices. Then $X \succeq 0$ says that the diagonal is nonnegative, and (P) and (D) are a standard LP and its dual.

**A positive duality gap.** Minimize $x_1$ subject to

$$F(x) = \begin{bmatrix} 0 & x_1 & 0 \\ x_1 & x_2 & 0 \\ 0 & 0 & x_1 + 1 \end{bmatrix} \succeq 0.$$

The $2 \times 2$ minor in the upper left corner is $-x_1^2 \ge 0$, so $x_1 = 0$ and the optimal value is $0$. The dual is $\max -Z_{33}$ subject to $Z \succeq 0$, $2Z_{12} + Z_{33} = 1$ and $Z_{22} = 0$. A positive semidefinite $Z$ with $Z_{22} = 0$ has $Z_{12} = 0$, so $Z_{33} = 1$, and the dual value is $-1$. The gap is $1$. Neither problem has a strictly feasible point (Vandenberghe and Boyd, 1996).

**An optimum that is not attained.** Minimize $x_1$ subject to $\begin{bmatrix} x_1 & 1 \\ 1 & x_2 \end{bmatrix} \succeq 0$, that is, $x_1, x_2 \ge 0$ and $x_1x_2 \ge 1$. The infimum is $0$, and no feasible point reaches it.

**Huge solutions.** The constraints $x_1 \ge 2$ and $\begin{bmatrix} 1 & x_i \\ x_i & x_{i+1} \end{bmatrix} \succeq 0$ for $i = 1, \dots, n - 1$ say that $x_{i+1} \ge x_i^2$. So every feasible point has $x_n \ge 2^{2^{n-1}}$, a number with $2^{n-1}$ bits, from an input of size $O(n)$.

## Known algorithms

- **Primal-dual [interior-point methods](/interior-point-method/).** The function $-\log\det X$ is a [self-concordant](/self-concordant-function/) barrier for the cone with the parameter $n$, so path-following methods need $O(\sqrt{n}\log(1/\varepsilon))$ Newton steps (Nesterov and Nemirovski; Alizadeh, 1995). Common search directions are the HKM direction (Helmberg, Rendl, Vanderbei and Wolkowicz, 1996, and others), the Nesterov-Todd direction and the AHO direction. Each step forms the $m \times m$ Schur complement matrix with entries $\operatorname{tr}(A_iXA_jS^{-1})$, in $O(mn^3 + m^2n^2)$ time for dense data, and solves it in $O(m^3)$ time. This limits interior-point methods to $n$ and $m$ in the low thousands.
- **The [ellipsoid method](/ellipsoid-method/).** A separation oracle is easy: if $X$ is not positive semidefinite, an eigenvector $v$ with $v^\top Xv < 0$ gives the cut. With bounds on the size of the solution, this gives polynomial time to any accuracy (Grötschel, Lovász and Schrijver).
- **Low-rank factorization.** Write $X = RR^\top$ with $R \in \mathbb{R}^{n \times r}$ and solve the nonconvex problem in $R$ with a local method (Burer and Monteiro, 2003). By the rank bound below, $r$ about $\sqrt{2m}$ is enough for an optimal solution to exist, and in practice local methods often find it.
- **First-order methods.** The spectral [bundle method](/bundle-method/) for problems with a fixed trace (Helmberg and Rendl, 2000), [ADMM](/admm/) with projections onto the cone by an eigenvalue decomposition, and the Frank-Wolfe method, whose steps need only one extreme eigenvector.

## Bounds

- **Approximate solutions in polynomial time.** If the feasible set contains a ball of radius $r$ and lies in a ball of radius $R$, the ellipsoid method and interior-point methods find an $\varepsilon$-optimal point in time polynomial in the input size and $\log(R/(r\varepsilon))$.
- **The exact complexity is open.** Whether the feasibility of an LMI with rational data can be decided in polynomial time in the bit model is not known. The example above shows that a solution can need exponentially many bits. Ramana (1997) gave an exact dual of polynomial size and showed that the feasibility problem is in NP exactly when it is in co-NP. Porkolab and Khachiyan (1997) showed that it is in polynomial time when $n$ or $m$ is fixed.
- **Rank of optimal solutions.** If (P) has an optimal solution, it has one of rank $r$ with $r(r + 1)/2 \le m$ (Barvinok, 1995; Pataki, 1998).
- **Iteration bound.** The barrier parameter is $n$, so the $O(\sqrt{n}\log(1/\varepsilon))$ iteration bound grows with the matrix order, not with $m$.

## Reductions

- **LP to SDP.** Use diagonal matrices, as in the example.
- **SOCP to SDP.** $\|u\| \le t$ holds exactly when $\begin{bmatrix} tI & u \\ u^\top & t \end{bmatrix} \succeq 0$, by the [Schur complement](/schur-complement/).
- **Quadratic constraints.** For $P = LL^\top$, the convex constraint $x^\top Px + q^\top x + r \le 0$ is $\begin{bmatrix} I & L^\top x \\ x^\top L & -q^\top x - r \end{bmatrix} \succeq 0$.
- **Nonconvex QCQP to SDP relaxation.** Replace $xx^\top$ by $X$ with $\begin{bmatrix} 1 & x^\top \\ x & X \end{bmatrix} \succeq 0$. This is the Shor relaxation, used for [max-cut](/maximum-cut/) and described on the [convex relaxation](/convex-relaxation/) page.
- **Sums of squares.** A polynomial $p$ of degree $2d$ is a sum of squares exactly when $p(x) = z(x)^\top Qz(x)$ for some $Q \succeq 0$, where $z(x)$ is the vector of monomials of degree at most $d$. Matching coefficients gives linear constraints on $Q$.
- **Stability.** The linear system $\dot x = Ax$ is stable exactly when there is $P \succ 0$ with $A^\top P + PA \prec 0$, an LMI in $P$. See the [Lyapunov equation](/lyapunov-equation/).

## Applications

- **Combinatorial optimization.** The Goemans-Williamson $0.878$-approximation for [max-cut](/maximum-cut/), the [Lovász theta function](/lovasz-theta-function/), which computes the clique number and the chromatic number of perfect graphs in polynomial time, and SDP-based approximations for coloring and constraint satisfaction.
- **Control theory.** Stability, performance and controller design problems written as LMIs (Boyd, El Ghaoui, Feron and Balakrishnan, 1994).
- **Polynomial optimization.** Sum-of-squares and moment relaxations give lower bounds for the minimum of a polynomial, which are exact at a finite level in many cases.
- **Geometry and statistics.** The [minimum-volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/), optimal experimental design, sensor network localization and the nuclear norm relaxation of matrix completion.
- **Quantum information.** Optimal measurements, fidelities and entanglement tests are SDPs over density matrices.

## References
