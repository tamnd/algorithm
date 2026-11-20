---
tag: 5QPDZX
kind: definition
slug: barker-code
name: Barker code
aliases:
- Barker sequence
area: communications/radar-waveforms
level: core
summary: "A binary sequence whose aperiodic autocorrelation sidelobes are at most 1 in magnitude. Barker codes exist for lengths 2, 3, 4, 5, 7, 11 and 13, and no longer one is known."
prereqs: [autocorrelation, phase-coded-waveform]
see_also: [pulse-compression, frank-code, costas-array, mismatched-filter-design, maximal-length-sequence, direct-sequence-spread-spectrum, kronecker-product, ambiguity-function]
sources:
  - book: "W. Jackson (editor), Communication Theory, Butterworths Scientific Publications, London, 1953"
    title: "R. H. Barker, Group synchronizing of binary digital systems"
    locator: "pp. 273 to 287 (binary sequences whose aperiodic autocorrelation sidelobes are 0 or of magnitude 1, used as synchronization words)"
  - paper: doi:10.1090/S0002-9939-1961-0125026-2
    title: "R. Turyn and J. Storer, On binary sequences, Proceedings of the American Mathematical Society 12(3), 1961"
    locator: pp. 394 to 399 (no Barker sequence of odd length greater than 13 exists)
  - paper: doi:10.1112/S1461157013000223
    title: "Peter Borwein and Michael J. Mossinghoff, Wieferich pairs and Barker sequences, II, LMS Journal of Computation and Mathematics 17(1), 2014"
    locator: pp. 24 to 32 (the computation that rules out the remaining lengths of Barker sequences up to a very large bound)
  - url: https://arxiv.org/abs/1602.03722
    title: "Kai-Uwe Schmidt, Sequences with small correlation, Designs, Codes and Cryptography, 2016"
    locator: the section on Barker sequences (the necessary form 4u squared of a longer Barker sequence and the bound of 4 times 10 to the 33 for its length)
  - book: isbn:9780471473787
    title: "Nadav Levanon and Eli Mozeson, Radar Signals, Wiley, 2004"
    locator: "Chapter 6, Phase-Coded Pulse (the Barker codes and their ambiguity functions)"
---

A Barker code is a sequence of $+1$ and $-1$ whose aperiodic [autocorrelation](/autocorrelation/) has every sidelobe equal to 0 or of magnitude 1, the least possible for a binary sequence. As a binary [phase-coded waveform](/phase-coded-waveform/), it gives [pulse compression](/pulse-compression/) with sidelobes $20\log_{10}(1/N)$ below the peak, $-22.28$ dB for the longest known code, of length 13. Barker codes exist for the lengths 2, 3, 4, 5, 7, 11 and 13. No Barker code of odd length above 13 exists, and none of even length between 14 and $4 \times 10^{33}$. The polyphase [Frank code](/frank-code/) and the frequency hopping [Costas array](/costas-array/) are codes of other kinds, chosen for longer lengths and for Doppler.

## Definition

**Barker sequence.** A sequence $a_0, \dots, a_{N-1}$ with every $a_n \in \{+1, -1\}$ is a Barker sequence if its aperiodic autocorrelation

$$r[k] = \sum_{n=0}^{N-1-k} a_{n+k}\, a_n$$

satisfies $|r[k]| \le 1$ for $1 \le k \le N - 1$.

**Parity.** $r[k]$ is a sum of $N - k$ terms equal to $\pm 1$, so it has the parity of $N - k$. So in a Barker sequence $r[k] = 0$ when $N - k$ is even and $r[k] = \pm 1$ when $N - k$ is odd, and $r[N-1] = a_{N-1} a_0 = \pm 1$ always. No binary sequence of length $N \ge 2$ has a peak sidelobe below 1, so Barker sequences are the best possible.

**Equivalence.** Negating every term, reversing the order, and multiplying $a_n$ by $(-1)^n$ all keep $|r[k]|$, so they map Barker sequences to Barker sequences.

**The known codes.** Up to these operations:

| $N$ | Code | $r[0], r[1], \dots, r[N-1]$ | Peak sidelobe | Merit factor |
|---|---|---|---|---|
| 2 | $+ -$ | $2, -1$ | $-6.02$ dB | |
| 3 | $+ + -$ | $3, 0, -1$ | $-9.54$ dB | 4.5 |
| 4 | $+ + - +$ | $4, -1, 0, 1$ | $-12.04$ dB | 4.0 |
| 4 | $+ + + -$ | $4, 1, 0, -1$ | $-12.04$ dB | 4.0 |
| 5 | $+ + + - +$ | $5, 0, 1, 0, 1$ | $-13.98$ dB | 6.25 |
| 7 | $+ + + - - + -$ | $7, 0, -1, 0, -1, 0, -1$ | $-16.90$ dB | 8.17 |
| 11 | $+ + + - - - + - - + -$ | $11, 0, -1, 0, -1, \dots, -1$ | $-20.83$ dB | 12.1 |
| 13 | $+ + + + + - - + + - + - +$ | $13, 0, 1, 0, 1, \dots, 1$ | $-22.28$ dB | 14.08 |

The merit factor is $N^2 / (2\sum_{k \ge 1} r[k]^2)$. The value 14.08 of the code of length 13 is the largest known for any binary sequence. An exhaustive search over all $2^N$ sequences of each length $N \le 16$ finds 4 Barker sequences of each length 2, 3, 5, 7, 11 and 13, 8 of length 4, and none of the other lengths.

**Which lengths exist (theorems).** Turyn and Storer proved in 1961 that no Barker sequence of odd length above 13 exists. A Barker sequence of even length $N > 4$ must have $N = 4u^2$ for an odd $u$, and number theoretic conditions on $u$, checked by computer, rule out every such length up to $4 \times 10^{33}$. It is conjectured, but not proved, that no Barker sequence longer than 13 exists.

## Examples and non-examples

**Barker 13 in a radar.** Thirteen chips of 1 µs with phases 0 and π form a pulse of 13 µs with a bandwidth of about 1 MHz. The matched filter output has a peak of 13, sidelobes of magnitude 1 at $-22.28$ dB, a range resolution of about $c t_c/2 = 149.9$ m, and a compression ratio of 13.

**Doppler.** A Doppler shift $\nu$ turns the phase by $2\pi\nu T$ across the pulse. Computed with one sample per chip, the code of length 13 keeps a peak of 0.90 and a peak sidelobe of $-10.63$ dB below it at $\nu T = 0.25$, and a peak of 0.64 with sidelobes only $2.99$ dB lower at $\nu T = 0.5$. Barker codes are for targets with $\nu T$ well below $1/4$.

**Periodic use.** Repeated without gaps, the code of length 13 has the periodic autocorrelation $13, 1, 1, \dots, 1$. Its periodic sidelobes are all 1, which is not as good as the $-1$ of a [maximal length sequence](/maximal-length-sequence/) of length $2^m - 1$.

**Compound Barker codes.** The [Kronecker product](/kronecker-product/) of two Barker codes, each chip of one code replaced by the whole other code with its sign, is a longer binary code. The product of the codes of length 13 and 13 has 169 chips and a peak sidelobe of 13, the same $-22.28$ dB as the code of length 13. The product of the codes of lengths 5 and 13 has 65 chips and a peak sidelobe of 13, which is $-13.98$ dB. Compound codes give more energy and more compression, not lower sidelobes.

**Non-example: a maximal length sequence of length 15.** It is binary and has ideal periodic autocorrelation, but its aperiodic peak sidelobe is 3 at best over its cyclic shifts, so it is not a Barker sequence.

**Non-example: polyphase codes.** A sequence of complex numbers of magnitude 1 with sidelobes at most 1 is a generalized or polyphase Barker sequence. Such sequences exist for many lengths above 13, but they are not binary.

**Non-example: a length of 6.** No binary sequence of length 6 is a Barker sequence. Every sequence of length 6 has some $|r[k]| \ge 2$.

## Related definitions

- **Phase-coded waveform.** The Barker code is the best known binary [phase-coded waveform](/phase-coded-waveform/) for short pulses.
- **Mismatched filter.** A [mismatched filter](/mismatched-filter-design/) of 39 taps lowers the sidelobes of the code of length 13 from $-22.28$ dB to $-38.47$ dB at a loss of 0.204 dB.
- **Spread spectrum.** The code of length 11 is the spreading code of the 1 and 2 Mbit/s rates of IEEE 802.11 [direct sequence spread spectrum](/direct-sequence-spread-spectrum/), where its low sidelobes help symbol timing.
- **Frank code.** The [Frank code](/frank-code/) reaches lower peak sidelobes at lengths of 16 and more, with more than two phases.
- **Costas array.** A [Costas array](/costas-array/) is the frequency hopping analog: a permutation whose two-dimensional autocorrelation has sidelobes of at most 1.

## References
