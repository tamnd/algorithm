---
title: When conjugate phase reconstruction is exact
proves: [correctness]
status: full
---

The setting is that of the algorithm. The image has $N$ pixels at positions $r_1, \ldots, r_N$, with the values $x_i$ and the off-resonance frequencies $\omega_i$ (rad/s). The scan has $m$ samples at the k-space positions $k_j$ and the times $t_j$, with the density weights $w_j > 0$. The signal model is $s = A x$ with

$$A_{ji} = e^{-i \omega_i t_j}\, e^{-2\pi i\, k_j \cdot r_i}.$$

Write $W = \operatorname{diag}(w_1, \ldots, w_m)$.

**Lemma 1 (the algorithm computes the adjoint).** The output of CONJUGATE-PHASE is $\hat x = A^H W s$.

*Proof.* Line L4 adds $w_j s_j e^{+2\pi i\, k_j \cdot r_i} e^{+i \omega_i t_j} = \overline{A_{ji}}\, w_j s_j$ for each sample $j$, and lines L1 to L5 do this for each pixel $i$. So $\hat x_i = \sum_j \overline{A_{ji}}\, w_j s_j = (A^H W s)_i$. $\square$

**Theorem 1 (exactness).** Let $P = A^H W A$. For data $s = A x$ without noise, $\hat x = P x$. Hence the method returns $x$ for every image $x$ if and only if $P = I$. The entries of $P$ are

$$P_{i i'} = \sum_{j=1}^{m} w_j\, e^{2\pi i\, k_j \cdot (r_i - r_{i'})}\, e^{i (\omega_i - \omega_{i'}) t_j}. \tag{1}$$

*Proof.* By Lemma 1, $\hat x = A^H W A x = P x$. If $P = I$, then $\hat x = x$. If $\hat x = x$ for every $x$, take $x$ to be each unit vector in turn; the columns of $P$ are then the columns of $I$. Equation (1) is the product $\sum_j \overline{A_{ji}}\, w_j A_{j i'}$ written out. $\square$

Column $i'$ of $P$ is the point spread function: the image that the method returns for a single point at $r_{i'}$.

**Theorem 2 (full Cartesian grid, no field).** Let the image be an $n \times n$ grid with $r_i \in \{-n/2, \ldots, n/2 - 1\}^2$ in pixel units, let the samples be the $n^2$ points $k_j = (u, v)/n$ with $u, v \in \{-n/2, \ldots, n/2 - 1\}$, each once, in any order and at any times, let $w_j = 1/n^2$ and let $\omega_i = 0$. Then $P = I$.

*Proof.* With $\omega = 0$, equation (1) gives $P_{i i'} = n^{-2} \sum_{u} \sum_{v} e^{2\pi i (u a + v b)/n}$, where $(a, b) = r_i - r_{i'}$ has integer entries with $|a|, |b| < n$. The double sum is the product of $\sum_u e^{2\pi i u a/n}$ and $\sum_v e^{2\pi i v b/n}$. Each factor is a sum of $n$ consecutive powers of the root of unity $e^{2\pi i a/n}$. It equals $n$ if $a = 0$, and otherwise $e^{2\pi i a/n} \ne 1$ because $0 < |a| < n$, so the geometric sum is $e^{-\pi i a}\,(e^{2\pi i a} - 1)/(e^{2\pi i a/n} - 1) = 0$. So $P_{i i'} = 1$ if $r_i = r_{i'}$ and $0$ otherwise. $\square$

**Theorem 3 (a constant field).** If $\omega_i = \omega_0$ for all $i$, then $P$ does not depend on $\omega_0$ or on the times $t_j$. In particular, under the sampling of Theorem 2 with any constant field and any sample times, $P = I$.

*Proof.* In equation (1), $\omega_i - \omega_{i'} = 0$, so the last factor is 1 for every $j$, and (1) reduces to the case $\omega = 0$. Theorem 2 then gives $P = I$. $\blacksquare$

**Remarks.**

- Equation (1) shows that the field enters $P$ only through the differences $\omega_i - \omega_{i'}$. When the field is nearly constant over the region where the point spread function without field is large, the entries of $P$ near the diagonal are close to those without field. This is why the method works well for smooth fields. It is a heuristic argument, not a bound; the page gives measured errors.
- For a field that varies, $P \ne I$ in general, and the exact answer is the solution of $A x = s$ in the least squares sense, for example by the conjugate gradient method. The tests compare both.
- A constant field still matters for the uncorrected image: with the weights of Theorem 2 but the correction left out, the output is $A_0^H W A x$ with $A_0$ the matrix for $\omega = 0$. Each sample then carries the extra phase $e^{-i \omega_0 t_j}$, which shifts and blurs the image along the direction in which $t_j$ grows.
