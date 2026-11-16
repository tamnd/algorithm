---
title: Impedance control gives the target impedance
proves: [correctness]
status: full
---

The arm obeys $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau + J(q)^T F_{\text{ext}}$, where $x = f(q)$ and $\dot x = J(q)\dot q$. We assume that the model in line L5 is exact, that $J(q)$ is nonsingular along the motion, and that the value $F_{\text{ext}}$ passed to IMPEDANCE is the true contact force. $M_d$, $D_d$ and $K_d$ are symmetric positive definite.

**Theorem 1 (target dynamics).** Under these assumptions, $M_d\ddot{\tilde x} + D_d\dot{\tilde x} + K_d\tilde x = F_{\text{ext}}$ at every time, where $\tilde x = x - x_0$.

*Proof.* Put the torque of line L5 into the arm equation:

$$M\ddot q + C\dot q + g = M a_q + C\dot q + g - J^T F_{\text{ext}} + J^T F_{\text{ext}}.$$

The terms $C\dot q$, $g$ and $J^T F_{\text{ext}}$ cancel, so $M\ddot q = M a_q$, and $\ddot q = a_q$ because $M$ is invertible. Differentiating $\dot x = J\dot q$ gives $\ddot x = J\ddot q + \dot J\dot q = J a_q + \dot J\dot q$. By line L4, $J a_q = a_x - \dot J\dot q$, so $\ddot x = a_x$. By line L3, $M_d(a_x - \ddot x_0) = F_{\text{ext}} - D_d\dot{\tilde x} - K_d\tilde x$. With $\ddot{\tilde x} = \ddot x - \ddot x_0 = a_x - \ddot x_0$ this is the target equation. $\square$

**Theorem 2 (bounded energy with a passive environment).** Let the goal be fixed ($\dot x_0 = 0$). Let the environment be a spring with energy $U_e(x) \ge 0$ and force $F_{\text{ext}} = -\nabla U_e(x)$. Then $W = \tfrac12\dot{\tilde x}^T M_d\dot{\tilde x} + \tfrac12\tilde x^T K_d\tilde x + U_e(x)$ satisfies $\dot W = -\dot{\tilde x}^T D_d\dot{\tilde x} \le 0$.

*Proof.* With a fixed goal, $\dot{\tilde x} = \dot x$. By Theorem 1 and the symmetry of $M_d$ and $K_d$,

$$\dot W = \dot x^T(F_{\text{ext}} - D_d\dot x - K_d\tilde x) + \tilde x^T K_d\dot x + \nabla U_e(x)^T\dot x = \dot x^T F_{\text{ext}} - \dot x^T D_d\dot x + \nabla U_e^T\dot x.$$

The first and last terms cancel because $F_{\text{ext}} = -\nabla U_e$. $\square$

So $\tilde x$ and $\dot x$ stay bounded by $W(0)$, and the contact force stays bounded on the bounded set of positions that the motion can reach.

**Theorem 3 (rest force against a spring wall).** Let the task directions be decoupled ($M_d$, $D_d$, $K_d$ diagonal), and let the wall act along the first coordinate with $F_{\text{ext},1} = -k_e(x_1 - x_w)$ for $x_1 > x_w$ and $0$ otherwise, with $k_e > 0$ and $x_{0,1} > x_w$. If the closed loop is at rest, then $x_1 = (k_d x_{0,1} + k_e x_w)/(k_d + k_e)$ and the force on the wall is $\frac{k_e k_d}{k_e + k_d}(x_{0,1} - x_w)$, where $k_d$ is the first diagonal entry of $K_d$.

*Proof.* At rest, $\dot{\tilde x} = \ddot{\tilde x} = 0$, so Theorem 1 gives $k_d(x_1 - x_{0,1}) = F_{\text{ext},1}$. If $x_1 \le x_w$, the right side is $0$, so $x_1 = x_{0,1} > x_w$, which is a contradiction. So $x_1 > x_w$ and $k_d(x_1 - x_{0,1}) = -k_e(x_1 - x_w)$. Solving gives the stated $x_1$. The force on the wall is $k_e(x_1 - x_w) = k_e\big(\frac{k_d x_{0,1} + k_e x_w}{k_d + k_e} - x_w\big) = \frac{k_e k_d}{k_d + k_e}(x_{0,1} - x_w)$. $\square$

**Law without a force sensor.** For $\tau = J^T(K_d(x_0 - x) - D_d\dot x) + g(q)$ with a fixed goal, the function $W' = \tfrac12\dot q^T M\dot q + \tfrac12\tilde x^T K_d\tilde x + U_e(x)$ satisfies $\dot W' = -\dot x^T D_d\dot x$. The computation is the one of PD control with gravity compensation: $\dot W' = \dot q^T(\tau + J^T F_{\text{ext}} - C\dot q - g) + \tfrac12\dot q^T\dot M\dot q + \tilde x^T K_d\dot x - F_{\text{ext}}^T\dot x$, the skew symmetry removes the $C$ and $\dot M$ terms, and $\dot q^T J^T = \dot x^T$ removes the rest except $-\dot x^T D_d\dot x$. At rest, $J^T(K_d(x_0 - x) + F_{\text{ext}}) = 0$, and since $J$ is nonsingular, $K_d\tilde x = F_{\text{ext}}$, so Theorem 3 holds for this law too.
