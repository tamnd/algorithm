---
tag: AMSQV3
kind: problem
slug: region-of-attraction-estimation
name: Region of attraction estimation
aliases:
- domain of attraction estimation
area: control/stability
level: advanced
summary: Given a system and an asymptotically stable equilibrium, find a large set of initial states that is proved to lie in its region of attraction, often a sublevel set of a Lyapunov function.
prereqs: [region-of-attraction, lyapunov-function]
see_also: [region-of-attraction, sum-of-squares-programming, lyapunov-function, converse-lyapunov-theorem, positively-invariant-set, reachable-set-computation, maximal-positively-invariant-set, barrier-certificate]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 8.2, Region of Attraction (estimates by sublevel sets of Lyapunov functions and the trajectory reversing method)
  - paper: doi:10.1109/TAC.1985.1104057
    title: "R. Genesio, M. Tartaglia and A. Vicino, On the estimation of asymptotic stability regions: state of the art and new proposals, IEEE Transactions on Automatic Control 30(8), 747-755, 1985"
    locator: the survey of Lyapunov and non-Lyapunov estimation methods and the trajectory reversing method
  - book: isbn:9780857299581
    title: "G. Chesi, Domain of Attraction: Analysis and Control via SOS Programming, Lecture Notes in Control and Information Sciences 415, Springer, 2011"
    locator: estimates by sublevel sets of polynomial Lyapunov functions with sum-of-squares certificates
  - paper: "A. A. Ahmadi, A. Majumdar and R. Tedrake, Complexity of ten decision problems in continuous time dynamical systems, Proceedings of the American Control Conference, 2013, arXiv:1210.7420"
    locator: the hardness of deciding whether all solutions from a ball converge to an equilibrium, for polynomial vector fields of low degree
---

Region of attraction estimation asks for a set of initial states that is proved to lie in the [region of attraction](/region-of-attraction/) of an asymptotically stable equilibrium, and that is as large as possible. The region itself is defined on its own page, with its properties and the basic sublevel set estimate. This page is about the computational problem: what the input and output are, how hard it is, and which methods give a certified answer. The exact region is rarely computable, so every practical method gives an inner estimate, and the methods differ in how large the estimate is and in what kind of proof comes with it. The standard certificate is a sublevel set of a [Lyapunov function](/lyapunov-function/) inside the set where the function decreases.

## In plain words

A controller or a physical system works well near its operating point, but how far can the state be pushed before it no longer returns? A simulation from one initial state answers the question for that state only. An estimate of the region of attraction answers it for a whole set at once, with a proof. The usual proof is a bowl-shaped function that decreases along every solution in a region: a solution that starts below a level of the bowl stays below it and slides down to the bottom. The task is to find a bowl and a level that cover as much of the state space as possible.

## Definition

**Input.** A vector field $\dot x = f(x)$ on $\mathbb{R}^n$, usually polynomial or given by a formula, with $f(0) = 0$ and the origin asymptotically stable (for example, with a [Hurwitz](/hurwitz-matrix/) Jacobian). Sometimes also a class of candidate sets, such as ellipsoids or sublevel sets of polynomials of a given degree, and a measure of size, such as the volume or the radius of the largest ball inside.

**Output.** A set $\Omega$ with $0 \in \Omega$ and a certificate that $\Omega \subseteq \mathcal{R}_A$. The usual certificate is a continuously differentiable $V$ and a level $c > 0$ such that

1. $\Omega = \{x : V(x) \le c\}$ (or its connected component that contains $0$) is bounded;
2. $V(x) > 0$ for $x \ne 0$ in $\Omega$, and $V(0) = 0$;
3. $\nabla V(x) \cdot f(x) < 0$ for $x \in \Omega$, $x \ne 0$.

Then $\Omega$ is [positively invariant](/positively-invariant-set/) and every solution from it converges to $0$ (Khalil 2002, Section 8.2).

**The optimization problem.** Among the candidate pairs $(V, c)$ that satisfy 1 to 3, find one that maximizes the size of $\Omega$. For a fixed $V$ the best level is

$$c^*(V) = \inf\{V(x) : x \ne 0,\ \nabla V(x) \cdot f(x) \ge 0\},$$

when the sublevel sets below $c^*$ are bounded.

**The decision form.** Given $f$ and a set $K$ (a ball, a box, a polytope), decide whether $K \subseteq \mathcal{R}_A$.

## Variants

- **Fixed $V$, best level.** $V$ is given, often $V = x^T P x$ from the Lyapunov equation of the linearization. Only $c^*(V)$ is computed. This is a nonconvex minimization over the curve or surface $\nabla V \cdot f = 0$.
- **Search over $V$.** $V$ ranges over a class, such as quadratic forms or polynomials of degree $2d$. The joint search over $V$ and $c$ is not convex in general.
- **Inner and outer estimates.** An inner estimate is a set inside $\mathcal{R}_A$. An outer estimate is a set that contains $\mathcal{R}_A$; it shows which initial states surely fail. Outer estimates use other certificates, such as [barrier certificates](/barrier-certificate/) or occupation measures.
- **Robust estimates.** $f$ depends on an uncertain parameter in a known set, and $\Omega$ must lie in the region of attraction for every value. One $V$ for all parameters gives a conservative answer; a parameter-dependent $V$ gives a larger one.
- **Design to enlarge the region.** The controller is a variable too, as with input saturation, where the goal is a feedback whose closed loop has a large certified region. For linear systems with linear constraints, the [maximal positively invariant set](/maximal-positively-invariant-set/) can be computed as a polytope.
- **Discrete time.** For $x_{k+1} = F(x_k)$, condition 3 becomes $V(F(x)) - V(x) < 0$.
- **Other attractors.** The same problem for a stable [limit cycle](/limit-cycle/) uses a function of the distance to the cycle.

## Examples

**A system with a saddle on the boundary.** Take

$$\dot x_1 = -x_1 + x_2, \qquad \dot x_2 = -x_2 + x_1^2 .$$

The equilibria are $(0, 0)$ and $(1, 1)$. The Jacobian at the origin is $A = \begin{bmatrix} -1 & 1 \\ 0 & -1 \end{bmatrix}$, which is Hurwitz. At $(1, 1)$ the Jacobian $\begin{bmatrix} -1 & 1 \\ 2 & -1 \end{bmatrix}$ has the eigenvalues $-1 \pm \sqrt 2$, so $(1, 1)$ is a saddle, and its stable solutions form the boundary of $\mathcal{R}_A$. The region is unbounded and not convex.

*Quadratic $V$ from the linearization.* With $Q = I$, the equation $A^T P + P A = -I$ gives $P = \begin{bmatrix} 1/2 & 1/4 \\ 1/4 & 3/4 \end{bmatrix}$. For $V = x^T P x$,

$$\dot V = -(x_1^2 + x_2^2) + x_1^2 \left(\tfrac12 x_1 + \tfrac32 x_2\right) .$$

On the ray $x = \rho (\cos\theta, \sin\theta)$, $\dot V = -\rho^2 + \rho^3 g(\theta)$ with $g(\theta) = \cos^2\theta\, (\tfrac12 \cos\theta + \tfrac32 \sin\theta)$, so $\dot V = 0$ at $\rho = 1 / g(\theta)$ where $g(\theta) > 0$. Minimizing $V$ over these points gives $c^* = 0.91189$, reached at $(1.0538, 0.4226)$. Any estimate must have $c < V(1, 1) = 1.75$, because the saddle is not in $\mathcal{R}_A$.

*Searching over the shape.* With $P = \begin{bmatrix} 1 & b \\ b & c \end{bmatrix}$ and the best level for each $(b, c)$ on a grid, the estimates grow a lot. The table compares them with the true boundary, which the trajectory reversing method finds: integrate backward in time from points close to the saddle along its stable eigenvector $(1, -\sqrt 2)$ (classical Runge-Kutta, step $0.001$).

| Method | Certified set | Area | Largest disc inside |
|---|---|---|---|
| $V$ from $Q = I$ | $x^T P x < 0.91189$ | 5.1247 | radius 1.0041 |
| Best area on the grid ($b$ step 0.025, $c$ step 0.05) | $b = 0.525$, $c = 0.55$, level 2.55606 | 15.330 | radius 1.3779 |
| Best disc on a finer grid (step 0.0025) | $b = 0.5$, $c = 0.57$, level 2.56807 | 14.262 | radius 1.3899 |
| Trajectory reversing (the true boundary) | no certificate by itself | unbounded | radius 1.3916 |

The closest point of the boundary to the origin is near $(1.1510, 0.7821)$. Along the axes, the region of attraction meets the $x_1$-axis in the interval $(-4.109, 1.650)$ and the $x_2$-axis in $(-17.17, 2.211)$. The best ellipses come close to the true distance $1.3916$, but no ellipse can cover a region that is unbounded and not convex. Polynomial $V$ of higher degree, found by [sum-of-squares programming](/sum-of-squares-programming/), give larger estimates.

The levels in the table come from a numerical minimization over $\theta$, so they are numerical values, not proofs. A simulation from 360 points on each ellipse at $0.999$ times its level converged to the origin in every case. That is a check, not a proof either. A proof needs an exact or verified certificate, as in the algorithms below.

## Known algorithms

- **Sublevel set of a fixed $V$.** Compute $c^*(V)$ by minimizing $V$ on $\{\dot V = 0\}$. In two dimensions this is a one-dimensional search, as in the example. To certify the result, show that $\dot V < 0$ on $\{0 < V \le c\}$ by an exact algebraic argument, by [interval arithmetic](/interval-arithmetic/) on a cover of the set, or by a sum-of-squares certificate (Khalil 2002, Section 8.2).
- **Sum-of-squares programming.** For polynomial $f$ and $V$, condition 3 on $\{V \le c\}$ holds if there are a sum-of-squares polynomial $s(x)$ and a small $\varepsilon > 0$ such that
  $$-\nabla V \cdot f - \varepsilon |x|^2 - s(x)\, (c - V(x)) \ \text{ is a sum of squares}.$$
  For fixed $V$ and $c$ this is a semidefinite feasibility problem, and bisection on $c$ gives the best level that this certificate can prove. The joint search over $V$, $s$ and $c$ is bilinear. The usual method alternates: fix $V$ and find $s$ and $c$, then fix $s$ and find $V$, and repeat (Chesi 2011). Each step is a semidefinite program. If each step starts from the previous solution, which is still feasible, the estimate does not decrease, but the iteration can stop at a point that is not the global optimum.
- **Trajectory reversing.** In the plane, the boundary of $\mathcal{R}_A$ consists of solutions, often the stable solutions of saddles or an unstable limit cycle. Integrating backward in time from near the saddle, or from any point near the cycle, traces the boundary (Genesio, Tartaglia and Vicino 1985). This gives the true region with the accuracy of the integrator, not a certificate.
- **Backward reachability.** If a set $\Omega_0$ is a certified estimate, then every state whose solution enters $\Omega_0$ is in $\mathcal{R}_A$. [Reachable set computation](/reachable-set-computation/) backward from $\Omega_0$, by level set methods such as [Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/) or by set propagation, enlarges a small estimate. The cost grows quickly with the dimension.
- **Zubov's method.** The exact region is $\{W < 1\}$ for the solution $W$ of a first-order partial differential equation, in one form $\nabla W \cdot f = -h(x) (1 - W)$ with a chosen positive definite $h$. Series solutions truncated at a finite degree give estimates near the origin.
- **Simulation and sampling.** Simulate from many initial states and record which converge. This gives a picture of the region and a good candidate for $V$ or $c$, but no proof: a finite set of samples says nothing about the points between them. Simulations are useful to find counterexamples, since one diverging solution proves that its initial state is outside $\mathcal{R}_A$, and so gives an upper bound on the level $c$.

## Bounds

- **Exact answers.** No general method computes $\mathcal{R}_A$ exactly for nonlinear systems. For linear systems with linear constraints the related maximal positively invariant set is a polytope that a finite algorithm finds under the conditions given on that page.
- **Hardness.** For polynomial vector fields of low degree (typically $3$), deciding whether all solutions from a given ball converge to a given equilibrium has no polynomial-time algorithm, and not even a pseudo-polynomial-time one, unless P = NP (Ahmadi, Majumdar and Tedrake 2013). So the decision form is hard in the worst case, and the methods above are relaxations or heuristics.
- **Size of the SOS relaxations.** A certificate of degree $2d$ in $n$ variables uses a Gram matrix of size $\binom{n + d}{d}$ for each sum-of-squares term. For $n = 2$, $d = 2$ that is $6 \times 6$; for $n = 6$, $d = 3$ it is $84 \times 84$. The [semidefinite programs](/semidefinite-programming/) are solved by interior point methods in a time that is polynomial in the size and in $\log(1/\varepsilon)$ for accuracy $\varepsilon$, under strict feasibility; this is not an exact decision procedure.
- **Completeness in principle.** By the [converse Lyapunov theorem](/converse-lyapunov-theorem/) for the region of attraction, there is a smooth $V$ on $\mathcal{R}_A$ whose sublevel sets are compact subsets of $\mathcal{R}_A$ and fill it. So every compact subset of $\mathcal{R}_A$ is inside some sublevel set certificate. Quadratic $V$, as the example shows, can be far from this.

## Reductions

- **To nonnegativity of polynomials.** For polynomial $f$ and $V$, the check of a given pair $(V, c)$ is the question whether a polynomial is positive on a semialgebraic set. Sum-of-squares programming replaces it by a semidefinite program, with a Positivstellensatz certificate in the general case. The [S-procedure](/s-procedure/) is the quadratic case.
- **To reachability.** $\mathcal{R}_A$ is the set of states that reach a certified neighborhood of the equilibrium, so estimation reduces to a small certified estimate plus a backward reachable set.
- **From the problem of [Lur'e](/lure-problem/).** Absolute stability asks for a global answer for a family of nonlinearities. When only a local sector holds, the answer is an estimate of the region of attraction, often an ellipsoid found with a [linear matrix inequality](/linear-matrix-inequality/).

## Applications

- *Saturated control.* A linear controller for a plant with actuator limits is only locally valid. The certified region tells which initial states and disturbances the closed loop tolerates, and [anti-windup](/anti-windup/) design tries to enlarge it.
- *Power systems.* After a fault is cleared, the state must lie in the region of attraction of the post-fault equilibrium. Lyapunov estimates give a bound on the time to clear the fault.
- *Gain scheduling and motion planning.* A controller designed at many operating points is valid only if the region of each one contains the states where the next one hands over. Certified estimates make this check.
- *Model predictive control.* The terminal set of an MPC scheme is a certified invariant set of a local controller, often a sublevel set of a quadratic $V$.

## References
