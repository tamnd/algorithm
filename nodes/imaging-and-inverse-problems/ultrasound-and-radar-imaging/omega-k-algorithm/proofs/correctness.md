---
title: After the reference multiply and the Stolt mapping, the phase of every target is linear in both frequencies, so one inverse DFT focuses all ranges
proves: [correctness]
status: full
---

We prove three facts about the omega-k algorithm as written on the main page (lines L1 to L7), for a straight track at the constant speed $V$, zero squint, point targets and the stop-and-go approximation. Theorem 1 is exact. Theorem 2 rests on the principle of stationary phase in the slow time, an asymptotic approximation; it uses no other approximation. Theorem 3 is exact given Theorem 2 and an exact interpolation in L4.

**Setting.** A target of amplitude $a$ at $(x_0, R_0)$ gives the raw signal $a\, w(\eta)\, p(\tau - 2R(\eta)/c)\, e^{-i 4\pi f_0 R(\eta)/c}$ with $R(\eta) = \sqrt{R_0^2 + (V\eta - x_0)^2}$, where $\tau$ is the absolute two-way time and $p$ the baseband pulse with spectrum $P$. The Fourier sign is $e^{-i 2\pi f t}$. For the range frequency $f_r$ and the Doppler frequency $f_a$ put $K = 4\pi (f_0 + f_r)/c$ and $k_x = 2\pi f_a / V$, and assume $|k_x| < K$ on the band.

**Theorem 1 (linearity).** The output of L1 to L7 is linear in the data.

*Proof.* L1 and L6 are DFTs; L2, L3, L5 and L7 are products with fixed functions; L4 is a weighted sum of samples with weights fixed by the geometry. $\square$

**Theorem 2 (the 2D spectrum).** After L2, the range Fourier transform of the target at $f_r$ is $a\, w(\eta)\, |P(f_r)|^2 e^{-i K R(\eta)}$, and under stationary phase in $\eta$ its Fourier transform in $\eta$ is

$$S(f_r, f_a) \approx a\, |P(f_r)|^2\, W\, A(f_r, f_a)\, e^{-i\pi/4}\, e^{-i R_0 \sqrt{K^2 - k_x^2}}\, e^{-i k_x x_0},$$

with a positive amplitude $A$ that varies slowly and does not depend on $x_0$.

*Proof.* The range Fourier transform of $p(\tau - \tau_d)$ is $P(f_r) e^{-i 2\pi f_r \tau_d}$. The DFT of the record measures time from $t_{\text{start}}$, so it gives $P(f_r) e^{-i 2\pi f_r (\tau_d - t_{\text{start}})}$, and the factor $e^{-i 2\pi f_r t_{\text{start}}}$ of L2 restores $e^{-i 2\pi f_r \tau_d}$. With $\tau_d = 2R/c$ and the carrier, the phase is $-4\pi (f_0 + f_r) R / c = -K R$, and $\text{conj}(P)$ turns $P$ into $|P|^2$. In $\eta$, the phase $\phi(\eta) = -K R(\eta) - 2\pi f_a \eta$ is that of the range-Doppler proof with $4\pi f_0/c$ replaced by $K$. With $u = V\eta - x_0$, $\phi'(\eta) = -K V u / R - 2\pi f_a$, so the stationary point has $u / R = -k_x / K$: the sine of the squint angle $\psi$ is $-k_x/K$. The value there is $-R_0 \sqrt{K^2 - k_x^2} - k_x x_0$, because $\phi = -\frac{K}{R}(R^2 - u^2) - k_x x_0$ at that point, $R^2 - u^2 = R_0^2$ and $\frac{K}{R}(R^2 - u^2) = K R_0 \cos\psi = R_0\sqrt{K^2 - k_x^2}$, and the term $-2\pi f_a x_0/V = -k_x x_0$ remains. The second derivative is negative, which gives $e^{-i\pi/4}$ and an amplitude $A = \sqrt{2\pi/|\phi''|}$ that depends on $R_0$, $f_r$, $f_a$ only. $\square$

**Theorem 3 (focus of every range).** Assume Theorem 2 and an exact interpolation in L4. After L3 to L5, the spectrum of the target, as a function of the new range frequency $f_r'$ with $|f_r'| \le B/2$ and of $f_a$, is

$$a\, \tilde A\, e^{-i\pi/4}\, e^{-i 4\pi f_0 (R_0 - r_{\text{ref}})/c}\, e^{-i 2\pi f_r' \cdot 2 (R_0 - r_{\text{start}})/c}\, e^{-i k_x x_0},$$

with $\tilde A = |P|^2 W A G$ slowly varying. So the 2D inverse DFT of L6 has its peak at the range bin $(R_0 - r_{\text{start}})/\Delta r$ and at the pulse of $x_0$, and after L7 the phase of the peak is $-\pi/4$ plus the phase of $a$, the same for every target.

*Proof.* L3 multiplies by $e^{+i r_{\text{ref}} \sqrt{K^2 - k_x^2}}$, which leaves $e^{-i (R_0 - r_{\text{ref}}) \sqrt{K^2 - k_x^2}}$. L4 evaluates the spectrum at the $f_r$ for which $\sqrt{K^2 - k_x^2} = 4\pi (f_0 + f_r')/c$; squaring, $(f_0 + f_r)^2 = (f_0 + f_r')^2 + (c f_a / (2V))^2$, which is the formula of L4. So the phase becomes $-4\pi (f_0 + f_r')(R_0 - r_{\text{ref}})/c - k_x x_0 = -4\pi f_0 (R_0 - r_{\text{ref}})/c - 2\pi f_r' \cdot 2(R_0 - r_{\text{ref}})/c - k_x x_0$. L5 adds $-2\pi f_r' \cdot 2(r_{\text{ref}} - r_{\text{start}})/c$, so the linear term becomes $-2\pi f_r' \cdot 2(R_0 - r_{\text{start}})/c$. A linear phase $e^{-i 2\pi f \Delta}$ over a band has an inverse DFT that peaks at the delay $\Delta$; here the delays are $2(R_0 - r_{\text{start}})/c$, which is bin $(R_0 - r_{\text{start}})/\Delta r$ at the sample rate $f_s$, and $x_0 / V$ in slow time. At that bin, L7 multiplies by $e^{+i 4\pi f_0 (R_0 - r_{\text{ref}})/c}$, which cancels the constant phase. $\square$

No step used an expansion of $\sqrt{K^2 - k_x^2}$, so the result holds for wide beams and for any $R_0$, which is the sense in which the algorithm is exact for its geometry. The errors that remain are those of the stationary phase step, the band edges where the Stolt mapping reads outside the recorded band, and the interpolation of L4. The example measures a common phase near $-44$ degrees, in line with the factor $e^{-i\pi/4}$.

**Cost.** L1 and L6 cost $O(M N \log(M N))$ with an FFT, L2, L3, L5 and L7 cost $O(M N)$, and L4 costs $O(K)$ per output sample, so the total is $O(M N (\log(M N) + K))$ in the real-RAM model, with $O(M N)$ extra space.
