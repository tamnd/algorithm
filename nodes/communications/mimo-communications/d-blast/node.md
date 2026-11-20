---
tag: YCBK18
kind: algorithm
slug: d-blast
name: D-BLAST
aliases:
- diagonal BLAST
area: communications/mimo-communications
level: advanced
summary: Spreads each coded layer diagonally over all transmit antennas and time, so that MMSE nulling and cancelling reaches the outage capacity of slow fading, minus a start-up rate loss.
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {n: the number of transmit antennas, m: the number of receive antennas, M: the constellation size, L: the number of layers in a frame, B: the number of symbols in a block}
  time: {worst: O(L n^3 m + L n^4 + L B n^2 m + L B n M)}
  space: {extra: O(L B n + n m)}
properties: {deterministic: true, linear: false, exact_ml: false, rate_fraction: "L / (L + n - 1)", middle_layer_sinr_sum_equals_log_det: true, needs_noise_level: "only for MMSE nulling"}
history:
  year: 1996
  people: [Gerard J. Foschini]
  note: "Foschini proposed the diagonal layered space-time architecture at Bell Labs and showed that its capacity grows linearly with the number of antennas. The simpler vertical version, V-BLAST, followed in 1998."
prereqs: [mimo-detection, mmse-mimo-detector, v-blast]
see_also: [spatial-multiplexing, mimo-capacity, outage-capacity, diversity-multiplexing-tradeoff, alamouti-code, successive-interference-cancellation, interleaving, rayleigh-fading-channel]
sources:
  - paper: doi:10.1002/bltj.2015
    title: Gerard J. Foschini, Layered space-time architecture for wireless communication in a fading environment when using multi-element antennas, Bell Labs Technical Journal 1(2), 41-59, 1996
    locator: the diagonal layering of the coded streams over the antennas and the nulling and cancelling receiver
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: "Section 8.5 (D-BLAST, an outage-optimal architecture), Section 8.5.2 (coding across the transmit antennas and the start-up loss) and Section 8.3.4 (the MMSE-SIC identity)"
---

D-BLAST (diagonal Bell Laboratories layered space-time) is a transmission scheme with a matching receiver for [spatial multiplexing](/spatial-multiplexing/) over a slow fading channel. The transmitter cuts each coded layer into $n$ blocks and sends block $k$ on antenna $k$ one block time after block $k - 1$, so every layer crosses all $n$ antennas on a diagonal of the antenna and time grid. The receiver decodes the layers one after the other. For each block it subtracts the earlier layers, which are already decoded, and nulls the later layers with the ZF or MMSE filter, as in [V-BLAST](/v-blast/). The difference from V-BLAST is the layering. In V-BLAST each stream stays on one antenna, so in slow fading a stream on a weak antenna fails even when the channel as a whole is good. In D-BLAST every layer sees every antenna, and with MMSE nulling the SINRs of the $n$ blocks of a middle layer satisfy $\sum_k \log_2(1 + \mathrm{SINR}_k) = \log_2 \det(I + (E_s / N_0) H^H H)$ (a theorem). So a layer code fails only when the channel is in outage, and D-BLAST reaches the [outage capacity](/outage-capacity/) of the channel (Tse and Viswanath, Section 8.5). The price is the start-up loss: the frame needs $L + n - 1$ block times for $L$ layers, so the rate is $L / (L + n - 1)$ of the V-BLAST rate.

## In plain words

Several antennas send at the same time. Each message is cut into pieces, and the pieces go out on the antennas in turn, one antenna after another, like a staircase. So every message uses every antenna once. The receiver reads one message at a time. It removes the messages that it already knows and blocks out the ones that it has not read yet. A message that only used one weak antenna would be lost. Here each message gets a fair share of the good and the bad antennas, so it gets through whenever the channel as a whole is good enough. The cost is a little time at the start and at the end of each frame, when some antennas are silent.

## The problem

The channel is $y_t = H x_t + w_t$ with $H \in \mathbb{C}^{m \times n}$ fixed for a whole frame (slow fading), $x_t \in \mathbb{C}^n$ the vector sent at time $t$, and $w_t \sim \mathcal{CN}(0, N_0 I)$ independent over time. The transmitter has $L$ layers. Each layer is cut into $n$ blocks of $B$ symbols from a constellation $\mathcal{S}$ of energy $E_s$, or of coded symbols. Block $k$ of layer $l$ ($0 \le k < n$, $0 \le l < L$) goes out on antenna $k$ at block time $l + k$. So at block time $t$, antenna $k$ sends block $k$ of layer $t - k$ when $0 \le t - k < L$, and is silent otherwise. The receiver knows $H$, and $N_0$ for MMSE nulling. It must find the symbols of every layer. ZF nulling needs $m \ge n$; MMSE nulling works for every $m$.

## The algorithm

```pseudo id=main
D-BLAST-DETECT(Y, H, S, L, a)            ▷ a = 0 for ZF nulling, a = N0/Es for MMSE
L1  for l ← 0 to L - 1                    ▷ the layers in order
L2      for k ← 0 to n - 1                ▷ the blocks of layer l
L3          t ← l + k
L4          r ← Y_t - Σ over k' > k of h_k' x̂(layer t - k', block k')   ▷ cancel earlier layers
L5          A ← {k' < k : antenna k' is active at time t} ∪ {k}          ▷ later layers, nulled
L6          P ← (H_Aᴴ H_A + a I)⁻¹;  z_k ← (row k of P H_Aᴴ) r, without bias
L7          γ_k ← the SNR or SINR of z_k
L8      x̂(layer l) ← DECODE(z_0, ..., z_{n-1}; γ_0, ..., γ_{n-1})
L9  return x̂
```

Line L4 subtracts the antennas $k' > k$, which carry the layers $t - k' < l$; the receiver has already decoded them. Line L5 collects the active antennas $k' < k$, which carry the later layers $t - k' > l$. Line L6 is the nulling filter of the [ZF MIMO detector](/zero-forcing-mimo-detector/) or the [MMSE MIMO detector](/mmse-mimo-detector/) on these columns, and line L7 records the quality of each block, $(E_s / N_0) / P_{kk}$ for ZF and $1 / (a P_{kk}) - 1$ for MMSE. Line L8 is the decoder of the layer code. It gets one output per block and a reliability per block, as for a code over parallel channels. The implementation gives two decoders: slicing each symbol alone (no code), and a repetition code, where the same $B$ symbols fill all $n$ blocks and the decoder adds the outputs with weights $\gamma_k$ before slicing. The filters of lines L5 and L6 depend only on $k$ and on which antennas are active, so a receiver computes them once per channel.

## Example

Take $n = m = 2$, $L = 3$, BPSK and the real channel $H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$. The frame has $L + n - 1 = 4$ block times:

| block time $t$ | antenna 0 | antenna 1 |
|---|---|---|
| 0 | layer 0, block 0 | silent |
| 1 | layer 1, block 0 | layer 0, block 1 |
| 2 | layer 2, block 0 | layer 1, block 1 |
| 3 | silent | layer 2, block 1 |

The rate is $3 / 4$ of V-BLAST. With ZF nulling, the receiver works as follows, with SNRs in units of $E_s / N_0$.

- Layer 0, block 0 at $t = 0$: antenna 1 is silent, so the receiver combines with $h_0$ alone, the [maximal ratio combining](/maximal-ratio-combining/) SNR $\|h_0\|^2 = 5$.
- Layer 0, block 1 at $t = 1$: antenna 0 carries layer 1, which is not decoded yet, so the receiver nulls it. The SNR is $1 / [(H^T H)^{-1}]_{11} = 1/5 = 0.2$.
- Layer 1: at $t = 1$, block 0 on antenna 0 sees antenna 1, which carries layer 0. The receiver cancels it, so the SNR is again 5. At $t = 2$, block 1 nulls layer 2 on antenna 0 and gets 0.2.
- Layer 2: block 0 cancels layer 1 and gets 5. Block 1 at $t = 3$ is alone and gets $\|h_1\|^2 = 2$.

Every layer has one strong block and one weak block, so no layer depends only on the weak direction of $H$. With MMSE nulling at $E_s / N_0 = 10$ dB ($a = 0.1$), the middle layer gets $\gamma_0 = 50$ and $\gamma_1 = 0.4 / 0.17 \approx 2.35$, and $(1 + 50)(1 + 2.35) = 171 = \det(I + 10 H^T H)$. So a layer code can carry $\log_2 171 \approx 7.42$ bit for each symbol position of a block. One layer ends at each block time, so this is $\log_2 \det(I + 10 H^T H)$ bit per channel use, the full capacity of the channel with equal power, apart from the start-up loss.

Without noise, if the layers carry $(+1, -1)$, $(-1, -1)$ and $(+1, +1)$ in blocks 0 and 1, the receiver gets $y_0 = (2, 1)$, $y_1 = (-3, -2)$, $y_2 = (1, 0)$ and $y_3 = (1, 1)$, and the ZF receiver recovers every symbol.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows five things. First, each layer visits each antenna once, and the frame has $L + n - 1$ block times (a closed form). Second, with ZF nulling and no noise, the receiver recovers every layer (a theorem). Third, block 0 of every layer has the maximal ratio combining SNR $\|h_0\|^2 E_s / N_0$ (a theorem). Fourth, with MMSE nulling and correct decisions on the earlier layers, each layer $l \le L - n$ has $\sum_k \log_2(1 + \gamma_k) = \log_2 \det(I + (E_s / N_0) H^H H)$, and the last $n - 1$ layers have at least this much (a theorem). Fifth, if the noise and interference of the $n$ outputs are uncorrelated, the weights $\gamma_k$ give the combined SINR $\sum_k \gamma_k$ (a closed form). The outage statement then follows from the coding theorem for parallel Gaussian channels, as in Tse and Viswanath, Section 8.5.2.

## Complexity

The filter of block $k$ inverts a matrix of size at most $k + 1$, at a cost of $O(k^2 m + k^3)$. Over the $n$ blocks of a layer this is $O(n^3 m + n^4)$. The implementation recomputes it for each of the $L$ layers; a receiver needs it only for the at most $n$ different patterns of active antennas. Each symbol of a block costs up to $n - 1$ cancellations of length $m$, one inner product of length $m$, and $O(M)$ for slicing. So a frame costs $O(L n^3 m + L n^4 + L B n^2 m + L B n M)$ in the [real RAM](/real-ram/), plus the cost of the layer decoder, with $O(L B n + n m)$ space for the decisions and the filters.

## Properties

- **Every layer sees every antenna.** Block $k$ of each layer is on antenna $k$ (closed form).
- **Rate loss.** $L$ layers need $L + n - 1$ block times, a fraction $L / (L + n - 1)$ of the V-BLAST rate. For $n = 4$ and $L = 20$ this is $20 / 23 \approx 0.87$ (closed form).
- **Capacity per layer.** With MMSE nulling and correct decisions on earlier layers, each middle layer sees $\log_2 \det(I + (E_s / N_0) H^H H)$ in total (theorem). This is the rate of the channel $H$ with equal power and no channel knowledge at the transmitter.
- **Outage optimal.** With capacity-achieving codes over the $n$ blocks, a layer fails only when the channel is in outage, apart from the rate loss (Tse and Viswanath, Section 8.5).
- **Error propagation between layers.** A layer that is decoded wrong spoils the cancellation in the next $n - 1$ layers.
- **Measured gain over vertical layering.** For 4-QAM with $m = n = 2$, $L = 6$, a repetition code over the $n$ blocks, i.i.d. Rayleigh fading per frame and $E_s / N_0 = 6$ dB, the test with seed 1505 runs 300 frames of 6 symbols. D-BLAST made 15 symbol errors. Vertical layering, where each antenna repeats its own symbol twice and the receiver uses MMSE V-BLAST, made 63 (measurement).

## Variants and improvements

- **ZF or MMSE nulling.** ZF nulling needs $m \ge n$ and loses SNR on the blocks that null many layers. MMSE nulling is the version that reaches the capacity identity above (Tse and Viswanath, Section 8.3.4).
- **Vertical layering.** [V-BLAST](/v-blast/) sends each stream on one antenna. It has no start-up loss and a simpler code structure, but in slow fading a stream on a weak antenna fails.
- **Other layer patterns.** Later layered schemes assign the layers to the antennas in other patterns, for example cyclic ones that keep every antenna busy. The receiver then cannot always cancel all earlier layers in one pass.
- **Space-time codes.** The [Alamouti code](/alamouti-code/) and other space-time codes give diversity with a simple receiver but less multiplexing gain. The [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/) compares these schemes.
- **Iterative receivers.** Soft cancellation with a turbo loop, as in [turbo equalization](/turbo-equalization/), reduces error propagation between layers.

## When to use it

Use D-BLAST when the channel stays the same for a whole codeword (slow fading), so that a stream on one antenna can be in a deep fade for its whole length, and when frames are long, so that $L$ is much larger than $n$ and the start-up loss is small. In fast fading, or when the code is long enough to see many channel states, V-BLAST with per-stream codes reaches the same rate without the diagonal structure. For short frames, the rate loss of $n - 1$ block times is large, so a space-time code or a joint detector is often better.

## Pitfalls

- **Wrong cancellation order.** At block time $t$, antenna $k' > k$ carries an earlier layer and must be cancelled. Antenna $k' < k$ carries a later layer and must be nulled. Mixing them up leaves interference in every block.
- **Forgetting the silent antennas.** At the start and the end of a frame some antennas are silent. Do not null them; the filter should only include the active antennas, or the receiver loses SNR on the edge layers.
- **Ignoring the start-up loss.** The rate is $L / (L + n - 1)$ of the V-BLAST rate. A comparison at equal $L$ that ignores this is unfair to V-BLAST.
- **Error propagation.** One wrong layer spoils the next $n - 1$ layers. Use strong codes and check each layer before cancelling it.
- **Correlated interference.** If two blocks of one layer null the same later layer and that layer repeats its symbols, the residual interference of the two outputs is correlated, and the combined SINR is lower than $\sum_k \gamma_k$. Real codes avoid this because the symbols of different blocks differ.

## Implementations

## History

Foschini described the layered space-time architecture with diagonal layers in the Bell Labs Technical Journal in 1996, together with the result that the capacity of a rich-scattering channel grows linearly with the number of antennas. The diagonal structure and the start-up loss made it hard to build, so Wolniansky, Foschini, Golden and Valenzuela built the vertical version, V-BLAST, in 1998. Tse and Viswanath (2005) explained why the diagonal layering matters: with MMSE-SIC it reaches the outage capacity in slow fading, where V-BLAST does not.

## References
