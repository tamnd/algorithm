---
title: VLAD is an order-invariant feature map of the same-cell residual match kernel and a scaled hard-assignment Fisher vector
proves: [correctness]
status: full
---

We use the notation of the page. The codebook is $c_1, \ldots, c_K \in \mathbb{R}^D$. For a descriptor $x$, $\mathrm{NN}(x)$ is the smallest index $k$ that minimizes $\lVert x - c_k \rVert_2$. For a finite multiset $X$ of descriptors, $X_k = \{x \in X : \mathrm{NN}(x) = k\}$, $n_k = |X_k|$, and $v_k(X)$ is block $k$ after lines L1 to L4 of VLAD. We write $v(X)$ for the concatenation of the blocks, before lines L5 to L8.

**Lemma 1 (what the loop computes).** After lines L1 to L4, $v_k(X) = \sum_{x \in X_k} (x - c_k)$ for every $k$.

*Proof.* Line L1 sets every block to 0. Each pass of the loop of line L2 handles one descriptor $x$. Line L3 computes $k = \mathrm{NN}(x)$, and line L4 adds $x - c_k$ to block $k$ and to no other block. By induction on the number of passes, after the descriptors $x_1, \ldots, x_j$ have been handled, block $k$ is the sum of $x_i - c_k$ over the $i \le j$ with $\mathrm{NN}(x_i) = k$. With $j = n$ this is the claim. $\square$

**Corollary 1 (order invariance and the mean form).** The output does not depend on the order in which line L2 visits $X$. If $n_k > 0$ and $\bar x_k$ is the mean of $X_k$, then $v_k(X) = n_k (\bar x_k - c_k)$; if $n_k = 0$, then $v_k(X) = 0$.

*Proof.* The right side of Lemma 1 is a sum over a set that is defined without an order, and addition in $\mathbb{R}^D$ is commutative and associative. Lines L5 to L8 are functions of the blocks only. For the mean form, $\sum_{x \in X_k} (x - c_k) = \sum_{x \in X_k} x - n_k c_k = n_k \bar x_k - n_k c_k$. $\square$

In floating point the sum can differ in the last bits for another order. The claim is about the exact values.

**Lemma 2 (additivity).** If $X$ and $Y$ are multisets and $X \uplus Y$ is their union with multiplicities, then $v(X \uplus Y) = v(X) + v(Y)$.

*Proof.* $\mathrm{NN}$ depends only on the descriptor, so $(X \uplus Y)_k = X_k \uplus Y_k$, and the sum of Lemma 1 splits. $\square$

**Theorem 1 (match kernel).** For two multisets $X$ and $Y$,
$$\langle v(X), v(Y) \rangle = \sum_{k=1}^{K} \sum_{x \in X_k} \sum_{y \in Y_k} \langle x - c_k, y - c_k \rangle.$$
Hence the function $k_{\mathrm{VLAD}}(X, Y) = \langle v(X), v(Y) \rangle$ on finite multisets is a positive semidefinite kernel.

*Proof.* The inner product of two concatenations is the sum of the inner products of the blocks: $\langle v(X), v(Y) \rangle = \sum_k \langle v_k(X), v_k(Y) \rangle$. By Lemma 1 and the bilinearity of the inner product,
$$\langle v_k(X), v_k(Y) \rangle = \Big\langle \sum_{x \in X_k} (x - c_k), \sum_{y \in Y_k} (y - c_k) \Big\rangle = \sum_{x \in X_k} \sum_{y \in Y_k} \langle x - c_k, y - c_k \rangle.$$
Summing over $k$ gives the identity. For the second claim, take multisets $X^{(1)}, \ldots, X^{(m)}$ and reals $a_1, \ldots, a_m$. Then $\sum_{i,j} a_i a_j k_{\mathrm{VLAD}}(X^{(i)}, X^{(j)}) = \lVert \sum_i a_i v(X^{(i)}) \rVert^2 \ge 0$. $\square$

The normalized versions are also positive semidefinite: if $z(X) = f(v(X))$ for any map $f$ into $\mathbb{R}^{KD}$, then $\langle z(X), z(Y) \rangle$ is again an inner product of feature vectors, and the same argument applies. This covers lines L5, L7 and L8.

**Lemma 3 (normalization).** If the output $z$ of line L9 is not zero, then $\lVert z \rVert_2 = 1$. If line L5 runs, every block of the vector before line L7 has norm 1 or is zero. Line L7 keeps the sign of each entry and keeps zero entries at zero, so it does not change which entries are zero.

*Proof.* Line L8 divides a nonzero vector by its norm. Line L5 divides each nonzero block by its norm and leaves zero blocks. For line L7, $\mathrm{sign}(t)|t|^\alpha$ is zero exactly when $t = 0$ and has the sign of $t$ otherwise, since $|t|^\alpha > 0$ for $t \ne 0$. So if $z \ne 0$ before line L7, it is still nonzero after it, and line L8 applies. $\square$

**Theorem 2 (VLAD as a Fisher vector).** Take a Gaussian mixture with $K$ components, weights $w_k = 1/K$, means $\mu_k = c_k$ and identity covariances, and replace its posteriors by the hard assignment $\gamma_x(k) = 1$ if $\mathrm{NN}(x) = k$ and 0 otherwise. The normalized gradient with respect to the means of the [Fisher vector](/fisher-vector/) of a set $X$ of $n \ge 1$ descriptors, $\mathcal{G}_{\mu_k} = \frac{1}{n\sqrt{w_k}} \sum_{x \in X} \gamma_x(k) \frac{x - \mu_k}{\sigma_k}$ (Sanchez et al. 2013, Eq. 17, divided by the number of descriptors), satisfies $\mathcal{G}_\mu = \frac{\sqrt{K}}{n} v(X)$. So, when $v(X) \ne 0$, the L2-normalized Fisher mean gradient equals the VLAD vector of lines L1 to L4 and L8.

*Proof.* With $\sigma_k = 1$ and $w_k = 1/K$, $\frac{1}{n \sqrt{w_k}} = \frac{\sqrt{K}}{n}$, and the sum over $x$ with the hard $\gamma_x(k)$ is the sum over $X_k$ of $x - c_k$, which is $v_k(X)$ by Lemma 1. The factor $\sqrt K / n$ is positive and the same for all blocks, so L2 normalization removes it. $\square$

With the true soft posteriors the two vectors differ. The difference goes to zero as the components move apart, because then each posterior goes to 0 or 1 for almost every descriptor.

**What is not claimed.** None of these facts says that VLAD ranks images well. The retrieval quality of VLAD, and the gain of power and intra-normalization, are benchmark results.
