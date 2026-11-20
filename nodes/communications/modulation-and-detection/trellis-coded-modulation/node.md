---
tag: NP37EZ
kind: technique
slug: trellis-coded-modulation
name: Trellis-coded modulation
aliases:
- TCM
- Ungerboeck codes
area: communications/modulation-and-detection
level: core
summary: Joins a convolutional code with a constellation by set partitioning, which gains several dB without more bandwidth.
prereqs: [convolutional-code, trellis, viterbi-algorithm, phase-shift-keying, quadrature-amplitude-modulation]
see_also: [bit-interleaved-coded-modulation, multilevel-coding, convolutional-code, trellis, viterbi-algorithm, maximum-likelihood-sequence-estimation, euclidean-distance, gray-labeling]
sources:
  - paper: doi:10.1109/TIT.1982.1056454
    title: Gottfried Ungerboeck, Channel coding with multilevel/phase signals, IEEE Transactions on Information Theory 28(1), 55-67, 1982
    locator: set partitioning, the mapping rules, the 4-state and 8-state codes for 8-PSK, and the tables of codes found by computer search
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Chapter 8 (trellis-coded modulation)
---

Trellis-coded modulation (TCM) joins a [convolutional code](/convolutional-code/) and a constellation into one code over the constellation points. The code works on a constellation with twice as many points as the uncoded system needs, so the rate in bits per symbol and the bandwidth do not change. The points are split into subsets with growing distance inside each subset (set partitioning), the coded bits choose the subset, and the uncoded bits choose the point inside it. The receiver runs the [Viterbi algorithm](/viterbi-algorithm/) on the [trellis](/trellis/) with squared Euclidean distances as branch metrics. A 4-state code on 8-PSK gains $3.01$ dB over uncoded QPSK at high SNR, with no extra bandwidth. Ungerboeck published the method in 1982. It made the voiceband modems of the late 1980s and the 1990s possible.

## In plain words

Adding redundancy usually costs bandwidth: the coded bits need more symbols. TCM pays instead with a bigger constellation: 8 points to send 2 bits per symbol. Points that are close together are made hard to confuse by the code, because the code never lets two paths differ in only one close pair. The trick is to sort the points into groups whose members are far apart, and to let the code pick the group, while the free bits pick a member. The receiver then compares whole sequences, not single symbols. The far-apart members protect the free bits, and the code protects the choice of group.

## When it applies

- The channel is band-limited and close to AWGN, so the only way to gain is in Euclidean distance at a fixed rate in bits per symbol.
- The receiver can run a Viterbi decoder with soft distance metrics.
- The rate is $n$ bits per symbol with $n \ge 1$, and a constellation of $2^{n+1}$ points is acceptable.
- The channel does not fade fast. On a fading channel the diversity order of TCM is small (see the pitfalls), and [bit-interleaved coded modulation](/bit-interleaved-coded-modulation/) is usually better.

## The template

1. **Partition the constellation.** Split the $2^{n+1}$ points into two subsets, each subset again into two, and so on, so that the minimum distance $d_i$ inside the subsets of level $i$ grows: $d_0 < d_1 < d_2 < \cdots$. For unit-energy 8-PSK, $d_0^2 = (2\sin(\pi/8))^2 = 0.586$ for the whole set, $d_1^2 = 2$ for the two QPSK subsets $B_0, B_1$, and $d_2^2 = 4$ for the four antipodal pairs $C_0, \ldots, C_3$.
2. **Split the input bits.** Of the $n$ input bits per symbol, $\tilde n$ go into a rate-$\tilde n/(\tilde n + 1)$ convolutional encoder. Its $\tilde n + 1$ output bits select one of the $2^{\tilde n + 1}$ subsets of level $\tilde n + 1$. The other $n - \tilde n$ bits are not coded; they select the point inside the subset. When $n > \tilde n$, each trellis branch holds $2^{n - \tilde n}$ parallel transitions.
3. **Assign the subsets to the trellis (Ungerboeck's rules).** Parallel transitions get points of the same smallest subset, so their distance is the largest $d_{\tilde n + 1}$. The branches that leave one state, and those that enter one state, get subsets of the same first-level subset ($B_0$ or $B_1$), so a diverging or merging pair of paths gains at least $d_1^2$. All points are used equally often.
4. **Compute the free distance.** $d_{\mathrm{free}}^2$ is the smaller of the parallel distance $d_{\tilde n + 1}^2$ and the smallest sum of squared distances along two paths that leave a state and merge again. The asymptotic coding gain over an uncoded constellation with minimum distance $d_u$ and the same average energy is $10\log_{10}(d_{\mathrm{free}}^2/d_u^2)$ dB.
5. **Decode.** Run the Viterbi algorithm on the trellis with branch metric $\min_{a \in \text{subset}}|y - h a|^2$: first find the best point in each subset, then decide the sequence of subsets, then read off the uncoded bits from the best points.

## Classic examples

**4-state 8-PSK code, 2 bits per symbol.** One bit goes through a rate-$1/2$ 4-state code whose two output bits select one of $C_0, \ldots, C_3$; the second bit picks one of the two antipodal points of that pair. Parallel transitions are at $d_2^2 = 4$. Two paths that diverge use two subsets of the same $B$ (distance $d_1^2 = 2$), they merge in the same way ($d_1^2 = 2$), and in between they differ by at least $d_0^2 = 0.586$, for $4.586$ in all. So $d_{\mathrm{free}}^2 = \min(4, 4.586) = 4$, against $d_u^2 = 2$ for uncoded unit-energy QPSK: a gain of $10\log_{10} 2 = 3.01$ dB.

**8-state 8-PSK code.** With two coded bits, no parallel transitions are left, and the shortest error path has $d_1^2 + d_0^2 + d_1^2 = 4.586$. The gain is $10\log_{10}(4.586/2) = 3.60$ dB. More states give more gain, with diminishing returns, at the cost of a Viterbi decoder that doubles in size with each extra memory bit.

**Voiceband modems.** The ITU V.32 modem at $9600$ bit/s uses an 8-state TCM code with a 32-point cross constellation, designed by Wei to be invariant under rotations by multiples of $90°$, so that the receiver does not need to know the absolute phase. V.34 uses a 4-dimensional trellis code.

**One-dimensional TCM.** On $2^{n+1}$-PAM, the partition takes every second point, then every fourth, with the raw distances $2, 4, 8, \ldots$. The same rules give codes for PAM and, on each axis, for QAM.

## Variations

- **Multidimensional TCM.** Partition a constellation in 4 or 8 dimensions, built from 2-dimensional points. It gives finer trade-offs between gain and complexity, and better rotational invariance.
- **Rotationally invariant codes.** Wei's nonlinear codes with differential encoding tolerate a phase ambiguity of the carrier loop. A linear code on 8-PSK is invariant under fewer rotations.
- **Pragmatic TCM.** Use one standard rate-$1/2$ 64-state code for all constellations, with the uncoded bits on the parallel transitions. It loses a little against the best code for each case but simplifies hardware.
- **TCM for fading channels.** Design for the effective length (the number of differing symbols on the shortest error path) and the product distance instead of $d_{\mathrm{free}}$, with a symbol interleaver.
- **Turbo TCM.** Two TCM encoders in parallel with an interleaver, decoded iteratively with the [BCJR algorithm](/bcjr-algorithm/) on each trellis.
- **Multilevel coding.** Protect each partition level with its own code: [multilevel coding](/multilevel-coding/), the general form of the same idea.

## Pitfalls

- **The gain is asymptotic.** $10\log_{10}(d_{\mathrm{free}}^2/d_u^2)$ is the gain at high SNR. At moderate error rates the number of nearest paths also matters, and the real gain is smaller.
- **Fading.** With parallel transitions, two sequences can differ in one symbol only, so the diversity order on a fast Rayleigh channel is $1$. Even without them, the effective length is short for small codes. Bit-interleaved coded modulation gives more diversity.
- **Phase ambiguity.** A carrier loop for 8-PSK locks to one of 8 phases. Unless the code is invariant under the rotations, or the receiver resolves the phase, the decoder fails after a phase slip.
- **Gray labels are wrong here.** TCM needs set-partitioning labels: the coded bits select subsets with large distance. Gray labeling, which is right for BICM, does not give the subset structure.
- **The constellation doubles.** Doubling the points at a fixed energy reduces the minimum distance, by about $3$ dB for large QAM and by $5.33$ dB for 8-PSK against QPSK ($d^2$ falls from $2$ to $0.586$). The code must win this back before it gains anything.

## Exercises

1. Compute $d_0^2, d_1^2, d_2^2$ for unit-energy 8-PSK and check the values above.
2. Draw the trellis of the 4-state 8-PSK code with the subsets on the branches, and find the error path with distance $4.586$.
3. For 16-QAM with set partitioning, show that the squared distances inside the levels double at each step: $d_{i+1}^2 = 2 d_i^2$.
4. Explain why a code with parallel transitions can never have $d_{\mathrm{free}}^2$ larger than $d_{\tilde n + 1}^2$, and why the 4-state 8-PSK code reaches this limit.
5. Explain why the Viterbi decoder of a TCM code first picks the best point in each subset.

## References
