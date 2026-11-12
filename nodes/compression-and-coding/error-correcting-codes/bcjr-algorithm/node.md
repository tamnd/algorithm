---
tag: PCHCXC
kind: algorithm
slug: bcjr-algorithm
name: BCJR algorithm
aliases:
- BCJR
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Compute the exact a posteriori LLR of every bit of a trellis code with one forward and one backward pass over the trellis, from channel LLRs and prior LLRs.
solves: [symbol-by-symbol-map-decoding]
model: word-ram
complexity:
  vars: {T: the number of trellis steps, S: the number of states per step, E: the number of edges, n: the code bits per edge}
  time: {worst: Θ(E n), total: Θ(T S n)}
  space: {extra: Θ(T S)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1974
  people: [Lalit Bahl, John Cocke, Frederick Jelinek, Josef Raviv]
  note: Bahl, Cocke, Jelinek and Raviv gave the algorithm in 1974 for convolutional and linear block codes. It was little used until turbo codes in 1993 needed soft outputs, and the log domain forms followed in the middle of the 1990s.
prereqs: [trellis, forward-backward-algorithm, symbol-by-symbol-map-decoding]
see_also: [maximum-likelihood-sequence-estimation, turbo-decoding, turbo-code, convolutional-code, viterbi-algorithm, hidden-markov-model, belief-propagation-decoding, dag-dynamic-programming]
sources:
  - paper: doi:10.1109/TIT.1974.1055186
    title: L. R. Bahl, J. Cocke, F. Jelinek and J. Raviv, Optimal decoding of linear codes for minimizing symbol error rate, IEEE Transactions on Information Theory 20(2), 1974, pages 284 to 287
    locator: The forward and backward recursions for the state and transition probabilities of a Markov source observed through a memoryless channel, and their use for convolutional and block codes
  - paper: "P. Robertson, E. Villebrun and P. Hoeher, A comparison of optimal and sub-optimal MAP decoding algorithms operating in the log domain, Proceedings of the IEEE International Conference on Communications (ICC), 1995"
    title: A comparison of optimal and sub-optimal MAP decoding algorithms operating in the log domain
    locator: The log-MAP algorithm with the correction term of the Jacobian logarithm, and its comparison with max-log-MAP
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 12 (the BCJR algorithm for convolutional codes, its log domain form and the max-log approximation)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 25 (exact marginalization in trellises, the forward and backward passes for the bitwise posterior)
---

The BCJR algorithm computes, for each information bit $u_t$ of a code with a [trellis](/trellis/), the exact posterior log-likelihood ratio $L(u_t) = \ln P(u_t = 0 \mid y) / P(u_t = 1 \mid y)$ given the whole channel output $y$. It does this with one forward pass and one backward pass over the trellis, each with a constant amount of work per edge. Its input is the code trellis, one channel LLR per code bit and an optional prior LLR per input bit. Its sign gives [symbol-by-symbol MAP decoding](/symbol-by-symbol-map-decoding/), and its magnitude is the soft output that the constituent decoders of [turbo decoding](/turbo-decoding/) exchange. It is the [forward-backward algorithm](/forward-backward-algorithm/) of hidden Markov models, applied to a code trellis with channel LLRs.

## In plain words

The Viterbi algorithm finds the single best path through the trellis. BCJR asks a different question: of all the paths, weighted by how well they fit the received signal, how much weight has a 0 at this position and how much has a 1?

The forward pass walks left to right and stores, for each state, the total weight of all path starts that end there. The backward pass walks right to left and stores the total weight of all path ends that start there. For one edge, the weight of all full paths through it is the forward value at its left end, times the edge weight, times the backward value at its right end. Add these over the edges with input 0 and over the edges with input 1, and take the log of the ratio. No path is ever listed.

## The problem

**Trellis.** Steps $t = 0, \ldots, T - 1$. An edge $e$ of step $t$ goes from state $s(e)$ at time $t$ to state $s'(e)$ at time $t + 1$, and carries an input bit $u(e)$ and code bits $x(e) = (x_1(e), \ldots, x_n(e))$. Paths start in state 0. A terminated code ends in state 0; otherwise any end state is allowed.

**Channel.** Each code bit $c$ is sent as $1 - 2c$ over a memoryless channel. The channel LLR of the $j$th bit of step $t$ is $L_c(y_{t,j}) = \ln P(y_{t,j} \mid c = 0) / P(y_{t,j} \mid c = 1)$, which is $2 y_{t,j} / \sigma^2$ on the [AWGN channel](/additive-white-gaussian-noise-channel/) with BPSK and noise variance $\sigma^2$. The input bits are independent with prior LLRs $L_a(u_t)$, which are 0 when nothing is known.

**Task.** Output $L(u_t) = \ln \dfrac{P(u_t = 0 \mid y)}{P(u_t = 1 \mid y)}$ for every $t$. The decision $\hat u_t = 1$ if and only if $L(u_t) < 0$ minimizes the probability that bit $t$ is wrong.

## The algorithm

Each edge gets the branch weight

$$\gamma_t(e) = \exp\Bigl(\tfrac12 (1 - 2u(e)) L_a(u_t) + \tfrac12 \sum_{j=1}^{n} (1 - 2x_j(e)) L_c(y_{t,j})\Bigr),$$

which is $P(u(e))\, P(y_t \mid x(e))$ times a factor that is the same for all edges of step $t$.

```pseudo id=main
BCJR(trellis, γ)                        ▷ T steps, γ_t(e) for each edge e of step t
L1  α_0(0) ← 1, and α_0(s) ← 0 for every other state s
L2  for t ← 0 to T − 1 do  α_{t+1}(s′) ← Σ over edges e of step t with s′(e) = s′ of α_t(s(e)) γ_t(e)
L3      divide every α_{t+1}(s′) by Σ_s′ α_{t+1}(s′)
L4  β_T(s) ← 1 for each allowed end state s, and 0 for the others
L5  for t ← T − 1 downto 0 do  β_t(s) ← Σ over edges e of step t with s(e) = s of γ_t(e) β_{t+1}(s′(e))
L6      divide every β_t(s) by Σ_s β_t(s)
L7  for t ← 0 to T − 1 do  p_t(b) ← Σ over edges e of step t with u(e) = b of α_t(s(e)) γ_t(e) β_{t+1}(s′(e))
L8      L(u_t) ← ln p_t(0) − ln p_t(1)      ▷ the output list
```

The divisions on lines L3 and L6 keep the numbers in range; they do not change the result, because the common factors cancel in the ratio of line L8. The implementation also has the two log domain modes of the section on variants.

## Example

**The (7, 5) code on the AWGN channel.** The [convolutional code](/convolutional-code/) with generators 111 and 101 encodes the message 1011 and two tail zeros as 11 10 00 01 01 11, sent as $\pm 1$ with $\sigma^2 = 1$, so $L_c = 2y$. The receiver gets

$$y = (-0.8, -1.1,\ 0.3, 0.9,\ 1.2, -0.2,\ 0.7, -0.6,\ 1.0, -1.3,\ -0.6, -0.9).$$

The first sample of step 2 and the second sample of step 3 have the wrong sign. The trellis has 4 states, 6 steps and 28 edges, and 16 paths, one per message. With $L_a = 0$ the outputs for the four message bits are:

| bit $t$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| sent $u_t$ | 1 | 0 | 1 | 1 |
| BCJR $L(u_t)$ | $-5.102$ | $5.426$ | $-6.039$ | $-6.632$ |
| max-log $\tilde L(u_t)$ | $-5.2$ | $6.2$ | $-6.6$ | $-7.6$ |

All four signs are right. The values are equal to the brute-force posteriors over the 16 paths to $10^{-9}$. With the path metric $\tfrac12 \sum (1 - 2c) L_c$, the best path is the message 1011 with metric 8.6, and the best path with $u_1 = 1$ is the message 1111 with metric 2.4. So $\tilde L(u_1) = 8.6 - 2.4 = 6.2$. The exact LLR $5.426$ is smaller, because it also counts the other paths with $u_1 = 1$.

## Correctness

The weight $\prod_t \gamma_t(e_t)$ of a path is proportional to its posterior probability, because paths and input sequences are in one to one correspondence and the channel is memoryless. The unnormalized forward value $A_t(s)$ is the sum of the weights of the partial paths from state 0 to $s$, and the backward value $B_{t+1}(s')$ is the sum over the partial paths from $s'$ to an allowed end state. Both recursions hold by splitting each path at its last or first edge and using the distributive law. A full path through edge $e$ is a partial path to $s(e)$, then $e$, then a partial path from $s'(e)$, so the sum of the weights of the paths through $e$ is $A_t(s(e))\, \gamma_t(e)\, B_{t+1}(s'(e))$. Summing over the edges with $u(e) = b$ gives $P(u_t = b \mid y)$ times a factor that does not depend on $b$. The full proof, with the log domain identity and the error bound of max-log, is in the [correctness proof](proofs/correctness.md).

## Complexity

Each pass visits each edge once and does a constant number of multiplications and additions, plus $n$ terms for the branch weight. So the time is $\Theta(E n)$ for $E$ edges. A rate $1/n$ binary code with memory $m$ has $S = 2^m$ states and $2S$ edges per step, so $E = \Theta(T S)$ and the time is $\Theta(T S n)$. The Viterbi algorithm on the same trellis makes one pass and keeps only survivors, so BCJR costs more by a constant factor. The memory is $\Theta(T S)$ for the stored forward values. A sliding window version stores only a window of $W$ steps and starts each backward pass from uniform values $W$ steps ahead, which costs $\Theta(W S)$ memory and gives approximate outputs.

## Properties

- The output is exact for any trellis and any memoryless channel, with or without termination.
- The decisions minimize the bit error probability, which is a different goal from the sequence error probability of [MLSE](/maximum-likelihood-sequence-estimation/). The two decoders can disagree on a bit; the [symbol-by-symbol MAP decoding](/symbol-by-symbol-map-decoding/) page has an example.
- The output splits as $L(u_t) = L_a(u_t) + L_c(y_{t,1}) + L_e(u_t)$ for a systematic code whose first code bit is $u_t$. The *extrinsic* part $L_e(u_t)$ depends only on the other inputs to the decoder, and it is what one decoder passes to the other in turbo decoding.
- It is the [forward-backward algorithm](/forward-backward-algorithm/) on the hidden Markov model whose hidden states are the trellis states. On the code trellis the transitions are fixed by the code and weighted only by the input priors.

## Variants and improvements

- **Log-MAP.** Work with $\ln \alpha$, $\ln \beta$ and $\ln \gamma$. Products become sums, and a sum $\ln(e^a + e^b)$ becomes $\max^*(a, b) = \max(a, b) + \ln(1 + e^{-|a - b|})$. This is exact and needs no normalization. The correction term takes values in $(0, \ln 2]$ and is often read from a small table.
- **Max-log-MAP.** Replace $\max^*$ by $\max$. The forward pass is then the Viterbi algorithm, and $\tilde L(u_t)$ is the difference of the best path metrics with $u_t = 0$ and $u_t = 1$. It does not depend on a scale factor of the channel LLRs, so the decoder does not need to know $\sigma^2$. The error of each output is at most the logarithm of the number of paths.
- **Soft-output Viterbi algorithm (SOVA).** Run Viterbi and estimate the reliability of each decision from the metric differences along the survivor. It is cheaper and less accurate than max-log-MAP.
- **Sliding window and parallel windows.** Split a long block into windows with a short training run for $\beta$ at each window end. This is how hardware turbo decoders bound their memory and run windows in parallel.
- **Block codes.** The same recursions on the syndrome trellis of a linear block code give the bitwise posteriors of its code bits; this was part of the 1974 paper.

## When to use it

- Use BCJR when the decoder must output soft information, as in iterative decoding of turbo codes and serial concatenations, and in turbo equalization.
- Use it when the goal is the least bit error rate. When only hard decisions are needed, the Viterbi algorithm gives almost the same bit error rate with less work and memory.
- Use max-log-MAP in hardware or when the noise variance is not known, and log-MAP when the last few tenths of a decibel matter.

## Pitfalls

- **Underflow.** Products of hundreds of $\gamma$ values underflow in floating point. Normalize at each step as on lines L3 and L6, or work in the log domain.
- **The wrong start of $\beta$.** For a terminated code $\beta_T$ is 1 only at state 0. For an unterminated code it must be uniform over the end states; starting it at state 0 makes the last bits wrong with high confidence.
- **The sign convention.** This page uses $L = \ln P(0) / P(1)$, so a positive LLR means 0 and BPSK maps 0 to $+1$. Mixing this with the opposite convention flips every decision.
- **Wrong channel scaling.** Log-MAP needs $L_c = 2y/\sigma^2$ with the true $\sigma^2$; a wrong scale gives wrong posteriors, while max-log-MAP decisions are not affected.
- **Passing the full posterior in turbo decoding.** A constituent decoder must pass only $L_e(u_t)$, not $L(u_t)$, or the other decoder counts the same evidence twice.

## Implementations

## History

Bahl, Cocke, Jelinek and Raviv published the algorithm in 1974, for both convolutional codes and linear block codes, with the trellis of a block code built from partial syndromes. For about twenty years it saw little use, because it costs more than the Viterbi algorithm and gives almost the same bit error rate on its own. The turbo codes of Berrou, Glavieux and Thitimajshima in 1993 needed exact soft outputs from each constituent decoder, and a modified BCJR algorithm was the decoder they used. Robertson, Villebrun and Hoeher compared the log-MAP and max-log-MAP forms in 1995. The same recursions had appeared earlier in the statistics of hidden Markov models, in the work of Baum and Welch.

## References
