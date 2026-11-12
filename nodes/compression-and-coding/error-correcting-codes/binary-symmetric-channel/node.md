---
tag: F9CZ5N
kind: model
slug: binary-symmetric-channel
name: Binary symmetric channel
aliases:
- BSC
area: compression-and-coding/error-correcting-codes
level: core
summary: A channel with input and output bits that flips each bit with the same probability p, independently of all other bits. Its capacity is 1 - h(p) bits per use.
prereqs: [binary-entropy-function, independent-random-variables]
see_also: [channel-capacity, binary-erasure-channel, additive-white-gaussian-noise-channel, maximum-likelihood-decoding, channel-coding-theorem, minimum-distance, undetected-error-probability, repetition-code]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Part II (the discrete channel with noise), Section 12 (equivocation and channel capacity, with the example of binary symbols received in error one time in 100)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 7.1.4 (binary symmetric channel, p. 187) and Section 7.2 (symmetric channels, p. 189)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 1 (the binary symmetric channel and the repetition and Hamming codes on it) and Chapter 9 (communication over a noisy channel)
  - paper: "Peter Elias, Coding for noisy channels, IRE Convention Record 3(4), 1955"
    locator: pp. 37 to 46 (block and convolutional parity check codes on the binary symmetric channel, and their error probability at rates below capacity)
---

The binary symmetric channel is the simplest model of a noisy link that carries bits. Each bit that goes in comes out flipped with probability $p$ and unchanged with probability $1 - p$, and the flips of different bits are [independent](/independent-random-variables/). It is the standard test bed for binary codes: decoding by maximum likelihood on it is decoding to the nearest codeword in [Hamming distance](/hamming-distance/), and its capacity has the closed form $1 - h(p)$.

## The machine

The channel has input alphabet $\{0, 1\}$, output alphabet $\{0, 1\}$ and one parameter, the **crossover probability** $p \in [0, 1]$. One use of the channel takes a bit $x$ and returns

$$y = x \oplus z, \qquad \Pr[z = 1] = p,$$

where $z$ is a fresh noise bit for each use. The transition matrix is

$$W = \begin{pmatrix} 1 - p & p \\ p & 1 - p \end{pmatrix}, \qquad W(y \mid x) = \Pr[\text{output } y \mid \text{input } x].$$

The channel is *memoryless*: over $n$ uses with inputs $x = (x_1, \ldots, x_n)$ the noise word $z = x \oplus y$ has independent bits, so

$$W^n(y \mid x) = \prod_{i=1}^{n} W(y_i \mid x_i) = p^{d(x, y)} (1 - p)^{n - d(x, y)},$$

where $d$ is the Hamming distance. The probability depends on $x$ and $y$ only through the number of flipped positions. The sender does not see the output (there is no feedback), and the receiver knows $p$ but not $z$.

A code for the channel is a set $C$ of $M$ binary words of length $n$. The sender picks a message, sends its codeword, and the receiver applies a decoder $g : \{0, 1\}^n \to C$.

## What it counts

- **Rate.** $R = (\log_2 M)/n$ message bits per channel use. For a [linear code](/linear-code/) of dimension $k$ it is $k/n$.
- **Block error probability.** The probability that $g(y)$ is not the codeword that was sent, for the worst message or on average over equally likely messages.
- **Bit error probability.** The average fraction of wrong message bits after decoding, for codes whose messages are bit strings.
- **Number of flips.** The weight of the noise word $z$ has the [binomial distribution](/binomial-distribution/) with parameters $n$ and $p$. Its mean is $np$, so a code of length $n$ must expect about $np$ errors, and by the [law of large numbers](/law-of-large-numbers/) the fraction of flips is close to $p$ for long blocks.

The cost of decoding (time and memory) is a separate measure; the model itself only says how reliable a given code and decoder are.

## Relation to other models

- **Values of $p$.** With $p = 0$ the channel is noiseless. With $p = 1/2$ the output is independent of the input and nothing can be sent. A channel with $p > 1/2$ is $\mathrm{BSC}(1 - p)$ with the output bits inverted, so one may assume $p \le 1/2$.
- **Cascades.** $\mathrm{BSC}(p)$ followed by $\mathrm{BSC}(q)$ is $\mathrm{BSC}(p(1 - q) + q(1 - p))$, because a bit ends up flipped when exactly one of the two channels flips it. For $p, q \le 1/2$ the result is at least as noisy as each part.
- **[Binary erasure channel](/binary-erasure-channel/).** The erasure channel $\mathrm{BEC}(\varepsilon)$ loses bits but never changes them. If the receiver replaces each erasure by a fair coin flip, the result is $\mathrm{BSC}(\varepsilon/2)$. So $\mathrm{BSC}(p)$ is a degraded form of $\mathrm{BEC}(2p)$, and its capacity is at most $1 - 2p$. An error whose place is unknown costs more than an erasure.
- **[Additive white Gaussian noise channel](/additive-white-gaussian-noise-channel/).** Send $\pm\sqrt{E_s}$ over a Gaussian channel and let the receiver keep only the sign of each output (a *hard decision*). The result is a BSC with $p = Q(\sqrt{2E_s/N_0})$. Hard decisions throw away information, and the loss is about 2 dB at low rates.
- **Other discrete channels.** The $q$-ary symmetric channel changes a symbol to each of the $q - 1$ others with probability $p/(q - 1)$. The Z channel flips only ones into zeros; it is not symmetric, and its best input is not uniform (see [channel capacity](/channel-capacity/)). Channels with memory, such as the Gilbert-Elliott channel, model [burst errors](/burst-errors/). On a BSC, errors come close together only by chance.

## Known results in the model

1. **Capacity.** The [channel capacity](/channel-capacity/) of $\mathrm{BSC}(p)$ is $C = 1 - h(p)$ bits per use, where $h$ is the [binary entropy function](/binary-entropy-function/). *Proof.* For any input law, $I(X; Y) = H(Y) - H(Y \mid X)$. Given $X = x$, the output is $x$ or its flip with probabilities $1 - p$ and $p$, so $H(Y \mid X) = h(p)$. A binary output has $H(Y) \le 1$, with equality when $Y$ is uniform, which happens for the uniform input. So $\max I(X; Y) = 1 - h(p)$. Examples: $C(0.01) \approx 0.919$, which is Shannon's example of 1000 bits per second with one bit in 100 received in error, where 81 bits per second are lost; $C(0.11) \approx 0.500$; $C(1/2) = 0$.
2. **Coding theorem.** By the [noisy-channel coding theorem](/channel-coding-theorem/), for each rate $R < 1 - h(p)$ there are codes with block error probability tending to 0 as $n$ grows, and for $R > 1 - h(p)$ the error probability of every code sequence tends to 1. Random linear codes are enough to reach capacity on the BSC (Elias, 1955), and [polar codes](/polar-code/) reach it with encoding and decoding in $O(n \log n)$ time.
3. **Maximum likelihood is minimum distance.** For $p < 1/2$, the [maximum likelihood decoder](/maximum-likelihood-decoding/) returns a codeword nearest to $y$ in Hamming distance. *Proof.* $W^n(y \mid x) = (1 - p)^n \bigl(p/(1 - p)\bigr)^{d(x, y)}$, and $p/(1 - p) < 1$, so the likelihood falls as the distance grows. For $p > 1/2$ the order reverses, which is the inversion above.
4. **Guarantees from the minimum distance.** A code with [minimum distance](/minimum-distance/) $d$ corrects every pattern of at most $t = \lfloor (d - 1)/2 \rfloor$ flips, so its block error probability under minimum distance decoding is at most $\sum_{i > t} \binom{n}{i} p^i (1 - p)^{n - i}$. For a perfect code, such as the Hamming code $[7, 4, 3]$, equality holds: decoding fails exactly when 2 or more of the 7 bits flip, which for $p = 0.05$ is about $0.0444$.
5. **Undetected errors.** A linear code used only to detect errors misses the noise word $z$ exactly when $z$ is a nonzero codeword, so the probability of an undetected error is $\sum_{w \ge 1} A_w p^w (1 - p)^{n - w}$, with $A_w$ the number of codewords of weight $w$. See [undetected error probability](/undetected-error-probability/).
6. **Repetition is not enough.** The [repetition code](/repetition-code/) of odd length $n$ makes its error probability tend to 0 only by letting the rate $1/n$ tend to 0. Reliable communication at a fixed positive rate needs long codes with many codewords, which is the content of the coding theorem.

## References
