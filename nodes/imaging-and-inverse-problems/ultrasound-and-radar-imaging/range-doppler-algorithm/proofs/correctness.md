---
title: The range-Doppler algorithm is linear and, under the stationary phase approximation, focuses a point target at its position with the matched filter gain
proves: [correctness]
status: full
---

We prove four facts about the RDA as written on the main page (lines L1 to L9) for the stripmap model with zero squint: a straight track at the speed $V$, point targets, a constant speed of light $c$, and the stop-and-go approximation. Theorem 1 is exact. Theorems 2 to 4 are statements about the continuous model under the principle of stationary phase, which is an asymptotic approximation that is good when the azimuth time-bandwidth product $K_a T_a^2$ is large; they are not exact statements about the sampled data.

**Setting.** After range compression, a target of amplitude $a$ at the along-track position $x_0 = V \eta_0$ and the closest range $R_0$ gives

$$s_c(\tau, \eta) = a\, w(\eta - \eta_0)\, p_c\!\left(\tau - \frac{2R(\eta)}{c}\right) e^{-i 4\pi f_0 R(\eta)/c}, \qquad R(\eta) = \sqrt{R_0^2 + V^2 (\eta - \eta_0)^2},$$

with the compressed pulse $p_c$ (peak $p_c(0)$ at zero delay), the window $w$ of the beam, and the Fourier sign $e^{-i 2\pi f t}$. Write $\lambda = c/f_0$, $D(f) = \sqrt{1 - (\lambda f / (2V))^2}$ and $K_a(f) = 2 V^2 f_0 D(f)^3 / (c R_0)$.

**Theorem 1 (linearity).** The output of lines L1 to L9 is a linear function of the input $s$. So the image of a sum of targets is the sum of their images.

*Proof.* L1, L2 and L9 are DFTs and products with a fixed sequence. L6 is a weighted sum of samples with weights that depend only on $j$, $k$ and the geometry. L8 multiplies by a factor that does not depend on the data. A composition of linear maps is linear. $\square$

**Theorem 2 (the range-Doppler signal).** Under the stationary phase approximation, and treating the envelope $p_c$ and the window $w$ as slowly varying, the azimuth Fourier transform $S_c(\tau, f) = \int s_c(\tau, \eta)\, e^{-i 2\pi f \eta}\, d\eta$ is

$$S_c(\tau, f) \approx \frac{a\, e^{-i\pi/4}}{\sqrt{K_a(f)}}\, W(f)\, p_c\!\left(\tau - \frac{2 R_0}{c\, D(f)}\right) e^{-i 4\pi f_0 R_0 D(f)/c}\, e^{-i 2\pi f \eta_0},$$

where $W(f)$ is the value of $w$ at the stationary point.

*Proof.* The phase of the integrand is $\phi(\eta) = -4\pi f_0 R(\eta)/c - 2\pi f \eta$. Put $u = \eta - \eta_0$. Then $\phi'(\eta) = -\frac{4\pi f_0}{c} \frac{V^2 u}{R} - 2\pi f$, which is zero when $\frac{V u}{R} = -\frac{\lambda f}{2V}$. Call this number $\sin\psi$; then $R_0 = R \cos\psi$, so $R = R_0 / D(f)$ at the stationary point, and $f u = -\frac{2 f_0 V^2 u^2}{c R}$. The phase there is

$$\phi^\ast = -\frac{4\pi f_0 R}{c} + \frac{4\pi f_0 V^2 u^2}{c R} - 2\pi f \eta_0 = -\frac{4\pi f_0}{c R}(R^2 - V^2 u^2) - 2\pi f \eta_0 = -\frac{4\pi f_0 R_0 D(f)}{c} - 2\pi f \eta_0,$$

because $R^2 - V^2 u^2 = R_0^2$ and $R_0^2 / R = R_0 D$. The second derivative is $\phi''(\eta) = -\frac{4\pi f_0}{c} \frac{V^2 R_0^2}{R^3}$, and at the stationary point its size is $\frac{4\pi f_0 V^2 D^3}{c R_0} = 2\pi K_a(f)$. The stationary phase formula $\int g(\eta) e^{i\phi(\eta)} d\eta \approx g(\eta^\ast) \sqrt{2\pi / |\phi''(\eta^\ast)|}\, e^{i\phi^\ast - i\pi/4}$ for $\phi'' < 0$ gives the factor $e^{-i\pi/4}/\sqrt{K_a}$, and the envelope is evaluated at the range $R_0/D(f)$ of the stationary point. $\square$

The range $R_0 / D(f)$ of the envelope depends on $R_0$ and $f$ only, not on $\eta_0$. This is the invariant that lets one interpolation correct all targets at the same range.

**Theorem 3 (migration correction).** Assume that L6 interpolates the range-Doppler line exactly (a band-limited signal and an ideal interpolator). Then after L6 the value in the bin $j$ with $r_{\text{start}} + j \Delta r = R_0$ at Doppler frequency $f$ is $S_c(2 R_0 / (c D(f)), f)$, which by Theorem 2 has the envelope value $p_c(0)$, its peak, for every $f$.

*Proof.* L5 sets $u$ to the fractional bin of the range $R_0 / D(f)$, and an exact interpolation returns the value of the line at that range. The delay argument of $p_c$ in Theorem 2 is then $0$. $\square$

Without L5, that is with $u = j$, the envelope is $p_c(2R_0(1 - 1/D)/c)$, smaller than the peak wherever the migration $R_0 (1/D - 1)$ is a sizable part of the range resolution. This is the loss that the example measures.

**Theorem 4 (azimuth compression and the peak).** Under the assumptions of Theorems 2 and 3, with the DFT approximating $\text{PRF}$ times the integral and the pulses at $\eta_p = (p - M/2)/\text{PRF}$, the image of the target is largest at the pulse $p_0$ with $\eta_{p_0} = \eta_0$, and its value there is about $a\, e^{-i\pi/4}\, n_a\, p_c(0)$, where $n_a$ is the number of pulses in the beam. For a chirp of $n_c$ samples of modulus 1, $p_c(0) = n_c$, so the value is $a$ times the energy of the echo, the matched filter value.

*Proof.* After L6 the value at Doppler bin $k$ (frequency $f_k$) is $\text{PRF}\, a\, e^{-i\pi/4} W(f_k) p_c(0) e^{-i 4\pi f_0 R_0 D(f_k)/c} e^{-i 2\pi f_k \eta_0} / \sqrt{K_a(f_k)}$. L7 and L8 multiply by $\text{PRF}\, e^{+i 4\pi f_0 R_0 D(f_k)/c} / \sqrt{K_a(f_k)}$, which leaves $a\, e^{-i\pi/4} p_c(0)\, \text{PRF}^2 W(f_k) e^{-i 2\pi f_k \eta_0} / K_a(f_k)$. The inverse DFT of L9 at pulse $p$ is $\frac{1}{M}\sum_k$ of this times $e^{i 2\pi f_k \eta_p}$, a sum of terms of one phase when $\eta_p = \eta_0$, and of rotating phases otherwise. At $\eta_p = \eta_0$, with $W = 1$ on the beam band, $K_a$ close to its value at $f = 0$, and $\frac{\text{PRF}}{M}$ the spacing of the Doppler bins, the sum is about $a\, e^{-i\pi/4} p_c(0)\, \text{PRF}\, B_a / K_a$, where $B_a$ is the Doppler bandwidth of the beam. The target is in view for the time $T_a = B_a / K_a$, which is $n_a / \text{PRF}$, so the value is $a\, e^{-i\pi/4} p_c(0)\, n_a$. The matched filter value of the target with itself is $a \sum_{p, j} |\text{echo}|^2 = a\, n_a n_c$. $\square$

The constant $e^{-i\pi/4}$ is common to all targets, so ratios of complex amplitudes are kept. The example measures a common phase of about $-38$ degrees and a peak of 0.90 of the matched filter value, the difference coming from the approximations above, the finite interpolator, and the coupling of range and azimuth that the basic RDA ignores.

**Cost.** L1 costs $O(M N \log N)$ with an FFT, L2 and L9 cost $O(M N \log M)$, and L3 to L8 cost $O(K)$ per Doppler bin and range bin, $O(M N K)$. The total is $O(M N (\log(M N) + K))$ in the real-RAM model, with $O(M N)$ extra space for the range-Doppler array.
