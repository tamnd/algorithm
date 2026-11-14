---
tag: WY97C5
kind: algorithm
slug: harmonic-balance-analysis
name: Harmonic balance analysis
aliases:
- harmonic balance circuit simulation
- spectral balance
area: eda/logic-and-circuit-simulation
level: advanced
summary: Finds the periodic steady state of a nonlinear circuit by writing node voltages as truncated Fourier series and solving KCL in the frequency domain with Newton.
model: real-ram
complexity:
  vars: {n: the number of MNA unknowns, K: the number of harmonics kept, I: the number of Newton iterations}
  time: {worst: "O(I n^3 K^3)"}
  space: {extra: "O(n^2 K^2)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1986
  people: [Kenneth S. Kundert, Alberto Sangiovanni-Vincentelli]
  note: Kundert and Sangiovanni-Vincentelli made harmonic balance a general circuit simulation method, with device models evaluated in the time domain, the DFT between the two domains and a Newton solve of the frequency-domain equations.
prereqs: [modified-nodal-analysis, newton-method-for-systems, discrete-fourier-transform, ac-small-signal-analysis]
see_also: [shooting-newton-steady-state, fast-fourier-transform, gmres, collocation-method, trigonometric-interpolation, aliasing, transient-circuit-analysis, phase-noise-analysis]
sources:
  - paper: doi:10.1109/TCAD.1986.1270223
    title: Kenneth S. Kundert and Alberto Sangiovanni-Vincentelli, Simulation of nonlinear circuits in the frequency domain, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 5(4), 521 to 535, 1986
    locator: the harmonic balance equations, the evaluation of nonlinear devices in the time domain with the DFT, and the Newton iteration with its Jacobian
  - book: doi:10.1007/978-1-4757-2081-5
    title: Kenneth S. Kundert, Jacob K. White and Alberto Sangiovanni-Vincentelli, Steady-State Methods for Simulating Analog and Microwave Circuits, Springer, 1990
    locator: the chapters on harmonic balance and on the solution of its Newton equations; the chapter numbers were not checked
  - paper: doi:10.1109/TCS.1976.1084181
    title: Michel S. Nakhla and Jiri Vlach, A piecewise harmonic balance technique for determination of periodic response of nonlinear systems, IEEE Transactions on Circuits and Systems 23(2), 85 to 91, 1976
    locator: the split of a circuit into a linear part solved in the frequency domain and a nonlinear part evaluated in the time domain
---

Harmonic balance finds the periodic steady state of a circuit driven by periodic sources without simulating the start-up transient. It writes every unknown as a Fourier series with $K$ harmonics, evaluates the devices in the time domain, and solves the circuit equations for the Fourier coefficients with [Newton's method](/newton-method-for-systems/). It belongs to the circuit simulation half of the logic and circuit simulation sub-area, where it is the standard method for RF and microwave circuits, amplifiers and mixers with mostly sinusoidal signals.

## In plain words

Drive a circuit with a sine wave and wait. After the start-up dies out, every voltage repeats with the period of the input. A transient simulation gets there by stepping through all of the start-up, which can take thousands of periods for a circuit with a slow bias network.

Harmonic balance skips the wait. It guesses each repeating waveform as a sum of sine waves: a constant, the input frequency, twice that frequency, and so on up to a limit. For a guess, it checks at a few points in one period whether the currents into each node add up to zero. If not, it corrects the sizes and phases of all the sine waves at once and checks again, until the currents balance. For a linear circuit one correction gives the exact answer; for a nonlinear one, more sine waves give a better answer.

## The problem

The circuit is in [modified nodal analysis](/modified-nodal-analysis/) form, $f(x) + \frac{d}{dt} q(x) = u(t)$, with $x = (e_1, \ldots, e_n, j_1, \ldots, j_m)$, and every source is periodic with period $T = 2\pi/\omega$. A periodic steady state is a solution with $x(t + T) = x(t)$ for all $t$. Harmonic balance looks for it as a truncated Fourier series

$$x(t) \approx \sum_{k=-K}^{K} X_k e^{jk\omega t}, \qquad X_{-k} = \overline{X_k},$$

so the unknowns are the $K + 1$ complex coefficient vectors $X_0, \ldots, X_K$ (the negative ones are their conjugates). With the [discrete Fourier transform](/discrete-fourier-transform/) $\mathcal F_k$ on $M = 2K + 1$ equally spaced samples $t_i = iT/M$, the equations are

$$R_k(X) = \mathcal F_k\big(f(x(t_i))\big) + jk\omega\,\mathcal F_k\big(q(x(t_i))\big) - \mathcal F_k\big(u(t_i)\big) = 0, \qquad |k| \le K.$$

Each $R_k$ is Kirchhoff's current law at harmonic $k$: resistive currents plus $jk\omega$ times charges, minus the sources. The term $jk\omega Q_k$ is the time derivative in the frequency domain, so linear elements are handled exactly as in [AC analysis](/ac-small-signal-analysis/), at every harmonic. Nonlinear devices cannot be written in the frequency domain, so they are evaluated on the time samples.

Input: the circuit, $\omega$ and $K$. Output: the coefficients $X_k$, from which any waveform, spectrum, gain or distortion figure follows. The device equations have fitted parameters: in the example below, the diode saturation current $I_S$ and emission coefficient $N$ are fitted to measurements, not derived.

## The algorithm

```pseudo id=main
HB(circuit, ω, K)
L1  M ← 2K + 1; t_i ← 2πi/(Mω) for i = 0, ..., M − 1
L2  U ← DFT of the source samples u(t_i); X ← a start spectrum (zero, or a DC or AC solution)
L3  repeat
L4      x_i ← inverse DFT of X, at every t_i
L5      evaluate every device at every x_i: f(x_i), q(x_i), G_i = ∂f/∂x, C_i = ∂q/∂x
L6      R_k ← F_k + jkω Q_k − U_k for |k| ≤ K, where F, Q are the DFTs of f(x_i), q(x_i)
L7      J ← the blocks Ĝ_{k−l} + jkω Ĉ_{k−l}, where Ĝ, Ĉ are the DFTs of G_i, C_i
L8      solve J ΔX = −R; X ← X + λΔX with a step limit λ ≤ 1
L9  until λ = 1 and ΔX is small
L10 return X
```

Lines L4 to L6 move between the two domains: the waveforms go to the time domain, where each device is evaluated as in a [transient](/transient-circuit-analysis/) step, and the currents and charges come back as spectra. Line L7 is the Jacobian. The derivative of the transform of $f(x(t_i))$ with respect to $X_l$ is the transform of $G_i e^{jl\omega t_i}$, which depends only on $k - l$. So $J$ is block Toeplitz: a time-invariant circuit gives $\hat G_d = 0$ for $d \ne 0$ and the blocks decouple by harmonic, while a device whose conductance varies over the period couples harmonic $l$ into harmonic $k$ through the $(k - l)$th harmonic of that conductance. This coupling is how a mixer moves signals from one frequency to another.

The implementation uses direct sums of cost $O(M^2)$ for the transforms and a dense solve for line L8. A production code uses the [FFT](/fast-fourier-transform/) for lines L4 to L7 and solves line L8 with [GMRES](/gmres/), where a product with $J$ is two FFTs and a block-diagonal product, and a preconditioner built from the averaged blocks $\hat G_0 + jk\omega \hat C_0$ makes the iteration converge in few steps when the circuit is mildly nonlinear. The step limit of line L8 keeps every voltage sample from moving more than 0.1 V per iteration.

## Example

**A linear RC circuit, by hand.** A source $v(t) = 1 + \cos\omega t$ drives $R = 1$ kΩ into $C = 1$ nF, with $\omega = 1/(RC) = 10^6$ rad/s, and $K = 1$. The source spectrum is $U_0 = 1$ and $U_{\pm1} = 1/2$. For a linear circuit $\hat G_d$ and $\hat C_d$ vanish for $d \ne 0$, so line L8 solves one small system per harmonic. At the output node, $X_0 = 1$ and $X_1 = \tfrac12/(1 + j\omega RC) = (1 - j)/4$, so the output is $1 + \tfrac{1}{\sqrt2}\cos(\omega t - 45°)$. This is the exact steady state, and Newton needs one step.

**A diode clipper, measured.** A 1 V, 1 MHz sine source behind 1 kΩ drives a node with 100 pF and a diode to ground, with $I_S = 10^{-14}$ A and $N = 1$ (fitted values for a small silicon diode). The diode cuts the positive peaks near 0.63 V. The reference is a trapezoidal transient with 1000 and 2000 steps per period, run for 12 periods from zero and extrapolated with Richardson's rule; the two step sizes differ by $5.7 \times 10^{-6}$ V, and 5 periods and 12 periods give the same last period to $10^{-14}$ V. The error is the largest difference over 1000 points of the period. Newton starts from zero and needs 11 to 13 iterations.

| $K$ | error (V) | DC part (V) | 1st harmonic amplitude (V) |
|---|---|---|---|
| 1 | 0.155 | −0.0923 | 0.7157 |
| 2 | 0.132 | −0.0536 | 0.7932 |
| 4 | 0.048 | −0.0545 | 0.7647 |
| 8 | 0.0132 | −0.0520 | 0.7674 |
| 16 | 0.00257 | −0.0519 | 0.7675 |
| 32 | 0.00014 | −0.0519 | 0.7675 |

**A cubic conductor, measured.** The same source as 1 mA into 100 pF and a conductor with $i = 10^{-3}(v + v^3)$ A gives a smoother waveform. With the same reference, the error is $8.4 \times 10^{-2}$ V at $K = 1$, $7.0 \times 10^{-3}$ at $K = 4$, $6.7 \times 10^{-5}$ at $K = 8$, $1.1 \times 10^{-8}$ at $K = 16$ and $9 \times 10^{-12}$ at $K = 32$, where it reaches the accuracy of the reference. Newton takes 10 iterations for every $K$. The error falls geometrically, as expected for a waveform that is analytic, while the diode's steep exponential makes its spectrum fall much more slowly.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **HB is collocation.** By the orthogonality of the sampled exponentials, the DFT is exact on trigonometric polynomials of degree $K$, so $R(X) = 0$ holds exactly when the circuit equations hold at the $M$ sample times, with the derivative of the charge taken from its trigonometric interpolant.
2. **Real waveforms stay real.** If $X_{-k} = \overline{X_k}$, the residual and the Newton step have the same symmetry.
3. **The Jacobian.** The derivative of $R_k$ with respect to $X_l$ is $\hat G_{(k-l) \bmod M} + jk\omega\,\hat C_{(k-l) \bmod M}$, the matrix of line L7; it is the transform of the time-domain collocation Jacobian, so Newton converges locally and quadratically under the usual conditions.
4. **Linear circuits are exact.** If $f$ and $q$ are linear, the sources have no harmonic above $K$ and $G + jk\omega C$ is nonsingular for every $k$, then $X_k = (G + jk\omega C)^{-1} U_k$ is the exact periodic steady state, and Newton reaches it in one step. With $K = 0$ the equations are those of the DC operating point.

The truncation error for a nonlinear circuit is not proved; the tables above measure it.

The tests check, with fixed seeds:

- The DFT round trip and the exact coefficients of a trigonometric polynomial.
- A linear RLC circuit with a source that has harmonics 1 and 3, against the analytic phasors at each harmonic, to $10^{-12}$; Newton stops after its second iteration, whose step is below the tolerance.
- $K = 0$ against a bisection solution of the DC diode equation, to $10^{-12}$ V.
- The Jacobian of line L7 against central differences of $R$ in random symmetric directions (seed 51), to a relative error of $10^{-6}$.
- The symmetry of the result and a residual below $10^{-12}$.
- The cubic and diode errors above against the transient reference, with fewer periods (5) to keep the test fast.

## Complexity

Each Newton iteration evaluates every device at $M = 2K + 1$ samples, computes the transforms (direct sums $O(nK^2)$ here, $O(nK\log K)$ with the FFT), fills $J$ in $O(n^2K^2)$, and solves a dense system of order $nM$ in $O(n^3K^3)$. Over $I$ iterations this is $O(I n^3 K^3)$ time and $O(n^2 K^2)$ space for $J$. The dense solve limits this form to small circuits. With the FFT, GMRES and a block-diagonal preconditioner, one iteration costs $O(nK\log K)$ per GMRES step plus one sparse factorization of each diagonal block, and the memory is $O(nK)$ plus those factors. The number of GMRES steps depends on how nonlinear the circuit is and is not bounded in advance.

## Properties

- **No start-up transient.** The cost does not depend on the time constants of the circuit, so slow bias networks and high-Q filters cost nothing extra, unlike transient analysis.
- **Exact for linear elements.** Distributed and frequency-dependent elements, such as transmission lines and S-parameter blocks, enter as their admittance at each harmonic, which time-domain methods cannot do directly.
- **Spectral accuracy for smooth waveforms.** The error falls geometrically with $K$ when the waveforms are analytic, and slowly when they have sharp edges.
- **Collocation with aliasing.** Harmonics of $f(x(t))$ above $K$ fold onto lower harmonics. At $K = 1$ the cubic example has a DC part of $-0.046$ V although the exact one is 0: harmonic 3 folds onto harmonic 0.
- **Dense coupling.** $J$ is dense in the harmonic index whenever a device is strongly nonlinear.

## Variants and improvements

- **Multitone and quasi-periodic harmonic balance.** Mixers and intermodulation tests have two or more unrelated frequencies. The series then runs over the sums $k_1\omega_1 + k_2\omega_2$, and the transforms use a multidimensional DFT or almost-periodic Fourier transforms.
- **Krylov harmonic balance.** GMRES with FFT matrix-vector products and a block-diagonal preconditioner, as above; this made harmonic balance usable for integrated circuits with many nodes.
- **Oversampling.** Using more than $2K + 1$ samples reduces aliasing at the cost of a larger transform.
- **Continuation.** Ramp the source amplitude from zero, or start from the [AC](/ac-small-signal-analysis/) solution, to help Newton converge for strongly driven circuits.
- **Periodic small-signal and noise analysis.** Linearizing around the steady state gives the conversion gain and noise of mixers; for autonomous oscillators the frequency becomes an unknown and the steady state feeds [phase noise analysis](/phase-noise-analysis/).
- **Time-domain alternative.** [Shooting Newton](/shooting-newton-steady-state/) finds the same steady state with transient steps over one period and is better for circuits with sharp edges.

## When to use it

Use harmonic balance for circuits whose waveforms are close to sums of a few sinusoids: RF amplifiers, power amplifiers near compression, mixers, frequency multipliers and microwave circuits with distributed elements. Use it when the circuit has long time constants that would make a transient run long. Use [shooting](/shooting-newton-steady-state/) or a [transient](/transient-circuit-analysis/) run for switching circuits, digital dividers and other circuits with fast edges, where the spectrum falls slowly, as the diode table shows.

## Pitfalls

- **Too few harmonics.** The error at $K = 4$ in the diode example is 48 mV, more than 5% of the swing. Check the result by doubling $K$.
- **Aliasing.** The DFT folds harmonics above $K$ back into the band and produces false DC and low-order terms. At $K = 1$ the DC part is wrong by 40 mV in the diode example and by 46 mV in the cubic example.
- **Newton failure.** Exponential devices make Newton diverge from a poor start. Limit the step, as in line L8, or use continuation in the source amplitude.
- **Several steady states.** A circuit can have more than one periodic solution, for example a divider or a circuit with hysteresis. Newton finds one of them, which depends on the start.
- **Autonomous circuits.** An oscillator has no external period. Plain harmonic balance with a fixed $\omega$ finds the trivial DC solution or fails; the frequency must be an extra unknown with a phase condition.
- **Memory of the dense Jacobian.** The direct form stores $(nM)^2$ entries. Use the Krylov form for more than a few nodes.
- **Fitted parameters.** The harmonics of a nonlinear device depend on high derivatives of its model, which the fitted parameters often reproduce badly. Distortion predictions are only as good as the model's fit of those derivatives.

## Implementations

## History

The idea of balancing harmonics is older than circuit simulation, and microwave engineers used it for nonlinear circuits in the 1970s. Nakhla and Vlach (1976) split a circuit into a linear part, which they solved in the frequency domain, and a nonlinear part, which they evaluated in the time domain, and balanced the currents at the interface. Kundert and Sangiovanni-Vincentelli (1986) made it a general method for circuit simulation, with device models evaluated in the time domain, the DFT between the domains and Newton's method on the frequency-domain equations. The book of Kundert, White and Sangiovanni-Vincentelli (1990) compared it with the time-domain steady-state methods. Later work replaced the direct solve with Krylov solvers that use FFT products, which made harmonic balance practical for larger integrated RF circuits.

## References
