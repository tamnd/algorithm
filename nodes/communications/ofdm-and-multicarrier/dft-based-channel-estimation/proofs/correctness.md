---
title: "The DFT-based estimate is an orthogonal projection onto the channels of L_t taps, exact without noise, with the noise cut by L_t / N"
proves: [correctness]
status: full
---

Notation. $N$ subcarriers, $j$ the imaginary unit. The DFT pair of the implementation is unnormalized: $\operatorname{dft}(g)[k] = \sum_n g[n] e^{-j 2\pi k n / N}$ and $\operatorname{idft}(G)[n] = \frac1N \sum_k G[k] e^{j 2\pi k n / N}$. With the unitary $F$, $F[k, n] = e^{-j 2\pi k n / N} / \sqrt N$, this is $\operatorname{dft} = \sqrt N F$ and $\operatorname{idft} = F^H / \sqrt N$. The channel has taps $h_0, \ldots, h_{L_t - 1}$ with $L_t \le N$, so $H = \operatorname{dft}(h)$ with $h$ padded by zeros. After the DFT, the receiver has $Y[k] = H[k] X[k] + W[k]$ with known nonzero $X[k]$ and independent $W[k] \sim \mathcal{CN}(0, N_0)$. Let $T$ be the diagonal matrix with ones in the first $L_t$ places and zeros elsewhere, and let $\mathcal S = \{\operatorname{dft}(g) : g[n] = 0 \text{ for } n \ge L_t\}$, the responses of channels with at most $L_t$ taps.

**Lemma 1 (the steps form a projection).** Lines L2 to L4 map a vector $G$ to $PG$ with $P = F T F^H$. $P$ is Hermitian, $P^2 = P$, its range is $\mathcal S$, and every diagonal entry of $P$ equals $L_t / N$.

*Proof.* Line L2 applies $F^H / \sqrt N$, line L3 applies $T$ and line L4 applies $\sqrt N F$, so the composition is $F T F^H$. It is Hermitian because $T$ is real diagonal, and $P^2 = F T F^H F T F^H = F T^2 F^H = P$ because $F^H F = I$ and $T^2 = T$. Its range is $F$ applied to the vectors supported on the first $L_t$ places, which is $\mathcal S$ (the factor $\sqrt N$ does not change a subspace). The diagonal entry is $P[k, k] = \sum_{l < L_t} |F[k, l]|^2 = L_t / N$. $\square$

**Theorem 1 (exact without noise).** Without noise, the algorithm returns $H$.

*Proof.* Line L1 gives $Y[k] / X[k] = H[k]$. $H \in \mathcal S$, and a projection leaves the vectors of its range unchanged, so $PH = H$. $\square$

**Theorem 2 (the noise).** With noise, the error of the output is $P E$, with $E[k] = W[k] / X[k]$ the error of the least squares estimate of line L1. Its mean squared error per subcarrier is $\frac{L_t}{N}$ times that of the least squares estimate:

$$\frac1N E \|P E\|^2 = \frac{L_t}{N} \cdot \frac1N \sum_k \frac{N_0}{|X[k]|^2}.$$

For $|X[k]| = 1$ this is $L_t N_0 / N$, against $N_0$ for least squares.

*Proof.* The output is $P(H + E) = H + PE$ by Theorem 1. The entries of $E$ are independent with variances $N_0 / |X[k]|^2$, so $E\|PE\|^2 = \operatorname{tr}(P\, \operatorname{diag}(N_0 / |X[k]|^2)\, P^H) = \sum_k (P^H P)[k, k]\, N_0 / |X[k]|^2$. With $P^H P = P$ and $P[k, k] = L_t / N$ from Lemma 1, the sum is $\frac{L_t}{N} \sum_k N_0 / |X[k]|^2$. $\square$

**Theorem 3 (least squares and maximum likelihood for the taps).** If $|X[k]| = 1$ for all $k$, the first $L_t$ outputs of line L3 are the least squares estimate of the taps from $Y$, which is also the maximum likelihood estimate in white Gaussian noise.

*Proof.* Write $Y = A h_{L} + W$ with $A = \operatorname{diag}(X)\, B$, where $B$ holds the first $L_t$ columns of the unnormalized DFT matrix. The least squares estimate is $(A^H A)^{-1} A^H Y$. The columns of $B$ are orthogonal with squared norm $N$, and $|X[k]| = 1$, so $A^H A = N I$ and the estimate is $\frac1N B^H \operatorname{diag}(X^*) Y = \frac1N B^H (Y / X)$, which is the first $L_t$ entries of $\operatorname{idft}(Y / X)$. In white Gaussian noise the log-likelihood is a constant minus $\|Y - A h_L\|^2 / N_0$, so the least squares estimate is the maximum likelihood estimate. $\square$

**The comb version (a theorem).** With pilots on $p_i = k_0 + iD$ for $i = 0, \ldots, P - 1$, $P = N / D$, and $L_t \le P$,

$$H[p_i] = \sum_{l < L_t} h_l e^{-j 2\pi (k_0 + iD) l / N} = \sum_{l < L_t} \left( h_l e^{-j 2\pi k_0 l / N} \right) e^{-j 2\pi i l / P},$$

because $D / N = 1 / P$. So an inverse DFT of size $P$ of the pilot estimates gives $h_l e^{-j 2\pi k_0 l / N}$ for $l < L_t$ and zero for the other $P - L_t$ places without noise. Multiplying by $e^{j 2\pi k_0 l / N}$ gives $h_l$, and a DFT of size $N$ gives $H$ on all subcarriers. With noise of variance $N_0$ on each pilot estimate, each output of the inverse DFT of size $P$ has the variance $N_0 / P$, the phase factors do not change it, and the DFT of size $N$ adds the $L_t$ independent tap errors with unit-modulus weights, so the mean squared error on every subcarrier is $L_t N_0 / P$.

**A delay between samples (a remark).** If a path has a delay that is not a whole number of samples, $H$ is not in $\mathcal S$ for any $L_t < N$: its inverse DFT has a sinc-like spread over all taps, including the taps near $N$ that stand for negative delays. The projection then has the bias $(I - P) H \ne 0$, which no amount of SNR removes. The tests measure this floor for a delay of 2.5 samples.
