---
tag: T1E2A7
kind: algorithm
slug: tomlinson-harashima-precoding
name: Tomlinson-Harashima precoding
aliases:
- THP
area: communications/channel-estimation-and-equalization
level: core
summary: Moves the feedback filter of a DFE to the transmitter and keeps the signal bounded with a modulo operation.
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {L: the number of channel taps, K: the number of symbols}
  time: {worst: O(K L)}
  space: {extra: O(L)}
properties: {deterministic: true, linear: false, needs_channel_at_transmitter: true, error_propagation: false, power_loss_db_4pam: 0.280}
history:
  year: 1971
  people: [M. Tomlinson, H. Harashima, H. Miyakawa]
  note: "Tomlinson described an equaliser with modulo arithmetic in 1971. Harashima and Miyakawa proposed the same matched-transmission technique for ISI channels in 1972."
prereqs: [decision-feedback-equalizer, pulse-amplitude-modulation, intersymbol-interference]
see_also: [mmse-dfe-canonical-theorem, dirty-paper-coding, vector-perturbation-precoding, zero-forcing-precoding, discrete-multitone, partial-response-signaling, faster-than-nyquist-signaling, quadrature-amplitude-modulation]
sources:
  - paper: "M. Tomlinson, New automatic equaliser employing modulo arithmetic, Electronics Letters 7(5-6), 1971, pages 138 to 139"
    locator: "the precoder with modulo arithmetic"
  - paper: "H. Harashima and H. Miyakawa, Matched-transmission technique for channels with intersymbol interference, IEEE Transactions on Communications 20(4), 1972, pages 774 to 780"
    locator: "the precoder at the transmitter and the modulo receiver"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 9.5-4 (equalization at the transmitter)"
  - paper: "John M. Cioffi, Glen P. Dudevoir, M. Vedat Eyuboglu and G. David Forney, Jr., MMSE decision-feedback equalizers and coding, Part II: Coding results, IEEE Transactions on Communications 43(10), 1995, pages 2595 to 2604"
    locator: "precoding with the MMSE-DFE and coding"
---

Tomlinson-Harashima precoding (THP) moves the feedback filter of a [decision feedback equalizer](/decision-feedback-equalizer/) from the receiver to the transmitter. The transmitter knows the symbols it sends, so it can subtract their echoes in advance, before the channel adds them. There are no wrong decisions and no error propagation. Subtracting echoes in advance would make the signal grow without bound on many channels, so a modulo operation folds each sample back into $[-M, M)$. The receiver applies the same modulo and then slices, with no feedback. The cost is a small increase of the transmit power, a factor $M^2/(M^2-1)$, which is 0.280 dB for 4-PAM. THP needs the channel at the transmitter, which the DFE does not. The [MMSE-DFE canonical theorem](/mmse-dfe-canonical-theorem/) is the reason to want the feedback at the transmitter: a channel code then works as on an ISI-free channel. On a matrix channel, the same idea is a form of [dirty paper coding](/dirty-paper-coding/) and is close to [vector perturbation precoding](/vector-perturbation-precoding/).

## In plain words

A DFE subtracts the echoes of the symbols it has already decided. If it decides wrong, it subtracts the wrong echo. The transmitter never decides wrong: it knows exactly what it sent. So it can send each symbol minus the echoes that the channel will add. The channel then adds the echoes back, and the receiver sees the clean symbol. The problem is that this subtraction can make the transmitted values large. The fix is to fold every value back into a fixed range, like the hand of a clock. The receiver folds what it gets in the same way, and the clean symbol appears.

## The problem

The input is a channel $h = (h_0, \ldots, h_{L-1})$ with $h_0 \ne 0$, known at the transmitter, and symbols $a[k]$ from M-PAM with the points $M-1-2i$, $i = 0, \ldots, M-1$, or from square $M^2$-QAM with M-PAM on each real dimension. The receiver gets $y[k] = \sum_l h_l\, x[k-l] + w[k]$, where $x$ is what the transmitter sends. The output is a transmitted sequence $x$ with bounded samples, and a receiver rule that recovers $a$ without a feedback loop. In a full system, $h$ is the cascade of the channel and the feedforward filter of an MMSE-DFE or a [whitened matched filter](/whitened-matched-filter/), which makes the channel causal with a strong first tap.

## The algorithm

The modulo $\mathrm{MOD}(v) = v - 2M \lfloor (v + M)/(2M) \rfloor$ maps a real number into $[-M, M)$; for a complex number it acts on the real and the imaginary parts.

```pseudo id=main
THP(a, h, M)                                      ▷ the transmitter
L1  g ← h / h[0]                                  ▷ the monic channel
L2  for k ← 0 to K - 1
L3      v ← Σ_{j=1}^{L-1} g[j] x[k - j]            ▷ the echo of the past samples
L4      x[k] ← MOD(a[k] - v)
L5  return x
THP-RECEIVE(y, h0, M)                             ▷ the receiver
L6  for k ← 0 to K - 1
L7      u ← y[k] / h0
L8      â[k] ← the PAM point nearest to MOD(u), on the circle of length 2M
L9  return â
```

Line L3 is the feedback filter of a ZF-DFE, run on the transmitted samples instead of the decisions. Line L4 subtracts the echo and folds the result. Lines L7 and L8 are the whole receiver. On the circle of length $2M$, the $M$ points are equally spaced, so the point $M-1$ and the point $-(M-1)$ are neighbours.

## Example

Take 4-PAM, so $M = 4$, the points are $\pm 1, \pm 3$ and the modulo maps into $[-4, 4)$. The channel is $h = (1, 0.5)$, with no noise.

| $k$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $a[k]$ | 3 | -3 | -3 | 3 | 3 |
| $a[k] - 0.5\, x[k-1]$ | 3 | -4.5 | -4.75 | 1.375 | 2.3125 |
| $x[k]$ | 3 | 3.5 | 3.25 | 1.375 | 2.3125 |
| $y[k] = x[k] + 0.5\, x[k-1]$ | 3 | 5 | 5 | 3 | 3 |
| $\mathrm{MOD}(y[k])$ | 3 | -3 | -3 | 3 | 3 |

At $k = 1$ the value $-4.5$ is below $-4$, so the transmitter adds 8 and sends 3.5. The channel output 5 is outside the alphabet, and the receiver folds it back to $-3$, the right symbol. Without the modulo, the transmitter would send $1/(1 + 0.5 z^{-1})$ applied to $a$, which stays bounded here but grows without bound on a channel with a zero outside the unit circle.

The transmit power was measured over 40000 random 4-PAM symbols (seed 7303). On $(1, 0.5)$ it is 5.328, close to the uniform value $16/3 = 5.333$, against 5 for 4-PAM itself: a loss of $10 \log_{10}(16/15) = 0.280$ dB. On the weak channel $(1, 0.1)$ the samples are not uniform and the power is 5.059. With Gaussian noise of standard deviation $\sigma = 0.4$ on $(1, 0.5)$, the symbol error rate of the modulo receiver is 0.01242 by the exact formula; 20000 symbols (seed 7304) gave 230 errors, 0.0115. A 4-PAM receiver on an ISI-free channel would have $2(1 - 1/4)\, Q(2.5) = 0.00931$, because its outer points have one neighbour each.

## Correctness

**Claim.** The samples $x[k]$ are in $[-M, M)$ on each dimension for every channel, and $y[k]/h_0 = a[k] + 2M d[k] + w[k]/h_0$ for some integer $d[k]$ on each dimension. So without noise the receiver returns $a$, and with noise it makes the same decisions as a zero-forcing DFE with correct feedback and an alphabet extended periodically by $2M$.

**Key step.** The modulo changes its input by a multiple of $2M$, so $x[k] + v[k] = a[k] + 2M d[k]$. The channel adds $v[k]$ back, because $y[k]/h_0 = x[k] + \sum_{j \ge 1} g_j x[k-j] + w[k]/h_0$. The modulo at the receiver removes $2M d[k]$, since the modulo of $v$ depends only on $v$ up to multiples of $2M$. The error rate on one dimension is then $1 - \sum_i [\Phi((2Mi+1)/\sigma) - \Phi((2Mi-1)/\sigma)]$, which is about $2Q(1/\sigma)$ for every point. The proofs folder has the details.

## Complexity

The precoder costs $L - 1$ complex multiplications and one modulo per symbol, so $K$ symbols cost $O(KL)$ in the [real RAM](/real-ram/), with $O(L)$ extra space for the past samples. The receiver costs $O(1)$ per symbol. The receiver has no feedback loop, so it can work at a higher rate than a DFE, whose next decision waits for the current one.

## Properties

- **No error propagation.** The receiver decides each symbol on its own, so one noise event causes one symbol error.
- **Bounded transmit signal.** Every sample is in $[-M, M)$, for every channel with $h_0 \ne 0$, also when $1/H(z)$ is unstable.
- **Power loss.** If the precoded samples are uniform on $[-M, M)$, the power is $M^2/3$ per dimension, a factor $M^2/(M^2 - 1)$ over M-PAM: 1.249 dB for 2-PAM, 0.280 dB for 4-PAM and 0.07 dB for 8-PAM. This is a heuristic; it holds closely on dispersive channels, by measurement.
- **Modulo loss.** The outer points get a second neighbour, so the error rate rises from $2(1 - 1/M)\, Q$ to about $2Q$. This is small for large $M$.
- **Needs the channel at the transmitter.** A wrong channel at the transmitter leaves residual ISI that the receiver cannot remove. The precoder needs feedback from the receiver.
- **Coding works.** The receiver output is the symbol plus noise modulo $2M$, with no dependence on past decisions, so a channel code and soft decoding work as on an ISI-free channel.

## Variants and improvements

- **MMSE-THP.** Use the feedback filter of the MMSE-DFE instead of the ZF-DFE, with the MMSE feedforward filter at the receiver. This is the usual design, because it keeps the gain of the MMSE-DFE.
- **Complex and lattice versions.** For square QAM the modulo acts on each real dimension. Other lattices and shapes give more general modulo precoders.
- **Flexible precoding and trellis precoding.** Other precoders for the voiceband modem standards combine the feedback with trellis shaping to remove most of the power loss.
- **MIMO and multiuser THP.** On a matrix channel, a QR or LQ factorization gives a triangular channel, and THP runs across the users or the antennas. It is a practical form of [dirty paper coding](/dirty-paper-coding/), and [vector perturbation precoding](/vector-perturbation-precoding/) chooses the modulo offsets jointly instead of one at a time.

## When to use it

Use THP when the transmitter knows the channel, the channel changes slowly enough for the receiver to report it, and the receiver must decode with a channel code at full gain. It was used in voiceband modems and in DSL, and it is used in multiuser downlinks. On a fast-changing channel, or when the channel cannot be fed back, use a DFE or a [Viterbi equalizer](/viterbi-equalizer/) at the receiver.

## Pitfalls

- **Forgetting the modulo at the receiver.** The received values lie far outside the alphabet; a plain slicer clips them to the outer points.
- **The modulo interval.** The points of M-PAM at spacing 2 need the interval $[-M, M)$ of length $2M$. A length of $2(M-1)$ folds the outer points onto each other.
- **A gain error.** The receiver must divide by $h_0$ exactly. A small gain error moves the folded values, and the effect is worst near the edges of $[-M, M)$, where the modulo wraps.
- **Channel mismatch.** The precoder subtracts the echoes of the channel it was told. A stale channel leaves ISI, and the modulo can turn a small ISI into a jump of $2M$ near the edges.
- **Counting the power.** Compare THP with a DFE at the same transmit power, not at the same symbol energy, to include the power loss.

## Implementations

## History

Tomlinson described an automatic equaliser with modulo arithmetic in Electronics Letters in 1971. Harashima and Miyakawa proposed the same structure, which they called matched transmission, for channels with intersymbol interference in 1972. The technique was little used at first, because it needs the channel at the transmitter. It became practical in voiceband modems, where the receiver sends the channel back at startup, and the analysis of the MMSE-DFE with coding by Cioffi, Dudevoir, Eyuboglu and Forney in 1995 explained why precoding is the right partner for a channel code. THP later spread to DSL and to multiuser MIMO downlinks.

## References
