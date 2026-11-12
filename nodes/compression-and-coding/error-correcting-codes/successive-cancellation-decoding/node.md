---
tag: CTNMA4
kind: algorithm
slug: successive-cancellation-decoding
name: Successive cancellation decoding
aliases:
- SC decoding
- successive cancellation decoder for polar codes
area: compression-and-coding/error-correcting-codes
level: research
summary: "Decoder of polar codes that decides u_0, u_1, ... in order. Each bit uses the channel LLRs and the earlier decisions. It takes O(N log N) time."
model: word-ram
complexity:
  vars: {N: the block length of the polar code, N = 2^n}
  time: {worst: Θ(N log N), average: Θ(N log N), best: Θ(N log N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, recursive: true, soft_decision: true, maximum_likelihood: false}
history:
  year: 2009
  people: [Erdal Arıkan]
  note: Arıkan defined SC decoding together with polar codes in 2009 and proved that it reaches capacity on polar codes.
prereqs: [polar-code, channel-polarization-theorem]
see_also: [maximum-likelihood-decoding, belief-propagation-decoding, list-decoding, cyclic-redundancy-check, binary-erasure-channel, additive-white-gaussian-noise-channel, reed-muller-code, butterfly-operation]
sources:
  - paper: doi:10.1109/TIT.2009.2021379
    title: Erdal Arıkan, Channel polarization, a method for constructing capacity-achieving codes for symmetric binary-input memoryless channels, IEEE Transactions on Information Theory 55(7), 2009, pages 3051 to 3073
    locator: Section V (the SC decoder and the bound P_e <= sum of Z(W_N^(i)) over the information set) and Section VIII (the recursive implementation in O(N log N))
  - paper: doi:10.1109/TIT.2015.2410251
    title: Ido Tal and Alexander Vardy, List decoding of polar codes, IEEE Transactions on Information Theory 61(5), 2015, pages 2213 to 2226
    locator: The SC decoder as a list of one path, and its extension to L paths
  - paper: doi:10.1109/TSP.2015.2439211
    title: Alexios Balatsoukas-Stimming, Mani Bastani Parizi and Andreas Burg, LLR-based successive cancellation list decoding of polar codes, IEEE Transactions on Signal Processing 63(19), 2015
    locator: The update rules f and g in the LLR domain and the min-sum approximation
---

Successive cancellation (SC) decoding is the decoder that Erdal Arıkan defined for [polar codes](/polar-code/). It decides the input bits $u_0, u_1, \ldots, u_{N-1}$ one at a time, in order, and each decision uses the channel outputs and all earlier decisions. It runs in $\Theta(N \log N)$ time with two small update rules on log-likelihood ratios. With it, polar codes reach the capacity of each symmetric binary-input memoryless channel, but for a fixed short code it is weaker than [maximum likelihood decoding](/maximum-likelihood-decoding/).

## In plain words

A polar code mixes the message bits with a fixed pattern of XORs, and each received bit is a noisy copy of one mixed bit. The decoder must undo the mixing. SC does it one input bit at a time, from the first to the last. For each bit, it asks how sure the received signal is that the bit is 0 or 1, and it takes the earlier decided bits as true. If the bit is a frozen bit, the decoder already knows it is 0. Otherwise it picks the more likely value. A decision is never changed later, so one early mistake can spoil the rest of the block. The work is shared through a tree of halves, so the cost is close to that of the encoder.

## The problem

**Notation.** Vectors are rows over $\mathrm{GF}(2)$ and indices run from $0$ to $N - 1$, with $N = 2^n$. The code is $x = u F^{\otimes n}$ with $F = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ and no bit reversal, $u_i = 0$ on the frozen set $\mathcal{F}$, and the message on the information set $\mathcal{A} = \mathcal{F}^c$, $K = |\mathcal{A}|$ (see [polar code](/polar-code/)).

**Channel.** Each code bit $x_j$ goes through an independent use of a binary-input memoryless channel $W$ with output $y_j$. The decoder gets *soft decisions*: the log-likelihood ratios (LLRs)

$$\lambda_j = \ln \frac{W(y_j \mid 0)}{W(y_j \mid 1)}.$$

A positive $\lambda_j$ favors $x_j = 0$. A *hard decision* is the sign alone. For BPSK on the [AWGN channel](/additive-white-gaussian-noise-channel/), with $0 \mapsto +1$, $1 \mapsto -1$ and noise variance $\sigma^2$, $\lambda_j = 2 y_j / \sigma^2$. On the [binary erasure channel](/binary-erasure-channel/) $\lambda_j$ is $+\infty$, $-\infty$ or $0$ for an erasure.

**Task.** Given $\lambda_0, \ldots, \lambda_{N-1}$ and $\mathcal{F}$, output an estimate $\hat u$ with $\hat u_i = 0$ for $i \in \mathcal{F}$, and the codeword $\hat x = \hat u F^{\otimes n}$.

## The algorithm

The two update rules combine the LLRs $a$ and $b$ of the bits at positions $j$ and $j + h$ of a block of length $2h$:

$$f(a, b) = 2 \operatorname{artanh}\Bigl(\tanh\frac{a}{2} \tanh\frac{b}{2}\Bigr) \approx \operatorname{sign}(a) \operatorname{sign}(b) \min(|a|, |b|), \qquad g(a, b, s) = b + (1 - 2s)\, a.$$

$f$ is the LLR of the XOR of two bits, and the right side is its *min-sum* approximation. $g$ adds two views of one bit when the bit $s$ that was XORed onto the first view is known. The call SC-DECODE$(\lambda, \mathcal{F})$ returns the pair $(\hat u, \hat x)$.

```pseudo id=main
SC-DECODE(λ, F)                              ▷ λ: N LLRs, F: N frozen flags
L1  N ← |λ|
L2  if N = 1 then
L3      if F[0] or λ[0] ≥ 0 then b ← 0 else b ← 1
L4      return ([b], [b])                     ▷ (û, x̂) of length 1
L5  h ← N / 2
L6  for j ← 0 to h − 1 do α[j] ← f(λ[j], λ[j + h])
L7  (û_a, x_a) ← SC-DECODE(α, F[0 .. h − 1])
L8  for j ← 0 to h − 1 do β[j] ← g(λ[j], λ[j + h], x_a[j])
L9  (û_b, x_b) ← SC-DECODE(β, F[h .. N − 1])
L10 return (û_a ‖ û_b, (x_a ⊕ x_b) ‖ x_b)
```

The recursion follows $F^{\otimes n} = \begin{pmatrix} G & 0 \\ G & G \end{pmatrix}$ with $G = F^{\otimes (n-1)}$. Split $u = (a, b)$ into halves and let $v = aG$, $w = bG$. Then $x = (v \oplus w, w)$. Position $j$ sees $v_j \oplus w_j$ and position $j + h$ sees $w_j$. So line L6 gives the LLR of $v_j$, and line L7 decodes the first half $a$ as a polar code of length $h$. Line L8 uses the decided $v$, which is $x_a$, to read $w_j$ from both positions, and line L9 decodes $b$. Line L10 re-encodes the two halves.

The leaves are reached in the order $u_0, u_1, \ldots, u_{N-1}$. A frozen leaf returns 0 whatever its LLR (line L3). On the BEC, $f$ and $g$ reduce to rules on known bits and erasures: $f$ is the XOR if both inputs are known and an erasure otherwise, and $g$ returns $b$ if $b$ is known, $a \oplus s$ if only $a$ is known, and an erasure otherwise.

## Example

Take the $[8, 4, 4]$ polar code with $\mathcal{A} = \{3, 5, 6, 7\}$. The message $(1, 1, 1, 0)$ gives $u = (0, 0, 0, 1, 0, 1, 1, 0)$ and $x = (1, 0, 0, 1, 0, 1, 1, 0)$ (see [polar code](/polar-code/)). The received LLRs are

$$\lambda = (-3,\ 2,\ 1,\ -4,\ -1,\ -2,\ -3,\ 2).$$

Position 4 has the wrong sign: $x_4 = 0$ but $\lambda_4 < 0$. Decode with min-sum. Line L6 at the top gives $\alpha = (f(-3, -1), f(2, -2), f(1, -3), f(-4, 2)) = (1, -2, -1, -2)$. The table lists each leaf in the order of the decisions, with the LLR that reaches it.

| $i$ | frozen | leaf LLR | $\hat u_i$ | how the LLR is made |
|---|---|---|---|---|
| 0 | yes | $-1$ | 0 | $f(f(1, -1), f(-2, -2)) = f(-1, 2)$ |
| 1 | yes | $1$ | 0 | $g(-1, 2, 0)$ |
| 2 | yes | $0$ | 0 | $f(0, -4)$ with $\beta = (g(1, -1, 0), g(-2, -2, 0)) = (0, -4)$ |
| 3 | no | $-4$ | 1 | $g(0, -4, 0)$ |
| 4 | yes | $2$ | 0 | $f(-2, -4)$ with right-half $\beta = (2, -4, -4, 6)$ |
| 5 | no | $-6$ | 1 | $g(-2, -4, 0)$ |
| 6 | no | $-6$ | 1 | $f(-6, 10)$ |
| 7 | no | $16$ | 0 | $g(-6, 10, 1)$ |

After the first half, $x_a = (1, 1, 1, 1)$, so line L8 at the top gives $\beta = (g(-3, -1, 1), g(2, -2, 1), g(1, -3, 1), g(-4, 2, 1)) = (2, -4, -4, 6)$. The output is $\hat u = (0, 0, 0, 1, 0, 1, 1, 0)$ and $\hat x = (1, 0, 0, 1, 0, 1, 1, 0)$. The decoder corrected the error. The exact $f$ gives the same decisions here.

**SC is not maximum likelihood.** On the same code, take $\lambda = (4, -1, -2, 3, -1, 6, -1, 3)$. SC outputs the all-zero word, with correlation $\sum_j (1 - 2\hat x_j)\lambda_j = 11$. The word $x = (0, 1, 1, 0, 1, 0, 0, 1)$, from $u = (0, 0, 0, 1, 0, 1, 1, 1)$, has correlation 13, so a maximum likelihood decoder picks it. On BEC(1/2) the exact block error probabilities of this code are $115/256 \approx 0.449$ for SC and $107/256 \approx 0.418$ for maximum likelihood. SC is equal to maximum likelihood on some codes: on the rate-one code and on the repetition code, for example. Those two codes are the base of the fast decoders below.

## Correctness

The proof is by induction on $N$ and shows two facts. First, with the exact $f$, the LLR at leaf $i$ is the LLR of the synthetic channel $W_N^{(i)}$ at the output $(y, \hat u_0, \ldots, \hat u_{i-1})$. So each $\hat u_i$ for $i \in \mathcal{A}$ is the maximum likelihood decision for $u_i$ on that channel, when the earlier decisions are taken as true. Second, the returned $\hat x$ is equal to $\hat u F^{\otimes n}$. The key step is that, for a uniform $b$, the vector $w = bG$ is uniform, so the pairs $(y_j, y_{j+h})$ are independent uses of the channel $W^-$ with input $v_j$. When $v$ is known they are independent uses of $W^+$ with input $w_j$. The full proof is in [the correctness proof](proofs/correctness.md).

As a consequence, the decoder makes no error if the channel makes none, and on a symmetric channel its block error probability is at most $\sum_{i \in \mathcal{A}} Z(W_N^{(i)})$ (Arıkan 2009).

## Complexity

Let $T(N)$ be the number of operations on a block of length $N$. Lines L6 and L8 make $N/2$ calls each of $f$ and $g$, and lines L7 and L9 decode two blocks of length $N/2$, so

$$T(N) = 2\, T(N/2) + \Theta(N), \qquad T(1) = \Theta(1).$$

The solution is $T(N) = \Theta(N \log N)$. The decoder calls $f$ exactly $(N/2) \log_2 N$ times and $g$ exactly $(N/2) \log_2 N$ times, the same count as the XORs of the encoder.

- The time is $\Theta(N \log N)$ in each case, because the work does not depend on the LLR values.
- The extra space is $\Theta(N)$: the live arrays have lengths $N/2 + N/4 + \cdots$ along one path of the recursion.
- The recursion depth is $\log_2 N$, so a recursive program is safe for each length that fits in memory.
- The leaves are decided in sequence, so the latency in a circuit is $\Theta(N)$ steps even with $N/2$ processing units.

## Properties

- **Exact on the BEC with a genie.** If the decoder is given the true earlier bits, the probability that leaf $i$ is erased is exactly $Z(W_N^{(i)})$, the value of the recursion $z \mapsto 2z - z^2$, $z \mapsto z^2$. The tests check this by enumeration of all erasure patterns for $N \le 8$.
- **No backtracking.** A wrong decision on an information bit is never corrected and is fed into all later LLRs.
- **Frozen values are trusted.** Line L3 ignores the LLR of a frozen leaf.
- **Min-sum loses little.** The min-sum $f$ needs no tables or exponentials. It is scale invariant, so the decoder needs no estimate of $\sigma^2$. It can change some decisions compared with the exact $f$: on the $[4, 3, 2]$ single parity check code with $\mathcal{A} = \{1, 2, 3\}$ and $\lambda = (0.2, 1.3, 3.0, -0.3)$, exact SC outputs $0000$ and maximum likelihood outputs $1001$, while min-sum SC agrees with maximum likelihood.
- **Optimal on its own code family.** With the information set of the polar code and $N \to \infty$, SC reaches the symmetric capacity (Arıkan 2009).

## Variants and improvements

- **SC list (SCL).** Keep up to $L$ decision paths, extend each path with both values at each information bit, and keep the $L$ paths with the best metric. In the LLR domain the metric of a path adds $\ln(1 + e^{-(1 - 2\hat u_i)\lambda_i})$ at each leaf (Balatsoukas-Stimming, Bastani Parizi and Burg 2015). The time is $O(L N \log N)$ with lazy copying (Tal and Vardy 2015). With $L = 2^K$, SCL is maximum likelihood.
- **CRC-aided SCL.** Put a [cyclic redundancy check](/cyclic-redundancy-check/) in the message and output the best path that passes it. 5G NR uses this decoder for polar codes.
- **Simplified and fast SC.** Recognize subtrees whose frozen pattern gives a rate-zero, rate-one, repetition or single parity check code, and decode them in one step by maximum likelihood. On rate-zero, rate-one and repetition subtrees this gives the same output as SC. On single parity check subtrees it can be better, as the $[4, 3, 2]$ example above shows. The number of sequential steps falls by a large factor.
- **SC flip.** If the CRC fails, run SC again with the least reliable information decision flipped.
- **Belief propagation on the factor graph.** Pass messages in both directions over the $n$ stages of butterflies, as in [belief propagation decoding](/belief-propagation-decoding/). It is parallel but usually weaker than SCL.

## When to use it

Use SC for long polar codes when the hardware must be small, and as the inner step of SCL and CA-SCL. Use it to compute the design of a polar code by simulation, because its error events are the errors of single synthetic channels. For short and medium codes at a target frame error rate, use CA-SCL with $L = 8$ or more. In the length 64 experiment on the [polar code](/polar-code/) page, CA-SCL with $L = 8$ had 11 frame errors where SC had 123. Do not use SC on a code that is not designed for it, such as a [Reed-Muller code](/reed-muller-code/) with a large minimum distance: the code may be strong but SC on it is weak.

## Pitfalls

- **g with the wrong bits.** Line L8 must use the re-encoded bits $x_a[j]$ of the first half, not the decided input bits $\hat u_a[j]$. With $\hat u_a = (0, 0, 0, 1)$ in place of $x_a = (1, 1, 1, 1)$, the example gets the LLR 0 at leaf 4 in place of 2.
- **Wrong re-encoding.** Line L10 must return $(x_a \oplus x_b) \,\|\, x_b$. Returning $x_a \,\|\, x_b$ gives the wrong partial sums to the caller, and the error shows only for $N \ge 4$.
- **Bit-reversed order.** If the encoder uses $G_N = B_N F^{\otimes n}$, permute the LLRs by the [bit-reversal permutation](/bit-reversal-permutation/) before line L1. Without that, the decoder reads each LLR at the wrong position.
- **Overflow in the exact f.** Computing $\tanh$ and $\operatorname{artanh}$ directly fails for large $|a|$ or $|b|$, because the product rounds to $\pm 1$. Use $f(a, b) = \operatorname{sign}(a)\operatorname{sign}(b)\min(|a|, |b|) + \ln(1 + e^{-|a+b|}) - \ln(1 + e^{-|a-b|})$, which is exact and stable, or use min-sum.
- **Frozen leaf decided from its LLR.** Line L3 must output the frozen value for a frozen leaf. A decoder that takes the sign there passes the error into the partial sums.

## Implementations

## History

Erdal Arıkan defined SC decoding in his 2009 paper on channel polarization. He proved that polar codes with SC decoding reach the symmetric capacity, and gave the $O(N \log N)$ recursive form. Tal and Vardy turned SC into a list decoder in 2011, with the journal version in 2015, and showed that a CRC makes the list decoder much stronger. Balatsoukas-Stimming, Bastani Parizi and Burg wrote the list decoder in the LLR domain in 2015, which is the form used in hardware.

## References
