---
title: Without noise the L and R estimate equals nu for |nu| < 1/(L+1), each R(m) is unbiased for a tone in white noise, and outside the range the estimate aliases in a known way
proves: [correctness]
status: full
---

The input is $z_k = A e^{j(2\pi\nu k + \phi)} + w_k$, $k = 0, \ldots, N - 1$, with $A > 0$, $w_k$ independent with mean zero and variance $N_0$, and an integer $1 \le L \le N - 1$. Line L4 adds the sample autocorrelations $R(m) = \frac{1}{N - m}\sum_{k=m}^{N-1} z_k \overline{z_{k-m}}$ for $m = 1, \ldots, L$, and line L5 returns $\hat\nu = \frac{\arg S}{\pi(L+1)}$ with $S = \sum_{m=1}^{L} R(m)$ and $\arg$ in $(-\pi, \pi]$.

**Lemma 1 (each autocorrelation is unbiased).** $E R(m) = A^2 e^{j2\pi\nu m}$ for $1 \le m \le N - 1$, and without noise $R(m) = A^2 e^{j2\pi\nu m}$ exactly.

*Proof.* Write $s_k = A e^{j(2\pi\nu k + \phi)}$. Then $z_k\overline{z_{k-m}} = s_k\overline{s_{k-m}} + s_k\overline{w_{k-m}} + w_k\overline{s_{k-m}} + w_k\overline{w_{k-m}}$. The first term is $A^2 e^{j2\pi\nu m}$ for every $k$. The other terms have mean zero, because $w_k$ has mean zero and, for $m \ge 1$, $w_k$ and $w_{k-m}$ are independent. Averaging over the $N - m$ values of $k$ gives the claim. $\square$

**Lemma 2 (the sum of the noise-free terms).** For $\nu \notin \mathbb{Z}$, $\sum_{m=1}^{L} e^{j2\pi\nu m} = e^{j\pi\nu(L+1)}\,\frac{\sin(\pi\nu L)}{\sin(\pi\nu)}$.

*Proof.* The geometric sum is $e^{j2\pi\nu}\frac{e^{j2\pi\nu L} - 1}{e^{j2\pi\nu} - 1} = e^{j2\pi\nu}\frac{e^{j\pi\nu L}}{e^{j\pi\nu}}\cdot\frac{\sin(\pi\nu L)}{\sin(\pi\nu)}$, and $e^{j2\pi\nu + j\pi\nu L - j\pi\nu} = e^{j\pi\nu(L+1)}$. $\square$

**Theorem 1 (exact without noise inside the range).** If $w_k = 0$ for all $k$ and $|\nu| < \frac{1}{L+1}$, then $\hat\nu = \nu$.

*Proof.* By Lemma 1, $S = A^2\sum_{m=1}^{L} e^{j2\pi\nu m}$. If $\nu = 0$, $S = LA^2 > 0$ and $\hat\nu = 0$. Otherwise, by Lemma 2, $S = A^2 e^{j\pi\nu(L+1)} D$ with $D = \frac{\sin(\pi\nu L)}{\sin(\pi\nu)}$. Since $0 < |\pi\nu L| < |\pi\nu (L+1)| < \pi$, the numbers $\sin(\pi\nu L)$ and $\sin(\pi\nu)$ have the sign of $\nu$, so $D > 0$. Hence $\arg S \equiv \pi\nu(L+1) \pmod{2\pi}$, and since $|\pi\nu(L+1)| < \pi$, $\arg S = \pi\nu(L+1)$ exactly. Line L5 gives $\hat\nu = \nu$. $\square$

**Theorem 2 (aliasing outside the range).** Without noise, if $\frac{1}{L+1} < \nu < \frac1L$, then $\hat\nu = \nu - \frac{2}{L+1}$. If $\frac1L < \nu < \frac{2}{L+1}$ (possible when $L \ge 2$), then $\hat\nu = \nu - \frac{1}{L+1}$.

*Proof.* In the first case, $D > 0$ still, since $0 < \pi\nu L < \pi$, and $\pi < \pi\nu(L+1) < \pi + \frac{\pi}{L} \le 2\pi$, so $\arg S = \pi\nu(L+1) - 2\pi$. In the second case, $\pi < \pi\nu L < 2\pi$ and $0 < \pi\nu < \pi$, so $D < 0$ and $\arg S \equiv \pi\nu(L+1) + \pi \pmod{2\pi}$. As $\pi\nu(L+1) \in (\pi + \pi/L, 2\pi)$, the value $\pi\nu(L+1) + \pi - 2\pi = \pi\nu(L+1) - \pi$ lies in $(0, \pi)$, so $\hat\nu = \nu - \frac{1}{L+1}$. $\square$

So the range of the estimator is $|\nu| < \frac{1}{L+1}$: a larger $L$ averages more lags but narrows the range. Without the noise, this is all exact.

**With noise.** By Lemma 1, $S$ is an unbiased estimate of $A^2 e^{j\pi\nu(L+1)}D$, and $D \ge 1$ inside the range ($D$ is the Dirichlet kernel, which decreases from $L$ at $\nu = 0$ to $\sin(\pi L/(L+1))/\sin(\pi/(L+1)) = 1$ at the edge). The angle of an unbiased estimate is not an unbiased estimate of the angle, so the statement that the estimate has a small bias and a variance close to the [Cramer-Rao bound](/cramer-rao-bound/) for $L \approx N/2$ is not a theorem here: it is a closed form under assumptions in the paper of Luise and Reggiannini (a high-SNR linearization) and a measurement in the tests. The noise terms $w_k\overline{w_{k-m}}$ are products of two noise samples, which is why the estimator degrades at low SNR, and why the degradation is mild: the sum over $k$ and $m$ averages about $NL$ such products.

**Complexity.** Line L4 computes $L$ sums of at most $N - 1$ terms, $O(NL)$ time; for $L = N/2$ this is $O(N^2)$, or $O(N\log N)$ if all autocorrelations are computed with a zero-padded FFT. The extra space is $O(1)$ for the direct form.
