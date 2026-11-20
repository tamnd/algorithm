---
title: The Langevin equation keeps the canonical density, and the OBABO step keeps the velocity law exactly
proves: [correctness]
status: full
---

The Langevin equations for $N$ particles in $d$ dimensions are
$$dx_i = v_i\,dt, \qquad m_i\,dv_i = f_i(x)\,dt - m_i \gamma v_i\,dt + \sqrt{2 m_i \gamma k_B T}\,dW_i, \qquad (1)$$
with $f = -\nabla U$, $\gamma \ge 0$ and independent Wiener processes $W_i$. Let $\rho(x, v) \propto \exp(-\beta(K + U))$ with $\beta = 1/(k_B T)$.

**Claim 1 (the canonical density is stationary).** $\rho$ is a stationary solution of the Fokker-Planck equation of (1).

*Proof.* The Fokker-Planck operator is $\mathcal{L}^* = \mathcal{L}^*_H + \mathcal{L}^*_O$. The Hamiltonian part $\mathcal{L}^*_H \rho = -\sum_i \bigl( v_i \cdot \nabla_{x_i} \rho + \frac{f_i}{m_i} \cdot \nabla_{v_i} \rho \bigr)$ is 0 for any function of $H = K + U$, since $v_i \cdot \nabla_{x_i} H + \frac{f_i}{m_i} \cdot m_i v_i = v_i \cdot (-f_i) + f_i \cdot v_i = 0$. The friction and noise part is
$$\mathcal{L}^*_O \rho = \sum_{i,a} \partial_{v_{ia}} \Bigl( \gamma v_{ia} \rho + \frac{\gamma k_B T}{m_i} \partial_{v_{ia}} \rho \Bigr),$$
and for $\rho$ the bracket is $\gamma v_{ia} \rho - \gamma v_{ia} \rho = 0$, because $\partial_{v_{ia}} \rho = -\beta m_i v_{ia} \rho$. $\square$

The size of the noise is fixed by the friction: with any other factor than $2 m_i \gamma k_B T$ the bracket does not vanish. This is the fluctuation-dissipation relation. For $\gamma > 0$ and a smooth $U$ that grows at infinity, $\rho$ is also the unique stationary law and time averages converge to canonical averages (the noise reaches all velocities and the forces couple them to the positions). We do not prove this part here.

**Claim 2 (the exact O step).** The solution of $dv = -\gamma v\,dt + \sqrt{2\gamma k_B T / m}\,dW$ over a time $t$ is
$$v(t) = c\,v(0) + \sqrt{(1 - c^2)\,k_B T / m}\;R, \qquad c = e^{-\gamma t},$$
with $R$ standard normal and independent of $v(0)$. Lines L3 and L8 apply it with $t = h/2$.

*Proof.* $v(t) = e^{-\gamma t} v(0) + \sqrt{2\gamma k_B T/m} \int_0^t e^{-\gamma(t - s)}\,dW_s$. The integral is normal with mean 0 and variance $\int_0^t e^{-2\gamma(t-s)} ds = (1 - c^2)/(2\gamma)$, so the noise term has variance $(1 - c^2) k_B T / m$. $\square$

So the O step keeps the Maxwell-Boltzmann law exactly: if $v(0)$ is normal with variance $k_B T/m$, then $v(t)$ is normal with variance $c^2 k_B T/m + (1 - c^2) k_B T/m = k_B T/m$. It does not change $x$, so it keeps $\rho$ exactly, for every $h$.

**Claim 3 (the step).** One step is $O_{h/2} \circ V_{h/2} \circ A_h \circ V_{h/2} \circ O_{h/2}$, the O half steps around a velocity Verlet step. The O parts keep $\rho$ exactly. The Verlet part keeps the volume of phase space and keeps $H$ up to $O(h^2)$, so it keeps $\rho$ only up to the time step error.

*Proof.* Lines L4 to L7 are velocity Verlet, as on the [molecular dynamics](/molecular-dynamics/) page; Claim 2 covers L3 and L8. $\square$

**Claim 4 (the harmonic oscillator).** Let $d = N = 1$, $U = \frac12 k x^2$, $\omega^2 = k/m$, $q = h^2\omega^2/4 < 1$ and $\gamma > 0$. Then the stationary law of the OBABO chain is normal, with $x$ and $v$ independent,
$$\langle v^2 \rangle = \frac{k_B T}{m}, \qquad \langle x^2 \rangle = \frac{k_B T}{k}\,\frac{1}{1 - q},$$
and the chain converges to it from any start.

*Proof.* Scale so that $m = \omega = k_B T = 1$ (put $h\omega$ for $h$). One velocity Verlet step is the linear map
$$x' = a x + h v, \qquad v' = a v - h(1 - q) x, \qquad a = 1 - h^2/2.$$
It keeps $Q = v^2 + (1 - q) x^2$: the cross terms are $-2ah(1-q)xv + 2ah(1-q)xv = 0$, the coefficient of $v^2$ is $a^2 + (1 - q)h^2 = 1$, and the coefficient of $x^2$ is $(1-q)(h^2(1-q) + a^2) = 1 - q$. Its determinant is 1. So it keeps the normal law $G$ with density proportional to $e^{-Q/2}$, which has $\langle v^2 \rangle = 1$, $\langle x^2 \rangle = 1/(1-q)$ and no correlation. The O step keeps $G$ by Claim 2, since under $G$ the velocity is independent of $x$ with variance 1. So $G$ is stationary.

For uniqueness, the chain is $z_{n+1} = M z_n + \epsilon_n$ with independent normal $\epsilon_n$ and $M = D P D$, where $D = \operatorname{diag}(1, c)$ and $P$ is the Verlet map. In the norm $\|z\|^2 = Q(z)$, $P$ is an isometry and $D$ is a contraction, with $\|Dz\| = \|z\|$ only if $v = 0$. If $\|Mz\| = \|z\|$, then $Dz = z$, so $v = 0$, and $D(Pz) = Pz$, so $v' = -h(1-q)x = 0$, so $x = 0$. So $\|Mz\| < \|z\|$ for $z \ne 0$, $\|M\| < 1$ by compactness of the unit sphere, and the law of $z_n$ converges to the unique stationary law. $\square$

So the velocities have the right variance for every stable $h$, and the positions have an error of relative size $q = h^2\omega^2/4$. For $h\omega = 1$ the position variance is $4/3$ of the right value. The tests compute both values by iteration of the covariance and by sampling.

**Claim 5 (limits).** With $\gamma = 0$, $c = 1$, the O steps do nothing, and the step is velocity Verlet. With $f = 0$, the Verlet part does not change $v$, so the velocities at the step times follow $O_{h/2} \circ O_{h/2} = O_h$: they are an exact sample path of the Ornstein-Uhlenbeck process, with correlation $e^{-\gamma h}$ between consecutive steps. $\square$
