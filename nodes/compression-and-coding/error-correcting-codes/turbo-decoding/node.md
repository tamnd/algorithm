---
tag: SCF5ND
kind: algorithm
slug: turbo-decoding
name: Turbo decoding
aliases:
- iterative turbo decoding
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Decode a turbo code by running a BCJR decoder on each constituent trellis in turn, each passing its extrinsic LLRs to the other through the interleaver as prior LLRs.
model: word-ram
complexity:
  vars: {N: the message length, I: the number of iterations, S: the number of states of a constituent encoder}
  time: {worst: Θ(I N S)}
  space: {extra: Θ(N S)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1993
  people: [Claude Berrou, Alain Glavieux, Punya Thitimajshima, Joachim Hagenauer, Robert J. McEliece, Stephan ten Brink]
  note: Berrou, Glavieux and Thitimajshima gave the iterative decoder with the turbo code in 1993. Hagenauer, Offer and Papke wrote it in LLR form in 1996, McEliece, MacKay and Cheng showed in 1998 that it is belief propagation, and ten Brink gave EXIT charts in 2001.
prereqs: [turbo-code, bcjr-algorithm]
see_also: [belief-propagation-decoding, loopy-belief-propagation, symbol-by-symbol-map-decoding, interleaving, ldpc-code, convolutional-code, cyclic-redundancy-check, forward-backward-algorithm]
sources:
  - paper: doi:10.1109/ICC.1993.397441
    title: C. Berrou, A. Glavieux and P. Thitimajshima, Near Shannon limit error-correcting coding and decoding, turbo-codes, Proceedings of the IEEE International Conference on Communications (ICC), 1993, pages 1064 to 1070
    locator: The feedback decoder with two modified BCJR decoders and the exchange of extrinsic information
  - paper: "J. Hagenauer, E. Offer and L. Papke, Iterative decoding of binary block and convolutional codes, IEEE Transactions on Information Theory 42(2), 1996, pages 429 to 445"
    title: Iterative decoding of binary block and convolutional codes
    locator: The LLR algebra, the split of the soft output into channel, a priori and extrinsic parts, and the iterative decoder
  - paper: "R. J. McEliece, D. J. C. MacKay and J.-F. Cheng, Turbo decoding as an instance of Pearl's belief propagation algorithm, IEEE Journal on Selected Areas in Communications 16(2), 1998, pages 140 to 152"
    title: "Turbo decoding as an instance of Pearl's belief propagation algorithm"
    locator: The turbo decoder as belief propagation on a graph with cycles
  - paper: "S. ten Brink, Convergence behavior of iteratively decoded parallel concatenated codes, IEEE Transactions on Communications 49(10), 2001, pages 1727 to 1737"
    title: Convergence behavior of iteratively decoded parallel concatenated codes
    locator: The extrinsic information transfer (EXIT) chart and the prediction of the turbo cliff
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 16 (iterative decoding of turbo codes with the log-MAP and max-log-MAP algorithms)
---

Turbo decoding is the iterative decoder of a [turbo code](/turbo-code/). It runs a [BCJR](/bcjr-algorithm/) decoder on the trellis of the first constituent code, removes from each output the parts that the second decoder already knows, and gives the rest, the *extrinsic* LLRs, to the second decoder as prior LLRs through the [interleaver](/interleaving/). The second decoder does the same in the other direction, and the two take turns for a fixed number of iterations or until a check passes. Each half iteration is exact for its own code, but the whole is an approximation of [symbol-by-symbol MAP decoding](/symbol-by-symbol-map-decoding/) of the turbo code. It works on the two code trellises with channel LLRs; it is the code form of [loopy belief propagation](/loopy-belief-propagation/), with each trellis handled as one exact block.

## In plain words

Two experts each check a different half of the evidence about the same secret message. The first expert reads the message bits and the first set of check bits, and forms an opinion on each bit. It then tells the second expert only what its check bits added, not what the message bits said, because the second expert can read those itself.

The second expert uses this as a starting opinion, adds its own check bits, and again sends back only the new part. After a few rounds the two opinions agree, and the message is read from them. The rule of passing on only new information keeps each expert from hearing its own evidence again and becoming too sure.

## The problem

A message $u$ of $N$ bits was encoded by the turbo encoder with interleaver $u'_i = u_{\pi(i)}$, and both constituent encoders were terminated. The receiver has the channel LLRs of the systematic bits $L_s(t)$, of the two parity streams $L_{p1}(t)$ and $L_{p2}(t)$, and of the tail bits. It wants the decisions $\hat u_t$ with a low bit error rate. Exact bitwise MAP decoding of the whole turbo code would need a sum over all $2^N$ messages, because the turbo code has no small trellis.

## The algorithm

All LLRs are $\ln P(0) / P(1)$. BCJR($c$, $L_s$, $L_p$, $\lambda$) is the log-MAP BCJR algorithm on the trellis of constituent code $c$, with systematic channel LLRs $L_s$, parity LLRs $L_p$, and prior LLRs $\lambda$ on the inputs (0 for the tail steps). It returns the posterior LLRs of the inputs.

```pseudo id=main
TURBO-DECODE(L_s, L_p1, L_p2, π, I)
L1  λ1 ← (0, ..., 0)                                   ▷ no prior knowledge yet
L2  repeat I times
L3      Λ1 ← BCJR(code 1, L_s, L_p1, λ1)
L4      E1(t) ← Λ1(t) − λ1(t) − L_s(t) for each t        ▷ extrinsic of decoder 1
L5      λ2(i) ← E1(π(i)) for each i                      ▷ interleave
L6      Λ2 ← BCJR(code 2, L_s ∘ π, L_p2, λ2)
L7      E2(i) ← Λ2(i) − λ2(i) − L_s(π(i)) for each i     ▷ extrinsic of decoder 2
L8      λ1(π(i)) ← E2(i) for each i                      ▷ deinterleave
L9      û_{π(i)} ← 0 if Λ2(i) ≥ 0, else 1, for each i
```

Line L9 records the decisions of each iteration; the last ones are the output. The full posterior of bit $u_t$ after line L6 is $L_s(t) + E_1(t) + E_2(\pi^{-1}(t))$: the channel, the first code and the second code.

## Example

**A simulation where the iterations help.** The code is the rate 1/3 turbo code with two $(1, 5/7)$ RSC encoders of 4 states, a seeded random interleaver of $N = 128$ bits, BPSK on the AWGN channel at $E_b/N_0 = 1$ dB (so $\sigma^2 = 1/(2 R\, E_b/N_0)$ with $R = 1/3$), and 30 blocks, 3840 message bits in total. The errors after each iteration were:

| iteration | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| bit errors | 200 | 95 | 74 | 47 | 54 | 47 |
| block errors (of 30) | 25 | 14 | 10 | 7 | 8 | 8 |

The first iteration already uses both codes. The next three cut the bit errors by a factor of about 4. After that the count does not fall further and even goes up and down by a few bits, which is common in short blocks: the decoder can oscillate between two wrong guesses. The test asserts only that iteration 6 has fewer than half the bit errors of iteration 1.

**What the extrinsic value is.** In the test of the extrinsic rule, changing the prior and the systematic LLR of one bit changes the posterior of that bit by exactly the sum of the two changes, and leaves its extrinsic value the same to $10^{-9}$.

## Correctness

Turbo decoding has no theorem of the form "the output is the MAP decision". What holds exactly is this:

- Lines L3 and L6 return the exact posterior LLRs of each constituent code, with the priors treated as independent evidence. This is the correctness of BCJR.
- The extrinsic value of line L4 does not depend on the bit's own prior or systematic LLR. In the sum over paths, the factor of these two terms is a constant in each of the two sums with $u_t = 0$ and $u_t = 1$, so it comes out as the additive term $\lambda_t + L_s(t)$. Subtracting it keeps decoder 2 from receiving the systematic LLR of the bit twice.
- If the priors that decoder 2 receives were independent of its other inputs, line L6 would return the exact posterior of the turbo code. They are not, because the extrinsic value of one bit depends on the systematic LLRs of its neighbors, which decoder 2 also uses. The factor graph of a turbo code has cycles, and the algorithm is belief propagation on it.

The [correctness proof](proofs/correctness.md) gives the three statements with proofs. The value of the decoder in practice comes from simulations and from EXIT chart and density evolution analysis.

## Complexity

Each BCJR call takes $\Theta(N S)$ time for $S$ states, so $I$ iterations take $\Theta(I N S)$. The memory is $\Theta(N S)$ for the forward values of one BCJR call, plus $\Theta(N)$ for the LLRs. Sliding window BCJR cuts the $\Theta(N S)$ part. In practice 4 to 8 iterations are usual, and a stopping rule cuts the average.

## Properties

- The two constituent decoders exchange only extrinsic LLRs; the channel LLRs stay in each decoder.
- With log-MAP each half iteration is exact. With max-log-MAP the decoder does not need $\sigma^2$, but it loses some performance; scaling the extrinsic values by a fixed factor below 1 recovers much of the loss.
- The decoder is not guaranteed to converge. It can reach a fixed point that is not a codeword, or oscillate.
- The decoder has the order of the half iterations as a choice. Running both decoders at the same time on the previous extrinsic values is also possible, at some cost in speed of convergence.

## Variants and improvements

- **Max-log-MAP and SOVA constituent decoders.** Cheaper soft-output decoders in place of log-MAP.
- **Stopping rules.** Stop when a CRC of the decoded block passes, as in LTE, where each code block carries a CRC, or when the hard decisions do not change, or when the two decoders agree.
- **EXIT charts (ten Brink 2001).** Model the prior LLRs of a decoder as Gaussian with a given mutual information $I_A$ with the bits, and measure the mutual information $I_E$ of its extrinsic output. This gives one transfer curve $I_E = T_1(I_A)$ for each decoder at a given $E_b/N_0$. Plot $T_1$ and the inverse of $T_2$ on the same axes. The iterations follow a staircase between the two curves. If the curves leave an open tunnel up to $I = 1$, the decoder converges to a low error rate; the $E_b/N_0$ at which the tunnel first opens predicts the steep fall of the error rate, the turbo cliff.
- **Serial concatenation and turbo equalization.** The same exchange of extrinsic LLRs between an outer decoder and an inner decoder, or between an equalizer and a decoder.
- **Parallel and windowed hardware decoders.** Split the block into windows and run them at the same time. The QPP interleaver of LTE was chosen so that parallel windows do not collide in memory.

## When to use it

- Use it to decode turbo codes, and in general any concatenation of codes with soft-output decoders linked by an interleaver.
- For new systems, LDPC codes with [belief propagation decoding](/belief-propagation-decoding/) give similar performance with more parallel decoders, and 5G NR chose them for data. Turbo decoding remains in LTE, in 3G systems and in CCSDS space links.

## Pitfalls

- **Passing the full posterior in place of the extrinsic value.** Then each decoder hears its own evidence again, becomes too confident, and stops improving after one or two iterations.
- **Not subtracting the systematic LLR.** The systematic LLR is in both decoders, so it must be removed from the extrinsic value as on lines L4 and L7.
- **Interleaver direction.** With $u'_i = u_{\pi(i)}$, interleaving reads $E_1(\pi(i))$ and deinterleaving writes to position $\pi(i)$. Using $\pi^{-1}$ by mistake gives a decoder that runs but does not improve.
- **The tail of encoder 2.** Its tail inputs are not message bits, so they are sent and given to decoder 2 only, with prior 0.
- **Wrong noise variance.** Log-MAP needs channel LLRs with the right scale. A wrong $\sigma^2$ makes the exchanged values too strong or too weak.
- **Short blocks and the error floor.** More iterations do not remove the error floor; it comes from light codewords of the code itself.

## Implementations

## History

Berrou, Glavieux and Thitimajshima built the turbo decoder in 1993 as a feedback loop between two soft-output decoders, a design taken from the turbo engine, which gave the codes their name. Hagenauer, Offer and Papke wrote the algorithm in the LLR algebra in 1996 and showed that the same principle decodes block codes. In 1998 McEliece, MacKay and Cheng showed that it is belief propagation on a graph with cycles, which linked it to Gallager's decoder for LDPC codes and to Pearl's algorithm. ten Brink's EXIT charts of 2001 gave a simple way to predict when the iterations converge.

## References
