---
tag: YQ1113
kind: model
slug: bloch-equations
name: Bloch equations
aliases:
- Bloch equation
area: imaging-and-inverse-problems/mri-reconstruction
level: core
summary: The differential equations for the nuclear magnetization in a magnetic field, with precession and T1 and T2 relaxation. They predict the MR signal for a sample of independent spins.
history:
  year: 1946
  people: [Felix Bloch]
  note: Bloch wrote the equations of motion of the nuclear magnetization, with precession about the field and two relaxation times, in his paper on nuclear induction.
prereqs: [ode-initial-value-problem]
see_also: [mri-signal-equation, classical-runge-kutta-4, rodrigues-rotation-formula, matrix-exponential, picard-lindelof-theorem, mr-fingerprinting, k-space, mri-reconstruction-problem]
sources:
  - paper: doi:10.1103/PhysRev.70.460
    title: Felix Bloch, Nuclear induction, Physical Review 70(7-8), 1946, 460 to 474
    locator: the equations of motion of the macroscopic nuclear moment with the longitudinal and transverse relaxation times (general locator)
  - book: isbn:9780780347236
    title: Zhi-Pei Liang and Paul C. Lauterbur, Principles of Magnetic Resonance Imaging, A Signal Processing Perspective, IEEE Press, 2000
    locator: the chapter on signal generation and detection (the Bloch equation, the rotating frame, excitation and relaxation; chapter number not confirmed)
  - book: isbn:9780471351283
    title: E. Mark Haacke, Robert W. Brown, Michael R. Thompson and Ramesh Venkatesan, Magnetic Resonance Imaging, Physical Principles and Sequence Design, Wiley-Liss, 1999
    locator: the chapters on the classical response of the magnetization, rotating frame and relaxation (general locator)
---

The Bloch equations describe how the nuclear magnetization of a sample moves in a magnetic field. The magnetization turns about the field at the Larmor frequency, its transverse part decays with the time constant $T_2$, and its longitudinal part returns to equilibrium with the time constant $T_1$. Felix Bloch wrote them in 1946. In MRI they are the physics model: they say what signal each small region of the body gives after the radio frequency pulses and gradients of a scan. The [MRI signal equation](/mri-signal-equation/) follows from them when relaxation during the readout is ignored. They are a model of nature, not a law that always holds: they treat the spins as independent and the relaxation as single exponentials.

## The machine

**The state.** The magnetization $M(t) = (M_x, M_y, M_z)$ of a small volume, a vector in $\mathbb{R}^3$. The $z$ axis is along the main field $B_0$. The transverse part is written as the complex number $M_{xy} = M_x + i M_y$.

**The parameters.**

- The gyromagnetic ratio $\gamma$ of the nucleus. For the proton, $\bar\gamma = \gamma/(2\pi) = 42.577$ MHz/T.
- The field $B(t) = (B_{1x}(t), B_{1y}(t), B_0 + G(t) \cdot r + \Delta B(r))$: the main field $B_0$, the radio frequency field $B_1$ in the transverse plane, the gradient $G$ and the field error $\Delta B$.
- The relaxation times $T_1 \ge T_2 > 0$ and the equilibrium magnetization $M_0$, which is proportional to the proton density.

**The equations.** With $\omega(t) = \gamma B(t)$,

$$\frac{dM}{dt} = \gamma\, M \times B - \Bigl(\frac{M_x}{T_2}, \frac{M_y}{T_2}, \frac{M_z - M_0}{T_1}\Bigr).$$

The first term is precession, the second is relaxation. In the frame that turns with the radio frequency $\omega_{rf}$ about $z$, the same equation holds with $\omega$ replaced by $(\gamma B_{1x}, \gamma B_{1y}, \gamma B_z - \omega_{rf})$, where $B_1$ is now written in the turning frame. On resonance, the $z$ component is zero and a pulse is a pure rotation about the $B_1$ direction.

**Where it holds.** The equations describe the average moment of many spins that do not interact, in fields that change slowly compared with the Larmor period. They fit water protons in most tissues well.

**Where it fails.**

- Diffusion moves spins through the gradient; the Bloch-Torrey equation adds a diffusion term.
- Many tissues have more than one water compartment, so the decay is a sum of exponentials, not one.
- Exchange between pools (magnetization transfer, chemical exchange) needs coupled equations for each pool.
- Coupled spins (J coupling) and solids with very short $T_2$ need the quantum density matrix.
- In a voxel with an uneven field, the signal decays with $T_2^\ast < T_2$, which is not a property of the equation for one point but of the sum over the voxel.

**A numerical solution.** For a general pulse, the equation is solved numerically. The implementation uses the [classical Runge-Kutta method](/classical-runge-kutta-4/) with a fixed step $h$.

```pseudo id=main
BLOCH-RK4(M, omega(.), T1, T2, M0, h, K)
L1  f(t, v) = v x omega(t) - (v_x/T2, v_y/T2, (v_z - M0)/T1)
L2  for s = 0 .. K - 1 do
L3      t <- s h
L4      a <- f(t, M);  b <- f(t + h/2, M + (h/2) a)
L5      c <- f(t + h/2, M + (h/2) b);  d <- f(t + h, M + h c)
L6      M <- M + h (a + 2 b + 2 c + d) / 6
L7  return M
```

Each step costs four evaluations of $f$, so a run of $K$ steps costs $O(K)$ operations. For a piecewise constant field, the exact solution of each piece (a rotation followed by relaxation) is faster and has no step error; the closed forms below give it.

## What it counts

- **The Larmor frequency** $f_0 = \bar\gamma B_0$: 63.87 MHz at 1.5 T and 127.73 MHz at 3 T for the proton.
- **The free induction decay.** After a 90 degree pulse, $M_{xy}(t) = M_0\, e^{-i \omega_0 t} e^{-t/T_2}$, the signal that the coil picks up.
- **Recovery and inversion.** After an inversion pulse, $M_z(t) = M_0 (1 - 2 e^{-t/T_1})$. For $T_1 = 0.8$ s the signal is zero at $t = T_1 \ln 2 = 0.555$ s, which is how inversion recovery suppresses one tissue.
- **The signal of a pulse sequence.** For a spoiled gradient echo with flip angle $\alpha$ and repetition time $T_R$, the steady state signal is $M_0 \sin\alpha\, (1 - E_1) / (1 - E_1 \cos\alpha)$ with $E_1 = e^{-T_R/T_1}$. For $T_R = 10$ ms and $T_1 = 1$ s, it is $0.0707\, M_0$ at the best angle $8.09$ degrees, and $0.00995\, M_0$ at 90 degrees.
- **The image contrast.** $M_0$, $T_1$ and $T_2$ of each tissue, through such signal formulas, give the contrast of $T_1$ and $T_2$ weighted images. [MR fingerprinting](/mr-fingerprinting/) fits these parameters to simulated signals.

## Relation to other models

- **[MRI signal equation](/mri-signal-equation/).** If relaxation during the readout is ignored and the field is $B_0 + G(t) \cdot r$, the transverse magnetization at $r$ is $m(r)\, e^{-i \gamma B_0 t} e^{-2\pi i k(t) \cdot r}$ with $k(t) = \bar\gamma \int_0^t G$. Summed over the body after demodulation, this is the signal equation. A field error $\Delta B$ adds the phase $e^{-i \gamma \Delta B(r) t}$ used in [conjugate phase reconstruction](/conjugate-phase-reconstruction/).
- **Quantum mechanics.** For a spin 1/2 in a field, the expected value of the spin follows the precession term exactly. The relaxation terms are a phenomenological addition for an ensemble.
- **Bloch-Torrey.** Adds diffusion, $D \nabla^2 M$. It gives the signal loss used in diffusion imaging.
- **Bloch-McConnell.** Couples several pools with exchange rates.
- **Linear time-invariant pieces.** On an interval where $\omega$ is constant, the equation is $\dot M = L M + b$ with a constant matrix $L$, so its solution is a [matrix exponential](/matrix-exponential/). This gives the exact solvers used for long sequences.

## Known results in the model

**Existence and uniqueness.** For a field $\omega(t)$ that is continuous in pieces, the equation has exactly one solution for each start, because the right side is linear in $M$ (the [Picard-Lindelöf theorem](/picard-lindelof-theorem/)).

**Free precession (theorem).** For $\omega = (0, 0, \omega_0)$, $M_{xy}(t) = M_{xy}(0)\, e^{-i \omega_0 t} e^{-t/T_2}$ and $M_z(t) = M_0 + (M_z(0) - M_0) e^{-t/T_1}$. For $\gamma > 0$ the transverse part turns clockwise when seen from $+z$. The [proof](proofs/correctness.md) gives the details.

**Pulses are rotations (theorem).** Without relaxation and with a constant $\omega$, $M(t)$ is $M(0)$ turned by the angle $-|\omega| t$ about $\omega/|\omega|$, given by the [Rodrigues formula](/rodrigues-rotation-formula/). The length $|M|$ stays constant. On resonance, a pulse along $x$ with $\gamma B_1 \tau = \pi/2$ takes $(0, 0, 1)$ to $(0, 1, 0)$.

**Relaxation shrinks the transverse part (theorem).** With relaxation, $\frac{d}{dt}|M_{xy}|^2 = -2|M_{xy}|^2/T_2$ when $\omega$ is along $z$, and in general $\frac{d}{dt}|M - M_0 \hat z|^2 \le 0$ when there is no radio frequency field, so the equilibrium $(0, 0, M_0)$ attracts every solution.

*Proof.* With $\omega$ along $z$, the precession term is orthogonal to $M - M_0 \hat z$, because it is orthogonal to $M$ and has no $z$ component. The relaxation term gives $-2 (M_x^2 + M_y^2)/T_2 - 2 (M_z - M_0)^2 / T_1 \le 0$. $\square$

**The Ernst angle (theorem, under perfect spoiling).** If the transverse magnetization is fully destroyed before each pulse, the steady state $M_z$ just before a pulse is $M_0 (1 - E_1)/(1 - E_1 \cos\alpha)$. The signal $M_0 \sin\alpha (1 - E_1)/(1 - E_1 \cos\alpha)$ is largest for $\cos\alpha = E_1$.

*Proof.* Let $z$ be the steady value before a pulse. The pulse leaves $z \cos\alpha$, and free recovery over $T_R$ gives $M_0 + (z\cos\alpha - M_0) E_1$, which must equal $z$. Solving gives the formula. The derivative of $\sin\alpha / (1 - E_1 \cos\alpha)$ in $\alpha$ has the numerator $\cos\alpha (1 - E_1\cos\alpha) - E_1 \sin^2\alpha = \cos\alpha - E_1$, which changes sign from positive to negative at $\cos\alpha = E_1$. $\square$

**Accuracy of the integrator (measurement).** With $h = 10^{-4}$ s over 0.05 s of free precession, the RK4 solution agreed with the closed form within $10^{-7}$; with $h = 10^{-6}$ s, the 90 degree pulse agreed within $10^{-10}$.

## References
