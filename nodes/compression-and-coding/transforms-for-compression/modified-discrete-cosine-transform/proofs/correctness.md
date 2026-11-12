---
title: Time domain aliasing cancels, the analysis keeps energy, and the fold and FFT compute the MDCT
proves: [correctness]
status: full
---

Fix $N \ge 1$. Let $C$ be the $N \times 2N$ matrix with $C_{kn} = \cos\big(\frac{\pi}{N}(n + \frac12 + \frac N2)(k + \frac12)\big)$, let $J$ be the $N \times N$ reversal matrix, $(Ja)[i] = a[N-1-i]$, and let $W = \operatorname{diag}(W_1, W_2)$ be the diagonal matrix of the window, with $W_1 = \operatorname{diag}(w[0], \dots, w[N-1])$ and $W_2 = \operatorname{diag}(w[N], \dots, w[2N-1])$. Then MDCT$(x) = \sqrt{2/N}\, C W x$ and IMDCT$(X) = \sqrt{2/N}\, W C^{\mathsf T} X$.

**Lemma 1 (cosine sum).** For each integer $p$, $S(p) = \sum_{k=0}^{N-1} \cos\frac{\pi p (2k+1)}{2N}$ equals $N(-1)^{p/(2N)}$ if $2N \mid p$, and 0 otherwise.

*Proof.* Let $z = e^{i\pi p/(2N)}$, so $S(p) = \operatorname{Re} \sum_{k<N} z^{2k+1}$. If $2N \mid p$, then $z = (-1)^{p/(2N)}$, $z^2 = 1$, and the sum is $Nz$. Otherwise $z^2 \ne 1$ and $\sum_{k<N} z^{2k+1} = z(z^{2N} - 1)/(z^2 - 1) = ((-1)^p - 1)/(z - z^{-1})$. The numerator is real and $z - z^{-1} = 2i \sin\frac{\pi p}{2N}$ is purely imaginary, so the sum is purely imaginary and its real part is 0. $\square$

**Lemma 2 (the aliasing term).** $\frac{2}{N} C^{\mathsf T} C = I_{2N} + \begin{pmatrix} -J & 0 \\ 0 & J \end{pmatrix}$.

*Proof.* Let $\alpha = n + \frac{N+1}{2}$ and $\beta = m + \frac{N+1}{2}$. By $2\cos A \cos B = \cos(A - B) + \cos(A + B)$,

$$(C^{\mathsf T}C)_{nm} = \sum_{k<N} \cos\tfrac{\pi \alpha (2k+1)}{2N} \cos\tfrac{\pi \beta (2k+1)}{2N} = \tfrac12 S(n - m) + \tfrac12 S(n + m + N + 1).$$

Since $|n - m| < 2N$, the first term is $N/2$ if $n = m$ and 0 otherwise. Since $N + 1 \le n + m + N + 1 \le 5N - 1$, the second term is nonzero only when $n + m + N + 1 \in \{2N, 4N\}$. If $n + m = N - 1$, it is $\frac N2 (-1)^1 = -\frac N2$; then $n$ and $m$ both lie in $[0, N)$ and $m = N - 1 - n$, which is entry $(n, m)$ of $-J$ in the first block. If $n + m = 3N - 1$, it is $+\frac N2$; then both lie in $[N, 2N)$ with $m - N = N - 1 - (n - N)$, which is entry $(n, m)$ of $J$ in the second block. $\square$

So for a frame $x = (a, b)$ with halves $a, b \in \mathbb{R}^N$,

$$\text{IMDCT}(\text{MDCT}(x)) = W\,\tfrac{2}{N} C^{\mathsf T} C\, W x = \big(W_1^2 a - W_1 J W_1 a,\ \ W_2^2 b + W_2 J W_2 b\big). \tag{1}$$

With $W = I$ this is $(a - Ja, b + Jb)$, the formula of the example.

**Theorem 1 (perfect reconstruction).** Suppose that $w[2N-1-n] = w[n]$ and $w[n]^2 + w[n+N]^2 = 1$ for $0 \le n < N$. Then for every signal $s$ of length $L$, SYNTHESIS(ANALYSIS$(s, N, w)$, $N$, $w$, $L$) $= s$.

*Proof.* ANALYSIS pads $s$ to $p = (B_0, B_1, \dots, B_{c+1})$, blocks of length $N$ with $B_0 = 0$, $B_{c+1} = 0$, and $c = \lceil L/N \rceil$; the blocks $B_1, \dots, B_c$ hold $s$ followed by zeros. Frame $t$, for $0 \le t \le c$, is $(B_t, B_{t+1})$. SYNTHESIS adds the output of frame $t$ at offset $tN$, so the part of the sum at block $j$, for $1 \le j \le c$, is the second half of the output of frame $j-1$ plus the first half of the output of frame $j$. By (1), with $b = B_j$ for frame $j-1$ and $a = B_j$ for frame $j$, this is

$$\big(W_1^2 + W_2^2\big) B_j + \big(W_2 J W_2 - W_1 J W_1\big) B_j .$$

The matrix $W_1^2 + W_2^2$ is diagonal with entries $w[i]^2 + w[N+i]^2 = 1$. The matrix $W_2 J W_2$ has the entry $w[N+i]\, w[N + (N-1-i)] = w[N+i]\, w[2N-1-i]$ at position $(i, N-1-i)$, and $W_1 J W_1$ has $w[i]\, w[N-1-i]$ there. By the symmetry, $w[N+i] = w[N-1-i]$ and $w[2N-1-i] = w[i]$, so the two entries are equal and the difference is 0. So the sum at block $j$ is $B_j$. SYNTHESIS returns the samples from offset $N$, that is the blocks $B_1, B_2, \dots$, cut to length $L$, which is $s$. $\square$

**Theorem 2 (energy).** Under the same conditions, $\sum_t \|F[t]\|^2 = \|s\|^2$, where $F = $ ANALYSIS$(s, N, w)$.

*Proof.* For a frame $x = (a, b)$, $\|F\|^2 = x^{\mathsf T} W \frac2N C^{\mathsf T} C W x$, which by Lemma 2 is

$$a^{\mathsf T} W_1^2 a - a^{\mathsf T} W_1 J W_1 a + b^{\mathsf T} W_2^2 b + b^{\mathsf T} W_2 J W_2 b .$$

Sum over the frames $t = 0, \dots, c$. Block $B_j$ is $b$ in frame $j-1$ and $a$ in frame $j$, so it contributes $B_j^{\mathsf T}(W_1^2 + W_2^2) B_j + B_j^{\mathsf T}(W_2 J W_2 - W_1 J W_1) B_j = \|B_j\|^2$, as in Theorem 1. The blocks $B_0$ and $B_{c+1}$ are zero and contribute nothing. The sum of $\|B_j\|^2$ is $\|s\|^2$. $\square$

On the infinite line the same computation shows that the analysis operator $A$ satisfies $A^{\mathsf T}A = I$, and the synthesis is $A^{\mathsf T}$; for a finite padded signal, $A$ has $(c+1)N \ge L$ rows, so $AA^{\mathsf T}$ is a projection and the error in the signal after quantization is at most the error in the coefficients.

**Lemma 3 (symmetries of the kernel).** Let $\phi(m) = \cos\big(\frac{\pi}{N}(m + \frac12)(k + \frac12)\big)$ for a fixed integer $k$. Then $\phi(2N - 1 - m) = -\phi(m)$ and $\phi(m + 2N) = -\phi(m)$.

*Proof.* $\frac{\pi}{N}(2N - 1 - m + \frac12)(k + \frac12) = (2k+1)\pi - \frac{\pi}{N}(m + \frac12)(k + \frac12)$, and $\cos((2k+1)\pi - \theta) = -\cos\theta$. Also $\frac{\pi}{N}(m + 2N + \frac12)(k + \frac12) = \frac{\pi}{N}(m + \frac12)(k + \frac12) + (2k+1)\pi$, and $\cos(\theta + (2k+1)\pi) = -\cos\theta$. $\square$

**Theorem 3 (the fold).** Let $N$ be even, $h = N/2$, $z[n] = w[n]x[n]$, and define $u$ as on the page: $u[j] = -z[3h-1-j] - z[3h+j]$ for $j < h$ and $u[j] = z[j-h] - z[3h-1-j]$ for $h \le j < N$. Then MDCT$(x)[k] = \sqrt{2/N}\, \sum_{j<N} u[j]\, \phi(j)$.

*Proof.* Since $n + \frac12 + \frac N2 = (n + h) + \frac12$, MDCT$(x)[k] = \sqrt{2/N} \sum_{n<2N} z[n]\, \phi(n + h)$. Split the sum by $m = n + h \in [h, 2N + h)$:

- $m \in [h, N)$: $j = m$, $n = j - h$, term $z[j-h]\, \phi(j)$ for $h \le j < N$.
- $m \in [N, 2N)$: $j = 2N - 1 - m \in [0, N)$, $n = 3h - 1 - j$, and $\phi(m) = -\phi(j)$ by Lemma 3; term $-z[3h-1-j]\, \phi(j)$ for $0 \le j < N$.
- $m \in [2N, 2N + h)$: $j = m - 2N \in [0, h)$, $n = 3h + j$, and $\phi(m) = -\phi(j)$ by Lemma 3; term $-z[3h+j]\, \phi(j)$ for $0 \le j < h$.

Collecting the coefficient of each $\phi(j)$ gives $u[j]$. $\square$

**Theorem 4 (DCT-IV by an FFT of length $N/2$).** Let $N$ be even and $X_4[k] = \sum_{j<N} u[j] \cos\big(\frac{\pi}{N}(j + \frac12)(k + \frac12)\big)$. With $c[n]$ and $D[k]$ as on the page, $X_4[2k] = \operatorname{Re} D[k]$ and $X_4[N-1-2k] = -\operatorname{Im} D[k]$ for $0 \le k < N/2$.

*Proof.* The exponent of the term $n$ of $D[k]$ is $-\frac{i\pi}{4N}\big((4n + 1) + 16nk + 4k\big) = -i\alpha_n$ with $\alpha_n = \frac{\pi (4n+1)(4k+1)}{4N}$. With $a_n = u[2n]$ and $b_n = u[N-1-2n]$,

$$D[k] = \sum_{n<N/2} (a_n + i b_n)(\cos\alpha_n - i \sin\alpha_n), \quad \operatorname{Re} D[k] = \sum_n (a_n \cos\alpha_n + b_n \sin\alpha_n), \quad -\operatorname{Im} D[k] = \sum_n (a_n \sin\alpha_n - b_n \cos\alpha_n).$$

The indices $j = 2n$ and $j = N - 1 - 2n$, for $0 \le n < N/2$, cover $0, \dots, N-1$ once each. For the output $2k$: at $j = 2n$ the angle is $\frac{\pi}{N}(2n + \frac12)(2k + \frac12) = \alpha_n$; at $j = N - 1 - 2n$ it is $\frac{\pi}{N}(N - 2n - \frac12)(2k + \frac12) = 2\pi k + \frac{\pi}{2} - \alpha_n$, whose cosine is $\sin\alpha_n$. So $X_4[2k] = \operatorname{Re} D[k]$. For the output $N - 1 - 2k$: at $j = 2n$ the angle is $\frac{\pi}{N}(2n + \frac12)(N - 2k - \frac12) = 2\pi n + \frac{\pi}{2} - \alpha_n$, with cosine $\sin\alpha_n$; at $j = N-1-2n$ it is $\frac{\pi}{N}(N - 2n - \frac12)(N - 2k - \frac12) = \pi N - 2\pi(n + k) - \pi + \alpha_n$, and since $N - 1$ is odd its cosine is $-\cos\alpha_n$. So $X_4[N-1-2k] = -\operatorname{Im} D[k]$. The sum over $n$ in $D[k]$ is a DFT of length $N/2$ of $c$, which an FFT computes when $N/2$ is a power of two. $\square$

**Lemma 4 ($C_4^2 = \frac N2 I$).** $\sum_{k<N} \cos\big(\frac{\pi}{N}(j + \frac12)(k + \frac12)\big) \cos\big(\frac{\pi}{N}(k + \frac12)(m + \frac12)\big)$ is $N/2$ if $j = m$ and 0 otherwise.

*Proof.* The product is $\frac12 \cos\frac{\pi (j - m)(2k+1)}{2N} + \frac12 \cos\frac{\pi (j + m + 1)(2k+1)}{2N}$. By Lemma 1, the first sum is $N$ if $j = m$ and 0 otherwise, since $|j - m| < N$; the second is 0, since $1 \le j + m + 1 \le 2N - 1$. $\square$

By Lemma 4 the DCT-IV is its own inverse up to the factor $N/2$, so FAST-IMDCT can use the same routine. Its unfold reverses Theorem 3: IMDCT$(X)[n] = \sqrt{2/N}\, w[n] \sum_k X[k]\, \phi_k(n + h)$, and Lemma 3 rewrites $\phi_k(n + h)$ as $\phi_k(n+h)$ for $n + h < N$, $-\phi_k(2N - 1 - n - h)$ for $N \le n + h < 2N$, and $-\phi_k(n + h - 2N)$ for $n + h \ge 2N$, which gives the three cases of $v'$ on the page.

$\blacksquare$
