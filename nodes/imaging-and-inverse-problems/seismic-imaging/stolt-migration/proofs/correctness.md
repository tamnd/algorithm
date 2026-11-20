---
title: Correctness of Stolt migration
proves: [correctness, termination]
status: full
---

**Setting.** The model is the exploding reflector model in the constant velocity $v$: the zero-offset section $d(t, x)$ is the upgoing field at $z = 0$ of the wave equation with the half velocity $v' = v/2$, and the image is the field at $t = 0$. Transforms use the sign of the area, $D(\omega, k_x) = \iint d(t, x)\, e^{-i\omega t - i k_x x}\,dt\,dx$, and the inverse carries the factor $(2\pi)^{-2}$. On the non-evanescent set $|k_x| < |\omega|/v'$ put $k_z(\omega, k_x) = \operatorname{sgn}(\omega)\sqrt{\omega^2/v'^2 - k_x^2}$.

**Step 1 (the image as an integral over $\omega$).** By the phase-shift lemma (the field at depth $z$ is $D(\omega, k_x)\, e^{i k_z z}$; see the proof of phase-shift migration), the image is
$$m(x, z) = \frac{1}{(2\pi)^2} \iint_{|k_x| < |\omega|/v'} D(\omega, k_x)\, e^{i k_z(\omega, k_x) z + i k_x x}\,d\omega\,dk_x,$$
because the factor $e^{i\omega t}$ of the inverse time transform is 1 at $t = 0$.

**Step 2 (the change of variables).** Fix $k_x$. On the branch $\omega > v'|k_x|$, the map $\omega \mapsto k_z = \sqrt{\omega^2/v'^2 - k_x^2}$ is a smooth bijection onto $(0, \infty)$ with inverse $\omega = v'\sqrt{k_x^2 + k_z^2}$ and
$$\frac{d\omega}{dk_z} = \frac{v' k_z}{\sqrt{k_x^2 + k_z^2}} > 0.$$
On the branch $\omega < -v'|k_x|$, the map $\omega \mapsto k_z = -\sqrt{\omega^2/v'^2 - k_x^2}$ is a bijection onto $(-\infty, 0)$ with inverse $\omega = -v'\sqrt{k_x^2 + k_z^2}$ and
$$\frac{d\omega}{dk_z} = \frac{-v' k_z}{\sqrt{k_x^2 + k_z^2}} = \frac{v'|k_z|}{\sqrt{k_x^2 + k_z^2}} > 0.$$
Both branches keep the orientation, so with $\omega(k_z, k_x) = \operatorname{sgn}(k_z)\, v'\sqrt{k_x^2 + k_z^2}$ the substitution gives
$$m(x, z) = \frac{1}{(2\pi)^2} \iint M(k_z, k_x)\, e^{i k_z z + i k_x x}\,dk_z\,dk_x, \qquad M(k_z, k_x) = \frac{v'|k_z|}{\sqrt{k_x^2 + k_z^2}}\, D(\omega(k_z, k_x), k_x).$$
The set $k_z = 0$ has measure zero. So $m$ is the inverse 2D Fourier transform of $M$: the Stolt mapping. Note the absolute value. The factor $v' k_z/\sqrt{k_x^2 + k_z^2}$ without it is correct only for $k_z \ge 0$; with it, $M(-k_z, -k_x) = \overline{M(k_z, k_x)}$ for real data, so the image is real. $\square$

**Step 3 (the discrete scale).** Let $D[k][j] = \sum_{\ell, r} d(\ell\Delta t, r\Delta x)\, e^{-i\omega_k \ell\Delta t - i k_{x,j} r\Delta x}$ be the DFT of line L2. For a section that is band limited and zero outside the record, $D[k][j] = D(\omega_k, k_{x,j})/(\Delta t\,\Delta x)$ (the sum is the Riemann sum of the integral, which is exact for band-limited samples on a grid finer than the Nyquist rate). The inverse DFT of an $n_z \times n_x$ array $M[i][j]$ gives $\frac{1}{n_z n_x}\sum M[i][j]\, e^{i(k_{z,i} z + k_{x,j} x)}$, the Riemann sum of $(2\pi)^{-2}\iint M e^{i(\cdot)}\,dk_z\,dk_x$ times $\Delta z\,\Delta x$, since $\Delta k_z \Delta k_x = (2\pi)^2/(n_z \Delta z\, n_x \Delta x)$. So the discrete image equals the continuous one when
$$M[i][j] = \frac{M(k_{z,i}, k_{x,j})}{\Delta z\,\Delta x} = \frac{\Delta t}{\Delta z}\cdot\frac{v'|k_{z,i}|}{\sqrt{k_{x,j}^2 + k_{z,i}^2}}\cdot D[\omega(k_{z,i}, k_{x,j})][j],$$
which is line L7, with $D$ at the frequency $\omega(k_{z,i}, k_{x,j})$. $\square$

**Theorem (what the pseudocode computes).** Lines L3 to L7 visit every pair $(i, j)$ once. For each, line L4 computes $\omega(k_{z,i}, k_{x,j})$ and the Jacobian of Step 2. Line L5 leaves $M[i][j] = 0$ when the Jacobian is 0 (the point $k_z = 0$) or when $\omega$ lies outside the open band of the DFT frequencies of the padded record. Line L6 is the linear interpolation of $D[\cdot][j]$ between the two DFT frequencies around $\omega$, and line L7 stores the value of Step 3 with this interpolated $D$. Line L8 is the inverse 2D DFT, and line L9 returns its real part. So the output is the inverse transform of the discrete Stolt mapping of Step 3, with $D(\omega)$ replaced by its linear interpolant. The loops have $n_z n_x$ passes, so the algorithm stops. $\blacksquare$

**Corollary (exact cases).** If every $\omega(k_{z,i}, k_{x,j})$ that is used falls on a frequency of the padded DFT, the interpolation in line L6 is exact and the result equals the discrete form of Step 2. This holds for $k_x = 0$ when $\Delta z = v'\Delta t$ and the padded length is a multiple of $n_z$: then $\omega = v' k_{z,i}$ is the DFT frequency $p\,i$ of the padded record with $p = n_t^{\text{pad}}/n_z$. A section that is constant in $x$ is then mapped sample by sample from time to depth, $z = v' t$, up to the frequencies removed at line L5.

**What is approximate.** In general $\omega(k_z, k_x)$ falls between DFT frequencies. Linear interpolation of a spectrum is a low-order approximation, and its error is the main error of the method (a heuristic statement, supported by a measurement: for the point diffractor of the tests, the relative difference to phase-shift migration was 0.84 without padding, 0.27 with padding by 2, 0.094 with padding by 4 and 0.067 with padding by 8). Both the DFT and the image are periodic, so events near the edges wrap around.
