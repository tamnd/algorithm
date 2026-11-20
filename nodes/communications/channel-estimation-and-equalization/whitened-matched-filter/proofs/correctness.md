---
title: The whitened matched filter gives the minimum-phase channel with white noise, and maximum likelihood on its output equals maximum likelihood on the received samples
proves: [correctness]
status: full
---

The channel taps are $h_0, \ldots, h_{L-1}$ with $h_0 \ne 0$ and $h_{L-1} \ne 0$, and $H(z) = \sum_l h_l z^{-l}$. The received block is $y = \mathbf{H} x + w$, where $x = (x_0, \ldots, x_{N-1})$, $\mathbf{H}$ is the $(N+L-1) \times N$ full convolution matrix with $\mathbf{H}_{kj} = h_{k-j}$, and $w \sim \mathcal{CN}(0, N_0 I)$. Write $n = N + L - 1$.

**Lemma 1 (the factor).** Write $H(z) = h_0 \prod_{i=1}^{L-1} (1 - \rho_i z^{-1})$, where $\rho_i$ are the roots of $h_0 z^{L-1} + \cdots + h_{L-1}$ (line L2). Let $\rho'_i = \rho_i$ if $|\rho_i| \le 1$ and $\rho'_i = 1/\bar\rho_i$ otherwise (line L3), and $F(z) = \gamma \prod_i (1 - \rho'_i z^{-1})$ with $\gamma = |h_0| \prod_{|\rho_i| > 1} |\rho_i|$ (line L4). Then $|F(e^{j\omega})| = |H(e^{j\omega})|$ for every $\omega$, all zeros of $F$ are in the closed unit disk, and the autocorrelations of $f$ and $h$ are equal: $R_f[k] = R_h[k]$ for every $k$.

*Proof.* For $|\rho| > 1$ and $|z| = 1$, $|1 - \rho z^{-1}| = |\rho| \cdot |\rho^{-1} - z^{-1}| = |\rho| \cdot |\bar\rho^{-1} - \bar z^{-1}|$, and $\bar z^{-1} = z$ on the unit circle, so this is $|\rho| \cdot |z| \cdot |\bar\rho^{-1} z^{-1} - 1| = |\rho| \cdot |1 - \bar\rho^{-1} z^{-1}|$. Multiplying over the factors gives $|F| = |H|$ on the circle. The autocorrelation $R[k]$ is the $k$-th Fourier coefficient of $|H(e^{j\omega})|^2$, so equal magnitudes give equal autocorrelations. $\square$

So $R(z) = H(z) H^*(1/z^*) = F(z) F^*(1/z^*)$, which is the spectral factorization of the folded spectrum. In particular, $\|f\|^2 = R[0] = \|h\|^2$.

**Lemma 2 (the matrices).** Let $\mathbf{F}$ be the $n \times N$ full convolution matrix of $f$. Then $\mathbf{H}^H \mathbf{H} = \mathbf{F}^H \mathbf{F}$.

*Proof.* The entry $(i, j)$ of $\mathbf{H}^H \mathbf{H}$ is $\sum_k \bar h_{k-i} h_{k-j}$, summed over all $k$ because the full convolution keeps every product. This is $R_h[i - j]$ (with $R[-k] = \overline{R[k]}$), and the same holds for $f$. Lemma 1 ends the proof. $\square$

**The filter.** Let $\mathbf{H}_s$ and $\mathbf{F}_s$ be the $n \times n$ lower triangular Toeplitz matrices of $h$ and $f$ (the convolution truncated to $n$ outputs). Line L5 computes $z = \mathbf{H}_s^H y$, the matched filter, with the samples after the block taken as 0. Lines L6 and L7 solve $\mathbf{F}_s^H y' = z$ by back substitution, from $k = n - 1$ down to 0. $\mathbf{F}_s^H$ is upper triangular with the diagonal $\bar f_0 = \gamma > 0$, so the solution exists and is unique.

**Theorem 1 (noiseless output).** If $w = 0$, then $y' = f * x$ exactly.

*Proof.* Pad $x$ with zeros to length $n$. Then $\mathbf{H}_s x = \mathbf{H} x = h * x$ and $\mathbf{F}_s x = f * x$, because the full convolutions have length $n$. We need $\mathbf{F}_s^H \mathbf{F}_s x = \mathbf{H}_s^H \mathbf{H}_s x$. Row $i$ of the right side is $\sum_{k=i}^{n-1} \bar h_{k-i} (h * x)_k = \sum_j x_j \sum_{k} \bar h_{k-i} h_{k-j}$. A product $\bar h_{k-i} h_{k-j}$ is nonzero only for $i \le k \le j + L - 1 \le n - 1$, so the inner sum runs over all $k$ and equals $R_h[i - j]$, the full autocorrelation. The same holds for $f$, and Lemma 1 gives $R_f = R_h$. So $\mathbf{F}_s^H (f * x) = z$, and uniqueness gives $y' = f * x$. $\square$

**Theorem 2 (the same maximum likelihood decisions).** For every $y$ and every candidate $x$ supported on the first $N$ entries,
$$\|y - h * x\|^2 - \|y' - f * x\|^2 = \|y\|^2 - \|y'\|^2,$$
which does not depend on $x$. So the sequence that minimizes $\|y' - f * x\|^2$ over any alphabet is the maximum likelihood sequence for $y$.

*Proof.* Expand both norms. The cross terms are $2\,\mathrm{Re}(x^H \mathbf{H}_s^H y)$ and $2\,\mathrm{Re}(x^H \mathbf{F}_s^H y')$, and $\mathbf{F}_s^H y' = z = \mathbf{H}_s^H y$, so they are equal. The quadratic terms are $x^H \mathbf{H}^H \mathbf{H} x$ and $x^H \mathbf{F}^H \mathbf{F} x$, equal by Lemma 2. $\square$

**Theorem 3 (white noise, for the infinite filter).** On an infinite sequence, the noise after the filter is $A(z) W(z)$ with $A(z) = H^*(1/z^*) / F^*(1/z^*)$, and $|A(e^{j\omega})| = 1$. So the output noise is white with variance $N_0$, and $y' = f * x + n'$ with $n' \sim \mathcal{CN}(0, N_0)$ i.i.d. If no zero of $H$ lies on the unit circle, $A$ is a stable anticausal filter.

*Proof.* The filter is $1/F^*(1/z^*)$ after $H^*(1/z^*)$. On the unit circle $|H^*(1/z^*)| = |H(z)|$ and the same for $F$, so $|A| = 1$ by Lemma 1. A linear filter with $|A| = 1$ maps white noise of spectrum $N_0$ to white noise of spectrum $N_0$, and a linear map of a circular Gaussian process is circular Gaussian. The zeros of $F^*(1/z^*)$ are at $1/\bar\rho'_i$, which lie outside the unit disk when $|\rho'_i| < 1$, so the anticausal inverse is stable. $\square$

For a finite block the back substitution starts at the end of the block, so the last samples carry an edge effect, which decays at the rate of the largest $|\rho'_i|$ away from the end. Theorem 2 needs no whiteness: it holds exactly for the finite block.

**Theorem 4 (minimum phase has the most energy first).** Among all $g$ with $|G| = |H|$ on the unit circle that are obtained by reflecting a subset of the zeros, the factor $f$ has the largest partial energy $\sum_{l=0}^{m} |g_l|^2$ for every $m$.

*Proof.* Compare a factor with the zero $\rho'$ ($|\rho'| < 1$) and the same factor with $1/\bar\rho'$, with the gain kept so that the magnitudes on the circle agree: $G_1(z) = C(z)(1 - \rho' z^{-1})$ and $G_2(z) = C(z)(\bar\rho' - z^{-1})$ up to a unit factor. Write $c$ for the taps of $C$, with $c_l = 0$ for $l < 0$. Then $(g_1)_l = c_l - \rho' c_{l-1}$ and $(g_2)_l = \bar\rho' c_l - c_{l-1}$, and
$$\sum_{l \le m} |(g_1)_l|^2 - \sum_{l \le m} |(g_2)_l|^2 = (1 - |\rho'|^2)\, |c_m|^2 \ge 0,$$
by a direct expansion where the cross terms cancel and the terms with $c_{l-1}$ telescope. Reflecting one zero at a time from any factor to $f$ never lowers a partial energy. $\square$
