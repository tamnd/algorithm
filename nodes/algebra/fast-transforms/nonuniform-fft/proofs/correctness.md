---
title: The Gaussian NUFFT of types 1 and 2 has error at most ε times the 1-norm of the input, in O(n log n + m log(1/ε)) operations
proves: [correctness, complexity]
status: full
---

**Setting.** Exact real arithmetic. Let $n \ge 1$, $0 < \varepsilon \le 1/2$, and $M, N, \tau$ as on the page: $M = \max(2, \lceil \frac{3}{2\pi} \ln(4/\varepsilon) \rceil)$, $N$ the least power of two with $N \ge \max(2n, 2M)$, $\tau = \pi M / (N(N - n/2))$. Put $h = 2\pi/N$, $s = \lfloor n/2 \rfloor$, $R = N/n \ge 2$, $G(x) = e^{-x^2/(4\tau)}$, and for points $t_j$ let $x_j = 2\pi (t_j \bmod 1)$. Write $e(t) = e^{-2\pi i t}$ and $A$ for the $m \times n$ matrix $A_{jk} = e(k t_j)$.

**Statement.** NUFFT-TYPE-1 returns $\tilde X$ with $|\tilde X_k - (A^{\mathsf T} c)_k| \le 4 e^{-2\pi M/3} \lVert c \rVert_1 \le \varepsilon \lVert c \rVert_1$ for $0 \le k < n$, and the type 2 procedure of the page returns $\tilde y$ with $|\tilde y_j - (A f)_j| \le \varepsilon \lVert f \rVert_1$. Both use $O(N \log N + mM)$ arithmetic operations and $O(mM + n)$ exponentials.

**Lemma 1 (the kernel).** The $2\pi$-periodic function $g_\tau(x) = \sum_{p \in \mathbb{Z}} G(x - 2\pi p)$ satisfies $g_\tau(x) = \sum_{\kappa \in \mathbb{Z}} \hat g(\kappa) e^{i\kappa x}$ for all $x$, with $\hat g(\kappa) = \sqrt{\tau/\pi}\, e^{-\tau\kappa^2}$, and the series converges absolutely.

*Proof.* The sum defining $g_\tau$ converges uniformly with all derivatives, so $g_\tau$ is smooth and periodic, and its Fourier series converges to it absolutely. Its coefficients are $\frac{1}{2\pi} \int_0^{2\pi} \sum_p G(x - 2\pi p) e^{-i\kappa x}\, dx = \frac{1}{2\pi} \int_{\mathbb{R}} G(x) e^{-i\kappa x}\, dx = \frac{1}{2\pi} \sqrt{4\pi\tau}\, e^{-\tau\kappa^2}$, by the Gaussian integral $\int_{\mathbb{R}} e^{-x^2/(4\tau)} e^{-i\kappa x}\, dx = \sqrt{4\pi\tau}\, e^{-\tau\kappa^2}$. $\square$

**Lemma 2 (the spread values).** For $0 \le j < m$ let $l_0 = \lfloor x_j/h \rfloor$ and $W_j = \{l_0 - M + 1, \ldots, l_0 + M\}$. Since $2M \le N$, the elements of $W_j$ are distinct modulo $N$. Line L5 adds to $v_{l}$, for $l \in [0, N)$, the amount $b_j \sum_{L \in W_j,\, L \equiv l} G(Lh - x_j)$. The full periodic kernel would add $b_j g_\tau(lh - x_j) = b_j \sum_{L \equiv l \ (N)} G(Lh - x_j)$, since $lh - 2\pi p = (l - pN)h$. So the omitted amount is $b_j \sum_{L \notin W_j,\, L \equiv l} G(Lh - x_j)$, and summed over $l$ its absolute value is at most

$$|b_j| \sum_{L \notin W_j} G(Lh - x_j) \le 2 |b_j| \sum_{q \ge 0} G((M + q) h) \le \frac{2 |b_j|\, G(Mh)}{1 - e^{-Mh^2/(2\tau)}}.$$

*Proof of the bounds.* Since $l_0 h \le x_j < (l_0 + 1) h$, the omitted $L = l_0 - M - q$ ($q \ge 0$) have $x_j - Lh \ge (M + q) h$, and the omitted $L = l_0 + M + 1 + q$ have $Lh - x_j > (M + q) h$. $G$ decreases in $|x|$, which gives the first inequality. For the second, $(M + q)^2 \ge M^2 + 2Mq$, so $G((M+q)h) \le G(Mh)\, (e^{-Mh^2/(2\tau)})^q$, and the geometric series sums. $\square$

**Lemma 3 (aliasing).** Let $v^{\mathrm{full}}_l = \sum_j b_j\, g_\tau(lh - x_j)$ and $V^{\mathrm{full}}_r = \sum_{l<N} v^{\mathrm{full}}_l\, \omega_N^{lr}$. Then for every integer $\kappa$,

$$V^{\mathrm{full}}_{\kappa \bmod N} = N \sum_{q \in \mathbb{Z}} \hat g(\kappa + qN) \sum_j b_j e^{-i(\kappa + qN) x_j}.$$

*Proof.* By Lemma 1, $v^{\mathrm{full}}_l = \sum_j b_j \sum_p \hat g(p) e^{ip(lh - x_j)}$. With $r = \kappa \bmod N$, $\omega_N^{lr} = e^{-i r l h}$, so $V^{\mathrm{full}}_r = \sum_j b_j \sum_p \hat g(p) e^{-ipx_j} \sum_{l<N} e^{i(p - r) l h}$, exchanging finite sums with an absolutely convergent one. The inner sum is a geometric sum of $N$-th roots of unity, equal to $N$ if $p \equiv r \equiv \kappa \pmod N$ and $0$ otherwise. Writing $p = \kappa + qN$ gives the claim. $\square$

**Type 1.** Fix $0 \le k < n$ and $\kappa = k - s$, so $|\kappa| \le n/2$. Since $s$ is an integer, $e(s t_j) = e^{-isx_j}$, so $b_j = c_j e^{-isx_j}$ (line L4) and $\sum_j b_j e^{-i\kappa x_j} = \sum_j c_j e^{-ikx_j} = X_k$. Line L6 computes $V = \mathrm{DFT}_N(v)$ and line L8 sets $\tilde X_k = V_{\kappa \bmod N} / (N \hat g(\kappa))$, because $\sqrt{\pi/\tau}\, e^{\tau\kappa^2} = 1/\hat g(\kappa)$. By Lemma 3 and linearity, $\tilde X_k - X_k = E_{\mathrm{alias}} - E_{\mathrm{trunc}}$, where

$$E_{\mathrm{alias}} = \sum_{q \ne 0} \frac{\hat g(\kappa + qN)}{\hat g(\kappa)} \sum_j b_j e^{-i(\kappa + qN) x_j}, \qquad E_{\mathrm{trunc}} = \frac{(V^{\mathrm{full}} - V)_{\kappa \bmod N}}{N \hat g(\kappa)}.$$

*Aliasing.* For $q \ne 0$, $(\kappa + qN)^2 - \kappa^2 = q^2N^2 + 2q\kappa N \ge |q| N (|q| N - n) \ge |q| N (N - n)$, using $|\kappa| \le n/2$. So $\hat g(\kappa + qN)/\hat g(\kappa) \le \rho^{|q|}$ with $\rho = e^{-\tau N (N - n)}$, and $|E_{\mathrm{alias}}| \le \lVert c \rVert_1 \cdot 2\rho/(1 - \rho)$, since $|b_j| = |c_j|$. Here $\tau N (N - n) = \pi M (R - 1)/(R - \frac12)$, which increases with $R$ and is $\frac23 \pi M$ at $R = 2$; so $\rho \le e^{-2\pi M/3} \le e^{-4\pi/3} < 0.016$ and $|E_{\mathrm{alias}}| \le 2.04\, e^{-2\pi M/3} \lVert c \rVert_1$.

*Truncation.* $|(V^{\mathrm{full}} - V)_r| \le \sum_l |v^{\mathrm{full}}_l - v_l|$, which by Lemma 2 is at most $2\lVert c \rVert_1 G(Mh)/(1 - e^{-Mh^2/(2\tau)})$. Now compute with the chosen $\tau$: $\frac{M^2h^2}{4\tau} = \pi M (1 - \frac{1}{2R})$, $\frac{Mh^2}{2\tau} = 2\pi (1 - \frac{1}{2R}) \ge \frac{3\pi}{2}$, and $\frac{1}{N \hat g(\kappa)} = \sqrt{\frac{\pi}{\tau}} \frac{e^{\tau\kappa^2}}{N} \le \sqrt{\frac{1 - 1/(2R)}{M}}\; e^{\tau n^2/4} \le \frac{1}{\sqrt 2} e^{\tau n^2/4}$ with $\frac{\tau n^2}{4} = \frac{\pi M}{4R(R - \frac12)}$. Hence $|E_{\mathrm{trunc}}| \le \frac{2}{\sqrt2\,(1 - e^{-3\pi/2})}\, e^{-\beta} \lVert c \rVert_1 \le 1.43\, e^{-\beta} \lVert c \rVert_1$, where $\beta = \pi M \bigl(1 - \frac{1}{2R} - \frac{1}{4R(R - 1/2)}\bigr)$. The bracket increases with $R$ and equals $\frac34 - \frac1{12} = \frac23$ at $R = 2$, so $e^{-\beta} \le e^{-2\pi M/3}$.

*Total.* $|\tilde X_k - X_k| \le (2.04 + 1.43)\, e^{-2\pi M/3} \lVert c \rVert_1 \le 4 e^{-2\pi M/3} \lVert c \rVert_1$. Since $M \ge \frac{3}{2\pi}\ln(4/\varepsilon)$, $e^{-2\pi M/3} \le \varepsilon/4$, so the error is at most $\varepsilon \lVert c \rVert_1$.

**Type 2.** Let $\Phi = \mathrm{diag}(e(s t_j))$, let $S$ be the $N \times m$ matrix with $S_{lj} = \sum_{L \in W_j,\, L \equiv l} G(Lh - x_j)$, $F$ the DFT matrix of order $N$, $F_{lr} = \omega_N^{lr}$, which is symmetric, and $D$ the $n \times N$ matrix with $D_{k, (k - s) \bmod N} = 1/(N \hat g(k - s))$ and zeros elsewhere (the indices $(k - s) \bmod N$ are distinct because $n \le N$). Type 1 computes $B c$ with $B = D F S \Phi$, and type 2, as defined on the page, computes $\Phi S^{\mathsf T} F D^{\mathsf T} f = B^{\mathsf T} f$, because $\Phi$ is diagonal and $F$ symmetric. Taking $c$ to be the $j$-th unit vector in the type 1 bound gives $|B_{kj} - A_{jk}| \le \varepsilon$ for all $j, k$. Hence $|(B^{\mathsf T} f - A f)_j| = |\sum_k (B_{kj} - A_{jk}) f_k| \le \varepsilon \lVert f \rVert_1$.

**Operation count.** Lines L3 to L5 do, per point, one complex exponential, $2M$ real exponentials, $2M$ products of a complex by a real number, $2M$ complex additions and $O(M)$ real operations for the arguments $Lh - x$: $O(mM)$ in all. Line L6 is a radix-2 FFT of length $N$, $\frac N2 \lg N$ complex multiplications and $N \lg N$ complex additions. Lines L7 and L8 do $n$ exponentials and $O(n)$ multiplications. Type 2 performs the same operations in reverse order. Since $M = O(\log(1/\varepsilon))$ and $N \le 4\max(n, M)$, the total is $O(n \log n + m \log(1/\varepsilon) + \log(1/\varepsilon) \log\log(1/\varepsilon))$, and the extra space is the grid of $N$ entries plus the output. $\blacksquare$
