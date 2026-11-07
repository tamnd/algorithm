---
title: FFT-CONVOLVE returns the linear convolution, with a first-order error bound in floating point
proves: [correctness, error-bound]
status: full
---

Let $R$ be a commutative ring, $a \in R^m$, $b \in R^\ell$ with $m, \ell \ge 1$, $L = m + \ell - 1$, and $N$ the least power of two with $N \ge L$. Assume that $\omega \in R$ is a principal $N$-th root of unity and that $N$ is a unit of $R$. Let $a', b' \in R^N$ be $a$ and $b$ padded with zeros (lines L4 and L5).

**Lemma 1 (padding).** For $0 \le k \le N - 1$, $(a' \circledast b')_k = (a * b)_k$ if $k \le L - 1$, and $0$ otherwise.

*Proof.* By definition $(a' \circledast b')_k = \sum_{j=0}^{N-1} a'_j b'_{(k - j) \bmod N}$. A term is nonzero only if $j \le m - 1$ and $r = (k - j) \bmod N \le \ell - 1$. Then $j + r \le m + \ell - 2 < N$, and $j + r \equiv k \pmod N$ with $0 \le j + r < N$, so $j + r = k$. Hence the sum is $\sum_{j + r = k,\ j < m,\ r < \ell} a_j b_r$, which is $(a * b)_k$ for $k \le L - 1$ and an empty sum for $k \ge L$. $\square$

**Theorem 1.** FFT-CONVOLVE$(a, b)$ returns $a * b$.

*Proof.* By the correctness theorem of the [FFT](/fast-fourier-transform/), line L6 sets $A = F_N a'$ and $B = F_N b'$, with $(F_N x)_k = \sum_j x_j \omega^{jk}$. Line L7 sets $C = A \cdot B$ entrywise. By the [convolution theorem](/convolution-theorem/) (forward form, which only needs $\omega^N = 1$), $C = F_N(a' \circledast b')$. Since $\omega$ is principal and $N$ is a unit, INVERSE-FFT computes $F_N^{-1}$, so line L8 leaves $a' \circledast b'$ in $C$. By Lemma 1, its first $L$ entries, returned by line L9, are $a * b$. $\blacksquare$

**Operation count.** Lines L6 and L8 run three FFTs of length $N$, each with $\frac{N}{2} \lg N$ multiplications and $N \lg N$ additions. Line L7 does $N$ multiplications, and the scaling in line L8 does $N$ more. In total $\frac{3}{2} N \lg N + 2N$ multiplications and $3 N \lg N$ additions, with $N < 2L$ by the choice of $N$.

**Theorem 2 (floating point, first order).** Over $\mathbb{C}$ with $\omega = e^{-2\pi i/N}$, let each FFT be computed in floating point with unit roundoff $u$, and assume the bound of Higham, Theorem 24.2: the computed transform $\hat y$ of any vector $x$ satisfies $\lVert \hat y - F x \rVert_2 \le \delta \lVert F x \rVert_2$, where $\delta = \lg N \cdot \eta / (1 - \lg N \cdot \eta)$ and $\eta = \mu + \gamma_4 (\sqrt 2 + \mu)$. The same bound holds for the transform with $\omega^{-1}$. Assume each computed complex product is $xy(1 + \theta)$ with $|\theta| \le \gamma = \sqrt 2 \gamma_2$, and that the division by the power of two $N$ is exact. Then the computed $\hat c$ satisfies

$$\lVert \hat c - a * b \rVert_\infty \le (3\delta + \gamma) K + O(u^2), \qquad K = \max(\lVert a \rVert_1 \lVert b \rVert_2, \ \lVert a \rVert_2 \lVert b \rVert_1).$$

*Proof.* We use two facts on $F = F_N$ and $G = F_N(\omega^{-1})$: $\lVert F x \rVert_2 = \sqrt N \lVert x \rVert_2$, by the [summation lemma](/fft-summation-lemma/), and $\lVert F x \rVert_\infty \le \lVert x \rVert_1$, since every entry of $F$ has modulus $1$; the same holds for $G$. Also $\lVert a' \rVert = \lVert a \rVert$ in each norm.

Let $A = F a'$ and $\hat A = A + E_A$ with $\lVert E_A \rVert_2 \le \delta \sqrt N \lVert a \rVert_2$, and in the same way $\hat B = B + E_B$ with $\lVert E_B \rVert_2 \le \delta \sqrt N \lVert b \rVert_2$. The computed product is $\hat C_k = \hat A_k \hat B_k (1 + \theta_k)$. With $C = A \cdot B$, and dropping products of two error terms,

$$\hat C - C = E_A \cdot B + A \cdot E_B + \theta \cdot A \cdot B + O(u^2).$$

Now $\lVert E_A \cdot B \rVert_2 \le \lVert E_A \rVert_2 \lVert B \rVert_\infty \le \delta \sqrt N \lVert a \rVert_2 \lVert b \rVert_1$, $\lVert A \cdot E_B \rVert_2 \le \lVert A \rVert_\infty \lVert E_B \rVert_2 \le \delta \sqrt N \lVert a \rVert_1 \lVert b \rVert_2$, and $\lVert \theta \cdot A \cdot B \rVert_2 \le \gamma \lVert A \rVert_2 \lVert B \rVert_\infty \le \gamma \sqrt N \lVert a \rVert_2 \lVert b \rVert_1$. So $\lVert \hat C - C \rVert_2 \le (2\delta + \gamma) \sqrt N K + O(u^2)$.

The inverse step computes $\hat c' = \frac{1}{N}(G \hat C + E_G)$ with $\lVert E_G \rVert_2 \le \delta \lVert G \hat C \rVert_2 = \delta \sqrt N \lVert \hat C \rVert_2$. The exact value is $c' = \frac{1}{N} G C = a' \circledast b'$, by Theorem 1. So

$$\hat c' - c' = \tfrac{1}{N} G (\hat C - C) + \tfrac{1}{N} E_G.$$

For the first term, $\lVert \frac{1}{N} G v \rVert_\infty \le \frac{1}{N} \lVert v \rVert_1 \le \frac{1}{\sqrt N} \lVert v \rVert_2$, which gives at most $(2\delta + \gamma) K + O(u^2)$. For the second term, $\lVert \frac{1}{N} E_G \rVert_\infty \le \frac{1}{N} \lVert E_G \rVert_2 \le \frac{\delta}{\sqrt N} \lVert \hat C \rVert_2$, and $\lVert \hat C \rVert_2 = \lVert C \rVert_2 + O(u) \le \lVert A \rVert_2 \lVert B \rVert_\infty + O(u) \le \sqrt N K + O(u)$, which gives at most $\delta K + O(u^2)$. Adding the two terms, and noting that $\hat c$ is the first $L$ entries of $\hat c'$ and $a * b$ the first $L$ entries of $c'$, proves the bound. $\blacksquare$

**Exact rounding.** If $a$ and $b$ are integer vectors, then $a * b$ is an integer vector, and if the right side of Theorem 2, including the second-order terms, is below $\frac{1}{2}$, rounding each real part of $\hat c$ to the nearest integer returns $a * b$ exactly.
