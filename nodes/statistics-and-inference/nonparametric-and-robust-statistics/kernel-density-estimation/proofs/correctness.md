---
title: The kernel estimate is a density, its bias and variance expansions, the AMISE-optimal bandwidth, and the error of the binned FFT estimate
proves: [correctness]
status: full
---

**Setting.** $X_1, \ldots, X_n$ are independent with density $f$ on $\mathbb{R}$. The kernel $K$ is a symmetric function with $\int K = 1$, $\int u^2 |K(u)|\,du < \infty$ and $\int K^2 < \infty$. Write $\mu_2 = \int u^2 K(u)\,du$, $R(g) = \int g(u)^2\,du$, $K_h(t) = K(t/h)/h$, and
$$\hat f_h(x) = \frac{1}{nh}\sum_{i=1}^n K\!\left(\frac{x - X_i}{h}\right) = \frac1n \sum_{i=1}^n K_h(x - X_i).$$

## Part 1. The estimate is a density

**Lemma 1.** $\int \hat f_h(x)\,dx = 1$. If $K \ge 0$, then $\hat f_h \ge 0$, so $\hat f_h$ is a probability density.

*Proof.* For each $i$, the substitution $u = (x - X_i)/h$ gives $\int K_h(x - X_i)\,dx = \int K(u)\,du = 1$. The estimate is the mean of $n$ such functions. A sum of non-negative terms is non-negative. $\square$

The test file checks Lemma 1 without rounding for the Epanechnikov kernel. Between two consecutive points of the set $\{X_i \pm h\}$, the estimate is a polynomial of degree at most 2, and Simpson's rule is exact for such polynomials. So Simpson's rule on each piece, in exact rational arithmetic, must give exactly 1.

## Part 2. Bias and variance at a point

**Lemma 2 (bias).** $\mathbb{E}\,\hat f_h(x) = \int K(u)\,f(x - hu)\,du$. If $f''$ is bounded and continuous at $x$, then as $h \to 0$,
$$\mathbb{E}\,\hat f_h(x) - f(x) = \frac{h^2}{2}\,\mu_2\, f''(x) + o(h^2).$$

*Proof.* The terms are identically distributed, so $\mathbb{E}\,\hat f_h(x) = \mathbb{E}\,K_h(x - X_1) = \int K_h(x - t) f(t)\,dt$, and the substitution $t = x - hu$ gives the first claim. By Taylor's theorem with the Lagrange remainder, $f(x - hu) = f(x) - hu\,f'(x) + \tfrac12 h^2u^2 f''(\xi_u)$ for some $\xi_u$ between $x$ and $x - hu$. Integrate against $K(u)$: the first term gives $f(x)$ because $\int K = 1$, and the second gives 0 because $K$ is symmetric. So
$$\mathbb{E}\,\hat f_h(x) - f(x) - \frac{h^2}{2}\mu_2 f''(x) = \frac{h^2}{2}\int u^2 K(u)\,\big(f''(\xi_u) - f''(x)\big)\,du.$$
For each $u$, $\xi_u \to x$ as $h \to 0$, so the bracket goes to 0. It is bounded by $2\sup|f''|$, and $u^2|K(u)|$ is integrable, so by dominated convergence the integral goes to 0. $\square$

**Lemma 3 (variance).** If $f$ is bounded and continuous at $x$, then as $h \to 0$ and $nh \to \infty$,
$$\operatorname{Var}\hat f_h(x) = \frac{R(K)\,f(x)}{nh} + o\!\left(\frac{1}{nh}\right).$$

*Proof.* The terms are independent and identically distributed, so $\operatorname{Var}\hat f_h(x) = \frac1n\left(\mathbb{E}\,K_h(x - X_1)^2 - \big(\mathbb{E}\,K_h(x - X_1)\big)^2\right)$. The same substitution as in Lemma 2 gives
$$\mathbb{E}\,K_h(x - X_1)^2 = \frac1h \int K(u)^2 f(x - hu)\,du = \frac{R(K) f(x)}{h} + \frac1h\int K(u)^2\big(f(x - hu) - f(x)\big)\,du,$$
and the last integral goes to 0 by dominated convergence, because $f$ is bounded and $K^2$ is integrable. The squared mean is at most $(\sup f \int |K|)^2$, a constant, so after the division by $n$ it is $O(1/n) = o(1/(nh))$. $\square$

So the mean squared error at $x$ is
$$\mathrm{MSE}(x) = \frac{h^4}{4}\mu_2^2 f''(x)^2 + \frac{R(K) f(x)}{nh} + o\!\left(h^4 + \frac1{nh}\right).$$
The squared bias grows with $h$ and the variance falls with $h$. A consistent estimate needs $h \to 0$ and $nh \to \infty$.

## Part 3. The AMISE and the optimal bandwidth

Integrate the mean squared error over $x$. If $f''$ is square integrable and the remainders in Lemmas 2 and 3 can be integrated, which holds for example when $f'''$ is bounded and integrable and $K$ has a finite fourth moment (Wand and Jones 1995, Section 2.5), then
$$\mathrm{MISE}(h) = \int \mathrm{MSE}(x)\,dx = \mathrm{AMISE}(h) + o\!\left(h^4 + \frac1{nh}\right), \qquad \mathrm{AMISE}(h) = \frac{h^4}{4}\mu_2^2 R(f'') + \frac{R(K)}{nh},$$
where $\int f = 1$ gives the variance term. The integrability step is quoted, not proved here.

**Theorem 4.** Let $A = \frac14 \mu_2^2 R(f'') > 0$ and $B = R(K) > 0$. On $h > 0$, $\mathrm{AMISE}(h) = A h^4 + B/(nh)$ has exactly one minimum, at
$$h^* = \left(\frac{R(K)}{\mu_2^2\, R(f'')\, n}\right)^{1/5} = C\, n^{-1/5},$$
and the minimum value is
$$\mathrm{AMISE}(h^*) = \frac54 \left(\mu_2^2\, R(K)^4\, R(f'')\right)^{1/5} n^{-4/5}.$$

*Proof.* The derivative is $4Ah^3 - B/(nh^2)$. It is negative for small $h$, positive for large $h$, and it is 0 only at $h^5 = B/(4An)$. Its own derivative $12Ah^2 + 2B/(nh^3)$ is positive, so the function is strictly convex on $h > 0$, and the zero is the unique minimum. Since $4A = \mu_2^2 R(f'')$, this gives $h^*$. At the minimum, $B/(nh^*) = 4A(h^*)^4$, so $\mathrm{AMISE}(h^*) = 5A(h^*)^4 = 5A\,(B/(4An))^{4/5} = 5\cdot 4^{-4/5} A^{1/5} (B/n)^{4/5}$. Put in $A^{1/5} = 4^{-1/5}(\mu_2^2 R(f''))^{1/5}$; the powers of 4 combine to $4^{-1}$, which gives the stated value. $\square$

**Corollary 5 (the rate).** If $h = c\,n^{-a}$ with $a \ne 1/5$, then $\mathrm{AMISE}(h)$ is of larger order than $n^{-4/5}$: for $a < 1/5$ the term $A h^4$ is of order $n^{-4a}$, and for $a > 1/5$ the term $B/(nh)$ is of order $n^{a - 1}$. Both exponents are larger than $-4/5$. So the bandwidth must shrink like $n^{-1/5}$, and the best MISE falls like $n^{-4/5}$, slower than the $n^{-1}$ of a parametric fit.

For the standard normal $f$, $R(f'') = 3/(8\sqrt\pi)$, and with the Gaussian kernel ($\mu_2 = 1$, $R(K) = 1/(2\sqrt\pi)$) Theorem 4 gives $h^* = (4/(3n))^{1/5} \approx 1.06\,n^{-1/5}$. The test file compares this with the minimizer of the exact MISE, which has a closed form for normal data and a Gaussian kernel. The ratio of the two is measured, not proved: about 1.056 for $n = 100$, 1.010 for $n = 10^4$ and 1.002 for $n = 10^6$.

## Part 4. The binned FFT estimate

Lines L2 to L6 compute the estimate on the grid $g_k = \mathrm{lo} + k\delta$, $k = 0, \ldots, m-1$, $\delta = (\mathrm{hi} - \mathrm{lo})/(m-1)$. Linear binning gives each $X_i$ in $[g_j, g_{j+1}]$ the weight $1 - t$ at $g_j$ and $t$ at $g_{j+1}$, where $X_i = g_j + t\delta$; $c_j$ is the total weight at $g_j$. The binned estimate is
$$\tilde f(g_k) = \frac1{nh}\sum_{j=0}^{m-1} c_j\,K\!\left(\frac{(k - j)\delta}{h}\right).$$

**Lemma 6 (the FFT computes the binned sum).** Let $\kappa_l = K(l\delta/h)/(nh)$ for $-L \le l \le L$, stored at positions $0, \ldots, 2L$, and let both sequences be padded with zeros to a length $N \ge m + 2L$. Then entry $k + L$ of the cyclic convolution is $\sum_{|k - j| \le L} c_j \kappa_{k-j}$.

*Proof.* By the convolution theorem, lines L4 and L5 give the cyclic convolution $s_r = \sum_{j} c_j\,a_{(r - j) \bmod N}$, where $a$ is the padded kernel sequence. For $r = k + L$ and $0 \le j \le m - 1$, the index $r - j = (k - j) + L$ lies in $[-(m-1), m - 1 + 2L]$. When it is in $[0, 2L]$, the term is $c_j\kappa_{k-j}$. When it is in $[2L+1, m-1+2L]$, it is at most $N - 1$, so no wrap occurs and $a$ is 0 there. When it is negative, it wraps to $N + (r - j) \ge N - (m - 1) > 2L$, where $a$ is again 0. $\square$

So the FFT result equals the binned sum with the kernel cut off at $|u| \le L\delta/h$. For the Epanechnikov kernel, $L = \lceil h/\delta \rceil$ and nothing is cut off. For the Gaussian kernel, the code uses $L\delta \ge 8h$ (or the whole grid), and each cut term has $K \le \varphi(8) < 5.1 \times 10^{-15}$; the total of the weights is $n$, so the cut changes the result by less than $5.1 \times 10^{-15}/h$. The test compares the FFT result with a direct $O(m^2)$ sum and finds agreement within $10^{-12}$.

**Lemma 7 (binning error).** If all $X_i$ lie in $[\mathrm{lo}, \mathrm{hi}]$ and $K$ has a bounded second derivative, then for every grid point
$$|\tilde f(g_k) - \hat f_h(g_k)| \le \frac{\delta^2 \sup|K''|}{8h^3}.$$

*Proof.* Fix $k$ and let $\psi(t) = K((g_k - t)/h)$. Point $X_i = g_j + t_i\delta$ adds $(1 - t_i)\psi(g_j) + t_i\psi(g_{j+1})$ to $nh\,\tilde f(g_k)$, which is the linear interpolant of $\psi$ at $X_i$. It adds $\psi(X_i)$ to $nh\,\hat f_h(g_k)$. The error of linear interpolation on an interval of length $\delta$ is at most $\frac{\delta^2}{8}\sup|\psi''|$, and $\sup|\psi''| = \sup|K''|/h^2$. Add the $n$ errors and divide by $nh$. $\square$

For the Gaussian kernel, $\sup|K''| = |K''(0)| = 1/\sqrt{2\pi}$, and the test checks the bound for three grid sizes. The Epanechnikov kernel has a kink at $\pm 1$, so Lemma 7 does not apply to it as stated; its binning error is of order $\delta/h^2$ near the kinks of the kernel.

## Part 5. Cost

Line L1 costs $O(n)$ kernel evaluations, so $q$ points cost $O(nq)$. Binning costs $O(n)$, the kernel weights $O(L)$ with $L \le m - 1$, and three FFTs of length $N < 2(m + 2L) \le 6m$ cost $O(m \log m)$. The total for the grid is $O(n + m\log m)$.
