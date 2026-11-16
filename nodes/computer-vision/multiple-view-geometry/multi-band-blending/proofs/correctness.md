---
title: Multi-band blending collapses the mixed bands exactly and reproduces the trivial blends
proves: [correctness]
status: full
---

We use the notation of the page. The images $A$, $B$ and the mask $M$ have size $W \times H$, with $W, H \ge 1$, and $N \ge 0$. Level $l$ has size $W_l \times H_l$ with $W_0 = W$, $H_0 = H$, $W_{l+1} = \lceil W_l / 2 \rceil$ and $H_{l+1} = \lceil H_l / 2 \rceil$. An image of size $w \times h$ is an $h \times w$ matrix. Let $\hat w = \frac{1}{16}(1, 4, 6, 4, 1)$, indexed by $k = -2, \ldots, 2$, and let $\rho_n(i)$ be the reflect-101 index of $i$ in $0, \ldots, n - 1$ (with $\rho_1(i) = 0$).

For $n \ge 1$ and $m = \lceil n / 2 \rceil$, define the $m \times n$ matrix $R_n$ and the $n \times m$ matrix $E_n$ by
$$(R_n)_{i, a} = \sum_{k : \rho_n(2i + k) = a} \hat w(k), \qquad (E_n)_{x, j} = \gamma_n \sum_{k : \rho_n(x - k) = 2j} \hat w(k),$$
with $\gamma_n = 2$ for $n > 1$ and $\gamma_1 = 1$. The code computes $\mathrm{REDUCE}(g) = R_{h} \, g \, R_{w}^{\mathsf T}$ for $g$ of size $w \times h$, since it filters each row with the taps $\hat w(k)$ at $\rho_w(2i + k)$ and then each column in the same way. It computes $\mathrm{EXPAND}(g)$ to size $w \times h$ as $E_{h} \, g \, E_{w}^{\mathsf T}$, since the zero-inserted grid is nonzero only at even indices $2j$, and the filter with gain $\gamma$ reads $\hat w(k)$ times the value at $\rho(x - k)$.

**Claim.** Let $S$ be the output of MULTI-BAND-BLEND$(A, B, M, N)$, and let $L^S_l$ be the bands of line L5.

(a) $S = C(L^S_0, \ldots, L^S_N)$, where the collapse $C$ is defined by $S_N = L^S_N$ and $S_l = L^S_l + \mathrm{EXPAND}(S_{l+1})$ to the size of level $l$, and $C(\ldots) = S_0$.

(b) If $M$ is the constant $c$, then $S = cA + (1 - c)B$. In particular $M = 1$ gives $S = A$ and $M = 0$ gives $S = B$.

(c) If $A = B$, then $S = A$ for every mask $M$.

(d) If $N = 0$, then $S = M \odot A + (1 - M) \odot B$.

(e) If every entry of $M$ is in $[0, 1]$, then every entry of every level $G^M_l$ is in $[0, 1]$, so each sample of $L^S_l$ is a convex combination of the matching samples of $L^A_l$ and $L^B_l$.

(f) For a fixed mask, $S$ is a linear function of the pair $(A, B)$.

**Lemma 1 (REDUCE takes weighted means).** Every entry of $R_n$ is non-negative, and every row of $R_n$ sums to 1. So REDUCE is linear, maps the constant image $c$ to the constant image $c$, and maps an image with all entries in $[0, 1]$ to an image with all entries in $[0, 1]$. EXPAND is linear.

*Proof.* Row $i$ of $R_n$ collects the five weights $\hat w(-2), \ldots, \hat w(2)$, each added to the column $\rho_n(2i + k)$. The map $\rho_n$ only decides into which column a weight goes; two weights may go to the same column, but none is lost and none is negative. So the row has non-negative entries with sum $\sum_k \hat w(k) = 16/16 = 1$. This also holds for $n = 1$, where all five weights go to column 0.

An entry of $\mathrm{REDUCE}(g)$ is $\sum_{a, b} (R_h)_{j, a} (R_w)_{i, b} \, g_{a, b}$. The coefficients $(R_h)_{j, a} (R_w)_{i, b}$ are non-negative and sum to $\big(\sum_a (R_h)_{j, a}\big)\big(\sum_b (R_w)_{i, b}\big) = 1$. So each entry is a weighted mean of the entries of $g$: it equals $c$ when $g$ is the constant $c$, and it lies between the least and the largest entry of $g$, hence in $[0, 1]$ when $g$ has entries in $[0, 1]$. Both REDUCE and EXPAND are products with fixed matrices on each side, so both are linear. $\square$

**Lemma 2 (the pyramids are linear).** For images $X$, $Y$ and reals $\alpha$, $\beta$, the Gaussian and Laplacian pyramids satisfy $G^{\alpha X + \beta Y}_l = \alpha G^X_l + \beta G^Y_l$ and $L^{\alpha X + \beta Y}_l = \alpha L^X_l + \beta L^Y_l$ for $l = 0, \ldots, N$.

*Proof.* For the Gaussian pyramid, use induction on $l$. Level 0 is the image itself. If the statement holds at level $l$, then level $l + 1$ is $\mathrm{REDUCE}(\alpha G^X_l + \beta G^Y_l) = \alpha G^X_{l+1} + \beta G^Y_{l+1}$ by Lemma 1. For $l < N$, $L_l = G_l - \mathrm{EXPAND}(G_{l+1})$ is a linear expression in the Gaussian levels, with EXPAND linear by Lemma 1, and $L_N = G_N$. $\square$

**Lemma 3 (collapse inverts the Laplacian pyramid).** For every image $X$ of size $W \times H$, $C(L^X_0, \ldots, L^X_N) = X$.

*Proof.* Let $S_l$ be the intermediate values of the collapse. We show $S_l = G^X_l$ by downward induction on $l$. For $l = N$, $S_N = L^X_N = G^X_N$. If $S_{l+1} = G^X_{l+1}$, then
$$S_l = L^X_l + \mathrm{EXPAND}(S_{l+1}) = \big(G^X_l - \mathrm{EXPAND}(G^X_{l+1})\big) + \mathrm{EXPAND}(G^X_{l+1}) = G^X_l .$$
Here both EXPAND terms are computed from the same array to the same size $W_l \times H_l$, so they are equal and cancel. At $l = 0$ this gives $S_0 = G^X_0 = X$. $\square$

The proof uses only that the same EXPAND appears in the build and in the collapse; with exact arithmetic (integers or fractions, as in the code) the cancellation is exact.

**Lemma 4 (the collapse is linear).** $C$ is a linear function of its $N + 1$ arguments, and $C(\Lambda_0, \ldots, \Lambda_N) = \sum_{l=0}^{N} \mathrm{EXPAND}^{(l)}(\Lambda_l)$, where $\mathrm{EXPAND}^{(0)}$ is the identity and $\mathrm{EXPAND}^{(l)}$ expands from level $l$ to level $l - 1$, then to level $l - 2$, and so on down to level 0.

*Proof.* By downward induction, $S_l = \sum_{k=l}^{N} \mathrm{EXPAND}^{(k \to l)}(\Lambda_k)$, where $\mathrm{EXPAND}^{(k \to l)}$ expands step by step from level $k$ to level $l$. This holds at $l = N$, and if it holds at $l + 1$, then $S_l = \Lambda_l + \mathrm{EXPAND}(S_{l+1}) = \Lambda_l + \sum_{k=l+1}^{N} \mathrm{EXPAND}^{(k \to l)}(\Lambda_k)$ by the linearity of EXPAND (Lemma 1). Take $l = 0$. A sum of linear maps is linear. $\square$

**Proof of the claim.**

(a) Lines L1 to L3 compute $G^M$, $G^A$, $G^B$, $L^A$ and $L^B$ as defined; in the code, `laplacian_from_gaussian` forms $L_l = G_l - \mathrm{EXPAND}(G_{l+1})$ for $l < N$ and keeps $L_N = G_N$. The loop L4 and L5 runs for $l = 0, \ldots, N$ and stores $L^S_l$. Line L6 sets $S = L^S_N = S_N$. The loop L7 and L8 runs for $l = N - 1$ down to 0. Before the pass for level $l$ the variable holds $S_{l+1}$, and line L8 replaces it by $L^S_l + \mathrm{EXPAND}(S_{l+1}) = S_l$. After the pass for $l = 0$, line L9 returns $S_0 = C(L^S_0, \ldots, L^S_N)$. If $N = 0$ the loop does not run and the output is $L^S_0 = S_0$.

(b) Let $M$ be the constant $c$. By Lemma 1 and induction on $l$, every level $G^M_l$ is the constant $c$. So line L5 gives $L^S_l = c L^A_l + (1 - c) L^B_l$, which is $L^{cA + (1 - c)B}_l$ by Lemma 2. By (a) and Lemma 3, $S = C(L^{cA + (1 - c)B}) = cA + (1 - c)B$. For $c = 1$ this is $A$, and for $c = 0$ it is $B$.

(c) If $A = B$, then $L^A_l = L^B_l$ and line L5 gives $L^S_l = G^M_l \odot L^A_l + (1 - G^M_l) \odot L^A_l = L^A_l$, whatever $G^M_l$ is. By (a) and Lemma 3, $S = A$.

(d) If $N = 0$, then $G^M_0 = M$ and $L^A_0 = G^A_0 = A$, $L^B_0 = B$. So $L^S_0 = M \odot A + (1 - M) \odot B$, and by (a) the output is $L^S_0$.

(e) $G^M_0 = M$ has entries in $[0, 1]$, and each next level is REDUCE of the previous one, so by Lemma 1 and induction every level has entries in $[0, 1]$. A sample of $L^S_l$ is $g a + (1 - g) b$ with $g \in [0, 1]$, a convex combination of $a$ and $b$.

(f) For a fixed $M$ the levels $G^M_l$ are fixed. The map $(A, B) \mapsto (L^A_l, L^B_l)$ is linear by Lemma 2, line L5 is linear in $(L^A_l, L^B_l)$ for fixed weights, and $C$ is linear by Lemma 4. A composition of linear maps is linear. $\blacksquare$

**Remark (the result is not a convex mix of pixels).** Part (e) holds for each band, but not for the collapsed image. The bands $L_l$ for $l < N$ take both signs, and the sum of Lemma 4 adds the mixed bands without any check on the range. For $A = (0, 0, 0, 0, 16, 16, 16, 16)$, $B = 16$ everywhere, $M = (1, 1, 1, 1, 1, 1, 0, 0)$, one row, and $N = 1$, the fifth output pixel is $1039/64 > 16$, larger than every input pixel. The test file checks this value.

**Remark (termination and cost).** The loops run $N + 1$ and $N$ times, and each REDUCE, EXPAND or mix touches each sample of its level a fixed number of times, which gives the bound $\Theta(W H + N)$ of the page.
