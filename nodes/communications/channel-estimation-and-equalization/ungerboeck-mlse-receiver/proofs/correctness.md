---
title: The Ungerboeck metric differs from the Euclidean metric by a constant, so the Viterbi search on it returns the maximum likelihood sequence
proves: [correctness]
status: full
---

The channel taps are $h_0, \ldots, h_{L-1}$, the block holds $N$ symbols $x_0, \ldots, x_{N-1}$ with $x_k = 0$ outside the block, and the received samples are $y_k = \sum_l h_l x_{k-l} + w_k$ for $k = 0, \ldots, N + L - 2$, with $w$ white $\mathcal{CN}(0, N_0)$. Write $\mathbf{H}$ for the $(N + L - 1) \times N$ full convolution matrix, $\mathbf{H}_{kj} = h_{k-j}$, so $y = \mathbf{H} x + w$. Define
$$z_k = \sum_{l=0}^{L-1} \bar h_l\, y_{k+l}, \qquad R_m = \sum_i h_{i+m} \bar h_i, \quad R_{-m} = \bar R_m,$$
and the increment $\lambda_k(x) = 2\,\mathrm{Re}(\bar x_k z_k) - R_0 |x_k|^2 - 2\,\mathrm{Re}\big(\bar x_k \sum_{m=1}^{L-1} R_m x_{k-m}\big)$.

**Lemma 1 (the matched filter).** $z = \mathbf{H}^H y$, and $\mathbf{H}^H \mathbf{H}$ is the $N \times N$ Toeplitz matrix with entry $(i, j)$ equal to $R_{i-j}$.

*Proof.* $(\mathbf{H}^H y)_i = \sum_k \bar h_{k-i} y_k = \sum_l \bar h_l y_{i+l} = z_i$, and the index $i + l \le N - 1 + L - 1$ stays inside the block, so no sample is lost (line L1). The entry $(i, j)$ of $\mathbf{H}^H \mathbf{H}$ is $\sum_k \bar h_{k-i} h_{k-j}$. With $l = k - i$ this is $\sum_l \bar h_l h_{l + i - j} = R_{i-j}$, and the sum runs over all $l$ because $\mathbf{H}$ keeps every output of the convolution (line L2). $\square$

**Theorem 1 (the metric identity).** For every $y$ and every $x \in \mathbb{C}^N$,
$$\sum_{k=0}^{N-1} \lambda_k(x) = \|y\|^2 - \|y - \mathbf{H} x\|^2 .$$

*Proof.* Expand $\|y - \mathbf{H} x\|^2 = \|y\|^2 - 2\,\mathrm{Re}(x^H \mathbf{H}^H y) + x^H \mathbf{H}^H \mathbf{H} x$. By Lemma 1, the middle term is $2\,\mathrm{Re}\sum_k \bar x_k z_k$. The last term is $\sum_{i,j} \bar x_i R_{i-j} x_j$. Split it into the diagonal $i = j$, which gives $R_0 \sum_k |x_k|^2$ (and $R_0$ is real), and the pairs with $i \ne j$. The term for $(j, i)$ with $j < i$ is $\bar x_j R_{j-i} x_i = \overline{\bar x_i R_{i-j} x_j}$, so the two terms of each pair add up to $2\,\mathrm{Re}(\bar x_i R_{i-j} x_j)$. Group the pairs by the larger index $k = i$ and $m = i - j \ge 1$. Since $R_m = 0$ for $m \ge L$, this gives $\sum_k 2\,\mathrm{Re}(\bar x_k \sum_{m=1}^{L-1} R_m x_{k-m})$. Collect the terms. $\square$

**Corollary 1 (maximum likelihood).** Over any set of candidate sequences, $x$ maximizes $\sum_k \lambda_k(x)$ if and only if it minimizes $\|y - \mathbf{H} x\|^2$, which is the maximum likelihood rule for white Gaussian noise.

*Proof.* $\|y\|^2$ does not depend on $x$. The likelihood is $(\pi N_0)^{-(N+L-1)} \exp(-\|y - \mathbf{H}x\|^2/N_0)$. $\square$

**Theorem 2 (the trellis search).** `ungerboeck_mlse` returns a sequence that maximizes $\sum_k \lambda_k$ over $\mathcal{A}^n$ followed by the known tail.

*Proof.* The increment $\lambda_k$ depends only on $x_k$ and the state $s_k = (x_{k-1}, \ldots, x_{k-L+1})$, where the entries with negative index are 0 (in the code, only the entries with $k - l \ge 0$ enter the ISI term). So the sum is a sum of branch metrics along a path in the trellis with $M^{L-1}$ states, and two paths into the same state have the same future increments. The same induction as for the Viterbi equalizer shows that after step $k$, `metric[s]` is the largest partial sum over the allowed paths into $s$, and the pointers give such a path (lines L4 to L7). At times $k \ge n$, only the tail symbol is allowed. Line L8 takes the best final state and traces back. Corollary 1 ends the proof. $\square$

**Remark (the noise).** The noise in $z$ is $\mathbf{H}^H w$, with covariance $N_0 \mathbf{H}^H \mathbf{H}$, which is colored. Theorem 1 does not need white noise in $z$: it rewrites the exact likelihood of $y$. This is why no whitening filter is needed. The increments are not distances and can be negative, so the search maximizes and starts from 0.
