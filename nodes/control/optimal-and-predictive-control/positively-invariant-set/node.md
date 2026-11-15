---
tag: G27P38
kind: definition
slug: positively-invariant-set
name: Positively invariant set
aliases:
- forward invariant set
area: control/optimal-and-predictive-control
level: core
summary: A set of states that a trajectory never leaves once it is inside, for a system with a fixed feedback.
prereqs: [state-space-representation, lyapunov-stability]
see_also: [control-invariant-set, maximal-positively-invariant-set, lyapunov-function, lyapunov-equation, lasalle-invariance-principle, controlled-invariant-subspace, recursive-feasibility, barrier-certificate]
sources:
  - paper: doi:10.1016/S0005-1098(99)00113-2
    title: Franco Blanchini, Set invariance in control, Automatica 35(11), 1747-1767, 1999
    locator: the survey of positively invariant and controlled invariant sets, contractive sets, ellipsoidal and polyhedral sets, and the tangent cone condition of Nagumo for continuous time
  - book: isbn:9783319179322
    title: Franco Blanchini and Stefano Miani, Set-Theoretic Methods in Control, 2nd edition, Birkhäuser, 2015
    locator: the chapters on invariant sets, on ellipsoidal and polyhedral invariant sets, and on their computation
  - paper: doi:10.1109/9.83532
    title: Elmer G. Gilbert and K. T. Tan, Linear systems with state and control constraints, the theory and application of maximal output admissible sets, IEEE Transactions on Automatic Control 36(9), 1008-1020, 1991
    locator: the maximal positively invariant set inside the output constraints for linear systems and its finite determination
  - book: isbn:9781107016880
    title: Francesco Borrelli, Alberto Bemporad and Manfred Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017
    locator: the chapter on invariant sets, with the predecessor set and the algorithms for the maximal invariant sets
---

A positively invariant set of a dynamical system is a set of states that the trajectory never leaves once it is inside. The system has no free input here: it is autonomous, such as a plant with a fixed feedback law $u = \kappa(x)$. Positive invariance is a property of the pair of a set and a system. A sublevel set of a [Lyapunov function](/lyapunov-function/) is the classic example. In predictive control, positively invariant sets inside the constraints are used as terminal sets: once the state is in such a set, a known controller keeps it there and meets the limits for all future time.

## Definition

Let $x_{k+1} = f(x_k)$ be a discrete-time system on $\mathbb{R}^n$. A set $\Omega \subseteq \mathbb{R}^n$ is **positively invariant** if

$$x \in \Omega \implies f(x) \in \Omega.$$

By induction, $x_0 \in \Omega$ then gives $x_k \in \Omega$ for all $k \ge 0$. With the predecessor set $\operatorname{Pre}(\Omega) = \{x : f(x) \in \Omega\}$, the condition is $\Omega \subseteq \operatorname{Pre}(\Omega)$.

For a continuous-time system $\dot x = f(x)$ with unique solutions, $\Omega$ is positively invariant if $x(0) \in \Omega$ implies $x(t) \in \Omega$ for all $t \ge 0$.

Three qualifiers are common.

- **Robust.** For $x_{k+1} = f(x_k, w_k)$ with a disturbance $w_k$ in a set $\mathbb{W}$, $\Omega$ is robust positively invariant if $f(x, w) \in \Omega$ for all $x \in \Omega$ and all $w \in \mathbb{W}$.
- **Constraint admissible.** For a constraint set $\mathbb{X}$, $\Omega$ is admissible if $\Omega \subseteq \mathbb{X}$. For a closed loop $f(x) = g(x, \kappa(x))$ with input limits $\mathbb{U}$, the condition also includes $\kappa(x) \in \mathbb{U}$ on $\Omega$.
- **Contractive.** For $0 \le \lambda < 1$ and a set $\Omega$ that contains the origin, $\Omega$ is $\lambda$-contractive if $f(x) \in \lambda\, \Omega$ for all $x \in \Omega$.

## Examples and non-examples

- **Trivial sets.** The empty set, $\mathbb{R}^n$, and any equilibrium $\{x_e\}$ with $f(x_e) = x_e$ are positively invariant. So is the forward orbit $\{x_0, f(x_0), f(f(x_0)), \dots\}$ of any point.
- **Lyapunov sublevel sets (theorem).** If $V(f(x)) \le V(x)$ for all $x$ in a set that contains $\{V \le \alpha\}$, then $\{x : V(x) \le \alpha\}$ is positively invariant: from $V(x) \le \alpha$ follows $V(f(x)) \le V(x) \le \alpha$.
- **Ellipsoids for linear systems (theorem).** For $x_{k+1} = A x_k$ with $A$ Schur, take $P > 0$ from the [Lyapunov equation](/lyapunov-equation/) $A^T P A - P = -Q$ with $Q > 0$. Then every ellipsoid $\{x : x^T P x \le \alpha\}$ is positively invariant, and in fact contractive.
- **Boxes for linear systems (theorem).** The box $\{x : \|x\|_\infty \le 1\}$ is positively invariant for $x_{k+1} = A x_k$ if and only if $\|A\|_\infty = \max_i \sum_j |a_{ij}| \le 1$. The same holds for any norm ball and the induced matrix norm.
- **Non-example: a Schur matrix and a box.** $A = \begin{bmatrix} 0.5 & 1 \\ 0 & 0.5 \end{bmatrix}$ is Schur (both eigenvalues are 0.5), but $\|A\|_\infty = 1.5$, and the corner $(1, 1)$ of the unit box maps to $(1.5, 0.5)$, outside the box. Every trajectory still tends to 0, but this box is not positively invariant. An ellipsoid from the Lyapunov equation is.
- **Non-example: an unstable mode.** For the double integrator without control, $x_{k+1} = (x_1 + x_2, x_2)$, no bounded set with a point where $x_2 \ne 0$ is positively invariant, because $x_1$ grows without bound.
- **Polyhedral example.** For the rotation by $\arccos(3/5)$ scaled by $9/10$, the [maximal positively invariant set](/maximal-positively-invariant-set/) page computes the largest positively invariant set inside the unit box: an octagon. Without the scaling, the largest one is the unit disc, which is not a polyhedron.

## Related definitions

- **Invariant set.** $\Omega$ is invariant if $f(\Omega) = \Omega$, so trajectories stay in it both forward and backward. Positive invariance asks only for the forward direction. The [LaSalle invariance principle](/lasalle-invariance-principle/) uses invariant sets in this stronger sense.
- **Control invariant set.** For a system with an input, $x_{k+1} = f(x_k, u_k)$, a set is [control invariant](/control-invariant-set/) if for each state in it some admissible input keeps the next state in it. A positively invariant set of the closed loop $f(x, \kappa(x))$ with admissible $\kappa$ is control invariant for the open loop.
- **Maximal positively invariant set.** The union of all positively invariant subsets of a constraint set $\mathbb{X}$ is again positively invariant. It is the largest one, $\mathcal{O}_\infty$, the set of initial states whose trajectory stays in $\mathbb{X}$ forever. See [maximal positively invariant set](/maximal-positively-invariant-set/).
- **Minimal robust positively invariant set.** For a Schur linear system with a bounded disturbance, the smallest closed robust positively invariant set that contains the origin; it is used in [tube MPC](/tube-mpc/).
- **Tangent cone condition.** In continuous time, a closed set $\Omega$ is positively invariant for a system with unique solutions if and only if $f(x)$ lies in the tangent cone of $\Omega$ at every $x \in \Omega$ (Nagumo's theorem, as stated in Blanchini 1999).
- **Controlled invariant subspace.** In geometric control, a [controlled invariant subspace](/controlled-invariant-subspace/) is a linear subspace that some state feedback makes invariant. It is a special case of a control invariant set without constraints.
- **Barrier certificate.** A function whose sublevel set is positively invariant and separates the initial states from the unsafe states; see [barrier certificate](/barrier-certificate/).

## References
