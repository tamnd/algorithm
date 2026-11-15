---
title: The ETFE is exact in periodic steady state, its noise error does not shrink, and smoothing averages it
proves: [correctness]
status: full
---

We work in exact real arithmetic, with $\cos$ and $e^{ix}$ as exact operations. Fix $N \ge 1$ and write $\omega_k = 2\pi k / N$ and, for a sequence $x$, $X_k = \sum_{t=0}^{N-1} x(t)\, e^{-i\omega_k t}$. Line L1 computes exactly these sums: by the direct formula, or by the radix-2 [FFT](/fast-fourier-transform/), which computes the same sums.

**Lemma 1 (delay in a periodic signal).** If $x$ is periodic with period $N$, the sequence $t \mapsto x(t - \ell)$ restricted to $t = 0, \ldots, N-1$ has the DFT $e^{-i\omega_k \ell} X_k$ for every integer $\ell$.

*Proof.* $\sum_{t=0}^{N-1} x(t - \ell)\, e^{-i\omega_k t} = e^{-i\omega_k \ell} \sum_{t=0}^{N-1} x(t - \ell)\, e^{-i\omega_k (t - \ell)}$. The summand $x(s)\, e^{-i\omega_k s}$ is periodic in $s$ with period $N$, because $e^{-i\omega_k N} = e^{-2\pi i k} = 1$, so the sum over the $N$ consecutive values $s = t - \ell$ equals the sum over $s = 0, \ldots, N-1$, which is $X_k$. $\square$

**Lemma 2 (periodic steady state).** Let $G$ be BIBO stable with impulse response $g$, so $\sum_\ell \lvert g_\ell \rvert < \infty$, let $u$ be periodic with period $N$ and let $y(t) = \sum_{\ell \ge 0} g_\ell\, u(t - \ell) + v(t)$. Then $Y_k = G(e^{i\omega_k})\, U_k + V_k$ for every $k$.

*Proof.* The input is bounded, so the series for $y(t)$ converges absolutely, and the finite sum over $t$ may be exchanged with the sum over $\ell$. By Lemma 1, $Y_k = \sum_\ell g_\ell\, e^{-i\omega_k \ell}\, U_k + V_k = G(e^{i\omega_k})\, U_k + V_k$, since $G(e^{i\omega}) = \sum_\ell g_\ell e^{-i\omega \ell}$. $\square$

**Lemma 3 (white noise on the grid).** If $v(0), \ldots, v(N-1)$ have zero mean, variance $\sigma^2$ and are uncorrelated, then $\mathbb{E}\, V_m \overline{V_n} = N \sigma^2$ if $m = n$ and $0$ if $m \ne n$, for $m, n \in \{0, \ldots, N-1\}$.

*Proof.* $\mathbb{E}\, V_m \overline{V_n} = \sum_{t, s} \mathbb{E}\, v(t) v(s)\, e^{-i\omega_m t + i\omega_n s} = \sigma^2 \sum_{t=0}^{N-1} e^{-i(\omega_m - \omega_n) t}$. For $m = n$ this is $N\sigma^2$. For $m \ne n$, $z = e^{-2\pi i (m - n)/N} \ne 1$ and $z^N = 1$, so the geometric sum $(1 - z^N)/(1 - z)$ is 0. $\square$

**Theorem.** Under the hypotheses of Lemma 2:

1. for every $k$ with $U_k \ne 0$, the raw value of L4 is $\hat G_k = G(e^{i\omega_k}) + V_k / U_k$; with $v = 0$ it equals $G(e^{i\omega_k})$;
2. if $u$ is fixed and $v$ is as in Lemma 3, $\mathbb{E} \lvert \hat G_k - G(e^{i\omega_k}) \rvert^2 = N\sigma^2 / \lvert U_k \rvert^2$;
3. if the denominator $D_k = \sum_{|j| \le \gamma} W_j \lvert U_{k+j} \rvert^2$ of L6 is positive, the smoothed value is $\tilde G_k = \sum_j \lambda_j \hat G_{k+j}$, a convex combination of the raw values with $\lambda_j = W_j \lvert U_{k+j} \rvert^2 / D_k$, the sum running over the $j$ with $U_{k+j} \ne 0$;
4. under the hypothesis of (2), $\tilde G_k = \sum_j \lambda_j G(e^{i\omega_{k+j}}) + E_k$ with $\mathbb{E}\, E_k = 0$ and $\mathbb{E} \lvert E_k \rvert^2 = N \sigma^2 \sum_j W_j^2 \lvert U_{k+j} \rvert^2 / D_k^2$.

*Proof.* (1) Divide the identity of Lemma 2 by $U_k$.

(2) By (1) the error is $V_k / U_k$, and by Lemma 3 $\mathbb{E} \lvert V_k \rvert^2 = N\sigma^2$.

(3) Every index $m = k + j$ is taken modulo $N$. If $U_m = 0$, the terms $W_j Y_m \overline{U_m}$ and $W_j \lvert U_m \rvert^2$ are both 0. If $U_m \ne 0$, $Y_m \overline{U_m} = \lvert U_m \rvert^2 \hat G_m$. Hence the numerator of L6 is $\sum_j W_j \lvert U_m \rvert^2 \hat G_m$, and dividing by $D_k$ gives the stated form. The weights $W_j = (1 + \cos(\pi j/(\gamma + 1)))/2$ are nonnegative and the $\lambda_j$ sum to 1, so the combination is convex.

(4) By Lemma 2 the numerator of L6 is $\sum_j W_j \big(G(e^{i\omega_m}) \lvert U_m \rvert^2 + V_m \overline{U_m}\big)$, so $E_k = \sum_j c_j V_{m_j}$ with $c_j = W_j \overline{U_{m_j}} / D_k$ and $m_j = (k + j) \bmod N$. Each $V_m$ has mean 0, so $\mathbb{E}\, E_k = 0$. Since $2\gamma + 1 \le N$, the indices $m_j$ are distinct, and Lemma 3 gives $\mathbb{E} \lvert E_k \rvert^2 = \sum_{j, j'} c_j \overline{c_{j'}}\, \mathbb{E}\, V_{m_j} \overline{V_{m_{j'}}} = N\sigma^2 \sum_j \lvert c_j \rvert^2$. $\blacksquare$

**Corollary (the Hann factor).** For $\gamma \ge 1$, $\sum_{|j| \le \gamma} W_j = \gamma + 1$ and $\sum_{|j| \le \gamma} W_j^2 = \frac34 (\gamma + 1)$. If $\lvert U_m \rvert^2 = c > 0$ for all $m$ in the window, then by (4) $\mathbb{E} \lvert E_k \rvert^2 = \frac{N\sigma^2}{c} \cdot \frac{3}{4(\gamma + 1)}$, which is $\frac{3}{4(\gamma + 1)}$ times the raw mean square error of (2).

*Proof.* Let $\alpha = \pi/(\gamma + 1)$. The $2\gamma + 2$ consecutive integers $j = -\gamma, \ldots, \gamma + 1$ cover one full period of $\cos(\alpha j)$, so $\sum_{j=-\gamma}^{\gamma+1} \cos(\alpha j) = 0$; removing the term $j = \gamma + 1$, which is $\cos \pi = -1$, gives $\sum_{|j| \le \gamma} \cos(\alpha j) = 1$. In the same way they cover two full periods of $\cos(2\alpha j)$, which has period $\gamma + 1 \ge 2$, so $\sum_{j=-\gamma}^{\gamma+1} \cos(2\alpha j) = 0$, and removing the term $\cos 2\pi = 1$ gives $\sum_{|j| \le \gamma} \cos(2\alpha j) = -1$. Then $\sum W_j = \frac12 (2\gamma + 1) + \frac12 = \gamma + 1$. With $\cos^2 x = (1 + \cos 2x)/2$, $\sum \cos^2(\alpha j) = \frac12 (2\gamma + 1) - \frac12 = \gamma$, so $\sum W_j^2 = \frac14 \big((2\gamma + 1) + 2 + \gamma\big) = \frac34 (\gamma + 1)$. With constant $\lvert U \rvert^2 = c$, (4) gives $N\sigma^2 c \sum W_j^2 / (c \sum W_j)^2$, which is the stated value. $\square$

The sums of $\cos(\alpha j)$ over a full period vanish because they are the real parts of sums of all the $(2\gamma + 2)$-th or $(\gamma + 1)$-th roots of unity, each of which is 0 when the number of roots is at least 2.
