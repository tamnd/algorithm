---
title: Selected mapping sends the candidate with the lowest PAPR, never does worse than plain OFDM, and the receiver recovers the data exactly
proves: [correctness]
status: full
---

Let $X \in \mathbb{C}^N$ be the data, $P_1, \ldots, P_U \in \mathbb{C}^N$ the phase sequences with $|P_u[k]| = 1$ for all $u$ and $k$, and $P_1 = (1, \ldots, 1)$. Write $X_u = X \odot P_u$ for the elementwise product of line L2, $x_u$ for its oversampled symbol of line L3 and $r_u$ for its PAPR of line L4. We work in exact arithmetic.

**Lemma 1 (loop invariant).** After the iteration of line L1 for index $u$, the stored index $u^\ast$ satisfies $r_{u^\ast} = \min_{v \le u} r_v$, and $u^\ast$ is the smallest index that reaches this minimum.

*Proof.* By induction on $u$. For $u = 1$ the test of line L5 stores index 1. If the claim holds after $u - 1$, line L5 replaces $u^\ast$ by $u$ exactly when $r_u < r_{u^\ast}$, that is, when $r_u$ is smaller than all earlier values. If $r_u$ equals the minimum, the earlier, smaller index stays. $\square$

**Theorem 1 (the choice).** Line L6 returns an index $u^\ast$ with $r_{u^\ast} = \min_{1 \le u \le U} r_u$ and the symbol $x_{u^\ast}$. In particular $r_{u^\ast} \le r_1$, the PAPR of plain OFDM of $X$, and adding sequences to the table never raises the PAPR of the output.

*Proof.* Lemma 1 at $u = U$. Since $P_1$ is all ones, $x_1$ is the plain OFDM symbol. A table that contains the first $U$ sequences of a larger table takes the minimum over fewer values, which cannot be smaller. $\square$

**Theorem 2 (exact recovery).** If the receiver gets the subcarrier values $Y[k] = X_{u^\ast}[k]$ (an ideal channel, or after a perfect one-tap equalizer) and the index $u^\ast$, then $Y[k]\, \overline{P_{u^\ast}[k]} = X[k]$ for every $k$.

*Proof.* $Y[k]\, \overline{P_{u^\ast}[k]} = X[k]\, P_{u^\ast}[k]\, \overline{P_{u^\ast}[k]} = X[k]\, |P_{u^\ast}[k]|^2 = X[k]$. $\square$

Recovering the subcarrier values from the transmitted samples is the OFDM demodulator: the oversampled symbol $x_u = \sqrt L F_{LN}^H Z_u$ has the values $X_u$ in its $N$ in-band bins, and the forward FFT returns them.

**Lemma 3 (each candidate is distributed as plain OFDM).** If the $X[k]$ are i.i.d. and uniform on the QPSK points $\{(\pm 1 \pm j)/\sqrt 2\}$, and every $P_u[k]$ is in $\{1, -1, j, -j\}$, then for each fixed $u$ the vector $X_u$ has the same distribution as $X$, so $r_u$ has the same distribution as $r_1$.

*Proof.* Multiplication by $j$ maps the QPSK set onto itself and is a bijection. So for a fixed $u$, each $X_u[k] = X[k] P_u[k]$ is uniform on the QPSK set, and the components stay independent because each one depends only on its own $X[k]$. $\square$

**A rule, not a theorem.** Let $p(\gamma) = \Pr(r_1 > \gamma)$. Lemma 3 gives $\Pr(r_u > \gamma) = p(\gamma)$ for each $u$, and Theorem 1 gives

$$\Pr(r_{u^\ast} > \gamma) = \Pr(r_1 > \gamma, \ldots, r_U > \gamma) \le p(\gamma).$$

If the $U$ ratios were independent, the probability would be $p(\gamma)^U$. They are not independent, since all candidates come from the same $X$; the value $p(\gamma)^U$ is the usual design rule, and a simulation is needed to check it for a given table.
