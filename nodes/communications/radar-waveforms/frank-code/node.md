---
tag: 63SGZP
kind: definition
slug: frank-code
name: Frank code
aliases:
- Frank polyphase code
- Frank sequence
area: communications/radar-waveforms
level: advanced
summary: "A polyphase code of M squared chips with phases 2 pi m n / M, the rows of the DFT matrix in a row, which has zero periodic autocorrelation sidelobes and approximates a chirp."
prereqs: [autocorrelation, discrete-fourier-transform, phase-coded-waveform]
see_also: [zadoff-chu-sequence, barker-code, costas-array, linear-frequency-modulation-pulse, mismatched-filter-design, range-doppler-coupling, pulse-compression, ambiguity-function]
sources:
  - paper: doi:10.1109/TIT.1963.1057798
    title: "R. L. Frank, Polyphase codes with good nonperiodic correlation properties, IEEE Transactions on Information Theory 9(1), 1963"
    locator: "pp. 43 to 45 (the code with phases 2 pi m n / M, its periodic and aperiodic correlation)"
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 6, Phase-Coded Pulse (polyphase codes, the Frank code and its ambiguity function)"
---

The Frank code is a polyphase [phase-coded waveform](/phase-coded-waveform/) of $N = M^2$ chips whose phases are $2\pi mn/M$ for $m, n = 0, \dots, M-1$. Its periodic autocorrelation is zero at every nonzero shift, and its aperiodic peak sidelobe falls roughly as $1/(\pi M)$ of the peak, $-29.80$ dB for 100 chips. It is in the same family as the [Zadoff-Chu sequence](/zadoff-chu-sequence/), which has the same perfect periodic autocorrelation for every length, not only for squares. The binary [Barker code](/barker-code/) stops at 13 chips, and the Frank code gives low sidelobes at longer lengths and keeps its peak under Doppler like the [chirp](/linear-frequency-modulation-pulse/) it approximates.

## Definition

**Frank code.** For an integer $M \ge 2$, let $\omega = e^{j 2\pi/M}$. The Frank code of length $N = M^2$ is

$$a_{mM + n} = \omega^{mn}, \qquad m, n = 0, 1, \dots, M - 1.$$

So the chip with index $i$ has the phase $2\pi\, \lfloor i/M \rfloor\, (i \bmod M)/M$. Written as an $M \times M$ array, row $m$ is $(1, \omega^m, \omega^{2m}, \dots, \omega^{(M-1)m})$: the code is the rows of the $M \times M$ [DFT](/discrete-fourier-transform/) matrix, with the sign of the exponent reversed, placed one after the other.

**A staircase chirp.** Inside row $m$ the phase grows by $2\pi m/M$ per chip, which is a constant frequency of $m/(M t_c)$ for a chip length $t_c$. So the code steps through $M$ frequencies, each held for $M$ chips, a staircase approximation of a [linear frequency modulation pulse](/linear-frequency-modulation-pulse/) that sweeps a band of $1/t_c$.

**Perfect periodic autocorrelation (theorem).** For every shift $s$ with $s \not\equiv 0 \pmod{N}$,

$$\tilde r[s] = \sum_{i=0}^{N-1} a_{(i + s) \bmod N}\, \overline{a_i} = 0.$$

*Proof.* Write $s = \alpha M + \beta$ with $0 \le \alpha, \beta < M$, and $i = mM + n$. Let $\varepsilon_n = 1$ if $n + \beta \ge M$ and $0$ otherwise. Then $i + s = (m + \alpha + \varepsilon_n)M + (n + \beta - \varepsilon_n M)$, and since $\omega^M = 1$ the index reduction modulo $N$ and modulo $M$ do not change the power of $\omega$, so

$$a_{i+s}\,\overline{a_i} = \omega^{(m + \alpha + \varepsilon_n)(n + \beta) - mn} = \omega^{m\beta}\, \omega^{(\alpha + \varepsilon_n)(n + \beta)}.$$

For a fixed $n$, the sum over $m$ of $\omega^{m\beta}$ is $0$ if $\beta \ne 0$, so $\tilde r[s] = 0$. If $\beta = 0$, then $\varepsilon_n = 0$, the sum over $m$ is $M$, and $\tilde r[s] = M\sum_n \omega^{\alpha n}$, which is $0$ since $\alpha \ne 0$. $\square$

A sequence of constant magnitude with this property is called a CAZAC sequence (constant amplitude, zero autocorrelation).

## Examples and non-examples

**$M = 2$.** $\omega = -1$ and the code is $(1, 1, 1, -1)$, a binary code of 4 chips and a [Barker code](/barker-code/). Its aperiodic autocorrelation is $4, 1, 0, -1$.

**$M = 3$.** In units of $2\pi/3$, the phases are $(0, 0, 0,\ 0, 1, 2,\ 0, 2, 1)$. Each group of three is one row of the DFT matrix.

**$M = 4$.** The code has 16 chips with the phases $0, \pi/2, \pi, 3\pi/2$. The magnitudes of its aperiodic autocorrelation begin $16, 1, 1.414, 1, 0, 1, 1.414, 1, 0, \dots$, so the peak sidelobe is $\sqrt 2$, which is $-21.07$ dB.

**Peak sidelobe against length.** Computed from the codes:

| $M$ | $N$ | largest $\lvert r[k] \rvert$ | PSL |
|---|---|---|---|
| 2 | 4 | 1 | $-12.04$ dB |
| 3 | 9 | 1 | $-19.08$ dB |
| 4 | 16 | 1.414 | $-21.07$ dB |
| 5 | 25 | 1.618 | $-23.78$ dB |
| 6 | 36 | 2 | $-25.11$ dB |
| 7 | 49 | 2.247 | $-26.77$ dB |
| 8 | 64 | 2.613 | $-27.78$ dB |
| 9 | 81 | 2.879 | $-28.98$ dB |
| 10 | 100 | 3.236 | $-29.80$ dB |

The ratio of the peak $N$ to the largest sidelobe is 30.90 for $M = 10$, close to $\pi M = 31.42$: the PSL is about $1/(\pi M)$ for large $M$ (a rule from these values and the staircase chirp, not a theorem here). The periodic sidelobes were zero for every $M$ from 2 to 10, as the theorem says.

**Doppler (computed with one sample per chip).** For $M = 4$, at a Doppler shift with $\nu T = 1$, the largest output is 0.85 of the peak, moved by one chip in delay, as for a chirp with its [range-Doppler coupling](/range-doppler-coupling/). The Barker code of 13 chips has no peak left at zero delay at the same $\nu T$.

**Non-example: Zadoff-Chu sequences.** A Zadoff-Chu sequence of length $N$ has the phases $-\pi u n(n + c)/N$ with $c = N \bmod 2$, for a root $u$ coprime to $N$. It is also CAZAC, but its phase is a smooth quadratic in $n$, not a product of the row and column indices, and it exists for every $N$. The two are often treated together as Frank-Zadoff-Chu sequences.

**Non-example: a sampled chirp.** A chirp sampled at one sample per chip has the phases $\pi k n^2 t_c^2$, quadratic in $n$. It is close to a Zadoff-Chu sequence, not to a Frank code, and it has zero periodic sidelobes only for special choices of the sweep.

**Non-example: $M$ not an integer square root.** For a length $N$ that is not a square, there is no Frank code. Use a Zadoff-Chu sequence or a P code of the same family.

## Related definitions

- **Zadoff-Chu sequence.** The [Zadoff-Chu sequence](/zadoff-chu-sequence/) is the other main CAZAC sequence. It is the reference signal of LTE and 5G, where the zero periodic autocorrelation matters.
- **Barker code.** The [Barker code](/barker-code/) is binary and has a lower PSL for the lengths at which it exists, up to 13 chips.
- **Costas array.** A [Costas array](/costas-array/) codes frequency, not phase, and its frequency order is a permutation, not a staircase. Its ambiguity function is close to a thumbtack, with no ridge.
- **Mismatched filter.** For the Frank code of 16 chips, a [mismatched filter](/mismatched-filter-design/) of 47 taps lowers the PSL from $-21.07$ dB to $-30.76$ dB at a loss of 0.664 dB.
- **Pulse compression.** Polyphase codes are used for [pulse compression](/pulse-compression/) in digital radars, where the phases are generated directly.

## References
