---
tag: YR55TR
kind: definition
slug: phase-coded-waveform
name: Phase-coded waveform
aliases:
- phase-coded pulse
- biphase code
- phase code
area: communications/radar-waveforms
level: core
summary: "A pulse cut into N chips of equal length, each with a constant phase taken from a code, whose matched filter output is the aperiodic autocorrelation of the code."
prereqs: [autocorrelation, matched-filter, pulse-compression]
see_also: [barker-code, frank-code, zadoff-chu-sequence, maximal-length-sequence, mismatched-filter-design, ambiguity-function, linear-frequency-modulation-pulse, direct-sequence-spread-spectrum]
sources:
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 6, Phase-Coded Pulse (pp. 100 to 167: binary codes, polyphase codes, the merit factor and the ambiguity functions of codes)"
  - book: isbn:9780071798327
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, second edition, McGraw-Hill, 2014"
    locator: "Chapter 4, Radar Waveforms (phase-coded waveforms, Barker and polyphase codes, and their sidelobes and Doppler response)"
  - paper: doi:10.1109/TIT.1963.1057798
    title: "R. L. Frank, Polyphase codes with good nonperiodic correlation properties, IEEE Transactions on Information Theory 9(1), 1963"
    locator: pp. 43 to 45 (polyphase codes for pulse compression and their correlation)
---

A phase-coded waveform is a pulse of constant amplitude cut into $N$ chips of equal length $t_c$, each with a constant phase given by a code. Its bandwidth is about $1/t_c$, so after [pulse compression](/pulse-compression/) it resolves about one chip, $c t_c/2$ in range, while its energy is that of the whole pulse of length $N t_c$. The [matched filter](/matched-filter/) output at whole chip delays is the aperiodic [autocorrelation](/autocorrelation/) of the code, so the choice of code sets the sidelobes. A [linear frequency modulation pulse](/linear-frequency-modulation-pulse/) changes the frequency smoothly instead, and the [Barker code](/barker-code/) and the [Frank code](/frank-code/) are two codes of this family, one binary and one polyphase.

## Definition

**Phase-coded pulse.** Let $a_0, \dots, a_{N-1}$ be complex numbers with $|a_n| = 1$, the code, and let $t_c > 0$ be the chip length. The complex envelope is

$$u(t) = \frac{1}{\sqrt{N t_c}} \sum_{n=0}^{N-1} a_n\, p(t - n t_c),$$

where $p(t) = 1$ for $0 \le t < t_c$ and $0$ otherwise. The pulse length is $T = N t_c$ and the energy is 1. The phases $\varphi_n = \arg a_n$ are the code. A code is binary if every $a_n$ is $+1$ or $-1$, and polyphase if it uses more than two phases.

**Aperiodic autocorrelation.** $r[k] = \sum_{n=0}^{N-1-k} a_{n+k}\, \overline{a_n}$ for $k = 0, \dots, N-1$, and $r[-k] = \overline{r[k]}$. Then $r[0] = N$.

**Matched filter output (closed form).** At zero Doppler, with the delay $\tau = m t_c + s$ for an integer $m$ and $0 \le s \le t_c$,

$$\chi(\tau, 0) = \frac{1}{N}\Bigl( \bigl(1 - \tfrac{s}{t_c}\bigr) r[m] + \tfrac{s}{t_c}\, r[m+1] \Bigr),$$

a linear interpolation between the values at whole chips. So the largest sidelobe of the output is the largest $|r[k]|$ with $k \ne 0$.

**Measures of a code.** The peak sidelobe level is $\mathrm{PSL} = \max_{k \ne 0} |r[k]| / N$, usually given in dB as $20\log_{10}$ of that ratio. The integrated sidelobe level is $\mathrm{ISL} = \sum_{k \ne 0} |r[k]|^2 / N^2$. The merit factor is $F = N^2 / (2\sum_{k=1}^{N-1} |r[k]|^2)$, the inverse of the ISL.

**Periodic autocorrelation.** $\tilde r[k] = \sum_{n=0}^{N-1} a_{(n+k) \bmod N}\, \overline{a_n}$. It describes the output for a code repeated without gaps, as in continuous wave radar. A code with $\tilde r[k] = 0$ for all $k \ne 0$ is called perfect. The aperiodic and periodic sidelobes of one code can be very different.

## Examples and non-examples

The values below are computed from the codes.

| Code | $N$ | Phases | Aperiodic PSL | Merit factor |
|---|---|---|---|---|
| Barker | 7 | binary, $(+, +, +, -, -, +, -)$ | $1/7$, $-16.90$ dB | 8.17 |
| Barker | 13 | binary, $(+, +, +, +, +, -, -, +, +, -, +, -, +)$ | $1/13$, $-22.28$ dB | 14.08 |
| maximal length sequence | 15 | binary, one cyclic shift | $4/15$, $-11.48$ dB | |
| maximal length sequence | 15 | binary, the best cyclic shift | $3/15$, $-13.98$ dB | |
| maximal length sequence | 31 | binary, the best cyclic shift | $4/31$, $-17.79$ dB | |
| Frank | 16 | 4 phases | $\sqrt{2}/16$, $-21.07$ dB | |
| Frank | 100 | 10 phases | $-29.80$ dB | |

**Barker codes.** The [Barker codes](/barker-code/) are the binary codes with every aperiodic sidelobe of magnitude at most 1. The longest known has 13 chips.

**Maximal length sequences.** A [maximal length sequence](/maximal-length-sequence/) of length $2^m - 1$ has the two-valued periodic autocorrelation $N$ and $-1$, which is ideal for a repeated code. Its aperiodic sidelobes depend on the cyclic shift that starts the pulse: for the sequence of length 15 above, from $4/15$ for one shift to $3/15$ for the best one.

**Polyphase codes.** The [Frank code](/frank-code/) of $M^2$ chips and the [Zadoff-Chu sequences](/zadoff-chu-sequence/) are perfect codes in the periodic sense, and the aperiodic PSL of the Frank code falls as the length grows. The P codes of Lewis and Kretschmer are related forms with the phases ordered differently. They follow a staircase approximation of a chirp, so they share its tolerance of Doppler and its [range-Doppler coupling](/range-doppler-coupling/).

**Doppler response (computed with one sample per chip).** A Doppler shift $\nu$ adds the phase $2\pi\nu t$, which turns across the pulse by $2\pi\nu T$. For the Barker code of 13 chips, the peak falls to 0.90 at $\nu T = 0.25$ and to 0.64 at $\nu T = 0.5$. The largest sidelobe rises from $-22.28$ dB to $-10.63$ dB and to $-2.99$ dB below the peak. The Frank code of 16 chips at $\nu T = 1$ keeps a peak of 0.85, moved by one chip, while the Barker code at $\nu T = 1$ has no peak left at zero delay.

**Non-example: the LFM pulse.** A chirp has a phase $\pi k t^2$ that changes at every instant, not in steps. Sampling it at the chip rate gives a polyphase code, but the chirp itself is not a phase-coded pulse.

**Non-example: a Costas pulse.** A pulse that hops through frequencies in the order of a [Costas array](/costas-array/) codes the frequency of each chip, not its phase.

**Non-example: a train of pulses with different phases.** Changing the phase from one pulse to the next, for example to separate the echoes of successive pulses, codes the train, not the pulse. Each pulse has one constant phase.

## Related definitions

- **Pulse compression.** The phase code is one of the two main waveforms of [pulse compression](/pulse-compression/), with frequency modulation.
- **Mismatched filter.** A [mismatched filter](/mismatched-filter-design/) can lower the sidelobes of any code below its autocorrelation sidelobes, at a small loss in signal to noise ratio.
- **Spread spectrum.** A [direct sequence spread spectrum](/direct-sequence-spread-spectrum/) signal is the same construction in communications, with a code that is often periodic and with data on top of it.
- **Ambiguity function.** The zero Doppler cut of the [ambiguity function](/ambiguity-function/) of a phase-coded pulse is the interpolated autocorrelation above, and its Doppler cuts show the Doppler response.

## References
