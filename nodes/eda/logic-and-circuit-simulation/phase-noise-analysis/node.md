---
tag: Y2MTGG
kind: algorithm
slug: phase-noise-analysis
name: Oscillator phase noise analysis
aliases:
- Demir-Mehrotra-Roychowdhury phase noise
- perturbation projection vector method
area: eda/logic-and-circuit-simulation
level: research
summary: Demir, Mehrotra and Roychowdhury's nonlinear analysis that projects noise on the oscillator's perturbation projection vector to get its phase diffusion and Lorentzian spectrum.
model: real-ram
complexity:
  vars: {n: the number of state variables, S: the number of time steps per period, I: the number of Newton iterations for the orbit, p: the number of noise sources}
  time: {worst: "O(I S n^3 + S n p)"}
  space: {extra: "O(S n^2)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 2000
  people: [Alper Demir, Amit Mehrotra, Jaijeet Roychowdhury]
  note: Demir, Mehrotra and Roychowdhury showed that white noise makes the phase of a nonlinear oscillator diffuse as a random walk whose rate is set by the perturbation projection vector, and that the spectrum of each harmonic is a Lorentzian.
prereqs: [shooting-newton-steady-state, limit-cycle, stochastic-differential-equation, circuit-noise-analysis]
see_also: [harmonic-balance-analysis, power-spectral-density, eigenvalue-problem, adjoint-sensitivity-analysis, classical-runge-kutta-4, heuns-method, euler-maruyama-method, transient-circuit-analysis]
sources:
  - paper: doi:10.1109/81.847872
    title: Alper Demir, Amit Mehrotra and Jaijeet Roychowdhury, Phase noise in oscillators, a unifying theory and numerical methods for characterization, IEEE Transactions on Circuits and Systems I, Fundamental Theory and Applications 47(5), 655 to 674, 2000
    locator: the split of the noisy solution into a phase shift and an orbital deviation, the perturbation projection vector as the Floquet left eigenvector, the diffusion constant c, the Lorentzian spectrum of the harmonics, and the numerical methods in the time and frequency domains
  - paper: "Ali Hajimiri and Thomas H. Lee, A general theory of phase noise in electrical oscillators, IEEE Journal of Solid-State Circuits 33(2), 179 to 194, 1998"
    title: Ali Hajimiri and Thomas H. Lee, A general theory of phase noise in electrical oscillators, IEEE Journal of Solid-State Circuits, 1998
    locator: the linear time-varying model of phase noise with the impulse sensitivity function
---

Oscillator phase noise analysis computes how noise in an oscillator's devices spreads its output spectrum around the carrier. Demir, Mehrotra and Roychowdhury (2000) showed that the noise makes the oscillator's phase drift as a random walk, with a rate $c$ fixed by the *perturbation projection vector* (PPV), the periodic adjoint solution that measures how much a kick at each instant shifts the phase for good. This page belongs to the circuit simulation half of the logic and circuit simulation sub-area; the method takes the periodic orbit from [shooting](/shooting-newton-steady-state/) or [harmonic balance](/harmonic-balance-analysis/) and returns $c$ and the spectrum $\mathcal L(f_m)$.

## In plain words

An oscillator has no clock to follow: it keeps its own time. When noise pushes it, the size of the swing recovers, but a shift in its timing does not, because nothing pulls it back. The small shifts add up, so the timing wanders more and more.

The analysis first finds the noiseless repeating waveform. Then it computes, for every instant of the cycle and every node, how much a small push at that instant would shift the timing for good. A push at the peak of a swing often does nothing to the timing, while a push at a zero crossing does a lot. The noise at each instant is weighted by this sensitivity and averaged over the cycle. The result is one number, the rate at which the timing wanders, and from it follow the jitter and the shape of the spectrum near the carrier.

## The problem

The oscillator is a state equation $\dot x = F(x) + B\,\xi(t)$ with $n$ states, a Jacobian $A(x) = \partial F/\partial x$ and $p$ independent white noise sources $\xi$ of unit two-sided density, $\mathbb E\,\xi(t)\xi(s)^{\mathsf T} = I\,\delta(t - s)$. A circuit in [modified nodal analysis](/modified-nodal-analysis/) form $f(x) + \frac{d}{dt}q(x) = b\,\xi$ with a nonsingular capacitance matrix gives this form; with algebraic unknowns the same method works on the differential-algebraic equation with more care. The noise columns of $B$ come from the device noise models of [circuit noise analysis](/circuit-noise-analysis/), for example $\sqrt{2kT/R}$ for the thermal current of a resistor $R$ as a two-sided density.

Without noise the oscillator has a stable periodic orbit $x_s(t)$ with an unknown period $T$, a [limit cycle](/limit-cycle/). The *PPV* is the periodic solution $v(t)$ of the adjoint equation $\dot v = -A(x_s(t))^{\mathsf T} v$ with $v(t)^{\mathsf T}\dot x_s(t) = 1$. The output is the diffusion constant

$$c = \frac1T\int_0^T v(t)^{\mathsf T} B B^{\mathsf T} v(t)\,dt,$$

in seconds, and the single-sideband phase noise of the first harmonic at offset $f_m$ from $f_0 = 1/T$,

$$\mathcal L(f_m) = 10\log_{10}\frac{f_0^2 c}{\pi^2 f_0^4 c^2 + f_m^2}\ \text{dBc/Hz}.$$

Demir, Mehrotra and Roychowdhury proved that the noisy solution stays close to $x_s(t + \alpha(t))$, where the phase shift $\alpha(t)$ is asymptotically a Wiener process with $\operatorname{Var}\alpha(t) = ct$; the timing jitter after a time $t$ has the standard deviation $\sqrt{ct}$. This is a model of a [stochastic differential equation](/stochastic-differential-equation/), and its spectrum is the [power spectral density](/power-spectral-density/) of the shifted waveform.

The device equations contain fitted parameters. In the example, the negative conductance of a cross-coupled transistor pair is modeled as $g_m v_0\tanh(v/v_0)$; $g_m$ and $v_0$ are fitted to the transistors. The noise of the tank resistor is the physical thermal noise; the noise models of real transistors also contain fitted coefficients.

## The algorithm

```pseudo id=main
PHASE-NOISE(F, A, B, x₀, T₀, S, offsets)
L1  (x_s, T) ← periodic orbit by shooting Newton with T unknown and a phase condition; P_k ← step Jacobians
L2  M ← P_{S−1} ⋯ P_1 P_0
L3  v_S ← left eigenvector of M for the eigenvalue 1, scaled so that v_Sᵀ F(x_0) = 1
L4  for k = S − 1 down to 0: v_k ← P_kᵀ v_{k+1}
L5  c ← (1/S) Σ_{k<S} |Bᵀ v_k|²
L6  for each offset f_m: 𝓛(f_m) ← 10 log₁₀ (f₀² c / (π² f₀⁴ c² + f_m²)), with f₀ = 1/T
L7  return x_s, T, v, c and 𝓛
```

Line L1 is [shooting Newton](/shooting-newton-steady-state/) for an autonomous circuit. The unknowns are the start state and $T$; the extra equation fixes one state at $t = 0$ (the phase condition), and the extra column of the Newton matrix is $\partial x_S/\partial T = F(x_S)$. The implementation uses $S$ steps of the [classical Runge-Kutta method](/classical-runge-kutta-4/) and forms the exact Jacobian $P_k$ of each step. A circuit simulator would use the step matrices of its implicit integration instead, or a harmonic balance solution.

Lines L2 to L4 compute the PPV. The monodromy matrix $M$ carries a small change of the state at $t = 0$ to its change one period later. Its eigenvalue 1 belongs to the direction along the orbit, $F(x_0)$; the other eigenvalues of a stable orbit have magnitude below 1. Line L3 is a small [eigenvalue problem](/eigenvalue-problem/): the implementation solves the bordered system $(M^{\mathsf T} - I)v_S + \mu F(x_0) = 0$, $F(x_0)^{\mathsf T}v_S = 1$, where $\mu$ absorbs the step error by which the eigenvalue of the discrete $M$ differs from 1. Line L4 runs the transposed steps backward, which is the discrete adjoint equation, as in [adjoint sensitivity analysis](/adjoint-sensitivity-analysis/). Line L5 averages the projected noise over the period, and line L6 evaluates the Lorentzian.

## Example

**The Hopf oscillator, by hand.** Take $F(a, b) = (\mu a - \omega b - r^2 a,\ \omega a + \mu b - r^2 b)$ with $r^2 = a^2 + b^2$, and noise $\sigma$ on both states. The orbit is the circle of radius $\sqrt\mu$, traversed at the angular frequency $\omega$. A radial kick decays and leaves the angle as it was, while a tangential kick of length $\delta$ shifts the angle by $\delta/\sqrt\mu$ for good, a time shift of $\delta/(\omega\sqrt\mu)$. So $v(t) = (-\sin\omega t, \cos\omega t)/(\omega\sqrt\mu)$ and $c = \sigma^2/(\mu\omega^2)$. For $\mu = 1$, $\omega = 2\pi$ and $\sigma = 0.1$, $c = 0.01/(4\pi^2) = 2.533 \times 10^{-4}$ s, and $\mathcal L(1\text{ Hz}) = 10\log_{10}(2.533 \times 10^{-4}) = -36.0$ dBc/Hz, because $\pi^2 c^2$ is negligible next to $f_m^2$. The implementation with $S = 200$ steps gave $T = 1.0000000081$ s and $c = 2.533029547 \times 10^{-4}$ s, a relative error of $1.7 \times 10^{-8}$, and $v_k^{\mathsf T}F(x_k) = 1$ to $1.7 \times 10^{-15}$.

**An LC oscillator, measured.** A tank of $L = 1$ µH and $C = 1$ nF with a loss of $R = 200$ Ω is driven by the negative conductance $i = g_m v_0\tanh(v/v_0)$, with the fitted values $g_m = 25$ mS and $v_0 = 0.1$ V; the states are the tank voltage and the inductor current, and the only noise is the thermal noise of $R$ at 300 K. The phase condition sets the inductor current to zero at $t = 0$. Starting from $v = 0.3$ V and $T_0 = 2\pi\sqrt{LC}$, line L1 converged in 5 Newton iterations with $S = 400$ to $f_0 = 5.0238$ MHz (the tank resonance is 5.0329 MHz) and a peak of 0.6298 V. The Floquet multipliers of $M$ were 1 and 0.6145. The results were:

| quantity | value |
|---|---|
| $c$ | $5.2719 \times 10^{-20}$ s |
| $\mathcal L(10\text{ kHz})$ | $-138.76$ dBc/Hz |
| $\mathcal L(100\text{ kHz})$ | $-158.76$ dBc/Hz |
| $\mathcal L(1\text{ MHz})$ | $-178.76$ dBc/Hz |
| corner $\pi f_0^2 c$ of the Lorentzian | $4.2 \times 10^{-6}$ Hz |
| largest $\lvert v_k^{\mathsf T}F(x_k) - 1\rvert$ | $1.9 \times 10^{-8}$ |

The spectrum falls by 20 dB per decade because every practical offset is far above the corner. With $S = 100$, 200, 400 and 800, $c$ was $5.271906$, $5.2719074$, $5.2719075$ and $5.27190754 \times 10^{-20}$ s. For a nearly sinusoidal swing of amplitude $A$ at $\omega_0 = 2\pi f_0$, the voltage component of the PPV is about $-\sin(\omega_0 t)/(A\omega_0)$, which gives the estimate $c \approx kT/(RC^2A^2\omega_0^2)$. With the measured first-harmonic amplitude $A = 0.6297$ V, the estimate is $5.242 \times 10^{-20}$ s, 0.6% below the PPV result; the difference comes from the distortion of the waveform. The analysis took 0.04 s of Python process time on one machine.

**Two checks against simulation.** First, a kick of $10^{-6}$ V to the voltage or $10^{-9}$ A to the current at a sample $x_k$, followed by 20 periods without noise, moved the settled orbit by a time shift that agreed with $v_k$ to a relative error between $4.5 \times 10^{-9}$ and $5.9 \times 10^{-5}$ at four (sample, state) pairs, measured by central differences. Second, Monte Carlo runs of the noisy equation with the stochastic Heun method:

| oscillator | runs | measured $\operatorname{Var}\alpha / (ct)$ |
|---|---|---|
| Hopf, $h = 0.02$, $t = 10$ s, 600 paths, phase from the unwrapped angle | seeds 71, 72, 73 | 0.998, 1.061, 1.039 |
| LC, noise scaled by $1.3 \times 10^4$, 50 steps per period, 40 periods, 400 paths, phase from the last up-crossing | seed 5 | 0.954 |
| LC, the same, 100 steps per period, 30 periods, 300 paths | seeds 6, 7 | 1.039, 1.086 |

The standard error of a sample variance of $P$ Gaussian values is $\sqrt{2/(P - 1)}$ of it, 0.06 for 600 paths and 0.07 to 0.08 for 300 to 400, so the runs agree with $c$ within their statistics. The noise of the LC runs was scaled up so that the phase spread is visible after 40 periods; $c$ scales with it.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **The PPV exists and is unique.** If the eigenvalue 1 of $M$ is simple, the left eigenvector with $v^{\mathsf T}\dot x_s(0) = 1$, carried by the adjoint equation, is periodic, and $v(t)^{\mathsf T}\dot x_s(t) = 1$ for all $t$.
2. **The backward recurrence is the discrete adjoint.** $v_k^{\mathsf T}y_k$ is the same for all $k$ along every solution of the linearized step map, so $v_k^{\mathsf T}d$ is the part of a kick $d$ at step $k$ that survives to the end of the period.
3. **The linearized phase is a random walk.** For $dy = A(t)y\,dt + B\,dW$, the projection $\alpha = v^{\mathsf T}y$ satisfies $d\alpha = v^{\mathsf T}B\,dW$, so it is Gaussian with $\operatorname{Var}\alpha(t) = ct$ plus a bounded periodic term.
4. **Exact Hopf result.** $c = \sigma^2/(\mu\omega^2)$.
5. **The Lorentzian.** If $\alpha$ is a Wiener process with variance $ct$, the first harmonic has the spectrum in $\mathcal L$, with total power 1.

The extension from the linearized equation to the nonlinear oscillator is the theorem of Demir, Mehrotra and Roychowdhury and is cited, not proved; the Monte Carlo runs measure it. The error of the discrete PPV is measured.

The tests check, with fixed seeds, that $c$ for the Hopf oscillator equals $\sigma^2/(\mu\omega^2)$ to a relative $10^{-7}$; that the PPV of the LC oscillator is periodic and normalized; the kick test at four (sample, state) pairs to a relative $10^{-3}$; the sinusoidal estimate to 2%; that $\mathcal L$ falls by 20 dB per decade; that the Lorentzian integrates to 1, by quadrature, to $10^{-9}$; and the Hopf (seed 71) and LC (seed 5) Monte Carlo ratios within 0.25 and 0.3 of 1. The whole file takes about 4.5 s of CPU time.

## Complexity

Line L1 costs $I$ shooting iterations of $S$ steps, each with $O(n^3)$ work for the step Jacobian and its product into the monodromy matrix, so $O(ISn^3)$ time. The PPV costs one more product of $S$ matrices, $O(Sn^3)$, one $(n+1) \times (n+1)$ solve, and $S$ transposed products of $O(n^2)$ each. Line L5 costs $O(Snp)$. The step Jacobians take $O(Sn^2)$ space. For large circuits, simulators keep the sparse factors of the steps instead of dense $P_k$, find the left eigenvector with an iterative solver, and apply $P_k^{\mathsf T}$ as one transposed sparse solve per step.

## Properties

- **One number per oscillator.** All white noise sources reduce to the scalar $c$, and $\mathcal L(f_m)$, the jitter $\sqrt{ct}$ and the spectra of all harmonics follow from it.
- **Finite power.** Unlike a linear time-invariant noise analysis, which gives a density that grows without bound as $f_m \to 0$, the Lorentzian has a finite peak $1/(\pi^2 f_0^2 c)$ and total power 1: phase noise moves power, it does not add it.
- **Nonlinear.** The orbit, the PPV and the noise all come from the large-signal waveform, so amplitude limiting and the shape of the waveform are included.
- **Cyclostationary noise.** A noise source whose strength depends on the waveform enters as a time-varying column of $B$ in line L5 with no other change.
- **Exact for the model.** For a given orbit and PPV the result is exact; the error comes from the discretization of the orbit, which is small, as the table over $S$ shows.

## Variants and improvements

- **Frequency-domain PPV.** Demir, Mehrotra and Roychowdhury also compute $v$ from the harmonic balance Jacobian, as the null vector of its transpose.
- **Implicit integration.** With the step matrices of a circuit simulator, $P_k = (C_{k+1} + \theta hG_{k+1})^{-1}(C_k - (1 - \theta)hG_k)$ as in shooting, and line L4 uses the transposed factors.
- **Linear time-varying model.** Hajimiri and Lee (1998) model phase noise with an impulse sensitivity function, the response of the phase to a charge kick at each instant, which plays the role of the PPV. Their model is linear in the phase, so it gives the $1/f_m^2$ region but not the finite Lorentzian peak.
- **Colored noise.** Flicker noise needs a separate treatment, because the phase is no longer a Wiener process; the white-noise result of this page covers the $1/f_m^2$ region.
- **Injection locking and coupled oscillators.** The same PPV gives the phase response to a small periodic input, which models locking range and oscillator coupling.

## When to use it

Use the PPV method for the phase noise and jitter of free-running oscillators: LC and ring oscillators, voltage-controlled oscillators in phase-locked loops, crystal oscillators and relaxation oscillators. It needs the steady-state orbit, so run it after shooting or harmonic balance. For driven circuits with a fixed period, such as mixers, use periodic small-signal noise analysis; for small linear networks, use [circuit noise analysis](/circuit-noise-analysis/).

## Pitfalls

- **Linear analysis around the orbit.** An ordinary linear noise analysis linearized at the periodic solution misses the phase diffusion and predicts a density that diverges at the carrier. The phase direction must be separated, as the PPV does.
- **Euler-Maruyama in a Monte Carlo check.** For the Hopf oscillator with $h = 0.01$, the Euler-Maruyama step map moves the orbit to the radius $\sqrt{\mu + \omega^2 h/2} = \sqrt{1.2}$, because each step adds the factor $1 + \omega^2h^2$ to the squared radius. Five seeds gave measured ratios between 0.82 and 0.94 instead of 1, near the predicted $1/1.2$. For the LC oscillator with 100 steps per period, the amplitude grew from 0.63 to 1.05 V and the ratio was 0.47. Use the stochastic Heun method or a small step, and compare the amplitude with the deterministic orbit.
- **Phase measured by crossings.** A crossing time mixes the phase with the bounded orbital deviation. Use a crossing late in the run, so that the diffusion term $ct$ dominates.
- **Weakly damped orbits.** If the second Floquet multiplier is close to 1, the amplitude recovers slowly, the kick test needs many periods, and the linear analysis holds only for very small noise.
- **Fitted parameters.** The result depends on the fitted transistor parameters through the waveform, and on the fitted coefficients of the device noise models. The tanh law of the example is a model of the transistor pair, not of a real process.
- **Units.** The two-sided density $2kT/R$ and the one-sided density $4kT/R$ differ by a factor of 2 in $c$; the formula for $\mathcal L$ assumes unit two-sided white noise in $\xi$.

## Implementations

## History

Earlier analyses of oscillator phase noise used linear time-invariant models of the oscillator. Hajimiri and Lee (1998) introduced a linear time-varying model with an impulse sensitivity function. Demir, Mehrotra and Roychowdhury (2000) gave a nonlinear theory: they separated the noisy solution into a phase shift and an orbital deviation, showed that the phase becomes a Wiener process with the diffusion constant $c$ computed from the Floquet left eigenvector, which they called the perturbation projection vector, and derived the Lorentzian spectrum. They also gave time-domain and harmonic balance methods to compute $c$, which circuit simulators adopted.

## References
