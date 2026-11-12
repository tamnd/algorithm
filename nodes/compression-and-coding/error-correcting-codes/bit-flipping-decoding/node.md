---
tag: 8C2WTA
kind: algorithm
slug: bit-flipping-decoding
name: Bit-flipping decoding
aliases:
- Gallager bit-flipping
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Hard-decision LDPC decoding on the Tanner graph that flips, in each round, the bits that are in the most unsatisfied checks. Gallager A and B and weighted flipping are its relatives.
model: word-ram
complexity:
  vars: {E: the number of edges of the Tanner graph, I: the number of rounds, m: the number of checks, n: the code length}
  time: {worst: Θ(I E)}
  space: {extra: Θ(m + n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1962
  people: [Robert G. Gallager, Michael Sipser, Daniel A. Spielman, Yu Kou, Shu Lin, Marc P. C. Fossorier]
  note: Gallager gave bit flipping and the hard message-passing algorithms A and B for LDPC codes in 1962 and 1963. Sipser and Spielman proved in 1996 that flipping corrects a constant fraction of errors on expanders. Kou, Lin and Fossorier added the weighted rule in 2001.
prereqs: [ldpc-code, tanner-graph]
see_also: [belief-propagation-decoding, min-sum-decoding, expander-codes, majority-logic-decoding, binary-symmetric-channel, syndrome, bike, maximum-likelihood-decoding]
sources:
  - paper: doi:10.1109/TIT.1962.1057683
    title: R. G. Gallager, Low-density parity-check codes, IRE Transactions on Information Theory 8(1), 1962, pages 21 to 28
    locator: The decoding of LDPC codes on the BSC by changing the digits that are in more than a set number of unsatisfied parity checks, and its probabilistic analysis on a tree
  - paper: "T. J. Richardson and R. L. Urbanke, The capacity of low-density parity-check codes under message-passing decoding, IEEE Transactions on Information Theory 47(2), 2001, pages 599 to 618"
    title: The capacity of low-density parity-check codes under message-passing decoding
    locator: Density evolution, with Gallager's algorithms A and B on the BSC as the first examples
  - paper: "L. Bazzi, T. J. Richardson and R. L. Urbanke, Exact thresholds and optimal codes for the binary-symmetric channel and Gallager's decoding algorithm A, IEEE Transactions on Information Theory 50(9), 2004, pages 2010 to 2021"
    title: Exact thresholds and optimal codes for the binary-symmetric channel and Gallager's decoding algorithm A
    locator: The threshold of algorithm A on regular ensembles, about 0.0394 for the (3, 6) ensemble
  - paper: "Y. Kou, S. Lin and M. P. C. Fossorier, Low-density parity-check codes based on finite geometries: a rediscovery and new results, IEEE Transactions on Information Theory 47(7), 2001, pages 2711 to 2736"
    title: "Low-density parity-check codes based on finite geometries: a rediscovery and new results"
    locator: The weighted bit-flipping algorithm, with check weights from the least reliable bit of each check
  - paper: "M. Sipser and D. A. Spielman, Expander codes, IEEE Transactions on Information Theory 42(6), 1996, pages 1710 to 1722"
    title: Expander codes
    locator: The sequential and parallel flipping decoders and the proof that they correct a constant fraction of errors when the graph expands
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 17 (hard-decision bit-flipping and weighted bit-flipping decoding of LDPC codes)
---

Bit-flipping decoding is the simplest iterative decoder of an [LDPC code](/ldpc-code/). It works on the [Tanner graph](/tanner-graph/) with hard decisions only: one bit per position, not channel LLRs. In each round it computes the [syndrome](/syndrome/), counts for each bit how many of its checks are unsatisfied, and flips the bits with the largest count. It stops when all checks hold. Gallager gave it in 1962 together with two hard message-passing decoders, algorithms A and B, whose error rates on long random codes follow an exact recursion. The weighted form of Kou, Lin and Fossorier also uses the size of each received sample. On codes whose graphs are good expanders, flipping provably corrects a constant fraction of errors; see [expander codes](/expander-codes/). It is much weaker than [belief propagation decoding](/belief-propagation-decoding/) and [min-sum decoding](/min-sum-decoding/), but it needs only XORs and counters.

## In plain words

Each bit takes part in a few parity checks. If a bit is wrong, all its checks fail. If a bit is right, most of its checks pass, because in a sparse code its checks share few other bits.

So the decoder counts, for each bit, how many of its checks fail, and it flips the bits that are the most suspect. Then it checks again. A codeword has no failed checks, so the decoder never moves away from one. When the errors are few and far apart, each wrong bit stands out, and one or two rounds fix them all. When the errors are many, correct bits can look as suspect as wrong ones, and the decoder can go around in circles, so it has a round limit.

## The problem

A codeword of $C = \{c : H c^T = 0\}$ is sent, and the receiver has only the hard decisions $r \in \{0, 1\}^n$: the output of a [binary symmetric channel](/binary-symmetric-channel/), or the signs of the samples of a soft channel. The goal is a codeword close to $r$ in [Hamming distance](/hamming-distance/), at a cost linear in the size of the Tanner graph. [Maximum likelihood decoding](/maximum-likelihood-decoding/) would find the nearest codeword, but for a general code that costs time exponential in the code size.

## The algorithm

$M(j)$ is the set of checks of bit $j$. The flips are parallel: all counts come from the same syndrome.

```pseudo id=main
BIT-FLIP-DECODE(H, r, I)
L1  c ← r
    for it ← 0 to I do
L2      s ← H c^T                                           ▷ the syndrome, one bit per check
L3      if s = 0 then return (c, it, success)
        if it = I then stop the loop
L4      for each j: u_j ← |{ i ∈ M(j) : s_i = 1 }|              ▷ unsatisfied checks of bit j
L5      t ← max_j u_j
L6      for each j with u_j = t: c_j ← 1 − c_j
L7  return (c, I, failure)
```

Gallager's own rule flips every bit with more than a fixed number of unsatisfied checks, instead of only those with the largest count. The largest count rule adapts the threshold to the round and always flips at least one bit.

**Gallager's algorithms A and B.** These pass one bit on each edge, as belief propagation passes an LLR. A check sends to each of its bits the XOR of the messages from its other bits. A bit sends to a check the complement of its received value when all its other checks (algorithm A), or at least $b$ of them (algorithm B), sent that complement, and its received value otherwise. The decision at each bit is a majority vote of its received value and all its check messages. Because each message leaves out what came from its target, the error rate on a long random code follows an exact recursion, density evolution.

**Weighted bit flipping.** For BPSK samples $y_j$, check $i$ gets the weight $w_i = \min_{j \in N(i)} |y_j|$, how sure its least sure bit is. Each bit gets the score $E_j = \sum_{i \in M(j)} (2 s_i - 1) w_i$: an unsatisfied check adds its weight and a satisfied one subtracts it. Each round flips the one bit with the largest score.

## Example

**The array code.** The implementation uses the array LDPC code with $p = 7$ and three block rows: $H$ has 21 rows and 49 columns, every column has weight 3, every row weight 7, and $H$ has rank 19, so the code has rate $30/49$. Block $(a, b)$ of $H$ is the $7 \times 7$ cyclic shift by $a b \bmod 7$. Two columns share at most one check, so the Tanner graph has no 4-cycle.

**One error.** Flip bit 10 of the zero codeword. The syndrome is column 10 of $H$: checks 3, 9 and 15 fail. Bit 10 has count 3, and any other bit shares at most one check with bit 10, so its count is at most 1. Line L6 flips only bit 10, and the next syndrome is zero.

**Two errors that tie with correct bits.** Flip bits 0 and 8. They share check 7, which sees two errors and is satisfied, so the failed checks are 0, 1, 14 and 20, two for each wrong bit. Bits 28 and 29 also have count 2: each is in one failed check of bit 0 and one of bit 8. Line L6 flips all four, so the wrong bits are now 28 and 29. These two are in no common check, so 6 checks fail, each wrong bit has count 3 and every other bit at most 1. The second round flips them back, and the word is decoded after two rounds. The test checks that all $\binom{49}{2} = 1176$ double errors are corrected by plain flipping, by algorithm A and by algorithm B with $b = 2$; 441 of them need two rounds. For three errors, plain flipping fails on 8722 of the 18424 patterns.

**Weighted flipping with no reliability.** If all $|y_j|$ are 1, every check has weight 1 and $E_j = 2 u_j - 3$, so the weighted rule flips one bit of largest count, the first on a tie. On the same code it then fails on 196 of the 1176 double errors, because it can flip a correct bit that ties. When the two wrong samples are weak, at $-0.2$, the checks that contain them get weight 0.2, and the weighted rule corrects every double error.

**Monte Carlo.** On BSC(0.02) with 200 frames of the array code, the 220 raw bit errors became 87 after plain flipping and 113 after algorithm A. On BPSK over AWGN at $E_b/N_0 = 4$ dB with 200 frames, the 385 raw errors became 328 after plain flipping and 156 after weighted flipping, which uses the sample sizes. On a $(3, 6)$-regular code of length 96 at 2 dB, the belief propagation page reports 83 bit errors for belief propagation, 125 for min-sum and 725 for plain flipping on the same frames, against 552 raw: at this noise level flipping is worse than no decoding, and the soft decoders are much better.

**Density evolution for algorithm A.** On the $(3, 6)$-regular ensemble over BSC($p$), the error probability of a message after $t$ rounds, on a tree, is $x_t$ with $x_0 = p$ and the recursion of the correctness section. For $p = 0.03$ it goes $0.03, 0.0246, 0.0184$, is $0.0028$ after 5 rounds and $10^{-5}$ after 10. For $p = 0.045$ it grows to a fixed point near $0.26$. Bisection gives the threshold $0.03946$, which matches the value about 0.0394 that Bazzi, Richardson and Urbanke give for this ensemble. The capacity of the BSC at rate 1/2 allows $p$ up to about 0.11, so algorithm A gives away much of it.

## Correctness

- **The output.** Line L3 returns success only when the syndrome is zero, so the word is a codeword. A received codeword is returned with no flip.
- **One error.** If every column has weight $\gamma \ge 2$ and the graph has no 4-cycle, a single wrong bit has count $\gamma$, and every other bit has count at most 1. So one round corrects it.
- **More errors.** No count argument alone bounds the number of errors that flipping corrects, because correct bits can tie with wrong ones, as in the example. On a graph whose small sets of bits have many unique neighbor checks, Sipser and Spielman proved that flipping corrects every error pattern up to a constant fraction of $n$.
- **Density evolution.** For algorithm A on a tree, the check messages are independent, a check message is right with probability $g = (1 + (1 - 2x)^{d_c - 1})/2$, and the next message error probability is $x' = p - p g^{d_v - 1} + (1 - p)(1 - g)^{d_v - 1}$. This map is nondecreasing in $x$ and in $p$, so the set of $p$ where $x_t \to 0$ is an interval, and bisection finds its end.

The [correctness proof](proofs/correctness.md) has the details, including the formula for algorithm B and the reduction of weighted flipping with equal sizes to plain flipping.

## Complexity

The syndrome of line L2 takes $\Theta(E)$ time, the counts of line L4 $\Theta(E)$, and lines L5 and L6 $\Theta(n)$. So a round takes $\Theta(E)$ time, and $I$ rounds $\Theta(I E)$. The memory is $\Theta(m + n)$ for the syndrome, the counts and the word, besides the graph. A faster form keeps the syndrome and the counts and updates them after each flip, at a cost of the degree of the flipped bit and of its checks, which is how the linear time decoder of Sipser and Spielman works. Algorithms A and B take $\Theta(E)$ per round with one bit per edge, and weighted flipping $\Theta(E)$ per round.

## Properties

- Hard input, hard output; the only arithmetic is XOR and small counts.
- A codeword is a fixed point, and a success flag means a codeword.
- Deterministic, and the parallel rule makes each round independent of the order of the bits.
- The result can cycle: the same set of words can repeat without reaching a codeword, so the round limit is needed.
- Algorithms A and B have exact thresholds by density evolution; plain flipping with the largest count rule does not have a simple one, because its rule depends on the whole word.

## Variants and improvements

- **Gallager's threshold rule.** Flip every bit with more than a fixed number of failed checks, for example more than half of its checks.
- **Sequential flipping.** Flip one bit at a time, a bit with more failed than satisfied checks. This is the decoder of Sipser and Spielman, and the number of failed checks falls with every flip.
- **Algorithms A and B.** Message passing with one bit per edge, with exact density evolution; B with a threshold that changes with the round does better than A.
- **Weighted bit flipping.** Use the sample sizes as check weights. Later forms also weight the bit's own sample, or flip with some randomness to escape cycles.
- **Use in cryptography.** The [BIKE](/bike/) key encapsulation scheme decodes a moderate-density parity-check code with a bit-flipping decoder. There the failure rate must be very small for security reasons.

## When to use it

- Use it when only hard decisions are available and the decoder must be very small or very fast, for example in memory and storage controllers as a first decoder before a soft one.
- Use it on codes with large column weight, such as codes from finite geometries, where the counts separate wrong and right bits well.
- Do not use it near the capacity of the channel: [min-sum](/min-sum-decoding/) and belief propagation correct far more errors on soft channels.

## Pitfalls

- **Ties.** With the largest count rule, correct bits that tie with wrong bits are flipped too. This usually costs a round, but it can also start a cycle.
- **Small column weight.** With weight 2, a wrong bit has count at most 2, and a correct bit next to two errors also has count 2. Weight 3 or more is the usual minimum for flipping.
- **4-cycles.** If two columns share two checks, a correct bit can have the same count as a single wrong bit, and even one error may not be corrected in one round.
- **Too many errors.** At high noise, flipping makes more errors than it removes, as in the length 96 example. Measure, and fall back to the raw word or a soft decoder.

## Implementations

## History

Gallager described bit flipping and the two hard message-passing algorithms in his 1962 paper and 1963 monograph on LDPC codes, and he analyzed them on a tree, the start of density evolution. The codes then got little attention until the 1990s, apart from Tanner's work of 1981. Sipser and Spielman in 1996 proved that on graphs with good expansion a simple flipping decoder corrects a constant fraction of errors in linear time. Kou, Lin and Fossorier in 2001 proposed weighted bit flipping for their finite geometry codes. Richardson and Urbanke in 2001 put density evolution in its general form with algorithms A and B as examples, and Bazzi, Richardson and Urbanke in 2004 found the exact thresholds of algorithm A.

## References
