---
title: Each step of B-mode image formation does what it claims, in the discrete model of the page
proves: [correctness]
status: full
---

We prove the facts behind lines L1 to L12 of the main page. A line is a real vector $x = (x_0, \ldots, x_{n-1})$, its DFT is $X_k = \sum_q x_q e^{-2\pi i q k / n}$, and the inverse has the factor $1/n$. Indices of $X$ are taken modulo $n$. The weights of line L3 are $h_0 = 1$, $h_k = 2$ for $0 < k < n/2$, $h_{n/2} = 1$ when $n$ is even, and $h_k = 0$ for the other $k$.

**Theorem 1 (the real part of the analytic signal is the line).** Let $a = \operatorname{IDFT}(h X)$ (lines L2 and L3). Then $\operatorname{Re} a_q = x_q$ for every $q$, so the imaginary part is a discrete Hilbert transform of $x$ and $|a_q| \ge |x_q|$.

*Proof.* For any complex vector $y$ with DFT $Y$, the DFT of $\bar y$ is $k \mapsto \overline{Y_{-k}}$, so the DFT of $\operatorname{Re} y = (y + \bar y)/2$ is $(Y_k + \overline{Y_{-k}})/2$. Take $Y = h X$. Since $x$ is real, $\overline{X_{-k}} = X_k$, and $h$ is real, so $(Y_k + \overline{Y_{-k}})/2 = \frac{h_k + h_{-k}}{2} X_k$. Check $h_k + h_{-k} = 2$ for every $k$: for $k = 0$ it is $1 + 1$; for $n$ even and $k = n/2$ it is $1 + 1$; for $0 < k < n/2$ it is $2 + 0$; for $n/2 < k < n$ it is $0 + 2$. So the DFT of $\operatorname{Re} a$ is $X$, and $\operatorname{Re} a = x$. $\square$

**Theorem 2 (the envelope of a tone).** Let $x_q = A \cos(2\pi k_0 q / n + \varphi)$ with $A \ge 0$ and an integer $0 < k_0 < n/2$. Then $a_q = A e^{i(2\pi k_0 q/n + \varphi)}$ and the envelope of line L4 is the constant $A$.

*Proof.* $x_q = \frac{A}{2}(e^{i\varphi} e^{2\pi i k_0 q/n} + e^{-i\varphi} e^{-2\pi i k_0 q/n})$, so $X$ is $\frac{nA}{2} e^{i\varphi}$ at $k_0$, $\frac{nA}{2} e^{-i\varphi}$ at $n - k_0$, and $0$ elsewhere. Line L3 doubles the first and removes the second, because $n - k_0 > n/2$. The inverse DFT of $n A e^{i\varphi}$ at $k_0$ is the stated $a$. $\square$

For a pulse $g(t)\cos(2\pi f_0 t)$ with a smooth envelope whose spectrum does not reach the zero frequency, the envelope is close to $g$, but not exact: the line is finite and the DFT treats it as periodic. This is a heuristic, and the test measures an error of $6.4 \cdot 10^{-4}$ for a Gaussian envelope with $\sigma_t = 0.1$ us at $f_0 = 5$ MHz, $f_s = 40$ MHz and $n = 64$.

**Theorem 3 (time gain compensation).** Suppose the echo of a scatterer at depth $z$ has the amplitude $b\, 10^{-2\alpha z/20}$, with an attenuation of $\alpha$ dB per mm one way. Line L5 with the gain $G = 2\alpha$ dB per mm gives $b$, independent of $z$.

*Proof.* $b\, 10^{-2\alpha z/20} \cdot 10^{G z / 20} = b$ when $G = 2\alpha$. $\square$

In this model the two echoes of the test, at 5.3 and 5.9 mm with $\alpha = 5$ dB/mm, differ by $2 \cdot 5 \cdot 0.6 = 6$ dB before the gain and by nothing after. Real attenuation depends on the frequency and on the tissue, so a real gain curve is set by the user or by an adaptive rule.

**Theorem 4 (log compression).** Let $e_{\max}$ be the largest envelope value (line L6) and $D$ the dynamic range in dB. Line L9 maps $e$ to the gray level $\ell(e) = \lfloor 255 (d + D)/D + \tfrac12 \rfloor$ with $d = \max(-D, 20 \log_{10}(e/e_{\max}))$. Then:

1. $\ell$ depends only on the ratio $e/e_{\max}$, so scaling all envelopes by $c > 0$ gives the same image;
2. $\ell$ is nondecreasing in $e$, $\ell(e_{\max}) = 255$, and $\ell(e) = 0$ for every $e \le e_{\max} 10^{-D/20}$, including $e = 0$;
3. every level lies in $\{0, \ldots, 255\}$.

*Proof.* (1) Scaling by $c$ scales $e_{\max}$ by $c$ too. (2) The logarithm, the clipping of line L8, the affine map and the rounding are nondecreasing. At $e_{\max}$, $d = 0$ and $\ell = 255$. For $e \le e_{\max} 10^{-D/20}$, $d = -D$ and $\ell = 0$. (3) $d \in [-D, 0]$, so $255(d + D)/D \in [0, 255]$, and rounding keeps it in that range. $\square$

For example, with $D = 40$ dB, the ratios $1, 0.1, 0.01$ give $0, -20, -40$ dB and the levels $255$, $\lfloor 128.0 \rfloor = 128$ and $0$.

**Theorem 5 (scan conversion).** Let the polar samples be $f(\theta_k, r_q)$ on an evenly spaced grid of angles and depths. For a pixel inside the sector, line L12 returns a convex combination of the four nearest samples, and it returns $f(\theta, r)$ exactly when $f$ has the form $\alpha + \beta r + \gamma \theta + \delta r \theta$. Pixels outside the sector get $0$ (line L11).

*Proof.* The weights $(1-a)(1-b)$, $a(1-b)$, $(1-a)b$ and $ab$ with $a, b \in [0, 1]$ are nonnegative and sum to $1$. Bilinear interpolation on one cell reproduces the functions $1$, $r$, $\theta$ and $r\theta$: for $r$, the result is $(1-b) r_q + b r_{q+1} = r$ because $r = r_q + b (r_{q+1} - r_q)$, and the same holds for $\theta$; for $r \theta$ the weights factor into a product of the two one-dimensional cases. By linearity it reproduces their combinations. $\square$

**Theorem 6 (cost).** For $K$ lines of $n$ samples and $P$ output pixels, the envelopes cost $O(K n \log n)$ with a radix-2 FFT (the helper uses it when $n$ is a power of 2, and an $O(n^2)$ DFT otherwise), lines L5 to L9 cost $O(K n)$, and lines L10 to L12 cost $O(P)$.

*Proof.* Each step is a fixed number of operations per sample or per pixel, apart from the DFT pair of each line. $\square$
