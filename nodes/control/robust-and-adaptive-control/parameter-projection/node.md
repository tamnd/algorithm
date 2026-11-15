---
tag: 5SVW7X
kind: technique
slug: parameter-projection
name: Parameter projection
aliases:
- projection operator for adaptive laws
area: control/robust-and-adaptive-control
level: advanced
summary: Projects the update of an adaptive law so that the estimates stay in a known convex set, which keeps them bounded.
prereqs: [model-reference-adaptive-control, convex-set, projected-gradient-descent]
see_also: [sigma-modification, rohrs-counterexample, l1-adaptive-control, certainty-equivalence, adaptive-pole-placement, lyapunov-function, persistent-excitation]
sources:
  - book: isbn:9780486498171
    title: "Petros A. Ioannou and Jing Sun, Robust Adaptive Control, Prentice Hall 1996 (Dover reprint 2012)"
    locator: "Section 4.4 (adaptive laws with projection: the projection operator for a convex set g(theta) <= 0 and its properties), Section 7.6.2 (projection that keeps the estimate in a stabilizable set) and Section 8.3.1 (the parameter drift example)"
  - paper: "Jean-Baptiste Pomet and Laurent Praly, Adaptive nonlinear regulation: estimation from the Lyapunov equation, IEEE Transactions on Automatic Control 37(6), 1992"
    locator: "pages 729 to 740 (a smooth projection operator that keeps the estimate in a slightly larger set and is Lipschitz)"
  - paper: "Bo Egardt, Stability of Adaptive Controllers, Lecture Notes in Control and Information Sciences 20, Springer 1979"
    locator: "the chapters on robustness (projection of the estimates into a bounded set as a remedy for bounded disturbances)"
---

Parameter projection is a modification of an adaptive law that keeps the parameter estimate inside a known closed convex set $S$ that contains the true parameter: when the estimate is on the boundary of $S$ and the update points outward, the outward part of the update is removed. The modified law keeps the Lyapunov property of the original law, because the removed part never increases the Lyapunov function, and it adds a bound on the estimate that holds even with disturbances and unmodeled dynamics. It also keeps the estimate in a region where a [certainty equivalence](/certainty-equivalence/) design exists, for example away from a zero gain. It is the continuous-time relative of [projected gradient descent](/projected-gradient-descent/), with the projection taken in the metric of the adaptation gain.

## In plain words

An adaptive controller learns some numbers while it runs. Noise or errors in the model can push these numbers far away from any sensible value, and then the controller can fail. Often you know in advance a range where the true numbers must be, for example a gain that is positive and not larger than 10. Projection is a fence around this range. Inside the range, learning goes on as before. At the fence, any push that would go outside is cut off, and only the part along the fence is kept. The numbers can never leave the range, and the cut never makes the learning worse with respect to the true values, because the true values are inside the fence too.

## When it applies

- The adaptive law has the gradient form $\dot\theta = \Gamma y$ with a symmetric positive definite gain $\Gamma$, and its analysis uses a Lyapunov function that contains $\tilde\theta^T\Gamma^{-1}\tilde\theta$ with $\tilde\theta = \theta - \theta^*$. This covers the laws of [MRAC](/model-reference-adaptive-control/), [L1 adaptive control](/l1-adaptive-control/) and gradient estimators.
- A closed convex set $S = \{\theta : g(\theta) \le 0\}$ with $\theta^* \in S$ is known, where $g$ is convex and continuously differentiable and $\nabla g \ne 0$ on the boundary.
- The initial estimate is in $S$.

## The template

Let $\theta \in S$ and let $y$ be the update direction of the original law. Ioannou and Sun (Section 4.4) define
$$\dot\theta = \begin{cases} \Gamma y & \text{if } g(\theta) < 0, \text{ or } g(\theta) = 0 \text{ and } (\Gamma y)^T\nabla g \le 0,\\[2pt] \Gamma y - \Gamma\dfrac{\nabla g\,\nabla g^T}{\nabla g^T\Gamma\nabla g}\Gamma y & \text{otherwise.}\end{cases}$$
In the second case $\nabla g^T\dot\theta = 0$: the update is tangent to the boundary.

**Property 1 (the estimate stays in the set).** If $\theta(0) \in S$, then $\theta(t) \in S$ for all $t$. Reason: on the boundary, $\frac{d}{dt}g(\theta) = \nabla g^T\dot\theta$, which is at most $0$ in the first case and exactly $0$ in the second, so $g$ cannot become positive.

**Property 2 (the Lyapunov function does not increase because of the projection).** Let $\theta^* \in S$. Then $\tilde\theta^T\Gamma^{-1}(\dot\theta - \Gamma y) \le 0$. Reason: the difference is zero in the first case. In the second, it equals $-\tilde\theta^T\nabla g\;\frac{\nabla g^T\Gamma y}{\nabla g^T\Gamma\nabla g}$, where $\nabla g^T\Gamma y > 0$. By convexity, $g(\theta^*) \ge g(\theta) + \nabla g(\theta)^T(\theta^* - \theta)$, and $g(\theta) = 0 \ge g(\theta^*)$, so $\tilde\theta^T\nabla g = (\theta - \theta^*)^T\nabla g \ge 0$. Hence the difference is at most $0$.

So if the original law gives $\dot V \le -W$ for $V = (\text{error terms}) + \tilde\theta^T\Gamma^{-1}\tilde\theta/2$, the projected law gives the same bound, and in addition $\theta$ is bounded by the size of $S$. Both properties are theorems.

**Discrete time.** For $\theta_{k+1} = \Pi_S(\theta_k + \Gamma y_k)$, where $\Pi_S$ is the projection onto $S$ in the norm $\|v\|_{\Gamma^{-1}}^2 = v^T\Gamma^{-1}v$, the projection is nonexpansive toward points of $S$: $\|\Pi_S(z) - \theta^*\|_{\Gamma^{-1}} \le \|z - \theta^*\|_{\Gamma^{-1}}$ for $\theta^* \in S$ (a theorem on projections onto closed [convex sets](/convex-set/)).

## Classic examples

**Parameter drift with a bounded disturbance.** Ioannou and Sun (Section 8.3.1) take $\dot x = ax + u + d$, $u = -kx$, $\dot k = \gamma x^2$ with $a = 1$, $\gamma = 1$, $x(0) = 1$, $k(0) = 5$ and the disturbance $d(t) = 5(1 + t)^{-1/5} - (1 + t)^{-2/5} - 0.4(1 + t)^{-7/5}$, which is bounded and goes to zero. The exact solution is $x = (1 + t)^{-2/5}$ and $k = 5(1 + t)^{1/5}$: the error goes to zero, but the gain grows without bound. With projection of $k$ onto $[0, 10]$, the gain reaches 10 at $t = 31$ ($5 \cdot 32^{1/5} = 10$) and stays there. A simulation with RK4 and the step 0.01 gives $k(1000) = 10$ and $x(1000) = 0.1325$, against $k(1000) = 19.91$ and $x(1000) = 0.0631$ without projection (measurements). The bounded gain costs a larger error while the disturbance lasts.

**A gain away from zero.** For a certainty equivalence law $u = -2y/\hat b$ with a known sign $b > 0$ and a known lower bound $b_0$, project $\hat b$ onto $[b_0, \infty)$, that is $g(\hat b) = b_0 - \hat b$. Then $u$ is always defined. The [adaptive pole placement](/adaptive-pole-placement/) page uses the same rule with $b_{\min} = 0.1$ for the leading coefficient of $\hat B$, which keeps the design equation solvable at the start.

**A ball.** For $|\theta| \le M$ with $\Gamma = \gamma I$, $g = \theta^T\theta - M^2$ and $\nabla g = 2\theta$. On the sphere $|\theta| = M$ with $\theta^Ty > 0$, the law becomes $\dot\theta = \gamma(y - \theta\theta^Ty/M^2)$, which removes the radial part.

**Smooth projection in L1 adaptive control.** The [L1 adaptive control](/l1-adaptive-control/) page uses $f(\theta) = (\theta^2 - \theta_b^2)/(\epsilon\theta_b^2)$ and scales the outward update by $1 - f$ in the band $0 < f \le 1$. The estimate stays in $|\theta| \le \theta_b\sqrt{1 + \epsilon}$ and the right-hand side is Lipschitz (Pomet and Praly 1992).

## Variations

- **Box constraints.** For a diagonal $\Gamma$ and the box $\theta_i \in [\ell_i, u_i]$, the template is the same as setting $\dot\theta_i = 0$ when $\theta_i$ is at a bound and its update points outward.
- **Smooth projection.** The update is reduced gradually in a thin band outside $S$, as in the L1 example; the vector field is then Lipschitz, which helps both the existence theory and simulation with a fixed step.
- **Projection in recursive least squares.** With the gain $P(t)$ in place of $\Gamma$, the projection uses the metric $P^{-1}$, so that the same Property 2 holds for $V = \tilde\theta^TP^{-1}\tilde\theta$.
- **Projection into a stabilizable set.** In indirect schemes, $S$ is chosen so that the estimated model has no common factor with a margin, as in Ioannou and Sun (Section 7.6.2).
- **Soft alternatives.** [Sigma modification](/sigma-modification/) and its switching version bound the estimate without a hard set, at the cost of a bias.

## Pitfalls

- **The set must contain the true parameter.** If $\theta^* \notin S$, Property 2 fails and the loop can have a persistent error. Choose $S$ from physics, with a margin.
- **Clipping is not projection for a nondiagonal gain.** Clipping each component of $\theta$ is the template only when $\Gamma$ is diagonal and $S$ is a box. With a nondiagonal $\Gamma$, clipping can increase $\tilde\theta^T\Gamma^{-1}\tilde\theta$.
- **Discontinuous right-hand side.** The hard projection switches on the boundary. Solutions exist in the sense of Filippov, but a simulation with a fixed step can chatter on the boundary; the smooth version avoids this.
- **No convergence of the parameters.** Projection gives bounds, not $\theta \to \theta^*$; that still needs [persistent excitation](/persistent-excitation/).
- **A large set gives a weak bound.** The bound on the estimate is the size of $S$. A set much larger than the true uncertainty allows large gains, which can still excite unmodeled dynamics, as in the [Rohrs counterexample](/rohrs-counterexample/).

## Exercises

1. Write the projected law for $S = \{|\theta| \le M\}$ and $\Gamma = \gamma I$, and show that $\frac{d}{dt}|\theta|^2 = 0$ when the projection is active.
2. Show that for a diagonal $\Gamma$ and a box, the template reduces to stopping each component that is at a bound and points outward.
3. In the drift example with $k \in [0, 10]$, find the time when $k$ reaches 10, and show that for later $t$, $x$ obeys $\dot x = -9x + d$, so $x$ stays bounded and goes to zero with $d$.
4. Find a $2 \times 2$ positive definite $\Gamma$, a point $\theta$ on the boundary of the box $[-1, 1]^2$ and a direction $y$ for which clipping each component increases $\tilde\theta^T\Gamma^{-1}\tilde\theta$ for some $\theta^*$ in the box.
5. Prove the discrete nonexpansive property from the variational inequality $(z - \Pi_S(z))^T\Gamma^{-1}(\theta^* - \Pi_S(z)) \le 0$ for $\theta^* \in S$.

## References
