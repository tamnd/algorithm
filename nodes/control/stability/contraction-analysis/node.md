---
tag: AM0BKV
kind: technique
slug: contraction-analysis
name: Contraction analysis
aliases:
- contraction theory
- incremental stability analysis
area: control/stability
level: research
summary: Shows that all solutions of a system converge to each other exponentially, by a uniform bound on the Jacobian in some metric, such as a negative matrix measure.
prereqs: [exponential-stability, matrix-norms]
see_also: [exponential-stability, lyapunov-function, matrix-norms, lyapunov-equation, banach-fixed-point-theorem, state-observer, high-gain-observer, strong-convexity]
sources:
  - paper: doi:10.1016/S0005-1098(98)00019-3
    title: "W. Lohmiller and J.-J. E. Slotine, On contraction analysis for non-linear systems, Automatica 34(6), 683-696, 1998"
    locator: the definition of a contraction region with a metric, the main convergence theorem, and the combination properties
  - paper: "B. P. Demidovich, Dissipativity of a nonlinear system of differential equations, Vestnik Moscow State University, Series Mathematics and Mechanics 6, 19-27, 1961 (in Russian)"
    locator: the sufficient condition with a constant positive definite matrix for the convergence of all solutions to one solution
  - paper: doi:10.1016/j.sysconle.2004.02.003
    title: "A. Pavlov, A. Pogromsky, N. van de Wouw and H. Nijmeijer, Convergent dynamics, a tribute to Boris Pavlovich Demidovich, Systems and Control Letters 52, 257-261, 2004"
    locator: the statement of Demidovich's condition and the notion of convergent systems
---

Contraction analysis proves that all solutions of a system forget their initial conditions: any two of them converge to each other exponentially. It does this with a bound on the Jacobian, not with a Lyapunov function for one equilibrium. If the symmetric part of the Jacobian, in a suitable metric, is uniformly negative definite, then the distance between any two solutions decays exponentially. The result is about pairs of solutions, so it applies without knowing where the solutions go: to systems with inputs, to time-varying systems, to the convergence to a periodic solution, and to observers, where the true state is one of the solutions. For an equilibrium of an autonomous system it gives global [exponential stability](/exponential-stability/) as a consequence. The idea is older than its name: Demidovich gave the condition with a constant metric in 1961, and Lohmiller and Slotine (1998) gave the general form with a state-dependent metric and the name.

## In plain words

Look at two solutions that start close to each other. Their difference moves by the Jacobian, the matrix of first derivatives of the system. If the Jacobian always pulls a small difference back toward zero, at a rate that does not depend on where the solutions are, then every small difference shrinks. A large difference is a chain of small ones along a path between the two states, so it shrinks too. One then knows that the system has at most one long-run behavior, without finding it first. The work is to find a way to measure distances, a metric, in which the pull back is visible; with the wrong ruler a contracting system can look as if it expands.

## When it applies

- The system is $\dot x = f(x, t)$ with $f$ continuously differentiable in $x$, on $\mathbb{R}^n$ or on a region that solutions do not leave. The time dependence can come from an input $u(t)$ that is known or not.
- One wants a property of all solutions together: a unique equilibrium that attracts everything, a unique periodic response to a periodic input, the decay of an observer error, or synchronization of copies of one system.
- A uniform bound on the Jacobian is available, or can be found, in a constant or state-dependent metric. Systems with several equilibria or with a [limit cycle](/limit-cycle/) are never contracting on a region that contains them, because two solutions that sit at different equilibria do not converge to each other.

## The template

1. **Write the differential dynamics.** For a virtual displacement $\delta x$ between neighboring solutions at a fixed time, $\dot{\delta x} = J(x, t)\, \delta x$ with $J = \partial f / \partial x$.
2. **Choose a metric.** Pick an invertible $\Theta(x, t)$ and set $M = \Theta^T \Theta$, uniformly positive definite: $\alpha_1 I \le M \le \alpha_2 I$. Start with $\Theta = I$; then try a diagonal scaling, a constant $P$ from the [Lyapunov equation](/lyapunov-equation/) of the linearization, and last a state-dependent $M(x)$, found for polynomial systems by [sum-of-squares programming](/sum-of-squares-programming/).
3. **Form the generalized Jacobian.** $F = (\dot \Theta + \Theta J) \Theta^{-1}$, where $\dot\Theta$ is the derivative along solutions.
4. **Bound it uniformly.** Find $\lambda > 0$ with
   $$\frac{F + F^T}{2} \le -\lambda I \quad \text{for all } x \text{ in the region and all } t \ge 0,$$
   which is the same as $\dot M + J^T M + M J \le -2\lambda M$. With $\Theta = I$ this is a bound on the matrix measure $\mu_2(J) = \lambda_{\max}\left((J + J^T)/2\right) \le -\lambda$. Other norms give other matrix measures, which are cheaper to bound, such as $\mu_\infty(J) = \max_i \left(J_{ii} + \sum_{j \ne i} |J_{ij}|\right)$.
5. **Check the region.** It must be forward invariant, and convex (for a constant metric) so that the straight segment between two states stays in it.
6. **Conclude.** For any two solutions in the region, the distance $d_M$ in the metric $M$ satisfies $d_M(x(t), y(t)) \le e^{-\lambda t} d_M(x(0), y(0))$, and in the Euclidean norm $|x(t) - y(t)| \le \sqrt{\alpha_2 / \alpha_1}\, e^{-\lambda t} |x(0) - y(0)|$ (Lohmiller and Slotine 1998).

**Why step 6 holds, for a constant metric.** With $\Theta$ constant and a convex region, let $e = x - y$ and $\tilde e = \Theta e$. By the mean value theorem in integral form,

$$f(x, t) - f(y, t) = \int_0^1 J(y + s e, t)\, ds\; e .$$

So $\frac{d}{dt} |\tilde e|^2 = 2 \tilde e^T \int_0^1 \Theta J(y + s e, t) \Theta^{-1} ds\; \tilde e \le -2\lambda |\tilde e|^2$, and $|\tilde e(t)| \le e^{-\lambda t} |\tilde e(0)|$. For a state-dependent metric the same bound holds for the length of a path between the two states, measured in $M$, and the distance is the length of the shortest path (Lohmiller and Slotine 1998).

**Demidovich's condition** is the case of a constant metric: if there are $P = P^T > 0$ and $Q = Q^T > 0$ with $J(x, t)^T P + P J(x, t) \le -Q$ for all $x$ and $t$, then all solutions converge to each other exponentially (Demidovich 1961; Pavlov et al. 2004).

## Classic examples

**A scalar system with an input.** $\dot x = -2x + \sin x + u(t)$. Here $J = -2 + \cos x \le -1$ for all $x$, so with $\Theta = 1$ the system is contracting with rate $\lambda = 1$ for every input $u$, and $|x(t) - y(t)| \le e^{-t} |x(0) - y(0)|$. With $u = \sin t$ and $x(0) = 5$, $y(0) = -5$ (classical Runge-Kutta, step $0.001$):

| $t$ | $\lvert x(t) - y(t) \rvert$ | bound $10 e^{-t}$ |
|---|---|---|
| 2 | $0.6146$ | $1.353$ |
| 5 | $2.193 \cdot 10^{-2}$ | $6.738 \cdot 10^{-2}$ |
| 10 | $7.809 \cdot 10^{-5}$ | $4.540 \cdot 10^{-4}$ |

**Entrainment by a periodic input.** If $u$ has period $T$ and the system is contracting on $\mathbb{R}^n$ with rate $\lambda$, the map that sends $x(0)$ to $x(T)$ is a contraction with factor $e^{-\lambda T}$ in the metric. By the [Banach fixed point theorem](/banach-fixed-point-theorem/) it has one fixed point, which is the initial state of the unique $T$-periodic solution, and every solution converges to it. In the scalar example with $u = \sin t$, iterating the period map gives the periodic solution with $x(0) = -0.47058$, which oscillates between $-0.68553$ and $0.68553$. The slope of the period map is $5.82 \cdot 10^{-4}$, below the bound $e^{-2\pi} = 1.867 \cdot 10^{-3}$.

**An autonomous system has one equilibrium.** If $\dot x = f(x)$ is contracting on $\mathbb{R}^n$ with a constant metric, then $z = \dot x$ satisfies $\dot z = J(x) z$, so $|\dot x(t)|$ decays exponentially. Then $x(t)$ has a limit $x^*$, $f(x^*) = 0$, and $x^*$ is the only equilibrium and is globally exponentially stable.

**Gradient flow of a strongly convex function.** For $\dot x = -\nabla V(x)$ with $V$ [strongly convex](/strong-convexity/) with modulus $m$, $J = -\nabla^2 V \le -m I$, so the flow is contracting with rate $m$ in the identity metric. All solutions converge to the unique minimizer. This is the continuous-time view of [gradient descent](/gradient-descent/).

**A cascade that needs a metric.** $\dot x_1 = -x_1 + 4 \tanh(x_2)$, $\dot x_2 = -x_2 + \cos t$. The Jacobian $J = \begin{bmatrix} -1 & 4\,\mathrm{sech}^2 x_2 \\ 0 & -1 \end{bmatrix}$ has the eigenvalues $-1, -1$, but at $x_2 = 0$ its symmetric part has the eigenvalue $-1 + 2 = 1 > 0$, so the identity metric fails. With $\Theta = \mathrm{diag}(1, 4)$, $F = \Theta J \Theta^{-1} = \begin{bmatrix} -1 & \mathrm{sech}^2 x_2 \\ 0 & -1 \end{bmatrix}$, whose symmetric part has eigenvalues $-1 \pm \tfrac12 \mathrm{sech}^2 x_2 \le -\tfrac12$. So the system is contracting with rate $\tfrac12$ in $M = \mathrm{diag}(1, 16)$. From $(3, 2)$ and $(-3, -2)$, the distance in $M$ is $0.4645$ at $t = 5$, $6.080 \cdot 10^{-3}$ at $t = 10$ and $5.360 \cdot 10^{-7}$ at $t = 20$, below the bound $d_M(0) e^{-t/2}$ with $d_M(0) = \sqrt{6^2 + 16 \cdot 4^2} = 17.09$. The true rate is close to $1$; the metric gives a bound, not the exact rate.

**Observers.** For $\dot x = f(x, t)$ with output $y = h(x)$, the observer $\dot{\hat x} = f(\hat x, t) + L (y - h(\hat x))$ is a system in $\hat x$ driven by $y(t)$. The true state $\hat x = x$ is one of its solutions. If the observer is contracting in $\hat x$, that is, if $\partial f / \partial x - L\, \partial h / \partial x$ satisfies step 4, every observer solution converges to the true state. This covers the [state observers](/state-observer/) of linear systems and nonlinear designs such as the [high-gain observer](/high-gain-observer/).

## Variations

- **Combinations.** A cascade of contracting systems is contracting, as in the example above. Two contracting systems in feedback with $J = \begin{bmatrix} J_1 & G \\ -G^T & J_2 \end{bmatrix}$ in the identity metric are contracting, because the skew-symmetric coupling cancels in $J + J^T$ (Lohmiller and Slotine 1998).
- **Partial contraction.** To show that solutions of one system converge to a particular set, build an auxiliary system that is contracting and that has both the actual solution and the target behavior as solutions. This is used for synchronization of identical coupled systems.
- **Non-Euclidean norms.** The matrix measures $\mu_1$ and $\mu_\infty$ of the [induced norms](/matrix-norms/) are bounded by sums of the entries, which is cheap and suits large networks with sparse coupling.
- **Discrete time.** For $x_{k+1} = f(x_k, k)$, the condition is $\|\Theta_{k+1} J_k \Theta_k^{-1}\| \le 1 - \beta$ with $\beta > 0$, and the map is a contraction in the usual sense of fixed point theory.
- **Searching for the metric.** For polynomial systems, the condition $\dot M + J^T M + M J \le -2\lambda M$ is a polynomial matrix inequality in $M$, and a polynomial $M(x)$ can be searched with sum-of-squares programming.
- **Weaker properties.** If the bound in step 4 holds with $\lambda = 0$, distances do not increase, but they need not decrease.

## Pitfalls

- **Eigenvalues of $J(x)$ are not enough.** A Hurwitz $J(x)$ at every $x$ does not give contraction, and not even convergence. The system $\dot x = -x + z (x + y z)^2$, $\dot y = -y - (x + y z)^2$, $\dot z = -z$ has a Jacobian whose eigenvalues are all $-1$ at every point, yet it has the unbounded solution $(x, y, z) = (18 e^{t}, -12 e^{2t}, e^{-t})$ (Cima, van den Essen, Gasull, Hubbers and Mañosas, 1997). Contraction needs a bound on the symmetric part in one metric that is uniform over the whole region.
- **A pointwise negative bound is not uniform.** For $\dot x = -x + \sin x$, $J = -1 + \cos x \le 0$ with equality at $x = 2\pi k$. The origin attracts every solution, but slowly: near it $\dot x \approx -x^3 / 6$, and from $x(0) = 1$ the state is $0.1711$ at $t = 100$ and $0.0547$ at $t = 1000$, close to $\sqrt{3/t}$. The bound must be $-\lambda$ with $\lambda > 0$, the same for all $x$ and $t$.
- **The region must be invariant.** A bound on a region that solutions can leave says nothing after they leave it. Local contraction near an equilibrium only gives the local result of the [indirect method](/lyapunov-indirect-method/).
- **A state-dependent metric adds a term.** With $M(x)$, the derivative $\dot M = \sum_i \frac{\partial M}{\partial x_i} \dot x_i$ along solutions belongs to the condition. Forgetting it is a common error.
- **The rate is in the metric.** The bound in the Euclidean norm carries the factor $\sqrt{\alpha_2 / \alpha_1}$ of the metric, which can be large, and the true rate can be faster than $\lambda$.

## Exercises

1. Show that $\dot x = -x + \tfrac12 \sin(x) + u(t)$ is contracting with rate $\tfrac12$ for every input $u$, and that two solutions with $|x(0) - y(0)| = 4$ are closer than $10^{-3}$ for $t \ge 2 \ln(4000) \approx 16.6$.
2. For the linear system $\dot x = A x$ with $A$ Hurwitz, take $M = P$ from $A^T P + P A = -I$. Find the contraction rate in terms of the largest eigenvalue of $P$.
3. Find the smallest $k > 0$ such that $\Theta = \mathrm{diag}(1, k)$ makes $J = \begin{bmatrix} -1 & 4 \\ 0 & -1 \end{bmatrix}$ contracting, and the rate for $k = 8$. (Answer: $k > 2$; rate $\tfrac34$.)
4. Show that a contracting autonomous system on $\mathbb{R}^n$ cannot have a periodic solution.
5. For $\dot x = -\nabla V(x) + u(t)$ with $V$ strongly convex with modulus $m$, show that two solutions with the same input converge to each other at rate $m$, for any input.

## References
