---
title: The Gardner detector has the S-curve A sin(2 pi Delta) with A = 4 sin(pi beta/2) / (pi (4 - beta^2)) for raised cosine pulses, and it does not depend on the carrier phase
proves: [correctness]
status: full
---

Times are in symbol periods, $T = 1$. The matched filter output is $y(t) = e^{j\theta}\sum_m a_m g(t - m - \tau) + v(t)$, with a raised cosine pulse $g$ of roll-off $0 < \beta < 1$, independent data with $E a_m = 0$ and $E|a_m|^2 = 1$, any carrier phase $\theta$, and noise $v$ independent of the data with zero mean. With $\tau_k$ held fixed, line L2 or line L9 gives the previous strobe $y(k - 1 + \tau_k)$, line L4 gives the midpoint $y(k - \frac12 + \tau_k)$ and line L5 the current strobe $y(k + \tau_k)$. Line L6 forms
$$e_k = \operatorname{Re}\bigl\{\overline{y(k - \tfrac12 + \tau_k)}\,\bigl(y(k - 1 + \tau_k) - y(k + \tau_k)\bigr)\bigr\}.$$
Write $\Delta = \tau - \tau_k$. $G(f)$ is the raised cosine spectrum, and on $|u| \le \frac{\beta}{2}$ it satisfies $G(\frac12 + u) = \frac12(1 - \sin\frac{\pi u}{\beta})$ and $G(\frac12 - u) = \frac12(1 + \sin\frac{\pi u}{\beta})$.

**Lemma 1 (phase invariance).** $e_k$ does not change when $y$ is replaced by $e^{j\phi}y$ for any real $\phi$.

*Proof.* $\overline{e^{j\phi}y_1}\,(e^{j\phi}y_2 - e^{j\phi}y_3) = e^{-j\phi}e^{j\phi}\,\overline{y_1}(y_2 - y_3)$. $\square$

**Lemma 2 (mean as a periodic sum).** Without noise, $E[e_k] = \sum_m p(m - \Delta)$, where $p(t) = g(t - \frac12)\bigl(g(t - 1) - g(t)\bigr)$.

*Proof.* By Lemma 1 we can take $\theta = 0$. Each of the three samples is $\sum_m a_m g(\cdot)$, with the arguments $k - m - \frac12 - \Delta$, $k - m - 1 - \Delta$ and $k - m - \Delta$. The cross terms with $m \ne m'$ have mean zero, and $E|a_m|^2 = 1$, so $E[e_k] = \sum_m p(k - m - \Delta)$. As $m$ runs over all integers, so does $n = k - m$, which gives $\sum_n p(n - \Delta)$. The result is real because $g$ is real. With noise, the extra term is $E[\overline{v(t_1)}(v(t_2) - v(t_3))]$ with $t_2 - t_1 = -\frac12$ and $t_3 - t_1 = \frac12$, which is zero for a stationary noise with an even real autocorrelation. $\square$

**Theorem 1 (S-curve).** $E[e_k] = A\sin(2\pi\Delta)$ with
$$A = \frac{4\sin(\pi\beta/2)}{\pi(4 - \beta^2)}.$$
For $\beta = 0.5$, $A = 0.2400843$ and the slope at lock is $K_D = 2\pi A = 1.508494$.

*Proof.* By Poisson summation, $\sum_m p(m - \Delta) = \sum_n P(n)e^{-j2\pi n\Delta}$, where $P$ is the Fourier transform of $p$. Each product of two shifted copies of $g$ has a transform supported on $|f| \le 1 + \beta < 2$, so only $n \in \{-1, 0, 1\}$ remain.

For $n = 0$: $P(0) = \int g(t - \frac12)g(t - 1)\,dt - \int g(t - \frac12)g(t)\,dt$. Both integrals equal the autocorrelation of $g$ at lag $\frac12$, because $g$ is even. So $P(0) = 0$.

For $n = 1$: let $q_s(t) = g(t - \frac12)g(t - \frac12 + s)$, so $p = q_{-1/2} - q_{1/2}$. Its transform at $1$ is $Q_s(1) = e^{-j\pi}\int G(f)G(1 - f)e^{j2\pi(1 - f)s}df$. The integrand is nonzero only for $f = \frac12 + u$, $|u| \le \frac{\beta}{2}$, where $G(f)G(1 - f) = \frac14\cos^2\frac{\pi u}{\beta}$. For $s = -\frac12$ the exponential is $-je^{j\pi u}$, and for $s = \frac12$ it is $je^{-j\pi u}$. So
$$P(1) = Q_{-1/2}(1) - Q_{1/2}(1) = \frac{j}{2}\int_{-\beta/2}^{\beta/2}\cos^2\frac{\pi u}{\beta}\cos(\pi u)\,du.$$
Write $\cos^2 x = \frac12(1 + \cos 2x)$. The constant part gives $\frac12\int_{-\beta/2}^{\beta/2}\cos(\pi u)\,du = \frac{1}{\pi}\sin\frac{\pi\beta}{2}$. For the other part, put $\alpha = \frac{2\pi}{\beta}$, so $\frac{\alpha\beta}{2} = \pi$. Then
$$\int_{-\beta/2}^{\beta/2}\cos(\alpha u)\cos(\pi u)\,du = \frac{\sin(\pi - \frac{\pi\beta}{2})}{\alpha - \pi} + \frac{\sin(\pi + \frac{\pi\beta}{2})}{\alpha + \pi} = \sin\frac{\pi\beta}{2}\Bigl(\frac{1}{\alpha - \pi} - \frac{1}{\alpha + \pi}\Bigr) = \frac{2\beta^2\sin(\pi\beta/2)}{\pi(4 - \beta^2)},$$
using $\alpha^2 - \pi^2 = \pi^2(4 - \beta^2)/\beta^2$. Half of this is the second part. Together,
$$\int_{-\beta/2}^{\beta/2}\cos^2\frac{\pi u}{\beta}\cos(\pi u)\,du = \frac{\sin(\pi\beta/2)}{\pi}\Bigl(1 + \frac{\beta^2}{4 - \beta^2}\Bigr) = \frac{4\sin(\pi\beta/2)}{\pi(4 - \beta^2)} = A,$$
so $P(1) = \frac{jA}{2}$. Since $p$ is real, $P(-1) = \overline{P(1)} = -\frac{jA}{2}$. The sum is $2\operatorname{Re}\{\frac{jA}{2}e^{-j2\pi\Delta}\} = A\sin(2\pi\Delta)$. $\square$

**Theorem 2 (lock points).** In the mean, the loop of lines L7 and L8 with $K_p > 0$ has stable points at $\Delta \in \mathbb{Z}$ and unstable points at $\Delta \in \frac12 + \mathbb{Z}$. The linear model of the [phase-locked loop](/phase-locked-loop/) with detector gain $K_D = 2\pi A$ applies near lock, for every carrier phase.

*Proof.* As for any sine S-curve: $A > 0$, the slope at $0$ is $2\pi A > 0$ and the slope at $\frac12$ is negative. Lemma 1 removes $\theta$. $\square$

**Theorem 3 (alternating data).** If $a_m = (-1)^m$ and there is no noise, then $e_k = \sin(2\pi\Delta)$ exactly.

*Proof.* As in the early-late gate proof, $y(t) = \pm e^{j\theta}\cos(\pi(t - \tau))$. With $c = \pi(k - \Delta)$, the samples are $\cos(c - \pi) = -\cos c$, $\cos(c - \frac{\pi}{2}) = \sin c$ and $\cos c$, so $e_k = \sin c\,(-2\cos c) = -\sin(2c) = -\sin(2\pi k - 2\pi\Delta) = \sin(2\pi\Delta)$. $\square$

The S-curve is a closed form under assumptions: raised cosine pulses, independent zero-mean data, stationary noise, and $\tau_k$ constant while the mean is taken. The detector also has self-noise from the data pattern, which is zero for alternating data (Theorem 3) and not zero for random data. The tests check Theorem 1 on 1280 random QPSK symbols at three offsets, and Theorem 3 to $10^{-5}$, the error of the truncated pulse sum in the test signal.
