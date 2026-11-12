---
tag: M3KJWK
kind: problem
slug: symbol-by-symbol-map-decoding
name: Symbol-by-symbol MAP decoding
aliases:
- bitwise MAP decoding
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Given the channel output, find for each bit the value with the larger posterior probability. This gives the least bit error rate, and the decisions need not form a codeword.
history:
  year: 1974
  people: [Lalit Bahl, John Cocke, Frederick Jelinek, Josef Raviv, Carlos R. P. Hartmann, Luther D. Rudolph]
  note: Bahl, Cocke, Jelinek and Raviv in 1974 computed the bitwise posteriors on a trellis. Hartmann and Rudolph in 1976 gave a formula for them as a sum over the dual code.
prereqs: [maximum-likelihood-decoding, linear-code, maximum-a-posteriori-estimation]
see_also: [bcjr-algorithm, belief-propagation-decoding, maximum-likelihood-sequence-estimation, turbo-decoding, tanner-graph, forward-backward-algorithm, belief-propagation, bayes-theorem]
sources:
  - paper: doi:10.1109/TIT.1974.1055186
    title: L. R. Bahl, J. Cocke, F. Jelinek and J. Raviv, Optimal decoding of linear codes for minimizing symbol error rate, IEEE Transactions on Information Theory 20(2), 1974, pages 284 to 287
    locator: The decoder that minimizes the symbol error probability, computed from the trellis
  - paper: "C. R. P. Hartmann and L. D. Rudolph, An optimum symbol-by-symbol decoding rule for linear codes, IEEE Transactions on Information Theory 22(5), 1976, pages 514 to 517"
    title: An optimum symbol-by-symbol decoding rule for linear codes
    locator: The decision rule for each symbol as a sum over the codewords of the dual code
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 25 (codeword decoding against bitwise decoding, and exact marginalization in trellises)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 12 (MAP decoding of convolutional codes with the BCJR algorithm)
---

Symbol-by-symbol MAP decoding is the problem of deciding each bit of a codeword by its own posterior probability, given the whole channel output. For bit $i$ it outputs the value $b$ that maximizes $P(c_i = b \mid y)$, usually as the posterior log-likelihood ratio $L(c_i) = \ln P(c_i = 0 \mid y) / P(c_i = 1 \mid y)$. This decision minimizes the probability that bit $i$ is wrong. [Maximum-likelihood decoding](/maximum-likelihood-decoding/) minimizes a different quantity, the probability that the whole word is wrong, and the two can disagree. The bitwise decisions together need not even be a codeword. On a [trellis](/trellis/) the [BCJR algorithm](/bcjr-algorithm/) solves the problem exactly; on a [Tanner graph](/tanner-graph/) [belief propagation decoding](/belief-propagation-decoding/) solves it exactly when the graph is a tree and approximately when it has cycles.

## In plain words

A receiver has a noisy copy of a codeword and wants to guess one bit, say the third. It looks at every codeword that could have been sent and weighs each by how well it fits the received signal. It adds the weights of all codewords with a 0 in the third place, and of all those with a 1, and picks the heavier side.

A maximum-likelihood decoder instead picks the single heaviest codeword and reads all bits from it. Usually the two agree. But many light codewords with a 1 in some place can outweigh one heavy codeword with a 0 there. Then the bitwise answer differs from the best codeword, and the bitwise answers together may not form any codeword at all.

## Definition

**Model.** $C \subseteq \{0, 1\}^n$ is a code, and a codeword $c$ is chosen with prior $P(c)$, usually uniform on $C$. It is sent over a memoryless binary input channel with output $y = (y_1, \ldots, y_n)$. The channel LLR of position $j$ is $L_j = \ln P(y_j \mid 0) / P(y_j \mid 1)$. With a uniform prior,

$$P(c \mid y) \propto \exp\Bigl(\tfrac12 \sum_{j=1}^{n} (1 - 2c_j) L_j\Bigr),$$

because $P(y_j \mid c_j) = \sqrt{P(y_j \mid 0) P(y_j \mid 1)}\, e^{(1 - 2c_j) L_j / 2}$ and the square root does not depend on $c$.

**Input.** The code (as a list, a generator matrix, a trellis or a Tanner graph) and the LLRs $L_1, \ldots, L_n$.

**Output.** For each $i$, the posterior LLR

$$L(c_i) = \ln \frac{\sum_{c \in C,\ c_i = 0} P(c \mid y)}{\sum_{c \in C,\ c_i = 1} P(c \mid y)},$$

and the decision $\hat c_i = 0$ if $L(c_i) \ge 0$ and $\hat c_i = 1$ otherwise.

**Optimality.** For any decoder that sees $y$, the probability that bit $i$ is wrong is $1 - P(c_i = \hat c_i \mid y)$, averaged over $y$. For each $y$ this is least when $\hat c_i$ is the value with the larger posterior, so the bitwise MAP rule minimizes the bit error probability of every position at once, and so also the average bit error rate. The same argument with the whole word in place of one bit shows that the word of largest posterior, the ML word under a uniform prior, minimizes the word error probability.

For a code with an encoder, the bits to decide can be the message bits $u_t$ in place of the code bits. For a systematic code the message bits are code bits, and the two forms agree.

## Variants

- **Message bits or code bits.** The BCJR algorithm usually outputs the LLRs of the input bits of a convolutional encoder. Belief propagation on a Tanner graph outputs the LLRs of the code bits.
- **Nonbinary symbols.** For a symbol over an alphabet of size $q$ the output is the posterior distribution of the symbol, and the decision is its mode.
- **Max-log form.** Replace each sum by its largest term: $\tilde L(c_i) = \max_{c_i = 0} \ln P(c \mid y) - \max_{c_i = 1} \ln P(c \mid y)$. The signs of these values are the bits of the ML codeword, so this form is ML decoding with a reliability for each bit.
- **Extrinsic output.** In iterative decoding the useful output is $L(c_i) - L_i - L_a(c_i)$, the part of the posterior that comes from the other positions.
- **Non-uniform priors.** Prior LLRs on the bits enter as extra terms in the exponent. This is how one decoder passes information to another in [turbo decoding](/turbo-decoding/).

## Examples

**The bitwise decisions are not a codeword.** Take the even weight code $C = \{000, 011, 101, 110\}$ and the LLRs $L = (1, 1, -0.5)$. The log weights $\tfrac12 \sum_j (1 - 2c_j) L_j$ are:

| codeword | 000 | 011 | 101 | 110 |
|---|---|---|---|---|
| log weight | 0.75 | 0.25 | 0.25 | $-1.25$ |

The ML codeword is 000. For bit 3, the codewords with $c_3 = 0$ have total weight $e^{0.75} + e^{-1.25} \approx 2.404$, and those with $c_3 = 1$ have $2 e^{0.25} \approx 2.568$. So $L(c_3) \approx -0.0662$ and the bitwise MAP decision is $\hat c_3 = 1$. For bits 1 and 2, $L(c_1) = L(c_2) \approx 0.7727$, so the decision vector is 001. It differs from the ML word in bit 3, and it is not a codeword. For this single parity check the posteriors also follow the tanh rule: $L(c_3) = L_3 + 2 \operatorname{artanh}\bigl(\tanh(L_1/2) \tanh(L_2/2)\bigr)$.

**The Hamming [7, 4] code on the BSC.** Each of the 16 codewords is sent with equal probability over a [binary symmetric channel](/binary-symmetric-channel/) with crossover probability $p$, and the receiver uses hard decisions. Summing over all $16 \cdot 2^7$ cases gives the exact rates:

| $p$ | bitwise MAP bit error rate | ML bit error rate | bitwise MAP word error rate | ML word error rate |
|---|---|---|---|---|
| 0.1 | 0.06688 | 0.06688 | 0.1496944 | 0.1496944 |
| 0.2 | 0.19616 | 0.19616 | 0.4232832 | 0.4232832 |
| 0.3 | 0.3 | 0.32184 | 0.9176457 | 0.6705828 |

At $p = 0.1$ and $p = 0.2$ the two decoders give the same rates. At $p = 0.3$ (and already at $p = 0.25$) the bitwise MAP decision of each bit is the received bit, for all 128 received words: the evidence from the other six bits never outweighs the bit itself. So its bit error rate is $p$. ML decoding still moves to the nearest codeword, and its bit error rate is higher than with no decoding at all, but its word error rate is far lower. Each decoder wins on its own criterion.

## Known algorithms

| method | input | time | exact |
|---|---|---|---|
| Brute force over the codewords | a list of $C$ | $\Theta(\lvert C \rvert n)$ | yes |
| [BCJR algorithm](/bcjr-algorithm/) | a trellis with $E$ edges | $\Theta(E)$ | yes |
| Hartmann and Rudolph (1976) | the dual code | $\Theta(2^{n-k} n^2)$ | yes |
| [Belief propagation decoding](/belief-propagation-decoding/) | a Tanner graph | linear per iteration | on trees only |
| [Turbo decoding](/turbo-decoding/) | two trellises and an interleaver | linear per iteration | no |

The rule of Hartmann and Rudolph comes from the Fourier transform over $\mathrm{GF}(2)^n$, which maps a sum over a linear code $C$ to a sum over its dual $C^\perp$. With $\rho_j = \tanh(L_j / 2)$,

$$\tanh\frac{L(c_i)}{2} = \frac{\sum_{c' \in C^\perp} \prod_{j} \rho_j^{\,c'_j \oplus [j = i]}}{\sum_{c' \in C^\perp} \prod_{j} \rho_j^{\,c'_j}}.$$

For a single parity check, $C^\perp = \{0, \mathbf 1\}$, and the formula becomes the tanh rule of the example. It is the better method for high rate codes, where $C^\perp$ is small.

## Bounds

- **The bit error rate of bitwise MAP is a lower bound** for every decoder of the same code and channel, and the word error rate of ML is a lower bound on the word error rate of every decoder. The table of the Hamming code shows that neither decoder is best on both.
- **An upper bound for both.** Since bitwise MAP has the lower bit error rate, the [union bound](/union-bound/) on the ML bit error rate, computed from the weight distribution of the code, is also an upper bound on the bitwise MAP bit error rate.
- **Cost.** No algorithm is known that computes the exact posteriors of a general linear code in time polynomial in $n$. The known exact methods are exponential in $\min(k, n - k)$ or in the trellis width.

## Reductions

- **Bitwise MAP is marginalization.** The posterior of bit $i$ is a marginal of the distribution $P(c \mid y)$, which factors over the parity checks of the code. So any exact marginalization method on a [factor graph](/factor-graph/) solves it, and [belief propagation](/belief-propagation/) is exact when that graph is a tree.
- **Trellis decoding is the forward-backward algorithm.** On a code trellis the posterior is a sum over paths. This is the computation of the [forward-backward algorithm](/forward-backward-algorithm/) for a hidden Markov model, with the code trellis as the state graph and the channel LLRs as the evidence.
- **Max-log bitwise MAP is ML decoding.** Replacing sums by maxima turns the problem into [maximum-likelihood decoding](/maximum-likelihood-decoding/), which on a trellis is [MLSE](/maximum-likelihood-sequence-estimation/).

## Applications

- The constituent decoders of turbo codes, which must output soft values and not hard decisions.
- Decoding of LDPC codes by belief propagation, which approximates the bitwise posteriors on a Tanner graph with cycles.
- Turbo equalization, where an equalizer for a channel with intersymbol interference and a decoder exchange bitwise posteriors.
- Any receiver whose output feeds a later stage that uses reliabilities, such as a soft input outer decoder.

## References
