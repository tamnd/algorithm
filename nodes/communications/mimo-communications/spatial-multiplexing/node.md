---
tag: BTX47R
kind: technique
slug: spatial-multiplexing
name: Spatial multiplexing
aliases:
- MIMO multiplexing
area: communications/mimo-communications
level: intro
summary: Sends independent streams from several antennas at once, so the rate grows with the smaller of the antenna counts.
prereqs: [mimo-channel-model, mimo-capacity]
see_also: [diversity-multiplexing-tradeoff, v-blast, d-blast, mimo-detection, zero-forcing-mimo-detector, mmse-mimo-detector, svd-precoding, alamouti-code]
sources:
  - paper: doi:10.1002/bltj.2015
    title: "Gerard J. Foschini, Layered space-time architecture for wireless communication in a fading environment when using multi-element antennas, Bell Labs Technical Journal 1(2), 41-59, 1996"
    locator: "the diagonally layered architecture and its rate, which grows linearly with the number of antennas"
  - paper: doi:10.1023/A:1008889222784
    title: "Gerard J. Foschini and Michael J. Gans, On limits of wireless communications in a fading environment when using multiple antennas, Wireless Personal Communications 6(3), 311-335, 1998"
    locator: the capacity of quasi-static Rayleigh MIMO channels and its growth with the number of antennas
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 7.1 (parallel spatial channels from the singular value decomposition), Section 8.1 (V-BLAST) and Section 8.5 (D-BLAST)"
  - book: isbn:9780521826150
    title: "Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003"
    locator: "Chapter 6, Space-time coding without channel knowledge at the transmitter (spatial multiplexing), and Chapter 7, Space-time receivers"
---

Spatial multiplexing sends several independent data streams at the same time and on the same frequency, one from each transmit antenna or one along each direction of the channel, and separates them at the receiver by the different ways each stream reaches the receive antennas. In a rich scattering channel the rate then grows with $\min(N_t, N_r)$, which is the slope that the [MIMO capacity](/mimo-capacity/) promises. The price is diversity: the [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/) says how much reliability a scheme gives up for each extra stream, and the [Alamouti code](/alamouti-code/) is the opposite choice, with one stream and full diversity.

## In plain words

Two people in a room both talk at once. A listener with one ear hears a mix and cannot follow either. A listener with two ears placed apart hears a different mix in each ear, and from the two mixes the brain can pull the two voices apart.

Spatial multiplexing does this with radio. Each transmit antenna sends its own stream of data on the same frequency at the same time. Because walls and objects scatter the waves, each receive antenna gets a different mix. If the mixes are different enough, the receiver can undo the mixing and recover every stream. Each extra pair of antennas adds one more stream, so the data rate grows without extra bandwidth or extra power.

## When it applies

- The channel has rank at least the number of streams. This needs rich scattering or antennas far enough apart; a single line-of-sight path gives rank one.
- The receiver knows the channel ($H$ known at the receiver), for example from orthogonal pilots, one set for each transmit antenna.
- For linear receivers, $N_r \ge N_t$ (or at least as many receive antennas as streams), so that the streams can be separated.
- The SNR is high enough that the extra streams are worth more than the diversity they cost. At low SNR, the capacity is $\rho N_r / \ln 2$ to first order, whatever the number of streams.

## The template

1. **Split.** Divide the data into $k \le \min(N_t, N_r)$ streams. Encode and modulate each one (or encode jointly and then split).
2. **Map to antennas.** Without channel knowledge at the transmitter, send stream $i$ from antenna $i$: $x = (s_1, \ldots, s_{N_t})^T$ with power $P/N_t$ each. With CSIT, send stream $i$ along the right singular vector $v_i$ of $H$, as in [SVD precoding](/svd-precoding/), with power from [water-filling](/water-filling-power-allocation/).
3. **Receive.** The receiver sees $y = Hx + w$ and solves [MIMO detection](/mimo-detection/): exact maximum likelihood by sphere decoding, or a linear filter such as the [zero-forcing](/zero-forcing-mimo-detector/) or [MMSE](/mmse-mimo-detector/) detector, or a filter followed by [successive interference cancellation](/successive-interference-cancellation/) as in [V-BLAST](/v-blast/).
4. **Decode.** Decode each stream from its filtered output.

The uncoded rate is $k \log_2 M$ bits per channel use for $M$-point constellations.

## Classic examples

**Two by two with zero forcing.** Take $H = \begin{pmatrix} 1 & 0.5 \\ 0.5j & 1 \end{pmatrix}$ and send the QPSK pair $s = ((1 + j)/\sqrt2, (1 - j)/\sqrt2)$, 4 bits per use. Without noise, $y = Hs = (1.0607 + 0.3536j,\ 0.3536 - 0.3536j)$. The zero-forcing filter is $H^{-1}$, with $\det H = 1 - 0.25j$, and $H^{-1} y$ returns $s$ exactly. With noise, stream $k$ has the SNR $(\rho/2) / [(H^H H)^{-1}]_{kk}$ after the filter. Here $[(H^H H)^{-1}]_{kk} = 1.17647$ for both streams, so at $\rho = 10$ dB each stream has 4.25 (6.28 dB), and the two streams carry $2 \log_2 5.25 = 4.785$ bits per use. The equal-power capacity of this $H$ at 10 dB is 5.324 bits, so the linear receiver loses 0.54 bits. A receiver with MMSE filtering and successive cancellation closes this gap.

**V-BLAST.** Each antenna sends its own coded stream. The receiver detects the strongest stream, subtracts it, and repeats; see [V-BLAST](/v-blast/). Wolniansky, Foschini, Golden and Valenzuela described it and a laboratory prototype at Bell Labs in 1998.

**D-BLAST.** Foschini's original 1996 architecture spreads each codeword over all antennas in a diagonal pattern, so that each codeword sees every antenna; see [D-BLAST](/d-blast/).

**Eigenmode transmission.** With CSIT, the SVD makes $\min(N_t, N_r)$ parallel channels with gains $\sigma_i$, and water-filling gives the capacity exactly.

**Standards.** Wi-Fi from IEEE 802.11n on and LTE send several spatial layers on the same subcarriers, with the number of layers chosen from the reported rank of the channel.

## Variations

- **Horizontal and vertical coding.** One code for each antenna (horizontal) is simple but gives each codeword only the diversity of its antenna. One code across all antennas (vertical) or diagonal layering gives more diversity at a cost in decoding.
- **Precoded multiplexing with limited feedback.** The receiver chooses a precoder from a codebook and reports its index; see [codebook-based precoding](/codebook-based-precoding/).
- **Multiuser spatial multiplexing.** The streams go to different users, with [zero-forcing precoding](/zero-forcing-precoding/) at the transmitter; this is the basis of [massive MIMO](/massive-mimo/).
- **Linear dispersion and full-rate space-time codes.** Codes such as the [golden code](/golden-code/) send $\min(N_t, N_r)$ symbols per use and also get full diversity, which pure multiplexing does not.

## Pitfalls

- **Rank deficiency.** In line of sight, with closely spaced antennas or a keyhole channel, $H$ has low rank, and the extra streams cannot be separated. Choose the number of streams from the rank, not from the antenna count.
- **Noise enhancement.** Zero forcing with $N_r = N_t$ has a diversity order of $N_r - N_t + 1 = 1$ per stream in i.i.d. Rayleigh fading (a theorem), so at a fixed rate the error rate falls only as $\rho^{-1}$.
- **Error propagation.** In successive cancellation, a wrong decision on one stream corrupts all later ones. Ordering by SNR and coding each stream reduce this.
- **Power per stream.** The total power is fixed, so with $N_t$ streams each gets $P/N_t$. Comparing a multiplexed link with a single-stream link at the same per-antenna power overstates the gain.
- **Pilot overhead.** The receiver must estimate $N_t N_r$ gains, and the pilots grow with $N_t$. In fast fading, this can cancel the gain.
- **Diversity is not free.** A scheme that sends $\min(N_t, N_r)$ uncoded streams with independent decisions does not reach the full diversity $N_t N_r$; see the [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/).

## Exercises

1. A $4 \times 4$ link sends four streams of 16-QAM. What is the uncoded rate in bits per channel use? *Answer: 16.*
2. For the $2 \times 2$ example above at $\rho = 20$ dB, find the zero-forcing SNR of each stream and the sum rate. *Answer: $50 / 1.17647 = 42.5$ (16.28 dB) each, and $2 \log_2 43.5 = 10.886$ bits, against 11.442 bits for the equal-power capacity.*
3. Show that $H = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ cannot carry two streams, and find its capacity at $\rho = 10$ with equal power. *Answer: $\det H = 0$, so the rank is one, and the capacity is $\log_2(1 + 2\rho) = \log_2 21 = 4.392$ bits.*
4. With $N_t = 2$ and $N_r = 1$, how many streams can a linear receiver separate? *Answer: one; use the [Alamouti code](/alamouti-code/) for diversity instead.*

## References
