---
tag: MRC17X
kind: algorithm
slug: rake-receiver
name: Rake receiver
aliases:
- RAKE combiner
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "Despreads each resolvable path of a spread-spectrum signal at its own delay, weights each finger output by the conjugate path gain and adds. It is the matched filter to the multipath pulse."
solves: [symbol-detection]
model: real-ram
complexity:
  vars: {L: the number of fingers, N: the number of chips per symbol}
  time: {worst: Θ(L N)}
  space: {extra: Θ(1)}
properties: {deterministic: true, needs_channel_estimate: true, maximal_ratio_weights: true, exact_ml_with_cyclic_prefix: true}
history:
  year: 1958
  people: [Robert Price, Paul E. Green Jr.]
  note: Price and Green described the Rake system in 1958 for a wideband HF link over multipath channels, with a tapped delay line that measured and combined the paths.
prereqs: [direct-sequence-spread-spectrum, matched-filter, autocorrelation, maximal-length-sequence]
see_also: [maximal-ratio-combining, tapped-delay-line-channel-model, delay-spread, multipath-fading, diversity-order, code-division-multiple-access, ovsf-codes, orthogonal-frequency-division-multiplexing]
sources:
  - paper: doi:10.1109/JRPROC.1958.286870
    title: R. Price and P. E. Green, Jr., A communication technique for multipath channels, Proceedings of the IRE 46(3), 1958
    locator: pp. 555 to 570 (the Rake system, its tapped delay line and the weighting of the paths by their measured gains)
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, 5th edition, McGraw-Hill, 2008
    locator: The chapter on fading channels (the RAKE demodulator for frequency-selective channels and its error probability)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: The chapter on diversity (frequency diversity, direct-sequence spread spectrum and the rake receiver)
  - book: isbn:9780201633740
    title: Andrew J. Viterbi, CDMA, Principles of Spread Spectrum Communication, Addison-Wesley, 1995
    locator: The material on multipath diversity reception in a direct-sequence CDMA receiver
---

A rake receiver demodulates a [direct-sequence spread-spectrum](/direct-sequence-spread-spectrum/) signal that arrives over several paths with different delays. Each path that is more than about one chip away from the others can be separated by despreading at its own delay. The receiver has one **finger** for each such path: the finger correlates the received chips with the code shifted by the path delay. A combiner then multiplies each finger output by the conjugate of the path gain and adds them. The result is the [matched filter](/matched-filter/) to the whole received pulse, so the receiver collects the energy of all paths instead of treating the late paths as interference. This is the multipath counterpart of [maximal ratio combining](/maximal-ratio-combining/): MRC combines antennas, and the rake combines delays. Price and Green described it in 1958.

## In plain words

A radio signal bounces off buildings and hills, so the receiver hears several copies of it, each a little late and each with its own strength.

A spread-spectrum signal is a long pattern of fast pulses. If the receiver lines up its copy of the pattern with one echo, it hears that echo clearly and the other echoes mostly cancel out, because the pattern does not match itself at other timings.

So the receiver uses several "fingers", one for each strong echo, each lined up with its own echo. Each finger gives a value. The receiver turns each value so that all of them point the same way, gives more weight to the strong echoes and less to the weak ones, and adds them up. The echoes, which would otherwise be a nuisance, now all help.

## The problem

One symbol $b$ is sent with a code $c \in \mathbb{C}^N$ of $N$ chips and unit energy, $\sum_n |c[n]|^2 = 1$. The channel has $L$ resolvable paths with known integer delays $d_1, \ldots, d_L$ (in chips) and known complex gains $h_1, \ldots, h_L$. With a cyclic prefix, so that there is no interference from the previous symbol, the received block is

$$r[n] = \sqrt{E_s}\, b \sum_{l=1}^{L} h_l\, c[(n - d_l) \bmod N] + w[n], \qquad n = 0, \ldots, N - 1,$$

with independent noise $w[n] \sim \mathcal{CN}(0, N_0)$. The task is to form the statistic for detecting $b$ that keeps all the information in $r$ about $b$, and to decide $b$. On a real link the delays and gains come from a channel estimate, for example from a pilot channel, and a searcher picks the delays with the most energy.

## The algorithm

```pseudo id=main
RAKE(r, c, (d_1, h_1), …, (d_L, h_L))
L1  y ← 0
L2  for l ← 1 to L do
L3      z_l ← Σ_{n=0}^{N-1} conj(c[(n - d_l) mod N]) · r[n]     ▷ finger l: despread at delay d_l
L4      y ← y + conj(h_l) · z_l                                ▷ maximal ratio weight
L5  return y                                                  ▷ for BPSK, decide b̂ = sign(Re y)
```

Write $T^d c$ for the code delayed by $d$ chips. Each finger output is $z_l = \sqrt{E_s}\, b \sum_m R_{lm} h_m + u_l$, where $R_{lm} = \langle T^{d_l} c, T^{d_m} c\rangle$ is the periodic [autocorrelation](/autocorrelation/) of the code at the shift $d_m - d_l$. A good spreading code has $R_{ll} = 1$ and $|R_{lm}|$ small for $l \ne m$, so each finger sees mainly its own path. The output is

$$y = \langle g, r\rangle, \qquad g = \sum_l h_l\, T^{d_l} c,$$

the correlation of $r$ with the received pulse $g$. Its signal part is $\sqrt{E_s}\, b\, \|g\|^2$ with $\|g\|^2 = h^H R h$, and for BPSK the error probability is $Q(\sqrt{2 E_s\, h^H R h / N_0})$.

## Example

Take the m-sequence code $1001011$ of length $N = 7$, as chips $(-1, 1, 1, -1, 1, -1, -1)/\sqrt 7$. Its periodic autocorrelation is $1$ at shift $0$ and $-1/7$ elsewhere. The channel has two paths at delays $0$ and $2$ with gains $h = (0.8, 0.6)$, and $b = +1$, $E_s = 1$, no noise.

- The received chips, times $\sqrt 7$, are $(-1.4, 0.2, 0.2, -0.2, 1.4, -1.4, -0.2)$.
- Finger 1 (delay 0) gives $z_1 = 0.8 + 0.6 \cdot (-1/7) = 0.7143$.
- Finger 2 (delay 2) gives $z_2 = 0.6 + 0.8 \cdot (-1/7) = 0.4857$.
- The combiner gives $y = 0.8 \cdot 0.7143 + 0.6 \cdot 0.4857 = 0.8629$, which is $h^H R h = 1 - 0.96/7$.

With noise at $E_s/N_0 = 6$ dB, the rake gives $P_b = 0.0044$. A single finger on the strong path has output SNR $(0.8 - 0.6/7)^2 = 0.5102$ times $E_s/N_0$ and $P_b = 0.0219$, five times worse.

If the second path has the gain $0.6j$ instead, the cross terms are imaginary and drop out of $h^H R h$, which becomes $|0.8|^2 + |0.6|^2 = 1$. The rake then gives $P_b = 0.0024$, the same as a single path of unit energy, and the single finger gives $0.0116$.

## Correctness

The loop computes $y = \sum_l \overline{h_l}\, z_l$, and since the inner product is conjugate-linear in its first argument this equals $\langle g, r\rangle$. Expanding $\|r - \sqrt{E_s} b g\|^2$ shows that the Gaussian likelihood depends on $r$ only through $\langle g, r\rangle$, so $y$ is a sufficient statistic, and for BPSK the sign of $\operatorname{Re} y$ is the maximum likelihood decision. The noise in $y$ is $\mathcal{CN}(0, N_0 \|g\|^2)$, which gives $P_b = Q(\sqrt{2 E_s \|g\|^2/N_0})$. For any other weights $a$, the output SNR is $E_s |a^H R h|^2 / (N_0\, a^H R a)$, and the Cauchy-Schwarz inequality in the inner product defined by $R$ shows that $a = h$ is best. The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/) model, each finger does $N$ complex multiply-adds (L3) and one more (L4). The total is $\Theta(L N)$ per symbol, with $\Theta(1)$ extra space. A matched filter to $g$ also costs $\Theta(N)$ per symbol once $g$ is built, but $g$ costs $\Theta(L N)$ to form and changes whenever the channel changes. The fingers need only the code, the delays and the gains.

## Properties

- **Matched filter to the multipath pulse.** The rake output equals $\langle g, r \rangle$ exactly, so it is optimal for one symbol when there is no interference between symbols.
- **Maximal ratio weights.** Weighting finger $l$ by $\overline{h_l}$ maximizes the output SNR over all linear combinations of the finger outputs.
- **Orthogonal codes give MRC.** If the shifted codes are orthogonal ($R = I$), the output SNR is $\sum_l |h_l|^2 E_s/N_0$, the same as maximal ratio combining of $L$ antennas. With independent Rayleigh paths this gives a [diversity order](/diversity-order/) of $L$.
- **Cross terms.** With a real code, the term $2 \operatorname{Re}(\overline{h_l} h_m R_{lm})$ can raise or lower the energy, depending on the phases of the paths. It goes to zero as $N$ grows for an m-sequence, since $R_{lm} = -1/N$.
- **Needs the channel.** The weights need the gains and the delays. Errors in them lower the SNR but do not change the structure of the receiver.

## Variants and improvements

- **Selective and partial rake.** Use only the $L' < L$ strongest paths, or the first $L'$ paths, to save hardware. The loss is the energy of the unused paths.
- **Equal gain combining.** Co-phase the fingers but give them equal weights. It needs only the phases, not the amplitudes.
- **Generalized rake (G-RAKE).** In interference-limited links, weight the fingers by $R_u^{-1} h$, where $R_u$ is the covariance of interference plus noise across fingers, and place extra fingers at delays with no path. It whitens colored interference.
- **Chip-level equalization.** In the WCDMA downlink, a linear equalizer before despreading restores the orthogonality of the [OVSF codes](/ovsf-codes/) that multipath destroys. The rake does not restore it.
- **Rake with soft handover.** Fingers can be assigned to paths from different base stations that send the same data, so the rake also combines across cells.

## When to use it

Use a rake receiver for direct-sequence signals whose [delay spread](/delay-spread/) is larger than a chip, so that several paths are resolvable, and whose spreading factor is large enough that the code keeps the fingers apart. This was the case for IS-95 and WCDMA. When the delay spread covers many chips and the spreading factor is small, the interference between symbols and between paths grows, and an equalizer or [OFDM](/orthogonal-frequency-division-multiplexing/) with a cyclic prefix is the better choice.

## Pitfalls

- **Paths closer than one chip.** Two paths less than about one chip apart cannot be separated by despreading. A single finger then sees their sum, which fades like one Rayleigh path; see [multipath fading](/multipath-fading/).
- **Ignoring the cross terms.** For short codes, $R_{lm}$ is not small, and the SNR is $h^H R h$, not $\sum_l |h_l|^2$. Formulas that assume orthogonal paths are then wrong by a visible amount: $0.8629$ against $1$ in the example.
- **Intersymbol interference.** Without a cyclic prefix, a path with delay $d$ brings $d$ chips of the previous symbol into the window. For long spreading codes this acts like noise; for short codes and a large delay spread it does not, and the error rate is worse than the formula.
- **Stale channel estimates.** On a fast fading channel, weights from old estimates can add the paths with the wrong phases. Track the gains at least as fast as the [coherence time](/coherence-time/) of the channel.
- **Finger management.** Paths appear and disappear. A searcher must keep looking for new delays, or the fingers end up on weak paths.

## Implementations

## History

Robert Price and Paul Green Jr. described the Rake system in the Proceedings of the IRE in 1958. It sent wideband signals over a multipath HF channel and used a tapped delay line to measure the channel and to weight and add the paths; the name refers to the taps of the delay line, which look like the teeth of a garden rake. With the cellular CDMA systems of the 1990s, IS-95 and later WCDMA, the rake receiver became the standard receiver for direct-sequence signals in mobile phones and base stations.

## References
