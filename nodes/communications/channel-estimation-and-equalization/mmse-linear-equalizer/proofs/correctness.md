---
title: The MMSE linear equalizer solves the Wiener-Hopf equations, its error is N0 Es times a diagonal entry of an inverse, and its output is biased by 1 - J/Es
proves: [correctness]
status: full
---

The channel taps are $h_0, \ldots, h_{L-1}$, not all zero. The received samples are $y[n] = \sum_l h_l\, x[n-l] + w[n]$, where the symbols $x[n]$ are independent with mean zero and $E|x[n]|^2 = E_s$, and the noise samples $w[n] \sim \mathcal{CN}(0, N_0)$ are independent of each other and of the symbols. The equalizer has the taps $c_0, \ldots, c_{N-1}$, its output is $z[n] = \sum_{i=0}^{N-1} c_i\, y[n-i]$, and $z[n]$ estimates $x[n - \Delta]$ for a delay $0 \le \Delta \le N + L - 2$.

Let $u = (y[n], y[n-1], \ldots, y[n-N+1])^T$ and $s = (x[n], x[n-1], \ldots, x[n-N-L+2])^T$. Since $y[n-i] = \sum_j h_{j-i}\, x[n-j] + w[n-i]$, we have $u = H s + v$ with $H_{ij} = h_{j-i}$ (line L1), an $N \times (N+L-1)$ matrix, and $v$ the noise vector. Then $E[s s^H] = E_s I$, $E[v v^H] = N_0 I$ and $E[s v^H] = 0$. Write $f = \bar c$, so that $z[n] = f^H u$, and $g = H^T c$, which is the combined response $g = c * h$ because $g_j = \sum_i c_i h_{j-i}$.

**Lemma 1 (the error of any taps).** For every $c$,
$$J(c) = E|z[n] - x[n-\Delta]|^2 = E_s \|g - e_\Delta\|^2 + N_0 \|c\|^2 .$$

*Proof.* $z[n] - x[n - \Delta] = \sum_j (g_j - [j = \Delta])\, x[n-j] + \sum_i c_i\, w[n-i]$. All terms are independent with mean zero, so the variances add: $E_s$ times $|g_j - [j = \Delta]|^2$ for each symbol and $N_0 |c_i|^2$ for each noise sample. $\square$

**Lemma 2 (R is positive definite).** $R = E[u u^H] = E_s H H^H + N_0 I$ is Hermitian and positive definite when $N_0 > 0$, and also when $N_0 = 0$.

*Proof.* The formula follows from $u = Hs + v$ and the moments above. For a vector $a \ne 0$, $a^H R a = E_s \|H^H a\|^2 + N_0 \|a\|^2$. If $N_0 > 0$, this is positive. If $N_0 = 0$, we need $H^H a \ne 0$, that is, $H$ has full row rank. Let $p$ be the first index with $h_p \ne 0$. Row $i$ of $H$ is zero in the columns $j < i + p$ and has $h_p \ne 0$ in column $i + p$. These leading entries are in different columns and move to the right from row to row, so the rows are linearly independent. $\square$

**Theorem 1 (the Wiener solution).** Let $r = E[u\, \overline{x[n-\Delta]}] = E_s H e_\Delta$ (lines L2 and L3). The taps $c = \bar f$ with $R f = r$ (lines L4 and L5) are the unique minimizer of $J$, and the minimum is $J = E_s - r^H f$ (line L6).

*Proof.* Expand $J = E|f^H u - x[n-\Delta]|^2 = f^H R f - f^H r - r^H f + E_s$. Let $f_0 = R^{-1} r$, which exists by Lemma 2. Completing the square gives
$$J(f) = E_s - r^H f_0 + (f - f_0)^H R (f - f_0).$$
The last term is positive for $f \ne f_0$, because $R$ is positive definite. So $f_0$ is the unique minimizer and $J(f_0) = E_s - r^H f_0$, which is real because $r^H R^{-1} r$ is a Hermitian form. $\square$

The minimizer satisfies the orthogonality principle: the error $e = f^H u - x[n - \Delta]$ has $E[u\, \bar e] = R f - r = 0$, so the error is uncorrelated with every input sample of the filter.

**Theorem 2 (the closed form of J).** If $N_0 > 0$, then
$$J = N_0 E_s \left[ (E_s H^H H + N_0 I)^{-1} \right]_{\Delta\Delta}.$$

*Proof.* The push-through identity $H^H (E_s H H^H + N_0 I) = (E_s H^H H + N_0 I) H^H$ gives $H^H R^{-1} = M^{-1} H^H$ with $M = E_s H^H H + N_0 I$, which is positive definite. Then
$$J = E_s - E_s^2\, e_\Delta^T H^H R^{-1} H e_\Delta = E_s\, e_\Delta^T M^{-1} (M - E_s H^H H)\, e_\Delta = N_0 E_s\, e_\Delta^T M^{-1} e_\Delta. \qquad \square$$

**Theorem 3 (the bias and the unbiased SINR).** With the MMSE taps, $E[z[n] \mid x[n-\Delta]] = (1 - J/E_s)\, x[n-\Delta]$. The rest of the output, $z[n] - g_\Delta x[n-\Delta]$, is uncorrelated with $x[n-\Delta]$ and has variance $J (1 - J/E_s)$. So, if $J < E_s$, the scaled output $z[n] / (1 - J/E_s)$ is unbiased, and its signal to interference plus noise ratio is $E_s / J - 1$.

*Proof.* $z[n] = g_\Delta x[n-\Delta] + q$, where $q = \sum_{j \ne \Delta} g_j x[n-j] + \sum_i c_i w[n-i]$ is independent of $x[n-\Delta]$ and has mean zero. So $E[z \mid x[n-\Delta]] = g_\Delta x[n-\Delta]$. Now $g_\Delta = e_\Delta^T H^T c = f^H H e_\Delta = f^H r / E_s$. Since $f^H r = \overline{r^H f}$ and $r^H f = E_s - J$ is real, $g_\Delta = 1 - J/E_s$, a real number in $[0, 1]$. By Lemma 1 split into the $\Delta$ term and the rest, $J = E_s |1 - g_\Delta|^2 + E|q|^2 = J^2/E_s + E|q|^2$, so $E|q|^2 = J(1 - J/E_s)$. The ratio of signal power to the power of $q$ is $g_\Delta^2 E_s / E|q|^2 = (E_s - J)/J$. $\square$

So the MMSE equalizer shrinks the wanted symbol by the factor $1 - J/E_s$. For PSK and for BPSK decisions by sign this does not matter, but for QAM with several amplitude levels the slicer must divide by this factor first.

**Corollary 1 (the limits in N0).** As $N_0 \to 0$, the taps tend to $c = \overline{(H H^H)^{-1} H e_\Delta}$, the least-squares fit that minimizes $\|H^T c - e_\Delta\|^2 = \|g - e_\Delta\|^2$. As $N_0 \to \infty$, $N_0 f \to E_s H e_\Delta$, the time-reversed and conjugated channel, a matched filter for the symbol at the delay.

*Proof.* $f = (E_s H H^H + N_0 I)^{-1} E_s H e_\Delta$ is continuous in $N_0 \ge 0$ by Lemma 2, and at $N_0 = 0$ it is $(H H^H)^{-1} H e_\Delta$. The normal equations of $\min_c \|H^T c - e_\Delta\|^2$ are $\bar H H^T c = \bar H e_\Delta$, whose conjugate is $H H^H \bar c = H e_\Delta$, the same system. For the second limit, $N_0 f = (I + (E_s/N_0) H H^H)^{-1} E_s H e_\Delta \to E_s H e_\Delta$. $\square$

**Corollary 2 (MMSE against ZF).** The ZF equalizer with the same $N$ and $\Delta$ has the error $J(c_{ZF}) = E_s \|g_{ZF} - e_\Delta\|^2 + N_0 \|c_{ZF}\|^2 \ge J$, by Lemma 1 and Theorem 1. On a channel with a near spectral null, $\|c_{ZF}\|^2$ is large, and the gap is large.

**Remark (the infinite-length error, cited).** As $N \to \infty$ with a suitable delay, $J$ decreases to
$$J_\infty = \frac{1}{2\pi} \int_{-\pi}^{\pi} \frac{E_s N_0}{E_s |H(e^{j\omega})|^2 + N_0}\, d\omega ,$$
the error of the unconstrained Wiener filter $C(e^{j\omega}) = E_s \overline{H(e^{j\omega})} / (E_s |H(e^{j\omega})|^2 + N_0)$; see Proakis and Salehi, Section 9.4-2. For $h = (1, a)$ and $E_s = 1$, $|H|^2 = 1 + a^2 + 2a \cos\omega$, and the integral $\frac{1}{2\pi}\int d\omega / (A + B\cos\omega) = (A^2 - B^2)^{-1/2}$ gives $J_\infty = N_0 / \sqrt{(1 + a^2 + N_0)^2 - 4a^2}$. The tests check the finite $J$ against this value.

**Remark (the cost).** Line L2 forms $R$ from $H$ in $O(N^2 (N + L))$ operations, line L4 solves the system in $O(N^3)$, and line L6 costs $O(N)$, once per channel and delay. Trying all $N + L - 1$ delays costs $N + L - 1$ solves, or one inverse of $M$ by Theorem 2, whose diagonal gives every $J$ at once.
