---
tag: VK14Z9
kind: theorem
slug: channel-coding-theorem
name: Noisy-channel coding theorem
aliases:
- Shannon's channel coding theorem
area: compression-and-coding/error-correcting-codes
level: core
summary: On a discrete memoryless channel, every rate below the capacity C has codes with error probability tending to 0, and no rate above C has. Shannon proved it in 1948 by random coding.
prereqs: [channel-capacity, asymptotic-equipartition-property, union-bound]
see_also: [source-coding-theorem, binary-symmetric-channel, binary-erasure-channel, additive-white-gaussian-noise-channel, polar-code, ldpc-code, concatenated-codes, gilbert-varshamov-bound]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Part II (the discrete channel with noise), Section 13 (the fundamental theorem for a discrete channel with noise) and Section 14 (discussion)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 7.5 (definitions, p. 192), Section 7.6 (jointly typical sequences, p. 195), Section 7.7 (channel coding theorem, p. 199), Section 7.9 (Fano's inequality and the converse, p. 206) and Section 2.10 (Fano's inequality, p. 37)
  - paper: doi:10.1215/ijm/1255380682
    title: J. Wolfowitz, The coding of messages subject to chance errors, Illinois Journal of Mathematics 1(4), 1957
    locator: pp. 591 to 606 (the strong converse for the discrete memoryless channel)
  - paper: doi:10.1109/TIT.1965.1053730
    title: Robert G. Gallager, A simple derivation of the coding theorem and some applications, IEEE Transactions on Information Theory 11(1), 1965
    locator: pp. 3 to 18 (the random coding bound with the exponent E_r(R), positive for all rates below capacity)
  - paper: "Amiel Feinstein, A new basic theorem of information theory, Transactions of the IRE Professional Group on Information Theory 4(4), 1954"
    locator: pp. 2 to 22 (a rigorous proof of the coding theorem with maximal error probability)
---

The noisy-channel coding theorem says that a noisy channel has a sharp speed limit, its [capacity](/channel-capacity/) $C$. At any rate below $C$, codes exist that make the probability of a decoding error as small as one wants; at any rate above $C$, no code does. Shannon stated and proved it in 1948 by a then new argument: choose the code at random, and show that the average error over all codes is small. It created the field of channel coding, whose goal since then has been to find codes that come close to $C$ with fast decoders.

## Statement

Let a discrete memoryless channel have input alphabet $\mathcal{X}$, output alphabet $\mathcal{Y}$, transition probabilities $W(y \mid x)$, no feedback, and capacity

$$C = \max_{r} I(X; Y), \qquad X \sim r.$$

An $(M, n)$ code maps each of $M$ messages to a word of $n$ input symbols, and a decoder maps each output word to a message. Its rate is $R = (\log_2 M)/n$, its maximal error probability $\lambda^{(n)}$ is the largest probability of a wrong decision over the messages, and its average error probability $P_e^{(n)}$ is the mean over equally likely messages.

**Theorem.**

1. **Achievability.** For every $R < C$ and every $\delta > 0$, for all large $n$ there is an $(M, n)$ code with $M \ge 2^{nR}$ and $\lambda^{(n)} < \delta$.
2. **Weak converse.** Every $(M, n)$ code with $M \ge 2^{nR}$ has
   $$P_e^{(n)} \ge 1 - \frac{C}{R} - \frac{1}{nR}.$$
   So for $R > C$ the error probability stays above a positive constant as $n \to \infty$.
3. **Strong converse** (Wolfowitz, 1957). For $R > C$, the error probability of every sequence of codes tends to 1.

## In plain words

Noise destroys some of what is sent. One might think that the only way to make errors rare is to send each bit many times, so that the rate falls toward zero. The theorem says this is wrong. Each channel has a number, its capacity. If you send slower than that, you can make errors as rare as you like by using long enough blocks, and you never have to slow down further. If you send faster, errors will happen, whatever you do.

The proof picks the code at random. On average a random code is good, so at least one good code exists. The proof does not say how to find it or how to decode it fast.

## Proof

The full proof is in the proof file. It has two halves, in the plan of Cover and Thomas.

1. **Joint typicality.** For an input law $r$, a pair of words $(x^n, y^n)$ is *jointly typical* if the empirical values of $-\frac1n \log_2$ of its probabilities are close to $H(X)$, $H(Y)$ and $H(X, Y)$. The [law of large numbers](/law-of-large-numbers/) makes the sent and received words jointly typical with probability tending to 1. Counting shows that an independent word is jointly typical with the received word with probability only about $2^{-n I(X; Y)}$. This is the [asymptotic equipartition property](/asymptotic-equipartition-property/) for pairs.
2. **Random code and decoder.** Choose $r$ with $I(X; Y) = C$ and draw about $2^{nR}$ codewords with i.i.d. symbols of law $r$. The decoder looks for the one codeword jointly typical with the output. It fails if the sent codeword is not typical (small probability) or if some other codeword is; by a [union bound](/union-bound/), the second event has probability at most about $2^{nR} \cdot 2^{-nC}$, which tends to 0 when $R < C$.
3. **Derandomize.** The error averaged over all codebooks is small, so some codebook has a small average error. Throw away the worse half of its codewords: each one that is left has a small error, and the rate drops by only $1/n$.
4. **Converse.** Let the message $U$ be uniform. Fano's inequality bounds the [conditional entropy](/conditional-entropy/) that is left about $U$ after decoding: $H(U \mid \hat U) \le 1 + P_e^{(n)} \log_2 M$. The data processing inequality and the memoryless property give $I(U; \hat U) \le I(X^n; Y^n) \le nC$. Since $\log_2 M = H(U \mid \hat U) + I(U; \hat U)$, dividing by $\log_2 M \ge nR$ gives the bound of part 2. $\blacksquare$

**A Monte Carlo view.** The implementation draws a new random codebook in each trial on the [binary symmetric channel](/binary-symmetric-channel/) with $p = 0.11$, where $C \approx 0.500$, and decodes by maximum likelihood (nearest codeword, ties broken at random). With seed 1 it gives these block error rates, with 2000 trials at rate $1/4$ and 500 at rate $3/4$.

| $n$ | rate $1/4$, error | union bound, ML decoding | $n$ | rate $3/4$, error | Fano lower bound |
|---|---|---|---|---|---|
| 8 | 0.086 | 0.167 | 4 | 0.384 | 0.000 |
| 16 | 0.062 | 0.099 | 8 | 0.508 | 0.167 |
| 24 | 0.027 | 0.059 | 12 | 0.600 | 0.222 |
| 32 | 0.017 | 0.036 | 16 | 0.640 | 0.250 |
| 40 | 0.020 | 0.022 | | | |

Below capacity the error falls with $n$ and stays under the union bound for maximum likelihood decoding of a random code; the last row differs from the one above it by sampling noise only. Above capacity it grows with $n$ and stays above the Fano bound, which tends to $1 - C/R = 1/3$. These lengths are tiny: a code of rate $3/4$ and length 16 has $2^{12}$ codewords, and exhaustive decoding of a random code becomes impossible long before the asymptotic regime.

## Consequences

- **Capacity has an operational meaning.** The formula $\max I(X; Y)$, a property of one channel use, equals the largest rate that long codes can use reliably. Examples: $1 - h(p)$ for the binary symmetric channel, $1 - \varepsilon$ for the [binary erasure channel](/binary-erasure-channel/), and $\frac12 \log_2(1 + \mathrm{SNR})$ for the [Gaussian channel](/additive-white-gaussian-noise-channel/), where the same proof works with a power limit.
- **Separation of source and channel coding.** Together with the [source coding theorem](/source-coding-theorem/), it shows that a source of entropy rate $H$ can be sent over the channel reliably if $H < C$ and not if $H > C$. So compression and error correction can be designed separately with no loss in rate, for long blocks.
- **Linear codes are enough.** For the binary symmetric channel the same random argument works with a random [linear code](/linear-code/) (Elias, 1955), so decoders can use the algebra of linear codes. Good codes have a [minimum distance](/minimum-distance/) that grows in proportion to $n$, as the [Gilbert-Varshamov bound](/gilbert-varshamov-bound/) also shows.
- **Error exponents (outline).** Gallager (1965) bounded the average error of random codes by $2^{-n E_r(R)}$, with
  $$E_r(R) = \max_{0 \le \rho \le 1} \max_r \bigl(E_0(\rho, r) - \rho R\bigr), \qquad E_0(\rho, r) = -\log_2 \sum_y \Bigl(\sum_x r(x) W(y \mid x)^{1/(1 + \rho)}\Bigr)^{1 + \rho}.$$
  $E_r(R) > 0$ for every $R < C$. For the binary symmetric channel with $p = 0.11$ and the uniform input, $E_r$ is about 0.199 at $R = 0.1$, 0.065 at $R = 0.25$ and 0.009 at $R = 0.4$. So the error falls exponentially in $n$, but the exponent goes to 0 as $R \to C$, and rates close to capacity need long blocks.
- **The search for practical codes.** The theorem shows that good codes exist but not how to decode them fast. [Concatenated codes](/concatenated-codes/) (Forney, 1966) gave error probability falling exponentially in $n$ at any rate below $C$ with polynomial-time decoding. [Turbo codes](/turbo-code/) (1993) and [LDPC codes](/ldpc-code/) with iterative decoding work close to capacity in practice, and [polar codes](/polar-code/) (Arikan, 2009) provably achieve the capacity of binary-input symmetric channels with $O(n \log n)$ encoding and decoding.

## Tightness

- **The constant $C$ is exact.** The converse shows that no rate above $C$ is achievable, so the threshold cannot move in either direction.
- **The weak converse is not the end.** It only keeps the error probability above $1 - C/R$. The strong converse shows that for a discrete memoryless channel the error tends to 1 above capacity, so there is no trade-off between rate and error probability for long blocks. For some channels with memory, only the weak converse holds.
- **Rate exactly $C$.** The theorem says nothing about codes of rate exactly $C$; the answer depends on the channel and on how fast the error must fall.
- **Feedback.** For a memoryless channel, feedback from the receiver to the sender does not raise the capacity, so the theorem holds with feedback too (the converse needs a slightly different argument, since $X^n$ then depends on past outputs). Feedback can make coding much simpler, as on the [binary erasure channel](/binary-erasure-channel/).
- **Average and maximal error.** The proof first gets a small average error and then removes the worst half of the codewords. For the rate, the two criteria give the same capacity.

## History

Shannon stated the theorem in "A mathematical theory of communication" in 1948, with the random coding argument and typical sequences. Feinstein (1954) gave a rigorous proof with maximal error probability, and Wolfowitz (1957) proved the strong converse for discrete memoryless channels. Elias (1955) showed that random linear codes reach the capacity of the binary symmetric channel and introduced convolutional codes. Gallager (1965) gave a short proof with an explicit exponential bound on the error, the form in which the theorem is often taught. The proof by joint typicality used here is the one in the textbook of Cover and Thomas.

## References
