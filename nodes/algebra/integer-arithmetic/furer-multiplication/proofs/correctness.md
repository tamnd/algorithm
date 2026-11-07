---
title: The toy Fürer scheme returns the product
proves: [correctness, termination]
status: full
---

This proof is for the exact toy model of the page: $R = \mathbb{Z}_q[x]/(x^m + 1)$ with $q$ prime, $m$ a power of 2, $K = 2m$, $N_t = K^L$ with $N_t \mid q - 1$, limbs of $b$ bits and $\beta = 2^b$. It does not cover Fürer's complex version, whose precision analysis is in his paper.

**Termination.** A call of FFT on a vector of length $K^\ell$ with $\ell \ge 2$ makes calls on vectors of length $K$ (line L7) and $K^{\ell - 1}$ (line L9) only, and a call of length $K$ stops at line L6, whose radix-2 DFT halves its length at each level. So the recursion depth is at most $L - 1 + \log_2 K$, and FURER-MULTIPLY makes three calls and finite loops.

**Lemma 1 (the ring and the root).** Let $\omega$ be a primitive $N_t$-th root of unity in $\mathbb{Z}_q$ and $\zeta = \omega^{N_t/K}$. The map $\phi(f) = (f(\zeta^{2i+1}))_{0 \le i < m}$ is a ring isomorphism $R \to \mathbb{Z}_q^m$. The element $\rho$ with $\phi(\rho) = (\omega^{2i+1})_i$ satisfies $\rho^{N_t/K} = x$, and $\rho$ is a principal $N_t$-th root of unity in $R$: $\rho^{N_t} = 1$, and $\sum_{j=0}^{N_t - 1} \rho^{jk} = 0$ for $k \not\equiv 0 \pmod{N_t}$.

*Proof.* $\zeta$ has order $K = 2m$, so $\zeta^m = -1$, and the $m$ numbers $\zeta^{2i+1}$ are distinct roots of $x^m + 1$. Hence $x^m + 1 = \prod_i (x - \zeta^{2i+1})$ over the field $\mathbb{Z}_q$, the factors are pairwise coprime, and $\phi$ is an isomorphism by the Chinese remainder theorem. Then $\phi(\rho^{N_t/K}) = (\omega^{(2i+1)N_t/K})_i = (\zeta^{2i+1})_i = \phi(x)$, so $\rho^{N_t/K} = x$. Each coordinate $\omega^{2i+1}$ is a primitive $N_t$-th root of unity, since $2i + 1$ is odd and $N_t$ is a power of 2. So $\rho^{N_t} = 1$, and for $k \not\equiv 0$ each coordinate of $\phi(\sum_j \rho^{jk})$ is a geometric sum $\sum_j \omega^{(2i+1)jk} = 0$, because $\omega^{(2i+1)k} \ne 1$ and its $N_t$-th power is 1. $\square$

**Lemma 2 (shifts).** For each integer $e$, SHIFT computes $a \cdot x^e$ in $R$.

*Proof.* $x^{2m} = 1$ in $R$, so only $e \bmod 2m$ matters, and $x^m = -1$ turns $e \ge m$ into a sign and $e - m$. Then $x^e \sum_i a_i x^i = \sum_i a_i x^{i+e}$, and each term with $i + e \ge m$ is $-a_i x^{i + e - m}$, which is what the code writes. $\square$

**Lemma 3 (FFT).** If $|v| \cdot s = N_t$ and $|v| = K^\ell$ with $\ell \ge 1$, then FFT$(v, s, \sigma)$ returns $X_k = \sum_{n < |v|} v_n \omega^{nk}$ for $0 \le k < |v|$, with $\omega = \rho^{\sigma s}$.

*Proof.* By induction on $\ell$. If $\ell = 1$, then $s = N_t/K$ and $\omega = \rho^{\sigma N_t/K} = x^\sigma$ by Lemma 1, and line L6 computes the DFT with root $x^\sigma$ by the radix-2 recursion, which is correct for each element $\omega$ with $\omega^{K} = 1$, using $\omega^{K/2} = x^{\sigma m} = -1$; its multiplications are by powers of $x$ and are correct by Lemma 2. If $\ell \ge 2$, let $J = K^{\ell - 1}$, and write $n = J n_2 + n_1$ and $k = k_1 + K k_2$ with $n_1, k_2 < J$ and $n_2, k_1 < K$. Since $\omega^{JK} = \omega^{|v|} = \rho^{\sigma N_t} = 1$,

$$\omega^{nk} = \omega^{J n_2 k_1} \cdot \omega^{n_1 k_1} \cdot \omega^{K n_1 k_2}.$$

So $X_{k_1 + K k_2} = \sum_{n_1} \omega^{K n_1 k_2} \left( \omega^{n_1 k_1} \sum_{n_2} v_{J n_2 + n_1} (\omega^{J})^{n_2 k_1} \right)$. Here $\omega^J = \rho^{\sigma s J}$ with $sJ = N_t/K$, so the inner sum is the DFT of length $K$ that line L7 computes by the induction hypothesis with stride $N_t/K$. Line L8 multiplies its $k_1$-th entry by $\omega^{n_1 k_1}$, skipping the factors equal to 1. The outer sum is the DFT of length $J$ with root $\omega^K = \rho^{\sigma s K}$, which line L9 computes with stride $sK$, where $J \cdot sK = N_t$, by the induction hypothesis. Line L9 stores it at index $k_1 + K k_2$. $\square$

**Lemma 4 (inversion).** If $\hat c = \mathrm{FFT}(c, 1, +1)$, then FFT$(\hat c, 1, -1) = N_t c$.

*Proof.* By Lemma 3 the $n$-th entry of FFT$(\hat c, 1, -1)$ is $\sum_k \sum_j c_j \rho^{jk} \rho^{-nk} = \sum_j c_j \sum_k \rho^{(j - n)k} = N_t c_n$, by Lemma 1. $\square$

**Theorem.** If $u, v < 2^{(N_t/2)(m/2) b}$ and $(N_t/2)(m/2)(\beta - 1)^2 < q$, then FURER-MULTIPLY returns $uv$.

*Proof.* Line L1 writes $u = \sum_{j < N_t/2} \sum_{t < m/2} u_{j,t} \beta^{t + j m/2}$ with $0 \le u_{j,t} < \beta$, and sets $a_j = \sum_t u_{j,t} x^t$ for $j < N_t/2$ and $a_j = 0$ for $j \ge N_t/2$; the same for $v$ and $b_j$. By Lemma 3 and the convolution property, which follows from Lemma 4 in the usual way, $c = \mathrm{FFT}(\hat a \cdot \hat b, 1, -1)/N_t$ is the cyclic convolution $c_n = \sum_{j + j' \equiv n \pmod{N_t}} a_j b_{j'}$ in $R$. Since $a_j$ and $b_{j'}$ vanish for $j, j' \ge N_t/2$, only pairs with $j + j' = n < N_t - 1$ contribute, and there is no wrap. Each $a_j b_{j'}$ has degree at most $m - 2 < m$ in $x$, so it is the plain product of the polynomials, with no use of $x^m = -1$. Hence the coefficient of $x^t$ in $c_n$, as an integer, is $\sum u_{j,s} v_{j',s'}$ over $j + j' = n$ and $s + s' = t$, a sum of at most $(N_t/2)(m/2)$ terms each at most $(\beta - 1)^2$, so it is less than $q$ and its residue modulo $q$ is the integer itself. Line L5 computes $\sum_n \sum_t c_{n,t} \beta^{t + n m/2}$, which is

$$\sum_{j, s} \sum_{j', s'} u_{j,s} v_{j',s'} \beta^{(s + s') + (j + j') m/2} = uv. \qquad \blacksquare$$
