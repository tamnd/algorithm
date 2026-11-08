---
title: The transforms compute the interpolants, both Fejér rules have degree n-1 (n for odd n) with positive weights, and the doubling driver terminates
proves: [correctness, error, termination]
status: full
---

We work on $[-1, 1]$; the affine map $x \mapsto \frac{a + b}{2} + \frac{b - a}{2}x$ preserves polynomial degree and multiplies integrals by $\frac{b - a}{2}$, which is negative when $b < a$. The first rule has nodes $x_j = \cos\theta_j$, $\theta_j = (j + \frac12)\pi/n$, $j = 0, \ldots, n - 1$. The second rule has $N = n + 1$ and nodes $x_j = \cos\theta_j$, $\theta_j = j\pi/N$, $j = 1, \ldots, n$. All nodes lie in $(-1, 1)$, so neither rule evaluates $f$ at an endpoint.

## Claim 1: discrete orthogonality

**First rule.** For every integer $m$, $\sum_{j=0}^{n-1}\cos m\theta_j = 0$ unless $2n \mid m$. Indeed $\sum_j e^{im\theta_j} = e^{im\pi/(2n)}\sum_{j=0}^{n-1}e^{imj\pi/n}$; when $e^{im\pi/n} \ne 1$ the geometric sum equals $\frac{1 - (-1)^m}{1 - e^{im\pi/n}}$, and multiplying by $e^{im\pi/(2n)}$ gives $\frac{1 - (-1)^m}{e^{-im\pi/(2n)} - e^{im\pi/(2n)}} = \frac{1 - (-1)^m}{-2i\sin(m\pi/(2n))}$, which is purely imaginary. For $0 \le k, l \le n - 1$, $k + l \le 2n - 2$ and $\lvert k - l\rvert < n$, so by the product formula for cosines

$$\sum_{j=0}^{n-1}\cos k\theta_j\cos l\theta_j = \begin{cases} n & k = l = 0,\\ n/2 & k = l > 0,\\ 0 & k \ne l.\end{cases}$$

**Second rule.** For $1 \le k, l \le N - 1$, $\sum_{j=1}^{N-1}\sin k\theta_j\sin l\theta_j = \frac{N}{2}\delta_{kl}$. The terms $j = 0$ and $j = N$ vanish, so this sum is the halved-end sum $\sum''_{j=0}^{N}$ of $\frac12(\cos(k - l)\theta_j - \cos(k + l)\theta_j)$, and $\sum''_{j=0}^N\cos\frac{jm\pi}{N}$ is $N$ when $2N \mid m$ and $0$ otherwise (the identity proved on the [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) page). Here $0 < k + l < 2N$ and $\lvert k - l\rvert < N$.

## Claim 2: the transforms return the interpolants

**First rule.** Let $p = \sum_{k=0}^{n-1}a_kT_k$ interpolate $f$ at the $n$ distinct nodes. Then $f_j = \sum_k a_k\cos k\theta_j$, and Claim 1 gives $a_k = \frac{2\varepsilon_k}{n}\sum_j f_j\cos k\theta_j$ with $\varepsilon_0 = \frac12$, $\varepsilon_k = 1$ otherwise. Let $Y$ be the FFT of $(f_0, \ldots, f_{n-1}, f_{n-1}, \ldots, f_0)$, of length $2n$. The entry $f_j$ appears at positions $j$ and $2n - 1 - j$, so $Y_k = \sum_j f_j(e^{-ijk\pi/n} + e^{i(j+1)k\pi/n})$, and

$$e^{-ik\pi/(2n)}\,Y_k = \sum_j f_j\bigl(e^{-ik\theta_j} + e^{ik\theta_j}\bigr) = 2\sum_j f_j\cos k\theta_j.$$

So the code's $\operatorname{Re}(e^{-ik\pi/(2n)}Y_k)/n$, with the $k = 0$ entry halved, is $a_k$ (line L4).

**Second rule.** Let $p$ of degree at most $n - 1 = N - 2$ interpolate $f$ at the $n$ nodes. Since $U_{k-1}(\cos\theta)\sin\theta = \sin k\theta$ and $U_0, \ldots, U_{N-2}$ span the polynomials of degree at most $N - 2$, $p(\cos\theta)\sin\theta = \sum_{k=1}^{N-1}\beta_k\sin k\theta$ for unique $\beta_k$. At the nodes, $s_j := f_j\sin\theta_j = \sum_k\beta_k\sin k\theta_j$, and Claim 1 gives $\beta_k = \frac{2}{N}\sum_j s_j\sin k\theta_j$. Let $G$ be the FFT of the odd extension $(0, s_1, \ldots, s_{N-1}, 0, -s_{N-1}, \ldots, -s_1)$ of length $2N$. Then $G_k = \sum_j s_j(e^{-ijk\pi/N} - e^{ijk\pi/N}) = -2i\sum_j s_j\sin k\theta_j$, so $\beta_k = -\operatorname{Im}G_k/N$ (line L5).

The FFT itself (radix 2, and Bluestein's method for other lengths) is the one proved on the Clenshaw-Curtis page.

## Claim 3: the integrals, and the degree

For the first rule, $\int_{-1}^1 T_k = \frac{2}{1 - k^2}$ for even $k$ and $0$ for odd $k$, so line L6 returns $\int p$. For the second, $\int_{-1}^1 p\,dx = \int_0^\pi p(\cos\theta)\sin\theta\,d\theta = \sum_k\beta_k\frac{1 - (-1)^k}{k}$, which is $\sum_{k\text{ odd}}\frac{2\beta_k}{k}$, again line L6. In both cases $Q_n(f) = \int p$, so the rule is exact for polynomials of degree at most $n - 1$.

Both node sets are symmetric about $0$. The interpolatory weights are unique, and reflecting $x \mapsto -x$ maps the rule to an interpolatory rule on the same nodes, so the weights are symmetric and every odd monomial is integrated exactly. For odd $n$, $n$ is odd, so the degree is at least $n$. That it is not larger (the failure at $x^{n+1}$ for odd $n$ and at $x^n$ for even $n$) is checked numerically by the test file for $n \le 33$.

## Claim 4: the weights are positive

**First rule.** Substituting Claim 2 into $\sum_k a_k\int T_k$ gives

$$w_j = \frac{2}{n}\Bigl(1 - 2\sum_{l=1}^{\lfloor (n-1)/2\rfloor}\frac{\cos 2l\theta_j}{4l^2 - 1}\Bigr).$$

(The code sums to $\lfloor n/2\rfloor$; for even $n$ the extra term has $\cos n\theta_j = \cos((j + \frac12)\pi) = 0$.) With $L$ the upper limit, the telescoping identity $\sum_{l=1}^{L}\frac{2}{4l^2 - 1} = 1 - \frac{1}{2L + 1}$ gives $w_j \ge \frac{2}{n(2L + 1)} > 0$.

**Second rule.** Substituting Claim 2 into $\sum_{k\text{ odd}}\frac{2\beta_k}{k}$ gives

$$w_j = \frac{4\sin\theta_j}{N}\,S(\theta_j), \qquad S(\theta) = \sum_{l=1}^{L}\frac{\sin(2l - 1)\theta}{2l - 1}, \quad L = \lfloor N/2\rfloor.$$

Since $\sin\theta_j > 0$, it suffices that $S > 0$ on $(0, \pi)$. As $\sin(2l - 1)(\pi - \theta) = \sin(2l - 1)\theta$, $S$ is symmetric about $\frac\pi2$, so take $\theta \in (0, \frac\pi2]$. Now $S(0) = 0$ and $S'(\theta) = \sum_{l=1}^L\cos(2l - 1)\theta = \frac{\sin 2L\theta}{2\sin\theta}$. Split $(0, \frac\pi2]$ into the $L$ intervals $I_k = [\frac{(k-1)\pi}{2L}, \frac{k\pi}{2L}]$. On $I_k$, $\sin 2L\theta$ has sign $(-1)^{k-1}$, and since $\frac{1}{\sin\theta}$ decreases on $(0, \frac\pi2]$ while $\lvert\sin 2L\theta\rvert$ has the same shape on every $I_k$, the magnitudes $b_k = \lvert\int_{I_k}S'\rvert$ strictly decrease in $k$. So $A_k = S(\frac{k\pi}{2L}) = b_1 - b_2 + b_3 - \cdots \pm b_k$ is an alternating sum of decreasing positive terms, hence $A_k > 0$ for every $k \ge 1$. On an interval $I_k$ where $S$ increases, $S(\theta) \ge A_{k-1} > 0$ (or $S(\theta) > 0$ directly when $k = 1$); where $S$ decreases, $S(\theta) \ge A_k > 0$. So $S > 0$ on $(0, \pi)$ and every $w_j > 0$.

Positive weights summing to $2$ (exactness on constants) bound the effect of sample errors $\delta$ by $2\lvert h\rvert\delta$, and by Pólya's theorem the rules converge for every continuous $f$.

## Claim 5: error

The error for $f$ analytic in a Bernstein ellipse $E_\rho$ decays like $\rho^{-n}$, as for Clenshaw-Curtis; this is cited (Trefethen 2008; ATAP Chapter 19), not proved here. The rates for endpoint singularities on the page ($N^{-3}$ for $\sqrt x$, about $N^{-2}$ for $\log x$, $N^{-1}$ for $x^{-1/2}$) are measurements.

## Claim 6: the doubling driver

The second-rule nodes nest: $\cos\frac{j\pi}{N} = \cos\frac{2j\pi}{2N}$, so the old $n = N - 1$ values sit at the odd positions of the new rule with $2N - 1$ nodes, and only the $N$ even positions are new. Starting at $n = 7$, after the rule with $n$ nodes the driver has used exactly $n$ evaluations. Each iteration replaces $n$ by $2n + 1$, and the loop returns "limit" before $n$ exceeds `max_n`, so it terminates after at most $\log_2((\texttt{max\_n} + 1)/8)$ iterations. The stopping quantity $\lvert Q_{\text{new}} - Q_{\text{old}}\rvert$ estimates the error of the old rule; that it bounds the error of the new one is a heuristic. $\blacksquare$
