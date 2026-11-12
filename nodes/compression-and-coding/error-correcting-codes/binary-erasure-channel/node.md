---
tag: 6KVV6B
kind: model
slug: binary-erasure-channel
name: Binary erasure channel
aliases:
- BEC
area: compression-and-coding/error-correcting-codes
level: core
summary: A channel that delivers each input bit unchanged or replaces it by an erasure mark, with probability eps and independently. It never flips a bit, and its capacity is 1 - eps.
prereqs: [binary-symmetric-channel]
see_also: [channel-capacity, erasure-decoding, erasure-codes, fountain-codes, peeling-decoding, ldpc-code, reed-solomon-code, channel-coding-theorem]
sources:
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 7.1.5 (binary erasure channel, p. 188) and Section 7.12 (feedback capacity)
  - book: isbn:9780521852296
    title: Tom Richardson and Rüdiger Urbanke, Modern Coding Theory, Cambridge University Press, 2008
    locator: Chapter 3 (binary erasure channel), on maximum a posteriori decoding by linear algebra and on LDPC codes with message passing on this channel
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 9 (communication over a noisy channel) and Chapter 50 (digital fountain codes for the erasure channel)
---

The binary erasure channel models a link that loses bits but never changes them. Each bit arrives intact with probability $1 - \varepsilon$, or is replaced by an erasure mark $?$ with probability $\varepsilon$, independently of the other bits, and the receiver sees which positions are missing. Decoding a linear code on it is a question of linear algebra, its capacity is $1 - \varepsilon$, and it is the model in which the modern capacity-achieving codes were first understood.

## The machine

The input alphabet is $\{0, 1\}$, the output alphabet is $\{0, 1, ?\}$, and the parameter is the **erasure probability** $\varepsilon \in [0, 1]$. The transition probabilities are

$$W(x \mid x) = 1 - \varepsilon, \qquad W(? \mid x) = \varepsilon, \qquad W(1 - x \mid x) = 0.$$

The channel is memoryless: over $n$ uses each position is erased independently, so the number of erasures has the [binomial distribution](/binomial-distribution/) with parameters $n$ and $\varepsilon$. A received bit that is not $?$ is always correct. As for the [binary symmetric channel](/binary-symmetric-channel/), there is no feedback unless the model says so.

The same model with an alphabet of $q$ symbols is the $q$-ary erasure channel. With packets as symbols it is the *packet erasure channel*: a packet with a failed checksum is thrown away, and its sequence number tells the receiver which one is missing.

## What it counts

- **Rate** $R = k/n$ for a code with $2^k$ codewords of length $n$.
- **Decoding failure probability.** On this channel a decoder never needs to guess wrong: it can return the message when only one codeword agrees with the received bits, and report a failure otherwise. The quantity of interest is the probability of failure.
- **Overhead.** For codes that send packets, the number of received symbols beyond $k$ that decoding needs. An ideal code needs exactly $k$ of them, whichever ones arrive.

## Relation to other models

- **Binary symmetric channel.** If the receiver replaces each $?$ by a fair coin flip, $\mathrm{BEC}(\varepsilon)$ becomes $\mathrm{BSC}(\varepsilon/2)$. So $\mathrm{BSC}(p)$ is a degraded form of $\mathrm{BEC}(2p)$, and $1 - h(p) \le 1 - 2p$ for $p \le 1/2$. An error at an unknown place costs more than an erasure at a known place. The same exchange rate shows in block codes: a code of [minimum distance](/minimum-distance/) $d$ fills $d - 1$ erasures but corrects only $\lfloor (d - 1)/2 \rfloor$ errors.
- **Errors and erasures together.** The binary symmetric erasure channel both flips and erases bits. A code of minimum distance $d$ handles $\tau$ errors and $e$ erasures when $2\tau + e < d$.
- **Soft information.** A receiver on the [additive white Gaussian noise channel](/additive-white-gaussian-noise-channel/) that marks outputs near zero as $?$ turns the channel into one with errors and erasures. The erasure channel is the extreme case where every output is either certain or carries no information at all.

## Known results in the model

1. **Capacity.** The [channel capacity](/channel-capacity/) is $C = 1 - \varepsilon$ bits per use. *Proof.* For any input law, $I(X; Y) = H(X) - H(X \mid Y)$. When $Y \ne ?$ it tells $X$ exactly, and when $Y = ?$ (probability $\varepsilon$, independent of $X$) it tells nothing, so $H(X \mid Y) = \varepsilon H(X)$ and $I(X; Y) = (1 - \varepsilon) H(X)$. This is largest, $1 - \varepsilon$, for the uniform input. The value is intuitive: a fraction $\varepsilon$ of the bits is lost, and no code can carry more than the bits that arrive.
2. **Decoding a linear code is solving a linear system.** Let $C$ have a $k \times n$ [generator matrix](/generator-matrix/) $G$, let $m$ be the message, and let $K$ be the set of positions that are not erased. Each $j \in K$ gives the equation $\sum_i m_i G_{ij} = y_j$ over $\mathrm{GF}(2)$. The message is the unique solution if and only if the columns of $G$ in $K$ have rank $k$; equivalently, no nonzero codeword is $0$ on all of $K$, that is, no nonzero codeword has its support inside the erased set $E$. When the rank is less than $k$, all solutions are equally likely, so Gaussian elimination is maximum likelihood decoding, and it takes $O(n k^2)$ bit operations. This is [erasure decoding](/erasure-decoding/).
3. **A worked case.** For the Hamming code $[7, 4, 3]$, every pattern of up to 2 erasures can be filled, because $d = 3$. Of the $\binom{7}{3} = 35$ patterns of 3 erasures, exactly 7 fail: those equal to the support of one of the 7 codewords of weight 3. Every pattern of 4 or more erasures fails, because then only 3 or fewer equations remain for 4 unknowns.
4. **MDS codes.** A code that fills every pattern of $n - k$ erasures has $d = n - k + 1$, the most the [Singleton bound](/singleton-bound/) allows. [Reed-Solomon codes](/reed-solomon-code/) are such codes over large alphabets, which is why they are used for lost packets and failed disks.
5. **Random codes reach capacity.** For a random binary $k \times n$ matrix, the probability that $k + s$ fixed columns have rank less than $k$ is less than $2^{-s}$, by a [union bound](/union-bound/) over the $2^k - 1$ nonzero messages. So with $n(1 - \varepsilon)$ positions received, any rate $k/n < 1 - \varepsilon$ works with failure probability that falls exponentially in $n$. The cost is cubic decoding, and the practical codes for this channel, [LDPC codes](/ldpc-code/) with [peeling decoding](/peeling-decoding/) and [fountain codes](/fountain-codes/), reach rates close to capacity in linear time.
6. **Repetition.** The [repetition code](/repetition-code/) of length $n$ fails only when all $n$ copies are erased, with probability $\varepsilon^n$. Its rate $1/n$ is far below $1 - \varepsilon$.
7. **Feedback does not raise capacity, but makes it easy.** If the sender learns which bits were erased, it can resend each erased bit until it arrives. Each bit then takes $1/(1 - \varepsilon)$ uses on average, so the rate is $1 - \varepsilon$: capacity with no code at all. For any memoryless channel, feedback does not raise capacity.

## References
