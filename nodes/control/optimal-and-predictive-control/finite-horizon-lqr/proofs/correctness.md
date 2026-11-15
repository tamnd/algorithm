---
title: The backward Riccati recursion gives the optimal feedback and the optimal cost of the finite-horizon LQ problem
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $Q = Q^T \ge 0$, $Q_f = Q_f^T \ge 0$, $R = R^T > 0$ and $N \ge 0$. The plant is $x_{k+1} = A x_k + B u_k$. For $0 \le k \le N$ and a state $x$, let $V_k(x)$ be the infimum of

$$J_k(x; u_k, \dots, u_{N-1}) = \sum_{j=k}^{N-1} \left( x_j^T Q x_j + u_j^T R u_j \right) + x_N^T Q_f x_N, \qquad x_k = x,$$

over all input sequences. The algorithm sets $P_N = Q_f$ and, for $k = N - 1, \dots, 0$,

$$S_k = R + B^T P_{k+1} B, \qquad K_k = S_k^{-1} B^T P_{k+1} A, \qquad P_k = Q + A^T P_{k+1} A - A^T P_{k+1} B K_k.$$

## Lemma 1: completing the square

Let $S = S^T > 0$ be $m \times m$, let $g \in \mathbb{R}^m$ and $c \in \mathbb{R}$. Then $f(u) = u^T S u + 2 u^T g + c$ has the unique minimizer $u^* = -S^{-1} g$, and $f(u) = f(u^*) + (u - u^*)^T S (u - u^*)$ with $f(u^*) = c - g^T S^{-1} g$.

*Proof.* Expand $(u - u^*)^T S (u - u^*) = u^T S u + 2 u^T g + g^T S^{-1} g$, using $S u^* = -g$ and the symmetry of $S$. So $f(u) - (u - u^*)^T S (u - u^*) = c - g^T S^{-1} g$, a constant. The term $(u - u^*)^T S (u - u^*)$ is positive for $u \ne u^*$ because $S > 0$. $\square$

## Lemma 2: the algebra of one step

Let $P = P^T \ge 0$, $S = R + B^T P B$, $K = S^{-1} B^T P A$ and $P' = Q + A^T P A - A^T P B K$. Then $S > 0$, $P'$ is symmetric, and

$$P' = Q + K^T R K + (A - B K)^T P (A - B K) \ge 0.$$

*Proof.* For $v \ne 0$, $v^T S v = v^T R v + (B v)^T P (B v) \ge v^T R v > 0$. So $S$ is positive definite and invertible. Expand the right side:

$$(A - BK)^T P (A - BK) + K^T R K = A^T P A - A^T P B K - K^T B^T P A + K^T S K.$$

Since $S K = B^T P A$, we have $K^T S K = K^T B^T P A$, so the last two terms cancel and the right side equals $Q + A^T P A - A^T P B K = P'$. The right side is a sum of symmetric matrices, and each of $Q$, $K^T R K$ and $(A - BK)^T P (A - BK)$ is positive semidefinite. So $P'$ is symmetric and $P' \ge 0$. $\square$

## Theorem

For every $k$ and $x$, $V_k(x) = x^T P_k x$. The minimum is attained, and an input sequence is optimal from $(k, x)$ if and only if $u_j = -K_j x_j$ for $j = k, \dots, N - 1$ along the trajectory it produces. All $P_k$ are symmetric and positive semidefinite.

*Proof.* By induction on $k$ downward. For $k = N$ there is no input and $V_N(x) = x^T Q_f x = x^T P_N x$, and $P_N = Q_f$ is symmetric and positive semidefinite.

Let $k < N$ and assume the claim for $k + 1$. Fix $x$ and any inputs $u_k, \dots, u_{N-1}$. Split the cost as

$$J_k(x; u_k, \dots) = x^T Q x + u_k^T R u_k + J_{k+1}(A x + B u_k; u_{k+1}, \dots).$$

By the induction hypothesis, $J_{k+1}(y; \dots) \ge y^T P_{k+1} y$ for $y = A x + B u_k$, with equality if and only if $u_{k+1}, \dots$ follow the feedback from step $k + 1$. So

$$J_k \ge x^T Q x + u_k^T R u_k + (A x + B u_k)^T P_{k+1} (A x + B u_k) = u_k^T S_k u_k + 2 u_k^T B^T P_{k+1} A x + x^T (Q + A^T P_{k+1} A) x.$$

This is $f(u_k)$ of Lemma 1 with $S = S_k$, $g = B^T P_{k+1} A x$ and $c = x^T (Q + A^T P_{k+1} A) x$; Lemma 2 gives $S_k > 0$. Lemma 1 gives $f(u_k) \ge f(-K_k x)$ with equality if and only if $u_k = -K_k x$, and

$$f(-K_k x) = x^T (Q + A^T P_{k+1} A) x - x^T A^T P_{k+1} B S_k^{-1} B^T P_{k+1} A x = x^T P_k x.$$

So $J_k \ge x^T P_k x$ for every input sequence. Equality holds if and only if $u_k = -K_k x$ and the later inputs are optimal from $(k + 1, A x + B u_k)$, which by the induction hypothesis means that they follow the feedback. This choice exists, so $V_k(x) = x^T P_k x$ and the minimum is attained. Lemma 2 with $P = P_{k+1}$ gives that $P_k$ is symmetric and $P_k \ge 0$. $\blacksquare$

This is the [principle of optimality](/principle-of-optimality/) for this problem: the tail of an optimal sequence is optimal for the tail problem, and $V_k$ satisfies the [Bellman equation](/bellman-equation/) $V_k(x) = \min_u \left( x^T Q x + u^T R u + V_{k+1}(A x + B u) \right)$.

**Exact arithmetic.** Each step uses only sums, products and one linear solve with the matrix $S_k$, which is invertible by Lemma 2. So with rational data every $P_k$ and $K_k$ is rational, and the implementation computes them exactly in Fraction.

## Continuous time

Let $Q$, $Q_f$, $R$ be as above and $T > 0$. Consider $\dot x = A x + B u$ on $[0, T]$ with a measurable, square integrable input $u$, and the cost $J = \int_0^T (x^T Q x + u^T R u)\, dt + x(T)^T Q_f x(T)$. Let $G = B R^{-1} B^T$.

**Lemma 3: the Riccati differential equation has a solution on all of $[0, T]$.** The equation $-\dot P = A^T P + P A - P G P + Q$, $P(T) = Q_f$, has a unique solution on $[0, T]$, and $0 \le P(t) \le \Pi(t)$, where $\Pi$ solves the linear equation $-\dot \Pi = A^T \Pi + \Pi A + Q$, $\Pi(T) = Q_f$.

*Proof.* The right side is a polynomial in the entries of $P$, so it is locally Lipschitz, and a unique solution exists on a maximal interval $(t_*, T]$. If $t_* \ge 0$, the solution must be unbounded as $t \downarrow t_*$. We show that it stays between $0$ and $\Pi$, which is bounded on $[0, T]$, so $t_* < 0$. On $(t_*, T]$, the identity of Lemma 4 below holds for every input, because its proof uses only the equation on the interval $[t, T]$. Taking any $s \in (t_*, T]$ and starting the plant at time $s$ from $x$, it gives $x^T P(s) x = J_s(x, u) - \int_s^T (u + K x)^T R (u + K x)\, dt$ for every input. With the feedback $u = -K x$, which gives a linear equation with continuous coefficients and so a solution on $[s, T]$, the integral vanishes and $x^T P(s) x$ is a cost, hence at least 0. With the input $u = 0$, $x^T P(s) x \le J_s(x, 0) = x^T \Pi(s) x$, where the last equality holds because, for $u = 0$, $\frac{d}{dt}(x^T \Pi x) = x^T (\dot \Pi + A^T \Pi + \Pi A) x = -x^T Q x$, and the integral of this from $s$ to $T$ gives $x(T)^T Q_f x(T) - x^T \Pi(s) x = -\int_s^T x^T Q x\, dt$. Both bounds hold for every $x$, so $0 \le P(s) \le \Pi(s)$. $\square$

**Lemma 4: the cost identity.** Let $K(t) = R^{-1} B^T P(t)$. For every input $u$ and every trajectory,

$$J = x(0)^T P(0) x(0) + \int_0^T (u + K x)^T R (u + K x)\, dt.$$

*Proof.* Along a trajectory, using the symmetry of $P$,

$$\frac{d}{dt} \left( x^T P x \right) = x^T \dot P x + 2 x^T P (A x + B u) = x^T (\dot P + A^T P + P A) x + 2 x^T P B u = x^T (P G P - Q) x + 2 x^T P B u.$$

Now $(u + K x)^T R (u + K x) = u^T R u + 2 x^T P B u + x^T P G P x$, because $K^T R K = P B R^{-1} B^T P = P G P$ and $x^T K^T R u = x^T P B u$. So

$$\frac{d}{dt} \left( x^T P x \right) = -x^T Q x - u^T R u + (u + K x)^T R (u + K x).$$

Integrate from 0 to $T$ and use $P(T) = Q_f$:

$$x(T)^T Q_f x(T) - x(0)^T P(0) x(0) = -\int_0^T (x^T Q x + u^T R u)\, dt + \int_0^T (u + K x)^T R (u + K x)\, dt.$$

Rearranging gives the identity. $\square$

**Theorem (continuous time).** The minimum of $J$ from $x(0) = x_0$ is $x_0^T P(0) x_0$. It is attained by the feedback $u(t) = -K(t) x(t)$, and every optimal input equals $-K(t) x(t)$ for almost every $t$.

*Proof.* By Lemma 4, $J \ge x_0^T P(0) x_0$, because $R > 0$ makes the integral nonnegative. The feedback makes the integral 0. If the integral is 0 for some input, then $u + K x = 0$ almost everywhere, again because $R > 0$. $\square$

**The numerical method.** The implementation integrates the equation in $\tau = T - t$, where it reads $dP / d\tau = A^T P + P A - P G P + Q$, with the classical RK4 method and a fixed step $h$. RK4 has global error $O(h^4)$ on a bounded interval for a smooth right side, and Lemma 3 shows that the exact solution stays in a bounded set, so for $h$ small enough the computed $P$ is within $O(h^4)$ of $P(t)$ at the grid points. The tests compare it with the scalar closed form within $10^{-9}$. This part is a property of the integrator, not of the LQ problem.
