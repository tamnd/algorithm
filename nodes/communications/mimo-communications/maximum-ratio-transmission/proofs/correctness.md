---
title: MRT maximizes the received SNR, its MIMO form reaches the top eigenvalue of H^H H, and its SNR law in Rayleigh fading is that of maximal ratio combining
proves: [correctness]
status: full
---

The single-antenna receiver sees $y = h^H x + w$ with $h \in \mathbb{C}^M$, $w \sim \mathcal{CN}(0, N_0)$ and one unit-power symbol $s$ sent as $x = f s$ with $\|f\|^2 \le P$. Lines L1 and L2 set $f = \sqrt{P}\, h / \|h\|$.

**Theorem 1 (best beamformer for one receive antenna).** For every $f$ with $\|f\|^2 \le P$, the SNR $|h^H f|^2 / N_0$ is at most $P \|h\|^2 / N_0$, and the MRT vector reaches this value. Any optimal $f$ equals $e^{j\phi} \sqrt{P}\, h / \|h\|$ for some phase $\phi$.

*Proof.* By the Cauchy-Schwarz inequality, $|h^H f|^2 \le \|h\|^2 \|f\|^2 \le P \|h\|^2$. Equality in Cauchy-Schwarz holds only if $f$ is a multiple of $h$, and equality in the second step needs $\|f\|^2 = P$. For the MRT vector, $h^H f = \sqrt{P}\, h^H h / \|h\| = \sqrt{P}\, \|h\|$, a positive real number, so the SNR is $P \|h\|^2 / N_0$. $\square$

So the receiver gets $y = \sqrt{P}\, \|h\|\, s + w$: the contributions of all $M$ antennas add in phase, and the SNR gain over one antenna with the same total power is $\|h\|^2$.

**Theorem 2 (several receive antennas).** Let $y = H x + w$ with $H \in \mathbb{C}^{N_r \times M}$, $w \sim \mathcal{CN}(0, N_0 I)$, $x = f s$ with $\|f\|^2 \le P$, and a receive vector $c$ with $\|c\| = 1$, so the SNR after combining is $|c^H H f|^2 / N_0$. The largest value over $f$ and $c$ is $\lambda_{\max}(H^H H)\, P / N_0$. It is reached by $f = \sqrt{P}\, v$ with $v$ a unit top eigenvector of $H^H H$ and $c = H v / \|H v\|$, the output of lines L5 and L6.

*Proof.* For a fixed $f$, Cauchy-Schwarz gives $|c^H H f|^2 \le \|H f\|^2$, with equality for $c = H f / \|H f\|$; this is [maximal ratio combining](/maximal-ratio-combining/). Then $\|H f\|^2 = f^H H^H H f$. Write $f$ in an orthonormal eigenbasis $e_1, \ldots, e_M$ of the Hermitian matrix $G = H^H H$, with the eigenvalues $\lambda_1 \ge \cdots \ge \lambda_M \ge 0$: $f = \sum_i a_i e_i$ gives $f^H G f = \sum_i \lambda_i |a_i|^2 \le \lambda_1 \sum_i |a_i|^2 \le \lambda_1 P$, with equality for $f = \sqrt{P}\, e_1$. $\square$

**Lemma 1 (power iteration).** Let $\lambda_1 > \lambda_2$ and let the start vector $z_0$ have $e_1^H z_0 \ne 0$. Then $G^t z_0 / \|G^t z_0\|$ approaches the line through $e_1$, with an error angle whose tangent is at most $(\lambda_2 / \lambda_1)^t \tan \theta_0$, where $\theta_0$ is the angle between $z_0$ and $e_1$. Among the nonzero columns of $G$, at least one is such a start.

*Proof.* Write $z_0 = \sum_i a_i e_i$ with $a_1 \ne 0$. Then $G^t z_0 = \sum_i \lambda_i^t a_i e_i$, and the ratio of the norm of the part orthogonal to $e_1$ to the part along $e_1$ is $\bigl(\sum_{i \ge 2} \lambda_i^{2t} |a_i|^2\bigr)^{1/2} / (\lambda_1^t |a_1|) \le (\lambda_2/\lambda_1)^t \bigl(\sum_{i \ge 2} |a_i|^2\bigr)^{1/2} / |a_1|$. The normalization and the phase fix of line L4 do not change the line. For the start: $e_1^H G e_k = (G e_1)^H e_k = \lambda_1 \overline{(e_1)_k}$. Since $e_1$ is not zero, some entry $(e_1)_k$ is not zero, and for that $k$ column $k$ of $G$ is a valid start. The code runs from every nonzero column and keeps the largest Rayleigh quotient $v^H G v$, which is the result of that good start or a value at least as large; by the proof of Theorem 2 no unit vector has a Rayleigh quotient above $\lambda_1$. $\square$

If $\lambda_1 = \lambda_2$, every unit vector of the top eigenspace is optimal, and power iteration converges to one of them.

**Theorem 3 (SNR law in Rayleigh fading).** If the entries of $h$ are i.i.d. $\mathcal{CN}(0, 1)$, the MRT SNR $\gamma = P \|h\|^2 / N_0$ has the Gamma distribution with shape $M$ and mean $M P / N_0$, the same law as the output SNR of maximal ratio combining over $M$ branches. With BPSK and $\bar\gamma = P / N_0$, the bit error probability is

$$P_b = \Bigl(\frac{1 - \mu}{2}\Bigr)^{M} \sum_{i=0}^{M-1} \binom{M - 1 + i}{i} \Bigl(\frac{1 + \mu}{2}\Bigr)^{i}, \qquad \mu = \sqrt{\frac{\bar\gamma}{1 + \bar\gamma}},$$

so the diversity order is $M$.

*Proof.* $\|h\|^2 = \sum_i |h_i|^2$ is a sum of $M$ independent unit exponentials, which is Gamma with shape $M$. By Theorem 1 the receiver sees $y = \sqrt{P}\, \|h\|\, s + w$, a real positive gain on BPSK, so the conditional error probability is $Q(\sqrt{2 \gamma})$. Its average over the Gamma law is the classical MRC result for $M$ independent Rayleigh branches with the average branch SNR $\bar\gamma$, which is the formula above. $\square$

For $M = 2$ and $\bar\gamma = 10$ dB the formula gives $P_b = 1.5991 \times 10^{-3}$, the MRC check value of the area.

**Lemma 2 (multiuser interference with conjugate beamforming).** For $K$ users with $w_k = \sqrt{P/K}\, h_k / \|h_k\|$ (line L7), the total power is $P$, and the interference that user $k$ gets from user $j$ is $(P/K)\, |h_k^H h_j|^2 / \|h_j\|^2$. It vanishes if the channels are orthogonal. If $h_k$ and $h_j$ are independent with i.i.d. $\mathcal{CN}(0, 1)$ entries, the unit vectors $u = h_k / \|h_k\|$ and $v = h_j / \|h_j\|$ satisfy $E|u^H v|^2 = 1/M$.

*Proof.* $\sum_k \|w_k\|^2 = K \cdot P/K = P$. The interference term is $|h_k^H w_j|^2$, which is the expression above. For the mean, condition on $u$. The vector $v$ is uniform on the unit sphere of $\mathbb{C}^M$ and independent of $u$, so $E|u^H v|^2 = u^H E[v v^H] u$. By symmetry $E[v v^H] = c I$, and its trace is $E\|v\|^2 = 1$, so $c = 1/M$ and $E|u^H v|^2 = \|u\|^2 / M = 1/M$. $\square$

So the interference relative to the signal power $(P/K)\|h_k\|^2$ falls as $1/M$; this is the [favorable propagation](/favorable-propagation/) effect that makes conjugate beamforming work in [massive MIMO](/massive-mimo/).

The tests check Theorem 1 against random unit vectors and a grid over all unit vectors of $\mathbb{C}^2$, the example values 7, 4 and 3, Theorem 2 by the eigenvector equation, the combined gain and random unit vectors, Lemma 1 on a matrix whose largest column is orthogonal to the top eigenvector, Theorem 3 by a BPSK error count with a Wilson interval, and Lemma 2 by the power, orthogonal channels and the sample mean of $|u^H v|^2$.
