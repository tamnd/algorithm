---
title: The iterative FFT computes the DFT, and FFT-MULTIPLY returns the product
proves: [correctness]
status: full
---

Let $R$ be a commutative ring with $1$, $N = 2^k$ with $k \ge 0$, and $\omega \in R$ with $\omega^N = 1$ and, if $N \ge 2$, $\omega^{N/2} = -1$. For a list $c = [c_0, \ldots, c_{N-1}]$ define $\operatorname{DFT}_\omega(c)_i = \sum_{j<N} c_j \omega^{ij}$ for $0 \le i < N$. For $0 \le l \le k$ and $0 \le t < 2^l$, write $\operatorname{rev}_l(t)$ for the number whose $l$ binary digits are those of $t$ in reverse order.

**Lemma 1 (powers of a principal root).** For $1 \le L \le N$ a power of two, $\omega_L = \omega^{N/L}$ satisfies $\omega_L^L = 1$ and, if $L \ge 2$, $\omega_L^{L/2} = -1$. Also $\omega^{-1} = \omega^{N-1}$ is again a principal $N$-th root of unity.

*Proof.* $\omega_L^L = \omega^N = 1$ and $\omega_L^{L/2} = \omega^{N/2} = -1$. For $\omega^{-1}$: $\omega \cdot \omega^{N-1} = 1$, $(\omega^{-1})^N = 1$, and $(\omega^{-1})^{N/2} = (\omega^{N/2})^{-1} = (-1)^{-1} = -1$. $\square$

**Lemma 2 (iterative FFT).** DFT$(a, \omega)$, lines F1 to F11, replaces $a$ by $\operatorname{DFT}_\omega(a)$.

*Proof.* Let $a$ be the input. Line F1 puts $a_{\operatorname{rev}_k(i)}$ at position $i$; the swap of $i$ and $\operatorname{rev}_k(i)$ is done once for each pair with $i < \operatorname{rev}_k(i)$, and $\operatorname{rev}_k$ is an involution, so this is a permutation. We prove by induction on $l$ the claim

> **(S$_l$)** after the stages with block lengths $2, 4, \ldots, 2^l$ (for $l = 0$, after line F1), for each block index $0 \le t < N/L$ with $L = 2^l$ and each $0 \le j < L$, the position $tL + j$ holds $Y_{l,t}(j) = \sum_{p<L} a_{r + pN/L}\, \omega_L^{jp}$, where $r = \operatorname{rev}_{k-l}(t)$.

*Base.* For $l = 0$, $L = 1$, the sum has one term, $a_{\operatorname{rev}_k(t)}$, which line F1 put at position $t$.

*Step.* Assume (S$_l$) and let $L = 2^l < N$. The stage with len $= 2L$ (line F4 sets $w_{\text{len}} = \omega^{N/2L} = \omega_{2L}$) works on the blocks $[s, s + 2L)$ with $s = 2L t'$. Such a block is the union of the old blocks $2t'$ and $2t' + 1$. Reversing $k - l$ digits, $\operatorname{rev}_{k-l}(2t') = \operatorname{rev}_{k-l-1}(t')$, since the low digit 0 of $2t'$ becomes the top digit, and $\operatorname{rev}_{k-l}(2t' + 1) = 2^{k-l-1} + \operatorname{rev}_{k-l-1}(t')$. Write $r' = \operatorname{rev}_{k-l-1}(t')$, and note $2^{k-l-1} = N/2L$. So by (S$_l$) the first half of the block holds $E(j) = \sum_{p<L} a_{r' + 2p N/2L}\, \omega_L^{jp}$ and the second half holds $O(j) = \sum_{p<L} a_{r' + N/2L + 2p N/2L}\, \omega_L^{jp}$, for $0 \le j < L$.

Lines F6 and F10 give $w = \omega_{2L}^j$ in step $j$ of line F7. Lines F8 and F9 set position $s + j$ to $E(j) + \omega_{2L}^j O(j)$ and position $s + j + L$ to $E(j) - \omega_{2L}^j O(j)$. Each step reads only the two positions it writes, so the steps do not interfere. Now split the target sum by the parity of $q$:

$$Y_{l+1,t'}(j) = \sum_{q<2L} a_{r' + qN/2L}\, \omega_{2L}^{jq} = \sum_{p<L} a_{r' + 2pN/2L}\, \omega_{2L}^{2jp} + \sum_{p<L} a_{r' + (2p+1)N/2L}\, \omega_{2L}^{j(2p+1)} = E(j) + \omega_{2L}^{j} O(j),$$

because $\omega_{2L}^2 = \omega_L$. For $j + L$, the same computation has $\omega_L^{(j+L)p} = \omega_L^{jp}$ (as $\omega_L^L = 1$) and $\omega_{2L}^{j+L} = -\omega_{2L}^j$ (as $\omega_{2L}^L = -1$, Lemma 1), so $Y_{l+1,t'}(j + L) = E(j) - \omega_{2L}^j O(j)$. This is (S$_{l+1}$).

*End.* The loop of line F3 runs for len $= 2, \ldots, N$, so (S$_k$) holds at the end. With $L = N$ there is one block, $t = 0$, $r = 0$, and position $j$ holds $\sum_{p<N} a_p \omega^{jp} = \operatorname{DFT}_\omega(a)_j$. $\square$

**Lemma 3 (orthogonality).** For each integer $j$ with $N \nmid j$, $\sum_{i<N} \omega^{ij} = 0$.

*Proof.* Then $N \ge 2$. Write $j \bmod N = 2^e o$ with $o$ odd and $0 \le e < k$, and let $h = N / 2^{e+1}$, an integer at least 1. Let $\eta = \omega^j$. Then $\eta^h = \omega^{2^e o N / 2^{e+1}} = (\omega^{N/2})^o = (-1)^o = -1$ (using $\omega^N = 1$ to reduce $j$ modulo $N$). Group the indices $0 \le i < N$ in pairs $\{i, i + h\}$ with $\lfloor i/h \rfloor$ even; these pairs cover $[0, N)$ because $2h$ divides $N$. In each pair $\eta^{i + h} = -\eta^i$, so each pair sums to $0$. $\square$

**Lemma 4 (inversion).** For each list $c$ of length $N$, if $N$ is a unit then $N^{-1} \operatorname{DFT}_{\omega^{-1}}(\operatorname{DFT}_\omega(c)) = c$.

*Proof.* The $j$-th entry of $\operatorname{DFT}_{\omega^{-1}}(\operatorname{DFT}_\omega(c))$ is

$$\sum_{i<N} \omega^{-ij} \sum_{l<N} c_l\, \omega^{il} = \sum_{l<N} c_l \sum_{i<N} \omega^{i(l - j)}.$$

For $l = j$ the inner sum is $N$. For $l \ne j$, $0 < |l - j| < N$, so $N \nmid l - j$, and the inner sum is $0$ by Lemma 3 (the exponent $l - j$ may be negative; $\omega^{l-j}$ means $\omega^{(l - j) \bmod N}$). So the entry is $N c_j$. $\square$

**Lemma 5 (the pointwise product).** Let $f = \sum_{i<m} a_i x^i$, $g = \sum_{j<n} b_j x^j$, $h = fg$, and let $\bar a, \bar b, \bar h$ be the coefficient lists padded with zeros to length $N \ge m + n - 1$. Then $\operatorname{DFT}_\omega(\bar a)_i \cdot \operatorname{DFT}_\omega(\bar b)_i = \operatorname{DFT}_\omega(\bar h)_i$ for each $i$.

*Proof.* $\operatorname{DFT}_\omega(\bar a)_i = f(\omega^i)$, because the padded zeros add nothing. Evaluation at $\omega^i$ is a ring homomorphism $R[x] \to R$, so $f(\omega^i) g(\omega^i) = h(\omega^i)$. Since $\deg h \le m + n - 2 < N$, $\bar h$ holds all coefficients of $h$, and $h(\omega^i) = \operatorname{DFT}_\omega(\bar h)_i$. $\square$

**Theorem.** If $\omega$ is a principal $N$-th root of unity in $R$ and $N$ is a unit, FFT-MULTIPLY$(a, b)$ returns the normalized coefficient list of $fg$.

*Proof.* If $a$ or $b$ is empty, a factor is zero and line L1 returns the empty list. Otherwise lines L2 and L3 give $N \ge m + n - 1$ and the padded lists. By Lemma 2, line L4 computes $A = \operatorname{DFT}_\omega(\bar a)$ and $B = \operatorname{DFT}_\omega(\bar b)$, and by Lemma 5, line L5 gives $C = \operatorname{DFT}_\omega(\bar h)$. By Lemma 1, $\omega^{-1}$ is a principal $N$-th root, so Lemma 2 applies to the call in line L6, and by Lemma 4 line L6 gives $c = \bar h$. Line L7 drops the padding above position $m + n - 2$, which is zero, and removes zero top entries, which do not change the polynomial. $\blacksquare$

**Remark (the reductions over $\mathbb{Z}$, $\mathbb{Z}/m\mathbb{Z}$ and $\mathbb{Q}$).** Over $\mathbb{Z}$, each coefficient satisfies $|h_k| = |\sum_{i+j=k} a_i b_j| \le \min(m, n) \max|a_i| \max|b_j| = B$, since the sum has at most $\min(m, n)$ terms. The theorem gives $h_k \bmod p$ for each prime $p$ used. If the product $P$ of the primes exceeds $2B$, then $h_k$ is the only integer in $(-P/2, P/2]$ with these residues, by the Chinese remainder theorem, and Garner's method returns it. For $\mathbb{Z}/m\mathbb{Z}$, the map $\mathbb{Z}[x] \to (\mathbb{Z}/m\mathbb{Z})[x]$ is a ring homomorphism, so reducing the integer product of the representatives gives the product modulo $m$. For $\mathbb{Q}$, $(d_a f)(d_b g) = d_a d_b\, fg$ with integer polynomials on the left. $\square$
