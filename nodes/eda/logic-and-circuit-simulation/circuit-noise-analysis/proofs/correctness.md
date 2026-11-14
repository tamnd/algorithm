---
title: One adjoint solve gives the output noise of every uncorrelated source
proves: [correctness]
status: full
---

We use the notation of the page. The small-signal circuit at the operating point $x_0$ has the real matrices $G$ and $C$, and at the frequency $f$, with $\omega = 2\pi f$, its complex MNA matrix is $Y = G + j\omega C$, assumed nonsingular. Noise source $k$ is a current $i_k$ that leaves node $p_k$ and enters node $q_k$ (node 0 is ground). Its one-sided power spectral density is $S_k(f)$. The output is $v = \ell^{\mathsf T} x$. The algorithm solves $Y^{\mathsf T} z = \ell$ and returns

$$S_{\mathrm{out}}(f) = \sum_k |z_{q_k} - z_{p_k}|^2\, S_k(f),$$

with $z_0 = 0$.

**Lemma 1 (the injection vector).** A current $I$ that leaves node $p$ and enters node $q$ adds $I\, a_k$ to the right side of the MNA equations, where $a_k = \mathbf e_{q} - \mathbf e_{p}$ (with $\mathbf e_0 = 0$).

*Proof.* The node rows of MNA are KCL in the form "the sum of the currents that leave the node through the elements equals the current that the sources put into it". The source puts $I$ into node $q$ and takes $I$ from node $p$, so it adds $+I$ to row $q$ and $-I$ to row $p$. It adds no element current and no branch row. $\square$

**Lemma 2 (the transfer of each source).** The transfer function from $i_k$ to the output is $H_k = \ell^{\mathsf T} Y^{-1} a_k = z_{q_k} - z_{p_k}$.

*Proof.* With only source $k$ active at the phasor $I$, the small-signal circuit is $Y X = I a_k$ by Lemma 1, so the output phasor is $\ell^{\mathsf T} Y^{-1} a_k I$, and $H_k = \ell^{\mathsf T} Y^{-1} a_k$. Since $z = Y^{-\mathsf T} \ell$ (the transpose, not the conjugate transpose),

$$\ell^{\mathsf T} Y^{-1} a_k = (Y^{-\mathsf T} \ell)^{\mathsf T} a_k = z^{\mathsf T} a_k = z_{q_k} - z_{p_k}. \qquad \square$$

So one solve with $Y^{\mathsf T}$ gives every $H_k$, and the cost of each is one subtraction. This is the identity $(A^{-1})^{\mathsf T} = (A^{\mathsf T})^{-1}$ and nothing more. In circuit terms $Y^{\mathsf T}$ is the matrix of the adjoint network, which turns every controlled source around, and $z$ is the response of the adjoint network to a unit source at the output (see the adjoint sensitivity page and Tellegen's theorem); the proof above does not need that reading.

**Lemma 3 (the sum of uncorrelated sources).** Let $n_1, \ldots, n_K$ be zero-mean, jointly wide-sense stationary processes, mutually uncorrelated, $E[n_k(t) n_l(s)] = 0$ for $k \ne l$, with spectral densities $S_k$. Let $y = \sum_k h_k * n_k$ for stable real impulse responses $h_k$ with frequency responses $H_k$. Then $S_y = \sum_k |H_k|^2 S_k$.

*Proof.* The autocorrelation of $y$ is

$$R_y(\tau) = E[y(t+\tau) y(t)] = \sum_{k,l} \iint h_k(a) h_l(b)\, E[n_k(t+\tau-a)\, n_l(t-b)]\, da\, db.$$

The terms with $k \ne l$ vanish because the sources are uncorrelated. The term with $k = l$ is the autocorrelation of $h_k * n_k$, so $R_y = \sum_k R_{h_k * n_k}$. The spectral density is the Fourier transform of the autocorrelation (the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/)), which is linear, so $S_y = \sum_k S_{h_k * n_k}$. Each term is $|H_k|^2 S_k$ by the filter rule of the [power spectral density](/power-spectral-density/), which we cite. $\square$

The rule holds for one-sided densities as well as for two-sided ones, since both sides of the identity are even in $f$ and the one-sided density is twice the two-sided one at $f > 0$.

**Theorem (correctness).** If the noise sources are mutually uncorrelated, the value $S_{\mathrm{out}}(f)$ that the algorithm returns is the spectral density of the output noise of the small-signal circuit, and the share of source $k$ is $|H_k|^2 S_k(f)$.

*Proof.* The small-signal circuit is linear and time invariant, so the output noise is $\sum_k h_k * i_k$, where $h_k$ is the impulse response whose transform is the transfer $H_k$ of Lemma 2. Lemma 3 gives the sum, and Lemma 2 shows that the algorithm computes each $|H_k|^2$ exactly as $|z_{q_k} - z_{p_k}|^2$. $\square$

**What is not proved.** Three steps are models, and the proof does not cover them.

1. The source densities. $4kT/R$ for a resistor is Nyquist's result, $2qI$ for a junction is the shot-noise formula, $4kT \cdot \frac23 g_m$ for a long-channel MOSFET in saturation and $K_F I_D^{A_F}/(f\, C_{\mathrm{ox}} L_{\mathrm{eff}}^2)$ for its flicker noise are device-model formulas with fitted $K_F$ and $A_F$. They are cited on the page.
2. The linearization. The noise is small, so the circuit is replaced by its small-signal model at $x_0$, as in AC analysis. Noise that moves the operating point, or mixes with a large signal, is outside this model.
3. Independence. Sources in different devices are uncorrelated by the physics of the model. Correlated sources, such as the induced gate noise and the channel noise of one transistor, need the cross spectrum, and the sum of Lemma 3 then gains the terms $2 \operatorname{Re}(H_k \overline{H_l} S_{kl})$.

**The kT/C result.** For a resistor $R$ from a grounded source to a node with a capacitor $C$ to ground, $H = R/(1 + j\omega RC)$ for the resistor current injected into the node, so

$$\int_0^\infty \frac{4kT}{R} \cdot \frac{R^2}{1 + (2\pi f R C)^2}\, df = 4kTR \cdot \frac{1}{2\pi R C} \cdot \frac{\pi}{2} = \frac{kT}{C},$$

with the substitution $2\pi f R C = \tan\theta$. The total does not depend on $R$. The test on the page computes the integral from the densities that the algorithm returns.
