---
title: Correctness of Kirchhoff migration
proves: [correctness, termination]
status: full
---

**Setting.** The model is the exploding reflector model in the constant velocity $v$, with $v' = v/2$. The zero-offset section $d(t, x)$ is the upgoing field at $z = 0$, and the exact image is the field at $t = 0$:
$$m(x, z) = \frac{1}{(2\pi)^2} \iint D(\omega, k_x)\, e^{i k_z z + i k_x x}\,d\omega\,dk_x, \qquad D(\omega, k_x) = \iint d(t, x)\, e^{-i\omega t - i k_x x}\,dt\,dx,$$
with $k_z = \operatorname{sgn}(\omega)\sqrt{\omega^2/v'^2 - k_x^2}$ (this is Step 1 of the proof of Stolt migration). For $|k_x| > |\omega|/v'$ we use the decaying branch $k_z = i\sqrt{k_x^2 - \omega^2/v'^2}$; these parts decay as $e^{-|k_z| z}$ with depth. The phase-shift method sets them to zero instead, so the two images differ by these decaying parts.

The proof has three parts. Theorem 1 says what the code computes, and it is exact. Theorem 2 says that the code's sum is the exact image up to an error that goes to zero at high frequency. Theorem 3 says that the stack and the modeling routine are exact adjoints.

**Theorem 1 (what the code computes).** Let $h_r$ be the trace at $x_r = r\Delta x$ after line L1, $h_r = \mathrm{IDFT}\big((-i\omega_k)^{1/2}\,\mathrm{DFT}(d_r)\big)$, with the principal square root and the value 0 at $\omega_k = 0$. For $i \ge 1$ the output of line L8 is
$$m[i][j] = \Delta x \sum_{r=0}^{n_x - 1} \frac{z_i / \rho}{\sqrt{2\pi v' \rho}}\; h_r^{\mathrm{lin}}(\rho / v'), \qquad \rho = \sqrt{z_i^2 + (x_j - x_r)^2},$$
where $h_r^{\mathrm{lin}}$ is the linear interpolant of the samples of $h_r$, set to zero outside the record. Row 0 is zero. The real part kept in line L1 is the whole value except at the Nyquist index: for $\omega_k < 0$ the principal root is the conjugate of the root at $-\omega_k$, so the filtered spectrum of a real trace keeps the conjugate symmetry.

*Proof.* Line L2 visits $i = 1, \ldots, n_z - 1$ and every $j$. For fixed $(i, j)$, line L3 sets $s = 0$, and lines L4 to L6 add, for every $r$, the weight and the sample of `kirchhoff_weight` and `sample`, which are the factor $(z_i/\rho)/\sqrt{2\pi v'\rho}$ and $h_r^{\mathrm{lin}}(\rho/v')$ (note $\rho/v' = 2\rho/v$). Line L7 stores $\Delta x\, s$. The loops have $(n_z - 1) n_x n_x$ passes, so the algorithm stops. $\blacksquare$

**Lemma (the kernel).** Fix $\omega > 0$ and put $k = \omega/v'$, $\xi = x - x_r$, $\rho = \sqrt{z^2 + \xi^2}$, $z > 0$. Then
$$G(\omega, \xi, z) := \frac{1}{2\pi}\int_{-\infty}^{\infty} e^{i k_z z + i k_x \xi}\,dk_x = \frac{i k}{2}\,\frac{z}{\rho}\,H_1^{(1)}(k\rho).$$

*Proof.* The Weyl (plane-wave) representation of the 2D outgoing Green's function is $H_0^{(1)}(k\rho) = \frac{1}{\pi}\int e^{i k_x \xi + i k_z z}\, k_z^{-1}\,dk_x$ for $z > 0$, with $k_z = \sqrt{k^2 - k_x^2}$ on the real branch and $k_z = i\sqrt{k_x^2 - k^2}$ on the decaying branch. Differentiate in $z$ under the integral (the factor $e^{-|k_z| z}$ makes this valid for $z > 0$): $\partial_z H_0^{(1)}(k\rho) = \frac{i}{\pi}\int e^{i k_x \xi + i k_z z}\,dk_x = 2i\,G$. On the other side, $\partial_z H_0^{(1)}(k\rho) = -k\,H_1^{(1)}(k\rho)\,\partial_z \rho = -k\,(z/\rho)\,H_1^{(1)}(k\rho)$. Divide by $2i$. $\square$

**Theorem 2 (the high-frequency limit).** Write $d_r(\omega)$ for the time transform of the trace at $x_r$. The exact image is
$$m(x, z) = \int dx_r\, \frac{1}{2\pi}\int d\omega\; d_r(\omega)\, G(\omega, x - x_r, z),$$
with $G(-\omega) = \overline{G(\omega)}$. As $k\rho \to \infty$,
$$G(\omega, \xi, z) = \frac{z/\rho}{\sqrt{2\pi v' \rho}}\,(-i\omega)^{1/2}\, e^{i\omega\rho/v'}\,\big(1 + O(1/(k\rho))\big).$$
So, up to this relative error at each frequency, $m(x, z) = \int dx_r\, \frac{z/\rho}{\sqrt{2\pi v'\rho}}\, h_r(\rho/v')$, where $h_r$ is the trace filtered by $(-i\omega)^{1/2}$. This is the continuous form of the sum in Theorem 1.

*Proof.* Put $D(\omega, k_x) = \int d_r(\omega)\, e^{-i k_x x_r}\,dx_r$ into the exact image and integrate over $k_x$ first; the inner integral is $2\pi\,G(\omega, x - x_r, z)$ by the lemma. For the asymptotic form use $H_1^{(1)}(y) = \sqrt{2/(\pi y)}\, e^{i(y - 3\pi/4)}\,(1 + O(1/y))$:
$$G = \frac{ik}{2}\,\frac{z}{\rho}\,\sqrt{\frac{2}{\pi k\rho}}\, e^{ik\rho}\, e^{-3i\pi/4}\,(1 + O(1/(k\rho))) = \frac{z}{\rho}\,\sqrt{\frac{k}{2\pi\rho}}\; e^{-i\pi/4}\, e^{ik\rho}\,(1 + O(1/(k\rho))),$$
since $i\,e^{-3i\pi/4} = e^{-i\pi/4}$. For $\omega > 0$, $\sqrt{k}\,e^{-i\pi/4} = \sqrt{\omega/v'}\,e^{-i\pi/4} = (-i\omega)^{1/2}/\sqrt{v'}$ with the principal root. The negative frequencies follow by conjugation. Finally $\frac{1}{2\pi}\int (-i\omega)^{1/2}\, d_r(\omega)\, e^{i\omega\rho/v'}\,d\omega = h_r(\rho/v')$ by the inverse time transform at $t = \rho/v'$. $\square$

The code replaces the integral over $x_r$ by the sum with the step $\Delta x$ and $h_r(t)$ by the linear interpolant of its samples. These two steps are discretizations, and their errors are not bounded here (a heuristic step; the tests measure a relative difference of about 0.09 to phase-shift migration for a point diffractor). The traces end at the edges of the line, so dips whose diffraction curves leave the line are lost.

**Theorem 3 (adjointness).** Let $S$ be the map of lines L2 to L8 (`diffraction_stack`) and $S^*$ the map of `kirchhoff_modeling`. For all data $d$ and images $m$, $\langle S d, m\rangle = \langle d, S^* m\rangle$ in the plain dot products of the arrays.

*Proof.* For $i \ge 1$ let $w = w_{ijr}$ be the weight, $\rho/v' = u\,\Delta t$ the time, $k = \lfloor u\rfloor$ and $f = u - k$, and let $\chi_{ijr} = 1$ if $0 \le k$ and $k + 1 < n_t$, else 0. Then
$$\langle S d, m\rangle = \sum_{i \ge 1, j} m[i][j]\,\Delta x \sum_r w\,\chi_{ijr}\,\big((1 - f)\,d[k][r] + f\,d[k + 1][r]\big).$$
All sums are finite, so they can be exchanged. Collecting the coefficient of each $d[k'][r]$ gives $\sum_{i \ge 1, j} \Delta x\, w\, \chi_{ijr}\, m[i][j]$ times $(1 - f)$ where $k = k'$ and times $f$ where $k + 1 = k'$. That is exactly the value that `kirchhoff_modeling` adds into `out[k'][r]` (an image value of 0 adds nothing, so skipping it changes nothing). $\blacksquare$

**What is not claimed.** The diffraction sum is not the inverse of the modeling operator $S^*$; it is the adjoint, up to the half-derivative filter. Amplitudes are correct only in the high-frequency limit of Theorem 2, for constant velocity, and with a dense and long enough line of traces.
