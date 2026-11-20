---
title: Kay's weights sum to one and are the best linear unbiased weights for the phase differences, so the estimate is exact without noise and reaches the Cramer-Rao bound in the high-SNR model
proves: [correctness]
status: full
---

The input is $r_t = A e^{j(\omega t + \phi)} + w_t$, $t = 0, \ldots, N - 1$, $N \ge 2$, with $|\omega| < \pi$, $A > 0$, and $w_t \sim \mathcal{CN}(0, N_0)$ white; $\mathrm{SNR} = A^2/N_0$. Lines L1 to L5 form $\hat\omega = \sum_{t=0}^{N-2} w_t d_t$ with $d_t = \arg(r_{t+1}\overline{r_t}) \in (-\pi, \pi]$ and
$$w_t = \frac{6(t + 1)(N - 1 - t)}{N(N^2 - 1)}.$$
Write $s = t + 1 \in \{1, \ldots, N - 1\}$ and $f(s) = s(N - s)$, so $w_t = \frac{6 f(s)}{N(N^2-1)}$.

**Lemma 1 (the weights sum to one).** $\sum_{t=0}^{N-2} w_t = 1$.

*Proof.* $\sum_{s=1}^{N-1} s(N - s) = N \cdot \frac{(N-1)N}{2} - \frac{(N-1)N(2N-1)}{6} = \frac{N(N-1)(3N - 2N + 1)}{6} = \frac{N(N^2-1)}{6}$. $\square$

**Theorem 1 (exact without noise).** If $w_t = 0$ for all $t$, then $\hat\omega = \omega$.

*Proof.* $r_{t+1}\overline{r_t} = A^2 e^{j\omega}$, and since $|\omega| < \pi$, $d_t = \omega$ for every $t$. By Lemma 1, $\hat\omega = \omega \sum_t w_t = \omega$. $\square$

**The high-SNR model.** Write $r_t = A e^{j(\omega t + \phi)}(1 + v_t)$ with $v_t = w_t e^{-j(\omega t + \phi)}/A \sim \mathcal{CN}(0, 1/\mathrm{SNR})$, white. Then $\arg r_t = \omega t + \phi + u_t$ modulo $2\pi$, with $u_t = \arg(1 + v_t) = \operatorname{Im} v_t + O(|v_t|^2)$. To first order, the $u_t$ are independent $\mathcal{N}(0, \sigma^2)$ with $\sigma^2 = \frac{1}{2\,\mathrm{SNR}}$. If no difference wraps, that is $|\omega + u_{t+1} - u_t| < \pi$ for all $t$, then
$$d_t = \omega + u_{t+1} - u_t,$$
so $d = \omega \mathbf{1} + e$ with $E e = 0$ and $\operatorname{cov} e = \sigma^2 C$, where $C$ is the $(N-1) \times (N-1)$ tridiagonal matrix with $2$ on the diagonal and $-1$ next to it. This is a linear model with one unknown $\omega$ and correlated noise.

**Theorem 2 (the weights are the BLUE).** In this model, $\hat\omega$ is the best linear unbiased estimator of $\omega$ from $d$, and its variance is
$$\operatorname{var}\hat\omega = \frac{12\sigma^2}{N(N^2 - 1)} = \frac{6}{\mathrm{SNR}\,N(N^2 - 1)},$$
which is the Cramer-Rao bound for $\omega$ with unknown amplitude and phase.

*Proof.* By the [Gauss-Markov theorem](/gauss-markov-theorem/) for correlated noise (generalized least squares), the BLUE of $\omega$ in $d = \omega\mathbf 1 + e$ is $\frac{\mathbf 1^\top C^{-1} d}{\mathbf 1^\top C^{-1}\mathbf 1}$, so its weight vector is the unique vector proportional to $C^{-1}\mathbf 1$ that sums to $1$. It is enough to show that $Cw$ is a constant vector. Set $f(0) = f(N) = 0$, which agrees with $f(s) = s(N - s)$. Row $s$ of $Cw$ is proportional to $2f(s) - f(s-1) - f(s+1)$, the negative second difference of $f$. As $f(s) = Ns - s^2$, the second difference is $-2$ for every $s$, so
$$(Cw)_t = \frac{6}{N(N^2-1)} \cdot 2 = \frac{12}{N(N^2-1)}$$
for every $t$, including the first and the last rows, where the missing neighbor is $f(0) = 0$ or $f(N) = 0$. With Lemma 1, $w$ is the BLUE weight vector. Its variance is $\sigma^2 w^\top C w = \sigma^2 \frac{12}{N(N^2-1)} \sum_t w_t = \frac{12\sigma^2}{N(N^2-1)}$. The [Cramer-Rao bound](/cramer-rao-bound/) for the frequency of a complex tone with unknown amplitude and phase in complex white Gaussian noise is $\frac{6}{\mathrm{SNR}\,N(N^2-1)}$, and $12\sigma^2 = 6/\mathrm{SNR}$. $\square$

**What this proves and what it does not.** Theorems 1 and 2 are exact statements; the claim that the true estimator has variance close to the bound is a closed form under assumptions: the first-order phase noise and no wrapped difference. Each $d_t$ wraps when $|u_{t+1} - u_t|$ is close to $\pi - |\omega|$, and the noise of $d_t$ has standard deviation $\sqrt2\,\sigma = 1/\sqrt{\mathrm{SNR}}$ for every $N$. So the probability of a wrap per difference depends on the per-sample SNR and on $\omega$, and does not fall as $N$ grows. Below a threshold SNR, wrapped differences add errors of size about $2\pi w_t$, and the mean square error rises far above the bound. This is a rule, and the tests measure it.

**Complexity.** Line L1 computes $N - 1$ weights, and lines L3 to L5 run $N - 1$ times with one complex product and one angle each. The total is $O(N)$ time; the weights can be computed on the fly, so the extra space is $O(1)$.
