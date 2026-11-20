---
title: With a cyclic prefix of at least L-1 samples, one tap per DFT bin gives the zero-forcing and the block MMSE equalizers exactly, with the stated mean squared errors
proves: [correctness]
status: full
---

The channel taps are $h_0, \ldots, h_{L-1}$. A block $x = (x_0, \ldots, x_{N-1})$ of independent zero-mean symbols with $E|x_n|^2 = E_s$ is sent as $s = (x_{N-P}, \ldots, x_{N-1}, x_0, \ldots, x_{N-1})$, a cyclic prefix of $P$ samples followed by the block. The received samples are $r_i = \sum_l h_l s_{i-l} + w_i$ with $w$ white $\mathcal{CN}(0, N_0)$, where $s_{i-l}$ for $i - l < 0$ are samples of the previous block. The DFT is unnormalized: $X_k = \sum_n x_n e^{-j 2\pi kn/N}$, and the inverse has the factor $1/N$. Write $H_k$ for the DFT of $h$ padded with zeros to length $N$ (line L3).

**Lemma 1 (the prefix makes the convolution circular).** If $P \ge L - 1$, then after the prefix is removed (line L1), $y_n = r_{P+n} = \sum_l h_l x_{(n-l) \bmod N} + w_{P+n}$ for $n = 0, \ldots, N-1$, whatever the previous block was.

*Proof.* $r_{P+n}$ uses $s_{P+n-l}$ for $0 \le l \le L-1$. The index $P + n - l \ge P - (L-1) \ge 0$, so no sample of the previous block enters. If $n - l \ge 0$, then $s_{P+n-l} = x_{n-l}$. If $n - l < 0$, then $P + n - l$ is in the prefix and $s_{P+n-l} = x_{N+n-l} = x_{(n-l) \bmod N}$. $\square$

**Lemma 2 (one tap per bin).** With $Y = \mathrm{DFT}(y)$ (line L2), $Y_k = H_k X_k + W_k$, where the $W_k$ are i.i.d. $\mathcal{CN}(0, N N_0)$.

*Proof.* The DFT of a circular convolution is the product of the DFTs. The DFT matrix $\mathbf{F}$ has $\mathbf{F}^H \mathbf{F} = N \mathbf{I}$, so $W = \mathbf{F} w$ has the covariance $N N_0 \mathbf{I}$, and it is circular Gaussian as a linear map of $w$. $\square$

In matrix form, $y = \mathbf{C} x + w$ with the circulant matrix $\mathbf{C}_{nm} = h_{(n-m) \bmod N}$ (zero where the index is $L$ or more). With the unitary $\mathbf{U} = \mathbf{F}/\sqrt N$, Lemma 2 says $\mathbf{C} = \mathbf{U}^H \Lambda \mathbf{U}$ with $\Lambda = \mathrm{diag}(H_0, \ldots, H_{N-1})$.

**Theorem 1 (zero forcing).** If every $H_k \ne 0$, lines L4 and L6 give $\hat x = x + \mathrm{IDFT}(W_k / H_k)$. Without noise $\hat x = x$. The noise in each output sample has the variance $\frac{N_0}{N} \sum_k |H_k|^{-2}$.

*Proof.* $\hat X_k = Y_k / H_k = X_k + W_k / H_k$. The noise sample $n$ is $\frac1N \sum_k e^{j2\pi kn/N} W_k/H_k$, a sum of independent terms, so its variance is $\frac{1}{N^2} \sum_k N N_0 / |H_k|^2$. $\square$

**Theorem 2 (MMSE).** Lines L5 and L6 compute $\hat x = (\mathbf{C}^H \mathbf{C} + \gamma \mathbf{I})^{-1} \mathbf{C}^H y$ with $\gamma = N_0/E_s$, which is the linear MMSE estimate of $x$ from $y$.

*Proof.* The linear MMSE estimate of $x$ with covariance $E_s \mathbf{I}$ from $y = \mathbf{C} x + w$ is $E_s \mathbf{C}^H (E_s \mathbf{C}\mathbf{C}^H + N_0 \mathbf{I})^{-1} y$, which equals $(\mathbf{C}^H \mathbf{C} + \gamma \mathbf{I})^{-1} \mathbf{C}^H y$ by the push-through identity. Substitute $\mathbf{C} = \mathbf{U}^H \Lambda \mathbf{U}$: the matrix is $\mathbf{U}^H \mathrm{diag}\big(\bar H_k / (|H_k|^2 + \gamma)\big) \mathbf{U}$. Applying it to $y$ is the DFT, one multiplication per bin and the inverse DFT, because $\mathbf{U}^H \mathbf{D} \mathbf{U} y = \mathbf{F}^{-1} \mathbf{D} \mathbf{F} y$. $\square$

**Theorem 3 (the MMSE value).** Each output sample of the MMSE equalizer has the mean squared error
$$J = \frac{1}{N} \sum_{k=0}^{N-1} \frac{N_0 E_s}{E_s |H_k|^2 + N_0}.$$

*Proof.* The error covariance of the linear MMSE estimate is $(E_s^{-1} \mathbf{I} + N_0^{-1} \mathbf{C}^H \mathbf{C})^{-1} = \mathbf{U}^H \mathrm{diag}\big(N_0 E_s/(N_0 + E_s |H_k|^2)\big) \mathbf{U}$. This matrix is circulant, so all diagonal entries are equal to the trace divided by $N$, and the trace is the sum of the eigenvalues. $\square$

**Corollary 1 (bias and SINR).** The MMSE output is $\hat x_n = g\, x_n + v_n$ with $g = 1 - J/E_s$ and $v_n$ uncorrelated with $x_n$, of variance $gJ$. So the unbiased output $\hat x_n / g$ has the SINR $E_s/J - 1$.

*Proof.* The output is $\hat x = \mathbf{A} x + \mathbf{B} w$ with $\mathbf{A} = \mathbf{U}^H \mathrm{diag}\big(|H_k|^2/(|H_k|^2 + \gamma)\big) \mathbf{U}$, a circulant matrix with all diagonal entries $g = \frac1N \sum_k |H_k|^2/(|H_k|^2 + \gamma) = 1 - \frac1N \sum_k \gamma/(|H_k|^2 + \gamma) = 1 - J/E_s$. The rest, $v_n = \sum_{m \ne n} \mathbf{A}_{nm} x_m + (\mathbf{B} w)_n$, is uncorrelated with $x_n$ because the symbols are independent with zero mean and the noise is independent of them. Then $J = E|\hat x_n - x_n|^2 = (1 - g)^2 E_s + \mathrm{Var}(v_n)$, so $\mathrm{Var}(v_n) = J - J^2/E_s = gJ$, and the SINR of $\hat x_n/g$ is $g^2 E_s / (gJ) = gE_s/J = E_s/J - 1$. $\square$

**Theorem 4 (the cost).** With $N$ a power of 2, lines L2 and L6 cost $O(N \log N)$ each by the radix-2 FFT, and lines L4 and L5 cost $O(N)$. The DFT of $h$ (line L3) is needed once per channel. So a block of $N$ symbols costs $O(N \log N)$, or $O(\log N)$ per symbol.

*Proof.* The radix-2 FFT does $\log_2 N$ passes of $N/2$ butterflies. $\square$
