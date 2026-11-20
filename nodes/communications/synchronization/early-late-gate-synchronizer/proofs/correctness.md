---
title: The square-law early-late gate has the S-curve (beta/2) sin(2 pi d) sin(2 pi Delta) for raised cosine pulses, so the loop locks at the true delay
proves: [correctness]
status: full
---

Times are in symbol periods, $T = 1$. The matched filter output is $y(t) = e^{j\theta}\sum_m a_m g(t - m - \tau) + v(t)$, where $g$ is a raised cosine pulse with roll-off $0 < \beta < 1$, the data $a_m$ are independent with $E a_m = 0$ and $E|a_m|^2 = 1$, $\theta$ is any carrier phase and $v$ is noise independent of the data. Line L6 strobes at $t_k = k + \tau_k$. Lines L3 and L4 take the early sample $y(t_k - d)$ and the late sample $y(t_k + d)$, and line L5 forms $e_k = |y(t_k + d)|^2 - |y(t_k - d)|^2$. Write $\Delta = \tau - \tau_k$ for the timing error. The S-curve is the mean of $e_k$ over data and noise with $\tau_k$ held fixed.

**Lemma 1 (folded energy of the raised cosine).** For every real $x$,
$$\sum_{m \in \mathbb{Z}} g(x + m)^2 = 1 - \frac{\beta}{4} + \frac{\beta}{4}\cos(2\pi x).$$

*Proof.* The function $h = g^2$ is integrable and its Fourier transform is $H = G * G$, where $G(f)$ is the raised cosine spectrum. $G$ is $1$ for $|f| \le \frac{1-\beta}{2}$, $\frac12\bigl(1 + \cos\frac{\pi}{\beta}(|f| - \frac{1-\beta}{2})\bigr)$ for $\frac{1-\beta}{2} < |f| \le \frac{1+\beta}{2}$, and $0$ beyond. By the Poisson summation formula, $\sum_m h(x + m) = \sum_n H(n) e^{j2\pi n x}$. $H$ is zero for $|f| > 1 + \beta$, and $1 + \beta < 2$, so only $n \in \{-1, 0, 1\}$ remain. First, $H(0) = \int G(f)^2 df = (1 - \beta) + 2\int_0^\beta \frac14\bigl(1 + \cos\frac{\pi v}{\beta}\bigr)^2 dv = 1 - \beta + \frac{3\beta}{4} = 1 - \frac{\beta}{4}$. Second, $H(1) = \int G(f) G(1 - f) df$, and the product is nonzero only for $f = \frac12 + u$ with $|u| \le \frac{\beta}{2}$. There $G(\frac12 + u) = \frac12(1 - \sin\frac{\pi u}{\beta})$ and $G(\frac12 - u) = \frac12(1 + \sin\frac{\pi u}{\beta})$, so the product is $\frac14\cos^2\frac{\pi u}{\beta}$ and its integral is $\frac{\beta}{8}$. $H(-1) = H(1)$ because $G$ is even. So the sum is $1 - \frac{\beta}{4} + 2\cdot\frac{\beta}{8}\cos(2\pi x)$. $\square$

**Lemma 2 (mean energy at an offset).** Without noise, $E|y(t_k + x)|^2 = 1 - \frac{\beta}{4} + \frac{\beta}{4}\cos(2\pi(x - \Delta))$. With noise, a constant $E|v(t)|^2$ is added if $v$ is stationary.

*Proof.* $y(t_k + x) = e^{j\theta}\sum_m a_m g(k - m + x - \Delta)$. The factor $e^{j\theta}$ has modulus one. Expand $|\cdot|^2$ and take the mean: the cross terms $E[a_m \overline{a_{m'}}]$ are zero for $m \ne m'$, so the mean is $\sum_m g(k - m + x - \Delta)^2$. Lemma 1 with the integer shift $k$ gives the formula. The noise is independent of the data and has zero mean, so its cross terms with the signal vanish too. $\square$

**Theorem 1 (S-curve).** For every gate half-width $d$ and every carrier phase $\theta$,
$$E[e_k] = \frac{\beta}{2}\sin(2\pi d)\sin(2\pi\Delta).$$
The slope at $\Delta = 0$ is $K_D = \pi\beta\sin(2\pi d)$. It is largest at $d = \frac14$ and zero at $d = \frac12$.

*Proof.* By Lemma 2 with $x = d$ and $x = -d$, the constant terms and the noise power cancel, and
$$E[e_k] = \frac{\beta}{4}\bigl(\cos(2\pi(d - \Delta)) - \cos(2\pi(d + \Delta))\bigr) = \frac{\beta}{4}\cdot 2\sin(2\pi d)\sin(2\pi\Delta).$$
The derivative in $\Delta$ at $0$ is $\pi\beta\sin(2\pi d)$. $\square$

**Theorem 2 (lock points).** For $0 < d < \frac12$, the mean error is zero at $\Delta \in \frac12\mathbb{Z}$. The points $\Delta \in \mathbb{Z}$ are stable for the update $\tau_{k+1} = \tau_k + K_p e_k + s_k$ with $K_p > 0$, and the points $\Delta \in \frac12 + \mathbb{Z}$ are unstable. So, in the mean, the loop locks at $\tau_k = \tau$ modulo one symbol.

*Proof.* $\sin(2\pi\Delta)$ is zero exactly at $\Delta \in \frac12\mathbb{Z}$. Near $\Delta = 0$, $E[e_k] \approx K_D\Delta$ with $K_D > 0$, so a positive error (the receiver is early) gives a positive step of $\tau_k$, which reduces $\Delta$. Near $\Delta = \frac12$ the slope is $-K_D < 0$ and the step moves the error away. The linear analysis of the [phase-locked loop](/phase-locked-loop/), with the phase replaced by $2\pi\tau$, gives convergence for $0 < K_p K_D < 2$ in the first-order loop and for the Jury conditions in the second-order loop. $\square$

**Theorem 3 (exact lock on alternating data).** If $a_m = (-1)^m$ and there is no noise, then $e_k = \sin(2\pi d)\sin(2\pi\Delta)$ exactly, for every $k$, so $\tau_k = \tau$ is an exact fixed point of the loop.

*Proof.* By Poisson summation, $\sum_m (-1)^m g(t - m) = \sum_n G(n + \frac12) e^{j2\pi(n + \frac12)t}$. Only $n = 0$ and $n = -1$ fall in the band, and $G(\pm\frac12) = \frac12$ for every $\beta$, so $y(t) = \pm e^{j\theta}\cos(\pi(t - \tau))$. Then $|y(t_k + x)|^2 = \cos^2(\pi(k + x - \Delta)) = \frac12\bigl(1 + \cos(2\pi(x - \Delta))\bigr)$, and the same subtraction as in Theorem 1 gives the result. At $\Delta = 0$ the error is $0$, and with $s = 0$ lines L7 and L8 leave $\tau_k$ unchanged. $\square$

The S-curve is a closed form under assumptions: raised cosine pulses, independent zero-mean data, and $\tau_k$ constant while the mean is taken. With random data the error $e_k$ also has a part that depends on the data pattern and is not zero at $\Delta = 0$ (self-noise), so the loop jitters around the lock point even without noise. Theorem 3 shows that this part is zero for alternating data. The tests check Theorem 1 by averaging $e_k$ over 1280 random QPSK symbols at three offsets, and Theorem 3 to $10^{-9}$.
