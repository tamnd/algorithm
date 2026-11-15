---
tag: 9FMBFG
kind: theorem
slug: brockett-condition
name: Brockett's condition
aliases:
- Brockett's necessary condition for stabilization
area: control/nonlinear-control
level: advanced
summary: "If a C^1 feedback makes x = 0 locally asymptotically stable, f maps each neighborhood of (0, 0) onto a set that contains a neighborhood of 0 (Brockett 1983; continuous feedback: Zabczyk 1989)."
prereqs: [asymptotic-stability, control-affine-system, lie-algebra-rank-condition]
see_also: [lie-algebra-rank-condition, nonholonomic-constraint, unicycle-model, control-lyapunov-function, artstein-sontag-theorem, stabilizability, asymptotic-stability, lie-bracket]
sources:
  - paper: "R. W. Brockett, Asymptotic stability and feedback stabilization, in R. W. Brockett, R. S. Millman and H. J. Sussmann (eds.), Differential Geometric Control Theory, Progress in Mathematics 27, Birkhäuser, Boston, 181-191, 1983"
    title: Asymptotic stability and feedback stabilization
    locator: Theorem 1, condition (iii), and the example of the nonholonomic integrator
  - paper: doi:10.1007/BF01448189
    title: "J. Zabczyk, Some comments on stabilizability, Applied Mathematics and Optimization 19, 1-9, 1989"
    locator: the extension of the condition from C^1 feedback to continuous feedback, through the index of an asymptotically stable equilibrium
  - paper: doi:10.1007/BF01211563
    title: "J.-M. Coron, Global asymptotic stabilization for controllable systems without drift, Mathematics of Control, Signals, and Systems 5(3), 295-312, 1992"
    locator: smooth periodic time-varying feedback that stabilizes driftless systems which satisfy the accessibility rank condition
  - paper: "F. H. Clarke, Yu. S. Ledyaev, E. D. Sontag and A. I. Subbotin, Asymptotic controllability implies feedback stabilization, IEEE Transactions on Automatic Control 42(10), 1394-1407, 1997"
    title: Asymptotic controllability implies feedback stabilization
    locator: discontinuous feedback, with sampling solutions, for every asymptotically controllable system
  - paper: "J.-M. Coron, A necessary condition for feedback stabilization, Systems and Control Letters 14, 227-232, 1990"
    title: A necessary condition for feedback stabilization
    locator: a stronger necessary condition for continuous feedback
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, Deterministic Finite Dimensional Systems, second edition, Springer, 1998
    locator: Chapter 5 (Feedback and stabilization)
---

Brockett's condition is a necessary condition for a nonlinear system $\dot x = f(x, u)$ to be stabilizable at an equilibrium by a continuous state feedback $u = k(x)$ that does not depend on time. It says that the map $(x, u) \mapsto f(x, u)$ must reach every small velocity: the image of every neighborhood of the equilibrium must contain a neighborhood of $0$. The condition is easy to test, and it fails for many systems that are controllable, such as the nonholonomic integrator and the [unicycle](/unicycle-model/). So for these systems, [controllability](/controllability/), even proved by the [Lie algebra rank condition](/lie-algebra-rank-condition/), does not give a continuous stabilizing feedback. Brockett (1983) proved it for $C^1$ feedback. Zabczyk (1989) extended it to continuous feedback, with an argument on the index of the equilibrium. Time-varying feedback (Coron 1992) and discontinuous feedback (Clarke, Ledyaev, Sontag and Subbotin 1997) are not covered, and they are the usual ways around it.

## Statement

**Setting.** The system is $\dot x = f(x, u)$ with $x \in \mathbb{R}^n$ and $u \in \mathbb{R}^m$. The map $f$ is continuously differentiable ($C^1$) on a neighborhood of $(0, 0)$, and $f(0, 0) = 0$. A feedback $u = k(x)$ with $k(0) = 0$ gives the closed loop $\dot x = F(x)$ with $F(x) = f(x, k(x))$. If $k$ is $C^1$, $F$ is locally Lipschitz, and solutions exist and are unique by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/).

**Theorem (Brockett 1983, Theorem 1 (iii)).** Suppose there is a $C^1$ feedback $k$ with $k(0) = 0$ such that $x = 0$ is a locally [asymptotically stable](/asymptotic-stability/) equilibrium of $\dot x = f(x, k(x))$. Then for every neighborhood $N$ of $(0, 0)$ in $\mathbb{R}^n \times \mathbb{R}^m$, the set $f(N) = \{f(x, u) : (x, u) \in N\}$ contains a neighborhood of $0$ in $\mathbb{R}^n$.

**Extension (Zabczyk 1989).** The same conclusion holds for a continuous feedback $k$ for which the closed loop has unique solutions. The proof below uses only the continuity of the closed-loop flow, which is what this extension needs.

Brockett's Theorem 1 also has two other necessary conditions. Condition (i) says that the linearization has no uncontrollable mode with an eigenvalue that has a positive real part. Condition (ii) says that every state near $0$ can be steered to $0$ as $t \to \infty$. Condition (iii) is the one that is called Brockett's condition.

## In plain words

To hold a system at rest with a smooth rule, the rule must be able to correct small errors in every direction. Near the rest point, the system must be able to move in every direction, at least slowly, by some choice of state and input close to rest. If there is a direction in which no nearby state and input can make the system move, no smooth rule that looks only at the current state can work. A car is the standard case. It can move forward, backward and turn, but at any instant it cannot slide sideways. It can still park, by a sequence of moves, but no smooth fixed rule from position to steering brings it to rest at one spot from all nearby starts.

## Proof

The proof uses the topological degree $\deg(G, B, 0)$ of a continuous map $G$ on a closed ball $B$ with no zero on the boundary $\partial B$. Three properties are used: (D1) if $\deg(G, B, 0) \neq 0$, then $G$ has a zero in $B$; (D2) if $H(x, s)$ is continuous and has no zero for $x \in \partial B$, $s \in [0, 1]$, then $\deg(H(\cdot, 0), B, 0) = \deg(H(\cdot, 1), B, 0)$; (D3) $\deg(-\mathrm{id}, B, 0) = (-1)^n$.

Let $F(x) = f(x, k(x))$, and let $\Phi_t$ be the flow of $\dot x = F(x)$. It is continuous in $(t, x)$, because solutions are unique. Let $N$ be a neighborhood of $(0, 0)$. Choose a closed ball $B$ of radius $\rho > 0$ around $0$ such that: $(x, k(x)) \in N$ for $x \in B$ (possible because $k$ is continuous and $k(0) = 0$); $B$ is in the region of attraction; and $F$ has no zero in $B$ except $0$ (an asymptotically stable equilibrium is isolated). Solutions from $B$ stay bounded and converge to $0$ uniformly on the compact set $B$. So there is $T > 0$ with $|\Phi_T(x)| \le \rho / 2$ for all $x \in B$.

*Step 1.* For $x \in \partial B$ and $t \in (0, T]$, $\Phi_t(x) \neq x$. Otherwise $x$ would be periodic, $\Phi_{jt}(x) = x$ for all integers $j$, while $\Phi_{jt}(x) \to 0$, so $x = 0$, which is not on $\partial B$.

*Step 2.* Let $H(x, t) = (\Phi_t(x) - x)/t$ for $t \in (0, T]$ and $H(x, 0) = F(x)$. Since $\Phi_t(x) - x = \int_0^t F(\Phi_\tau(x))\, d\tau$, $H$ is continuous on $\partial B \times [0, T]$, and by Step 1 and the choice of $B$ it has no zero there. By (D2), $\deg(F, B, 0) = \deg(\Phi_T - \mathrm{id}, B, 0)$; the positive factor $1/T$ does not change the degree.

*Step 3.* The map $(x, s) \mapsto s \Phi_T(x) - x$ for $s \in [0, 1]$ has no zero on $\partial B$, because $|s \Phi_T(x)| \le \rho/2 < \rho = |x|$. By (D2) and (D3), $\deg(\Phi_T - \mathrm{id}, B, 0) = \deg(-\mathrm{id}, B, 0) = (-1)^n$.

*Step 4.* Let $\mu = \min_{x \in \partial B} |F(x)| > 0$. For $|\xi| < \mu$, the map $(x, s) \mapsto F(x) - s \xi$ has no zero on $\partial B$. By (D2), $\deg(F - \xi, B, 0) = \deg(F, B, 0) = (-1)^n \neq 0$. By (D1), there is $x \in B$ with $f(x, k(x)) = \xi$, and $(x, k(x)) \in N$. So $f(N)$ contains the ball of radius $\mu$ around $0$. $\blacksquare$

The number $(-1)^n$ is the index of an asymptotically stable equilibrium. Steps 1 to 3 compute it with the flow, which is Zabczyk's route; the smoothness of $k$ is used only to make the flow continuous.

## Consequences

- **The nonholonomic integrator.** For $\dot x_1 = u_1$, $\dot x_2 = u_2$, $\dot x_3 = x_1 u_2 - x_2 u_1$, the point $(0, 0, \varepsilon)$ with $\varepsilon \neq 0$ is not in $f(N)$ for any $N$: the first two components force $u_1 = u_2 = 0$, and then the third is $0$. So no continuous feedback with unique solutions makes $0$ asymptotically stable. Yet the system is controllable: $[g_1, g_2] = (0, 0, 2)$, so the [Lie algebra rank condition](/lie-algebra-rank-condition/) holds everywhere, and the theorem of Chow and Rashevsky applies. Brockett (1983) used this example.
- **The unicycle.** For $\dot p_1 = v \cos\theta$, $\dot p_2 = v \sin\theta$, $\dot\theta = \omega$, take $N$ with $|\theta| < \pi/2$. To get $f = (0, \varepsilon, 0)$ one needs $\omega = 0$ and $v \cos\theta = 0$, so $v = 0$, and then $v \sin\theta = 0 \neq \varepsilon$. So a [unicycle](/unicycle-model/) or car with a [nonholonomic constraint](/nonholonomic-constraint/) cannot be stabilized at a pose by continuous time-invariant feedback.
- **Driftless systems in general.** For $\dot x = \sum_{i=1}^m g_i(x) u_i$ with $m < n$ and $g_1(0), \dots, g_m(0)$ independent, the image of a small neighborhood lies in the ranges of $G(x) = [g_1(x), \dots, g_m(x)]$ for $x$ near $0$. These $m$-dimensional subspaces are close to the range of $G(0)$, so a vector orthogonal to that range is not in the image. No continuous feedback with unique solutions stabilizes such a system.
- **Linear systems.** For $f(x, u) = A x + B u$, the image of any neighborhood contains a neighborhood of $0$ if and only if $\operatorname{rank} [A \;\, B] = n$. This is weaker than [stabilizability](/stabilizability/), which asks that $\operatorname{rank} [A - \lambda I \;\, B] = n$ for every eigenvalue $\lambda$ with $\operatorname{Re} \lambda \ge 0$; the condition here is the case $\lambda = 0$.
- **Control Lyapunov functions.** By the [Artstein-Sontag theorem](/artstein-sontag-theorem/), a smooth [control Lyapunov function](/control-lyapunov-function/) for a control-affine system gives a feedback that is smooth away from $0$; with the small control property, the feedback is continuous at $0$ too. So the nonholonomic integrator has no smooth control Lyapunov function with the small control property.

## Tightness

- **The condition is not sufficient.** For $\dot x_1 = u$, $\dot x_2 = x_2$, $f(x, u) = (u, x_2)$, and every small vector $(a, b)$ equals $f$ at $x = (0, b)$, $u = a$. So the condition holds. But $x_2(t) = e^t x_2(0)$ for every input, so no feedback stabilizes the origin. Brockett's condition (i) detects this case: the mode $x_2$ is uncontrollable with eigenvalue $1$.
- **Time-varying feedback escapes it.** Coron (1992) showed that driftless systems that satisfy the accessibility rank condition, such as the nonholonomic integrator, can be stabilized globally by smooth feedback $u = k(t, x)$ that is periodic in $t$.
- **Discontinuous feedback escapes it.** Clarke, Ledyaev, Sontag and Subbotin (1997) showed that every asymptotically controllable system can be stabilized by a discontinuous feedback, with solutions defined by sampling.
- **Continuity alone.** The proof above needs unique solutions, so that the flow is continuous. Without uniqueness, other arguments are necessary, and the exact hypotheses differ from paper to paper. Coron (1990) gave a stronger necessary condition for continuous feedback.

## History

Brockett presented the condition in 1983, in a volume on differential geometric control theory, as part of Theorem 1, and used the nonholonomic integrator to show that controllable systems may not be stabilizable by smooth feedback. Zabczyk (1989) gave the proof through the index of an asymptotically stable equilibrium, which works for continuous feedback with unique solutions. Coron (1990) found a stronger necessary condition. The obstruction led to the study of time-varying feedback for driftless systems, with Coron's 1992 result, and of discontinuous feedback, with Clarke, Ledyaev, Sontag and Subbotin (1997).

## References
