---
title: The PTS search finds the best phase factors with one transform per subblock, and the receiver recovers the data exactly
proves: [correctness]
status: full
---

Let $X \in \mathbb{C}^N$ be the data and let the subcarriers be split into disjoint subblocks $S_1, \ldots, S_V$ that cover $\{0, \ldots, N-1\}$. Let $W$ be a finite set of complex numbers of magnitude 1 (for example $\{1, -1, j, -j\}$). For a vector $b = (b_1, \ldots, b_V)$, the rotated data are $X_b[k] = b_v X[k]$ for $k \in S_v$. Write $T$ for the map of line L2 from $N$ subcarrier values to the oversampled symbol, $T(Y) = \sqrt L F_{LN}^H Z(Y)$, where $Z(Y)$ puts $(L - 1)N$ zeros in the middle of $Y$. We work in exact arithmetic.

**Lemma 1 (linearity).** $T$ is linear, so with $x_v = T(X \cdot 1_{S_v})$, the symbol of the subblock $v$ alone,

$$T(X_b) = \sum_{v=1}^V b_v\, x_v \quad \text{for every } b.$$

*Proof.* $Z$ is a linear map, since it only places values and zeros, and $F_{LN}^H$ is linear. The rotated data are $X_b = \sum_v b_v\, (X \cdot 1_{S_v})$, because the subblocks are disjoint and cover all subcarriers. Apply $T$ to both sides. $\square$

So line L5 computes the exact oversampled symbol of $X_b$, the one a direct inverse FFT of $X_b$ would give.

**Lemma 2 (loop invariant).** After the iterations of line L4 over a prefix of $W^{V-1}$ in its fixed order, the stored value $\mathit{best}$ is the minimum of $\mathrm{PAPR}(T(X_b))$ over the vectors $b = (1, b_2, \ldots, b_V)$ seen so far, and $b^\ast$ is the first vector that reaches it.

*Proof.* By induction on the number of iterations. Before the loop $\mathit{best} = \infty$ (line L3). Line L7 replaces the stored pair exactly when the new PAPR is strictly smaller than the stored minimum, so the minimum is kept, and on a tie the earlier vector stays. $\square$

**Theorem 1 (the search is exact).** Line L8 returns a vector $b^\ast$ with $b^\ast_1 = 1$ that minimizes $\mathrm{PAPR}(T(X_b))$ over all $b \in \{1\} \times W^{V-1}$, and the symbol $T(X_{b^\ast})$.

*Proof.* Lemma 2 at the end of the loop, which visits every element of $W^{V-1}$ once, and Lemma 1 for the symbol. $\square$

**Lemma 3 (fixing $b_1$ loses nothing).** For any $c$ with $|c| = 1$, $\mathrm{PAPR}(T(X_{cb})) = \mathrm{PAPR}(T(X_b))$. So if $W$ is closed under division (a group, such as $\{\pm 1\}$ or $\{\pm 1, \pm j\}$), the minimum over $\{1\} \times W^{V-1}$ equals the minimum over all of $W^V$.

*Proof.* $T(X_{cb}) = c\, T(X_b)$ by linearity, and multiplying every sample by $c$ with $|c| = 1$ changes neither $|x[m]|^2$ nor the mean power. For $b \in W^V$ take $c = 1/b_1 = \overline{b_1}$; then $cb$ has first entry 1 and, since $W$ is a group, all its entries in $W$. $\square$

**Theorem 2 (never worse than OFDM, and exact recovery).** The returned PAPR is at most the PAPR of plain OFDM of $X$. If the receiver gets $Y[k] = X_{b^\ast}[k]$ and knows $b^\ast$ and the partition, then $Y[k]\, \overline{b^\ast_v} = X[k]$ for $k \in S_v$.

*Proof.* The vector $b = (1, \ldots, 1)$ is in the search space and gives $X_b = X$, so Theorem 1 gives the first claim. For the second, $Y[k]\, \overline{b^\ast_v} = X[k]\, |b^\ast_v|^2 = X[k]$. $\square$
