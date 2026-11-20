---
title: Each BAOAB part is an exact flow, and for a harmonic force the positions have the exact canonical law
proves: [correctness]
status: full
---

We use the Langevin equations $dx = v\,dt$, $m\,dv = f(x)\,dt - m\gamma v\,dt + \sqrt{2m\gamma k_B T}\,dW$ and the pseudocode of the page.

**Claim 1 (the parts).** Line L3 and line L8 are the exact flow $B_{h/2}$ of $dv = (f/m)\,dt$ with $x$ fixed. Lines L4 and L6 are the exact flow $A_{h/2}$ of $dx = v\,dt$ with $v$ fixed. Line L5 is an exact draw from the flow $O_h$ of $dv = -\gamma v\,dt + \sqrt{2\gamma k_B T/m}\,dW$ with $x$ fixed.

*Proof.* With $x$ fixed, $f$ is constant, so the kick is exact. With $v$ fixed, the drift is exact. The O flow over a time $h$ is $v \mapsto c v + \sqrt{(1 - c^2) k_B T/m}\,R$ with $c = e^{-\gamma h}$ and $R$ standard normal (the Ornstein-Uhlenbeck solution, as on the [Langevin dynamics](/langevin-dynamics/) page). Line L5 uses $c$ and the standard deviation computed before the loop. The force used in line L3 of a step was computed in line L7 of the step before, at the same positions, because nothing changes $x$ between them. $\square$

**Claim 2 (what each part keeps).** $O_h$ keeps the canonical density $\rho \propto e^{-\beta(K + U)}$ exactly. $A$ and $B$ keep the volume of phase space, but not $\rho$.

*Proof.* $O_h$ keeps the Maxwell-Boltzmann law of $v$ ($c^2 + (1 - c^2) = 1$ times $k_B T/m$) and does not touch $x$. $A$ and $B$ are shears, with Jacobian determinant 1. $\square$

So BAOAB is not exact for a general force. The error in the configurational averages is $O(h^2)$ in general. Leimkuhler and Matthews (2013) show that in the limit of large friction it becomes $O(h^4)$ for BAOAB; this proof does not repeat that analysis. The next claim shows the effect in a case we can solve.

**Claim 3 (the regrouped chain).** Let $u_n$ be the state just before line L5 of step $n + 1$. Then $u_{n+1} = N(u_n)$ with $N = A_{h/2} \circ B_h \circ A_{h/2} \circ O_h$, read from right to left, and the state at the end of step $n + 1$ is $z_{n+1} = B_{h/2} \circ A_{h/2} \circ O_h (u_n)$.

*Proof.* After line L5 of step $n + 1$ the step applies $A_{h/2}$ (L6) and $B_{h/2}$ (L8). The next step applies $B_{h/2}$ (L3) and $A_{h/2}$ (L4) before its line L5. Two kicks at the same positions add up to $B_h$. $\square$

$A_{h/2} B_h A_{h/2}$ is one step of position Verlet.

**Claim 4 (the harmonic oscillator).** Let $U = \frac12 k x^2$ in one dimension, $\omega^2 = k/m$, $q = h^2\omega^2/4 < 1$ and $\gamma > 0$. Then the chain $z_n$ of states at the ends of the steps has a unique stationary law, it converges to it from any start, and the law is normal with
$$\langle x^2 \rangle = \frac{k_B T}{k}, \qquad \langle v^2 \rangle = \frac{k_B T}{m}(1 - q), \qquad \langle x v \rangle = 0.$$
So the positions have the exact canonical law for every stable $h$.

*Proof.* Scale so that $m = \omega = k_B T = 1$ (put $h\omega$ for $h$). Position Verlet is the linear map
$$x' = a x + h(1 - q) v, \qquad v' = a v - h x, \qquad a = 1 - h^2/2,$$
with determinant 1. It keeps $Q = x^2/(1 - q) + v^2$: the cross terms are $2ahxv - 2ahxv = 0$, the coefficient of $x^2$ is $(a^2 + h^2(1 - q))/(1 - q) = 1/(1 - q)$, and the coefficient of $v^2$ is $h^2(1 - q) + a^2 = 1$. So it keeps the normal law $G$ with density proportional to $e^{-Q/2}$: $x$ and $v$ independent, $\langle x^2 \rangle = 1 - q$, $\langle v^2 \rangle = 1$. $O_h$ keeps $G$, since under $G$ the velocity is independent of $x$ with variance 1. So $G$ is stationary for $N$.

It is the only stationary law. In the norm $\|z\|^2 = Q(z)$, position Verlet $P$ is an isometry and $D = \operatorname{diag}(1, c)$, the mean part of $O_h$, is a contraction with $\|Dz\| = \|z\|$ only if $v = 0$. If $\|PDPDz\| = \|z\|$, then $v = 0$ and the velocity of $Pz$ is 0, which is $-hx = 0$, so $z = 0$. So $\|(PD)^2\| < 1$, the spectral radius of $PD$ is less than 1, and $u_n$ converges in law to $G$.

Now push $G$ through $O_h$ (no change), then $A_{h/2}$ and $B_{h/2}$:
$$x_1 = x + \tfrac{h}{2} v, \qquad v_1 = v - \tfrac{h}{2} x_1 = (1 - q) v - \tfrac{h}{2} x.$$
Then $\langle x_1^2 \rangle = (1 - q) + h^2/4 = 1$, $\langle v_1^2 \rangle = (1 - q)^2 + \frac{h^2}{4}(1 - q) = 1 - q$ and $\langle x_1 v_1 \rangle = \frac{h}{2}(1 - q) - \frac{h}{2}(1 - q) = 0$. $\square$

The error is moved into the velocities, which have the variance $1 - q$ of the right value. Velocity averages, such as the kinetic temperature, must therefore not be computed from $v$ at the end of a BAOAB step if the time step is large. For $h\omega = 1$ the velocity variance is $3/4$ of the right value.

**Claim 5 (limits).** With $\gamma = 0$, $c = 1$ and the noise is 0, so line L5 does nothing and the step is $B_{h/2} A_h B_{h/2}$, velocity Verlet. $\square$
