---
title: With exact correlations, a white input of unit power and subchannels with no common zero, the TXK steps return the channel up to a phase
proves: [correctness]
status: full
---

**Setting.** The window $Y[k] = H_N s[k] + n[k]$ has length $PN$, where $H_N$ is the $PN \times d$ block Toeplitz matrix with block $(i, m)$ equal to $h(m - i)$, $d = N + L - 1$, and $s[k] = (a[k], a[k-1], \ldots, a[k-d+1])$. The symbols are independent with $E a = 0$ and $E|a|^2 = 1$. The noise $n[k]$ stacks $w[k], \ldots, w[k-N+1]$, white with power $\sigma^2$ on each output and independent of the symbols. $J$ is the $d \times d$ matrix with $J_{i, j} = 1$ if $i = j + 1$ and $0$ otherwise, and $J_N$ is the same for size $N$. Indices start at 0, and $e_j$ is unit vector $j$.

**Lemma 1 (the correlations).** $R(0) = H_N H_N^H + \sigma^2 I$ and $R(1) = H_N J H_N^H + \sigma^2 (J_N \otimes I_P)$.

*Proof.* $E[s[k]_i\, \overline{s[k]_j}] = E[a[k-i]\, \overline{a[k-j]}] = \delta_{ij}$, so $E[s[k] s[k]^H] = I$. For lag 1, $E[s[k]_i\, \overline{s[k-1]_j}] = E[a[k-i]\, \overline{a[k-1-j]}]$, which is 1 if $i = j + 1$ and 0 otherwise, so $E[s[k] s[k-1]^H] = J$. For the noise, block $(i, j)$ of $E[n[k] n[k-1]^H]$ is $E[w[k-i]\, w[k-1-j]^H]$, which is $\sigma^2 I_P$ if $i = j + 1$ and 0 otherwise; this is $\sigma^2 (J_N \otimes I_P)$. The cross terms vanish by independence and zero means. $\square$

So line L1 gives $A_0 = H_N H_N^H$ and $A_1 = H_N J H_N^H$ exactly.

**Lemma 2 (rank).** If the subchannels have no common zero, $h(0) \ne 0$, $h(L-1) \ne 0$ and $N \ge L - 1$, then $H_N$ has full column rank $d$.

For $P = 2$ this is Lemma 1 in the proof on the [subspace identification](/subspace-channel-identification/) page, which is complete. For $P > 2$, a common zero of all subchannels is the only obstruction; this is the result of Tong, Xu and Kailath (1994) and Moulines and others (1995), cited and not proved here. If two of the $P$ subchannels already have no common zero, the $P = 2$ proof applies to their rows, and the full matrix, which has more rows, has full column rank as well.

**Theorem.** Under the conditions of Lemma 2, lines L1 to L9 return $\hat h = e^{j\theta} h$ for some real $\theta$.

*Proof.* By Lemma 2, $A_0 = H_N H_N^H$ is positive semidefinite with rank $d$, and its range equals the range of $H_N$. Line L2 takes $A_0 = U \Lambda U^H$ with $U$ of size $PN \times d$, orthonormal columns, and $\Lambda$ diagonal and positive. Then $U U^H$ is the orthogonal projector onto the range of $H_N$, so $U U^H H_N = H_N$.

*Step 1: V is unitary.* Let $F = \Lambda^{-1/2} U^H$ (line L3) and $V = F H_N$, a $d \times d$ matrix. Then
$$V V^H = \Lambda^{-1/2} U^H H_N H_N^H U \Lambda^{-1/2} = \Lambda^{-1/2} U^H (U \Lambda U^H) U \Lambda^{-1/2} = I.$$
A square matrix with $V V^H = I$ is unitary.

*Step 2: M.* Line L4 gives $M = F A_1 F^H = F H_N J H_N^H F^H = V J V^H$.

*Step 3: the null vector.* $M M^H = V J J^T V^H$, and $J J^T$ is diagonal with entries $(0, 1, \ldots, 1)$: row 0 of $J$ is zero and every other row has a single 1. So the eigenvalues of $M M^H$ are $0$ once and $1$ with multiplicity $d - 1$, and the eigenvector for $0$ is $V e_0$. Line L5 returns $v = e^{j\theta} V e_0$ for some $\theta$, since a unit eigenvector of a simple eigenvalue is fixed up to a unit scalar.

*Step 4: the walk.* $J e_l = e_{l+1}$ for $l < d - 1$, so $M^l V e_0 = V J^l V^H V e_0 = V J^l e_0 = V e_l$ for $l \le d - 1$. Since $L \le d$, after $l$ passes through line L8, $v = e^{j\theta} V e_l$ for $l = 0, \ldots, L - 1$.

*Step 5: back to the channel.* $U \Lambda^{1/2} V e_l = U \Lambda^{1/2} \Lambda^{-1/2} U^H H_N e_l = U U^H H_N e_l = H_N e_l$, which is column $l$ of $H_N$. Block 0 of that column is $h(l - 0) = h(l)$. So line L7 sets $\hat h(l) = e^{j\theta} h(l)$ for every $l$. $\square$

**The unknown noise power.** If $\sigma^2$ is not given, the code takes the mean of the $PN - d$ smallest eigenvalues of $R(0)$. By Lemma 1 and Lemma 2, $R(0)$ has exactly $PN - d$ eigenvalues equal to $\sigma^2$ and $d$ eigenvalues larger than $\sigma^2$, so the estimate is exact with exact statistics.

**Necessity of the condition.** Suppose every subchannel has the factor $(1 - z_0 z^{-1})$, with $z_0 \ne 0$ and $|z_0| \ne 1$, and let $h'$ be the channel in which this factor is replaced by $(-\bar z_0 + z^{-1})$ in every subchannel. On the unit circle $|{-\bar z_0} + e^{-j\omega}| = |1 - z_0 e^{-j\omega}|$, so the matrix spectrum $\sum_l \sum_{l'} h(l) h(l')^H e^{-j\omega (l - l')}$ of $h'$ equals that of $h$. With a white input, the output correlation at every lag is a Fourier coefficient of that spectrum, so $R(m)$ is the same for $h$ and $h'$ at every lag $m$. The two channels are not related by a scalar, so no method based on second-order statistics can identify the channel. The test `test_a_common_zero_flipped_by_an_allpass_gives_the_same_statistics` checks this for $z_0 = 0.5$.

**Remark on the white input.** If $E[s[k] s[k]^H] = R_a \ne I$ or the lag-1 input correlation is not $J$, then Step 1 gives $V V^H = \Lambda^{-1/2} U^H H_N R_a H_N^H U \Lambda^{-1/2}$ in place of the identity, and Step 3 fails. The input model is part of the method.
