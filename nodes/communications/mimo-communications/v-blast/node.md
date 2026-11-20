---
tag: Z0RT80
kind: algorithm
slug: v-blast
name: V-BLAST
aliases:
- vertical BLAST
- ordered successive interference cancellation
area: communications/mimo-communications
level: core
summary: Detects the spatially multiplexed streams one at a time, the stream with the best post-detection SNR first, nulling the streams not yet detected and cancelling each decision.
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {n: the number of transmitted streams, m: the number of receive antennas, M: the constellation size}
  time: {worst: O(n^3 m + n^4 + n M)}
  time_per_vector_after_setup: {worst: O(n m + n M)}
  space: {extra: O(n m)}
properties: {deterministic: true, linear: false, exact_ml: false, order_depends_only_on_channel: true, order_maximizes_smallest_snr: true, needs_noise_level: "only for MMSE nulling", mmse_nulling_reaches_capacity_with_coding: true}
history:
  year: 1998
  people: [Peter W. Wolniansky, Gerard J. Foschini, Glen D. Golden, Reinaldo A. Valenzuela]
  note: "Bell Labs proposed V-BLAST as a simpler version of the diagonal BLAST of Foschini (1996), and built a laboratory prototype of it."
prereqs: [mimo-detection, zero-forcing-mimo-detector, mmse-mimo-detector]
see_also: [d-blast, successive-interference-cancellation, k-best-detector, babai-nearest-plane, decision-feedback-equalizer, mimo-capacity, spatial-multiplexing, qr-decomposition]
sources:
  - paper: doi:10.1109/ISSSE.1998.738086
    title: Peter W. Wolniansky, Gerard J. Foschini, Glen D. Golden and Reinaldo A. Valenzuela, V-BLAST - an architecture for realizing very high data rates over the rich-scattering wireless channel, Proc. URSI International Symposium on Signals, Systems and Electronics, Pisa, 1998, pages 295-300
    locator: the detection algorithm (nulling with the rows of the pseudoinverse, the ordering by the smallest row norm and the cancellation)
  - paper: doi:10.1049/el:19990058
    title: Glen D. Golden, Gerard J. Foschini, Reinaldo A. Valenzuela and Peter W. Wolniansky, Detection algorithm and initial laboratory results using V-BLAST space-time communication architecture, Electronics Letters 35(1), 14-16, 1999
    locator: the recursive detection algorithm and the measured spectral efficiencies
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: "Section 8.1 (the V-BLAST architecture), Section 8.3.2 (successive cancellation and error propagation) and Section 8.3.4 (MMSE-SIC reaches the capacity)"
  - paper: doi:10.1109/ICASSP.2000.859065
    title: Babak Hassibi, An efficient square-root algorithm for BLAST, Proc. IEEE ICASSP 2000, pages 737-740
    locator: the square-root algorithm that finds the order and the nulling vectors without one matrix inverse per step
---

V-BLAST (vertical Bell Laboratories layered space-time) is the receiver that made [spatial multiplexing](/spatial-multiplexing/) practical. It solves the [MIMO detection](/mimo-detection/) problem one stream at a time. At each step it computes the nulling filter of the [zero-forcing MIMO detector](/zero-forcing-mimo-detector/) or the [MMSE MIMO detector](/mmse-mimo-detector/) for the streams not yet detected, picks the stream with the highest post-detection SNR, slices it, and subtracts its contribution from the received vector. Each cancellation removes one interferer, so the later streams see a channel with fewer columns and less noise enhancement. The detector differs from the linear detectors because it uses its own decisions, and from multiuser [successive interference cancellation](/successive-interference-cancellation/) because it chooses the order from the post-detection SNR of the channel matrix, not from the received power of each user. The order maximizes the smallest post-detection SNR over all $n!$ orders (a theorem). A wrong decision propagates to the later streams, so V-BLAST is still far from ML at high SNR. [D-BLAST](/d-blast/) uses the same receiver on a diagonal layering that removes the rate loss in slow fading.

## In plain words

Several antennas send different symbols at the same time. The receiver first finds the one symbol that it can see most clearly, after it blocks out the others. It decides that symbol. Then it subtracts that symbol from what it received, as if that antenna had never sent anything. Now the problem is smaller, and the next symbol is easier to see. The receiver repeats this until all symbols are decided. Starting with the clearest symbol is important: an early mistake spoils every later step, so the receiver makes its first decisions where a mistake is least likely.

## The problem

The model is $y = H x + w$. Here $H \in \mathbb{C}^{m \times n}$ is the known channel matrix with columns $h_1, \ldots, h_n$, $x \in \mathcal{S}^n$ holds one point of a constellation $\mathcal{S}$ of size $M$ and energy $E_s$ per stream, and $w \sim \mathcal{CN}(0, N_0 I)$. ZF nulling needs $m \ge n$ and full column rank. MMSE nulling works for every $m$ and needs $N_0 > 0$. For a set $K$ of streams, $H_K$ is the matrix of the columns in $K$. The output is a decision $\hat x \in \mathcal{S}^n$ and the order in which the streams were detected.

## The algorithm

```pseudo id=main
V-BLAST(y, H, S, a)                       ▷ a = 0 for ZF nulling, a = N0/Es for MMSE
L1  r ← y;  K ← {1, ..., n}
L2  while K is not empty
L3      P ← (H_Kᴴ H_K + a I)⁻¹;  W ← P H_Kᴴ
L4      k ← the stream in K with the smallest P_kk
L5      z ← (row k of W) r                ▷ for MMSE, divide by 1 - a P_kk
L6      x̂_k ← the point of S nearest to z
L7      r ← r - h_k x̂_k
L8      K ← K \ {k}
L9  return x̂
```

Line L3 is the nulling filter for the streams still in $K$. For ZF ($a = 0$) the stream $k$ has the post-detection SNR $(E_s / N_0) / P_{kk}$, and for MMSE it has the unbiased SINR $1 / (a P_{kk}) - 1$, so line L4 picks the stream with the best SNR or SINR in both cases. Line L5 for MMSE removes the bias of the MMSE estimate, as in the [MMSE MIMO detector](/mmse-mimo-detector/). Line L7 cancels the decided stream. If the decision is right, the new $r$ equals $H_{K \setminus k} x_{K \setminus k} + w$, a smaller problem of the same kind. Lines L3 and L4 depend only on $H$ and $a$, so a receiver computes the order and the nulling rows once per channel and reuses them for every received vector of a block.

## Example

Take $m = n = 2$, BPSK with $\mathcal{S} = \{+1, -1\}$, $E_s = 1$, and the real channel

$$H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}, \qquad (H^T H)^{-1} = \begin{pmatrix} 2 & -3 \\ -3 & 5 \end{pmatrix}.$$

The transmitter sends $x = (+1, -1)$, so $H x = (1, 0)$. The noise is $w = (-0.3, 0.4)$, and the receiver gets $y = (0.7, 0.4)$. The plain ZF output is $H^{-1} y = (0.3, 0.1)$, which gives $(+1, +1)$: stream 2 is wrong.

V-BLAST with ZF nulling runs as follows.

1. Lines L3 and L4: $P_{11} = 2 < P_{22} = 5$, so stream 1 goes first. Its nulling row is row 1 of $H^{-1}$, $(1, -1)$, and line L5 gives $z = 0.7 - 0.4 = 0.3$, so $\hat x_1 = +1$.
2. Line L7: $r = y - h_1 \cdot (+1) = (0.7 - 2, 0.4 - 1) = (-1.3, -0.6)$.
3. Now $K = \{2\}$ and $P = 1 / \|h_2\|^2 = 1/2$. Line L5 gives $z = (h_2^T r) / 2 = -1.9 / 2 = -0.95$, so $\hat x_2 = -1$.

The decision $(+1, -1)$ is right, and it is also the ML decision: its metric $\|y - H x\|^2 = 0.25$ is the smallest of the four candidates (the others give 3.05, 7.85 and 19.45). In units of $E_s / N_0$, the post-detection SNRs of the two steps are $1/2 = 0.5$ and $\|h_2\|^2 = 2$. The other order would give $1/5 = 0.2$ for stream 2 first and then $\|h_1\|^2 = 5$. V-BLAST takes the order whose worse step is better, 0.5 against 0.2.

The other order also fails on this $y$. Stream 2 first gives $z = -0.7 + 2 \cdot 0.4 = 0.1$, so $\hat x_2 = +1$, which is wrong. The cancellation then subtracts the wrong symbol: $r = y - h_2 = (-0.3, -0.6)$, and $z = (h_1^T r) / 5 = -0.24$ gives $\hat x_1 = -1$, which is wrong too. This is error propagation.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows four things. First, with ZF nulling and no noise, every step sees its stream with no interference, and V-BLAST returns $x$ (a theorem). Second, the post-detection SNR of a stream can only grow when other streams leave $K$, for ZF and for MMSE (a theorem). Third, from this monotonicity, an exchange argument shows that the greedy choice of line L4 maximizes the smallest post-detection SNR or SINR over all $n!$ orders, assuming correct earlier decisions (a theorem). Fourth, with MMSE nulling and correct cancellation, $\sum_k \log_2 (1 + \mathrm{SINR}_k) = \log_2 \det(I + (E_s / N_0) H^H H)$ in every order, so per-stream coding at these rates reaches the [MIMO capacity](/mimo-capacity/) of the channel (a theorem, Tse and Viswanath, Section 8.3.4).

## Complexity

The direct method of line L3 inverts an $j \times j$ matrix for $j = n, n - 1, \ldots, 1$, at a cost of $O(j^2 m + j^3)$ each, so the setup per channel costs $O(n^3 m + n^4)$ in the [real RAM](/real-ram/). The square-root algorithm of Hassibi (2000) finds the same order and nulling rows without a new inverse at each step. After the setup, each received vector costs $n$ inner products of length $m$ for line L5, $n$ updates of length $m$ for line L7 and $n$ slicings of $O(M)$ each, so $O(n m + n M)$. The extra space is $O(n m)$ for the nulling rows. The implementation on this page recomputes the setup on every call, for clarity.

## Properties

- **Exact without noise.** With ZF nulling and $w = 0$, every decision is right (theorem).
- **Best order in the max-min sense.** Among all $n!$ orders, the order of line L4 maximizes the smallest post-detection SNR (ZF) or SINR (MMSE), assuming correct earlier decisions (theorem).
- **Order from the channel only.** The order does not depend on $y$, so it is computed once per channel.
- **Never worse than linear in SNR.** The first stream has the best ZF or MMSE SNR of all streams, and each later stream has an SNR at least as high as with linear detection (theorem, from the monotonicity).
- **Capacity with MMSE and coding.** With MMSE nulling, Gaussian codebooks and correct cancellation, the stream rates $\log_2 (1 + \mathrm{SINR}_k)$ add up to $\log_2 \det(I + (E_s / N_0) H^H H)$ (theorem).
- **Error propagation.** Uncoded V-BLAST cancels hard decisions, so a wrong early decision makes later decisions more likely wrong.
- **Diversity.** In i.i.d. Rayleigh fading with ZF nulling, the first detected stream has at least the diversity $m - n + 1$ of a ZF stream (theorem). Because of error propagation, uncoded V-BLAST does not reach the diversity $m$ of ML in general (rule).
- **Measured agreement with ML.** For 4-QAM with $m = n = 4$, i.i.d. $\mathcal{CN}(0, 1)$ channel entries and $E_s / N_0 = 15$ dB, the test with seed 1405 runs 150 random vectors. ZF V-BLAST agreed with ML on 147 vectors and MMSE V-BLAST on all 150. ZF V-BLAST made 7 symbol errors, and plain ZF made 24 (measurement).

## Variants and improvements

- **MMSE nulling.** Set $a = N_0 / E_s$ in line L3. This is often called MMSE V-BLAST or MMSE-SIC. It needs $N_0$. In the 4 by 4, 4-QAM measurement under Properties, it agreed with ML on every vector at 15 dB.
- **Square-root and QR methods.** The square-root algorithm of Hassibi (2000) avoids one inverse per step. A [QR decomposition](/qr-decomposition/) with the columns sorted during the factorization gives a near-optimal order for the cost of one QR. With a fixed order, ZF-SIC is the [Babai nearest plane](/babai-nearest-plane/) rule and the spatial version of the [decision feedback equalizer](/decision-feedback-equalizer/).
- **Coded layers.** If each stream carries its own channel code, the receiver decodes a whole stream before it cancels it, which reduces error propagation. With MMSE nulling this reaches the capacity in fast fading (Tse and Viswanath, Section 8.3.4).
- **Diagonal layering.** In slow fading a stream that sits on one bad antenna fails. [D-BLAST](/d-blast/) rotates each codeword over all antennas.
- **Several candidates.** The [K-best detector](/k-best-detector/) keeps the $K$ best partial decisions instead of one, which reduces error propagation at a known cost.

## When to use it

Use V-BLAST when the linear detectors lose too much and ML or a sphere search is too expensive, with $n$ up to about 8 streams. Use MMSE nulling whenever $N_0$ is known. In a coded system, use it with per-stream codes and decode each stream before cancelling. For a near-ML error rate on a square channel at high SNR, use the [K-best detector](/k-best-detector/), [lattice reduction aided detection](/lattice-reduction-aided-detection/), or [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) instead.

## Pitfalls

- **Wrong order of the bias step.** Line L4 compares $P_{kk}$ before the bias removal of line L5. Removing the bias does not change the order, because the unbiased SINR $1 / (a P_{kk}) - 1$ also falls with $P_{kk}$.
- **Picking the stream by its column norm.** The stream with the strongest column is not always the one with the best post-detection SNR. In the example, stream 1 has $\|h_1\|^2 = 5$ but only the SNR 0.5 after ZF nulling; the right measure is $1 / P_{kk}$.
- **Cancelling with the wrong scale.** Line L7 subtracts $h_k \hat x_k$ with the full column, not with the nulled output $z$.
- **Error propagation is not in the SNR.** The post-detection SNRs assume correct earlier decisions. The real error rate of later streams is higher.
- **ZF with $n > m$.** The first step has a singular $H^H H$. Use MMSE nulling, which works for any $m$, or transmit fewer streams.
- **Recomputing per vector.** Lines L3 and L4 depend only on $H$; recomputing them for each received vector multiplies the cost by the block length.

## Implementations

## History

Foschini described the layered space-time architecture with diagonal layers (D-BLAST) in 1996, and showed that its capacity grows linearly with the number of antennas. The diagonal layering was hard to build, so Wolniansky, Foschini, Golden and Valenzuela proposed the simpler vertical version in 1998, with the nulling, ordering and cancelling receiver on this page. Golden, Foschini, Valenzuela and Wolniansky reported the laboratory prototype in Electronics Letters in 1999. Hassibi gave the square-root algorithm in 2000. The view of the receiver as MMSE-SIC that reaches the capacity is part of the textbook treatment of Tse and Viswanath (2005).

## References
