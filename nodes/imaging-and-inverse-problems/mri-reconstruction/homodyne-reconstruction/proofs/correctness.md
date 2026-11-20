---
title: Homodyne reconstruction is exact for a real image with a constant phase
proves: [correctness]
status: full
---

The setting is that of the algorithm. The line has even length $n$, and $F_u$ is the unitary DFT, $(F_u v)(f) = n^{-1/2} \sum_{j=0}^{n-1} v_j e^{-2\pi i j f / n}$. Frequencies $f$ are taken modulo $n$ and written in $-n/2, \ldots, n/2 - 1$. The scan acquires the set $S = \{-n/2, \ldots, k_0\}$ with $0 \le k_0 < n/2 - 1$. The filter $H$ of line L1 is real, is $0$ for $f > k_0$, and satisfies

$$H(f) + H(-f) = 2 \quad \text{for every } f. \tag{1}$$

The step filter and the ramp filter both satisfy (1): for $|f| \le k_0$ the step filter gives $1 + 1$ and the ramp gives $(1 - f/(k_0+1)) + (1 + f/(k_0+1))$; for $k_0 < f < n/2$ the pair is $0 + 2$; and $f = -n/2$ is its own negative modulo $n$, with $H(-n/2) = 1$. The window $T$ of line L2 is $T(f) = 1 - |f|/(k_0+1)$ for $|f| \le k_0$ and $0$ otherwise.

**Theorem.** Let $x_j = e^{i\varphi_0} \rho_j$ with a constant $\varphi_0$ and a real vector $\rho$, and let $y_f = (F_u x)(f)$ for $f \in S$. Let $r = F_u^H (T \cdot F_u \rho)$. Then $r$ is real, and the output of HOMODYNE is $\hat\rho_j = \operatorname{sign}(r_j)\, \rho_j$ where $r_j \ne 0$ and $\hat\rho_j = 0$ where $r_j = 0$. If $\rho \ge 0$, then $\hat\rho = \rho$.

**Lemma 1.** Let $G$ be a sequence on the frequencies with $G(-f) = \overline{G(f)}$ for all $f$. Then $F_u^H G$ is real. If instead $G(-f) = -\overline{G(f)}$ for all $f$, then $F_u^H G$ is purely imaginary.

*Proof.* Write $g = F_u^H G$, so $g_j = n^{-1/2} \sum_f G(f) e^{2\pi i j f/n}$. Then

$$\overline{g_j} = n^{-1/2} \sum_f \overline{G(f)}\, e^{-2\pi i j f/n} = n^{-1/2} \sum_f \overline{G(-f)}\, e^{2\pi i j f/n},$$

after the change of index $f \to -f$, which is a bijection modulo $n$. In the first case $\overline{G(-f)} = G(f)$, so $\overline{g_j} = g_j$. In the second case $\overline{G(-f)} = -G(f)$, so $\overline{g_j} = -g_j$. $\square$

**Lemma 2.** For $\rho \ge 0$ and $\rho_j > 0$, the value $r_j$ is positive.

*Proof.* The product $T \cdot F_u \rho$ is a pointwise product in frequency, so $r$ is the periodic convolution $r_j = \sum_i \kappa_{j-i}\, \rho_i$ with the kernel $\kappa_m = n^{-1} \sum_{|f| \le k_0} T(f) e^{2\pi i m f/n}$. For $|f| \le k_0$, the number of pairs $(a, b)$ with $0 \le a, b \le k_0$ and $a - b = f$ is $k_0 + 1 - |f|$, so $T(f) = (k_0+1)^{-1} \#\{(a,b) : a - b = f\}$. The frequencies $-k_0, \ldots, k_0$ are distinct modulo $n$ because $2k_0 + 1 < n$. Hence

$$\kappa_m = \frac{1}{n (k_0+1)} \sum_{a=0}^{k_0} \sum_{b=0}^{k_0} e^{2\pi i m (a - b)/n} = \frac{1}{n (k_0+1)} \Bigl|\sum_{a=0}^{k_0} e^{2\pi i m a/n}\Bigr|^2 \ge 0,$$

the discrete Fejér kernel, with $\kappa_0 = (k_0+1)/n > 0$. All terms of $r_j$ are then nonnegative, and $r_j \ge \kappa_0 \rho_j > 0$. $\square$

*Proof of the theorem.* Put $R = F_u \rho$. Because $\rho$ is real, $R(-f) = \overline{R(f)}$. By linearity $y_f = e^{i\varphi_0} R(f)$ for $f \in S$.

First, lines L3 and L4 read $y$ only on $S$: $H(f) = 0$ for $f > k_0$, and $T(f) = 0$ for $|f| > k_0$. So $H \cdot y = e^{i\varphi_0} H \cdot R$ and $T \cdot y = e^{i\varphi_0} T \cdot R$ as full sequences.

The window. $T$ is real and even, so $G = T \cdot R$ satisfies $G(-f) = T(f) \overline{R(f)} = \overline{G(f)}$. By Lemma 1, $r = F_u^H G$ is real, and line L4 gives $l = e^{i\varphi_0} r$.

The filter. Write $H = 1 + A$ with $A(f) = H(f) - 1$. By (1), $A(-f) = 1 - H(f) = -A(f)$, so $A$ is real and odd. The sequence $G' = A \cdot R$ satisfies $G'(-f) = -A(f)\, \overline{R(f)} = -\overline{G'(f)}$. By Lemma 1, $q' = F_u^H G'$ is purely imaginary; write $q' = i q$ with $q$ real. Since $F_u^H R = \rho$, line L3 gives

$$z = e^{i\varphi_0} \bigl(F_u^H R + F_u^H (A \cdot R)\bigr) = e^{i\varphi_0} (\rho + i q).$$

Lines L5 to L7. If $l_j = 0$, then $r_j = 0$ and line L6 returns $0$. Otherwise $|l_j| = |r_j|$ and

$$\frac{\overline{l_j}\, z_j}{|l_j|} = \frac{r_j\, e^{-i\varphi_0}\, e^{i\varphi_0} (\rho_j + i q_j)}{|r_j|} = \operatorname{sign}(r_j)\,(\rho_j + i q_j),$$

whose real part, kept by line L7, is $\operatorname{sign}(r_j)\, \rho_j$. This is the first claim.

If $\rho \ge 0$: where $\rho_j > 0$, Lemma 2 gives $r_j > 0$ and the output is $\rho_j$. Where $\rho_j = 0$, the output is $\operatorname{sign}(r_j) \cdot 0 = 0$ or, if $r_j = 0$, the value $0$ of line L6. In both cases the output is $\rho_j$. $\blacksquare$

**Remarks.**

- The two-dimensional method of the page applies an inverse DFT along the fully sampled readout axis first. That step is exact and acts on each column separately, so the theorem holds column by column when the phase is constant over the image.
- The imaginary part $q$ is the error that a filter with (1) puts into the image. Taking the real part after the phase removal discards it. A filter without (1) leaves a real error term that the real part cannot remove.
- For a phase that is not constant, the phase of $l$ is only an estimate of the phase of $x$, and the output is an approximation. The theorem gives no error bound in that case.
