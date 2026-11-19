---
title: What each step of MFCC computes, and why the gain only moves c_0
proves: [correctness]
status: full
---

We work in the real RAM. The frames, the window and the FFT are those of the shared helper, and the FFT returns the DFT exactly. Lines L6 and L7 are the [mel filter bank](/mel-filter-bank/), whose weights are proved there to be triangles that sum to 1 between the first and last centers. What is left to prove is the part that is new on this page: the DCT of line L8, the effect of a gain, the meaning of the truncation, and the lifter. Let $M \ge 1$ and $1 \le K \le M$.

**Lemma 1 (a cosine sum).** For every integer $d$ with $0 < |d| < 2M$, $\sum_{m=1}^{M} \cos\bigl(\pi d (m - \frac{1}{2}) / M\bigr) = 0$.

*Proof.* Let $\theta = \pi d / (2M)$, so $0 < |\theta| < \pi$ and $\sin \theta \ne 0$. The sum is the real part of $S = \sum_{m=1}^{M} e^{i (2m - 1) \theta} = e^{i\theta} (1 - e^{2iM\theta}) / (1 - e^{2i\theta})$, a geometric sum with ratio $e^{2i\theta} \ne 1$. Here $e^{2iM\theta} = e^{i \pi d} = (-1)^d$. If $d$ is even, $S = 0$. If $d$ is odd, $S = 2 e^{i\theta} / (1 - e^{2i\theta}) = 2 / (e^{-i\theta} - e^{i\theta}) = i / \sin\theta$, which is purely imaginary. In both cases the real part is 0. $\square$

**Lemma 2 (the DCT is orthogonal).** Let $C$ be the $M \times M$ matrix with entries $C_{n,m} = s_n \cos(\pi n (m - \frac{1}{2}) / M)$ for $0 \le n \le M - 1$ and $1 \le m \le M$, where $s_0 = \sqrt{1/M}$ and $s_n = \sqrt{2/M}$ for $n \ge 1$. Then $C C^{\mathsf T} = I$.

*Proof.* Write $a = \pi n (m - \frac{1}{2})/M$ and $b = \pi n' (m - \frac{1}{2})/M$, and use $\cos a \cos b = \frac{1}{2}(\cos(a - b) + \cos(a + b))$. Summed over $m$, the two terms are the sums of Lemma 1 with $d = n - n'$ and $d = n + n'$, or the constant $M$ when $d = 0$. If $n \ne n'$, both $d$ are nonzero and $|d| \le 2M - 3 < 2M$, so the sum is 0. If $n = n' = 0$, the sum of $\cos^2$ is $M$, and $s_0^2 M = 1$. If $n = n' \ge 1$, then $d = 0$ gives $M$ and $d = 2n$, with $0 < 2n < 2M$, gives 0, so the sum is $M/2$ and $s_n^2 M / 2 = 1$. $\square$

So line L8 computes $c = C_K \ell$, where $C_K$ is the first $K$ rows of $C$. With $K = M$ and no lifter, $\sum_n c_n^2 = \ell^{\mathsf T} C^{\mathsf T} C \ell = \sum_m \ell_m^2$, because a square matrix with $C C^{\mathsf T} = I$ also has $C^{\mathsf T} C = I$.

**Lemma 3 (constant vectors).** If $\ell_m = a$ for every $m$, then $c_0 = \sqrt{M}\, a$ and $c_n = 0$ for $n \ge 1$.

*Proof.* $c_0 = \sqrt{1/M} \cdot M a = \sqrt{M}\, a$. For $1 \le n \le M - 1$, $c_n = s_n a \sum_m \cos(\pi n (m - \frac{1}{2})/M) = 0$ by Lemma 1 with $d = n$. $\square$

**Lemma 4 (a gain moves only $c_0$).** Let the frame $v$ give the log energies $\ell$, and let the frame $g v$ with $g \ne 0$ give $\tilde\ell$. If all energies of both frames are at least $10^{-10}$, then $\tilde c_0 = c_0 + 2 \sqrt{M} \ln |g|$ and $\tilde c_n = c_n$ for $1 \le n \le K - 1$, before and after the lifter.

*Proof.* Line L1 is linear, and lines L4 and L5 give a power spectrum that scales by $g^2$. Line L6 is linear, so $\tilde E[m] = g^2 E[m]$, and line L7 gives $\tilde\ell_m = \ell_m + 2 \ln |g|$ by the condition. Line L8 is linear, so $\tilde c = c + C_K (2 \ln |g|, \ldots, 2 \ln|g|)^{\mathsf T}$, and Lemma 3 gives the claim. The lifter of line L9 multiplies $c_n$ by a factor that depends only on $n$, and its factor at $n = 0$ is $1 + \frac{Q}{2} \sin 0 = 1$, so the claim holds after it too. $\square$

**Lemma 5 (truncation is a least squares fit).** For $K \le M$, the vector $\hat\ell = C_K^{\mathsf T} c$, built from the $K$ kept coefficients, is the vector closest to $\ell$ in the Euclidean norm among all combinations of the first $K$ rows of $C$.

*Proof.* The rows of $C$ are orthonormal by Lemma 2, so the first $K$ rows are an orthonormal basis of their span. The closest point of a subspace with an orthonormal basis $u_0, \ldots, u_{K-1}$ is $\sum_n \langle \ell, u_n \rangle u_n$, and $\langle \ell, u_n \rangle = c_n$. $\square$

**Theorem.** For every frame, MFCC returns $c'_n = (1 + \frac{Q}{2} \sin(\pi n / Q))\, c_n$ for $0 \le n \le K - 1$, where $c$ is the first $K$ coefficients of an orthogonal transform of the floored log mel energies of the pre-emphasized, Hamming-windowed frame. A gain on the signal changes only $c'_0$, by $2 \sqrt{M} \ln |g|$, as long as no energy is at the floor, and the kept coefficients give the best fit of the log energies by $K$ cosines.

*Proof.* Lines L1 to L7 compute the floored log energies by their definitions and by the [mel filter bank](/mel-filter-bank/) proof. Lemma 2 gives the orthogonality, Lemma 4 the gain, and Lemma 5 the fit. Line L9 is the definition of the lifter. $\square$

The tests check Lemma 2 on an $8 \times 8$ matrix, the Parseval identity with 26 coefficients, Lemma 3 on silence, Lemma 4 with $g = 3$, and the whole chain against a slow direct computation with explicit DFT sums, triangles and cosine sums.
