---
title: Computed-torque control makes the joint error exponentially stable
proves: [correctness]
status: full
---

The arm obeys $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$, where $M(q)$ is symmetric positive definite for each $q$. The desired trajectory $q_d$ is twice differentiable. We write $e = q_d - q$.

**Lemma 1 (closed loop).** Assume that the model is exact: $\hat M(q) = M(q)$, $\hat C(q, \dot q)\dot q = C(q, \dot q)\dot q$ and $\hat g(q) = g(q)$ for all $q$, $\dot q$. Then under COMPUTED-TORQUE, $\ddot e + K_d \dot e + K_p e = 0$.

*Proof.* Lines L1 and L2 compute $e$ and $\dot e$, and line L3 computes $a = \ddot q_d + K_d \dot e + K_p e$. Line L4 gives $\tau = M(q) a + C(q, \dot q)\dot q + g(q)$. We put this $\tau$ into the manipulator equation. The terms $C\dot q$ and $g$ are on both sides and cancel, so $M(q)\ddot q = M(q) a$. Because $M(q)$ is invertible, $\ddot q = a$. Then $\ddot e = \ddot q_d - \ddot q = \ddot q_d - a = -K_d \dot e - K_p e$. $\square$

**Theorem.** If also $K_p$ and $K_d$ are symmetric positive definite, then the state $(e, \dot e) = (0, 0)$ of the closed loop is globally exponentially stable.

*Proof.* Write $z = (e, \dot e) \in \mathbb{R}^{2n}$. By Lemma 1, $\dot z = A z$ with

$$A = \begin{bmatrix} 0 & I \\ -K_p & -K_d \end{bmatrix}.$$

This is a linear time-invariant system, so it is enough to show that each eigenvalue of $A$ has a negative real part. Let $A z = \lambda z$ with $z = (x, y) \ne 0$ and $\lambda \in \mathbb{C}$. The first block row gives $y = \lambda x$, so $x \ne 0$. The second block row gives $-K_p x - \lambda K_d x = \lambda^2 x$. We multiply on the left by $x^*$, the conjugate transpose of $x$, and set $p = x^* K_p x$, $d = x^* K_d x$ and $s = x^* x$. Because $K_p$ and $K_d$ are symmetric positive definite and $x \ne 0$, the numbers $p$, $d$ and $s$ are real and positive. Then

$$s \lambda^2 + d \lambda + p = 0.$$

The roots of a quadratic with positive real coefficients have negative real parts. If the discriminant $d^2 - 4 s p$ is negative, both roots have the real part $-d/(2s) < 0$. If it is not negative, both roots are real, their product $p/s$ is positive and their sum $-d/s$ is negative, so both are negative. Thus $A$ is Hurwitz, and there are constants $k \ge 1$ and $\sigma > 0$ with $\|z(t)\| \le k e^{-\sigma t}\|z(0)\|$ for every initial state. $\blacksquare$

**Diagonal gains.** If $K_p = \operatorname{diag}(\omega_i^2)$ and $K_d = \operatorname{diag}(2 \omega_i)$ with $\omega_i > 0$, the equations separate into $\ddot e_i + 2 \omega_i \dot e_i + \omega_i^2 e_i = 0$. The characteristic polynomial is $(\lambda + \omega_i)^2$, and the solution is $e_i(t) = (e_i(0) + (\dot e_i(0) + \omega_i e_i(0)) t) e^{-\omega_i t}$. One checks this by differentiation: with $c = \dot e_i(0) + \omega_i e_i(0)$, $\dot e_i = (c - \omega_i e_i(0) - \omega_i c t) e^{-\omega_i t}$, which equals $\dot e_i(0)$ at $t = 0$, and $\ddot e_i + 2\omega_i \dot e_i + \omega_i^2 e_i = 0$.

**Steady offset under a model error.** Let the set point be constant ($\dot q_d = \ddot q_d = 0$), and let the model be wrong. Suppose that the closed loop comes to rest at some $q$. Then $\dot q = 0$ and $\ddot q = 0$, so the manipulator equation gives $\tau = g(q)$. Line L4 at rest gives $\tau = \hat M(q) K_p e + \hat g(q)$, because $a = K_p e$ and $\hat C \dot q = 0$. Hence $K_p e = \hat M(q)^{-1}(g(q) - \hat g(q))$, provided $\hat M(q)$ is invertible. The offset is zero when the gravity model is exact at the rest pose, and for $K_p = k I$ its size is of order $1/k$, because $g$, $\hat g$ and $\hat M^{-1}$ are bounded on a bounded set of poses. This statement assumes a rest point; it does not prove that one is reached.
