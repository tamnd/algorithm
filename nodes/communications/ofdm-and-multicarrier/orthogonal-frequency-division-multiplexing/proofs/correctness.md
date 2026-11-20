---
title: "With a prefix of at least L - 1 samples, OFDM turns an L-tap channel into N independent one-tap channels"
proves: [correctness]
status: full
---

We use the unitary DFT pair of the page: $F[k, n] = e^{-j 2\pi k n / N} / \sqrt{N}$ for $k, n = 0, \ldots, N - 1$, $x = F^H X$ and $Y = F y$. The matrix $F$ is unitary, $F F^H = F^H F = I$, because $\sum_{n} e^{j 2\pi (k - k') n / N}$ is $N$ for $k = k'$ and $0$ otherwise (a geometric sum of $N$-th roots of unity). The channel has the taps $h[0], \ldots, h[L-1]$ and the frequency response $H[k] = \sum_{l=0}^{L-1} h[l]\, e^{-j 2\pi k l / N}$, the unnormalized DFT of the taps padded to length $N$. Indices of $x$ are taken modulo $N$.

Line L1 gives $x = F^H X$. Line L2 sends the $N + N_{cp}$ samples $s[i] = x[(i - N_{cp}) \bmod N]$ for $i = 0, \ldots, N + N_{cp} - 1$. The channel output is

$$r[i] = \sum_{l=0}^{L-1} h[l]\, s[i - l] + w[i], \tag{1}$$

where $s[i - l]$ for $i - l < 0$ is a sample of the previous symbol, and $w[i]$ are independent $\mathcal{CN}(0, N_0)$ samples. Line L3 keeps $y[n] = r[N_{cp} + n]$ for $n = 0, \ldots, N - 1$, and line L4 computes $Y = F y$.

**Lemma 1 (the prefix makes the convolution circular).** If $N_{cp} \ge L - 1$, then for $n = 0, \ldots, N - 1$

$$y[n] = \sum_{l=0}^{L-1} h[l]\, x[(n - l) \bmod N] + w[N_{cp} + n].$$

*Proof.* In (1) with $i = N_{cp} + n$, the index $i - l = N_{cp} + n - l$ is at least $N_{cp} - (L - 1) \ge 0$, so every sample that reaches $y[n]$ belongs to the current symbol, and none belongs to the previous one. By the definition of line L2, $s[N_{cp} + m] = x[m \bmod N]$ for every $m$ with $-N_{cp} \le m \le N - 1$. Here $m = n - l \ge -(L - 1) \ge -N_{cp}$, so $s[i - l] = x[(n - l) \bmod N]$. $\square$

**Lemma 2 (the DFT turns circular convolution into products).** Let $c[n] = \sum_{l=0}^{L-1} h[l]\, x[(n - l) \bmod N]$ with $L \le N$. Then $(F c)[k] = H[k]\, (F x)[k]$ for every $k$.

*Proof.*

$$(F c)[k] = \frac{1}{\sqrt N} \sum_{n=0}^{N-1} \sum_{l=0}^{L-1} h[l]\, x[(n - l) \bmod N]\, e^{-j 2\pi k n / N}.$$

Write $e^{-j 2\pi k n / N} = e^{-j 2\pi k l / N}\, e^{-j 2\pi k (n - l) / N}$ and exchange the sums. For a fixed $l$, the map $n \mapsto (n - l) \bmod N$ is a bijection of $\{0, \ldots, N - 1\}$, and $e^{-j 2\pi k (n - l)/N}$ depends only on $(n - l) \bmod N$. So the inner sum over $n$ is $\sqrt N\, (F x)[k]$, and the outer sum gives $H[k]\, (F x)[k]$. $\square$

**Lemma 3 (white noise stays white).** If $v$ has independent $\mathcal{CN}(0, N_0)$ entries, then $V = F v$ has independent $\mathcal{CN}(0, N_0)$ entries.

*Proof.* $V$ is a linear map of a circularly symmetric Gaussian vector, so it is circularly symmetric Gaussian with zero mean and covariance $F (N_0 I) F^H = N_0 I$. Uncorrelated jointly Gaussian entries are independent. $\square$

**Theorem.** If $N_{cp} \ge L - 1$, lines L1 to L4 give, for every subcarrier $k$,

$$Y[k] = H[k]\, X[k] + W[k],$$

with $W[0], \ldots, W[N-1]$ independent and $\mathcal{CN}(0, N_0)$. Line L6 returns $\hat X[k] = X[k] + W[k] / H[k]$ for each $k$ with $H[k] \ne 0$. Without noise, $\hat X = X$ exactly.

*Proof.* By Lemma 1, $y = c + v$ with $c$ the circular convolution of $h$ and $x$ and $v[n] = w[N_{cp} + n]$. By linearity and Lemma 2, $Y[k] = H[k]\, (F x)[k] + (F v)[k]$, and $F x = F F^H X = X$. The samples $w[N_{cp}], \ldots, w[N_{cp} + N - 1]$ are independent $\mathcal{CN}(0, N_0)$, so Lemma 3 applies to $W = F v$. Line L5 computes $H[k]$ by the same sum, so line L6 divides by the exact gain. $\blacksquare$

**Remarks.**

- Energy. Because $F$ is unitary, $\sum_n |x[n]|^2 = \sum_k |X[k]|^2$ (Parseval for this pair). With $E|X[k]|^2 = E_s$ for every $k$, each time sample has mean energy $E_s$, and subcarrier $k$ sees the SNR $|H[k]|^2 E_s / N_0$. With the unnormalized pair, $W[k]$ would have variance $N N_0$ and the transmit samples energy $E_s / N$; the SNR per subcarrier is the same.
- The prefix condition is sufficient, not necessary for a given channel. If the last taps are zero, the condition only needs the index of the last nonzero tap. If $N_{cp} < L - 1$, Lemma 1 fails: $y[n]$ for $n < L - 1 - N_{cp}$ contains samples of the previous symbol, and $y$ is no longer a circular convolution, so the subcarriers interfere. The tests show an error above $10^{-3}$ for $N_{cp} = 2$ and $3$ with five taps.
- The rate cost of the prefix is the factor $N / (N + N_{cp})$, because $N + N_{cp}$ samples carry $N$ symbols.
