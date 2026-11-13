---
title: The periodogram computes the defined estimate, its mean is the Fejér-smoothed spectrum, and on Gaussian white noise its variance does not shrink
proves: [correctness]
status: full
---

The notation is that of the page: a record $x[0], \dots, x[N-1]$, a window $w[0], \dots, w[N-1]$ with $U = \frac{1}{N}\sum_n w[n]^2 > 0$, a grid size $L \ge N$ and the bin frequencies $\omega_m = 2\pi m / L$ in radians per sample.

**Claim 1 (the output).** For every $m \in \{0, \dots, L-1\}$, the algorithm returns

$$P[m] = \frac{1}{NU}\left|\sum_{n=0}^{N-1} w[n]\,x[n]\, e^{-i\omega_m n}\right|^2.$$

*Proof.* Line L3 sets $a[n] = w[n]x[n]$ for $n < N$ and $a[n] = 0$ for $N \le n < L$. Line L4 computes the length-$L$ DFT $A[m] = \sum_{n=0}^{L-1} a[n] e^{-2\pi i m n / L}$; the FFT computes exactly this sum, as the [FFT](/fast-fourier-transform/) page proves. The terms with $n \ge N$ are zero, so $A[m] = \sum_{n<N} w[n]x[n] e^{-i\omega_m n}$. Line L5 divides $|A[m]|^2$ by $NU$, with $U$ from line L2. $\square$

**Claim 2 (the mean).** Let $x$ be a zero-mean WSS process with autocorrelation $r$ and the rectangular window. Then for every real $\omega$,

$$\mathbb{E}\,P(\omega) = \sum_{|k| < N}\left(1 - \frac{|k|}{N}\right) r[k]\, e^{-i\omega k}.$$

*Proof.* Expand $|\sum_n x[n]e^{-i\omega n}|^2 = \sum_{m,n} x[m]\overline{x[n]} e^{-i\omega(m-n)}$, take the expectation term by term, use $\mathbb{E}\,x[m]\overline{x[n]} = r[m-n]$, and count the $N - |k|$ pairs with $m - n = k$. This is claim 3 of the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/), which also shows that the right side tends to $S(\omega)$ when $\sum|r[k]| < \infty$. With a window, the same computation gives the weights $\frac{1}{NU}\sum_n w[n+k]w[n]$ in place of $1 - |k|/N$; they equal $1$ at $k = 0$. $\square$

**Claim 3 (the law on white noise).** Let $x[n]$ be independent real Gaussian variables with mean $0$ and variance $\sigma^2$, let the window be rectangular and $L = N$. For $0 < m < N/2$, $P[m]/\sigma^2$ has the exponential law with mean $1$, so $\mathbb{E}\,P[m] = \sigma^2$ and $\operatorname{Var} P[m] = \sigma^4$ for every $N$. For $m = 0$ and, when $N$ is even, $m = N/2$, $P[m]/\sigma^2$ has the chi-square law with one degree of freedom, and $\operatorname{Var} P[m] = 2\sigma^4$.

*Proof.* Write $A[m] = C - iD$ with $C = \sum_n x[n]\cos(\omega_m n)$ and $D = \sum_n x[n]\sin(\omega_m n)$. $C$ and $D$ are linear in the Gaussian vector $x$, so $(C, D)$ is jointly Gaussian with mean $0$, and

$$\operatorname{Var} C = \sigma^2 \sum_n \cos^2(\omega_m n), \qquad \operatorname{Var} D = \sigma^2 \sum_n \sin^2(\omega_m n), \qquad \operatorname{Cov}(C, D) = \sigma^2 \sum_n \cos(\omega_m n)\sin(\omega_m n).$$

For $0 < m < N/2$, $2\omega_m = 4\pi m/N$ is not a multiple of $2\pi$, so $\sum_{n<N} e^{2i\omega_m n} = 0$. Its real part gives $\sum \cos^2 - \sum \sin^2 = 0$, and its imaginary part gives $2\sum \cos\sin = 0$. Since $\sum \cos^2 + \sum \sin^2 = N$, both variances are $\sigma^2 N/2$, and $C$ and $D$ are uncorrelated, so independent. Hence $P[m] = (C^2 + D^2)/N = \frac{\sigma^2}{2}(Z_1^2 + Z_2^2)$ with $Z_1, Z_2$ independent standard normal. $Z_1^2 + Z_2^2$ is chi-square with two degrees of freedom, which is the exponential law with mean $2$; so $P[m]/\sigma^2$ is exponential with mean $1$ and variance $1$. For $m = 0$ and $m = N/2$, $\sin(\omega_m n) = 0$ for all $n$, so $D = 0$, $\operatorname{Var} C = \sigma^2 N$ and $P[m] = \sigma^2 Z_1^2$, whose variance is $2\sigma^4$. $\square$

**Consequence (not consistent).** An estimator $\hat S_N(\omega)$ is consistent when $\hat S_N(\omega) \to S(\omega)$ in probability. By claim 3, at a bin with fixed relative position $m/N = c \in (0, 1/2)$, the law of $P[m]$ is the same exponential law for every $N$, so $\Pr(|P[m] - \sigma^2| > \sigma^2/2) = 1 - e^{-1/2} + e^{-3/2} \approx 0.616$ for all $N$, and $P[m]$ does not converge to $S = \sigma^2$. The same computation for two bins $0 < m \ne m' < N/2$ shows that $P[m]$ and $P[m']$ are independent, because the four sums $C, D, C', D'$ are pairwise uncorrelated by the orthogonality of the DFT basis. So a larger $N$ gives more bins, each as noisy as before, and not a smoother curve. $\blacksquare$
