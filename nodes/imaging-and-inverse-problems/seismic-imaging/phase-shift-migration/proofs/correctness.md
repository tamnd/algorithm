---
title: Correctness of phase-shift migration
proves: [correctness, termination]
status: full
---

**Setting.** The model is the exploding reflector model: the zero-offset section $d(t, x)$ is the upgoing wavefield $p(t, x, z)$ at $z = 0$, where $p$ solves the scalar wave equation $p_{zz} + p_{xx} - p_{tt}/v'^2 = 0$ with the half velocity $v' = v/2$, and the image is $p(0, x, z)$. The velocity is constant in each layer $z_i \le z < z_{i+1}$, $z_i = i\,\Delta z$, with the value $v'_i = v_i/2$. Transforms use the sign of the area: $P(\omega, k_x, z) = \iint p(t, x, z)\, e^{-i\omega t - i k_x x}\,dt\,dx$. For $\omega \ne 0$ and $\omega^2/v'^2 > k_x^2$ put $k_z(\omega, k_x, v') = \operatorname{sgn}(\omega)\sqrt{\omega^2/v'^2 - k_x^2}$; the other pairs $(\omega, k_x)$ are called evanescent.

The discrete statements are about the arrays of the pseudocode. $P_i[k][j]$ is the value of the array $P$ at the start of pass $i$ of the loop at line L2. $\omega_k$ and $k_{x,j}$ are the signed DFT frequencies of index $k$ and $j$ ($k$ for $2k < n$, else $k - n$, times $2\pi/(n\,\Delta)$).

**Lemma 1 (one layer).** In a layer of constant $v'$, every solution of the wave equation has, for a non-evanescent pair $(\omega, k_x)$, the form $P(z) = A e^{i k_z z} + B e^{-i k_z z}$. The upgoing part is $A e^{i k_z z}$, so the upgoing field at $z + \Delta z$ is $P(z + \Delta z) = P(z)\, e^{i k_z \Delta z}$.

*Proof.* The transform turns $\partial_t$ into $i\omega$ and $\partial_x$ into $i k_x$, so the wave equation becomes $P_{zz} + (\omega^2/v'^2 - k_x^2) P = P_{zz} + k_z^2 P = 0$, a linear ODE in $z$ with the two solutions $e^{\pm i k_z z}$. For $k_x = 0$ the upgoing wave is $p(t, x, z) = p(t + z/v', x, 0)$, because the wave reaches the depth $z$ a time $z/v'$ before it reaches the surface. Its transform is $P(\omega, 0, z) = P(\omega, 0, 0)\, e^{i\omega z/v'}$, which is $e^{+i k_z z}$ with $k_z = \omega/v'$. The function $k_x \mapsto k_z(\omega, k_x, v')$ is continuous and never zero on the non-evanescent interval $|k_x| < |\omega|/v'$, so the root with the sign of $\omega$ is the upgoing branch on the whole interval. $\square$

**Lemma 2 (the image row).** For any array $Q[k][j]$, line L3 followed by line L4 gives the row $\operatorname{Re}\, q(0, x_j)$, where $q(t_\ell, x_j) = \frac{1}{n_t n_x}\sum_{k,j'} Q[k][j']\, e^{i\omega_k t_\ell + i k_{x,j'} x_j}$ is the inverse 2D DFT of $Q$.

*Proof.* At $t_0 = 0$ the factor $e^{i\omega_k t_0}$ is 1, so the inverse transform in time at $t = 0$ is $\frac{1}{n_t}\sum_k Q[k][j']$, which is line L3. Line L4 applies the inverse DFT in $x$ (the helper divides by $n_x$) and keeps the real part. $\square$

**Theorem 1 (loop invariant).** At the start of pass $i$ of the loop at line L2,
$$P_i[k][j] = \begin{cases} D[k][j]\, \exp\Big(i \sum_{l=0}^{i-1} k_z(\omega_k, k_{x,j}, v'_l)\,\Delta z\Big) & \text{if } (\omega_k, k_{x,j}) \text{ is non-evanescent for } v'_0, \ldots, v'_{i-1}, \\ 0 & \text{otherwise,} \end{cases}$$
where $D = \mathrm{DFT2}(d)$ is the array of line L1. So $P_i$ is the DFT of the field continued to depth $z_i$ by Lemma 1 in each layer, with the evanescent parts removed, and row $i$ of the image is $\operatorname{Re}$ of that field at $t = 0$.

*Proof.* Induction on $i$. Initialization: before pass 0 the sum is empty and $P_0 = D$ by line L1. Maintenance: assume the claim for $i$. Line L3 and line L4 do not change $P$, and by Lemma 2 they store the real part of the inverse transform of $P_i$ at $t = 0$ as row $i$. Lines L5 to L9 then visit every pair $(k, j)$ once (line L6). If the pair is evanescent for $v'_i$, line L8 sets the entry to 0, which is the second case for $i + 1$. Otherwise line L7 computes $k_z(\omega_k, k_{x,j}, v'_i)$ and line L9 multiplies the entry by $e^{i k_z \Delta z}$, which adds the term $l = i$ to the sum (an entry that is already 0 stays 0). This is the claim for $i + 1$. Termination: the loop at line L2 runs $n_z$ times and the inner loop $n_t n_x$ times, so the algorithm stops after $n_z n_t n_x$ updates and line L10 returns the $n_z$ rows. $\blacksquare$

**Theorem 2 (exact for $v(z)$ in the discrete model).** Let the true field in the model be a finite sum of the DFT plane waves $e^{i(\omega_k t + k_{x,j} x)}$ restricted to the upgoing branch, periodic in $t$ and $x$ with the periods $n_t \Delta t$ and $n_x \Delta x$, and with no evanescent components. Then row $i$ of the image is exactly the field $p(0, x_j, z_i)$.

*Proof.* By Lemma 1 each plane wave at depth $z_i$ is the plane wave at the surface times $\prod_l e^{i k_z(\omega_k, k_{x,j}, v'_l)\Delta z}$, which is the factor in Theorem 1. The DFT of the sampled sum is the array of coefficients, so $P_i$ is the DFT of the samples of $p(\cdot, \cdot, z_i)$, and by Lemma 2 row $i$ is $\operatorname{Re}\, p(0, x_j, z_i)$. A real field has a real value. $\square$

**Corollary (vertical waves).** For $k_x = 0$ the factor of Theorem 1 is $e^{i\omega_k \tau_i}$ with $\tau_i = \sum_{l<i} \Delta z/v'_l = \sum_{l<i} 2\Delta z/v_l$, the two-way vertical time to $z_i$. So a section that is constant in $x$ is mapped by $z_i \mapsto$ the trigonometric interpolant of the trace at $t = \tau_i$ (without the frequency $\omega = 0$ and with the Nyquist index treated as a negative frequency). When $\tau_i$ falls on a sample, the image is that sample. This is the time-to-depth conversion. $\square$

**What is not claimed.** The data of a real experiment are not periodic, the wavelet is not band limited, and the exploding reflector model ignores multiples and ray paths that differ for the down and up legs. Theorem 2 is a statement about the model and the discrete grid. Lateral velocity changes are outside the method: Lemma 1 needs a constant velocity across $x$ inside each layer.
