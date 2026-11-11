---
tag: R2MHB2
kind: algorithm
slug: bkw-algorithm
name: BKW algorithm
aliases:
- Blum-Kalai-Wasserman algorithm
area: cryptography/post-quantum
level: research
summary: Solves LPN by adding samples that agree on a block, which clears that block. The bias squares at each level. With blocks of about n/log n bits it takes time 2^(O(n/log n)).
solves: [learning-parity-with-noise]
model: word-ram
complexity:
  vars: {n: the length of the secret, tau: the noise rate, a: the number of blocks, b: "the block size, with a b = n"}
  time: {worst: "2^(O(n/log n))"}
  space: {extra: "2^(O(n/log n))"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 2003
  people: [Avrim Blum, Adam Kalai, Hal Wasserman]
  note: Presented at STOC 2000 and published in the Journal of the ACM in 2003. It was the first algorithm for learning parity with constant noise in time below 2^n.
prereqs: [learning-parity-with-noise, learning-with-errors]
see_also: [fast-walsh-hadamard-transform, walsh-hadamard-transform, generalized-birthday-problem, hoeffding-inequality, birthday-paradox, arora-ge-algorithm, core-svp-hardness, learning-with-rounding]
sources:
  - paper: "Avrim Blum, Adam Kalai and Hal Wasserman, Noise-tolerant learning, the parity problem, and the statistical query model, Journal of the ACM 50(4), 2003, pages 506 to 519"
    locator: the block reduction, the bias (1 - 2 tau)^(2^a) after a levels, and the bound 2^(O(n/log n)) for constant noise rate with a = (1/2) log n
  - paper: "Martin R. Albrecht, Carlos Cid, Jean-Charles Faugere, Robert Fitzpatrick and Ludovic Perret, On the complexity of the BKW algorithm on LWE, Designs, Codes and Cryptography 74(2), 2015, pages 325 to 354"
    locator: the LWE version, with tables indexed by a block mod q that store a and -a together, and the hypothesis testing step for the last block
  - paper: "Paul Kirchner and Pierre-Alain Fouque, An improved BKW algorithm for LWE with applications to cryptography and lattices, CRYPTO 2015, LNCS 9215, pages 43 to 62"
    locator: reduction of each block only modulo a smaller modulus, with the error this adds, which lowers the cost for LWE with small secrets
  - paper: "Eric Levieil and Pierre-Alain Fouque, An improved LPN algorithm, SCN 2006, LNCS 4116"
    locator: the LF1 variant, which recovers a whole block with a Walsh-Hadamard transform over all reduced samples
  - paper: "Vadim Lyubashevsky, The parity problem in the presence of noise, decoding random linear codes, and the subset sum problem, APPROX-RANDOM 2005, LNCS 3624"
    locator: a version that needs only n^(1 + epsilon) samples at the cost of time 2^(O(n/log log n))
---

The BKW algorithm of Blum, Kalai and Wasserman solves [learning parity with noise](/learning-parity-with-noise/) (LPN) in time $2^{O(n / \log n)}$ for a constant noise rate. It splits the $n$ secret bits into $a$ blocks of $b$ bits. Two samples that agree on a block add up to a sample that is zero on that block, so after $a - 1$ rounds of this, the samples have only one block left, and some of them are unit vectors that show one secret bit each. Each addition makes the noise worse: the bias of the error squares at each level, so the number of levels must stay small. The same idea, with tables mod $q$, attacks [learning with errors](/learning-with-errors/).

**Notation.** A sample is $(x, y)$ with $x \in \mathbb{F}_2^n$ uniform and $y = \langle x, s \rangle + e$, where $e = 1$ with probability $\tau < 1/2$. The bias of the error is $\delta = 1 - 2\tau = \Pr[e = 0] - \Pr[e = 1]$. The secret $s$ has $n = ab$ bits in $a$ blocks of $b$ bits; block $i$ is the coordinates $(i - 1)b + 1, \ldots, ib$. A level is one pass that clears one block. $e_j$ is the unit vector with a 1 at position $j$. Logarithms are to base 2.

## In plain words

Each sample is a noisy answer to the question "which of these secret bits, added together, are odd?". If two samples ask about the same bits in one part of the secret, their sum asks about none of the bits in that part. So we sort the samples by one part, add pairs inside each group, and the part is gone. We repeat this for each part except the last.

At the end, some samples ask about one single secret bit. We read that bit by a vote over all such samples. The catch is that each sum carries the noise of both samples. After a few rounds the noise is close to a coin flip, so we need very many samples to win the vote. The trick works because the number of rounds is small.

## The problem

The input is $m$ LPN samples $(x_k, y_k)$ for an unknown $s \in \mathbb{F}_2^n$ and a noise rate $\tau$, and the block shape $a \times b$ with $ab = n$. The output is $s$. BKW is a search algorithm for LPN with many samples: it needs about $2^b$ samples for each level, and many more for the final vote. For LWE the samples are $(x, y) \in \mathbb{Z}_q^n \times \mathbb{Z}_q$ with $y = \langle x, s \rangle + e \bmod q$ and a small error $e$.

## The algorithm

```pseudo id=main
BKW(S, a, b)
L1  s ← 0
L2  for t ← a down to 1 do
L3      R ← S with blocks t + 1..a removed, y corrected by the known bits of s
L4      for i ← 1 to t − 1 do
L5          group R by the bits of block i
L6          in each group add the first sample to the others and drop it
L7      for each position j in block t do
L8          s_j ← majority of y over the samples in R with x = e_j
L9  return s
```

The code with this page uses 0-based block numbers. Line L3 removes the bits of the blocks found so far: if $x_{\text{high}}$ is the part of $x$ on blocks $t + 1, \ldots, a$, the new label is $y + \langle x_{\text{high}}, s_{\text{high}} \rangle$. Line L6 keeps the relation, because over $\mathbb{F}_2$ the sum of $y = \langle x, s \rangle + e$ and $y' = \langle x', s \rangle + e'$ is $y + y' = \langle x + x', s \rangle + (e + e')$, and $x + x'$ is zero on block $i$. After $t - 1$ levels every sample in $R$ is zero outside block $t$ and is a sum of up to $2^{t-1}$ original samples.

The original BKW draws a fresh batch of samples for each vote, so that the votes are independent. The code with this page reuses one batch for all rounds and all votes, as most practical versions do. The reduced samples then share representatives and their errors are correlated. This is a heuristic: it works well on the toy sizes of the tests, but the proof does not cover it.

## Example

Take $n = 4$, $a = b = 2$ and the secret $s = 1011$, written $s_1 s_2 s_3 s_4$, so block 1 is $(s_1, s_2) = (1, 0)$ and block 2 is $(s_3, s_4) = (1, 1)$. There are ten samples $x;y$, with one wrong label (sample 6, whose true parity is 0):

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $x_k$ | 0100 | 0101 | 1001 | 1101 | 0010 | 0011 | 1111 | 0101 | 1011 | 1011 |
| $y_k$ | 0 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |

**Round $t = 2$.** Line L5 groups by $(x_1, x_2)$. The group 01 has samples 1, 2 and 8; the group 10 has 3, 9 and 10; the group 11 has 4 and 7; the group 00 has 5 and 6. Line L6 adds the first sample of each group to the others:

- group 01: $0100 + 0101 = 0001$ with label $0 + 1 = 1$, twice (samples 2 and 8);
- group 10: $1001 + 1011 = 0010$ with label $0 + 1 = 1$, twice (samples 9 and 10);
- group 11: $1101 + 1111 = 0010$ with label $0 + 1 = 1$;
- group 00: $0010 + 0011 = 0001$ with label $1 + 1 = 0$.

The votes for $s_3$ (from $x = 0010$) are 1, 1, 1, so $s_3 = 1$. The votes for $s_4$ (from $x = 0001$) are 1, 1, 0, so $s_4 = 1$. The wrong label of sample 6 moved into one vote and lost.

**Round $t = 1$.** Line L3 drops $x_3, x_4$ and adds $x_3 + x_4$ to $y$. Samples 3, 9 and 10 become $x = 10$ with labels $0 + 1 = 1$, $1 + 0 = 1$ and $1 + 0 = 1$, so $s_1 = 1$. Samples 1, 2 and 8 become $x = 01$ with labels $0$, $1 + 1 = 0$ and $1 + 1 = 0$, so $s_2 = 0$. Line L9 returns $1011$.

**At a larger size.** With $n = 32$, $a = 4$, $b = 8$, $\tau = 0.05$ and $2^{14} = 16384$ samples, the three levels leave 16128, 15872 and 15616 samples. In one run, the eight unit vectors of the last block got between 48 and 74 votes each, and between 12 and 21 of these votes were wrong. The error rate of all reduced samples was 0.277, against $(1 - 0.9^8)/2 \approx 0.285$ from the formula for a sum of 8 errors. Every vote had a clear majority, and BKW returned $s$; it did so in 20 of 20 runs with the majority vote and in 20 of 20 with the Walsh-Hadamard step.

## Correctness

Line L6 keeps the relation $y = \langle x, s \rangle + \text{error}$ and clears one block, so after $t - 1$ levels a sample with $x = e_j$ has $y = s_j + E$, where $E$ is the sum of at most $2^{t-1}$ original errors. Without noise every vote is $s_j$, and BKW returns $s$ as soon as every unit vector appears. With noise, the piling-up rule $\mathbb{E}[(-1)^{e_1 + e_2}] = \mathbb{E}[(-1)^{e_1}] \, \mathbb{E}[(-1)^{e_2}]$ gives the error $E$ a bias of at least $\delta^{2^{t-1}}$: the bias squares at each level. If the $V$ votes for a bit are independent, the [Hoeffding inequality](/hoeffding-inequality/) makes the majority wrong with probability at most $e^{-V \delta^{2^t} / 2}$. So $V = O(\delta^{-2^a} \log n)$ votes per bit suffice. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Bias.** After $k$ levels the bias is $\delta^{2^k}$. For $\tau = 0.05$, $\delta = 0.9$, and the bias after 1, 2, 3 and 4 levels is 0.81, 0.656, 0.430 and 0.185. The number of votes grows like the inverse square of the bias: $\delta^{-2^a}$ is about 5.4 for $a = 4$, about 850 for $a = 6$ and about $5 \cdot 10^{11}$ for $a = 8$.
- **Samples.** Each level drops at most $2^b$ samples, one for each group. One vote needs about $a \cdot 2^b$ fresh samples, and there are $O(\delta^{-2^a} \log n)$ votes for each bit. Blum, Kalai and Wasserman show that samples and time are polynomial in $\delta^{-2^a}$ and $2^b$.
- **The choice of $a$.** Take $a = \frac{1}{2} \log n$, so $2^a = \sqrt{n}$ and $b = 2n / \log n$. Then $\delta^{-2^a} = 2^{\sqrt{n} \log(1/\delta)}$, which is $2^{o(n / \log n)}$ for a constant $\tau$, and $2^b = 2^{2n / \log n}$. So time, samples and memory are all $2^{O(n / \log n)}$.
- **The code.** One batch of $m$ samples costs $O(a m)$ word operations for the reduction in each round, so $O(a^2 m)$ in all, plus $O(2^b b)$ for the Walsh-Hadamard step. The final round has about $(m - (a - 1)2^b) / 2^b$ votes for each bit.

## Properties

- **Subexponential.** For a constant noise rate it beats the $2^n$ of trying all secrets, and also Gaussian elimination on noise-free subsets of samples.
- **Sample-hungry.** It needs $2^{O(n / \log n)}$ samples. With only $O(n)$ samples it does not apply directly.
- **Probabilistic answer.** Given the samples, the steps are fixed, but the answer is right only with high probability over the samples.
- **Memory-heavy.** It stores about $2^b$ representatives for each level and all the samples of one round.

## Variants and improvements

- **LF1 and the Walsh-Hadamard step.** Levieil and Fouque (2006) keep every reduced sample, not only the unit vectors. For each candidate $c$ of the last block they count $\sum (-1)^{y + \langle x, c \rangle}$, which is a [Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) of size $2^b$, and pick the largest. This uses about $2^b$ times more votes for each bit. `solve_block_wht` in the code with this page is this step.
- **Fewer samples.** Lyubashevsky (2005) builds the many samples BKW needs from only $n^{1 + \varepsilon}$ given samples, at the cost of time $2^{O(n / \log \log n)}$.
- **LWE.** Albrecht, Cid, Faugère, Fitzpatrick and Perret (2015) analyse BKW for LWE. The table for a block holds vectors mod $q$, and a vector $x$ and its negative $-x$ share one entry, so that a new sample can always be cleared by adding or subtracting the stored one. This gives $(q^b - 1)/2$ entries. Each level doubles the variance of the error. The last block is found by hypothesis testing over all $q^b$ candidates, scoring each by how small the remaining errors are.
- **Modulus switching.** Kirchner and Fouque (2015) clear each block only modulo a smaller modulus, which adds a small rounding error but needs far smaller tables. Lazy modulus switching and coded BKW follow the same idea. These versions make BKW much cheaper for LWE with a small secret.
- **Generalized birthday.** Clearing $b$ bits by matching pairs is the same step as in Wagner's algorithm for the [generalized birthday problem](/generalized-birthday-problem/).

## When to use it

Use it for LPN and for LWE with a small modulus when the attacker gets very many samples, and to estimate the security of LPN-based schemes. For LPN parameters with a constant noise rate it, or one of its descendants such as LF1, is often the best known attack. For LWE at the sizes of ML-KEM, which gives an attacker only a few hundred samples, lattice attacks counted in the [core-SVP](/core-svp-hardness/) model are cheaper, and BKW needs far more samples than are available.

## Pitfalls

- **Too many levels.** The bias $\delta^{2^{a-1}}$ falls fast, and the votes needed grow like $\delta^{-2^a}$. One extra level squares the bias, so choose $a$ small and $b$ large.
- **Missing unit vectors.** If no reduced sample equals $e_j$, the vote for $s_j$ is empty and the code leaves $s_j = 0$. Use at least $a \cdot 2^b$ samples plus enough for the votes, or the Walsh-Hadamard step, which uses all samples.
- **Shared samples.** Reusing one batch makes the votes correlated. The real error rate after two levels in our tests varied from about 0.16 to 0.23 between runs, against the expected 0.172.
- **Errors spread.** A wrong bit in a high block corrupts the label correction of line L3 in all later rounds. A check of the final $s$ against fresh samples catches this.
- **LWE tables.** Storing $x$ and $-x$ apart doubles the memory and halves the matches.

The Python code with this page implements BKW for LPN with the majority vote and the LF1 Walsh-Hadamard step, and recovers the secret for $n$ from 12 to 32. It reuses one batch of samples, which is the heuristic described above. It is for study only, is not constant time, and runs only on toy parameters. To estimate the cost of BKW for real LWE parameters, use the lattice estimator of Albrecht, Player and Scott, which models coded BKW.

## Implementations

## History

Blum, Kalai and Wasserman presented the algorithm at STOC 2000, and the full paper appeared in the Journal of the ACM in 2003. Their goal was in learning theory: the algorithm learns parity functions on the first $O(\log n \log \log n)$ bits under noise in polynomial time, which no statistical query algorithm can do, so it separates noise-tolerant learning from the statistical query model. Cryptographers soon used it as the main attack on LPN, for example against the HB family of authentication protocols, and Levieil and Fouque improved its last step in 2006. Regev noted that it also applies to LWE, and Albrecht, Cid, Faugère, Fitzpatrick and Perret gave the first detailed analysis of the LWE version in 2015.

## References
