---
title: The FFT computes the Chebyshev interpolant, Clenshaw-Curtis has degree N (N+1 for even N) with positive weights, and the doubling driver terminates
proves: [correctness, error, termination]
status: full
---

We use the notation of the page: $n \ge 2$ nodes, $N = n - 1$, nodes $x_j = \cos(j\pi/N)$ for $j = 0, \ldots, N$ on $[-1, 1]$, $T_k(\cos\theta) = \cos k\theta$, and $\sum''$ is a sum whose first and last terms are halved. The general interval follows from the affine map $x \mapsto \frac{a + b}{2} + \frac{b - a}{2}x$, which preserves polynomial degree and multiplies the integral by $\frac{b - a}{2}$ (negative when $b < a$).

## Claim 1: discrete orthogonality

For every integer $m$,

$$\sum_{j=0}^{N}{}'' \cos\frac{jm\pi}{N} = \begin{cases} N & 2N \mid m, \\ 0 & \text{otherwise.}\end{cases}$$

Since $\cos\frac{(2N - j)m\pi}{N} = \cos\frac{jm\pi}{N}$, the left side is $\frac12\sum_{j=0}^{2N-1}\cos\frac{jm\pi}{N} = \frac12\operatorname{Re}\sum_{j=0}^{2N-1}\zeta^j$ with $\zeta = e^{im\pi/N}$, a $2N$-th root of unity. The geometric sum is $2N$ when $\zeta = 1$, that is $2N \mid m$, and $0$ otherwise. By $\cos A\cos B = \frac12(\cos(A + B) + \cos(A - B))$, for $0 \le k, l \le N$,

$$\sum_{j=0}^{N}{}'' \cos\frac{jk\pi}{N}\cos\frac{jl\pi}{N} = \begin{cases} N & k = l \in \{0, N\}, \\ N/2 & k = l, \ 0 < k < N, \\ 0 & k \ne l,\end{cases}$$

because $k + l$ and $k - l$ lie in $[-N, 2N]$, so $2N$ divides $k + l$ only if $k = l \in \{0, N\}$ and divides $k - l$ only if $k = l$.

## Claim 2: `dct1` returns the coefficients of the interpolant

Let $p = \sum_{k=0}^N a_k T_k$ be the polynomial of degree at most $N$ with $p(x_j) = f_j$ (it exists and is unique since the $N + 1$ nodes are distinct). Then $f_j = \sum_k a_k\cos\frac{jk\pi}{N}$. Multiplying by $\cos\frac{jl\pi}{N}$, summing with $\sum''$ and using Claim 1 gives

$$a_l = \frac{2\,\varepsilon_l}{N}\sum_{j=0}^{N}{}'' f_j\cos\frac{jl\pi}{N}, \qquad \varepsilon_0 = \varepsilon_N = \tfrac12,\ \varepsilon_l = 1 \text{ otherwise}.$$

Let $g = (f_0, \ldots, f_N, f_{N-1}, \ldots, f_1)$, of length $2N$. Its discrete Fourier transform is $G_l = \sum_{j=0}^{2N-1} g_j e^{-2\pi i jl/(2N)} = f_0 + (-1)^l f_N + 2\sum_{j=1}^{N-1}f_j\cos\frac{jl\pi}{N} = 2\sum''_j f_j\cos\frac{jl\pi}{N}$, which is real; the sine parts cancel between $j$ and $2N - j$. So $a_l = \varepsilon_l\,G_l/N$, which is what `dct1` computes (lines L3 to L5).

**The FFT.** For a power-of-two length, the iterative radix-2 transform applies the Cooley-Tukey splitting $X_k = E_k + e^{-2\pi i k/m}O_k$, $X_{k+m/2} = E_k - e^{-2\pi i k/m}O_k$ after a bit-reversal permutation, which is the standard proof. For other lengths, $jk = \frac12(j^2 + k^2 - (k - j)^2)$ gives $X_k = w_k\sum_j (x_j w_j)\,\overline{w_{k-j}}$ with $w_j = e^{-i\pi j^2/m}$, a convolution, which is computed exactly (in exact arithmetic) by zero-padding to a power of two at least $2m - 1$ and two radix-2 transforms (Bluestein's method). Reducing $j^2$ modulo $2m$ does not change $w_j$ and keeps the angle below $2\pi$.

## Claim 3: the moments

With $x = \cos\theta$, $\int_{-1}^1 T_k\,dx = \int_0^\pi\cos k\theta\sin\theta\,d\theta = \frac12\int_0^\pi(\sin(k + 1)\theta - \sin(k - 1)\theta)\,d\theta$. Since $\int_0^\pi\sin r\theta\,d\theta = \frac{1 - (-1)^r}{r}$ for $r \ne 0$ and $0$ for $r = 0$, this is $0$ for odd $k$ and $\frac{1}{k + 1} - \frac{1}{k - 1} = \frac{2}{1 - k^2}$ for even $k$ (including $k = 0$). So line L6 returns $\int_{-1}^1 p$ exactly, and the rule is the interpolatory rule on the Chebyshev extreme points.

## Claim 4: degree

Since $Q_n(f) = \int p$ and $p = f$ when $f$ is a polynomial of degree at most $N$, the rule has degree at least $N$. The nodes are symmetric ($x_{N-j} = -x_j$), and the weights are symmetric because the interpolatory weights are unique and reflecting $x \mapsto -x$ maps the rule to an interpolatory rule on the same nodes. So every odd monomial is integrated exactly, to $0$. When $N$ is even, $N + 1$ is odd, so the degree is at least $N + 1$.

For odd $N$ the degree is exactly $N$. The node polynomial is $\omega(x) = 2^{1-N}(x^2 - 1)U_{N-1}(x)$, monic of degree $N + 1$ and zero at every node, where $U_{N-1}(\cos\theta) = \sin N\theta/\sin\theta$. Then $x^{N+1} - \omega$ has degree at most $N$ and agrees with $x^{N+1}$ at the nodes, so $E_n(x^{N+1}) = \int\omega$. With $x = \cos\theta$, $\int_{-1}^1 (x^2 - 1)U_{N-1}\,dx = -\int_0^\pi\sin^2\theta\sin N\theta\,d\theta$. For odd $N \ge 3$, writing $\sin^2\theta = \frac12(1 - \cos 2\theta)$ and using Claim 3's integral, this is $-\bigl(\frac1N - \frac{N}{N^2 - 4}\bigr) = \frac{4}{N(N^2 - 4)} \ne 0$; for $N = 1$, $\int(x^2 - 1) = -\frac43$. So $E_n(x^{N+1}) = \frac{2^{3-N}}{N(N^2 - 4)}$ for odd $N \ge 3$. For even $N$ the failure at degree $N + 2$ is checked numerically in the test file.

## Claim 5: the weights, and their positivity

Substituting Claim 2 into $\sum_k a_k m_k$ with $m_k = \int T_k$ gives $Q_n(f) = \sum_j w_j f_j$ with

$$w_j = \frac{2\gamma_j}{N}\sum_{k=0}^{N}\varepsilon_k\,m_k\cos\frac{jk\pi}{N}, \qquad \gamma_0 = \gamma_N = \tfrac12,\ \gamma_j = 1 \text{ otherwise}.$$

`clenshaw_curtis_weights` computes this by the same FFT applied to the even extension of $(m_0, \ldots, m_N)$, whose transform is $2\sum_k\varepsilon_k m_k\cos\frac{jk\pi}{N}$. Only even $k = 2l$ contribute, $m_0 = 2$, and $m_{2l} = -\frac{2}{4l^2 - 1}$, so

$$w_j = \frac{c_j}{N}\Bigl(1 - \sum_{l=1}^{\lfloor N/2\rfloor}\frac{b_l}{4l^2 - 1}\cos\frac{2lj\pi}{N}\Bigr), \qquad c_j = 2\gamma_j,\quad b_l = \begin{cases}1 & 2l = N,\\ 2 & \text{otherwise},\end{cases}$$

the explicit formula of `clenshaw_curtis_weights_direct`. Since $\lvert\cos\rvert \le 1$, $0 < b_l \le 2$ and $\frac{2}{4l^2 - 1} = \frac{1}{2l - 1} - \frac{1}{2l + 1}$ telescopes,

$$w_j \ge \frac{c_j}{N}\Bigl(1 - \sum_{l=1}^{L}\frac{2}{4l^2 - 1}\Bigr) = \frac{c_j}{N}\cdot\frac{1}{2L + 1} > 0, \qquad L = \lfloor N/2\rfloor.$$

So all weights are positive and, by exactness on constants, sum to $2$. Consequently, if each $f_j$ is computed with error at most $\delta$, the computed sum differs from $Q_n(f)$ by at most $2\delta$ plus the rounding of the FFT. At $j = 0$ all cosines are $1$, and the sum gives $w_0 = \frac{1}{N^2 - 1}$ for even $N$ and $\frac{1}{N^2}$ for odd $N$.

## Claim 6: error for analytic integrands (cited, with proof sketch)

**Theorem (Trefethen, ATAP Theorem 19.3).** If $f$ is analytic in the open Bernstein ellipse $E_\rho$, $\rho > 1$, and $\lvert f\rvert \le M$ there, then for $N \ge 2$

$$\lvert I(f) - Q_n(f)\rvert \le \frac{64}{15}\,\frac{M\rho^{1-N}}{\rho^2 - 1}.$$

Sketch: the Chebyshev coefficients satisfy $\lvert c_k\rvert \le 2M\rho^{-k}$. The rule integrates $T_k$ exactly for $k \le N$; for $k > N$, $T_k$ agrees at the nodes with an aliased $T_{k'}$, $k' \le N$, and $\lvert I(T_k) - Q(T_k)\rvert$ is bounded by a constant multiple of $\frac{1}{k^2}$-type terms that sum to the stated factor. We do not reproduce the constant; the test file checks the inequality on the Runge function. The bound is proved; the observed rate on the Runge function, close to $\rho^{-2N}$ for moderate $N$ (the kink phenomenon of Weideman and Trefethen 2007), is a measurement.

## Claim 7: the doubling driver

The nodes nest: $\cos\frac{j\pi}{N} = \cos\frac{2j\pi}{2N}$, so the $(N + 1)$-point values are the even-indexed values of the $(2N + 1)$-point rule, and only the $N$ odd-indexed nodes are new. The driver starts at $N = 8$ and doubles; after the rule with $N$ it has used exactly $N + 1$ evaluations ($9 + 8 + 16 + \cdots + N/2$). Each iteration doubles $N$, and the loop returns "limit" before $2N + 1$ exceeds `max_n`, so it stops after at most $\log_2(\texttt{max\_n}/8)$ iterations. The stopping quantity $\lvert Q_{2N} - Q_N\rvert$ estimates the error of $Q_N$, and is used for $Q_{2N}$; that it bounds the true error is a heuristic, not a theorem. $\blacksquare$
