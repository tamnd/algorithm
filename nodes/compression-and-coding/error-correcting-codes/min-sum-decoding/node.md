---
tag: TA9NEY
kind: algorithm
slug: min-sum-decoding
name: Min-sum decoding
aliases:
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Belief propagation decoding with the tanh rule at each check replaced by a sign product and the least incoming magnitude, with normalized and offset corrections.
model: word-ram
complexity:
  vars: {E: the number of edges of the Tanner graph, I: the number of iterations}
  time: {worst: Θ(I E)}
  space: {extra: Θ(E)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1996
  people: [Niclas Wiberg, Marc P. C. Fossorier, Jinghu Chen]
  note: Wiberg described the min-sum algorithm on graphs of codes in 1996. Fossorier, Mihaljević and Imai studied it for LDPC codes in 1999, and Chen and Fossorier gave the normalized and offset corrections in 2002.
prereqs: [belief-propagation-decoding, tanner-graph]
see_also: [ldpc-code, bit-flipping-decoding, symbol-by-symbol-map-decoding, maximum-likelihood-sequence-estimation, max-product, viterbi-algorithm, loopy-belief-propagation, scalar-quantization]
sources:
  - paper: "N. Wiberg, Codes and decoding on general graphs, PhD thesis, Linköping University, 1996"
    title: Codes and decoding on general graphs
    locator: The min-sum algorithm on graphs of codes, its exactness on cycle-free graphs, and its relation to the Viterbi algorithm
  - paper: "M. P. C. Fossorier, M. Mihaljević and H. Imai, Reduced complexity iterative decoding of low-density parity check codes based on belief propagation, IEEE Transactions on Communications 47(5), 1999, pages 673 to 680"
    title: Reduced complexity iterative decoding of low-density parity check codes based on belief propagation
    locator: The BP-based (min-sum) check update for LDPC codes, which needs no knowledge of the noise level
  - paper: "J. Chen and M. P. C. Fossorier, Density evolution for two improved BP-based decoding algorithms of LDPC codes, IEEE Communications Letters 6(5), 2002, pages 208 to 210"
    title: Density evolution for two improved BP-based decoding algorithms of LDPC codes
    locator: The normalized and offset BP-based check updates, and the choice of the factor and the offset by density evolution
  - paper: "J. Chen, A. Dholakia, E. Eleftheriou, M. P. C. Fossorier and X.-Y. Hu, Reduced-complexity decoding of LDPC codes, IEEE Transactions on Communications 53(8), 2005, pages 1288 to 1299"
    title: Reduced-complexity decoding of LDPC codes
    locator: Normalized and offset min-sum with quantized messages, and their performance against belief propagation
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 17 (iterative decoding of LDPC codes, including the min-sum approximation of the sum-product algorithm)
---

Min-sum decoding is the cheap form of [belief propagation decoding](/belief-propagation-decoding/) for [LDPC codes](/ldpc-code/) and other codes with a sparse parity-check matrix. It works on the [Tanner graph](/tanner-graph/) of the matrix, with the channel LLRs as input, and passes the same messages on the same schedule. Only the check rule changes: the outgoing message keeps the sign that the tanh rule gives, and its size is the least size among the other incoming messages. This needs only comparisons and additions, and it does not need the noise level. The price is a loss in error rate, because the messages are too large. The normalized and offset forms of Chen and Fossorier shrink them and recover most of the loss. On a tree, min-sum computes the max-log LLRs of the bits, the soft form of maximum likelihood decoding. It is the code form of the [max-product](/max-product/) algorithm of the machine learning area, in the log domain.

## In plain words

Each check tells each of its bits what the other bits of the check imply. Belief propagation computes how sure that hint is with a formula of hyperbolic functions. Min-sum uses a simple rule instead: a chain is only as strong as its weakest link. The hint has the sign that makes the check even, and its strength is that of the least sure of the other bits.

This rule is too confident, because several uncertain bits together are less sure than the least sure of them. So the corrected forms multiply each hint by a number a little below 1, or subtract a small constant. Everything else, the sums at the bits and the stop when all checks hold, is the same as in belief propagation.

## The problem

A codeword $c$ of $C = \{c : H c^T = 0\}$, with $H$ an $m \times n$ binary matrix, is sent over a memoryless channel, and the receiver has the channel LLRs $L_j = \ln P(y_j \mid c_j = 0) / P(y_j \mid c_j = 1)$. The goal is decisions with a low error rate, at less cost per edge than belief propagation and, if possible, without an estimate of the noise. On BPSK over AWGN, $L_j = 2 y_j / \sigma^2$, and plain min-sum can use $y_j$ itself.

## The algorithm

$N(i)$ is the set of variables of check $i$ and $M(j)$ the set of checks of variable $j$. The schedule is flooding. The correction is one of: plain, $g(x) = x$; normalized, $g(x) = \alpha x$ with $0 < \alpha \le 1$; offset, $g(x) = \max(x - \beta, 0)$ with $\beta \ge 0$.

```pseudo id=main
MIN-SUM-DECODE(H, L, I, g)
L1  for each edge (i, j): q_{j→i} ← L_j                                 ▷ variable to check
L2  for it ← 1 to I do
L3      for each check i: a_i ← an edge of i with the least |q|; m1_i ← that |q|; m2_i ← the least |q| of the other edges
L4      for each edge (i, j): s ← sgn q_{j→i} · Π_{k ∈ N(i)} sgn q_{k→i}          ▷ sign of the others
L5      for each edge (i, j): r_{i→j} ← s · g(m2_i if j = a_i, else m1_i)
L6      for each j: Λ_j ← L_j + Σ_{i ∈ M(j)} r_{i→j}; ĉ_j ← 0 if Λ_j ≥ 0, else 1
L7      if H ĉ^T = 0 then return (ĉ, Λ, success)
L8      for each edge (i, j): q_{j→i} ← Λ_j − r_{i→j}                           ▷ leave out what came from i
L9  return (ĉ, Λ, failure)
```

Lines L3 to L5 give each edge $(i, j)$ the message $\bigl(\prod_{k \ne j} \operatorname{sgn} q_{k \to i}\bigr) \, g\bigl(\min_{k \ne j} |q_{k \to i}|\bigr)$, but with one pass over the check: the least size over the others is $m_1$ for every edge except the one that holds it, which gets $m_2$. Lines L1, L2 and L6 to L9 are those of belief propagation. A check with one edge has no other edges; the implementation then sends a very large positive message, which forces that bit to 0.

## Example

**The Hamming code, where plain min-sum is too confident.** Take the [Hamming code](/hamming-code/) with checks $\{0, 2, 3, 4\}$, $\{0, 1, 2, 5\}$ and $\{1, 2, 3, 6\}$, the codeword 0000000 and the channel LLRs

$$L = (2.0,\ 1.5,\ -0.8,\ 2.2,\ 1.8,\ 2.5,\ 1.2),$$

the same as on the belief propagation page. Bit 2 has the wrong sign, and it is in all three checks. So each check has one negative input, and in iteration 1 each check sends $-0.8$ to every bit except bit 2, and the least other size with a plus sign to bit 2:

| check | to bit 2 | to the other bits |
|---|---|---|
| 0 | $+\min(2.0, 2.2, 1.8) = 1.8$ | $-0.8$ to bits 0, 3, 4 |
| 1 | $+\min(2.0, 1.5, 2.5) = 1.5$ | $-0.8$ to bits 0, 1, 5 |
| 2 | $+\min(1.5, 2.2, 1.2) = 1.2$ | $-0.8$ to bits 1, 3, 6 |

The posteriors after iteration 1 are $(0.4, -0.1, 3.7, 0.6, 1.0, 1.7, 0.4)$. Bit 2 is fixed, but bit 1 now has the wrong sign: it got $-0.8$ twice. The word 0100000 is not a codeword, so the decoder goes on, and after iteration 2 the posteriors are $(4.1, 3.9, 1.8, 4.1, 3.0, 3.2, 1.9)$ and it returns 0000000.

Belief propagation decodes the same word in one iteration. Its message from check 0 to bit 0 is $2 \operatorname{artanh}(\tanh(-0.4) \tanh(1.1) \tanh(0.9)) = -0.443$, against $-0.8$ for min-sum: three uncertain bits together are less sure than the least sure of them. The corrections fix this here. Normalized min-sum with $\alpha = 0.8$ gives the posteriors $(0.72, 0.22, 2.8, 0.92, 1.16, 1.86, 0.56)$ after iteration 1, and offset min-sum with $\beta = 0.15$ gives $(0.7, 0.2, 3.25, 0.9, 1.15, 1.85, 0.55)$. Both stop after one iteration.

**Max-log on a tree.** The checks $\{0, 1, 2\}$, $\{2, 3, 4\}$, $\{4, 5\}$ and $\{1, 6, 7\}$ give a tree with 4 checks on its longest path. With the LLRs $(-1.3, 2.2, 1.8, -0.7, 0.5, 0.2, 1.3, 1.9)$ and no early stop, plain min-sum gives after 4 iterations and later

$$(-0.2,\ 2.4,\ -0.2,\ -0.2,\ 0.2,\ 0.2,\ 2.4,\ 3.0).$$

These are the max-log LLRs: for bit 0, the best codeword with $c_0 = 1$ is 10110000, with $\sum_k c_k L_k = -1.3 + 1.8 - 0.7 = -0.2$, and the best with $c_0 = 0$ is 00000000, with 0. The signs give the ML codeword 10110000. Belief propagation on the same tree gives the exact posterior $+0.086$ for bit 0, so the bitwise MAP decision of bit 0 is 0: min-sum on a tree is maximum likelihood decoding of the word, and belief propagation is MAP decoding of each bit. The test compares min-sum with brute-force max-log LLRs for 200 random LLR vectors.

**Monte Carlo.** On a $(3, 6)$-regular Gallager code with $n = 96$, BPSK on AWGN at $E_b/N_0 = 2$ dB and 60 frames, with at most 30 iterations, the bit errors were 125 for plain min-sum, 107 for normalized min-sum with $\alpha = 0.8$, 106 for offset min-sum with $\beta = 0.5$, and 725 for hard-decision [bit flipping](/bit-flipping-decoding/). Belief propagation on the same frames had 83. So the order is belief propagation, then corrected min-sum, then plain min-sum, then bit flipping.

## Correctness

- **The check rule is max-log.** For bits with LLRs $\ell_k$, the best configuration of even parity minus the best of odd parity, in log weights, is $\bigl(\prod_k \operatorname{sgn} \ell_k\bigr) \min_k |\ell_k|$: the free best choice takes each bit by its sign, and the cheapest way to change the parity flips the least sure bit. So lines L3 to L5 with $g(x) = x$ give the max-log LLR of the XOR of the other bits of the check.
- **Two least values.** For every edge except the one with the least size, the least size over the others is $m_1$; for that edge it is $m_2$. The tests compare the decoder with a direct per-edge version for all three corrections.
- **Trees.** The tree argument of belief propagation goes through with $(\max, +)$ in place of $(+, \times)$. After as many iterations as the longest path has checks, the posterior of line L6 is $\min_{c \in C, c_j = 1} \sum_k c_k L_k - \min_{c \in C, c_j = 0} \sum_k c_k L_k$, and its signs give the ML codeword when it is unique.
- **Overestimate.** $|2 \operatorname{artanh} \prod_k \tanh(\ell_k / 2)| \le \min_k |\ell_k|$ with the same sign, so the plain message is never smaller than the belief propagation message from the same inputs. Normalization and offset reduce the size without a change of sign.
- **The output.** Line L7 returns only words that satisfy all checks.

The [correctness proof](proofs/correctness.md) has the details. With cycles the result is an approximation, as for belief propagation.

## Complexity

Line L3 takes one pass over the $d_i$ edges of check $i$ to find the least and second least sizes and the sign product, and lines L4 and L5 take one more pass. So an iteration takes $\Theta(E)$ time, against $\Theta(\sum_i d_i^2)$ for the direct tanh rule of the belief propagation implementation. The memory is $\Theta(E)$ for the messages. A hardware check node can store only $m_1$, $m_2$, the index $a_i$ and the signs, instead of one message per edge.

## Properties

- Exact max-log on a tree, which is maximum likelihood decoding of the word; approximate with cycles.
- Plain and normalized min-sum are scale invariant: multiplying all LLRs by $s > 0$ multiplies every message by $s$ and does not change any decision, so they need no estimate of $\sigma^2$. Offset min-sum needs the LLR scale, because $\beta$ is in LLR units.
- The check update uses only comparisons, sign products and, for the corrections, one multiply or subtract.
- The decision on the stop is a codeword, but not always the ML or the bitwise MAP decision.

## Variants and improvements

- **Normalized min-sum.** Multiply the size by $\alpha < 1$. Chen and Fossorier chose $\alpha$ by density evolution for each pair of degrees.
- **Offset min-sum.** Subtract $\beta > 0$ and stop at 0. In hardware it needs only a subtraction, and a message smaller than $\beta$ becomes 0, which means "no information".
- **Layered schedule.** Update the checks one group at a time and use the new messages at once, as in belief propagation. Layered normalized or offset min-sum is a common choice in hardware decoders of quasi-cyclic LDPC codes.
- **Quantized messages.** Min-sum works well with messages of a few bits, because it never needs a nonlinear function, as Chen, Dholakia, Eleftheriou, Fossorier and Hu showed. See [scalar quantization](/scalar-quantization/).
- **Self-correcting and adaptive forms.** Some forms erase a variable message whose sign changed in the last iteration, or use a different $\alpha$ for each iteration.
- **Min-sum on a trellis.** The same rule on a trellis is the [Viterbi algorithm](/viterbi-algorithm/), and its two-sided form is the max-log BCJR algorithm.

## When to use it

- Use it in hardware LDPC decoders, where the tanh rule is too costly, and when the noise level is not known.
- Use the normalized or offset form unless there is a reason not to: they cost almost nothing more and remove most of the gap to belief propagation.
- Use full belief propagation when the best error rate matters more than the cost, and [bit flipping](/bit-flipping-decoding/) when only hard decisions are available.

## Pitfalls

- **Plain min-sum is too confident.** Its messages are never smaller than those of belief propagation, so wrong bits can spread, as bit 1 did in the example. Use a correction.
- **A wrong correction.** $\alpha$ too small or $\beta$ too large makes the decoder too slow to decide. The best values depend on the degrees of the code and, for $\beta$, on the LLR scale.
- **The two-least shortcut and ties.** If two edges share the least size, $m_2 = m_1$, and every edge gets $m_1$. This is correct, but a version that searches for "the second least distinct value" is wrong.
- **Checks of degree one.** The minimum over an empty set must give "the bit is 0 for sure", not 0. Such checks are unusual but appear in punctured or shortened codes.
- **Oscillation.** With cycles, plain min-sum can switch between two words without stopping. An iteration limit and the flag of line L9 are needed.

## Implementations

## History

Wiberg, Loeliger and Kötter in 1995 and Wiberg in his 1996 thesis described the min-sum algorithm on general graphs of codes and showed that the Viterbi algorithm is a special case. Fossorier, Mihaljević and Imai in 1999 proposed the BP-based check update for LDPC codes and noted that it needs no noise estimate. Chen and Fossorier in 2002 analyzed the normalized and offset forms by density evolution and showed that they come close to belief propagation. Chen, Dholakia, Eleftheriou, Fossorier and Hu in 2005 studied them with quantized messages, and these forms became the standard check update in hardware decoders.

## References
