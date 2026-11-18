---
title: Correctness and error bound of the nine term irradiance map
proves: [correctness]
status: full
---

**Setting.** The lighting is a radiance $L(\omega) \ge 0$ on the unit sphere $S^2$, for distant sources, so it depends on the direction only. The surface is Lambertian and the visibility is ignored. The irradiance at a unit normal $n$ is

$$E(n) = \int_{S^2} L(\omega)\, A(n \cdot \omega)\, d\omega, \qquad A(t) = \max(t, 0).$$

$Y_{lm}$ are the real spherical harmonics of the page, orthonormal on $S^2$. Lines L1 to L3 compute $L_{lm} = \sum_k L(\omega_k) Y_{lm}(\omega_k) \Delta\omega_k$ for $l \le 2$, line L4 builds the matrix $M$ and line L7 returns $E_9(n) = \tilde n^T M \tilde n$ with $\tilde n = (x, y, z, 1)$. The claims are about this computation in exact arithmetic.

**Claim 1 (the kernel in each band).** For every $l$ and every unit $n$,

$$\int_{S^2} Y_{lm}(\omega) A(n \cdot \omega)\, d\omega = \hat A_l\, Y_{lm}(n), \qquad \hat A_l = 2\pi \int_0^1 t\, P_l(t)\, dt,$$

where $P_l$ is the Legendre polynomial. In particular $\hat A_0 = \pi$, $\hat A_1 = 2\pi/3$ and $\hat A_2 = \pi/4$.

*Proof.* The function $A$ is in $L^2([-1, 1])$, so it has the Legendre expansion $A(t) = \sum_j a_j P_j(t)$ with $a_j = \frac{2j+1}{2} \int_{-1}^1 A(t) P_j(t)\, dt = \frac{2j+1}{2} \int_0^1 t P_j(t)\, dt$. The addition theorem gives $P_j(n \cdot \omega) = \frac{4\pi}{2j+1} \sum_{m'} Y_{jm'}(n) Y_{jm'}(\omega)$. Put this into the integral. By orthonormality only the term $j = l$, $m' = m$ is left, and its value is $a_l \frac{4\pi}{2l+1} Y_{lm}(n) = 2\pi \int_0^1 t P_l(t)\, dt \cdot Y_{lm}(n)$. With $P_0 = 1$, $P_1 = t$ and $P_2 = (3t^2 - 1)/2$, the integrals are $1/2$, $1/3$ and $(3/4 - 1/2)/2 = 1/8$, so $\hat A_0 = \pi$, $\hat A_1 = 2\pi/3$ and $\hat A_2 = \pi/4$. $\square$

**Claim 2 (the matrix is the truncated sum).** For all coefficients $L_{lm}$ and all unit $n$, $\tilde n^T M \tilde n = \sum_{l \le 2} \sum_m \hat A_l L_{lm} Y_{lm}(n)$.

*Proof.* Write the constants as $c_1 = \hat A_2 \cdot 0.546274 = \hat A_2 \cdot \frac14 \sqrt{15/\pi}$, $c_2 = \frac12 \hat A_1 \sqrt{3/(4\pi)}$, $c_3 = 3 \hat A_2 \cdot \frac14 \sqrt{5/\pi}$, $c_4 = \hat A_0 \cdot \frac12 \sqrt{1/\pi}$ and $c_5 = \hat A_2 \cdot \frac14 \sqrt{5/\pi}$. Expand $\tilde n^T M \tilde n$ for the symmetric $M$ of line L4:

$$c_1 L_{22}(x^2 - y^2) + c_3 L_{20} z^2 + c_4 L_{00} - c_5 L_{20} + 2 c_1 (L_{2,-2} xy + L_{21} xz + L_{2,-1} yz) + 2 c_2 (L_{11} x + L_{1,-1} y + L_{10} z).$$

Compare with the sum term by term. Band 0: $\hat A_0 L_{00} Y_{00} = c_4 L_{00}$. Band 1: $\hat A_1 \sqrt{3/(4\pi)} = 2 c_2$, and $Y_{1,-1}, Y_{10}, Y_{11}$ are $\sqrt{3/(4\pi)}$ times $y, z, x$. Band 2: the factor of $Y_{2,-2}, Y_{2,-1}, Y_{21}$ is $\frac12\sqrt{15/\pi} = 2 \cdot \frac14 \sqrt{15/\pi}$, so their terms are $2 c_1$ times $xy$, $yz$, $xz$; the term of $Y_{22}$ is $c_1 (x^2 - y^2)$; the term of $Y_{20}$ is $\hat A_2 \frac14 \sqrt{5/\pi} (3 z^2 - 1) = c_3 z^2 - c_5$. Every term matches. $\square$

**Claim 3 (exact for band limited lighting).** If the rule of lines L1 to L3 gives the exact coefficients $L_{lm} = \int L Y_{lm}\, d\omega$, and $L$ has no component in the bands $l \ge 3$, then $E_9(n) = E(n)$ for every $n$.

*Proof.* Write $L = \sum_{l \le 2, m} L_{lm} Y_{lm}$. By linearity and Claim 1, $E(n) = \sum_{l \le 2, m} L_{lm} \hat A_l Y_{lm}(n)$, which is $E_9(n)$ by Claim 2. $\square$

The test file uses a rule that is Gauss-Legendre in $z$ on each hemisphere and uniform in $\varphi$. It integrates every polynomial of degree at most 4 in $(x, y, z)$ exactly, so the coefficients of a band limited lighting, and of the sky of the page, are exact.

**Claim 4 (the kernel of nine terms).** Define $A_9(t) = \sum_{l \le 2} \frac{2l+1}{4\pi} \hat A_l P_l(t)$. Then $A_9(t) = \frac{3}{32} + \frac t2 + \frac{15}{32} t^2$, and $\max_{t \in [-1, 1]} |A(t) - A_9(t)| = \frac{3}{32}$, reached only at $t = 0$.

*Proof.* The three terms are $\frac{1}{4\pi}\pi = \frac14$, $\frac{3}{4\pi}\frac{2\pi}{3} t = \frac t2$ and $\frac{5}{4\pi}\frac{\pi}{4}\frac{3t^2 - 1}{2} = \frac{15 t^2 - 5}{32}$. Their sum is the stated polynomial. On $[0, 1]$, $A_9(t) - A(t) = (15 t^2 - 16 t + 3)/32$. This parabola has its values $3/32$ at $t = 0$ and $2/32$ at $t = 1$, and its smallest value $-19/480 \approx -0.0396$ at $t = 8/15$, so its absolute value is at most $3/32$, with equality only at $t = 0$. On $[-1, 0]$, $A_9(t) - A(t) = (15 t^2 + 16 t + 3)/32$, the mirror image of the same parabola, with the same bound. $\square$

**Claim 5 (error bound for any lighting).** If $L \ge 0$ and the coefficients are exact, then for every unit $n$,

$$|E(n) - E_9(n)| \le \frac{3}{32} \int_{S^2} L(\omega)\, d\omega.$$

The same bound holds for the texel sums: if $E$ is the brute force sum $\sum_k L_k A(n \cdot \omega_k) \Delta\omega_k$ and $E_9$ is computed from the coefficients of lines L1 to L3 on the same texels, then $|E - E_9| \le \frac{3}{32} \sum_k L_k \Delta\omega_k$. The bound is reached by a point light at a normal perpendicular to it.

*Proof.* By the addition theorem, $\sum_{l \le 2, m} \hat A_l Y_{lm}(n) Y_{lm}(\omega) = A_9(n \cdot \omega)$. Multiply by $L(\omega)$ and integrate, then use Claim 2: $E_9(n) = \int L(\omega) A_9(n \cdot \omega)\, d\omega$. So $E(n) - E_9(n) = \int L(\omega) (A - A_9)(n \cdot \omega)\, d\omega$. With $L \ge 0$ and Claim 4, its absolute value is at most $\frac{3}{32} \int L$. For the texels, the same steps hold with the integral replaced by the sum over $k$, because the coefficients of line L3 are exactly $\sum_k L_k Y_{lm}(\omega_k) \Delta\omega_k$. For a point light of power $P$ in the direction $d$ and $n \perp d$, $E(n) = 0$ and $E_9(n) = P A_9(0) = \frac{3}{32} P$. $\square$

Ramamoorthi and Hanrahan state this as a maximum pixel error of 9% of the total intensity; $3/32 = 9.375\%$. Their second number, an average error under 3% over all normals for any physical lighting, they take from Basri and Jacobs. This proof does not cover it.

**Cost.** Lines L1 to L3 do 9 multiply-adds per texel, $\Theta(s)$ for $s$ texels, and keep 9 numbers. Line L4 costs $O(1)$. Lines L6 and L7 cost 16 multiplications and additions, $O(1)$ per normal. An RGB map repeats the work three times. $\blacksquare$
