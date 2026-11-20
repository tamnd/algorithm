---
tag: 04NE33
kind: algorithm
slug: alamouti-code
name: Alamouti code
aliases:
- Alamouti scheme
area: communications/mimo-communications
level: core
summary: A space-time block code for two transmit antennas that gets full diversity at full rate with simple linear decoding.
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {m: the number of receive antennas, M: the number of constellation points}
  time: {worst: Θ(m + M)}
  time_with_slicer: {worst: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact_ml: true, needs_csit: false, rate_symbols_per_slot: 1, diversity_order: 2m}
history:
  year: 1998
  people: [Siavash M. Alamouti]
  note: "Alamouti published the two-antenna scheme in the IEEE Journal on Selected Areas in Communications in October 1998. Tarokh, Jafarkhani and Calderbank generalized it to orthogonal designs for more antennas in 1999."
prereqs: [mimo-channel-model, maximal-ratio-combining, diversity-order]
see_also: [orthogonal-space-time-block-codes, rank-and-determinant-criteria, golden-code, space-time-trellis-codes, maximum-ratio-transmission, diversity-multiplexing-tradeoff, minimum-distance-detector, rayleigh-fading-channel]
sources:
  - paper: doi:10.1109/49.730453
    title: "Siavash M. Alamouti, A simple transmit diversity technique for wireless communications, IEEE Journal on Selected Areas in Communications 16(8), 1451-1458, 1998"
    locator: "the whole paper (the two-branch transmit scheme with one receiver, its extension to M receivers and the comparison with maximal ratio combining)"
  - paper: doi:10.1109/18.771146
    title: "Vahid Tarokh, Hamid Jafarkhani and A. Robert Calderbank, Space-time block codes from orthogonal designs, IEEE Transactions on Information Theory 45(5), 1456-1467, 1999"
    locator: "the definition of orthogonal designs and the linear maximum likelihood decoder, of which the Alamouti code is the 2 by 2 complex case"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 3.3.2, Transmit diversity - space-time codes (the Alamouti scheme and the determinant criterion)"
  - book: isbn:9780521826150
    title: "Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003"
    locator: "Chapter 5, Spatial diversity, and Chapter 6, Space-time coding without channel knowledge at the transmitter"
---

The Alamouti code sends two symbols from two transmit antennas over two time slots, with the second slot a conjugated and swapped copy of the first. The receiver needs no joint search: a linear combiner separates the two symbols, and each one sees a channel with the sum of all $2m$ channel gains, the same as [maximal ratio combining](/maximal-ratio-combining/) over $2m$ branches with half the power on each. So the code reaches the full [diversity order](/diversity-order/) $2m$ with $m$ receive antennas at a rate of one symbol per slot, and the transmitter needs no channel knowledge. The Alamouti code is the 2 by 2 case of the [orthogonal space-time block codes](/orthogonal-space-time-block-codes/); OSTBCs for more antennas keep the linear decoder but lose rate. The [rank and determinant criteria](/rank-and-determinant-criteria/) explain why the code has full diversity. [Space-time trellis codes](/space-time-trellis-codes/) add coding gain at the cost of a trellis search, and the [golden code](/golden-code/) sends two symbols per slot on a 2 by 2 channel at the cost of a joint decoder.

## In plain words

A base station has two antennas, and a phone has one. If the phone sits in a deep fade from one antenna, the other antenna may still reach it well. The Alamouti code makes use of both paths without the base station knowing which one is good.

In the first time slot, the two antennas send two different symbols. In the second slot, they send the same two symbols again, but swapped, with one sign flipped and both mirrored. The phone receives two mixed values. It adds and subtracts them with weights from the channel, and the mixing cancels exactly: one output holds only the first symbol and the other holds only the second. Each symbol arrives as strong as the two paths together. The phone then picks the nearest point for each symbol, one at a time.

## The problem

The channel has two transmit antennas and $m$ receive antennas. The gain $h_{ik}$ from transmit antenna $k$ to receive antenna $i$ is known at the receiver and stays fixed for two symbol periods. The transmitter sends the codeword

$$X = \begin{pmatrix} s_1 & -s_2^* \\ s_2 & s_1^* \end{pmatrix},$$

where row $k$ is antenna $k$ and column $t$ is slot $t$, and $s_1, s_2$ are points of a constellation $\mathcal{A}$ of $M$ points. Receive antenna $i$ sees

$$y_{i1} = h_{i1} s_1 + h_{i2} s_2 + w_{i1}, \qquad y_{i2} = -h_{i1} s_2^* + h_{i2} s_1^* + w_{i2},$$

with independent noise samples $w \sim \mathcal{CN}(0, N_0)$. When the total symbol energy $E_s$ is split over the two antennas, each antenna sends with amplitude $\sqrt{E_s/2}$, and this factor is part of the $h_{ik}$ below. The output is a maximum likelihood decision on the pair $(s_1, s_2)$.

## The algorithm

```pseudo id=main
ALAMOUTI-ENCODE(s1, s2)                 ▷ rows are antennas, columns are slots
L1  row 1 ← (s1, -conj(s2))
L2  row 2 ← (s2, conj(s1))

ALAMOUTI-DECODE(y, h, A)               ▷ y[i] = (y_i1, y_i2), h[i] = (h_i1, h_i2), i = 1..m
L3  g ← Σ_i (|h_i1|² + |h_i2|²)
L4  z1 ← Σ_i (conj(h_i1) y_i1 + h_i2 conj(y_i2))
L5  z2 ← Σ_i (conj(h_i2) y_i1 - h_i1 conj(y_i2))
L6  u1 ← z1 / g ;  u2 ← z2 / g
L7  return (nearest point of A to u1, nearest point of A to u2)
```

Lines L4 and L5 are the matched filter of the equivalent channel: after the second slot is conjugated, the two symbols see orthogonal columns of equal norm. So $z_k = g s_k + n_k$ with $n_1, n_2$ independent $\mathcal{CN}(0, g N_0)$. Line L7 can use the slicer of the [minimum distance detector](/minimum-distance-detector/) for PAM, square QAM or PSK.

## Example

**One receive antenna, QPSK.** Take $h_{11} = 0.6 + 0.8j$, $h_{12} = -1 + 0.5j$, $s_1 = (1 + j)/\sqrt2$ and $s_2 = (-1 + j)/\sqrt2$. The noise samples are $w_{11} = 0.1 - 0.2j$ and $w_{12} = -0.15 + 0.05j$.

| quantity | value |
|---|---|
| $y_{11}$ | $0.3121 - 0.2707j$ |
| $y_{12}$ | $-0.6450 + 2.1006j$ |
| $g$ (line L3) | $0.36 + 0.64 + 1 + 0.25 = 2.25$ |
| $z_1$ (line L4) | $1.6660 + 1.3660j$ |
| $z_2$ (line L5) | $-1.7410 + 1.8910j$ |
| $u_1$, $u_2$ (line L6) | $0.7404 + 0.6071j$, $-0.7738 + 0.8404j$ |

The noise parts of $z_1$ and $z_2$ are $h_{11}^* w_{11} + h_{12} w_{12}^* = 0.075 - 0.225j$ and $h_{12}^* w_{11} - h_{11} w_{12}^* = -0.15 + 0.3j$; there is no trace of the other symbol. Line L7 returns $(1 + j)/\sqrt2$ at squared distance $0.0111$ from $u_1$, and $(-1 + j)/\sqrt2$ at squared distance $0.0222$ from $u_2$. Both decisions are correct.

**Error rate.** With BPSK, one receive antenna, i.i.d. Rayleigh gains and a total $E_s/N_0$ of 10 dB, the bit error rate of the Alamouti code is that of maximal ratio combining over two branches at 5 (7 dB) each: $0.0055282$. One antenna at 10 dB gives $0.023269$, and one transmitter with two receive antennas at 10 dB gives $0.0015991$. The 3 dB gap to receive combining is the price of splitting the power without channel knowledge (closed forms, Rayleigh fading).

## Correctness

The decoder returns a maximum likelihood decision of the pair. Conjugate the second slot of each receive antenna, and the block becomes $\tilde y = G s + \tilde w$ with a $2m \times 2$ matrix $G$ that satisfies $G^H G = g I$. Lines L4 and L5 compute $z = G^H \tilde y = g s + G^H \tilde w$, and the noise $G^H \tilde w$ has the covariance $g N_0 I$. Expanding $\|\tilde y - G s\|^2$ gives a constant plus $g \sum_k |s_k - z_k/g|^2$, a sum of one term for each symbol, so the joint minimum over $\mathcal{A}^2$ is the pair of separate minima of line L7. A Chernoff bound on each symbol, averaged over $2m$ i.i.d. Rayleigh gains, gives the diversity order $2m$. The full proof is below.

## Complexity

Lines L3 to L5 each sum $m$ terms, so the combiner costs $\Theta(m)$ complex operations per block of two symbols. Line L7 costs $\Theta(M)$ with a brute force search and $\Theta(1)$ with a slicer. Joint maximum likelihood detection of a general 2 by 2 code costs $\Theta(m M^2)$ by brute force, so the orthogonal structure removes a factor of $M$. The extra space is $\Theta(1)$.

## Properties

- **Rate one.** Two symbols in two slots, the highest rate of any complex orthogonal design.
- **Full diversity.** The difference of two distinct codewords is $\Delta = \begin{pmatrix} e_1 & -e_2^* \\ e_2 & e_1^* \end{pmatrix}$ with $\Delta \Delta^H = (|e_1|^2 + |e_2|^2) I$, so it has rank 2 for every pair; see the [rank and determinant criteria](/rank-and-determinant-criteria/).
- **No channel knowledge at the transmitter.** Compare [maximum ratio transmission](/maximum-ratio-transmission/), which needs the channel at the transmitter and has a 3 dB array gain over the Alamouti code with one receive antenna.
- **Not capacity achieving for two or more receive antennas.** With $m \ge 2$, the code sends one symbol per slot, while the 2 by $m$ channel supports two streams; its tradeoff curve on the 2 by 2 channel is $4(1 - r)$, below the optimal [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/) for $r > 0$. With $m = 1$ and Gaussian symbols, it reaches the capacity of the 2 by 1 channel with CSIR (a theorem): each symbol sees the SNR $(\rho/2)(|h_{11}|^2 + |h_{12}|^2)$, and $\log_2$ of one plus this SNR is the 2 by 1 capacity with equal power.
- **Unit-modulus not needed.** The decoupling holds for any complex symbols, including QAM.

## Variants and improvements

- **Space-frequency block coding.** In [OFDM](/orthogonal-frequency-division-multiplexing/), the two columns go on two adjacent subcarriers instead of two slots. The channel must then be flat over the two subcarriers.
- **Orthogonal designs for more antennas.** For three or four antennas, the rate drops to $3/4$; see [orthogonal space-time block codes](/orthogonal-space-time-block-codes/).
- **Differential Alamouti.** Tarokh and Jafarkhani built a differential version that needs no channel estimate. As for other differential schemes, it loses about 3 dB against coherent detection.
- **Quasi-orthogonal codes.** Jafarkhani's quasi-orthogonal codes reach rate one for four antennas by giving up full orthogonality, so pairs of symbols must be decoded jointly.
- **Full-rate codes.** For two receive antennas, the [golden code](/golden-code/) sends four symbols in two slots with full diversity and a nonvanishing determinant.

## When to use it

Use the Alamouti code when a transmitter has two antennas, has no channel knowledge, and wants diversity at a low decoder cost: downlink transmit diversity in cellular systems is the standard case. When the receiver has two or more antennas and the SNR is high, spatial multiplexing or the golden code gives more rate. When the transmitter knows the channel, beamforming such as maximum ratio transmission gives an extra array gain.

## Pitfalls

- **The channel must stay constant over two slots.** Fast fading breaks the orthogonality and leaves interference between $s_1$ and $s_2$. The same holds for frequency selectivity across two subcarriers in the space-frequency form.
- **Conjugate the right sample.** The combiner uses $y_{i2}^*$, not $y_{i2}$. Mixing the conventions of different textbooks (signs on $s_2^*$ or on $s_1^*$) gives a combiner that does not decouple.
- **Power normalization.** Each antenna must send with half the power, so that the total equals the one-antenna case. Without this, the gain over one antenna looks 3 dB better than it is.
- **Channel estimation.** The decoder needs both $h_{i1}$ and $h_{i2}$, so the pilots must be orthogonal across the two antennas.
- **Diversity is not rate.** With two receive antennas, the code gives no multiplexing gain; see [spatial multiplexing](/spatial-multiplexing/).

## Implementations

## History

Siavash Alamouti published the scheme in October 1998 in the IEEE Journal on Selected Areas in Communications, as a two-branch transmit diversity method whose performance with one receiver equals that of two-branch receive combining with the same total power, minus 3 dB. Tarokh, Seshadri and Calderbank had given the rank and determinant criteria for space-time codes earlier in 1998, and in 1999 Tarokh, Jafarkhani and Calderbank showed that the code is an instance of a complex orthogonal design and generalized it to more antennas. The code entered the third-generation cellular standards as space-time transmit diversity, and its space-frequency form is the two-antenna transmit diversity mode of LTE.

## References
