---
tag: 8XKR8Q
kind: algorithm
slug: svd-precoding
name: SVD precoding
aliases:
- eigenbeamforming
- SVD transmission
area: communications/mimo-communications
level: core
summary: Sends streams along the right singular vectors of the channel, which turns a MIMO channel into parallel scalar channels.
model: real-ram
complexity:
  vars: {m: the number of receive antennas, n: the number of transmit antennas}
  time: {worst: "O(m n min(m, n))"}
  space: {extra: O(m n)}
properties: {deterministic: true, linear: true, needs_channel_at_transmitter: true, capacity_achieving: true, single_user: true}
history:
  year: 1998
  people: [Gregory G. Raleigh, John M. Cioffi, Emre Telatar]
  note: "Raleigh and Cioffi used the SVD of the channel to send parallel streams in 1998, and Telatar showed in 1999 that the SVD with water-filling reaches the capacity of a known MIMO channel."
prereqs: [mimo-capacity, singular-value-decomposition, water-filling-power-allocation]
see_also: [maximum-ratio-transmission, zero-forcing-precoding, block-diagonalization, codebook-based-precoding, hybrid-beamforming, spatial-multiplexing, bit-loading, kkt-conditions]
sources:
  - paper: doi:10.1002/ett.4460100604
    title: "Emre Telatar, Capacity of multi-antenna Gaussian channels, European Transactions on Telecommunications 10(6), 585-595, 1999"
    locator: the section on the capacity of a channel with a fixed and known H (the SVD of H and water-filling over its singular values)
  - paper: doi:10.1109/26.662641
    title: "Gregory G. Raleigh and John M. Cioffi, Spatio-temporal coding for wireless communication, IEEE Transactions on Communications 46(3), 357-366, 1998"
    locator: the transmission of parallel streams along the singular vectors of the channel
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: "Section 7.1.1, Capacity via singular value decomposition (the parallel channels, water-filling and the precoder V)"
  - book: isbn:9780521826150
    title: Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003
    locator: the chapter on the capacity of MIMO channels (the channel known at the transmitter and water-filling over the eigenmodes)
---

SVD precoding is the transmitter that reaches the [capacity of a MIMO channel](/mimo-capacity/) when the transmitter knows the channel. It computes the [singular value decomposition](/singular-value-decomposition/) $H = U \Sigma V^H$, sends stream $i$ along the right singular vector $v_i$, and gives the streams powers by [water-filling](/water-filling-power-allocation/) over the gains $s_i^2 / N_0$. The receiver multiplies by $U^H$. The result is a set of $r = \mathrm{rank}(H)$ independent scalar channels with no interference between them, so each stream can use its own scalar code and its own [bit loading](/bit-loading/). This is a single-user method: one transmitter and one receiver that has all $m$ antennas and can apply $U^H$ jointly. In a multiuser downlink the users cannot cooperate, so the base station uses [zero-forcing precoding](/zero-forcing-precoding/) or [block diagonalization](/block-diagonalization/) instead. With $r = 1$ or when only the strongest mode gets power, SVD precoding becomes beamforming on the principal eigenvector, which is [maximum ratio transmission](/maximum-ratio-transmission/). [Codebook-based precoding](/codebook-based-precoding/) replaces $V$ by the nearest matrix of a finite set when the transmitter learns the channel only through a few feedback bits, and [hybrid beamforming](/hybrid-beamforming/) splits $V$ into an analog and a digital part when the array has few RF chains.

## In plain words

A channel with several antennas at each end mixes the signals. Some directions in space reach the receiver strongly, some weakly and some not at all. The transmitter finds these directions and their strengths from the channel. It sends one data stream along each strong direction, so the streams arrive without disturbing each other, and the receiver unmixes them with a fixed rotation. The transmitter then shares its power between the streams. Strong directions get more power, and very weak ones get nothing, because power spent there gives little data. This gives the highest data rate that the channel can support.

## The problem

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$ known at the transmitter and at the receiver, $m$ receive antennas, $n$ transmit antennas and $w \sim \mathcal{CN}(0, N_0 I_m)$. The input has the covariance $Q = E[x x^H]$ with the power constraint $\mathrm{tr}(Q) \le P$, and $\rho = P / N_0$. The goal is a precoder $F \in \mathbb{C}^{n \times r}$, with $x = F d$ for $r$ unit-power streams $d$, and a receive matrix that together reach the capacity

$$C = \max_{Q \succeq 0,\ \mathrm{tr}(Q) \le P} \log_2 \det\Bigl(I_m + \frac{H Q H^H}{N_0}\Bigr)$$

in bits per channel use.

## The algorithm

```pseudo id=main
SVD-PRECODE(H, P, N0)
L1  (U, s, V) ← SVD(H)                          ▷ H = U diag(s) Vᴴ, s₁ ≥ s₂ ≥ ...
L2  r ← the number of nonzero sᵢ
L3  p ← WATER-FILL(s₁²/N0, ..., s_r²/N0; P)    ▷ pᵢ = (μ - N0/sᵢ²)⁺, Σ pᵢ = P
L4  F ← [√p₁ v₁, ..., √p_r v_r]                ▷ transmit x = F d
L5  return (F, [u₁, ..., u_r], s, p)
RECEIVE(y, U)
L6  z ← Uᴴ y                                    ▷ zᵢ = sᵢ √pᵢ dᵢ + noise
```

Line L1 is the expensive step. The implementation uses one-sided Jacobi rotations: each rotation makes two columns of $H$ orthogonal, and the product of the rotations is $V$. Line L3 sorts the gains and drops the weakest channel until the water level $\mu$ lies above $1 / g_i$ for every channel that is left. Line L4 is the only step that the transmitter needs once it has $F$; line L6 runs at the receiver, which must know $U$ or estimate the effective channel $H F$ from precoded pilots.

## Example

Take $m = n = 2$, $P = 2$, $N_0 = 1$ and

$$H = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}.$$

$H$ is real and symmetric with the eigenvectors $(1, 1)/\sqrt{2}$ and $(1, -1)/\sqrt{2}$ and the eigenvalues 3 and 1, so line L1 gives $s = (3, 1)$ and $V = U$ with these two columns. The gains are $g = (9, 1)$. Line L3 tries both channels: $\mu = (2 + 1/9 + 1)/2 = 14/9$, which is above $1/g_2 = 1$, so both stay on, with

$$p_1 = \frac{14}{9} - \frac{1}{9} = \frac{13}{9} \approx 1.444, \qquad p_2 = \frac{14}{9} - 1 = \frac{5}{9} \approx 0.556.$$

The rate is $\log_2(1 + 9 \cdot 13/9) + \log_2(1 + 5/9) = \log_2 14 + \log_2(14/9) = 4.4448$ bits per channel use. The two other simple choices do worse:

| power split | rate (bits per channel use) |
|---|---|
| water-filling $(1.444, 0.556)$ | 4.4448 |
| equal power $(1, 1)$ | $\log_2 10 + \log_2 2 = 4.3219$ |
| strongest mode only $(2, 0)$ | $\log_2 19 = 4.2479$ |

The last row is beamforming on $v_1$. It loses 0.20 bits, and at this SNR the weak mode is still worth some power. At $P = 0.5$ the water level is below $1/g_2$, and water-filling itself puts all power on $v_1$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem 1 shows $U_r^H H F = \mathrm{diag}(s_i \sqrt{p_i})$, so the receiver sees $r$ scalar channels with noise $\mathcal{CN}(0, N_0)$ each and no crosstalk, and $\|F\|_F^2 = \sum_i p_i = P$. Lemma 1 proves from the [KKT conditions](/kkt-conditions/) that $p_i = (\mu - 1/g_i)^+$ is the unique best power split, and that the drop loop of line L3 finds the right water level. Theorem 2 uses Hadamard's inequality on $V^H Q V$ to show that no input covariance of trace $P$ does better, so SVD precoding reaches the capacity $C$.

## Complexity

The SVD of line L1 costs $O(m n \min(m, n))$ by the usual bidiagonalization methods, to a fixed precision. A one-sided Jacobi sweep costs $O(m n^2)$, and a few sweeps are enough in practice because the method converges quadratically near the end. Line L3 costs $O(r \log r)$ for the sort and $O(r)$ for the loop. Line L4 costs $O(n r)$, and line L6 costs $O(m r)$ per received vector. The extra space is $O(m n)$ for $U$ and $V$. In a block fading channel lines L1 to L4 run once per channel realization.

## Properties

- **Capacity achieving.** With Gaussian codebooks on the streams, the rate equals the capacity of the known channel (theorem).
- **No interference between streams.** The receiver needs no joint detection. Each stream sees a scalar AWGN channel with the gain $s_i^2$.
- **Needs the channel at both ends.** The transmitter needs $V$ and the receiver needs $U$, or the effective channel $H F$.
- **Unique power split.** The powers are unique. The singular vectors are unique only up to a phase per stream, and up to a rotation inside a group of equal singular values; any choice gives the same rate.
- **High and low SNR limits.** At high SNR water-filling tends to equal power on the $r$ modes, and the rate grows as $r \log_2 \rho$. At low SNR only the strongest mode gets power, and SVD precoding becomes beamforming on $v_1$.

## Variants and improvements

- **Equal power.** Give $P/r$ to each mode. This is near optimal at high SNR and needs no water level.
- **Dominant eigenmode.** Use only $v_1$. This is [maximum ratio transmission](/maximum-ratio-transmission/) for a MIMO channel, with the gain $s_1^2$.
- **Bit loading with real constellations.** Replace the Shannon rate by a gap to capacity and integer bits per mode; see [bit loading](/bit-loading/).
- **Limited feedback.** Quantize $V$ with a codebook known at both ends; see [codebook-based precoding](/codebook-based-precoding/).
- **Fewer RF chains.** Approximate $F$ by $F_{RF} F_{BB}$ with a phase-only analog part; see [hybrid beamforming](/hybrid-beamforming/).
- **Multiuser.** For several receivers with several antennas each, [block diagonalization](/block-diagonalization/) first removes the interference between users and then applies SVD precoding to each user.
- **Statistical channel knowledge.** If the transmitter knows only the transmit correlation of a [Kronecker channel](/kronecker-channel-model/), it sends along the eigenvectors of that correlation matrix instead.

## When to use it

Use SVD precoding on a point-to-point link where the transmitter has a good channel estimate, for example in time division duplex from the reverse link, or with fine feedback in a slowly varying channel. It is the reference for every other MIMO precoder, because no linear or nonlinear scheme beats its rate on a known single-user channel. With OFDM it runs once per subcarrier. If the channel changes faster than the feedback, or if the transmitter knows only statistics, use [space-time codes](/orthogonal-space-time-block-codes/) or open-loop [spatial multiplexing](/spatial-multiplexing/) instead.

## Pitfalls

- **Stale channel.** If $H$ changes after the transmitter computes $V$, the streams leak into each other and the rate falls quickly at high SNR.
- **Phase of the singular vectors.** Two SVD routines can return $v_i$ with different phases. The receiver must use the $u_i$ that match the $v_i$ of the transmitter, or estimate $H F$ from precoded pilots.
- **Power units.** The gains in line L3 are $s_i^2 / N_0$, not $s_i / N_0$. Using $s_i$ gives the wrong water level.
- **Rank.** Give no stream to a singular value that is zero to rounding. Use a relative threshold such as $s_i > 10^{-12} s_1$.
- **Sum of powers.** The power constraint is on $\mathrm{tr}(F F^H)$. If $F$ is rescaled after rounding, rescale all columns by the same factor.

## Implementations

## History

The idea is the vector form of the classic water-filling result for parallel Gaussian channels: a unitary change of basis at each end makes a matrix channel parallel. For wireless links with antenna arrays, Raleigh and Cioffi (1998) used the SVD of the channel to send parallel streams, and Telatar (1999, first circulated as a Bell Labs report in 1995) proved that the SVD with water-filling gives the capacity of a MIMO channel known at the transmitter. Today the same structure appears in LTE and 5G NR as closed-loop precoding, usually through a codebook rather than an exact $V$.

## References
