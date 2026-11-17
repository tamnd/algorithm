---
title: The collision impulse makes Newton's restitution law hold, conserves momentum and removes a known amount of energy
proves: [correctness, termination]
status: full
---

The setting is one contact point $p$ between two rigid bodies $A$ and $B$ at one instant. Body $X \in \{A, B\}$ has center of mass $x_X$, linear velocity $v_X$, angular velocity $\omega_X$, mass $m_X$ and inertia tensor $I_X$ in world coordinates. $I_X$ is symmetric positive definite. A static body has $m_X^{-1} = 0$ and $I_X^{-1} = 0$. The unit normal $n$ points from $B$ to $A$, $r_X = p - x_X$, and the velocity of the material point of $X$ at $p$ is $u_X = v_X + \omega_X \times r_X$. The relative normal velocity is $v_{rel} = n \cdot (u_A - u_B)$. The collision is instantaneous: positions do not change, and only the impulse $j n$ on $A$ and $-j n$ on $B$ acts. A superscript $-$ marks a value before the impulse and $+$ a value after it.

**Lemma 1 (response of one body).** If an impulse $J$ acts on body $X$ at $p$, then $v_X^+ = v_X^- + m_X^{-1} J$ and $\omega_X^+ = \omega_X^- + I_X^{-1} (r_X \times J)$. So $u_X^+ - u_X^- = m_X^{-1} J + (I_X^{-1} (r_X \times J)) \times r_X$.

*Proof.* An impulse is the integral of a force over a time interval of length tending to zero. The linear momentum $m_X v_X$ changes by $J$, and the angular momentum about the center of mass, $I_X \omega_X$, changes by the moment $r_X \times J$ (Newton-Euler equations, integrated over the interval; the bounded terms such as $\omega \times I \omega$ integrate to zero as the interval shrinks). Divide by $m_X$ and multiply by $I_X^{-1}$. The second formula is the definition of $u_X$ applied to the differences. $\square$

**Lemma 2 (the scalar $k$).** Let $k = m_A^{-1} + m_B^{-1} + n \cdot ((I_A^{-1} (r_A \times n)) \times r_A) + n \cdot ((I_B^{-1} (r_B \times n)) \times r_B)$, the value of line L4. Then $n \cdot ((I_X^{-1} (r_X \times n)) \times r_X) = (r_X \times n)^T I_X^{-1} (r_X \times n) \ge 0$, so $k \ge 0$, and $k > 0$ when at least one body is not static.

*Proof.* For vectors $a, b, c$, the scalar triple product satisfies $a \cdot (b \times c) = b \cdot (c \times a)$. With $a = n$, $b = I_X^{-1} (r_X \times n)$ and $c = r_X$, this gives $n \cdot (b \times r_X) = b \cdot (r_X \times n) = (r_X \times n)^T I_X^{-1} (r_X \times n)$. The inverse of a symmetric positive definite matrix is symmetric positive definite, so this is $\ge 0$, and it is $0$ for a static body. A body that is not static has $m_X^{-1} > 0$. $\square$

**Theorem 1 (restitution).** If $v_{rel}^- < 0$ and $k > 0$, then after lines L5 to L7, $v_{rel}^+ = -e\, v_{rel}^-$.

*Proof.* By Lemma 1 with $J = j n$ on $A$ and $J = -j n$ on $B$, and by linearity in $J$, $n \cdot (u_A^+ - u_A^-) = j\,(m_A^{-1} + n \cdot ((I_A^{-1} (r_A \times n)) \times r_A))$ and $n \cdot (u_B^+ - u_B^-) = -j\,(m_B^{-1} + n \cdot ((I_B^{-1} (r_B \times n)) \times r_B))$. Subtract: $v_{rel}^+ - v_{rel}^- = j k$. Line L5 sets $j = -(1 + e) v_{rel}^- / k$, so $v_{rel}^+ = v_{rel}^- - (1 + e) v_{rel}^- = -e\, v_{rel}^-$. $\square$

For $0 \le e \le 1$ and $v_{rel}^- < 0$, $j > 0$, so the impulse pushes the bodies apart and $v_{rel}^+ \ge 0$. If $v_{rel}^- \ge 0$, line L3 returns with no change, because the bodies do not approach and a contact cannot pull.

**Theorem 2 (momentum).** If neither body is static, the total linear momentum $m_A v_A + m_B v_B$ and the total angular momentum about any fixed point $o$, $\sum_X ((x_X - o) \times m_X v_X + I_X \omega_X)$, do not change. A static body takes up the impulse without moving, so with a static body the momentum of the moving body changes, as it must.

*Proof.* The change of linear momentum is $j n - j n = 0$. The change of angular momentum about $o$ is $(x_A - o) \times j n + r_A \times j n - (x_B - o) \times j n - r_B \times j n$ by Lemma 1, because $x_X$ does not change. Since $x_X + r_X = p$ for both bodies, this is $(p - o) \times j n - (p - o) \times j n = 0$. $\square$

**Theorem 3 (energy).** Let $T = \sum_X \tfrac12 (m_X v_X \cdot v_X + \omega_X \cdot I_X \omega_X)$. Then $T^- - T^+ = (1 - e^2) (v_{rel}^-)^2 / (2k)$. In particular, for $e = 1$ the kinetic energy does not change, and for $0 \le e < 1$ it decreases.

*Proof.* For one body and an impulse $J$ at $p$: $\tfrac12 m (v^+ \cdot v^+ - v^- \cdot v^-) = \tfrac12 m (v^+ - v^-) \cdot (v^+ + v^-) = \tfrac12 J \cdot (v^+ + v^-)$. Since $I$ is symmetric, $\tfrac12 (\omega^{+T} I \omega^+ - \omega^{-T} I \omega^-) = \tfrac12 (\omega^+ - \omega^-)^T I (\omega^+ + \omega^-) = \tfrac12 (r \times J) \cdot (\omega^+ + \omega^-) = \tfrac12 J \cdot ((\omega^+ + \omega^-) \times r)$, by Lemma 1 and the triple product rule. The sum is $\tfrac12 J \cdot (u^+ + u^-)$. With $J = j n$ on $A$ and $-j n$ on $B$, the total change is $T^+ - T^- = \tfrac12 j (v_{rel}^+ + v_{rel}^-) = \tfrac12 j (1 - e) v_{rel}^-$ by Theorem 1. Insert $j = -(1 + e) v_{rel}^- / k$: $T^+ - T^- = -(1 + e)(1 - e) (v_{rel}^-)^2 / (2k)$. $\square$

**Termination and cost.** The procedure has no loop. It does a fixed number of cross products, dot products and 3 by 3 matrix-vector products, so it ends after $O(1)$ arithmetic operations.

**What is not proved.** The theorems are about the model: an instantaneous collision at one point, no friction, and Newton's law $v_{rel}^+ = -e\, v_{rel}^-$ with an empirical $e$. They say nothing about the accuracy of that model for real objects. With friction, or with several simultaneous contacts that are treated one at a time, Theorem 3 does not apply as stated.
