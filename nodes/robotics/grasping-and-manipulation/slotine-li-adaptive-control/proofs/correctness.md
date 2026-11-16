---
title: The Slotine-Li controller drives the tracking error to zero
proves: [correctness]
status: full
---

The arm obeys $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$ with $q \in \mathbb{R}^n$. We assume:

1. $M(q)$ is symmetric, and there are constants $0 < \mu \le \bar\mu$ with $\mu\, x^T x \le x^T M(q) x \le \bar\mu\, x^T x$ for all $q$, $x$.
2. $C$ is the Christoffel matrix, so $\dot M - 2C$ is skew-symmetric: $x^T(\dot M - 2C)x = 0$ for every vector $x$, where $\dot M = \frac{d}{dt}M(q(t))$.
3. $M$, $C$, $g$ and $Y$ are continuous, and $Y(q, \dot q, v, a)\pi = M(q)a + C(q, \dot q)v + g(q)$ for all arguments, with a constant $\pi$. On bounded sets of arguments they are bounded.
4. $q_d$, $\dot q_d$ and $\ddot q_d$ are bounded, and $\Lambda$, $K_D$, $\Gamma$ are symmetric positive definite.

We write $\tilde q = q - q_d$, $\tilde\pi = \hat\pi - \pi$, and $Y$ for $Y(q, \dot q, \dot q_r, \ddot q_r)$.

**Lemma 1 (closed loop).** Under SLOTINE-LI, $\dot{\tilde q} = -\Lambda\tilde q + s$ and $M(q)\dot s + C(q, \dot q)s + K_D s = Y\tilde\pi$.

*Proof.* Line L4 gives $s = \dot q - \dot q_r = \dot q - \dot q_d + \Lambda\tilde q = \dot{\tilde q} + \Lambda\tilde q$, which is the first equation. The derivative of $\dot q_r = \dot q_d - \Lambda\tilde q$ is $\ddot q_d - \Lambda(\dot q - \dot q_d)$, which is the value $\ddot q_r$ of line L3. So $\dot s = \ddot q - \ddot q_r$. By assumption 3, $Y\pi = M\ddot q_r + C\dot q_r + g$, and line L5 gives $\tau = Y\pi + Y\tilde\pi - K_D s$. The arm equation becomes $M\ddot q + C\dot q + g = M\ddot q_r + C\dot q_r + g + Y\tilde\pi - K_D s$. We subtract and use $\dot s = \ddot q - \ddot q_r$ and $s = \dot q - \dot q_r$ to get $M\dot s + Cs = Y\tilde\pi - K_D s$. $\square$

**Lemma 2.** The function $V = \tfrac12 s^T M(q)s + \tfrac12\tilde\pi^T\Gamma^{-1}\tilde\pi$ satisfies $\dot V = -s^T K_D s$.

*Proof.* $\pi$ is constant, so $\dot{\tilde\pi} = \dot{\hat\pi} = -\Gamma Y^T s$ by line L6. $M$ and $\Gamma^{-1}$ are symmetric, so

$$\dot V = s^T M\dot s + \tfrac12 s^T\dot M s + \tilde\pi^T\Gamma^{-1}\dot{\tilde\pi} = s^T(Y\tilde\pi - Cs - K_D s) + \tfrac12 s^T\dot M s - \tilde\pi^T Y^T s.$$

The terms $s^T Y\tilde\pi$ and $\tilde\pi^T Y^T s$ are the same number and cancel. What is left is $-s^T K_D s + \tfrac12 s^T(\dot M - 2C)s$, and the last term is zero by assumption 2. $\square$

**Theorem.** Under assumptions 1 to 4, every solution of the closed loop is bounded, $\hat\pi$ is bounded, and $\tilde q(t) \to 0$ and $\dot{\tilde q}(t) \to 0$ as $t \to \infty$.

*Proof.* Step 1 (boundedness). By Lemma 2, $V(t) \le V(0)$. By assumption 1, $\tfrac12\mu\|s\|^2 \le V$, so $s$ is bounded, and $\tilde\pi$ is bounded because $\Gamma^{-1}$ is positive definite. The equation $\dot{\tilde q} = -\Lambda\tilde q + s$ is a linear system with the Hurwitz matrix $-\Lambda$ and a bounded input, so $\tilde q$ is bounded, and then $\dot{\tilde q}$ is bounded. With assumption 4, $q$, $\dot q$, $\dot q_r$ and $\ddot q_r$ are bounded. So $Y$, $C$ and $g$ are bounded by assumption 3. By Lemma 1 and assumption 1, $\dot s = M^{-1}(Y\tilde\pi - Cs - K_D s)$ is bounded, since $\|M^{-1}\| \le 1/\mu$.

Step 2 ($s \to 0$). Integrating Lemma 2 gives $\int_0^t s^T K_D s\, d\tau = V(0) - V(t) \le V(0)$. So the function $w(t) = s(t)^T K_D s(t) \ge 0$ has a finite integral over $[0, \infty)$. Its derivative $2 s^T K_D\dot s$ is bounded by step 1, so $w$ is uniformly continuous. By Barbalat's lemma, $w(t) \to 0$, and since $K_D$ is positive definite, $s(t) \to 0$.

Step 3 ($\tilde q \to 0$). Let $\kappa > 0$ be the smallest eigenvalue of $\Lambda$. Then $\|e^{-\Lambda t}\| = e^{-\kappa t}$ because $\Lambda$ is symmetric. For $t \ge T \ge 0$,

$$\tilde q(t) = e^{-\Lambda(t - T)}\tilde q(T) + \int_T^t e^{-\Lambda(t - \tau)}s(\tau)\, d\tau.$$

Given $\varepsilon > 0$, choose $T$ with $\|s(\tau)\| \le \varepsilon$ for $\tau \ge T$. Then $\|\tilde q(t)\| \le e^{-\kappa(t - T)}\|\tilde q(T)\| + \varepsilon/\kappa$, which is less than $2\varepsilon/\kappa$ for $t$ large. So $\tilde q \to 0$, and $\dot{\tilde q} = -\Lambda\tilde q + s \to 0$. $\blacksquare$

**Remark on the parameters.** The proof shows that $\hat\pi$ is bounded, not that it converges to $\pi$. When $\tilde q \to 0$ and $s \to 0$, Lemma 1 gives $Y\tilde\pi \to 0$ along the trajectory. If $Y$ along the desired trajectory is persistently exciting, this forces $\tilde\pi \to 0$; otherwise $\tilde\pi$ can stay away from zero.
