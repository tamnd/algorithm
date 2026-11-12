---
tag: 16771S
kind: problem
slug: maximum-likelihood-decoding
name: Maximum-likelihood decoding
aliases:
- ML decoding
- maximum likelihood block decoding
area: compression-and-coding/error-correcting-codes
level: core
summary: Given a received word y, find a codeword c that maximizes the channel probability P(y | c). On BSC(p) with p < 1/2 this is nearest codeword decoding, but not on other channels.
prereqs: [binary-symmetric-channel, hamming-distance, bayes-theorem]
see_also: [nearest-codeword-problem, syndrome-decoding, additive-white-gaussian-noise-channel, maximum-likelihood-sequence-estimation, symbol-by-symbol-map-decoding, maximum-a-posteriori-estimation, union-bound, erasure-decoding]
sources:
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 1 (maximum likelihood decoding, the binary symmetric channel and minimum distance decoding, soft decisions on the AWGN channel)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 1 (decoding rules, maximum likelihood and maximum a posteriori decoding, and nearest codeword decoding on the binary symmetric channel)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 1 (the optimal decoder of the repetition code and of the (7,4) Hamming code by posterior probability)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 7 (channel capacity, the probability of error of a code, and decoding rules)
---

Maximum likelihood (ML) decoding is the problem of finding, for a received word $y$, a codeword $c$ that makes $y$ most probable: it maximizes $P(y \mid c)$ over the code. When all codewords are equally likely to be sent, an ML decoder has the least possible probability of a block error. On a binary symmetric channel with crossover probability below $1/2$ it is the same as decoding to a nearest codeword in Hamming distance, but on other channels, and with soft decisions, the two rules differ.

## In plain words

A message is sent as one of a fixed list of codewords, and noise changes some symbols. The receiver sees the noisy word and must guess which codeword was sent. The maximum likelihood guess is the codeword that would most often produce exactly what was received.

When each wrong symbol is equally likely and rare, the best guess is the codeword that differs from the received word in the fewest places. That is the familiar nearest codeword rule. But if the noise changes ones into zeros more often than zeros into ones, or if the receiver also knows how sure it is of each symbol, the most likely codeword can be a farther one.

If the receiver also knows that some messages are sent more often than others, it should weigh them by how common they are. That rule is called maximum a posteriori decoding.

## Definition

**Notation.** A block code $C$ of length $n$ over an input alphabet $\mathcal{X}$, with $M$ codewords. For a linear code, $C$ is an $[n, k, d]_q$ code over $\mathrm{GF}(q)$, $M = q^k$, $R = k/n$, $t = \lfloor (d - 1)/2 \rfloor$, vectors are rows and $c = m G$. $d(x, y)$ is the [Hamming distance](/hamming-distance/).

**Channel.** A memoryless channel with transition probabilities $W(b \mid a)$ (a density for continuous outputs) maps the sent word $c$ to $y$ with

$$P(y \mid c) = \prod_{i=1}^{n} W(y_i \mid c_i).$$

**Problem (ML decoding).** Input: the code (by a generator matrix or a list), the channel $W$, and a received word $y$. Output: a codeword

$$\hat c_{\mathrm{ML}}(y) \in \arg\max_{c \in C} P(y \mid c).$$

**MAP decoding.** With a prior $\pi(c)$ on the codewords, the maximum a posteriori decoder outputs $\arg\max_c \pi(c) P(y \mid c)$, which by [Bayes' theorem](/bayes-theorem/) maximizes the posterior $P(c \mid y)$. With a uniform prior, MAP and ML are the same rule.

**MAP is optimal.** For a decoder $D$, the probability of correct decoding is $\sum_y \pi(D(y)) P(y \mid D(y))$, a sum over $y$ of terms each at most $\max_c \pi(c) P(y \mid c)$. The MAP decoder reaches this maximum for every $y$, so no decoder has a lower block error probability. With a uniform prior the same holds for ML.

**ML on the BSC is nearest codeword decoding.** On the [binary symmetric channel](/binary-symmetric-channel/) BSC($p$),

$$P(y \mid c) = p^{d(y, c)} (1 - p)^{n - d(y, c)} = (1 - p)^n \left( \frac{p}{1 - p} \right)^{d(y, c)}.$$

For $p < 1/2$ the ratio $p/(1 - p)$ is below 1, so the probability falls strictly as $d(y, c)$ grows, and the ML codewords are exactly the nearest codewords. For $p > 1/2$ they are the farthest codewords, and for $p = 1/2$ all codewords tie. The same holds on the $q$-ary symmetric channel with $p < (q - 1)/q$. For a linear code, nearest codeword decoding is the [nearest codeword problem](/nearest-codeword-problem/), and [syndrome decoding](/syndrome-decoding/) solves it with a table.

**Soft decisions on the AWGN channel.** Send a binary codeword with BPSK, $x_i = 1 - 2 c_i \in \{+1, -1\}$, with symbol energy $E_s = 1$, over the [AWGN channel](/additive-white-gaussian-noise-channel/): $y_i = x_i + z_i$ with independent $z_i \sim N(0, \sigma^2)$. We define $\mathrm{SNR} = E_s / \sigma^2 = 1/\sigma^2$ per real dimension. With $\sigma^2 = N_0/2$ and $E_s = R E_b$,

$$\frac{E_b}{N_0} = \frac{E_s}{R N_0} = \frac{1}{2 R \sigma^2} = \frac{\mathrm{SNR}}{2R}.$$

The likelihood is $P(y \mid c) \propto \exp(-\lVert y - x \rVert^2 / (2 \sigma^2))$, and $\lVert y - x \rVert^2 = \lVert y \rVert^2 - 2 \sum_i y_i x_i + n$, where only the middle term depends on $c$. So soft decision ML decoding maximizes the correlation $\sum_i y_i x_i$, which is minimum Euclidean distance decoding. Hard decisions first quantize $y_i$ to its sign, which turns the channel into BSC($p$) with $p = Q(1/\sigma) = Q(\sqrt{2 R E_b / N_0})$, and so discard the reliability of each symbol. The Examples below show what this costs for the Hamming code.

## Variants

- **Hard or soft decisions.** Hard decision ML works on a discrete channel such as BSC($p$). Soft decision ML uses the real channel outputs, or their log likelihood ratios.
- **Block or symbol.** ML and MAP as defined here choose a whole codeword and minimize the block error rate. [Symbol-by-symbol MAP decoding](/symbol-by-symbol-map-decoding/) chooses each information symbol separately and minimizes the symbol error rate; the [BCJR algorithm](/bcjr-algorithm/) computes it on a trellis.
- **Sequences.** For convolutional codes, ML over the paths of a trellis is [maximum likelihood sequence estimation](/maximum-likelihood-sequence-estimation/), solved by the Viterbi algorithm.
- **Erasures.** On the [binary erasure channel](/binary-erasure-channel/), all codewords that agree with the unerased symbols have the same likelihood. ML decoding of a linear code is then the solution of a linear system, and [erasure decoding](/erasure-decoding/) by Gaussian elimination finds it in polynomial time.
- **Incomplete decoders.** A bounded distance decoder returns the codeword within distance $t$ if there is one, and otherwise reports a failure. It is not ML, but it is often what an algebraic decoder computes.
- **List decoding.** Return all codewords within a radius, or the $L$ most likely codewords. See [list decoding](/list-decoding/).

## Examples

**ML and minimum distance differ: a Z channel.** The Z channel never changes 0, and changes 1 into 0 with probability 0.4. Take the code $\{000, 111\}$ and $y = 001$. Then $P(001 \mid 000) = 0$, since a 0 never becomes 1, and $P(001 \mid 111) = 0.4 \cdot 0.4 \cdot 0.6 = 0.096$. ML decodes to $111$, but the nearest codeword is $000$, at distance 1 against 2.

**ML and minimum distance differ: both crossovers below 1/2.** On a binary asymmetric channel with $P(0 \to 1) = 0.01$ and $P(1 \to 0) = 0.3$, take the code $\{00000, 11110\}$ and $y = 10000$:

$$P(y \mid 00000) = 0.01 \cdot 0.99^4 = 0.0096060, \qquad P(y \mid 11110) = 0.7 \cdot 0.3^3 \cdot 0.99 = 0.018711 .$$

ML decodes to $11110$, at distance 3, and not to $00000$, at distance 1: three lost ones are more likely than one created one.

**MAP and ML differ.** The repetition code $\{000, 111\}$ on BSC($0.1$) with $y = 011$: $P(y \mid 000) = 0.1^2 \cdot 0.9 = 0.009$ and $P(y \mid 111) = 0.1 \cdot 0.9^2 = 0.081$, so ML decodes to $111$. With the prior $\pi(000) = 0.95$, the weighted values are $0.95 \cdot 0.009 = 0.00855$ and $0.05 \cdot 0.081 = 0.00405$, so MAP decodes to $000$, with posterior $0.00855 / 0.0126 = 19/28 \approx 0.679$. With $\pi(000) = 0.9$ the two values are both $0.0081$, an exact tie.

**Soft beats hard.** The same code with BPSK on AWGN, and $y = (0.9, -0.2, -0.3)$. Hard decisions give $011$, which majority vote decodes to $111$. The correlations are $0.9 - 0.2 - 0.3 = 0.4$ for $000$ (signal $+1, +1, +1$) and $-0.4$ for $111$, so soft ML decodes to $000$. One strong positive value outweighs two weak negative values.

**Error rates of the Hamming code.** For the $[7, 4, 3]$ [Hamming code](/hamming-code/) on BSC($p$), ML decoding corrects exactly the error patterns of weight at most 1, so the block error rate is $1 - (1 - p)^7 - 7 p (1 - p)^6$, which is $0.0443805$ at $p = 0.05$. With BPSK on AWGN and soft decision ML by exhaustive search over the 16 codewords, a simulation with 20000 codewords and the seed 7 gives the block error rates below. The union bound uses the weight distribution $A_3 = A_4 = 7$, $A_7 = 1$:

$$P_B \le \sum_{w} A_w\, Q\!\left(\sqrt{2 w R E_b / N_0}\right), \qquad P_B \ge Q\!\left(\sqrt{2 d R E_b / N_0}\right).$$

The lower bound holds because a nearest neighbor at distance $d$ alone causes errors with that probability. The last column is the exact hard decision rate, with $p = Q(\sqrt{2 R E_b/N_0})$.

| $E_b/N_0$ | soft ML, simulated | union bound | lower bound | hard decisions, exact |
|---|---|---|---|---|
| 2 dB | 0.0622 | 0.09419 | 0.00987 | 0.12354 |
| 4 dB | 0.0120 | 0.01415 | 0.00167 | 0.03671 |
| 6 dB | 0.0006 | 0.000841 | 0.000110 | 0.005386 |

The simulated values lie between the bounds, and soft decisions give about a tenfold lower error rate than hard decisions at 6 dB.

## Known algorithms

- **Exhaustive search.** Compute $P(y \mid c)$, or the correlation, for all $M$ codewords: $O(M n)$ operations, $O(q^k n)$ for a linear code. The implementation of this page does this.
- **Syndrome table (BSC).** [Syndrome decoding](/syndrome-decoding/) solves hard decision ML on BSC($p$), $p < 1/2$, with a table of $q^{n-k}$ coset leaders and $O(n^2)$ work per word.
- **Trellis search.** The Viterbi algorithm on a trellis of the code finds the ML codeword in time proportional to the number of trellis edges. For convolutional codes this is linear in the length; for a block code the trellis can have up to $\min(q^k, q^{n-k})$ states at a section.
- **Erasure channel.** Gaussian elimination, $O(n^3)$.
- **Near ML for long codes.** Ordered statistics decoding and sphere decoding search near the hard decision, and [belief propagation](/belief-propagation-decoding/) on LDPC and turbo codes approximates symbol-wise MAP. None is exact ML in general.

## Bounds

- **Optimality.** No decoder has a lower block error probability than MAP; with equally likely codewords, than ML.
- **Union bound (AWGN, soft ML, linear code).** $P_B \le \sum_{w \ge d} A_w Q(\sqrt{2 w R E_b / N_0})$, from the [union bound](/union-bound/) over the pairwise errors, with the codeword weight distribution $A_w$. At high $E_b/N_0$ the term $A_d Q(\sqrt{2 d R E_b/N_0})$ dominates.
- **BSC, exact.** For a linear code and ML by coset leaders, $P_c = \sum_w \alpha_w p^w (1 - p)^{n - w}$, where $\alpha_w$ is the number of coset leaders of weight $w$.
- **Coding theorem.** By the [channel coding theorem](/channel-coding-theorem/), for every rate below the [capacity](/channel-capacity/) there are codes whose ML block error probability tends to 0 as $n$ grows; above capacity it tends to 1 for every code and decoder.

## Reductions

- **ML on BSC($p$), $p < 1/2$, for linear codes** is the [nearest codeword problem](/nearest-codeword-problem/), which is NP-hard by Berlekamp, McEliece and van Tilborg (1978). So no polynomial algorithm solves ML decoding of all linear codes unless P = NP, even for hard decisions.
- **ML on the BEC** reduces to solving a linear system, so it is in polynomial time.
- **Soft ML on AWGN with BPSK** is the maximization of a linear function $\sum_i y_i (1 - 2 c_i)$ over the codewords, a binary integer program over the code.
- **ML on a trellis** is a shortest path problem in a layered graph with edge costs $-\log W(y_i \mid c_i)$.

## Applications

- **Reference curves.** Simulations of practical decoders report the gap to ML, or to the union bound, for short codes where exhaustive or trellis ML is feasible.
- **Convolutional codes.** The Viterbi decoder, which is ML for sequences, decodes the convolutional codes of GSM, of IEEE 802.11 and of space links.
- **Short block codes.** Codes for control channels and for ultra reliable short packets have so few codewords that near ML decoding is affordable, and its gain over hard decisions is large.
- **Memory and storage.** Single error correcting codes in memory are decoded by syndrome tables, which are ML on a BSC model of independent bit flips.

## References
