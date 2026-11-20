---
title: Chirp scaling equalizes the range cell migration of every range exactly, so phase multiplies focus the range-Doppler signal model
proves: [correctness]
status: full
---

We prove three facts about the CSA as written on the main page (lines L1 to L8) for the stripmap model with zero squint. Theorem 1 is exact. Theorem 2 is an exact identity about chirps. Theorem 3 applies it to the range-Doppler signal model, which itself rests on the principle of stationary phase in azimuth and on the rate $K_m$ evaluated at the reference range; those are approximations, not theorems about the sampled data.

**Setting.** Write $D = D(f) = \sqrt{1 - (\lambda f/(2V))^2}$ for a fixed Doppler frequency $f$, $a = 1/D - 1$, and $\tau$ for the two-way time measured from the center of the chirp. The range-Doppler signal model (Cumming and Wong, Chapter 7) says that, after the azimuth DFT of L1, a target of amplitude $\alpha$ at the closest range $R_0$ and along-track time $\eta_0$ is

$$S(\tau, f) = C(f)\, \alpha\, e^{i\pi K_m (\tau - \tau_d)^2}\, e^{-i 4\pi f_0 R_0 D/c}\, e^{-i 2\pi f \eta_0}, \qquad \tau_d = \frac{2 R_0}{c D},$$

for $|\tau - \tau_d| \le T/2$, with a factor $C(f)$ that does not depend on $R_0$ or $\tau$. The derivation of the delay $\tau_d$ and of the azimuth phase is the stationary phase computation of the range-Doppler algorithm proof; the rate $K_m$ comes from the same computation carried to second order in the range frequency, and the model takes it at $R_0 = r_{\text{ref}}$.

**Theorem 1 (linearity).** The output of L1 to L8 is linear in the data.

*Proof.* Every line is a DFT, an inverse DFT, or a product with a function that depends only on the indices and the geometry. $\square$

**Theorem 2 (chirp scaling identity).** For real numbers $K$, $a$ with $1 + a \ne 0$ and any $\tau_d$, $\tau_{\text{ref}}$,

$$e^{i\pi K (\tau - \tau_d)^2}\, e^{i\pi K a (\tau - \tau_{\text{ref}})^2} = e^{i\pi K (1 + a) (\tau - \tau_c)^2}\, e^{i\pi K \frac{a}{1 + a} (\tau_d - \tau_{\text{ref}})^2}, \qquad \tau_c = \tau_{\text{ref}} + \frac{\tau_d - \tau_{\text{ref}}}{1 + a}.$$

*Proof.* Put $t = \tau - \tau_{\text{ref}}$ and $\delta = \tau_d - \tau_{\text{ref}}$. The exponent divided by $i\pi K$ is $(t - \delta)^2 + a t^2 = (1 + a) t^2 - 2\delta t + \delta^2 = (1 + a)\big(t - \frac{\delta}{1 + a}\big)^2 + \delta^2 - \frac{\delta^2}{1 + a}$, and $\delta^2 - \frac{\delta^2}{1 + a} = \frac{a}{1 + a}\delta^2$. $\square$

**Theorem 3 (equal migration and focus).** In the signal model, take $K = K_m$, $a = 1/D - 1$ and $\tau_{\text{ref}} = 2 r_{\text{ref}}/(c D)$ as in L2 and L3. Then:

1. after L3, the target is a chirp of rate $K_m / D$ centered at $\tau_c = 2R_0/c + 2 r_{\text{ref}}\, a / c$;
2. the extra constant phase is $\Delta\varphi = 4\pi K_m (1 - D)(R_0 - r_{\text{ref}})^2 / (c^2 D^2)$;
3. after L4 to L6, the target is a compressed pulse centered at $2R_0/c$, the time of its own range bin, for every $f$;
4. after L7, the remaining phase is $e^{-i 2\pi f \eta_0}$ times a constant that does not depend on $f$, so L8 focuses the target at $\eta_0$.

*Proof.* Here $1 + a = 1/D$. By Theorem 2 the rate is $K_m/D$ and $\tau_c = \tau_{\text{ref}} + D(\tau_d - \tau_{\text{ref}}) = \frac{2 r_{\text{ref}}}{c D} + \frac{2 (R_0 - r_{\text{ref}})}{c} = \frac{2R_0}{c} + \frac{2 r_{\text{ref}}}{c}\Big(\frac1D - 1\Big)$, which is part 1. The constant phase is $\pi K_m \frac{a}{1 + a} \delta^2 = \pi K_m (1 - D)\, \frac{4 (R_0 - r_{\text{ref}})^2}{c^2 D^2}$ with $\delta = 2(R_0 - r_{\text{ref}})/(c D)$, which is part 2. For part 3, a chirp $e^{i\pi K (\tau - \tau_c)^2}$ has, by stationary phase, the spectrum $K^{-1/2} e^{i\pi/4} e^{-i\pi f_q^2 / K} e^{-i 2\pi f_q \tau_c}$ over its band. With $K = K_m/D$, L5 multiplies by $e^{+i\pi D f_q^2 / K_m}$, which removes the quadratic phase, and by $e^{+i 2\pi f_q \cdot 2 r_{\text{ref}} a / c}$, which changes $\tau_c$ into $2R_0/c$. The spectrum left is flat in phase except the delay $2R_0/c$, so the inverse DFT of L6 is a compressed pulse at that delay, the same for every $f$. For part 4, the phase left is $e^{-i 4\pi f_0 R_0 D/c}\, e^{-i 2\pi f \eta_0}\, e^{i\Delta\varphi}$ times a constant; at the bin of $R_0$, L7 multiplies by $e^{+i 4\pi f_0 R_0 D / c}\, e^{-i\Delta\varphi}$. What remains is linear in $f$, and the inverse DFT of L8 turns it into a peak at $\eta_0$, as in the proof for the range-Doppler algorithm. $\square$

The scaling factor $a$ depends on $f$ but not on $R_0$, so one multiply per Doppler line serves every range; this is why no interpolation is needed. The model error is the use of $K_m$ at $r_{\text{ref}}$: for a target at $R_0 \ne r_{\text{ref}}$ the true rate differs, which leaves a small range defocus that grows with $|R_0 - r_{\text{ref}}|$ and with the Doppler frequency. The wide-beam example, with $K_m/K_r$ up to 1.25 at the edge of the band, still measures 1.05 of the ideal peak at the right pixel.

**Cost.** L1 and L8 cost $O(M N \log M)$, L4 and L6 cost $O(M N \log N)$ with an FFT, and the multiplies cost $O(M N)$. The total is $O(M N \log(M N))$ in the real-RAM model, with $O(M N)$ extra space.
