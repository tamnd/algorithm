---
title: The periodic fast wavelet transform is orthogonal, its transposed cascade inverts it, and its rounding error grows linearly in the number of levels
proves: [correctness, complexity, error-bound]
status: full
---

Let $h = (h_0, \ldots, h_{L-1})$ be real with $L$ even and $\sum_l h_l h_{l + 2s} = \delta_{s,0}$ for every integer $s$, where $h_l = 0$ outside $0 \le l < L$ and $\delta$ is the Kronecker delta. Let $g_l = (-1)^l h_{L-1-l}$, also zero outside $0 \le l < L$. For an even $m \ge 2$, let $W_m$ be the $m \times m$ matrix with

$$(W_m)_{i, c} = \sum_{l \,:\, 2i + l \equiv c \ (\mathrm{mod}\ m)} h_l, \qquad (W_m)_{m/2 + i, c} = \sum_{l \,:\, 2i + l \equiv c \ (\mathrm{mod}\ m)} g_l, \qquad 0 \le i < m/2,$$

so that lines L6 and L7 compute $(s, d) = W_m a$ for the block $a$ of length $m$.

**Lemma 1 (filter identities).** For every integer $s$, $\sum_l g_l g_{l+2s} = \delta_{s,0}$ and $\sum_l h_l g_{l+2s} = 0$.

*Proof.* With $r = L - 1 - l$, $\sum_l g_l g_{l+2s} = \sum_l (-1)^{2l + 2s} h_{L-1-l} h_{L-1-l-2s} = \sum_r h_r h_{r - 2s} = \delta_{s,0}$, by the hypothesis with the shift $-s$. Next, $P = \sum_l h_l g_{l+2s} = \sum_l (-1)^l h_l h_{L-1-2s-l}$, using $(-1)^{2s} = 1$. Substitute $l' = L - 1 - 2s - l$: $P = \sum_{l'} (-1)^{L-1-2s-l'} h_{L-1-2s-l'} h_{l'} = -\sum_{l'} (-1)^{l'} h_{l'} h_{L-1-2s-l'} = -P$, because $L - 1 - 2s$ is odd. So $P = 0$. $\square$

**Lemma 2 (periodization).** Let $p, q$ be filters with $\sum_l p_l q_{l+2s} = c \, \delta_{s,0}$ for every integer $s$, and let $m$ be even. Then for $0 \le i, i' < m/2$, $\sum_{c=0}^{m-1} P_{i,c} Q_{i',c} = c \, \delta_{i,i'}$, where $P_{i,c} = \sum_{l : 2i + l \equiv c} p_l$ and $Q_{i',c}$ is defined in the same way from $q$.

*Proof.* Expanding, $\sum_c P_{i,c} Q_{i',c} = \sum_{l, l'} p_l q_{l'} [2i + l \equiv 2i' + l' \pmod m]$. The condition says $l' = l + 2(i - i') + t m$ for some integer $t$, and since $m$ is even, $2(i - i') + tm = 2\sigma_t$ with $\sigma_t = i - i' + tm/2$. So the sum is $\sum_t \sum_l p_l q_{l + 2\sigma_t} = c \sum_t \delta_{\sigma_t, 0}$. Since $|i - i'| < m/2$, $\sigma_t = 0$ holds for at most one $t$, namely $t = 0$ when $i = i'$, and for no $t$ when $i \ne i'$. $\square$

**Theorem 1 (one level).** $W_m$ is orthogonal for every even $m \ge 2$.

*Proof.* The rows of $W_m$ are the periodized shifts of $h$ (rows $i < m/2$) and of $g$ (rows $m/2 + i$). Lemma 2 with $(p, q) = (h, h)$ and $c = 1$ (the hypothesis), with $(g, g)$ and $c = 1$, and with $(h, g)$ and $c = 0$ (Lemma 1) gives $W_m W_m^{\mathsf T} = I$. A square matrix with $W W^{\mathsf T} = I$ is orthogonal. $\square$

**Theorem 2 (forward and inverse).** Let $n$ be divisible by $2^J$, and let $T = (W_{n/2^{J-1}} \oplus I) \cdots (W_{n/2} \oplus I_{n/2}) W_n$, where $W_m \oplus I$ acts on the first $m$ entries and fixes the rest. Then FWT$(x, h, J)$ returns $T x$, $T$ is orthogonal, and INVERSE-FWT$(T x, h, J) = x$.

*Proof.* Keep the array $z = (a, y[m \ldots n-1])$, the current smooth block followed by the details already stored. Initially (line L3) $z = x$. A pass of lines L5 to L8 replaces the first $m$ entries of $z$ by $W_m a = (s, d)$, storing $d$ at positions $m/2, \ldots, m - 1$ and keeping $s$ as the new smooth block of length $m/2$; so it multiplies $z$ by $W_m \oplus I$. Each block length $m = n/2^{\ell - 1}$ for $\ell \le J$ is even because $2^J \mid n$. After $J$ passes and line L9, $y = T x$. Each factor is orthogonal by Theorem 1, so $T$ is orthogonal, with $T^{-1} = T^{\mathsf T} = W_n^{\mathsf T} (W_{n/2}^{\mathsf T} \oplus I) \cdots$. For the inverse, line L14 computes, for the block $(a, d)$ with $d = y[m \ldots 2m - 1]$,

$$b_c = \sum_{i < m} \sum_{l : 2i + l \equiv c \ (\mathrm{mod}\ 2m)} (h_l a_i + g_l d_i) = \sum_{r < 2m} (W_{2m})_{r, c} \, (a, d)_r = \left(W_{2m}^{\mathsf T} (a, d)\right)_c.$$

So the passes of lines L12 to L15 apply $W_{2m}^{\mathsf T}$ for $2m = n/2^{J-1}, \ldots, n$, in the reverse order of the forward passes, each to the leading block, while the details still to be used stay in place in $y$. This is $T^{\mathsf T}$, so INVERSE-FWT$(T x) = T^{\mathsf T} T x = x$. With $J = 0$, $T = I$ and both procedures return their input. $\square$

**Lemma 3 (counting).** For a filter $p$ of even length $L$ with $\sum_l p_l^2 = 1$, an even $m$ and a vector $a \in \mathbb{R}^m$, $\sum_{i < m/2} \left(\sum_l |p_l| \, |a_{(2i + l) \bmod m}|\right)^2 \le \frac{L}{2} \lVert a \rVert_2^2$.

*Proof.* By the Cauchy-Schwarz inequality the left side is at most $\sum_i \sum_l a_{(2i+l) \bmod m}^2$. For a fixed index $r$, the pairs $(i, l)$ with $2i + l \equiv r \pmod m$ are, for each $l$ with $l \equiv r \pmod 2$, exactly one $i \in [0, m/2)$, and none for the other $l$, because $m$ is even. There are $L/2$ such $l$, so each $a_r^2$ appears exactly $L/2$ times. $\square$

**Theorem 3 (rounding error).** Suppose the stored filter satisfies $|\hat h_l - h_l| \le \mu |h_l|$, so also $|\hat g_l - g_l| \le \mu |g_l|$, and each dot product of length $L$ in lines L6 and L7 is evaluated in floating point with unit roundoff $u$ and $\gamma_L = Lu/(1 - Lu)$. Then the computed $\hat y$ satisfies

$$\lVert \hat y - T x \rVert_2 \le J \sqrt L \, (\mu + \gamma_L) \, \lVert x \rVert_2 + O(u^2).$$

*Proof.* Let $z_0 = x$ and let $z_\ell$ be the computed array after the pass $\ell$, and write $M_\ell = W_{m_\ell} \oplus I$ with $m_\ell = n/2^{\ell-1}$. Lines L8 and L9 only copy, so $z_\ell = M_\ell z_{\ell-1} + e_\ell$, where $e_\ell$ is zero outside the first $m_\ell$ entries. Write $a$ for the first $m_\ell$ entries of $z_{\ell - 1}$. The standard bound for a dot product computed with perturbed coefficients gives, for each output, $|\hat s_i - s_i| \le \left(\mu + \gamma_L (1 + \mu)\right) \sum_l |h_l| \, |a_{(2i+l) \bmod m_\ell}|$, and the same with $g$ for $d_i$. Since $\sum_l h_l^2 = \sum_l g_l^2 = 1$, Lemma 3 for $h$ and for $g$ gives $\lVert e_\ell \rVert_2^2 \le (\mu + \gamma_L)^2 L \lVert a \rVert_2^2 + O(u^3)$, so $\lVert e_\ell \rVert_2 \le \sqrt L (\mu + \gamma_L) \lVert z_{\ell-1} \rVert_2 + O(u^2)$. By induction, using linearity, $z_J = M_J \cdots M_1 x + \sum_{\ell=1}^{J} M_J \cdots M_{\ell+1} e_\ell$. Each $M_k$ is orthogonal by Theorem 1, and $\lVert z_{\ell - 1} \rVert_2 = \lVert x \rVert_2 + O(u)$, so

$$\lVert \hat y - T x \rVert_2 \le \sum_{\ell=1}^{J} \lVert e_\ell \rVert_2 \le J \sqrt L \, (\mu + \gamma_L) \, \lVert x \rVert_2 + O(u^2). \qquad \square$$

The same argument, with Lemma 3 applied to the transposed sums of line L14 (each output $b_c$ is a sum of $L$ products, $L/2$ from each filter), gives a bound of the same form for INVERSE-FWT.

**Operation count.** The pass for the block length $m$ computes $m/2$ dot products of length $L$ with $h$ and $m/2$ with $g$: $L m$ multiplications and $(L - 1) m$ additions. Summing over $m = n, n/2, \ldots, n/2^{J-1}$ gives $L n (2 - 2^{1-J}) < 2 L n$ multiplications and $(L - 1) n (2 - 2^{1-J}) < 2 (L - 1) n$ additions. Line L2 costs nothing but sign changes. The inverse pass for the output length $2m$ does $2Lm$ multiplications and $2Lm$ additions, so less than $2 L n$ of each in total. Both procedures therefore run in $\Theta(L n)$ time, independent of $J$. $\blacksquare$
