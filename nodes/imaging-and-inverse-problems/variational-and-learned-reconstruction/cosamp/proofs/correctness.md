---
title: One CoSaMP iteration contracts the error by a factor below 1/2 when delta_4s <= 0.1, up to a fixed multiple of the noise
proves: [correctness, convergence-rate]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix, $x \in \mathbb{R}^n$ has at most $s$ nonzero entries, and $y = Ax + e$. For a set $T$ of indices, $A_T$ holds the columns in $T$, $v_T$ is the restriction of $v$ to $T$ and $T^c$ is the complement. $H_s(v)$ keeps the $s$ entries of largest magnitude. The restricted isometry constant $\delta_k$ is the smallest $\delta$ with $(1 - \delta)\|z\|^2 \le \|Az\|^2 \le (1 + \delta)\|z\|^2$ for all $z$ with at most $k$ nonzero entries; it does not decrease with $k$. We write $\delta = \delta_{4s}$ and assume $\delta < 1$.

One iteration starts from an $s$-sparse vector $a$ and computes:

1. the proxy $p = A^T(y - Aa)$ and the set $\Omega$ of the indices of its $2s$ largest entries;
2. the merged set $T = \Omega \cup \operatorname{supp}(a)$, with $|T| \le 3s$;
3. the least squares solution $b$ with $b_T = \arg\min_z \|y - A_Tz\|$ and $b_{T^c} = 0$;
4. the pruned vector $a' = H_s(b)$.

**Theorem.** With $c = \delta/(1 - \delta)$,

$$\|x - a'\| \le \rho\,\|x - a\| + \tau\,\|e\|,\qquad \rho = \frac{4\delta\sqrt{1 + c^2}}{1 - \delta},\qquad \tau = \frac{4\sqrt{1 + c^2}\sqrt{1 + \delta}}{1 - \delta} + \frac{2}{\sqrt{1 - \delta}}.$$

For $\delta = 0.1$ this gives $\rho \approx 0.4472$ and $\tau \approx 6.798$, and $\rho < 1$ holds for $\delta$ up to about $0.1954$. When $\rho < 1$, the iterates from $a^0 = 0$ satisfy $\|x - a^k\| \le \rho^k\|x\| + \tau\|e\|/(1 - \rho)$, which is about $12.3\|e\|$ in the limit at $\delta = 0.1$.

## Two facts about restricted isometries

**Lemma 1.** If $|U| \le k$, every eigenvalue of $A_U^TA_U$ lies in $[1 - \delta_k, 1 + \delta_k]$. Hence $\|A_U^Tw\| \le \sqrt{1 + \delta_k}\,\|w\|$ for all $w$, $\|A_U^TA_Uz\| \ge (1 - \delta_k)\|z\|$, and the pseudoinverse satisfies $\|A_U^+\| \le 1/\sqrt{1 - \delta_k}$ and $\|(A_U^TA_U)^{-1}\| \le 1/(1 - \delta_k)$.

*Proof.* The Rayleigh quotient of $A_U^TA_U$ is $\|A_Uz\|^2/\|z\|^2 \in [1 - \delta_k, 1 + \delta_k]$. The singular values of $A_U$ are the square roots of these eigenvalues, and $\|A_U^+\|$ is the inverse of the smallest one. $\square$

**Lemma 2.** If $U$ and $V$ are disjoint and $|U| + |V| \le k$, then $\|A_U^TA_V\| \le \delta_k$.

*Proof.* Let $W = U \cup V$. The matrix $A_W^TA_W - I$ has norm at most $\delta_k$ by Lemma 1, and $A_U^TA_V$ is its off-diagonal block (the identity has no entries there). The norm of a block is at most the norm of the whole matrix. $\square$

## Proof of the theorem

Let $d = x - a$ and $R = \operatorname{supp}(d)$, so $|R| \le 2s$. The residual is $y - Aa = A_Rd_R + e$.

**Step 1 (identification).** We show $\|d_{\Omega^c}\| \le \frac{2\delta}{1 - \delta}\|d\| + \frac{2\sqrt{1 + \delta}}{1 - \delta}\|e\|$.

Since $\Omega$ holds the $2s$ largest entries of $p$ and $|R| \le 2s$, we have $\|p_R\|^2 \le \|p_\Omega\|^2$. Remove the common part $R \cap \Omega$: $\|p_{R \setminus \Omega}\| \le \|p_{\Omega \setminus R}\|$.

Upper bound: $p_{\Omega \setminus R} = A_{\Omega \setminus R}^TA_Rd_R + A_{\Omega \setminus R}^Te$. The sets $\Omega \setminus R$ and $R$ are disjoint with at most $4s$ elements together, so Lemma 2 and Lemma 1 give $\|p_{\Omega \setminus R}\| \le \delta\|d\| + \sqrt{1 + \delta}\,\|e\|$.

Lower bound: split $A_Rd_R = A_{R \setminus \Omega}d_{R \setminus \Omega} + A_{R \cap \Omega}d_{R \cap \Omega}$. Then

$$p_{R \setminus \Omega} = A_{R \setminus \Omega}^TA_{R \setminus \Omega}d_{R \setminus \Omega} + A_{R \setminus \Omega}^TA_{R \cap \Omega}d_{R \cap \Omega} + A_{R \setminus \Omega}^Te,$$

and by the two lemmas $\|p_{R \setminus \Omega}\| \ge (1 - \delta)\|d_{R \setminus \Omega}\| - \delta\|d\| - \sqrt{1 + \delta}\,\|e\|$.

Combine the two bounds: $(1 - \delta)\|d_{R \setminus \Omega}\| \le 2\delta\|d\| + 2\sqrt{1 + \delta}\,\|e\|$. Since $d$ vanishes off $R$, $d_{\Omega^c} = d_{R \setminus \Omega}$, which proves the claim.

**Step 2 (merge).** $a$ vanishes off $T$, so $x_{T^c} = d_{T^c}$. Since $T^c \subseteq \Omega^c$, $\|x_{T^c}\| \le \|d_{\Omega^c}\|$.

**Step 3 (least squares).** We show $\|x - b\| \le \sqrt{1 + c^2}\,\|x_{T^c}\| + \|e\|/\sqrt{1 - \delta}$.

Write $y = A_Tx_T + A_{T^c}x_{T^c} + e$. The least squares solution is $b_T = A_T^+y$, and $A_T^+A_T = I$ because $A_T$ has full column rank ($|T| \le 3s$ and $\delta_{3s} \le \delta < 1$). So

$$x_T - b_T = -A_T^+(A_{T^c}x_{T^c} + e) = -(A_T^TA_T)^{-1}A_T^TA_{T^c}x_{T^c} - A_T^+e.$$

The vector $x_{T^c}$ has at most $s$ nonzero entries, on a set disjoint from $T$, so Lemma 2 (with at most $4s$ indices) and Lemma 1 give $\|x_T - b_T\| \le c\|x_{T^c}\| + \|e\|/\sqrt{1 - \delta}$. Now $\|x - b\|^2 = \|x_{T^c}\|^2 + \|x_T - b_T\|^2$, and the triangle inequality in $\mathbb{R}^2$ for the vectors $(\|x_{T^c}\|, c\|x_{T^c}\|)$ and $(0, \|e\|/\sqrt{1 - \delta})$ gives the claim.

**Step 4 (prune).** $a' = H_s(b)$ is the best $s$-sparse approximation of $b$ (keeping the largest entries minimizes the discarded energy), and $x$ is $s$-sparse, so $\|b - a'\| \le \|b - x\|$. Hence $\|x - a'\| \le \|x - b\| + \|b - a'\| \le 2\|x - b\|$.

**Conclusion.** Chain the four steps:

$$\|x - a'\| \le 2\sqrt{1 + c^2}\left(\frac{2\delta}{1 - \delta}\|d\| + \frac{2\sqrt{1 + \delta}}{1 - \delta}\|e\|\right) + \frac{2}{\sqrt{1 - \delta}}\|e\| = \rho\|x - a\| + \tau\|e\|.$$

If $\rho < 1$, induction from $a^0 = 0$ gives $\|x - a^k\| \le \rho^k\|x\| + \tau\|e\|(1 + \rho + \dots + \rho^{k-1}) \le \rho^k\|x\| + \tau\|e\|/(1 - \rho)$. $\square$

## Remarks

The proof uses the restricted isometry property only on the set $U = \operatorname{supp}(x) \cup \operatorname{supp}(a) \cup \Omega$, which has at most $4s$ elements. So the one-step bound holds for every matrix with $\delta$ replaced by $\|I - A_U^TA_U\|$, whenever that number is below 1. The test file checks this local form on a Gaussian matrix.

Needell and Tropp (2009) prove the invariant $\|x - a^{k+1}\| \le 0.5\|x - a^k\| + 10\nu$ under $\delta_{4s} \le 0.1$, where $\nu$ is the unrecoverable energy: the noise norm plus terms from the tail of $x$, which vanish when $x$ is exactly $s$-sparse. The argument above has the same four steps with simpler constants and treats only exactly sparse $x$. For a general $x$, apply it to the best $s$-term approximation $x_s$ and put $A(x - x_s)$ into the noise.
