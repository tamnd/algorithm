---
title: Correctness of split-step Fourier migration
proves: [correctness, termination]
status: full
---

**Setting.** The model is the exploding reflector model with the slowness $s(x, z) = 2/v(x, z)$ of the half velocity. The velocity is constant in depth inside each layer $z_i \le z < z_{i+1}$, with the values $s_i[j]$ at $x_j = j\Delta x$, and $s_{0,i} = \frac{1}{n_x}\sum_j s_i[j]$ is the reference slowness of line L5. The time transform is $U(\omega) = \sum u(t)\, e^{-i\omega t}$, and $\omega_k = 2\pi k/(n_t\Delta t)$. For a frequency $\omega$ and a layer $i$, one step of the method is the linear map $A_{\omega, i}$ of lines L6 to L9:
$$A_{\omega, i}\, p = \Lambda_{\omega, i}\; \mathrm{IDFT}\big(\Phi_{\omega, i}\; \mathrm{DFT}(p)\big),$$
where $\Phi_{\omega, i}$ multiplies entry $j$ by $e^{i\sqrt{\omega^2 s_{0,i}^2 - k_{x,j}^2}\,\Delta z}$ if the root is real and by 0 otherwise, and $\Lambda_{\omega, i}$ multiplies entry $j$ by $e^{i\omega(s_i[j] - s_{0,i})\Delta z}$.

**Theorem 1 (what the code computes).** Let $p_k^{(i)} = A_{\omega_k, i-1}\cdots A_{\omega_k, 0}\, p_k^{(0)}$, where $p_k^{(0)}[j]$ is the DFT of trace $j$ at index $k$ (line L1). Then line L10 returns
$$m[i][j] = \frac{2}{n_t} \operatorname{Re} \sum_{0 < k < n_t/2} p_k^{(i)}[j].$$

*Proof.* Line L2 runs over $k = 1, \ldots, \lceil n_t/2\rceil - 1$, which is the set $0 < k < n_t/2$. Fix $k$. By induction on $i$, at the start of pass $i$ of line L3 the array $p$ is $p_k^{(i)}$: it is $p_k^{(0)}$ before pass 0, and lines L6 to L9 apply $A_{\omega_k, i}$ once (line L7 is $\Phi$, line L9 is $\Lambda$). Line L4 adds $\frac{2}{n_t}\operatorname{Re} p_k^{(i)}[j]$ to row $i$ before the step. The loops have a fixed number of passes, so the algorithm stops. $\blacksquare$

**Lemma 1 (the positive frequencies are enough).** Let $q_k$ be any family of continued fields with $q_{n_t - k} = \overline{q_k}$ (the symmetry of the DFT of real traces). Then the inverse DFT in time at $t = 0$ is
$$\frac{1}{n_t}\sum_{k=0}^{n_t - 1} q_k = \frac{1}{n_t}\Big(q_0 + [\,q_{n_t/2}\,] + 2\operatorname{Re}\sum_{0 < k < n_t/2} q_k\Big),$$
where the term in brackets is present only for even $n_t$.

*Proof.* Pair the index $k$ with $n_t - k$ for $0 < k < n_t/2$; each pair adds $q_k + \overline{q_k} = 2\operatorname{Re} q_k$. The indices $0$ and $n_t/2$ are their own partners. $\square$

The continuation keeps the symmetry: the step for $-\omega$ uses $k_z = -\sqrt{\omega^2 s_0^2 - k_x^2}$ and the factor $e^{-i\omega(s - s_0)\Delta z}$, and both factors depend on $k_x$ only through $k_x^2$, so $A_{-\omega, i}\,\bar{p} = \overline{A_{\omega, i}\, p}$. So by Lemma 1, Theorem 1 gives the field at $t = 0$ of the continued data after the frequency $\omega = 0$ and (for even $n_t$) the Nyquist frequency are removed. The image is real.

**Theorem 2 (exact when the velocity does not change along $x$).** If $s_i[j] = s_i$ for all $j$ in every layer, the output is the phase-shift image of the same data without the frequency 0 and the Nyquist frequency. In particular, for a velocity $v(z)$ the method is exact in the sense of the proof of phase-shift migration.

*Proof.* Then $s_{0,i} = s_i$, so $\Lambda_{\omega, i} = I$, and $A_{\omega, i}$ is the inverse DFT of the phase shift with $k_z = \sqrt{\omega^2 s_i^2 - k_x^2}$, the evanescent parts set to zero. For $\omega > 0$ and $s_i = 2/v_i$ this is $\operatorname{sgn}(\omega)\sqrt{\omega^2/v_i'^2 - k_x^2}$ with $v_i' = v_i/2$: the factor of the phase-shift loop invariant, applied in the $x$ domain. Apply Lemma 1 to both methods. $\square$

**Theorem 3 (the phase error for a plane wave).** Suppose a layer has the constant slowness $s$ but the step uses a reference $s_0$ (as happens locally where $s(x)$ differs from its mean). For a propagating plane wave $e^{i k_x x}$ with both roots real, the step gives the phase $\Delta z\big(\sqrt{\omega^2 s_0^2 - k_x^2} + \omega(s - s_0)\big)$, while the exact phase is $\Delta z\sqrt{\omega^2 s^2 - k_x^2}$. The error
$$E = \Delta z\Big(\sqrt{\omega^2 s_0^2 - k_x^2} + \omega(s - s_0) - \sqrt{\omega^2 s^2 - k_x^2}\Big)$$
is 0 when $k_x = 0$ or $s = s_0$, and
$$E = \Delta z\,\frac{k_x^2}{2\omega}\Big(\frac{1}{s} - \frac{1}{s_0}\Big) + O\Big(\Delta z\,\frac{k_x^4}{\omega^3}\Big)\Big(\frac{1}{s^3} + \frac{1}{s_0^3}\Big).$$

*Proof.* For $k_x = 0$ the two roots are $\omega s_0$ and $\omega s$, and the sum cancels. For $s = s_0$ the correction is 0 and the roots agree. For the expansion use $\sqrt{\omega^2 a^2 - k_x^2} = \omega a - \frac{k_x^2}{2\omega a} + O\big(\frac{k_x^4}{\omega^3 a^3}\big)$ for $a = s_0$ and $a = s$; the terms $\omega s_0$, $\omega(s - s_0)$ and $-\omega s$ cancel. $\square$

So the error grows with the square of the propagation angle ($k_x = \omega s \sin\theta$) and with the slowness contrast $|1/s - 1/s_0|$. Vertical waves are always continued exactly. How these local errors add up in a medium with a smooth $s(x)$ is not proved here; the statement that the method is accurate for moderate contrasts and angles is a heuristic, supported by the test with a lateral cosine velocity (every column focuses at the true depth).

**Energy.** $\Phi$ multiplies the propagating coefficients by numbers of modulus 1 and removes the others, and $\Lambda$ has modulus 1 everywhere. So each step does not increase the energy $\sum_j |p[j]|^2$, and the method is unconditionally stable for every $\Delta z$.
