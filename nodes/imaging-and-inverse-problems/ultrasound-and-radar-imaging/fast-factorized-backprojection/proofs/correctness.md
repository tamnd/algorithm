---
title: Before interpolation, merging subaperture images is exact, so fast factorized backprojection differs from direct backprojection only by its interpolation error
proves: [correctness]
status: full
---

We prove three facts about FFBP as written on the main page (lines L1 to L9). Theorems 1 and 2 are exact. Theorem 3 is exact under the far-field approximation that it states; how small the interpolation error is for a given oversampling is a measurement, given on the main page.

**Setting.** The pulses $d_p$ are range compressed and the antenna positions are $(x_p, 0)$. For a point $q$ and a pulse $p$ write $R_p(q) = |q - (x_p, 0)|$ and $T_p(q) = d_p(2R_p(q)/c)\, e^{+i 4\pi f_0 R_p(q)/c}$, so that direct backprojection is $I(q) = \sum_p T_p(q)$. A subaperture $s$ is a set of pulses with the center $(x_s, 0)$; write $r_s(q) = |q - (x_s, 0)|$ and $\beta_s(q) = (q_x - x_s)/r_s(q)$. The map $q \mapsto (r_s(q), \beta_s(q))$ is one-to-one on the half plane $q_y > 0$, with the inverse $(r, \beta) \mapsto (x_s + r\beta, r\sqrt{1 - \beta^2})$. Define the exact subimage by $J_s(r_s(q), \beta_s(q)) = e^{-i 4\pi f_0 r_s(q)/c} \sum_{p \in s} T_p(q)$.

**Theorem 1 (linearity).** The output of L1 to L9 is linear in the data.

*Proof.* L1 is a DFT, a zero padding and an inverse DFT; L2, L6 and L9 are weighted sums of stored values with weights fixed by the geometry; L7 is a sum with fixed phase factors. A composition of linear maps is linear. $\square$

**Theorem 2 (exact factorization).** Let $s$ be the union of the disjoint subapertures $a$ and $b$. For every point $q$ with $q_y > 0$,
$$J_s(r_s(q), \beta_s(q)) = \sum_{h \in \{a, b\}} J_h(r_h(q), \beta_h(q))\, e^{+i 4\pi f_0 (r_h(q) - r_s(q))/c}.$$
For a single pulse $p$ as its own subaperture, with the center $x_p$, $J_p(r, \beta) = d_p(2r/c)$ for every $\beta$. For the final set $S$ of subapertures, which is a partition of all pulses, $I(q) = \sum_{s \in S} J_s(r_s(q), \beta_s(q))\, e^{+i 4\pi f_0 r_s(q)/c}$.

*Proof.* By the definition, $J_h(r_h(q), \beta_h(q))\, e^{+i 4\pi f_0 r_h(q)/c} = \sum_{p \in h} T_p(q)$. Summing over $h \in \{a, b\}$ gives $\sum_{p \in s} T_p(q)$ because $a$ and $b$ are disjoint with the union $s$, and multiplying by $e^{-i 4\pi f_0 r_s(q)/c}$ gives $J_s$. For one pulse the center is $x_p$, so $r_p(q) = R_p(q)$ and $J_p = d_p(2R_p/c)$, which depends on $r$ only. For the last statement, sum $\sum_{p \in s} T_p(q)$ over the partition $S$. $\square$

So if L2, L6 and L9 read the subimages exactly, by induction over the stages every stored value equals the exact subimage at its grid point, and L9 returns $I(q)$. The output differs from direct backprojection only through the interpolation of the stored grids.

**Theorem 3 (the angle bandwidth).** Let $s$ have the length $l_s$, so $|x_p - x_s| \le l_s/2$ for $p \in s$. Under the far-field approximation $R_p(q) = r_s(q) - (x_p - x_s)\beta_s(q)$, and for a fixed $r$, the term of pulse $p$ in $J_s(r, \beta)$ is $d_p(2R_p/c)\, e^{-i 2\pi \nu_p \beta}$ with the frequency $\nu_p = 2(x_p - x_s)/\lambda$, and $|\nu_p| \le l_s/\lambda$. So if the envelopes $d_p(2R_p/c)$ vary slowly in $\beta$, the spectrum of $J_s(r, \cdot)$ lies in $[-l_s/\lambda, l_s/\lambda]$ and the sampling theorem allows the step $\lambda/(2 l_s)$.

*Proof.* For the point $(x_s + r\beta, r\sqrt{1 - \beta^2})$, $R_p^2 = r^2 - 2r\beta(x_p - x_s) + (x_p - x_s)^2$, and to first order in $(x_p - x_s)/r$, $R_p = r - (x_p - x_s)\beta$. The phase of the term is then $4\pi f_0 (R_p - r)/c = -4\pi (x_p - x_s)\beta/\lambda = -2\pi \nu_p \beta$. With $|x_p - x_s| \le l_s/2$, $|\nu_p| \le l_s/\lambda$, and a signal with this two-sided band is fixed by samples at a step of at most $1/(2 l_s/\lambda)$. $\square$

When two subapertures merge, $l_s$ doubles, so the step in $\beta$ halves: this is why L4 doubles the number of angle samples at each stage while the number of subimages halves, which keeps the work of a stage about constant. The implementation uses $\lambda/(O\, l_s)$ with $O = 16$, much finer than the Nyquist step, because it interpolates linearly.

**Cost.** For $P = \Theta(N)$ pulses and an $N \times N$ scene, the subimages of one stage hold $O(N^2)$ samples together, by Theorem 3 and the fixed range step, and each costs $O(1)$ with two bilinear interpolations. There are $O(\log N)$ stages, so L3 to L8 cost $O(N^2 \log N)$. L1 and L2 cost $O(N \cdot F N \log(F N))$ and L9 costs $O(N^2)$ for a fixed number of final subimages. The total is $O(N^2 \log N)$ in the real-RAM model for fixed $F$ and $O$, with $O(N^2)$ extra space.
