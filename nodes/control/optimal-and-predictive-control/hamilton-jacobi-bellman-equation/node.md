---
tag: H499AQ
kind: theorem
slug: hamilton-jacobi-bellman-equation
name: Hamilton-Jacobi-Bellman equation
aliases:
- HJB equation
area: control/optimal-and-predictive-control
level: core
summary: The optimal cost-to-go of a continuous-time problem solves a partial differential equation, and its minimizer gives an optimal feedback.
prereqs: [optimal-control-problem, principle-of-optimality, bellman-equation]
see_also: [pontryagin-maximum-principle, costate, control-hamiltonian, lqr-problem, value-iteration, hamilton-jacobi-reachability, time-optimal-control, finite-horizon-lqr]
sources:
  - book: isbn:9780486428093
    title: Richard Bellman, Dynamic Programming, Princeton University Press, 1957 (Dover reprint, 2003)
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 5.1.3 (the HJB equation), Section 5.1.4 (the sufficient condition), Section 5.2 (the HJB equation and the maximum principle, with a value function that is not differentiable) and Section 5.3 (viscosity solutions)
  - paper: doi:10.1090/S0002-9947-1983-0690039-8
    title: Michael G. Crandall and Pierre-Louis Lions, Viscosity solutions of Hamilton-Jacobi equations, Transactions of the American Mathematical Society 277(1), 1-42, 1983
  - book: isbn:9780387260457
    title: Wendell H. Fleming and H. Mete Soner, Controlled Markov Processes and Viscosity Solutions, second edition, Springer, 2006
    locator: the chapters on deterministic optimal control and on viscosity solutions
  - url: https://math.berkeley.edu/~evans/control.course.pdf
    title: Lawrence C. Evans, An Introduction to Mathematical Optimal Control Theory, lecture notes, University of California, Berkeley
    locator: Chapter 5 (dynamic programming)
---

The Hamilton-Jacobi-Bellman (HJB) equation is the partial differential equation

$$-V_t(t, x) = \min_{u \in U} \left( L(x, u) + V_x(t, x)\, f(x, u) \right), \qquad V(T, x) = K(x),$$

for the value function $V(t, x)$ of an [optimal control problem](/optimal-control-problem/), the smallest cost that can still be reached from state $x$ at time $t$. It is the continuous-time form of the [Bellman equation](/bellman-equation/) and follows from the [principle of optimality](/principle-of-optimality/). This page proves two statements: a $C^1$ solution of the equation is the value function and gives an optimal feedback (the verification theorem), and a value function that is $C^1$ solves the equation. In general the value function is not differentiable, and then it is the unique viscosity solution; that statement is cited, not proved.

## Statement

**Setting.** A horizon $T > 0$, a compact input set $U \subset \mathbb{R}^m$, and continuous functions $f : \mathbb{R}^n \times U \to \mathbb{R}^n$, $L : \mathbb{R}^n \times U \to \mathbb{R}$ and $K : \mathbb{R}^n \to \mathbb{R}$. $f$ is bounded and satisfies a [Lipschitz condition](/lipschitz-condition/) in $x$ uniformly in $u$, so each piecewise continuous input $u : [t, T] \to U$ gives a unique trajectory from any $(t, x)$ ([Picard-Lindelöf theorem](/picard-lindelof-theorem/)). The cost and the value function are

$$J(t, x; u) = \int_t^T L(x(s), u(s))\, ds + K(x(T)), \qquad V(t, x) = \inf_u J(t, x; u).$$

**Theorem.**

1. **Verification.** Let $W \in C^1([0, T] \times \mathbb{R}^n)$ satisfy $-W_t(t, x) = \min_{u \in U} \left( L(x, u) + W_x(t, x) f(x, u) \right)$ for all $(t, x)$, and $W(T, x) = K(x)$. Then $W(t, x) \le J(t, x; u)$ for every admissible $u$, so $W \le V$. If, from $(t, x)$, an admissible input $u^*$ attains the minimum at $(s, x^*(s))$ for every $s$ except finitely many, then $u^*$ is optimal and $W(t, x) = V(t, x)$.
2. **Necessity.** If $V$ is $C^1$ on an open set $\Omega \subseteq (0, T) \times \mathbb{R}^n$, then $V$ satisfies the HJB equation at every point of $\Omega$.
3. **Viscosity solutions** (cited). If in addition $L$ and $K$ are bounded and uniformly continuous and $L$ is Lipschitz in $x$, then $V$ is bounded and uniformly continuous, and it is the unique such viscosity solution of

$$-V_t + \max_{u \in U} \left( -L(x, u) - V_x f(x, u) \right) = 0, \qquad V(T, \cdot) = K$$

(Crandall and Lions 1983; Fleming and Soner 2006). The equation is the HJB equation multiplied by $-1$ inside the maximum. The order matters: a viscosity solution of $F = 0$ need not be one of $-F = 0$.

## In plain words

Suppose you knew, for every place and every moment, the least cost you could still achieve from there. Then the best move now is easy to find: pick the move that minimizes the cost of this short step plus the least cost from where the step takes you. Writing this for steps of length tending to zero gives one equation for the table of least costs. If you can solve the equation, you can check that a plan is optimal and you get the best action as a function of the current state, a feedback. The catch is that the table often has kinks, and then the equation only holds in a weaker sense.

## Proof

**Part 1.** Let $u$ be admissible from $(t, x)$ and $x(s)$ its trajectory. The function $s \mapsto W(s, x(s))$ is continuous and piecewise $C^1$, with

$$\frac{d}{ds} W(s, x(s)) = W_t + W_x f(x(s), u(s)) \ge -L(x(s), u(s)),$$

because the equation says $-W_t \le L(x, v) + W_x f(x, v)$ for every $v \in U$. Integrate from $t$ to $T$ and use $W(T, \cdot) = K$:

$$K(x(T)) - W(t, x) \ge -\int_t^T L\, ds, \qquad \text{so} \qquad W(t, x) \le J(t, x; u).$$

For $u^*$ the inequality is an equality at all but finitely many $s$, so $W(t, x) = J(t, x; u^*)$. Since $J(t, x; u^*) \ge V(t, x) \ge W(t, x)$, all three are equal, and $u^*$ is optimal.

**Part 2, the inequality $\le$.** Fix $(t, x) \in \Omega$, a value $v \in U$ and a small $h > 0$. Use $v$ on $[t, t + h]$ and then any input from $(t + h, x(t + h))$. Taking the infimum over the second part (the [principle of optimality](/principle-of-optimality/)),

$$V(t, x) \le \int_t^{t+h} L(x(s), v)\, ds + V(t + h, x(t + h)).$$

Subtract $V(t, x)$, divide by $h$ and let $h \to 0$. Since $V$ is $C^1$ near $(t, x)$, the limit is $0 \le L(x, v) + V_t(t, x) + V_x(t, x) f(x, v)$. This holds for every $v$, so $-V_t \le \min_v (L + V_x f)$.

**Part 2, the inequality $\ge$.** For each small $h > 0$ take an input $u_h$ with $J(t, x; u_h) \le V(t, x) + h^2$. Its tail from $t + h$ costs at least $V(t + h, x_h(t + h))$, so

$$\int_t^{t+h} L(x_h, u_h)\, ds + V(t + h, x_h(t + h)) - V(t, x) \le h^2.$$

Write the difference of $V$ as $\int_t^{t+h} (V_t + V_x f)(s, x_h(s), u_h(s))\, ds$ and divide by $h$:

$$\frac1h \int_t^{t+h} \left( L + V_t + V_x f \right)(s, x_h(s), u_h(s))\, ds \le h.$$

Because $f$ is bounded, $|x_h(s) - x| \le C h$ on the interval. $V_t$ and $V_x$ are continuous, and $L$ and $f$ are uniformly continuous on compact sets, so the integrand differs from $L(x, u_h(s)) + V_t(t, x) + V_x(t, x) f(x, u_h(s))$ by at most $\omega(h)$ with $\omega(h) \to 0$. That expression is at least $\min_v (L(x, v) + V_t + V_x f(x, v))$. Hence $\min_v(\dots) \le h + \omega(h)$, and letting $h \to 0$ gives $-V_t \ge \min_v (L + V_x f)$. $\blacksquare$

## Consequences

**A worked example.** For $\dot x = u$, $U = \mathbb{R}$ (the problem is still fine without compactness here), $L = u^2$ and $K = x^2$, try $V = p(t) x^2$. Then $\min_u (u^2 + 2 p x u) = -p^2 x^2$ at $u = -p x$, and the equation becomes $-\dot p\, x^2 = -p^2 x^2$, so $\dot p = p^2$ with $p(T) = 1$. The solution is $p(t) = 1/(1 + T - t)$, and

$$V(t, x) = \frac{x^2}{1 + T - t}, \qquad u^*(t, x) = -\frac{x}{1 + T - t}.$$

Check: $V_t = x^2/(1 + T - t)^2$ and $\min_u (u^2 + V_x u) = -V_x^2/4 = -x^2/(1 + T - t)^2$, so $-V_t$ equals the minimum. From $x_0$ the feedback gives the constant input $-x_0/(1 + T)$ and the cost $x_0^2/(1 + T)$. For $x_0 = 1$, $T = 1$ this is the cost $1/2$ found on the [optimal control problem](/optimal-control-problem/) page.

- **Feedback.** The minimizer $u^*(t, x)$ in the equation is an optimal feedback for all initial states at once, not only an open-loop input from one start.
- **LQR.** For $\dot x = A x + B u$, $L = x^T Q x + u^T R u$ and $K = x^T Q_f x$, the guess $V = x^T P(t) x$ gives $u^* = -R^{-1} B^T P x$ and the Riccati differential equation $-\dot P = A^T P + P A - P B R^{-1} B^T P + Q$, $P(T) = Q_f$ ([finite-horizon LQR](/finite-horizon-lqr/)). By Part 1 this feedback is optimal.
- **The costate.** Where $V$ is $C^2$, $\lambda(t) = V_x(t, x^*(t))^T$ is a [costate](/costate/) of the [maximum principle](/pontryagin-maximum-principle/), and the right side of the equation is the minimized [Hamiltonian](/control-hamiltonian/) $h(x, V_x^T)$. The characteristics of the HJB equation are the extremals of the maximum principle.
- **Infinite horizon.** For $T = \infty$ and data that do not depend on time, $V(x)$ solves the stationary equation $0 = \min_u (L + V_x f)$, under conditions that make the cost finite.
- **Discrete time and computation.** The discrete form $V_k(x) = \min_u (L(x, u) + V_{k+1}(F(x, u)))$ is the [Bellman equation](/bellman-equation/), solved backward or by [value iteration](/value-iteration/). On a grid with $N$ points per axis, one sweep touches $N^n$ points, so the cost grows exponentially with the state dimension $n$. The same equations, with a target set instead of a cost, compute reachable sets ([Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/)).

## Tightness

**The value function is often not differentiable.** Take $\dot x = u$, $U = [-1, 1]$, on the interval $(-1, 1)$, and let $V(x)$ be the least time to reach the set $\{-1, 1\}$. Then $V(x) = 1 - |x|$, which has a kink at $x = 0$. The stationary equation with $L = 1$ is $\min_u (1 + V' u) = 1 - |V'| = 0$. Both $1 - |x|$ and $|x| - 1$ satisfy $|V'| = 1$ at every $x \ne 0$ and the boundary values, and so do many zigzag functions, so "solution almost everywhere" does not determine $V$. In the form of Part 3, $\max_u(-1 - V' u) = |V'| - 1 = 0$. At the kink of $1 - |x|$, every smooth function that touches it from above has a slope $p \in [-1, 1]$ there, and $|p| - 1 \le 0$, so the subsolution test holds; no smooth function touches it from below, so the supersolution test is empty. So $1 - |x|$ is a viscosity solution. For $|x| - 1$, the function $\varphi = -1$ touches it from below at 0 with slope 0, and $|0| - 1 \ge 0$ fails, so it is not one. The [time-optimal](/time-optimal-control/) double integrator has a value function that is not differentiable on its switching curve, for the same reason.

**The value function can be discontinuous or infinite.** Without controllability, some states cannot reach the target, and the minimum time is $+\infty$ there. Part 3 needs its hypotheses.

**A $C^1$ solution need not exist.** Part 1 is a sufficient condition. It applies only when a $C^1$ solution is known, as for the LQR problem.

## History

Hamilton and Jacobi wrote the equation of the calculus of variations that carries their names in the 1830s, and Carathéodory used it as a sufficient condition in the 1930s. Bellman developed dynamic programming at RAND in the early 1950s and wrote the equation for control problems; his book appeared in 1957. Kalman used it for the linear quadratic problem around 1960. The question of nonsmooth value functions stayed open until Crandall and Lions (1983) defined viscosity solutions and proved uniqueness. Fleming and Soner (2006) give the theory for deterministic and stochastic control.

## References
