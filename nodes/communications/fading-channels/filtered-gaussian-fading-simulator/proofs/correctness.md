---
title: The filtered Gaussian noise simulator outputs a circular Gaussian vector with power Omega and a circular autocorrelation set by the filter
proves: [correctness]
status: full
---

Let $F[0], \ldots, F[N-1]$ be the filter of lines L1 to L4, with $F[0] = 0$, $F[k] = F[N-k]$ for $1 \le k \le k_m$, and $F[k] = 0$ for $k_m < k < N - k_m$. The condition $k_m < N/2$ makes the bins $1, \ldots, k_m$ and $N - k_m, \ldots, N - 1$ disjoint, so the mirror step of line L4 is well defined, and $s = \sum_k F[k]^2 > 0$ because $F[1] > 0$. Let $G[0], \ldots, G[N-1]$ be independent $CN(0, 1)$, which means $E G[k] = 0$, $E|G[k]|^2 = 1$ and $E G[k]^2 = 0$. With $c = N\sqrt{\Omega/s}$, lines L5 to L7 give

$$h[n] = \frac{c}{N} \sum_{k=0}^{N-1} F[k]\, G[k]\, e^{j 2\pi k n/N}.$$

Indices of $h$ are taken modulo $N$.

**Lemma 1 (Gaussian output).** The vector $(h[0], \ldots, h[N-1])$ is circular complex Gaussian with mean 0.

*Proof.* It is a fixed linear map of the vector $G$, which is circular complex Gaussian, and a linear map preserves this class. Directly, $E h[n] = 0$ and $E[h[n]h[m]] = (c/N)^2 \sum_{k,l} F[k]F[l] e^{j2\pi(kn + lm)/N} E[G[k]G[l]] = 0$, because $E[G[k]G[l]] = 0$ for $k \ne l$ by independence and for $k = l$ by $E G^2 = 0$. A zero-mean complex Gaussian vector with zero pseudo-covariance is circular. $\square$

**Theorem 1 (autocorrelation).** For all $n$ and $d$,

$$E\big[h[n+d]\,\overline{h[n]}\big] = r[d] = \frac{\Omega}{s} \sum_{k=0}^{N-1} F[k]^2 \cos\Big(\frac{2\pi k d}{N}\Big),$$

which is real, does not depend on $n$, and satisfies $r[0] = \Omega$ and $r[N - d] = r[d]$.

*Proof.* $E[h[n+d]\overline{h[n]}] = (c/N)^2 \sum_{k,l} F[k]F[l]\, e^{j2\pi(k(n+d) - l n)/N}\, E[G[k]\overline{G[l]}]$. The expectation is 1 for $k = l$ and 0 otherwise, so the sum is $(c/N)^2\sum_k F[k]^2 e^{j2\pi kd/N}$, and $n$ cancels. Group the terms $k$ and $N - k$: they have equal $F^2$ and conjugate exponentials, so the imaginary parts cancel and each exponential can be replaced by its cosine. The terms $k = 0$ and, for even $N$, $k = N/2$ have $F = 0$. With $(c/N)^2 = \Omega/s$ this is $r[d]$. At $d = 0$ every cosine is 1, so $r[0] = \Omega$. Since $\cos(2\pi k(N - d)/N) = \cos(2\pi k d/N)$, $r[N-d] = r[d]$. $\square$

**Corollary (quadratures).** Write $h = X_c + jX_s$. Then $E[X_c[n+d]X_c[n]] = E[X_s[n+d]X_s[n]] = r[d]/2$ and $E[X_c[n+d]X_s[n]] = 0$.

*Proof.* Let $a = h[n+d]$ and $b = h[n]$. By Lemma 1, $E[ab] = 0$; by Theorem 1, $E[a\bar b] = r[d]$ is real. Adding and subtracting $E[a\bar b] = E[X_cX_c'] + E[X_sX_s'] + j(E[X_sX_c'] - E[X_cX_s'])$ and $E[ab] = E[X_cX_c'] - E[X_sX_s'] + j(E[X_sX_c'] + E[X_cX_s'])$, where the prime marks the sample at $n$, gives $E[X_cX_c'] = E[X_sX_s'] = r[d]/2$ and $E[X_cX_s'] = E[X_sX_c'] = 0$. $\square$

So each $h[n]$ is $CN(0, \Omega)$, and $|h[n]|$ has the Rayleigh distribution with $E|h[n]|^2 = \Omega$, for any $N$ and any filter.

**Remark (the edge bin).** For $1 \le k < k_m$, $F[k]^2$ is the sampled spectrum $1/(2\sqrt{1 - (k/(N f_m))^2})$, which is finite because $k < N f_m$. At the edge, $\int_{k_m-1}^{k_m} \frac{dk}{2\sqrt{1 - (k/k_m)^2}} = \frac{k_m}{2}\Big[\arcsin\frac{k}{k_m}\Big]_{k_m - 1}^{k_m} = \frac{k_m}{2}\Big(\frac\pi2 - \arcsin\frac{k_m - 1}{k_m}\Big)$, which is line L3; it is finite, and it is the integral of the spectrum, scaled to the band edge $k_m$, over the last bin. The sum $\sum_k F[k]^2 \cos(2\pi k d/N)$ is then a Riemann sum for $\int_{-f_D}^{f_D} S(f)\cos(2\pi f \tau)\, df$, which is proportional to $J_0(2\pi f_D\tau)$. The theorem above does not depend on how close this sum is to the integral; that closeness is measured, not proved.
