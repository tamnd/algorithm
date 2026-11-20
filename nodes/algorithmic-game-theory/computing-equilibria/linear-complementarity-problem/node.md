---
tag: B708RE
kind: problem
slug: linear-complementarity-problem
name: Linear complementarity problem
aliases:
- linear complementarity
area: algorithmic-game-theory/computing-equilibria
level: core
summary: Given a matrix M and vector q, find z >= 0 with w = Mz + q >= 0 and z^T w = 0. Nash equilibria of bimatrix games are solutions of one.
prereqs: [linear-programming-problem, lp-duality, complementary-slackness]
see_also: [lemke-algorithm, lemke-howson-algorithm, rigid-contact-complementarity, projected-gauss-seidel, quadratic-programming, kkt-conditions, nash-equilibrium-computation, ppad]
sources:
  - book: "Richard W. Cottle, Jong-Shi Pang and Richard E. Stone, The Linear Complementarity Problem, Academic Press, 1992"
    title: Richard W. Cottle, Jong-Shi Pang and Richard E. Stone, The Linear Complementarity Problem
    locator: the problem, its sources (quadratic programs, bimatrix games, contact problems), the matrix classes and the pivoting and iterative methods
  - paper: doi:10.1007/BF00940344
    title: "Sung-Jin Chung, NP-completeness of the linear complementarity problem, Journal of Optimization Theory and Applications 60(3) (1989), 393-399"
    locator: deciding whether an LCP has a solution is NP-complete
  - paper: doi:10.1287/mnsc.11.7.681
    title: "C. E. Lemke, Bimatrix equilibrium points and mathematical programming, Management Science 11(7) (1965), 681-689"
    locator: the LCP of a bimatrix game and the complementary pivot method for the general LCP
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel), the equilibria of a bimatrix game as the solutions of an LCP
---

The linear complementarity problem (LCP) asks: given an $n \times n$ matrix $M$ and a vector $q$, find $z \ge 0$ such that $w = Mz + q \ge 0$ and $z_i w_i = 0$ for every $i$. Each index is a switch with two states: either $z_i = 0$ and $w_i$ is free to be positive, or $w_i = 0$ and $z_i$ is free to be positive. In rigid-body simulation, $z_i$ is the impulse (or force) at contact $i$ and $w_i$ is the velocity at which the two bodies separate there: a contact can push but not pull, it pushes only if the bodies stay together, and $M$ says how the impulses at all the contacts change all the velocities ([rigid contact complementarity](/rigid-contact-complementarity/)). Physics engines often solve it approximately with [projected Gauss-Seidel](/projected-gauss-seidel/), and pivoting methods such as [Lemke's algorithm](/lemke-algorithm/) solve it exactly. The same problem describes the optimality conditions of linear and quadratic programs and the Nash equilibria of two-player games. The general problem is NP-complete; what is easy or hard depends on the class of $M$.

## In plain words

There are $n$ pairs of numbers. In each pair both numbers must be zero or positive, and at least one of them must be zero. The second number of each pair is a fixed linear function of all the first numbers: a matrix times them, plus a vector. Find the first numbers. If you knew which member of each pair is zero, a linear system would give the answer. So the problem is a choice among $2^n$ patterns, and the matrix decides whether there is one answer, many, or none, and how hard it is to find.

## Definition

**LCP$(q, M)$.** Input: $M \in \mathbb{Q}^{n \times n}$ and $q \in \mathbb{Q}^n$. Find $z \in \mathbb{R}^n$ with

$$z \ge 0, \qquad w = Mz + q \ge 0, \qquad z^{\mathsf T} w = 0 .$$

Because $z \ge 0$ and $w \ge 0$, the last condition is the same as $z_i w_i = 0$ for each $i$. A vector $z$ with $z \ge 0$ and $Mz + q \ge 0$ is feasible; a feasible $z$ with $z^{\mathsf T} w = 0$ is a solution. A short form is $0 \le z \perp Mz + q \ge 0$.

For each set $S \subseteq \{1, \ldots, n\}$ the pattern "$w_i = 0$ for $i \in S$ and $z_i = 0$ for $i \notin S$" gives the linear system $M_{SS} z_S = -q_S$. A solution is a pattern whose system has a solution with $z_S \ge 0$ and with the other entries of $w$ nonnegative. This gives a finite but exponential algorithm.

The class of $M$ decides the main properties.

| class of $M$ | definition | what it gives |
|---|---|---|
| positive definite | $z^{\mathsf T} M z > 0$ for $z \ne 0$ (not necessarily symmetric) | a P-matrix: a unique solution for every $q$; polynomial time |
| P-matrix | every principal minor is positive | a unique solution for every $q$, and P-matrices are exactly the matrices with this property; Lemke's method finds it |
| positive semidefinite | $z^{\mathsf T} M z \ge 0$ for all $z$ | if feasible, solvable; the solution set is convex; polynomial time by interior point methods |
| copositive-plus | $z^{\mathsf T} M z \ge 0$ for $z \ge 0$, and $z \ge 0$, $z^{\mathsf T} M z = 0$ imply $(M + M^{\mathsf T}) z = 0$ | if feasible, solvable, and Lemke's method finds a solution or proves infeasibility |
| strictly copositive | $z^{\mathsf T} M z > 0$ for $z \ge 0$, $z \ne 0$ (for example $M > 0$ entrywise) | a solution for every $q$; Lemke's method finds one |
| copositive | $z^{\mathsf T} M z \ge 0$ for $z \ge 0$ | no guarantee by itself; the LCP of a bimatrix game has such an $M$ |
| general | none | deciding whether a solution exists is NP-complete |

The statement that P-matrices are exactly the matrices for which LCP$(q, M)$ has a unique solution for every $q$ is a classical theorem of Samelson, Thrall and Wesler (1958).

## Variants

- **Mixed LCP.** Some variables are free and some rows are equations, as in the KKT conditions with equality constraints, or in contact with bilateral joints. It reduces to the standard form by splitting free variables or by eliminating them when their block is nonsingular.
- **Box-constrained LCP.** Each $z_i$ lies in an interval $[\ell_i, u_i]$, and $w_i$ has the sign that points into the box, or is 0 inside it. Physics engines use this form for friction with a bound proportional to the normal force.
- **Nonlinear complementarity problem.** $w = F(z)$ for a nonlinear map $F$.
- **Variational inequality.** Find $z$ in a convex set $K$ with $(y - z)^{\mathsf T} F(z) \ge 0$ for all $y \in K$; the LCP is the case $K = \mathbb{R}^n_{\ge 0}$ and $F(z) = Mz + q$.
- **Search versus decision.** For P-matrices and strictly copositive matrices a solution always exists, so the problem is a total search problem; for general $M$ the question is whether a solution exists.

## Examples

- **A block on the floor.** One contact, unit mass, $M = (1)$. If the block moves down at speed 2, $q = (-2)$ and the solution is $z = 2$, $w = 0$: the floor gives an impulse of 2 and the block stops. If it moves up at speed 1, $q = (1)$ and the solution is $z = 0$, $w = 1$: no impulse.
- **Two coupled contacts.** $M = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, $q = (-1, 1)$. The solution is $z = (1/2, 0)$ with $w = (0, 3/2)$; the worked pivots are on the [Lemke's algorithm](/lemke-algorithm/) page.
- **No solution.** $M = (-1)$, $q = (-1)$: $w = -z - 1 < 0$ for all $z \ge 0$.
- **Two solutions.** $M = (-1)$, $q = (1)$: $z = 0$, $w = 1$ and $z = 1$, $w = 0$ both work. $M$ is not a P-matrix, because its only principal minor is negative.
- **Bimatrix games.** For an $m \times n$ game with positive payoff matrices $A$ and $B$, the problem $0 \le x \perp \mathbf 1 - Ay \ge 0$, $0 \le y \perp \mathbf 1 - B^{\mathsf T} x \ge 0$ on the [best response polytopes](/best-response-polytope/) is an LCP whose solutions other than $x = 0$, $y = 0$, with $x$ and $y$ scaled to sum 1, are the Nash equilibria; the [Lemke-Howson algorithm](/lemke-howson-algorithm/) solves it.

## Known algorithms

- **Enumeration of the $2^n$ patterns.** Exact and exponential; useful as a reference for small $n$.
- **[Lemke's algorithm](/lemke-algorithm/)** (1965). A complementary pivoting method with an artificial variable. It solves P-matrix, strictly copositive and copositive-plus problems, the last with a proof of infeasibility when it ends on a ray. Exponential in the worst case (Murty 1978).
- **[Lemke-Howson algorithm](/lemke-howson-algorithm/)** (1964). The special case for bimatrix games, started from the artificial solution $z = 0$ by dropping a label.
- **Principal pivoting methods.** Murty's least index method and the Cottle-Dantzig method work on P-matrices and some other classes, without an artificial variable.
- **Iterative splitting methods.** [Projected Gauss-Seidel](/projected-gauss-seidel/) and projected SOR update one $z_i$ at a time and clip it at 0. They converge for symmetric positive definite $M$, and they are the usual choice in real-time physics, with a fixed number of sweeps.
- **[Interior point methods](/interior-point-method/).** Polynomial time for positive semidefinite $M$, where the LCP is a convex [quadratic program](/quadratic-programming/).
- **Newton-type methods.** Semismooth Newton methods on a reformulation such as the Fischer-Burmeister function, with fast local convergence.

## Bounds

- The general LCP is NP-complete: Chung (1989) showed that deciding whether a solution exists is NP-complete.
- The LCP of a bimatrix game always has a nontrivial solution, and finding one is [PPAD](/ppad/)-complete, because it is the problem of finding a Nash equilibrium of a two-player game ([Nash equilibrium computation](/nash-equilibrium-computation/)).
- For a P-matrix a solution always exists and is unique, and the problem is in the class CLS (Daskalakis and Papadimitriou, 2011); no polynomial-time algorithm is known.
- For positive semidefinite $M$ the LCP is solvable in polynomial time, by interior point or ellipsoid methods for convex quadratic programs.
- Complementary pivot methods take $2^n$ pivots on some LCPs of order $n$ (Murty 1978).

## Reductions

- **Linear programming to LCP.** The pair of LPs $\min c^{\mathsf T} x$ subject to $Ax \ge b$, $x \ge 0$ and $\max b^{\mathsf T} y$ subject to $A^{\mathsf T} y \le c$, $y \ge 0$ has optimal solutions $x$, $y$ exactly when $z = (x, y)$ solves the LCP with $M = \begin{pmatrix} 0 & -A^{\mathsf T} \\ A & 0 \end{pmatrix}$ and $q = (c, -b)$. This is [complementary slackness](/complementary-slackness/), and $M$ is skew-symmetric, so it is positive semidefinite.
- **Convex quadratic programming to LCP.** The [KKT conditions](/kkt-conditions/) of $\min \tfrac12 x^{\mathsf T} Q x + c^{\mathsf T} x$ subject to $Ax \ge b$, $x \ge 0$, with $Q$ positive semidefinite, are the LCP with $M = \begin{pmatrix} Q & -A^{\mathsf T} \\ A & 0 \end{pmatrix}$, $q = (c, -b)$.
- **Bimatrix games to LCP.** The example above is LCP$(q, M)$ with $z = (x, y)$, $M = \begin{pmatrix} 0 & -A \\ -B^{\mathsf T} & 0 \end{pmatrix}$ and $q = \mathbf 1$. Because $q \ge 0$, the trivial solution $z = 0$ is always there and gives no equilibrium; Lemke-Howson starts from it. The [Lemke's algorithm](/lemke-algorithm/) page gives a different LCP with a positive $M$ and $q = -\mathbf 1$, on which Lemke's method with the all-ones covering vector always ends with an equilibrium.
- **Extensive-form games to LCP.** With the [sequence form](/sequence-form/), an equilibrium of a two-player game tree with perfect recall is a solution of an LCP of size linear in the tree.

## Applications

- **Contact and friction in physics simulation.** The impulses at the contacts of rigid bodies at each time step, with a linearized friction cone, solve an LCP ([rigid contact complementarity](/rigid-contact-complementarity/)). Cloth and particle contact give similar problems.
- **Game theory.** Equilibria of two-player games in strategic and in extensive form.
- **Optimization.** Linear and convex quadratic programs, through their optimality conditions.
- **Economics and engineering.** Market equilibrium models, traffic equilibrium, and the analysis of structures with unilateral supports and of circuits with ideal diodes.

## References
