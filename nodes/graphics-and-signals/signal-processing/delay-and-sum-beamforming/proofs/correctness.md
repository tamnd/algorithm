---
title: Delay-and-sum aligns the look direction, gains M against white noise, and has grating lobes exactly when the spacing is too large
proves: [correctness]
status: full
---

We prove four facts about the algorithm on the main page. The first two are about the time-domain form with whole-sample delays (lines L1 to L8), and the last two are about the beam pattern of a uniform linear array. We work in exact real arithmetic.

**Setting.** Sensor $m$, for $m = 0, \ldots, M-1$, records $x_m[t] = s[t - \tau_m] + n_m[t]$, where $s$ is the wave from the look direction, $\tau_m$ is its arrival delay at sensor $m$ in whole samples, as line L1 computes it, and $n_m$ is noise. Let $\tau_{\min} = \min_m \tau_m$ and $\Delta = \max_m \tau_m - \tau_{\min}$.

**Theorem 1 (alignment).** For every $t$ with $0 \le t < T - \Delta$, the output is $y[t] = s[t - \tau_{\min}] + \frac1M \sum_m n_m[t + \tau_m - \tau_{\min}]$.

*Proof.* Lines L4 to L7 compute $y[t] = \frac1M \sum_m x_m[t + \tau_m - \tau_{\min}]$. The index is at least $0$ because $\tau_m \ge \tau_{\min}$, and at most $t + \Delta < T$, so every sample exists. Substituting the model, sensor $m$ contributes $s[t + \tau_m - \tau_{\min} - \tau_m] = s[t - \tau_{\min}]$, the same value for all $m$, and the $M$ equal terms divided by $M$ give $s[t - \tau_{\min}]$. $\square$

**Theorem 2 (array gain).** If the noise samples $n_0[t_0], \ldots, n_{M-1}[t_{M-1}]$ at any fixed times are uncorrelated with mean $0$ and variance $\sigma^2$, the noise in $y[t]$ has variance $\sigma^2 / M$. So the signal-to-noise ratio of the output is $M$ times that of one sensor.

*Proof.* By Theorem 1 the noise in $y[t]$ is $\frac1M \sum_m n_m[t_m]$ with $t_m = t + \tau_m - \tau_{\min}$. Its mean is $0$ and, because the cross terms have expectation $0$, its variance is $\frac1{M^2} \sum_m \sigma^2 = \sigma^2/M$. The signal term is unchanged. $\square$

By the Cauchy-Schwarz inequality, no other weights do better against white noise; this bound is on the [beamforming](/beamforming/) page.

**Beam pattern.** For a uniform linear array with spacing $d$ and a narrowband wave of wavelength $\lambda$, a unit wave from the direction with $u = \sin\theta$ gives the snapshot $a(u)$ with $a_m(u) = e^{-i 2\pi (d/\lambda) m u}$. Delay-and-sum steered to $u_0$ has the weights $w = a(u_0)/M$, and its response is $B(u) = |w^H a(u)|$. Let $\psi = 2\pi (d/\lambda)(u - u_0)$.

**Theorem 3 (the pattern and its peak).** $B(u) = \left| \dfrac{\sin(M\psi/2)}{M \sin(\psi/2)} \right|$ when $\psi \notin 2\pi\mathbb Z$, and $B(u) = 1$ when $\psi \in 2\pi\mathbb Z$. For all $u$, $B(u) \le 1 = B(u_0)$, and for $M \ge 2$ equality holds exactly when $\psi \in 2\pi\mathbb Z$.

*Proof.* $\bar a_m(u_0) a_m(u) = e^{-i m \psi}$, so $w^H a(u) = \frac1M \sum_{m=0}^{M-1} z^m$ with $z = e^{-i\psi}$. If $z = 1$ the sum is $M$ and $B = 1$. Otherwise the geometric sum is $(1 - z^M)/(1 - z)$, and $|1 - e^{-i\phi}| = 2|\sin(\phi/2)|$ gives the quotient. By the triangle inequality, $|\sum_m z^m| \le \sum_m |z^m| = M$, with equality exactly when all terms $z^m$ point in the same direction as $z^0 = 1$. For $M \ge 2$ this includes the term $z^1 = z$, so equality forces $z = 1$, that is $\psi \in 2\pi\mathbb Z$. $\square$

**Theorem 4 (grating lobes).** Call $u \in [-1, 1]$ with $u \ne u_0$ and $B(u) = 1$ a grating lobe, for $M \ge 2$ and $|u_0| \le 1$. Then:

1. The grating lobes are the points $u_0 + k \lambda / d$ with $k$ a nonzero integer that lie in $[-1, 1]$.
2. A grating lobe exists exactly when $d \ge \lambda / (1 + |u_0|)$.
3. There is a look direction $u_0 \in (-1, 1)$ with a grating lobe exactly when $d > \lambda/2$. For broadside steering, $u_0 = 0$, a grating lobe exists exactly when $d \ge \lambda$.

*Proof.* Part 1 is Theorem 3: $\psi = 2\pi k$ means $(d/\lambda)(u - u_0) = k$.

For part 2, suppose $u_0 \ge 0$; the other case follows by the reflection $u \mapsto -u$. The candidate closest to $u_0$ on the side with more room is $u_0 - \lambda/d$, which lies in $[-1, 1]$ exactly when $u_0 - \lambda/d \ge -1$, that is $d(1 + u_0) \ge \lambda$. If this fails, then $\lambda/d > 1 + u_0$. Every candidate $u_0 - k\lambda/d$ with $k \ge 1$ is then below $-1$, and every candidate $u_0 + k\lambda/d$ with $k \ge 1$ is above $u_0 + (1 + u_0) \ge 1$. So no grating lobe exists.

For part 3, if $d > \lambda/2$, take $u_0 = \lambda/d - 1$, which lies in $(-1, 1)$ because $0 < \lambda / d < 2$. If $u_0 \ge 0$ then $d(1 + |u_0|) = \lambda$, so part 2 gives a lobe. If $u_0 < 0$ then $d > \lambda$, and $d(1 + |u_0|) \ge d > \lambda$, so part 2 again gives a lobe. Conversely, if $d \le \lambda/2$ and $|u_0| < 1$, then $d(1 + |u_0|) < 2d \le \lambda$, and part 2 gives no lobe. For $u_0 = 0$ the condition of part 2 is $d \ge \lambda$. $\blacksquare$

**Remarks.** At $d = \lambda/2$ the only look directions with a grating lobe are the two endfire directions $u_0 = \pm 1$, where the lobe is the opposite endfire direction. The time-domain form of lines L1 to L8 gives the same pattern for a tone of angular frequency $\omega$ per sample: if the true delays are $m D$ and the look delays are $m D_0$, the phase step between sensors is $\psi = \omega (D - D_0)$, and the output is the input tone scaled by $B$ of Theorem 3. The tests check this, the closed form against the defining sum, the peak against a brute-force grid, and the lobes in exact rational arithmetic.
