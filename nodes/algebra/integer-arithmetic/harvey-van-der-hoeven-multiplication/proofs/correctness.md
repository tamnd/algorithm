---
title: The toy Harvey-van der Hoeven scheme returns the product
proves: [correctness, termination]
status: full
---

This proof is for the exact toy of the page: distinct primes $s_1, \dots, s_d$, $S = s_1 \cdots s_d$, a prime $q \equiv 1 \pmod S$, limbs of $b$ bits and $\beta = 2^b$. It does not cover Gaussian resampling or the complex arithmetic of the paper, whose analysis is in Harvey and van der Hoeven's Sections 4 and 5.

**Termination.** Every loop of the toy runs over a finite range: $d$ dimensions, $S$ cells, $s - 1$ convolution indices. PRIME-DFT is not recursive, and DFT$_d$ calls it $\sum_i S/s_i$ times.

**Lemma 1 (the cell map).** The map $\kappa(j) = (j \bmod s_1, \dots, j \bmod s_d)$ is a bijection from $\{0, \dots, S - 1\}$ to $\prod_i \{0, \dots, s_i - 1\}$, and $\kappa(j + j') = \kappa(j) + \kappa(j')$ with addition in each coordinate modulo $s_i$, for every $j, j'$, where $j + j'$ is read modulo $S$.

*Proof.* The $s_i$ are distinct primes, hence pairwise coprime, so by the Chinese remainder theorem $\mathbb{Z}/S \to \prod_i \mathbb{Z}/s_i$, $j \mapsto (j \bmod s_i)_i$, is a group isomorphism. Both sets have $S$ elements. $\square$

**Lemma 2 (Rader).** Let $s$ be prime, $g$ a generator of $(\mathbb{Z}/s)^\times$ and $\omega$ an element of $\mathbb{Z}_q$ with $\omega^s = 1$. Lines L10 to L12 return $X_k = \sum_{n < s} x_n \omega^{nk}$ for every $0 \le k < s$.

*Proof.* For $k = 0$, $X_0 = \sum_n x_n$, line L10. For $s = 2$ the code passes $\omega = -1$, the primitive square root of unity, which is its own inverse, and returns $(x_0 + x_1, x_0 - x_1)$, which is the DFT. For $s > 2$, each $k \ne 0$ is $g^{-p} \bmod s$ for exactly one $p \in \{0, \dots, s - 2\}$, and each $n \ne 0$ is $g^{m} \bmod s$ for exactly one $m$, since $g$ generates a cyclic group of order $s - 1$. Then

$$X_{g^{-p}} = x_0 + \sum_{m=0}^{s-2} x_{g^m}\, \omega^{g^{m - p}} = x_0 + \sum_{m=0}^{s-2} a_m c_{(p - m) \bmod (s - 1)},$$

with $a_m = x_{g^m}$ and $c_k = \omega^{g^{-k}}$, because $\omega^e$ depends only on $e \bmod s$ and $g^{m-p} = g^{-(p - m)}$, where the exponent of $g$ can be read modulo $s - 1$. The last sum is entry $p$ of the cyclic convolution of $a$ and $c$, line L11, and line L12 stores $x_0 + c_p$ at $g^{-p}$. $\square$

**Lemma 3 (DFT$_d$).** For an array $A$ indexed by $(j_1, \dots, j_d)$ with $0 \le j_i < s_i$, DFT$_d(A, \sigma)$ returns

$$\hat A(k_1, \dots, k_d) = \sum_{j_1, \dots, j_d} A(j_1, \dots, j_d) \prod_i \omega_i^{\sigma j_i k_i}.$$

*Proof.* After the pass $i$ of line L7, the array holds the transform in the first $i$ coordinates: this holds for $i = 0$, and the pass $i$ applies, by Lemma 2, the one-dimensional DFT with root $\omega_i^\sigma$ to every line along coordinate $i$, which multiplies by $\omega_i^{\sigma j_i k_i}$ and sums over $j_i$ with the other coordinates fixed. The kernel is a product of one-dimensional kernels, so the $d$ passes give $\hat A$. $\square$

**Lemma 4 (inversion and convolution).** If $\omega_i$ is a primitive $s_i$-th root of unity for each $i$, then DFT$_d(\mathrm{DFT}_d(A, +1), -1) = S \cdot A$, and DFT$_d(\hat F \cdot \hat G, -1)/S$ is the cyclic convolution $H(\ell) = \sum_{j + j' = \ell} F(j) G(j')$, with $j + j'$ taken coordinatewise modulo the $s_i$.

*Proof.* For a primitive $s$-th root $\omega$ and an integer $e$, $\sum_{k < s} \omega^{ek}$ is $s$ if $s \mid e$ and 0 otherwise, since $\omega^e \ne 1$ is a root of $\sum_{k < s} z^k$ in the field $\mathbb{Z}_q$. Expanding both claims with Lemma 3 gives products of these sums over the $d$ coordinates, which are $S$ when $j = \ell$ (resp. $j + j' = \ell$) in each coordinate and 0 otherwise. $\square$

**Theorem.** If $0 \le u, v < \beta^{(S+1)/2}$ and $\frac{S+1}{2}(\beta - 1)^2 < q$, then HVDH-TOY-MULTIPLY returns $uv$.

*Proof.* Line L1 writes $u = \sum_{j < C} f_j \beta^j$ and $v = \sum_{j < C} g_j \beta^j$ with $C = (S + 1)/2$ and $0 \le f_j, g_j < \beta$, and sets $f_j = g_j = 0$ for $C \le j < S$. Line L2 puts $f_j$ in the cell $\kappa(j)$; by Lemma 1 each cell receives exactly one index. By Lemmas 3 and 4, after line L5 the cell $\kappa(\ell)$ holds $\sum f_j g_{j'}$ over the pairs with $\kappa(j) + \kappa(j') = \kappa(\ell)$, which by Lemma 1 are the pairs with $j + j' \equiv \ell \pmod S$. Since $f_j g_{j'} \ne 0$ only for $j, j' < C$, we have $j + j' \le 2C - 2 = S - 1$, so the congruence is an equality, and the cell holds $h_\ell = \sum_{j + j' = \ell} f_j g_{j'}$ reduced modulo $q$. This integer is a sum of at most $C$ terms, each at most $(\beta - 1)^2$, so it is less than $q$ and equals its residue. Line L6 computes $\sum_\ell h_\ell \beta^\ell = \sum_{j, j'} f_j g_{j'} \beta^{j + j'} = uv$. $\blacksquare$
