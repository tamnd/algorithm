---
title: The Mth-power loop removes M-PSK data, locks to the carrier phase modulo 2 pi/M, and has the variance (B_L T/M^2) sum C(M,n)^2 n! N0^n in the linear model
proves: [correctness]
status: full
---

The input is $r_k = a_k e^{j\theta_k} + w_k$, where $a_k = e^{j(\phi_c + 2\pi m_k/M)}$ is an M-PSK symbol with unknown index $m_k$, $\phi_c$ is the known phase of the constellation (the argument `phase0`), $E_s = 1$, and $w_k \sim \mathcal{CN}(0, N_0)$ are independent, with $\mathrm{SNR} = 1/N_0$. The loop of lines L5 to L7 is the second-order [phase-locked loop](/phase-locked-loop/) acting on $\psi$, and line L3 outputs $\psi/M$. We use the PLL proof for the linear closed loop $H(z)$, the stability conditions and the noise bandwidth $B_L T = \frac12 \sum h_k^2$.

**Lemma 1 (the power removes the data).** Without noise, $y_k = r_k^M e^{-jM\phi_c} = e^{jM\theta_k}$ for every $m_k$.

*Proof.* $a_k^M = e^{jM\phi_c} e^{j2\pi m_k} = e^{jM\phi_c}$. $\square$

So line L5 outputs $\sin(M\theta_k - \psi_k)$, and the PLL proof applies to $\psi$ with the input phase $M\theta_k$ and detector gain $1$.

**Theorem 1 (lock and ambiguity).** With gains that satisfy the PLL stability conditions and no noise, the estimate $\psi_k/M$ tends to $\theta$ modulo $2\pi/M$ for a constant $\theta$, and the phase error tends to zero modulo $2\pi/M$ for a frequency step $\theta_k = \theta_0 + \omega k$ in the linear model.

*Proof.* The stable lock points of a PLL with the detector $\sin(M\theta - \psi)$ are $\psi \in M\theta + 2\pi\mathbb{Z}$. Dividing by $M$ gives $\theta + \frac{2\pi}{M}\mathbb{Z}$. A frequency step $\omega$ on $\theta$ is a frequency step $M\omega$ on $M\theta$, which the PLL tracks with zero steady-state error. $\square$

The ambiguity is a property of the input, not of the loop: the sequences $(\theta, a_k)$ and $(\theta + 2\pi/M, a_k e^{-j2\pi/M})$ give the same $r_k$, and $a_k e^{-j2\pi/M}$ is again an M-PSK symbol.

**Lemma 2 (the noise after the power).** At $\theta$ fixed, $y_k = e^{jM\theta} + v_k$ with

$$v_k = e^{-jM\phi_c} \sum_{n=1}^{M} \binom{M}{n} (a_k e^{j\theta})^{M-n} w_k^n, \qquad E[v_k] = 0, \qquad E|v_k|^2 = \sum_{n=1}^{M} \binom{M}{n}^2 n!\, N_0^n,$$

and $v_k$ is circular, so its component along any fixed direction has half this variance. The $v_k$ are independent over $k$.

*Proof.* The binomial theorem gives the sum. For circular complex Gaussian $w$, $E[w^n \overline{w^m}] = 0$ for $n \ne m$ and $E|w|^{2n} = n!\, N_0^n$, since $|w|^2$ is exponential with mean $N_0$. The terms of the sum are therefore uncorrelated, and $|a_k| = 1$. Each $w^n$ is circular, because a rotation of $w$ by $\beta$ rotates $w^n$ by $n\beta$ and leaves its law unchanged, so $v_k$ is circular. Independence over $k$ follows from the independence of the $w_k$ and the $a_k$. $\square$

**Theorem 2 (variance in the linear model).** At lock, in the linear model, the carrier phase error $\theta - \psi_k/M$ has variance

$$\sigma_\phi^2 = \frac{B_L T}{M^2} \sum_{n=1}^{M} \binom{M}{n}^2 n!\, N_0^n.$$

For $M = 2$ this is $B_L T\, N_0 (1 + N_0/2)$, and for $M = 4$ it is $B_L T\, N_0 (1 + 4.5 N_0 + 6 N_0^2 + 1.5 N_0^3)$.

*Proof.* Near lock, line L5 outputs $\sin(M\theta - \psi) + \operatorname{Im}(v_k e^{-j\psi_k})$. By Lemma 2 and the independence of $v_k$ from the past, the noise term is white with variance $\frac12 E|v_k|^2$. The PLL proof gives the variance of $\psi$ as $\frac12 E|v_k|^2 \cdot 2B_L T$, and dividing $\psi$ by $M$ divides the variance by $M^2$. For $M = 2$: $(4 N_0 + 2 N_0^2)/4$. For $M = 4$: $(16 N_0 + 72 N_0^2 + 96 N_0^3 + 24 N_0^4)/16$. $\square$

The ratio of $\sigma_\phi^2$ to $B_L T\, N_0$, the variance of a loop that knows the data, is the *squaring loss*. It is $1 + N_0/2$ for $M = 2$ and grows with $M$, because the power $M$ multiplies noise terms with each other.

**Lemma 3 (M = 2 is the BPSK Costas loop).** For $M = 2$ and $\phi_c = 0$, $\psi_k/2$ equals the phase of the BPSK Costas loop with the same $K_p$ and $K_i$ at every step.

*Proof.* With $\phi = \psi/2$ and $z = r e^{-j\phi}$, line L5 is $\operatorname{Im}(r^2 e^{-j\psi}) = \operatorname{Im}(z^2) = 2IQ$. Write the Costas loop as $\phi \leftarrow \phi + K_p (IQ) + s$, $s \leftarrow s + K_i (IQ)$, and multiply by 2: it is lines L6 and L7 with $\psi = 2\phi$ and the integrator $2s$. $\square$

The tests check Lemma 3 sample by sample, Theorem 1 for $M = 2$, $4$ and $8$, and Theorem 2 by simulation at 10 dB and 6 dB within a factor of 1.25.
