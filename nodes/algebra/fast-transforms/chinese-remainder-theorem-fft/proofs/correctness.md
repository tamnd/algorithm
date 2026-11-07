---
title: The Good-Thomas re-indexing turns a DFT with coprime factors into a multidimensional DFT without twiddle factors
proves: [correctness, complexity, error-bound]
status: full
---

Let $R$ be a commutative ring, $n = n_1 \cdots n_r$ with the $n_i$ pairwise coprime, and $\omega \in R$ a principal $n$-th root of unity: $\omega^n = 1$ and $\sum_{j=0}^{n-1} \omega^{jl} = 0$ for $1 \le l \le n - 1$. Put $N_i = n/n_i$ and $e_i = N_i^{-1} \bmod n_i$. Define $\iota(j_1, \ldots, j_r) = \sum_i N_i j_i \bmod n$ (line L2) and $\kappa(k_1, \ldots, k_r) = \sum_i N_i e_i k_i \bmod n$ (line L5), on tuples with $0 \le j_i, k_i < n_i$.

**Lemma 1 (bijections).** $\iota$ and $\kappa$ are bijections onto $\{0, \ldots, n - 1\}$, and $\kappa(k_1, \ldots, k_r) \equiv k_i \pmod{n_i}$ for every $i$.

*Proof.* For $a \ne i$, $n_a \mid N_i$, so $\iota(j) \equiv N_a j_a \pmod{n_a}$ and $\kappa(k) \equiv N_a e_a k_a \equiv k_a \pmod{n_a}$. Since $\gcd(N_a, n_a) = 1$, $N_a$ is invertible modulo $n_a$, so the residues of $\iota(j)$ modulo all $n_a$ determine $j$, and those of $\kappa(k)$ are $k$ itself. By the [Chinese remainder theorem](/chinese-remainder-theorem/) a number in $\{0, \ldots, n - 1\}$ is determined by its residues modulo the $n_a$, so both maps are injective, and both sets have $n$ elements. $\square$

**Lemma 2 (splitting the kernel).** $\omega^{\iota(j) \kappa(k)} = \prod_{i=1}^{r} (\omega^{N_i})^{j_i k_i}$.

*Proof.* Since $\omega^n = 1$, exponents may be taken modulo $n$. $\iota(j) \kappa(k) \equiv \sum_{a, i} N_a N_i e_i j_a k_i \pmod n$. For $a \ne i$, $N_a N_i$ is a multiple of $n$, since every $n_b$ divides $N_a$ or $N_i$ and the $n_b$ are pairwise coprime; so only the terms $a = i$ remain, and $\omega^{\iota(j)\kappa(k)} = \prod_i (\omega^{N_i})^{N_i e_i j_i k_i}$. Now $(\omega^{N_i})^{n_i} = 1$ and $N_i e_i \equiv 1 \pmod{n_i}$, so $(\omega^{N_i})^{N_i e_i j_i k_i} = (\omega^{N_i})^{j_i k_i}$. $\square$

**Lemma 3 (axis roots).** If $n$ is a unit of $R$, then $\omega^{N_i}$ is a principal $n_i$-th root of unity. (Theorem 1 below does not need this; it matters when line L4 uses a fast short DFT, such as a radix-2 FFT, that requires a principal root.)

*Proof.* Let $\zeta = \omega^{N_i}$. Then $\zeta^{n_i} = \omega^n = 1$. Fix $1 \le l \le n_i - 1$ and put $T = \sum_{m=0}^{n_i - 1} \zeta^{ml}$. Writing $j = q n_i + m$ with $0 \le q < N_i$ and $0 \le m < n_i$, and using $\omega^{q n_i N_i l} = 1$, we get $\sum_{j=0}^{n-1} \omega^{j N_i l} = N_i T$. The left side is $0$ because $1 \le N_i l \le n - N_i < n$ and $\omega$ is principal. Since $N_i n_i = n$ is a unit, so is $N_i$, hence $T = 0$. $\square$

**Theorem 1 (correctness).** GOOD-THOMAS returns $X = F_n x$, $X_k = \sum_j x_j \omega^{jk}$.

*Proof.* Line L2 sets $A[j_1, \ldots, j_r] = x_{\iota(j)}$. The loop of lines L3 and L4 applies, for $i = 1, \ldots, r$, the DFT of length $n_i$ with the root $\omega^{N_i}$ along the axis $i$. These maps act on different indices and are linear, so after the loop

$$A[k_1, \ldots, k_r] = \sum_{j_1, \ldots, j_r} x_{\iota(j)} \prod_i (\omega^{N_i})^{j_i k_i} = \sum_{j_1, \ldots, j_r} x_{\iota(j)} \, \omega^{\iota(j) \kappa(k)}$$

by Lemma 2. Since $\iota$ is a bijection (Lemma 1), this is $\sum_{j=0}^{n-1} x_j \omega^{j \kappa(k)} = X_{\kappa(k)}$. Line L5 stores it at the index $\kappa(k)$, and since $\kappa$ is a bijection, every entry of $X$ is written exactly once. $\square$

**Theorem 2 (inverse).** If $n$ is a unit of $R$, running GOOD-THOMAS with $\omega^{-1}$ and multiplying by $n^{-1}$ returns $x$ from $X$.

*Proof.* $\omega^{-1}$ is a principal $n$-th root (as in Theorem 2 of the [FFT proof](/fast-fourier-transform/)), so by Theorem 1 the procedure computes $Y_l = \sum_k X_k \omega^{-lk} = \sum_j x_j \sum_k \omega^{(j - l)k} = n x_l$, by the definition of a principal root. $\square$

**Operation count.** Line L4 for the axis $i$ runs $N_i = n/n_i$ short DFTs. If each costs $M(n_i)$ multiplications and $S(n_i)$ additions, the total is $n \sum_i M(n_i)/n_i$ multiplications and $n \sum_i S(n_i)/n_i$ additions. Lines L2 and L5 are permutations, with no ring operations. The direct short DFT used by the implementation does $(n_i - 1)^2$ multiplications by roots other than $1$ and $n_i(n_i - 1)$ additions, so the total is at most $n \sum_i (n_i - 1)$ of each.

**Theorem 3 (rounding error over $\mathbb{C}$).** Suppose $\omega = e^{-2\pi i/n}$, each computed root power $\hat r$ has $|\hat r - r| \le \mu$, complex products have relative error at most $\sqrt 2 \gamma_2$ (Higham, Lemma 3.5), and the short DFTs are direct sums evaluated left to right. Then

$$\lVert \hat X - X \rVert_2 \le \sum_{i=1}^{r} \sqrt{n_i} \, (\gamma_{n_i - 1} + \sqrt 2 \gamma_2 + \mu) \, \lVert X \rVert_2 + O(u^2).$$

*Proof.* Let $c_i = \gamma_{n_i - 1} + \sqrt 2 \gamma_2 + \mu$. Consider one short DFT of a line $z \in \mathbb{C}^{m}$, $m = n_i$, with outputs $Y_k = \sum_l z_l r^{lk}$, $|r| = 1$. Each product $z_l \hat r^{lk}$ is computed with error at most $(\mu + \sqrt 2 \gamma_2)|z_l| + O(u^2)$, and the recursive sum of $m$ complex terms $t_l$ has error at most $\gamma_{m-1} \sum_l |t_l|$, since each of the real and imaginary parts does and $\sqrt{(\sum_l a_l)^2 + (\sum_l b_l)^2} \le \sum_l \sqrt{a_l^2 + b_l^2}$ for $a_l, b_l \ge 0$. So $|\hat Y_k - Y_k| \le c_i \sum_l |z_l| + O(u^2) \le c_i \sqrt m \lVert z \rVert_2 + O(u^2)$, and over the $m$ outputs, $\lVert \hat Y - Y \rVert_2 \le c_i \, m \, \lVert z \rVert_2 + O(u^2) = c_i \sqrt m \, \lVert Y \rVert_2 + O(u^2)$, since $\lVert Y \rVert_2 = \sqrt m \lVert z \rVert_2$. Summing over the lines of an axis, the pass $i$ maps the array $z^{(i-1)}$ to $S_i z^{(i-1)}$ with $S_i = \sqrt{n_i} \, Q_i$, $Q_i$ unitary, and adds an error $e_i$ with $\lVert e_i \rVert_2 \le c_i \sqrt{n_i} \lVert S_i z^{(i-1)} \rVert_2 + O(u^2)$. The permutations of lines L2 and L5 are exact and preserve norms. By linearity, the final error is $\sum_i S_r \cdots S_{i+1} e_i$, and $\lVert S_r \cdots S_{i+1} S_i z^{(i-1)} \rVert_2 = \sqrt n \lVert x \rVert_2 (1 + O(u)) = \lVert X \rVert_2 (1 + O(u))$, so each term has norm at most $c_i \sqrt{n_i} \lVert X \rVert_2 + O(u^2)$. Summing over $i$ gives the bound. $\blacksquare$
