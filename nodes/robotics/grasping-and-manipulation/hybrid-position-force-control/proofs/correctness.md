---
title: Hybrid control decouples the free directions and sets the contact force
proves: [correctness]
status: full
---

The arm obeys $M\ddot q + C\dot q + g = \tau + J^T F_{\text{ext}}$ with $M$ positive definite and $J$ square and nonsingular, and $x = f(q)$, so $\dot x = J\dot q$ and $\ddot x = J\ddot q + \dot J\dot q$. The matrices $S_f$ and $S_p = I - S_f$ are diagonal with entries 0 or 1, so $S_f^2 = S_f$, $S_p^2 = S_p$ and $S_f S_p = 0$. The gains $K_p$, $K_d$, $K_{fi}$ and $K_v$ are diagonal with positive entries ($K_{fi}$ may be zero). Write $I_f = \int(F_d - F)\,dt$ for the integral state, with $\dot I_f = S_f(F_d - F)$ and $I_f(0) = 0$, and $F = -F_{\text{ext}}$ for the force that the tool applies. Parts 1 to 4 assume that the controller uses the exact model.

**Lemma 1 (closed loop in task space).** Under the torque of lines L1 to L7,

$$\ddot x = S_p a_p + \Lambda^{-1}(S_f F_f + F_{\text{ext}}).$$

*Proof.* Let $h = C\dot q + g$. Then $\ddot q = M^{-1}(J^T F_{\text{cmd}} + J^T F_{\text{ext}} - h)$, so

$$\ddot x = J M^{-1} J^T (F_{\text{cmd}} + F_{\text{ext}}) - J M^{-1} h + \dot J\dot q = \Lambda^{-1}(F_{\text{cmd}} + F_{\text{ext}}) - \Lambda^{-1}\mu,$$

using $\Lambda^{-1} = J M^{-1} J^T$ and $\Lambda^{-1}\mu = J M^{-1} h - \dot J\dot q$ from line L4. The matrix $J M^{-1} J^T$ is positive definite because $J$ is nonsingular, so $\Lambda$ exists. Putting in $F_{\text{cmd}} = \Lambda S_p a_p + S_f F_f + \mu$ from line L5 gives the claim. $\square$

**Lemma 2.** Let $\Lambda^{-1}$ be positive definite and let $w = S_f w$. If $S_f\Lambda^{-1} w = 0$, then $w = 0$.

*Proof.* $w^T\Lambda^{-1}w = (S_f w)^T\Lambda^{-1}w = w^T S_f\Lambda^{-1}w = 0$, and positive definiteness gives $w = 0$. $\square$

**Theorem 1 (rigid frictionless contact).** Let the environment be a rigid frictionless constraint along the force directions: $S_f\dot x = 0$ for all time and $S_p F_{\text{ext}} = 0$. Then at all times the applied force is $F = S_f(F_d + K_{fi} I_f)$ and the position error $e = S_p(x - x_d)$ satisfies $\ddot e + K_d\dot e + K_p e = 0$. With $K_{fi} = 0$, $F = S_f F_d$. With $K_{fi} > 0$, $I_f$ stays zero and $F = S_f F_d$ too.

*Proof.* Let $w = S_f F_f + F_{\text{ext}}$. Since $F_{\text{ext}} = S_f F_{\text{ext}}$, $w = S_f w$. Multiply Lemma 1 by $S_f$: $0 = S_f\ddot x = S_f S_p a_p + S_f\Lambda^{-1}w = S_f\Lambda^{-1}w$. By Lemma 2, $w = 0$, so $F = -F_{\text{ext}} = S_f F_f = S_f(F_d + K_{fi}I_f - K_v\dot x)$. The last term is zero because $S_f K_v\dot x = K_v S_f\dot x = 0$ for diagonal $K_v$. Lemma 1 now reads $\ddot x = S_p a_p$, so $S_p\ddot x = S_p a_p$, and with diagonal gains $S_p a_p = S_p\ddot x_d + K_d S_p(\dot x_d - \dot x) + K_p S_p(x_d - x)$. Subtracting $S_p\ddot x_d$ gives $\ddot e + K_d\dot e + K_p e = 0$. For the integral, $\dot I_f = S_f(F_d - F) = -K_{fi}S_f I_f$, and since $I_f(0) = 0$, $I_f = 0$ for all time. $\square$

With positive diagonal gains, each component of $e$ is a stable second-order linear system, so $e \to 0$ exponentially, and with $K_d^2 = 4K_p$ it does not overshoot.

**Theorem 2 (rest points against a spring surface).** Let $x_d$ be constant and let the environment push only along the force directions, $S_p F_{\text{ext}} = 0$, with any law $F_{\text{ext}}(x)$. At every rest point of the closed loop ($\dot q = 0$, $\ddot q = 0$, $\dot I_f = 0$), $S_p x = S_p x_d$ and $F = S_f F_d$.

*Proof.* At rest, $\dot x = 0$ and $\ddot x = 0$, and $S_p a_p = K_p S_p(x_d - x)$. Let $w = S_f F_f + F_{\text{ext}}$, so $w = S_f w$. Lemma 1 gives $\Lambda^{-1}w = -S_p a_p$. Then $w^T\Lambda^{-1}w = -w^T S_f S_p a_p = 0$, so $w = 0$, and then $S_p a_p = 0$, which gives $S_p x = S_p x_d$. From $w = 0$, $F = S_f F_f = S_f(F_d + K_{fi}I_f)$. In each force direction, either $K_{fi} = 0$ and the force is that component of $F_d$, or $K_{fi} > 0$ and $\dot I_f = 0$ gives the same. $\square$

**Theorem 3 (stability of one force direction).** Let there be one force direction $f$, a spring surface with $F_{\text{ext},f} = -k_e(x_f - x_w)$ in contact, $S_p F_{\text{ext}} = 0$ and constant $F_d$. Hold $c = (\Lambda^{-1})_{ff} > 0$ fixed and put $m_f = 1/c$. Then the force subsystem is exponentially stable if and only if $K_{fi} < K_v/m_f$ (for $K_{fi} > 0$); for $K_{fi} = 0$, its motion part is exponentially stable for all $K_v > 0$.

*Proof.* The vector $w = S_f F_f + F_{\text{ext}}$ has only entry $f$ nonzero, equal to $F_f + F_{\text{ext},f}$, and the entry $f$ of $S_p a_p$ is zero. So the $f$ row of Lemma 1 is $\ddot x_f = c(F_f + F_{\text{ext},f})$, which does not involve the position directions. With $z = x_f - x_w$ and $F_f = F_d + K_{fi}I - K_v\dot z$,

$$m_f\ddot z = F_d + K_{fi}I - K_v\dot z - k_e z,\qquad \dot I = F_d - k_e z.$$

Differentiating the first equation and using the second gives $m_f\dddot z + K_v\ddot z + k_e\dot z + K_{fi}k_e z = K_{fi}F_d$. The characteristic polynomial is $m_f s^3 + K_v s^2 + k_e s + K_{fi}k_e$. For $K_{fi} > 0$, the Routh-Hurwitz test for a cubic with positive coefficients says that all roots have negative real part if and only if $K_v k_e > m_f K_{fi}k_e$, which is $K_{fi} < K_v/m_f$. For $K_{fi} = 0$, the variable $I$ does not enter, and the motion obeys $m_f\ddot z + K_v\dot z + k_e z = F_d$, which is exponentially stable for $K_v, k_e > 0$. $\square$

**Remark (wrong model).** If the controller uses a wrong model, Lemma 1 fails, and so does the conclusion of Theorem 2 for $K_{fi} = 0$. The step "$\dot I_f = 0$ gives $F = S_f F_d$" does not use the model, so with $K_{fi} > 0$ every rest point still has the exact force $S_f F_d$. The position directions have no integral term, so their rest error remains. $\blacksquare$
