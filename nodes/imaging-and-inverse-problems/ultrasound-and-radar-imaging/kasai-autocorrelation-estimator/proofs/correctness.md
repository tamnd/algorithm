---
title: The phase of the lag one autocorrelation gives the Doppler velocity of one scatterer exactly and the center of a narrow symmetric spectrum exactly, and the width formula is a second order approximation
proves: [correctness]
status: full
---

We prove the facts behind lines L1 to L5 of the main page. The slow time step is $T = 1/\mathrm{PRF}$, the IQ samples are complex numbers, and $\arg$ returns a value in $(-\pi, \pi]$. Let $\kappa = c \cdot \mathrm{PRF}/(4 \pi f_0)$, so line L3 is $v = \kappa \arg R_1$, and $f_D = 2 v f_0 / c$ is the Doppler frequency.

**Lemma 1 (the phase of one scatterer).** Under the model of the main page, a scatterer that moves toward the probe with constant axial velocity $v$ has the IQ samples $x[k] = a\, e^{i(\varphi_0 + 2 \pi f_D k T)}$ for a complex $a$ and a real $\varphi_0$.

*Proof.* The delay of pulse $k$ is $\tau_k = 2(z_0 - v k T)/c$. The demodulated sample is the echo amplitude times $e^{-i 2 \pi f_0 \tau_k} = e^{-i 4 \pi f_0 z_0 / c}\, e^{i 4 \pi f_0 v k T / c}$, and $4 \pi f_0 v / c = 2 \pi f_D$. The envelope of the pulse is assumed constant over the small shift $v k T$, so the amplitude $a$ does not depend on $k$. $\square$

**Theorem 1 (exact for one scatterer).** If $|v| < v_a = c \cdot \mathrm{PRF}/(4 f_0)$ and $a \ne 0$, then for any $G \ge 1$ and $N \ge 2$ lines L1 to L4 return $v$, $R_0 = |a|^2$ and $\sigma_v = 0$, when every gate holds the same scatterer velocity (with any amplitudes and phases per gate).

*Proof.* For gate $g$, $\overline{x_g[k]}\, x_g[k+1] = |a_g|^2 e^{i 2 \pi f_D T}$ for every $k$. So $R_1 = \bar A\, e^{i 2 \pi f_D T}$ and $R_0 = \bar A$, where $\bar A > 0$ is the mean of $|a_g|^2$. The condition $|v| < v_a$ is $|2 \pi f_D T| = 4 \pi f_0 |v| / (c \cdot \mathrm{PRF}) < \pi$, so $\arg R_1 = 2 \pi f_D T$ and $\kappa \arg R_1 = \frac{c\, \mathrm{PRF}}{4 \pi f_0} \cdot \frac{4 \pi f_0 v}{c\, \mathrm{PRF}} = v$. Also $|R_1| = R_0$, so line L4 gives 0. $\square$

If $|v| \ge v_a$, the same computation gives $\arg R_1 = 2 \pi f_D T - 2 \pi m$ for the integer $m$ that puts it in $(-\pi, \pi]$, so the estimate is $v - 2 m v_a$. This is the aliasing of the main page.

**Lemma 2 (invariances).** Let $R_1$ be computed from data $x_g$. (a) For data $c\, x_g$ with a complex $c \ne 0$, the value is $|c|^2 R_1$. (b) For the conjugate data $\overline{x_g}$, it is $\overline{R_1}$. (c) For the reversed data $x_g[N-1-k]$, it is $\overline{R_1}$.

*Proof.* (a) $\overline{c x}\, c y = |c|^2 \bar x y$. (b) $x \bar y = \overline{\bar x y}$. (c) Reversal turns the pair $(x[k], x[k+1])$ into $(x[k+1], x[k])$, and $\overline{x[k+1]}\, x[k] = \overline{\overline{x[k]}\, x[k+1]}$. $\square$

So the velocity does not depend on the gain, and conjugation or time reversal changes the sign of $v$ (when $\arg R_1 \ne \pi$).

**Theorem 2 (the center of a symmetric spectrum).** Let the slow time samples be a wide-sense stationary process with autocorrelation $R(m) = E[\overline{x[k]}\, x[k+m]]$ and a spectral measure $S$ on the circle $[-\mathrm{PRF}/2, \mathrm{PRF}/2)$, so that $R(m) = \int S(f)\, e^{i 2 \pi f m T}\, df$ (the Herglotz representation, which is the Wiener-Khinchin relation for sampled processes). Suppose that $S$ is symmetric about $\bar f$, that is $S(\bar f + u) = S(\bar f - u)$ with frequencies taken modulo PRF, that $S$ puts all its mass on $|u| < \mathrm{PRF}/4$, and that $S \ne 0$. Then $\arg R(1) = 2 \pi \bar f T$ modulo $2\pi$, and $\kappa \arg R(1)$ is the velocity of $\bar f$ when $|\bar f| < \mathrm{PRF}/2$.

*Proof.* Substitute $f = \bar f + u$, with $u$ in a period centered at 0:

$$R(1) = e^{i 2 \pi \bar f T} \int S(\bar f + u)\, e^{i 2 \pi u T}\, du = e^{i 2 \pi \bar f T} \int S(\bar f + u) \cos(2 \pi u T)\, du,$$

because the sine part is odd in $u$ and the measure is even in $u$. On the support, $|2 \pi u T| < \pi/2$, so the cosine is positive and the integral is a positive number. So the phase of $R(1)$ is $2 \pi \bar f T$. $\square$

The test checks Theorem 2 on a discrete spectrum with lines at $\bar f$, $\bar f \pm 200$, $\bar f \pm 450$ and $\bar f \pm 900$ Hz at PRF 5 kHz, to 1e-12.

**Lemma 3 (the estimate of R(1) is unbiased).** For a wide-sense stationary process, $E[R_1] = R(1)$ and $E[R_0] = R(0)$, where $R_0$ and $R_1$ are lines L1 and L2 over independent or dependent gates of the same process.

*Proof.* Each term $\overline{x_g[k]}\, x_g[k+1]$ has the mean $R(1)$, and line L2 divides the sum of the $G(N - 1)$ terms by their number. The same holds for line L1. $\square$

If the process is ergodic in the second moment (for example a Gaussian process with a continuous spectrum, or independent gates), $R_1 \to R(1)$ in probability as $G N \to \infty$, and since arg is continuous away from 0, the estimate converges to $\kappa \arg R(1)$. With Theorem 2, it converges to the velocity of the center $\bar f$. For finite $N$ the estimate has a variance and, because arg is nonlinear, a small bias; the main page labels these as statistical properties, not as exact facts.

**Lemma 4 (the phase slope at zero is the mean frequency).** If $S$ has a finite first moment and $R(0) > 0$, the continuous lag function $R(\tau) = \int S(f) e^{i 2 \pi f \tau} df$ satisfies

$$\frac{d}{d\tau} \arg R(\tau) \Big|_{\tau = 0} = 2 \pi \frac{\int f\, S(f)\, df}{\int S(f)\, df}.$$

*Proof.* $R(0) = \int S > 0$ is real and $R'(0) = i 2 \pi \int f S(f)\, df$. The derivative of $\arg R$ is $\operatorname{Im}(R'/R)$, which at 0 is $2 \pi \int f S / \int S$. $\square$

So $\arg R(T)/T$ is the slope of a chord of the phase curve, and it equals the slope at 0, the mean frequency, when the phase is linear in $\tau$. Theorem 2 is such a case. For a skewed spectrum the two differ by a term of order $T^2$ times the third central moment, so the estimate is close to the mean frequency only for narrow spectra.

**Lemma 5 (the width formula is second order).** Let $S$ have mean frequency $\bar f$ and variance $\sigma_f^2$, with finite fourth moment. Then

$$\frac{|R(T)|}{R(0)} = 1 - 2 \pi^2 \sigma_f^2 T^2 + O(T^3),$$

so $\frac{2}{T^2}\left(1 - \frac{|R(T)|}{R(0)}\right) = 4 \pi^2 \sigma_f^2 + O(T)$, and line L4 is $\kappa \sqrt{2(1 - |R_1|/R_0)} \approx c\, \sigma_f/(2 f_0)$, the velocity spread.

*Proof.* Write $R(T)/R(0) = e^{i 2 \pi \bar f T} \, E[e^{i 2 \pi U T}]$ with $U = f - \bar f$ distributed by $S / \int S$, so $E[U] = 0$ and $E[U^2] = \sigma_f^2$. A Taylor expansion gives $E[e^{i 2 \pi U T}] = 1 - 2 \pi^2 \sigma_f^2 T^2 + i\, O(T^3) + O(T^4)$, whose modulus is $1 - 2 \pi^2 \sigma_f^2 T^2 + O(T^3)$. Finally $\kappa \cdot 2 \pi \sigma_f T \cdot \mathrm{PRF} \cdot T = \frac{c}{4 \pi f_0} 2 \pi \sigma_f = \frac{c\, \sigma_f}{2 f_0}$. $\square$

Lemma 5 is an approximation for small $\sigma_f T$; for wide spectra line L4 underestimates the spread, and noise adds to it. The main page calls it an estimate, not an exact value.

**Theorem 3 (cost).** One pixel with $G$ gates of $N$ samples costs $O(G N)$ operations and $O(1)$ extra space; an $n \times n$ image costs $O(n^2 G N)$.

*Proof.* Lines L1 and L2 each visit every sample or every adjacent pair once. Lines L3 to L5 are a fixed number of operations. Only $R_0$ and $R_1$ are stored. $\square$
