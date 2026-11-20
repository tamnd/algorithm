---
tag: 17KZND
kind: algorithm
slug: maximum-ratio-transmission
name: Maximum ratio transmission
aliases:
- MRT
- conjugate beamforming
area: communications/mimo-communications
level: core
summary: Sends one stream along the conjugate of the channel vector, the transmit dual of maximal ratio combining.
model: real-ram
complexity:
  vars: {M: the number of transmit antennas, K: the number of users, N: the number of receive antennas, t: the number of power iterations}
  time: {worst: O(M K)}
  time_mimo: {worst: "O(M^2 N + t M^2)"}
  space: {extra: O(M K)}
properties: {deterministic: true, linear: true, needs_channel_at_transmitter: true, optimal_single_user_single_stream: true, needs_noise_level: false}
history:
  year: 1999
  people: [Titus K. Y. Lo]
  note: "Lo named and analyzed maximum ratio transmission in 1999 as the transmit counterpart of maximal ratio combining. As conjugate beamforming it became the basic linear precoder of massive MIMO after 2010."
prereqs: [beamforming, maximal-ratio-combining, mimo-channel-model]
see_also: [maximal-ratio-combining, svd-precoding, zero-forcing-precoding, regularized-zero-forcing-precoding, codebook-based-precoding, massive-mimo, favorable-propagation, power-iteration]
sources:
  - paper: doi:10.1109/26.795811
    title: "Titus K. Y. Lo, Maximum ratio transmission, IEEE Transactions on Communications 47(10), 1458-1461, 1999"
    locator: the transmit weights proportional to the conjugate channel, the receive combining and the diversity analysis
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: "Section 5.3.2, MISO channel (transmit beamforming along the channel vector and its capacity log(1 + P ||h||^2 / N0))"
  - paper: doi:10.1109/TCOMM.2013.020413.110848
    title: "Hien Quoc Ngo, Erik G. Larsson and Thomas L. Marzetta, Energy and spectral efficiency of very large multiuser MIMO systems, IEEE Transactions on Communications 61(4), 1436-1449, 2013"
    locator: the analysis of maximum ratio processing in very large arrays and the comparison with zero forcing
  - book: isbn:9781107175570
    title: Thomas L. Marzetta, Erik G. Larsson, Hong Yang and Hien Quoc Ngo, Fundamentals of Massive MIMO, Cambridge University Press, 2016
    locator: the chapters on downlink linear precoding (conjugate beamforming and its effective SINR)
---

Maximum ratio transmission (MRT) is the transmitter that sends one stream from $M$ antennas so that the copies add in phase at the receiver. For the channel $y = h^H x + w$ it sends $x = \sqrt{P}\, h / \|h\|\, s$, which gives the largest possible SNR $P \|h\|^2 / N_0$ for the power $P$. It is the transmit dual of [maximal ratio combining](/maximal-ratio-combining/): MRC weights the receive antennas by the conjugate channel, MRT weights the transmit antennas by it, and both give the gain $\|h\|^2$ and the [diversity order](/diversity-order/) $M$ in i.i.d. Rayleigh fading. With several receive antennas MRT sends along the top eigenvector of $H^H H$; this is the one-stream case of [SVD precoding](/svd-precoding/), which sends up to $\mathrm{rank}(H)$ streams. With $K$ single-antenna users, MRT gives each user the beam $h_k / \|h_k\|$ and ignores the interference between users; this is called conjugate beamforming. [Zero-forcing precoding](/zero-forcing-precoding/) removes that interference at the cost of a smaller beam gain, and [regularized zero-forcing precoding](/regularized-zero-forcing-precoding/) moves between the two. When the transmitter knows only a few feedback bits about $h$, [codebook-based precoding](/codebook-based-precoding/) picks the best beam from a fixed set instead.

## In plain words

Several antennas send the same symbol to one receiver. Each signal reaches the receiver with its own delay and strength. The transmitter knows these effects and corrects the phase of each antenna in advance, so all the copies arrive in step and add up. It also puts more power on the antennas with a strong path to the receiver and less on the weak ones. The result is the strongest possible signal at the receiver for the given total power. With many users, the transmitter does the same for each user and accepts that each beam leaks a little to the other users.

## The problem

The base station has $M$ antennas. In the single-user case the receiver has one antenna and gets $y = h^H x + w$ with $h \in \mathbb{C}^M$ known at the transmitter and $w \sim \mathcal{CN}(0, N_0)$. The transmitter sends one unit-power symbol $s$ as $x = f s$ with $\|f\|^2 \le P$, and it wants the largest SNR $|h^H f|^2 / N_0$. With $N$ receive antennas the model is $y = H x + w$ with $H \in \mathbb{C}^{N \times M}$, and the receiver combines with a unit vector $c$. In the multiuser downlink, user $k$ gets $y_k = h_k^H x + w_k$ and $x = \sum_k w_k s_k$; MRT here is a simple rule, not the solution of an optimization problem.

## The algorithm

```pseudo id=main
MRT(h, P)
L1  a ← ‖h‖
L2  return f ← √P h / a                       ▷ hᴴ f = √P ‖h‖, a real number
MRT-MIMO(H, P)
L3  G ← Hᴴ H
L4  repeat v ← G v / ‖G v‖ until v stops changing    ▷ power iteration
L5  λ ← vᴴ G v                                ▷ the top eigenvalue
L6  c ← H v / ‖H v‖; return (√P v, c, λ)        ▷ c is the receive combiner
CONJUGATE-BEAMFORMING(h₁, ..., h_K, P)
L7  for each user k: w_k ← MRT(h_k, P/K)
```

Lines L1 and L2 are the whole single-user algorithm. Line L4 needs a start vector that is not orthogonal to the top eigenvector; the implementation starts once from each nonzero column of $G$ and keeps the best result, because at least one column has a component along that eigenvector. Any [eigenvalue](/eigenvalue/) routine or an [SVD](/singular-value-decomposition/) of $H$ can replace line L4. Line L7 splits the power equally; other splits are a matter of power control.

## Example

Take $M = 3$, $h = (1 + j,\ 2,\ -j)$, $P = 1$ and $N_0 = 1$. Then $\|h\|^2 = 2 + 4 + 1 = 7$, and line L2 gives $f = (1 + j,\ 2,\ -j)/\sqrt{7}$. Antenna $i$ contributes $\bar h_i f_i = |h_i|^2 / \sqrt{7}$ to the received amplitude, so the three contributions $2/\sqrt7$, $4/\sqrt7$ and $1/\sqrt7$ are positive real numbers and add in phase to $\sqrt{7}$. The SNR is 7, or 8.451 dB. Two simpler schemes with the same power do worse:

| scheme | $\lvert h^H f \rvert^2 / N_0$ | in dB |
|---|---|---|
| MRT, $f = h / \|h\|$ | 7 | 8.451 |
| the strongest antenna only, $f = e_2$ | 4 | 6.021 |
| equal amplitudes and no phase correction, $f = (1, 1, 1)/\sqrt{3}$ | 3 | 4.771 |

The last row shows why the phase matters: without the phase correction the three terms do not add up in step.

With two receive antennas and $H = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$, line L3 gives $G = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix}$, with the top eigenvalue $\lambda = (3 + \sqrt{5})/2 = 2.618$ and $v = (0.526, 0.851)$. The SNR gain is 2.618 (4.18 dB). The best single transmit antenna is the second one, whose column has squared norm 2 (3.01 dB).

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Theorem 1 shows by the Cauchy-Schwarz inequality that $|h^H f|^2 \le P \|h\|^2$ for every $f$ with $\|f\|^2 \le P$, with equality exactly for $f$ along $h$. Theorem 2 shows that with $N$ receive antennas the best SNR is $\lambda_{\max}(H^H H) P / N_0$, reached by the top eigenvector and the MRC combiner of line L6, and Lemma 1 shows that the power iteration of line L4 finds it from at least one of its starts. Theorem 3 shows that in i.i.d. Rayleigh fading the MRT SNR has the same Gamma law as MRC over $M$ branches, which gives the BPSK error rate $1.5991 \times 10^{-3}$ for $M = 2$ at 10 dB. Lemma 2 shows that conjugate beamforming meets the power constraint and that the normalized interference $|u^H v|^2$ between two independent isotropic channels has the mean $1/M$.

## Complexity

Lines L1 and L2 cost $O(M)$, and conjugate beamforming for $K$ users costs $O(M K)$, with $O(M K)$ space for the precoder. The MIMO form costs $O(M^2 N)$ for $G$ and $O(M^2)$ per power iteration, so $O(M^2 N + t M^2)$ for $t$ iterations. The number of iterations grows with $1 / \log(\lambda_1 / \lambda_2)$. MRT needs no matrix inversion, which is its main advantage over zero forcing when $M$ and $K$ are large.

## Properties

- **Optimal for one stream to one antenna.** No other beamformer gives a larger SNR (theorem).
- **Array gain and diversity.** The SNR is $P \|h\|^2 / N_0$, which has mean $M P / N_0$ in i.i.d. Rayleigh fading and diversity order $M$.
- **Same law as MRC.** The SNR distributions of MRT with $M$ transmit antennas and MRC with $M$ receive antennas are the same. This is the uplink-downlink duality in its simplest form.
- **No noise level needed.** The beam depends only on $h$.
- **Interference in the multiuser case.** Conjugate beamforming ignores the other users, so at high SNR the SINR is limited by interference and the sum rate saturates, unless $M$ grows.
- **Local operation.** Each antenna needs only its own channel coefficients for its weight, up to the common normalization. This makes MRT the natural precoder for distributed arrays such as [cell-free massive MIMO](/cell-free-massive-mimo/).

## Variants and improvements

- **MIMO MRT.** Send along the top eigenvector of $H^H H$ and combine with MRC at the receiver (lines L3 to L6). This is SVD precoding with one stream.
- **Conjugate beamforming.** One MRT beam per user with a share of the power (line L7). In [massive MIMO](/massive-mimo/) with $M \gg K$, [favorable propagation](/favorable-propagation/) makes the beams nearly orthogonal.
- **Equal gain transmission.** Keep only the phases: $f_i = \sqrt{P/M}\, h_i / |h_i|$. Every antenna sends the same power, which suits power amplifiers with a per-antenna limit.
- **Quantized MRT.** Pick the beam from a codebook known at both ends; see [codebook-based precoding](/codebook-based-precoding/).
- **Zero forcing and regularized zero forcing.** Replace $h_k$ by the corresponding column of a channel inverse to remove or reduce the interference between users.
- **Statistical MRT.** With only the transmit correlation matrix known, send along its top eigenvector.

## When to use it

Use MRT for a single stream to one user when the transmitter has a reliable channel estimate, for example from reverse-link pilots in time division duplex. In the multiuser downlink, use conjugate beamforming when $M$ is much larger than $K$, at low SNR where noise dominates interference, or when the antennas are distributed and cannot share their channel estimates. At high SNR with $K$ close to $M$, interference dominates, and zero forcing or regularized zero forcing give a much higher sum rate.

## Pitfalls

- **Wrong conjugation.** With the model $y = h^H x + w$ the beam is along $h$. With the model $y = h^T x + w$ it is along $\bar h$. Mixing the two conventions destroys the phase alignment.
- **Stale channel.** A phase error on the estimate of $h$ reduces the gain. MRT needs the channel at the time of transmission, not at the time of the pilot.
- **Interference limit.** In the multiuser case the SINR does not grow without bound with $P$. Plan the system with the SINR formula, not with the SNR $P \|h_k\|^2 / N_0$.
- **Power iteration start.** A fixed start vector can be orthogonal to the top eigenvector, and then the iteration converges to the wrong eigenvalue. Start from several vectors, or use an eigenvalue routine.
- **Two names for two things.** The 1999 paper treats one user with several receive antennas. Conjugate beamforming for many users is a later use of the same weights.

## Implementations

## History

Lo (1999) named maximum ratio transmission, gave the joint transmit and receive weights for several receive antennas, and showed that it gives the same diversity as maximal ratio combining. With the rise of [massive MIMO](/massive-mimo/) after Marzetta's work of 2010, the same rule for many users, under the name conjugate beamforming, became the simplest downlink precoder of large arrays, and Ngo, Larsson and Marzetta (2013) compared its energy and spectral efficiency with zero forcing.

## References
