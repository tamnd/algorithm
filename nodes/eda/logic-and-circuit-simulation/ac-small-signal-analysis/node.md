---
tag: ZS7YDS
kind: algorithm
slug: ac-small-signal-analysis
name: AC small-signal analysis
aliases:
- AC analysis
- small-signal frequency analysis
area: eda/logic-and-circuit-simulation
level: intro
summary: Linearizes the circuit at its DC operating point and solves the complex MNA system at each frequency to get gains, phases and transfer functions.
model: real-ram
complexity:
  vars: {n: the number of MNA unknowns, F: the number of frequency points, D: the cost of the DC operating point, S: the cost of one sparse LU factorization and solve of the complex MNA matrix}
  time: {worst: "O(D + F S)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1975
  people: [Laurence W. Nagel]
  note: SPICE2 computed the small-signal AC response by linearizing its device models at the DC operating point and solving the complex nodal equations at each frequency of a sweep.
prereqs: [modified-nodal-analysis, dc-operating-point-analysis, jacobian-linearization, transfer-function, lu-decomposition]
see_also: [bode-plot, laplace-transform, circuit-noise-analysis, adjoint-sensitivity-analysis, pade-via-lanczos, harmonic-balance-analysis, transient-circuit-analysis, klu-solver]
sources:
  - paper: "Laurence W. Nagel, SPICE2: A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, Electronics Research Laboratory, University of California, Berkeley, 1975"
    title: Laurence W. Nagel, SPICE2, A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, University of California, Berkeley, May 1975
    locator: the small-signal AC analysis (linearized device models at the operating point and the complex nodal solve at each frequency)
  - paper: doi:10.1109/TCS.1975.1084079
    title: Chung-Wen Ho, Albert E. Ruehli and Pierce A. Brennan, The modified nodal approach to network analysis, IEEE Transactions on Circuits and Systems 22(6), 504 to 509, 1975
    locator: the modified nodal formulation, which holds in the frequency domain with complex admittances
  - book: isbn:9780442011949
    title: Jiri Vlach and Kishore Singhal, Computer Methods for Circuit Analysis and Design, second edition, Van Nostrand Reinhold, 1994
    locator: the chapters on frequency-domain analysis of linear networks and on small-signal models of nonlinear devices; the chapter numbers were not checked
  - book: isbn:9780898713534
    title: K. E. Brenan, S. L. Campbell and L. R. Petzold, Numerical Solution of Initial-Value Problems in Differential-Algebraic Equations, SIAM Classics in Applied Mathematics 14, 1996
    locator: Chapter 2, linear constant-coefficient systems and the Weierstrass (Kronecker) canonical form of a regular pencil
  - paper: doi:10.1109/JSSC.1968.1049902
    title: Harold Shichman and David A. Hodges, Modeling and simulation of insulated-gate field-effect transistor switching circuits, IEEE Journal of Solid-State Circuits 3(3), 285 to 289, 1968
    locator: the square-law MOSFET model of the amplifier example
---

AC small-signal analysis computes how a circuit responds to small sinusoidal inputs at each frequency: it finds the [DC operating point](/dc-operating-point-analysis/), replaces every device by its linearization there, and solves one complex linear system $(G + j\omega C)X = b$ per frequency. It belongs to the circuit simulation half of the logic and circuit simulation sub-area, and it is the analysis behind every gain, bandwidth, phase margin and [Bode plot](/bode-plot/) that a circuit simulator reports. The result is exact for the linearized circuit: it is the [transfer function](/transfer-function/) $H(s) = \ell^{\mathsf T}(G + sC)^{-1} b$ evaluated on the imaginary axis.

## In plain words

An amplifier sits at a quiet bias point. Wiggle its input a tiny bit, as a sine wave, and the output wiggles too: bigger or smaller, earlier or later. AC analysis asks how much bigger and how much later, for every frequency you care about.

Because the wiggle is tiny, every transistor behaves like a fixed resistor and a fixed controlled source around its bias point, and every capacitor is just a capacitor. The circuit becomes linear. For a linear circuit, a sine wave in gives a sine wave out at the same frequency, and one complex number per frequency says everything: its size is the gain and its angle is the phase shift. So the simulator solves one set of linear equations with complex numbers per frequency, and draws the gain and phase curves from the answers.

## The problem

The circuit is written in [modified nodal analysis](/modified-nodal-analysis/) form, $f(x) + \frac{d}{dt} q(x) = u(t)$, with $x = (e_1, \ldots, e_n, j_1, \ldots, j_m)$: node voltages first, then the currents of voltage sources and inductors. The sources are DC values $u_0$ plus small AC parts. Each AC source has a phasor, a complex number $A e^{j\phi}$ that stands for the signal $A\cos(\omega t + \phi)$; the vector $b$ collects them in the rows of their sources, as the MNA stamps place the DC values. The output is a linear combination $\ell^{\mathsf T} x$, usually a node voltage or a difference of two.

Input: the circuit with its device models, the AC phasors, an output vector $\ell$ and a list of angular frequencies $\omega_1, \ldots, \omega_F$. Output: $H(j\omega_k) = \ell^{\mathsf T} X(\omega_k)$ for each $k$, usually shown as $20\log_{10}|H|$ in dB and $\arg H$ in degrees.

The device parameters are fitted, not derived: in the example the MOSFET transconductance $k$, threshold $V_T$, channel-length modulation $\lambda$ and the gate-drain overlap capacitance come from fits to measured devices. AC analysis uses whatever values the model card gives.

## The algorithm

```pseudo id=main
AC(circuit, ω_1..ω_F, ℓ)
L1  x₀ ← the DC operating point: solve f(x) = u₀ by Newton's method
L2  G ← ∂f/∂x at x₀; C ← ∂q/∂x at x₀   (the small-signal model of every device)
L3  b ← the vector of AC phasors of the sources
L4  for k = 1, ..., F
L5      Y ← G + jω_k C
L6      solve Y X = b by sparse complex LU factorization
L7      H_k ← ℓᵀ X
L8  return H_1, ..., H_F
```

Line L2 is where the devices enter. A resistor contributes its conductance to $G$ and a capacitor its capacitance to $C$, as in the MNA stamps. A transistor contributes its small-signal parameters at the operating point: for the level-1 MOSFET in saturation, the transconductance $g_m = \partial I_D/\partial V_{GS}$ and the output conductance $g_{ds} = \partial I_D/\partial V_{DS}$. An inductor's row $e_p - e_q - L\, dj/dt = 0$ becomes $e_p - e_q - j\omega L J = 0$, the impedance $j\omega L$. Nonlinear capacitances contribute their derivative $dq/dv$ at the operating point.

The matrix $Y$ has the same sparsity pattern at every frequency, so the fill-reducing ordering and the symbolic analysis of a sparse solver such as [KLU](/klu-solver/) are done once and only the numerical factorization is repeated. Frequencies are usually spaced evenly on a log scale, a fixed number per decade.

## Example

**RC low-pass.** A 1 V AC source drives $R = 1$ kΩ in series with $C = 1$ nF to ground. The output node has $X = 1/(1 + j\omega RC)$. At $\omega = 1/(RC) = 10^6$ rad/s, $X = 1/(1 + j)$: $|X| = 1/\sqrt 2$, which is $-3.01$ dB, and the phase is $-45°$.

**A common-source amplifier.** An n-channel MOSFET with $k = 200\ \mu\mathrm{A/V^2}$, $V_T = 0.5$ V and $\lambda = 0.05\ \mathrm{V^{-1}}$ has its source at ground and its gate at a source of 0.8 V DC with AC phasor 1. A resistor $R_D = 50$ kΩ connects the drain to $V_{DD} = 1.8$ V; a load $C_L = 100$ fF goes from the drain to ground, and an overlap capacitance $C_{gd} = 5$ fF from the gate to the drain.

*Operating point.* In saturation $\frac{k}{2} V_{ov}^2 (1 + \lambda V_{DS}) R_D = V_{DD} - V_{DS}$ with $V_{ov} = 0.3$ V, so $V_{DS} = (1.8 - 0.45)/(1 + 0.45 \cdot 0.05) = 1.3203$ V, above $V_{ov}$ as saturation requires.

*Small-signal model.* $g_m = k V_{ov}(1 + \lambda V_{DS}) = 63.96\ \mu$S and $g_{ds} = \frac{k}{2} V_{ov}^2 \lambda = 0.45\ \mu$S.

*Transfer function.* KCL at the drain gives

$$H(j\omega) = \frac{-(g_m - j\omega C_{gd})}{1/R_D + g_{ds} + j\omega (C_L + C_{gd})}.$$

The DC gain is $-g_m/(1/R_D + g_{ds}) = -3.128$, or 9.90 dB with a phase of $180°$. The pole is at $(1/R_D + g_{ds})/(2\pi (C_L + C_{gd})) = 31.0$ MHz, the right half plane zero at $g_m/(2\pi C_{gd}) = 2.04$ GHz, and at high frequency the gain tends to $C_{gd}/(C_L + C_{gd}) = 0.048$ ($-26.44$ dB), the signal that the overlap capacitance carries past the transistor. The AC analysis of the implementation gives:

| frequency | gain (dB) | phase (degrees) |
| --- | --- | --- |
| 100 kHz | 9.904 | 179.81 |
| 1 MHz | 9.900 | 178.12 |
| 10 MHz | 9.475 | 161.84 |
| 100 MHz | $-0.657$ | 104.41 |
| 1 GHz | $-19.335$ | 65.62 |
| 10 GHz | $-26.268$ | 11.69 |
| 100 GHz | $-26.443$ | 1.18 |

The gain crosses 0 dB at 92.0 MHz, found by bisection on the AC result. The test checks every point of a sweep with four points per decade from 1 kHz to 100 GHz against the formula above to a relative error of $10^{-12}$.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows the following. Write the small-signal circuit as $Gy + C\dot y = \beta(t)$, the first-order term in the amplitude of the response of the nonlinear circuit.

1. If $G + j\omega C$ is nonsingular, $\operatorname{Re}(X e^{j\omega t})$ with $(G + j\omega C)X = b$ solves the small-signal circuit for the input $\operatorname{Re}(b e^{j\omega t})$ exactly, and it is the only solution of that form.
2. If every root of $\det(G + sC) = 0$ (the poles) has a negative real part, every solution tends to this one: it is the sinusoidal steady state. The proof uses the Weierstrass canonical form, cited.
3. $\ell^{\mathsf T}(G + sC)^{-1}b$ is the [Laplace](/laplace-transform/) transfer function of the small-signal circuit, so AC analysis evaluates it at $s = j\omega$.
4. At $\omega = 0$, $H(0)$ is the derivative of the DC output with respect to the DC value of the source.

The step from the nonlinear circuit to the small-signal circuit is the approximation; it is measured, not proved. The tests check:

- The RC and series RLC hand formulas.
- 30 random RC networks (seed 72) against a nodal admittance matrix built independently.
- The amplifier formula above.
- $H(0)$ against a central difference of two DC solves with a step of 1 µV, to a relative error below $10^{-7}$.
- A transient simulation of the amplifier with the input amplitude scaled by $\varepsilon$, at 31 MHz, with the trapezoidal rule for eight periods. The complex amplitude of the output's fundamental in the last period, divided by $\varepsilon$, matches the AC result to $5.9 \times 10^{-5}$ with 200 steps per period, and to $2.4 \times 10^{-4}$ with 100 steps, so this part of the error is the second-order error of the integration. The nonlinear part, the change of that amplitude from $\varepsilon = 10^{-4}$ to $\varepsilon = 10^{-3}$ and to $10^{-2}$, grows by a factor of about 100 for a tenfold $\varepsilon$, as $\varepsilon^2$.

## Complexity

The DC operating point is computed once. Each frequency then costs one factorization and one solve of an $n \times n$ complex sparse matrix, $F$ of them in all. The sparsity pattern of $G + j\omega C$ is the union of those of $G$ and $C$ and does not depend on $\omega$, so the ordering is computed once. The cost $S$ of one factorization depends on the fill-in, as in the [Gilbert-Peierls](/gilbert-peierls-lu/) analysis. The frequencies are independent and can be solved in parallel. The implementation uses dense complex Gaussian elimination, $O(n^3)$ per frequency, which is the reference method for small circuits.

## Properties

- **Exact for the linear model.** No time stepping and no truncation error: the result is the transfer function of the linearized circuit up to rounding.
- **Linear in the AC sources.** Doubling every phasor doubles the result, so the source magnitude is a convention; 1 V or 1 A gives the transfer function directly.
- **Local.** The model holds near one operating point. Distortion, clipping and slewing are outside it.
- **Independent frequencies.** Any frequency grid can be used, and points can be added near a resonance.

## Variants and improvements

- **Noise analysis.** Propagate the noise sources of all devices to the output; with the adjoint system, one transposed solve per frequency serves every source: [small-signal noise analysis](/circuit-noise-analysis/).
- **Sensitivity.** The derivative of $H(j\omega)$ with respect to every element value, again with one adjoint solve per frequency: [adjoint sensitivity analysis](/adjoint-sensitivity-analysis/).
- **Pole-zero analysis and model order reduction.** Instead of sampling $H$ on a grid, compute its poles and zeros, or a reduced model that matches its moments: [Padé via Lanczos](/pade-via-lanczos/).
- **Periodic small-signal analysis.** Linearize around a periodic steady state found by [harmonic balance](/harmonic-balance-analysis/) or [shooting](/shooting-newton-steady-state/) instead of a DC point, for mixers and sampled circuits.
- **DC transfer function.** The $\omega = 0$ case alone gives small-signal DC gains and input and output resistances.

## When to use it

Use AC analysis for the gain, bandwidth, phase margin, input and output impedance and frequency response of any circuit that works around a fixed bias point: amplifiers, filters, regulators and their feedback loops. Use [transient analysis](/transient-circuit-analysis/) or harmonic balance when signals are large, when the circuit switches, or when distortion matters.

## Pitfalls

- **The wrong operating point.** Every result depends on $x_0$. A circuit with several DC solutions, such as a latch, or a bias point that a DC solver reached with the wrong device in saturation, gives a correct analysis of the wrong circuit.
- **Small means small.** The response is exact only in the limit of zero amplitude. A 1 V AC source on a transistor gate does not produce 1 V of real signal; it only scales the transfer function.
- **Unstable circuits.** If the linearized circuit has poles in the right half plane, AC analysis still returns finite numbers, but no steady state exists. Check the poles or a transient run.
- **Singular at resonance.** A lossless LC loop makes $G + j\omega C$ singular at its resonance frequency.
- **A coarse grid.** A sharp resonance can fall between frequency points and be missed. Refine the grid where the phase changes fast.
- **Fitted parameters.** The gain depends on $g_m$ and $g_{ds}$, which come from fitted model parameters. The output conductance in particular is often poorly fitted by simple models.

## Implementations

## History

SPICE2 (Nagel, 1975) offered small-signal AC analysis next to DC and transient analysis. It linearized the device models at the DC operating point, as in line L2, and solved the complex nodal equations at each frequency of a linear, decade or octave sweep. The modified nodal formulation of Ho, Ruehli and Brennan (1975) is the form that SPICE and most later simulators solve, in the frequency domain as in the time domain.

## References
