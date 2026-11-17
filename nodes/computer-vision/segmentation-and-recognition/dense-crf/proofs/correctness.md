---
title: Correctness of mean field inference in the fully connected CRF
proves: [correctness]
status: full
---

This proof covers lines L1 to L7 of the main page, with exact messages. The model has $n = WH$ pixels and $L$ labels. The energy of a labeling $x$ is
$$E(x) = \sum_i U_i(x_i) + \sum_{i < j} [x_i \ne x_j]\, k(i, j), \qquad k(i, j) = \sum_m w^{(m)} k^{(m)}(f_i, f_j),$$
with weights $w^{(m)} \ge 0$ and Gaussian kernels $k^{(m)}$, so $k(i, j) = k(j, i) \ge 0$. The distribution is $P(x) = e^{-E(x)} / Z$. A mean field distribution is $Q(x) = \prod_i Q_i(x_i)$, and its free energy is
$$F(Q) = \mathbb{E}_Q[E] - H(Q) = \sum_i \sum_l Q_i(l) \bigl(U_i(l) + \log Q_i(l)\bigr) + \sum_{i < j} k(i, j) \Bigl(1 - \sum_l Q_i(l) Q_j(l)\Bigr).$$
The pair term is the probability under $Q$ that $x_i \ne x_j$, times $k(i, j)$. Nothing here says that the model labels images well. That is a benchmark question.

**Lemma 1 (the lines compute the mean field equation).** Given $Q$, lines L3 to L6 compute, for each pixel $i$,
$$Q_i^{\mathrm{new}}(l) = \frac{1}{Z_i} \exp\Bigl(-U_i(l) - \sum_{j \ne i} k(i, j) \sum_{l' \ne l} Q_j(l')\Bigr),$$
which is equation (4) of Krähenbühl and Koltun (2011) for the Potts compatibility $\mu(l, l') = [l \ne l']$.

*Proof.* Line L3 sets $M_i(l) = \sum_{j \ne i} k(i, j) Q_j(l)$. Line L4 sets $B_i(l) = \sum_{l'} M_i(l') - M_i(l) = \sum_{l' \ne l} M_i(l') = \sum_{j \ne i} k(i, j) \sum_{l' \ne l} Q_j(l')$. Lines L5 and L6 exponentiate $-U_i(l) - B_i(l)$ and divide by the sum over $l$. $\square$

**Lemma 2 (free energy and the partition function).** For every product distribution $Q$,
$$F(Q) = \mathrm{KL}(Q \,\|\, P) - \log Z \ge -\log Z,$$
with equality if and only if $Q = P$.

*Proof.* $\mathrm{KL}(Q \| P) = \sum_x Q(x) \log Q(x) - \sum_x Q(x) \log P(x) = -H(Q) + \mathbb{E}_Q[E] + \log Z$. The expectation of $U_i(x_i)$ under $Q$ is $\sum_l Q_i(l) U_i(l)$. For $i \ne j$ the labels are independent under $Q$, so $\Pr_Q(x_i \ne x_j) = 1 - \sum_l Q_i(l) Q_j(l)$. The entropy of a product is the sum of the entropies. This gives the formula for $F$. The KL divergence is nonnegative, and zero only for $Q = P$ (Gibbs inequality). $\square$

**Lemma 3 (one pixel update is an exact minimization).** Fix $Q_j$ for all $j \ne i$. Over all distributions $Q_i$ on the labels, $F$ has the unique minimizer $Q_i^{\mathrm{new}}$ of Lemma 1.

*Proof.* Collect the terms of $F$ that contain $Q_i$:
$$\sum_l Q_i(l) \bigl(U_i(l) + \log Q_i(l)\bigr) + \sum_{j \ne i} k(i, j) \Bigl(1 - \sum_l Q_i(l) Q_j(l)\Bigr).$$
Since $\sum_l Q_i(l) = 1$, the term $k(i, j)(1 - \sum_l Q_i(l) Q_j(l))$ equals $\sum_l Q_i(l)\, k(i, j) \sum_{l' \ne l} Q_j(l')$. So the part of $F$ that depends on $Q_i$ is $\sum_l Q_i(l) (U_i(l) + B_i(l) + \log Q_i(l))$, with $B_i$ as in Lemma 1. With $R(l) = e^{-U_i(l) - B_i(l)} / Z_i$ this is $\mathrm{KL}(Q_i \| R) - \log Z_i$, which is smallest, and only then, at $Q_i = R = Q_i^{\mathrm{new}}$. $\square$

**Theorem 1 (sequential updates).** If the pixels are updated one at a time with the rule of Lemma 1, each with the current values of the others, then $F$ never increases. $F$ is bounded below by $-\log Z$, so the sequence of values of $F$ converges.

*Proof.* Each step replaces $Q_i$ by the minimizer of $F$ over $Q_i$ with the rest fixed (Lemma 3), so $F$ does not increase. A non-increasing sequence that is bounded below (Lemma 2) converges. $\square$

This is the classical result for mean field (Wainwright and Jordan 2008, Section 5). It is a statement about the values of $F$, at a local minimum or a saddle in general, not about the global minimum of $F$ over all product distributions.

**Parallel updates.** Lines L3 to L6 update all pixels at once, from the old $Q$. Lemma 3 does not apply, because each pixel uses old values of its neighbors. Krähenbühl and Koltun (2013) point out that the parallel update loses the guarantee. A two-pixel example shows that it can fail to converge: $U_1 = (0, 1)$, $U_2 = (1, 0)$, and $k(1, 2) = 5 e^{-1/18} \approx 4.73$. At the start $Q_1(0) = Q_2(1) \approx 0.731$. In each parallel step each pixel adopts the label that the other pixel had, because the Potts penalty $4.73 \cdot 0.731$ outweighs the unary difference 1. The beliefs swap at each step: $Q_1(0) \approx 0.731, 0.234, 0.971, 0.031, 0.996, \ldots$ The sequential rule from the same start converges, with both pixels on label 1. The test file checks this example.

**Theorem 2 (a convergent parallel variant).** Krähenbühl and Koltun (2013, Section 3.2). Add the self term to the message: $M_i(l) = \sum_j k(i, j) Q_j(l)$ with $k(i, i) = \sum_m w^{(m)}$, the value of the kernels at zero distance. Then each parallel update does not increase
$$\tilde D(Q) = \sum_i \sum_l Q_i(l) \bigl(U_i(l) + \log Q_i(l)\bigr) - \frac{1}{2} \sum_{i, j} k(i, j) \sum_l Q_i(l) Q_j(l),$$
where the double sum includes $i = j$.

*Proof.* Write $\tilde D = f + g$ with $f(Q) = \sum_{i, l} Q_i(l) \log Q_i(l)$, which is convex, and $g(Q) = \sum_{i, l} Q_i(l) U_i(l) - \frac{1}{2} \sum_l q_l^{\top} K q_l$, where $q_l = (Q_1(l), \ldots, Q_n(l))$ and $K$ is the matrix of $k(i, j)$ with the diagonal included. Each Gaussian kernel is positive definite (its Fourier transform is positive, by Bochner's theorem), and the appearance kernel is a Gaussian in the joint feature of position and color. So $K$, a sum of Gram matrices with weights $w^{(m)} \ge 0$, is positive semidefinite, and $g$ is concave.

The concave-convex procedure takes $Q' = \arg\min_Q f(Q) + \nabla g(Q^{\mathrm{old}}) \cdot Q$ over products of distributions. The objective splits over the pixels, and $\nabla g$ at pixel $i$ and label $l$ is $U_i(l) - M_i(l)$. By the argument of Lemma 3, the minimizer is $Q'_i(l) \propto \exp(-U_i(l) + M_i(l))$. The line L4 penalty is $\sum_{l'} M_i(l') - M_i(l)$, which differs from $-M_i(l)$ by a constant in $l$, so lines L5 and L6 give the same $Q'_i$. Then
$$\tilde D(Q') = f(Q') + g(Q') \le f(Q') + g(Q^{\mathrm{old}}) + \nabla g(Q^{\mathrm{old}}) \cdot (Q' - Q^{\mathrm{old}}) \le f(Q^{\mathrm{old}}) + g(Q^{\mathrm{old}}).$$
The first inequality is concavity of $g$, and the second is the choice of $Q'$. $\square$

$\tilde D$ differs from $F + \log Z$ only by the self terms $-\frac{1}{2} k(i, i) \sum_l Q_i(l)^2$ and a constant. Krähenbühl and Koltun argue that for wide kernels this part is small. That is an approximation, not a bound proved here. On the two-pixel example the variant converges, but to a state where each pixel keeps its own label, which shows that the self term changes the fixed points.

**Lemma 4 (separable filtering of the spatial kernel).** For the spatial kernel $k(i, j) = \exp(-\lVert p_i - p_j \rVert^2 / (2 \theta^2))$ on the grid, a blur of each label plane along the rows with the 1D Gaussian $g(d) = e^{-d^2 / (2\theta^2)}$, then along the columns, gives $\sum_j k(i, j) Q_j(l)$ over all $j$, including $j = i$. Subtracting $Q_i(l)$ gives the message of line L3.

*Proof.* $k(i, j) = g(u_i - u_j)\, g(v_i - v_j)$. The row blur gives $R(u, v) = \sum_{x} g(u - x) Q_{(x, v)}(l)$, and the column blur gives $\sum_y g(v - y) R(u, y) = \sum_{x, y} g(u - x) g(v - y) Q_{(x, y)}(l)$. The self term has $k(i, i) = 1$. $\square$

The appearance kernel does not split in this way, because it depends on the colors. Krähenbühl and Koltun filter it with the permutohedral lattice of Adams, Baek and Davis (2010), which downsamples, blurs and upsamples. That step is an approximation of the sum, and the proofs above do not cover its error.

**Cost.** With exact messages, line L3 costs $O(n^2 L)$, line L4 costs $O(n L)$ for the Potts model ($O(n L^2)$ for a general compatibility matrix), and lines L5 and L6 cost $O(n L)$. So $N$ iterations cost $O(N n^2 L)$ time in the real-RAM model, with $n = WH$, plus $O(n^2)$ for the kernel matrix if it is stored. With a filter whose cost is linear in $n$, an iteration costs $O(n L)$ times the cost per sample of the filter.
