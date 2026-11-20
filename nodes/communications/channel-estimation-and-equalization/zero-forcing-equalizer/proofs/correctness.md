---
title: The ZF equalizer forces the combined response to a unit pulse on its window, and its noise gain tends to the integral of 1/|H|^2
proves: [correctness]
status: full
---

The channel taps are $h_0, \ldots, h_{L-1}$, with $h_t = 0$ for $t < 0$ and $t \ge L$. The equalizer has the taps $c_0, \ldots, c_{N-1}$, and the received samples are $y[n] = \sum_l h_l\, x[n - l] + w[n]$ with $w[n] \sim \mathcal{CN}(0, N_0)$ independent. The equalizer output is

$$z[n] = \sum_{i=0}^{N-1} c_i\, y[n - i] = \sum_k g_k\, x[n - k] + \sum_i c_i\, w[n - i], \qquad g_k = \sum_{i=0}^{N-1} c_i\, h_{k - i}, \tag{1}$$

so $g = c * h$ is the combined response, with $N + L - 1$ terms $g_0, \ldots, g_{N+L-2}$. Let $\Delta$ be the decision delay, with $0 \le \Delta \le N + L - 2$, and let $s$ be the value of line L1.

**Lemma 1 (the window is valid).** $0 \le s \le L - 1$, the window $s, \ldots, s + N - 1$ lies in $0, \ldots, N + L - 2$, and it contains $\Delta$.

*Proof.* Line L1 clamps $s$ to $[0, L-1]$, so $s + N - 1 \le N + L - 2$. Let $u = \Delta - \lfloor (N-1)/2 \rfloor$. If $0 \le u \le L - 1$, then $s = u$ and $s \le \Delta \le s + N - 1$, because $0 \le \lfloor (N-1)/2 \rfloor \le N - 1$. If $u < 0$, then $s = 0 \le \Delta$ and $\Delta < \lfloor (N-1)/2 \rfloor \le N - 1$. If $u > L - 1$, then $s = L - 1 < \Delta$ and $\Delta \le N + L - 2 = s + N - 1$. $\square$

**Theorem 1 (zero forcing).** If the matrix $A$ of line L2 is invertible, the taps $c$ of line L4 give $g_\Delta = 1$ and $g_k = 0$ for every other $k$ in the window $s, \ldots, s + N - 1$. They are the only $N$ taps that do so.

*Proof.* By (1), $g_{s + k} = \sum_i h_{s + k - i}\, c_i = (A c)_k$ for $0 \le k < N$. Line L4 makes $A c = e$, where $e$ has a single 1 at index $\Delta - s$, which is in $0, \ldots, N-1$ by Lemma 1. So $g_{s+k} = 1$ for $s + k = \Delta$ and $0$ for the other $k$. Any $c'$ with the same forcing satisfies $A c' = e$, and so $c' = A^{-1} e = c$. $\square$

So the output is $z[n] = x[n - \Delta] + \sum_{k \notin W} g_k\, x[n-k] + \nu[n]$, where $W$ is the window, the middle sum is the residual ISI from the $L - 1$ indices outside the window, and $\nu[n] = \sum_i c_i w[n-i]$ is the filtered noise.

**Lemma 2 (noise enhancement).** $\nu[n]$ has mean zero and variance $N_0 \|c\|^2$.

*Proof.* The samples $w[n - i]$ for $i = 0, \ldots, N-1$ are independent with mean zero and variance $N_0$, so $E|\nu[n]|^2 = \sum_i |c_i|^2 E|w[n-i]|^2 = N_0 \|c\|^2$. $\square$

**Lemma 3 (when the system is solvable, delay 0).** If $s = 0$, then $A$ is lower triangular with $h_0$ on its diagonal, so it is invertible if and only if $h_0 \ne 0$. For $\Delta = 0$ the taps are the first $N$ coefficients of the power series of $1/H(z)$, where $H(z) = \sum_l h_l z^{-l}$:

$$c_0 = \frac{1}{h_0}, \qquad c_k = -\frac{1}{h_0} \sum_{l=1}^{\min(k, L-1)} h_l\, c_{k-l} \quad (1 \le k < N).$$

*Proof.* With $s = 0$, $A_{ki} = h_{k-i}$ is zero for $i > k$ and $h_0$ for $i = k$. Its determinant is $h_0^N$. Row $k$ of $A c = e$ reads $\sum_{l=0}^{\min(k, L-1)} h_l c_{k-l} = [k = 0]$, which is the stated recursion. The same recursion defines the coefficients $d_k$ of $D(z) = \sum_k d_k z^{-k} = 1/H(z)$, since $H(z) D(z) = 1$ means $\sum_l h_l d_{k-l} = [k = 0]$ for all $k \ge 0$. So $c_k = d_k$ for $k < N$. $\square$

For $h = (1, a)$, this gives $c_k = (-a)^k$, the combined response $g = (1, 0, \ldots, 0, -(-a)^N)$, and $\|c\|^2 = (1 - |a|^{2N})/(1 - |a|^2)$.

**Theorem 2 (the limit of the noise gain).** Let $\Delta = 0$ and let all zeros of $H(z)$ lie strictly inside the unit circle, with $h_0 \ne 0$ (a minimum-phase channel). Then, as $N \to \infty$, the residual ISI tends to 0 and

$$\|c\|^2 \to \frac{1}{2\pi} \int_{-\pi}^{\pi} \frac{d\omega}{|H(e^{j\omega})|^2}.$$

*Proof.* $H(z) = h_0 \prod_{r=1}^{L-1} (1 - \zeta_r z^{-1})$ with all $|\zeta_r| < 1$. Each factor $1/(1 - \zeta_r z^{-1}) = \sum_k \zeta_r^k z^{-k}$ has absolutely summable coefficients, and so does their product $D(z) = 1/H(z)$, with $|d_k| \le C \rho^k$ for some $C$ and any $\rho$ with $\max_r |\zeta_r| < \rho < 1$. By Lemma 3, $c_k = d_k$ for $k < N$, so $\|c\|^2 = \sum_{k<N} |d_k|^2 \to \sum_k |d_k|^2$. On the unit circle, $D(e^{j\omega}) = \sum_k d_k e^{-j \omega k} = 1/H(e^{j\omega})$, and Parseval's theorem gives $\sum_k |d_k|^2 = \frac{1}{2\pi}\int_{-\pi}^{\pi} |D(e^{j\omega})|^2 d\omega$. The residual ISI is $g_k = \sum_{i < N} d_i h_{k-i}$ for $N \le k \le N + L - 2$, and $|g_k| \le \sum_l |h_l|\, C \rho^{N - L + 1} \to 0$. $\square$

For other channels the same limit holds with a delay that grows with $N$: the zeros outside the unit circle need an anticausal inverse, which a delayed FIR filter approximates. If $H(e^{j\omega})$ has a zero on the unit circle, the integral diverges, and so does the noise gain of the ZF equalizer as $N$ grows.

**Remark (Lucky's theorem, cited).** Let $p$ be the index of the largest tap and define the initial distortion $D_0 = \sum_{l \ne p} |h_l| / |h_p|$. For odd $N$ and the delay $\Delta = p + (N-1)/2$, which puts the cursor under the center tap, the window of line L1 is centered on $\Delta$. Lucky proved that if $D_0 < 1$, this ZF equalizer minimizes the peak distortion $\sum_{k \ne \Delta} |g_k| / |g_\Delta|$ over all equalizers with $N$ taps. The proof uses the convexity of the peak distortion in $c$; see Lucky 1965 and Proakis and Salehi, Section 9.4-1. The tests check this optimality on random channels by perturbation, but this file does not prove it.

**Remark (the cost).** Line L2 builds $N^2$ entries, and the Gaussian elimination of line L4 costs $O(N^3)$, once per channel. Filtering costs $N$ complex multiplications per symbol.
