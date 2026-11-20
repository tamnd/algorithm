---
title: The Costas detector removes BPSK and QPSK data, the loop locks modulo pi or pi/2, and its BPSK variance has the squaring loss 1 + 1/(2 SNR)
proves: [correctness]
status: full
---

The input is $r_k = a_k e^{j\theta} + w_k$ with data $a_k$ from BPSK ($\pm1$) or QPSK ($e^{j(\pi/4 + m\pi/2)}$), $E_s = E|a_k|^2 = 1$, and $w_k \sim \mathcal{CN}(0, N_0)$ white, with $\mathrm{SNR} = 1/N_0$. Line L4 forms $z_k = r_k e^{-j\phi_k}$, with arms $I = \operatorname{Re} z_k$ and $Q = \operatorname{Im} z_k$. Lines L6 and L7 are the loop filter and the oscillator of the [phase-locked loop](/phase-locked-loop/), whose proof gives the linear closed loop, the Jury conditions and the noise bandwidth $B_L T = \frac12 \sum h_k^2$. Write $\Delta = \theta - \phi$ for the phase error.

**Lemma 1 (BPSK detector).** Without noise, $e = IQ = \frac12 \sin 2\Delta$ for both values of $a_k$. Also $IQ = \frac12 \operatorname{Im}(z^2)$ for every $z$.

*Proof.* $z = a e^{j\Delta}$ with $a = \pm1$, so $I = a\cos\Delta$, $Q = a\sin\Delta$ and $IQ = a^2 \sin\Delta\cos\Delta = \frac12 \sin 2\Delta$. For any $z = I + jQ$, $z^2 = I^2 - Q^2 + 2jIQ$. $\square$

**Lemma 2 (QPSK detector).** Let $e(z) = \operatorname{sgn}(I)\,Q - \operatorname{sgn}(Q)\,I$. Then $e(jz) = e(z)$, and without noise $e = \sqrt2 \sin\Delta$ for $|\Delta| < \pi/4$, for each of the four symbols. So the S-curve has period $\pi/2$.

*Proof.* $jz = -Q + jI$, so $e(jz) = \operatorname{sgn}(-Q)\,I - \operatorname{sgn}(I)(-Q) = e(z)$, using $\operatorname{sgn}(-x) = -\operatorname{sgn}(x)$ for $x \ne 0$. The four symbols are $j^m e^{j\pi/4}$, so it suffices to take $a = e^{j\pi/4}$. Then $z = e^{j(\pi/4 + \Delta)}$, and for $|\Delta| < \pi/4$ both arms are positive: $e = \sin(\pi/4 + \Delta) - \cos(\pi/4 + \Delta) = \sqrt2 \sin\Delta$. $\square$

**Lemma 3 (BPSK Costas loop is a PLL on the squared signal).** Let $\psi_k = 2\phi_k$ and $S_k = 2 s_k$. Then $\psi_{k+1} = \psi_k + K_p E_k + S_k$ and $S_k = S_{k-1} + K_i E_k$, with $E_k = \operatorname{Im}(r_k^2 e^{-j\psi_k})$.

*Proof.* By Lemma 1, $2e_k = \operatorname{Im}(z_k^2) = \operatorname{Im}(r_k^2 e^{-j2\phi_k}) = E_k$. Multiply lines L6 and L7 by 2. $\square$

So the BPSK Costas loop and the [squaring loop](/squaring-loop/) with $M = 2$ and the same gains give the same phase, exactly. The tests check this sample by sample.

**Theorem 1 (lock points and ambiguity).** Assume the gains satisfy the conditions of the PLL with $K_d K_p$ and $K_d K_i$, where $K_d = 1$ for BPSK and $K_d = \sqrt2$ for QPSK. Without noise, the stable equilibria of the error are $\Delta \in \pi\mathbb{Z}$ for BPSK and $\Delta \in \frac{\pi}{2}\mathbb{Z}$ for QPSK. Near each of them the linear model of the PLL holds with the detector gain $K_d$, and the loop follows a phase step and a frequency step with zero steady-state error modulo the ambiguity.

*Proof.* By Lemmas 1 and 2, the detector output without noise depends only on $\Delta$, not on the data. The zeros of $\frac12 \sin 2\Delta$ are $\Delta \in \frac{\pi}{2}\mathbb{Z}$, and the slope $\cos 2\Delta$ is $+1$ at $\Delta \in \pi\mathbb{Z}$ and $-1$ at the odd multiples of $\pi/2$, which are unstable. For QPSK, the S-curve is $\sqrt2\sin\Delta$ on $(-\pi/4, \pi/4)$ with slope $\sqrt2$ at $0$, and it jumps from $+1$ to $-1$ at $\Delta = \pi/4$, so it drives the error away from $\pm\pi/4$ and toward the nearest multiple of $\pi/2$. Near a stable point, the loop is the PLL with detector gain $K_d$, and the PLL proof gives the rest. $\square$

The ambiguity cannot be removed by any detector that does not know the data. For BPSK, the received sequence for $(\theta, a)$ and for $(\theta + \pi, -a)$ is the same, so no function of $r$ alone can tell $\theta$ from $\theta + \pi$. For QPSK the same holds for $(\theta + \pi/2, -ja)$.

**Theorem 2 (BPSK variance with the squaring loss).** For BPSK in the linear model, the phase error variance is

$$\sigma_\phi^2 = \frac{B_L T}{\mathrm{SNR}}\left(1 + \frac{1}{2\,\mathrm{SNR}}\right).$$

*Proof.* At lock, $z_k = a_k e^{j\Delta} + n_k$ with $n_k = n_I + j n_Q \sim \mathcal{CN}(0, N_0)$, independent of the past by the rotation invariance used in the PLL proof. For small $\Delta$, $I = a_k + n_I$ and $Q = a_k \Delta + n_Q$ to first order, so

$$e_k = \Delta(1 + a_k n_I) + a_k n_Q + n_I n_Q.$$

The mean slope is $1$. The noise term $v_k = a_k n_Q + n_I n_Q$ has mean $0$ and variance $E[n_Q^2] + E[n_I^2] E[n_Q^2] = \frac{N_0}{2} + \frac{N_0^2}{4}$, and the $v_k$ are uncorrelated. The PLL proof gives the variance $\sigma_v^2 \cdot 2 B_L T = N_0 B_L T (1 + N_0/2)$. With $N_0 = 1/\mathrm{SNR}$ this is the formula. $\square$

The factor $1 + 1/(2\,\mathrm{SNR})$ is the *squaring loss*: the noise times noise term $n_I n_Q$. For QPSK with correct signs of $I$ and $Q$, the same expansion gives $e_k = \sqrt2\Delta + v_k$ with $\operatorname{Var} v_k = N_0$, so $\sigma_\phi^2 = N_0 \cdot 2B_L T/2 = B_L T/\mathrm{SNR}$; wrong signs add a small extra error at low SNR. The tests compare both values with a simulation at 10 dB within a factor of 1.25.
