---
title: RECONSTRUCT returns the image exactly for any deterministic EXPAND, and EXPAND keeps constants exactly under equal contribution
proves: [correctness]
status: full
---

Let $G_0 = I, G_1, \ldots, G_N$ be the levels that line L5 makes, with $G_l$ of size $W_l \times H_l$. Let $E_l$ be any function that maps an array of size $W_{l+1} \times H_{l+1}$ to one of size $W_l \times H_l$ and depends only on its argument (the same input gives the same output). BUILD and RECONSTRUCT both call $E_l$ for the step between level $l + 1$ and level $l$. The values lie in a ring in which subtraction and addition are exact: the integers, the rationals, or the reals of the [real RAM](/real-ram/).

**Claim 1 (exact reconstruction).** RECONSTRUCT applied to the output of BUILD returns $I$.

*Proof.* Lines L6 and L7 give $L_l = G_l - E_l(G_{l+1})$ for $0 \le l < N$ and $L_N = G_N$. Let $g^{(l)}$ be the value of $g$ after the pass of line L10 for level $l$, and $g^{(N)}$ the value set by line L9. We show $g^{(l)} = G_l$ by downward induction on $l$.

Base: $g^{(N)} = L_N = G_N$ by lines L9 and L7.

Step: assume $g^{(l+1)} = G_{l+1}$ for some $l$ with $0 \le l < N$. Line L10 sets $g^{(l)} = L_l + E_l(g^{(l+1)}) = L_l + E_l(G_{l+1})$, where the second equality uses the hypothesis and the fact that $E_l$ is a function. Substituting $L_l$ gives $g^{(l)} = G_l - E_l(G_{l+1}) + E_l(G_{l+1}) = G_l$, because subtraction and addition are exact and are done sample by sample on arrays of the same size $W_l \times H_l$.

The loop ends after the pass for $l = 0$, so line L11 returns $g^{(0)} = G_0 = I$. $\square$

The proof does not use the kernel, linearity, or the form of $E_l$. So it covers every kernel, including kernels that are not of equal contribution, and an EXPAND that rounds its output to integers, provided that both procedures use the same one.

**Claim 2 (constants).** Let $n \ge 2$ and $c$ be a constant. Let $z$ be the row of length $n$ with $z[k] = c$ for even $k$ and $z[k] = 0$ for odd $k$, which is line L1 applied to the constant row of length $\lceil n/2 \rceil$. Then the row filter of line L2, $e[x] = \sum_{m=-2}^{2} 2 \hat w(m)\, z[\rho_n(x - m)]$, gives $e[x] = c$ for all $x$ exactly when

$$
\hat w(-2) + \hat w(0) + \hat w(2) = \tfrac{1}{2} \quad\text{and}\quad \hat w(-1) + \hat w(1) = \tfrac{1}{2}.
$$

For a symmetric kernel with sum 1, these two conditions are the equal contribution rule $\hat w(0) + 2 \hat w(2) = 2 \hat w(1)$, and with $\hat w(0) = a$ they hold for every $a$ in the family $(1/4 - a/2, 1/4, a, 1/4, 1/4 - a/2)$.

*Proof.* First, $\rho_n$ keeps the parity of its argument. It reduces $k$ modulo $2n - 2$, which is even, and possibly replaces the result $i$ by $2n - 2 - i$; neither step changes the parity. Line L1 fills every even index $2i \le n - 1$, since the coarse row has $\lceil n/2 \rceil$ samples and $2(\lceil n/2 \rceil - 1) \le n - 1$. So $z[\rho_n(k)] = c$ if $k$ is even and $0$ if $k$ is odd, for every integer $k$.

If $x$ is even, $x - m$ is even exactly for $m \in \{-2, 0, 2\}$, so $e[x] = 2c\,(\hat w(-2) + \hat w(0) + \hat w(2))$. If $x$ is odd, $x - m$ is even exactly for $m \in \{-1, 1\}$, so $e[x] = 2c\,(\hat w(-1) + \hat w(1))$. Both equal $c$ for $c \ne 0$ exactly when the two sums are $1/2$. Since $n \ge 2$, both an even and an odd $x$ occur, so both conditions are needed.

For a symmetric kernel with sum 1, write $\hat w(0) = a$, $\hat w(\pm 1) = b$, $\hat w(\pm 2) = c'$, so $a + 2b + 2c' = 1$. The odd condition is $2b = 1/2$, that is $b = 1/4$, and then the even condition $a + 2c' = 1/2$ follows from the sum. Equal contribution $a + 2c' = 2b$ gives the same pair. The Burt and Adelson family has $b = 1/4$ and $a + 2(1/4 - a/2) = 1/2$. $\square$

The column pass of line L3 is the same 1D filter along the other axis, so in 2D a constant level expands to the same constant when both conditions hold and both sizes are at least 2. An axis of length 1 has no zeros, and EXPAND copies it unchanged, which also keeps constants. Then $L_l = c - c = 0$ for a constant image at every level $l < N$.

**A kernel without equal contribution.** For $\hat w = \frac{1}{9}(1, 2, 3, 2, 1)$ the even class sums to $5/9$ and the odd class to $4/9$. Along one axis a constant $c$ expands to $\frac{10}{9}c$ at even and $\frac{8}{9}c$ at odd positions, so in 2D the constant 9 becomes $100/9$, $80/9$ and $64/9$ at (even, even), (odd, even) and (odd, odd) positions. The bands of a flat image are then not zero, while Claim 1 still gives exact reconstruction.
