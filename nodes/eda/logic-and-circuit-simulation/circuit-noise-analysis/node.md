---
tag: P2C0RA
kind: algorithm
slug: circuit-noise-analysis
name: Small-signal noise analysis
aliases:
- AC noise analysis
- adjoint noise analysis
area: eda/logic-and-circuit-simulation
level: core
summary: Sums the thermal, shot and flicker noise of every device at an output, using one adjoint solve per frequency as in Rohrer, Nagel, Meyer and Weber.
model: real-ram
complexity:
  vars: {n: the number of MNA unknowns, F: the number of frequency points, K: the number of noise sources, D: the cost of the DC operating point, S: the cost of one sparse LU factorization and solve of the complex MNA matrix}
  time: {worst: "O(D + F (S + K))"}
  space: {extra: "O(n^2 + K)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1971
  people: [Ronald A. Rohrer, Laurence W. Nagel, Robert G. Meyer, L. Weber]
  note: Rohrer, Nagel, Meyer and Weber computed the output noise of all uncorrelated device noise sources with one analysis of the interreciprocal adjoint network per frequency, instead of one analysis per source.
prereqs: [ac-small-signal-analysis, adjoint-sensitivity-analysis, power-spectral-density]
see_also: [tellegen-theorem, wiener-khinchin-theorem, phase-noise-analysis, transfer-function, shichman-hodges-model, klu-solver, harmonic-balance-analysis]
sources:
  - paper: doi:10.1109/JSSC.1971.1050169
    title: Ronald Rohrer, Laurence Nagel, Robert Meyer and L. Weber, Computationally efficient electronic-circuit noise calculations, IEEE Journal of Solid-State Circuits 6(4), 204 to 213, 1971
    locator: the interreciprocal adjoint network, which gives the transfer from every noise source to the output with one analysis
  - paper: doi:10.1103/PhysRev.32.110
    title: H. Nyquist, Thermal agitation of electric charge in conductors, Physical Review 32(1), 110 to 113, 1928
    locator: the thermal noise of a resistor from thermodynamics, the density 4kTR for the voltage
  - paper: doi:10.1103/PhysRev.32.97
    title: J. B. Johnson, Thermal agitation of electricity in conductors, Physical Review 32(1), 97 to 109, 1928
    locator: the measurement of the thermal noise of resistors
  - url: "https://github.com/imr/ngspice/blob/master/src/spicelib/analysis/nevalsrc.c"
    title: ngspice source code, src/spicelib/analysis/nevalsrc.c
    locator: the function NevalSrc, which multiplies 2 q |I| (shot noise) or 4 k T G (thermal noise) by the squared magnitude of the adjoint voltage across the source
  - url: "https://github.com/imr/ngspice/blob/master/src/spicelib/devices/mos1/mos1noi.c"
    title: ngspice source code, src/spicelib/devices/mos1/mos1noi.c
    locator: the channel thermal noise 4 k T (2/3) |gm| and the flicker noise KF |Id|^AF / (f Cox Leff^2) of the level-1 MOSFET
  - url: "https://github.com/imr/ngspice/blob/master/src/spicelib/analysis/noisean.c"
    title: ngspice source code, src/spicelib/analysis/noisean.c
    locator: the frequency loop, which solves the AC system and then the adjoint system once per frequency and sums the contributions of every generator
  - paper: "Laurence W. Nagel, SPICE2: A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, Electronics Research Laboratory, University of California, Berkeley, 1975"
    title: Laurence W. Nagel, SPICE2, A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, University of California, Berkeley, May 1975
    locator: the noise analysis of SPICE2; the section was not checked
---

Small-signal noise analysis computes the spectral density of the random noise at a circuit output: it linearizes the circuit at its [DC operating point](/dc-operating-point-analysis/), gives every resistor, junction and transistor channel a noise current source, and adds the power that each source delivers to the output. It belongs to the circuit simulation half of the logic and circuit simulation sub-area. The key step, due to Rohrer, Nagel, Meyer and Weber (1971), is one solve with the transposed MNA matrix per frequency, which gives the transfer from every source to the output at once.

## In plain words

Every resistor hisses, because the electrons in it move at random with the heat. Every diode crackles, because current crosses a junction in single charges. Transistors do both and also make a slow rumble that is strong at low frequencies. An amplifier amplifies all of these together with the signal, so its output is never perfectly clean.

The simulator wants to know how loud that hiss is at the output, frequency by frequency, and which device makes most of it. Each tiny noise source travels to the output through the circuit, which makes it louder or softer. The sources are independent, so their powers simply add. The trick is to find how strongly every source reaches the output with one calculation instead of one calculation per source: run the circuit backwards from the output once, and read off every answer.

## The problem

The circuit is in [modified nodal analysis](/modified-nodal-analysis/) form, $f(x) + \frac{d}{dt} q(x) = u(t)$, with $x = (e_1, \ldots, e_n, j_1, \ldots, j_m)$. At the operating point $x_0$ the small-signal matrices are $G = \partial f/\partial x$ and $C = \partial q/\partial x$, as in [AC small-signal analysis](/ac-small-signal-analysis/), and at the frequency $f$ the complex MNA matrix is $Y = G + j\omega C$ with $\omega = 2\pi f$.

Noise source $k$ is a current that leaves node $p_k$ and enters node $q_k$, with a one-sided [power spectral density](/power-spectral-density/) $S_k(f)$ in $\mathrm{A^2/Hz}$, computed from the operating point. The standard sources are:

| element | source | density $S_k(f)$ |
| --- | --- | --- |
| resistor $R$ | thermal | $4kT/R$ |
| junction with current $I$ | shot | $2q\lvert I\rvert$ |
| MOSFET in saturation | channel thermal | $4kT \cdot \tfrac23 g_m$ |
| MOSFET or junction | flicker | $K_F \lvert I\rvert^{A_F} / (f\, C_{\mathrm{ox}} L_{\mathrm{eff}}^2)$ |

Here $k$ is Boltzmann's constant, $T$ the temperature, $q$ the electron charge and $g_m$ the transconductance at the operating point. The thermal density is Nyquist's result. The factor $\tfrac23$ is the long-channel value that ngspice uses in its level-1 MOSFET. The flicker coefficients $K_F$ and $A_F$ are fitted to measurements of each process and are not derived; $C_{\mathrm{ox}}$ and $L_{\mathrm{eff}}$ come from the geometry. The current and $g_m$ come from the device model, whose parameters are fitted too: for the [Shichman-Hodges model](/shichman-hodges-model/) of the example, $k$, $V_T$ and $\lambda$.

Input: the circuit, an output vector $\ell$ (the output is $\ell^{\mathsf T} x$, usually a node voltage) and the frequencies $f_1, \ldots, f_F$. Output: the output noise density $S_{\mathrm{out}}(f_i)$ in $\mathrm{V^2/Hz}$ and the share of each source in it. The sources are assumed mutually uncorrelated.

## The algorithm

```pseudo id=main
NOISE(circuit, f_1..f_F, ℓ)
L1  x₀ ← the DC operating point; G ← ∂f/∂x and C ← ∂q/∂x at x₀
L2  list the noise sources (p_k, q_k, S_k) with S_k evaluated at x₀
L3  for i = 1, ..., F
L4      Yᵀ ← (G + j2πf_i C)ᵀ, factored by sparse complex LU
L5      solve Yᵀ z = ℓ                       ▷ the adjoint system, one solve
L6      for every source k: share_k ← |z_{q_k} − z_{p_k}|² S_k(f_i)
L7      S_out(f_i) ← Σ_k share_k
L8  return S_out(f_1..f_F) and the shares
```

The transfer from source $k$ to the output is $H_k = \ell^{\mathsf T} Y^{-1} a_k$, where $a_k = \mathbf e_{q_k} - \mathbf e_{p_k}$ is the KCL right side of a unit current from $p_k$ to $q_k$. The direct method solves $Y x = a_k$ once per source. Line L5 instead solves once with $Y^{\mathsf T}$, and then $H_k = z^{\mathsf T} a_k = z_{q_k} - z_{p_k}$ for every $k$. The transpose is the plain transpose, not the conjugate transpose. In circuit terms $Y^{\mathsf T}$ is the matrix of the adjoint network, the circuit with every controlled source turned around, driven by a unit current at the output; this is the same transposed solve as in [adjoint sensitivity analysis](/adjoint-sensitivity-analysis/), and the factors of $Y$ serve for it, $Y^{\mathsf T} = U^{\mathsf T} L^{\mathsf T} P$.

The output noise is often referred to the input: divide $S_{\mathrm{out}}$ by $|H|^2$, the squared gain from the signal source to the output from an AC analysis. The total noise in a band is the integral of $S_{\mathrm{out}}$ over the band, and its root is the RMS noise voltage.

## Example

**A divider.** $R_1$ from a quiet source to the output and $R_2$ from the output to ground. Each resistor injects into the output node, whose impedance is $R_1 \parallel R_2$, so $S_{\mathrm{out}} = (4kT/R_1 + 4kT/R_2)(R_1 \parallel R_2)^2 = 4kT\,(R_1 \parallel R_2)$: the thermal noise of the parallel resistance.

**kT/C.** Put a capacitor $C$ across the output of a resistor $R$ from a grounded source. The output impedance is $R/(1 + j\omega RC)$, and the integral of $4kTR/(1 + (2\pi fRC)^2)$ over all $f \ge 0$ is $kT/C$, whatever $R$ is. For 1 pF at 300 K that is 64.4 µV RMS.

**The common-source amplifier.** This is the amplifier of the AC analysis page: an n-channel MOSFET with $k = 200\ \mu\mathrm{A/V^2}$, $V_T = 0.5$ V and $\lambda = 0.05\ \mathrm{V^{-1}}$, its gate at a quiet 0.8 V source, $R_D = 50$ kΩ to $V_{DD} = 1.8$ V, $C_L = 100$ fF from the drain to ground and $C_{gd} = 5$ fF from the gate to the drain. The flicker parameters are $K_F = 10^{-28}$ and $A_F = 1$ (fitted values), with $C_{\mathrm{ox}} L_{\mathrm{eff}}^2 = 8.6\ \mathrm{mF/m^2} \times (1\ \mu\mathrm m)^2$. At the operating point $I_D = 9.594\ \mu$A, $g_m = 63.96\ \mu$S and $g_{ds} = 0.45\ \mu$S.

Three sources reach the drain through the same impedance $Z = 1/(1/R_D + g_{ds} + j\omega(C_L + C_{gd}))$, since the gate is held by an ideal source:

$$S_{\mathrm{out}}(f) = \Big(\frac{4kT}{R_D} + \frac83 kT g_m + \frac{K_F I_D}{f\, C_{\mathrm{ox}} L_{\mathrm{eff}}^2}\Big)\, |Z|^2.$$

The white part is $3.31 \times 10^{-25} + 7.06 \times 10^{-25}\ \mathrm{A^2/Hz}$, so the channel makes 68.1% of the white noise and $R_D$ 31.9%. The flicker term equals the white part at the corner frequency $K_F I_D/(C_{\mathrm{ox}} L_{\mathrm{eff}}^2 \cdot 1.038 \times 10^{-24}) = 107.5$ kHz. The implementation gives:

| frequency | output (nV/√Hz) | referred to the input (nV/√Hz) | flicker share |
| --- | --- | --- | --- |
| 1 Hz | 16333 | 5222 | 1.000 |
| 100 Hz | 1634 | 522.4 | 0.999 |
| 10 kHz | 170.8 | 54.6 | 0.915 |
| 100 kHz | 71.76 | 22.94 | 0.518 |
| 1 MHz | 52.40 | 16.76 | 0.097 |
| 10 MHz | 47.66 | 16.01 | 0.011 |
| 100 MHz | 14.76 | 15.92 | 0.001 |
| 1 GHz | 1.543 | 14.30 | 0.000 |

The output falls above the 31.0 MHz pole. Referred to the input, the white floor is $\sqrt{4kT/R_D + \frac83 kT g_m}/g_m = 15.93$ nV/√Hz; it falls at the highest frequencies because the gain there includes the feedthrough of $C_{gd}$. The white output noise integrated over all frequencies is 347.6 µV RMS, against 198.6 µV for $kT/(C_L + C_{gd})$ alone: the transistor adds noise beyond that of a resistor.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that line L5 gives every transfer exactly, $\ell^{\mathsf T} Y^{-1} a_k = (Y^{-\mathsf T}\ell)^{\mathsf T} a_k = z_{q_k} - z_{p_k}$. For mutually uncorrelated sources the cross terms of the output autocorrelation vanish, so the output density is $\sum_k |H_k|^2 S_k$ by the filter rule of the power spectral density and the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/), which are cited. It also derives the kT/C integral. The source densities and the small-signal model are models, not theorems; the proof states where they enter.

The tests check, with measured tolerances:

- The divider against $4kT(R_1 \parallel R_2)$ and each share against $4kT/R_i \cdot (R_1 \parallel R_2)^2$, to $10^{-12}$ relative.
- The RC integral, by the midpoint rule with 64 points on $2\pi fRC = \tan\theta$, against $kT/C$ for $R$ from 100 Ω to 1 MΩ, to $10^{-9}$ relative. The substitution makes the integrand constant, so the rule is exact up to rounding and the test checks the density at every point.
- The amplifier against the formula above at 45 frequencies from 1 Hz to 100 GHz, to $10^{-12}$ relative, and the flicker share at the corner, $\tfrac12$.
- A diode biased by a current $I_B$ from 1 µA to 1 mA against $2qI_B/g_d^2$; at 1 mA this is 0.463 nV/√Hz.
- 40 random networks (seed 81) of 3 to 7 nodes with resistors, capacitors, an inductor and controlled sources: the adjoint result matches the direct sum, one forward solve per source, within a relative difference of $3.9 \times 10^{-15}$ (measured worst case). Solving with $Y$ in place of $Y^{\mathsf T}$ gives an error above 0.1% in 33 of the 40, because the controlled sources make $Y$ unsymmetric.

## Complexity

The operating point is computed once, at cost $D$. Each frequency costs one factorization and one solve, $S$, plus $O(1)$ per source in lines L6 and L7, so the total is $O(D + F(S + K))$. The direct method costs $O(D + F(S + K s))$, where $s$ is the cost of one extra solve with the factors, so it is slower by a factor that grows with $K$. The implementation uses dense elimination; on an RC ladder its CPU time per frequency, measured with `time.process_time`, was 5.3 times less than the direct method's with 18 sources, 12 times less with 38 and 38 times less with 78. The extra space is the factors and one adjoint vector, plus the $K$ shares.

## Properties

- **One solve for all sources.** The cost per frequency hardly depends on the number of noise sources.
- **Exact for the linear model.** Up to rounding, the result is the output density of the small-signal circuit with the given source densities.
- **A breakdown by source.** The shares come free and tell the designer which device to change.
- **Powers add, not amplitudes.** Uncorrelated sources add in $|H_k|^2 S_k$. Two equal sources give $\sqrt2$ times the noise voltage of one, not twice.

## Variants and improvements

- **Input-referred noise and noise figure.** Divide by the squared gain from an AC analysis, or compare with the noise of the source resistance.
- **Correlated sources.** Two sources in one device with a cross spectrum $S_{kl}$ add the terms $2\operatorname{Re}(H_k \overline{H_l} S_{kl})$; the adjoint still gives every $H_k$.
- **Integrated noise.** Integrate $S_{\mathrm{out}}$ over a band, as in the kT/C example. A model reduced by [Padé via Lanczos](/pade-via-lanczos/) can give the transfer functions at many frequencies cheaply.
- **Periodic and cyclostationary noise.** Mixers and switched circuits are linearized around a periodic steady state from [harmonic balance](/harmonic-balance-analysis/) or [shooting](/shooting-newton-steady-state/), and noise is folded between sidebands.
- **Oscillator phase noise.** In an oscillator the noise accumulates in the phase, which the small-signal model cannot describe; [phase noise analysis](/phase-noise-analysis/) treats it.

## When to use it

Use noise analysis for the noise floor, input-referred noise, noise figure and signal-to-noise ratio of amplifiers, filters, references and receivers that work around a fixed bias point. Do not use it for oscillators, for circuits that switch, or for noise large enough to change the operating point; use phase noise analysis or a transient analysis with noise there.

## Pitfalls

- **The transpose, not the conjugate transpose.** $Y$ is complex symmetric for RLC circuits but not with controlled sources; solving with $Y$, or with $Y^{\mathsf H}$, gives wrong transfers. The random test measures this.
- **Fitted noise parameters.** $K_F$ and $A_F$ are fitted per process, and the factor $\tfrac23$ is the long-channel value. The flicker corner and the low-frequency noise are only as good as the fit.
- **Noiseless sources.** Ideal sources and controlled sources make no noise. A bias network built from them can hide noise that a real one would add.
- **One-sided and two-sided densities.** $4kT/R$ is one-sided, over $f \ge 0$. Mixing it with a two-sided density from another tool gives a factor of 2.
- **The operating point.** The densities and transfers depend on $x_0$, like every small-signal result.
- **Flicker at zero frequency.** The $1/f$ density has no finite integral down to $f = 0$; integrate from a stated low frequency.

## Implementations

## History

Johnson measured the thermal noise of resistors in 1928, and Nyquist derived its density from thermodynamics in the same issue of the Physical Review. Rohrer, Nagel, Meyer and Weber (1971) gave the method of this page: one analysis of the interreciprocal adjoint network yields the transfer from every uncorrelated noise source to the output, so the work no longer grows with the number of sources. SPICE2 (Nagel, 1975) included a noise analysis, and the ngspice simulator still solves the AC system and then the adjoint system once per frequency and sums the contribution of every generator.

## References
