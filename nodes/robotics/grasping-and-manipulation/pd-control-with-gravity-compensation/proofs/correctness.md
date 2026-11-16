---
title: PD control with gravity compensation makes the set point globally asymptotically stable
proves: [correctness]
status: full
---

The arm obeys $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$ with $q \in \mathbb{R}^n$. We assume:

1. $M(q)$ is symmetric, and there is a constant $\mu > 0$ with $x^T M(q) x \ge \mu\, x^T x$ for all $q$ and $x$.
2. $M$, $C$ and $g$ are continuously differentiable, and $C$ satisfies $\dot q^T(\dot M(q) - 2C(q, \dot q))\dot q = 0$ for all $q$, $\dot q$, where $\dot M = \frac{d}{dt}M(q(t))$.
3. The gravity model is exact: $\hat g = g$.
4. $K_p$ and $K_d$ are symmetric positive definite, and $q_d$ is constant.

Assumption 2 holds for every factorization $C\dot q$ of the Coriolis and centripetal torques, because the quadratic form only sees the product $C\dot q$, and for the Christoffel choice the matrix $\dot M - 2C$ is skew-symmetric.

**Closed loop.** Lines L1 and L2 give $\tau = K_p e - K_d \dot q + g(q)$ with $e = q_d - q$. The gravity terms cancel, and the state $x = (e, \dot q)$ obeys

$$\dot e = -\dot q, \qquad M(q)\ddot q = K_p e - K_d \dot q - C(q, \dot q)\dot q.$$

Because $q = q_d - e$, the right side depends only on $x$, so the closed loop is an autonomous system $\dot x = f(x)$ on $\mathbb{R}^{2n}$ with a continuously differentiable $f$. Its equilibria have $\dot q = 0$, so $\ddot q = 0$ and $K_p e = 0$, so $e = 0$. The only equilibrium is $x = 0$.

**Lemma 1.** The function $V(x) = \tfrac12 \dot q^T M(q)\dot q + \tfrac12 e^T K_p e$ is positive definite and radially unbounded, and $\dot V = -\dot q^T K_d \dot q$ along the closed loop.

*Proof.* Let $k > 0$ be the smallest eigenvalue of $K_p$. By assumption 1, $V(x) \ge \tfrac12 \mu \|\dot q\|^2 + \tfrac12 k \|e\|^2$, which is positive for $x \ne 0$ and tends to infinity as $\|x\| \to \infty$. Also $V(0) = 0$. For the derivative, $M$ is symmetric, so

$$\dot V = \dot q^T M \ddot q + \tfrac12 \dot q^T \dot M \dot q + e^T K_p \dot e.$$

We put in $M\ddot q$ from the closed loop and $\dot e = -\dot q$:

$$\dot V = \dot q^T K_p e - \dot q^T K_d \dot q - \dot q^T C \dot q + \tfrac12 \dot q^T \dot M \dot q - e^T K_p \dot q.$$

The first and last terms cancel because $K_p$ is symmetric, and the middle terms give $\tfrac12 \dot q^T(\dot M - 2C)\dot q = 0$ by assumption 2. So $\dot V = -\dot q^T K_d \dot q$. $\square$

**Theorem.** Under assumptions 1 to 4, $x = 0$ is a globally asymptotically stable equilibrium of the closed loop: every solution tends to $q = q_d$, $\dot q = 0$.

*Proof.* By Lemma 1, $\dot V \le 0$, so $V(x(t)) \le V(x(0))$. The sublevel set $\Omega = \{x : V(x) \le V(x(0))\}$ is closed, and it is bounded because $V$ is radially unbounded. So $\Omega$ is compact and positively invariant, and the solution exists for all $t \ge 0$.

Let $E = \{x \in \Omega : \dot V(x) = 0\}$. Because $K_d$ is positive definite, $E$ is the set of points of $\Omega$ with $\dot q = 0$. Let $x(t)$ be a solution that stays in $E$ for all $t$. Then $\dot q(t) = 0$ for all $t$, so $\ddot q(t) = 0$ and $e$ is constant. The closed loop then gives $0 = M(q)\ddot q = K_p e$, so $e = 0$. The largest invariant set in $E$ is therefore $\{0\}$. By the LaSalle invariance principle, every solution that starts in $\Omega$ tends to $\{0\}$. The initial state was arbitrary, so every solution tends to $0$.

Lyapunov stability of $0$ follows from Lemma 1: $V$ is positive definite and $\dot V \le 0$. Together with the global attraction, $0$ is globally asymptotically stable. $\blacksquare$

**Rest error with a wrong gravity model.** If $\hat g \ne g$ and the arm comes to rest at some $q$, then $\dot q = \ddot q = 0$, and the manipulator equation gives $\tau = g(q)$. Line L2 at rest gives $\tau = K_p e + \hat g(q)$. Hence $K_p e = g(q) - \hat g(q)$. With no gravity model ($\hat g = 0$) this is $K_p e = g(q)$. This relation assumes a rest point; it does not prove that one is reached.
