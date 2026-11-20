---
title: ZF removes all interference, its noise covariance is N0 (H^H H)^-1, it is ML on orthogonal channels, and its diversity in i.i.d. Rayleigh fading is m - n + 1
proves: [correctness]
status: full
---

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$ of full column rank, $x \in \mathcal{S}^n$ and $w \sim \mathcal{CN}(0, N_0 I_m)$. Let $G = H^H H$ and $W = G^{-1} H^H$, as in lines L1 and L2. Let $h_k$ be column $k$ of $H$.

**Lemma 1 ($G$ is invertible).** If $H$ has full column rank, $G$ is Hermitian positive definite.

*Proof.* $G^H = H^H H = G$. For $u \ne 0$, $u^H G u = \|H u\|^2 > 0$, because $H u \ne 0$ when the columns are independent. A positive definite matrix has only positive eigenvalues, so it is invertible. $\square$

**Theorem 1 (no interference, exact without noise).** $W H = I_n$, so $z = W y = x + W w$. If $w = 0$, lines L4 and L5 return $x$.

*Proof.* $W H = G^{-1} H^H H = G^{-1} G = I_n$, so $W y = W H x + W w = x + W w$. If $w = 0$, then $z_k = x_k$, which is a point of $\mathcal{S}$, and the point of $\mathcal{S}$ nearest to $x_k$ is $x_k$ itself at distance 0. $\square$

**Lemma 2 (least squares).** $z = W y$ is the unique minimizer of $\|y - H u\|^2$ over $u \in \mathbb{C}^n$.

*Proof.* For any $u$, write $u = z + d$. Then $y - H u = (y - H z) - H d$, and $H^H (y - H z) = H^H y - G G^{-1} H^H y = 0$. So the cross term vanishes and $\|y - H u\|^2 = \|y - H z\|^2 + \|H d\|^2$. The second term is positive for $d \ne 0$ by full column rank. $\square$

**Theorem 2 (noise covariance and post-detection SNR).** The noise $W w$ at the output is $\mathcal{CN}(0, N_0 G^{-1})$. So $z_k = x_k + \nu_k$ with $\nu_k \sim \mathcal{CN}(0, N_0 [G^{-1}]_{kk})$, and the SNR of stream $k$ after ZF is $(E_s / N_0) / [G^{-1}]_{kk}$. Also $[G^{-1}]_{kk} = \|W_{k,:}\|^2$, the squared norm of row $k$ of $W$.

*Proof.* A linear map of a circularly symmetric Gaussian vector is circularly symmetric Gaussian, with covariance $E[W w w^H W^H] = N_0 W W^H = N_0 G^{-1} H^H H G^{-1} = N_0 G^{-1}$, because $G^{-1}$ is Hermitian. The diagonal entry $k$ of $W W^H$ is the squared norm of row $k$. $\square$

**Theorem 3 (ML on orthogonal channels).** If $G$ is diagonal, the decision of lines L4 and L5 is an ML decision.

*Proof.* By the proof of Lemma 2, $\|y - H x\|^2 = \|y - H z\|^2 + \|H(x - z)\|^2$ for every $x$. If $G = \mathrm{diag}(g_1, \ldots, g_n)$, then $\|H (x - z)\|^2 = (x - z)^H G (x - z) = \sum_k g_k |x_k - z_k|^2$. The first term does not depend on $x$, and each $g_k > 0$. So the minimum over $x \in \mathcal{S}^n$ is reached by minimizing each $|x_k - z_k|$ over $\mathcal{S}$ on its own, which is what line L5 does. $\square$

The orthogonality is needed. When $G$ is not diagonal, the cross terms $\bar d_i G_{ik} d_k$ couple the streams, and the nearest point per stream can be a worse vector, as the example on the page shows.

**Lemma 3 (geometry of the noise gain).** Let $P$ be the orthogonal projection onto the orthogonal complement of the span of the columns $h_j$, $j \ne k$. Then $1 / [G^{-1}]_{kk} = \|P h_k\|^2$.

*Proof.* Order the columns so that $k$ is the last one and write $H = [A \; h_k]$. The block inverse formula, with the [Schur complement](/schur-complement/) of the block $A^H A$, gives

$$[G^{-1}]_{kk} = \bigl(h_k^H h_k - h_k^H A (A^H A)^{-1} A^H h_k\bigr)^{-1} = \bigl(h_k^H (I - A (A^H A)^{-1} A^H) h_k\bigr)^{-1}.$$

The matrix $I - A (A^H A)^{-1} A^H$ is the projection $P$, which is Hermitian and idempotent, so $h_k^H P h_k = \|P h_k\|^2$. $\square$

**Theorem 4 (diversity $m - n + 1$; Tse and Viswanath, Section 8.3.1).** Let the entries of $H$ be i.i.d. $\mathcal{CN}(0, 1)$, with $m \ge n$. Then $1 / [G^{-1}]_{kk}$ has the Gamma distribution with shape $m - n + 1$ and scale 1, the distribution of a sum of $m - n + 1$ independent unit exponentials. With BPSK, the error probability of stream $k$ is

$$P_e = \Bigl(\frac{1 - \mu}{2}\Bigr)^{d} \sum_{i=0}^{d-1} \binom{d - 1 + i}{i} \Bigl(\frac{1 + \mu}{2}\Bigr)^{i}, \qquad d = m - n + 1, \quad \mu = \sqrt{\frac{\mathrm{SNR}}{1 + \mathrm{SNR}}},$$

which decays as $\binom{2d - 1}{d} (4\,\mathrm{SNR})^{-d}$. So the diversity order is $m - n + 1$.

*Proof.* The columns $h_j$, $j \ne k$, are independent of $h_k$. Condition on them. With probability 1 they span a subspace of dimension $n - 1$, so $P$ projects onto a fixed subspace of dimension $d = m - n + 1$. Pick an orthonormal basis $u_1, \ldots, u_d$ of that subspace. Since $h_k \sim \mathcal{CN}(0, I_m)$ is unitarily invariant, the coordinates $u_i^H h_k$ are i.i.d. $\mathcal{CN}(0, 1)$, and $\|P h_k\|^2 = \sum_i |u_i^H h_k|^2$ is a sum of $d$ independent unit exponentials. This law does not depend on the conditioning, so it holds unconditionally. By Lemma 3 and Theorem 2, stream $k$ is BPSK in Gaussian noise with the SNR $\gamma = \mathrm{SNR}\, \|P h_k\|^2$, so its error probability is $E[Q(\sqrt{2 \gamma})]$ with $\gamma$ a Gamma variable of shape $d$ and mean $d\,\mathrm{SNR}$. This is the same average as for maximal ratio combining over $d$ independent Rayleigh branches, which gives the closed form above and its high SNR limit. $\square$

So ZF with $m = n$ has diversity 1. The tests check Theorem 1 on random channels with 16-QAM, Theorem 2 by $W H = I$ and the row norms, Theorem 3 on channels with orthogonal columns, and Theorem 4 by the mean of $1 / [G^{-1}]_{11}$ and by a BPSK error count against the closed form with a Wilson interval.
