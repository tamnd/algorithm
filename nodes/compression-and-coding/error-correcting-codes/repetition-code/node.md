---
tag: 8TYFGD
kind: definition
slug: repetition-code
name: Repetition code
aliases:
- majority-vote code
area: compression-and-coding/error-correcting-codes
level: intro
summary: The [n, 1, n] code that sends each symbol n times and decodes by majority vote. Its error falls exponentially in n, but its rate 1/n falls to 0, far from capacity.
prereqs: [minimum-distance, binary-symmetric-channel, binomial-distribution]
see_also: [majority-logic-decoding, hamming-code, hamming-bound, channel-coding-theorem, chernoff-bound, parity-bit, product-codes, binary-erasure-channel]
sources:
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 1, Section 1.2 (repetition codes on the binary symmetric channel, the code R3 and its error probability 3p^2 - 2p^3, and the length needed for very small error)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 3.7 (single-parity-check codes, repetition codes and self-dual codes)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 7.11 (Hamming codes, p. 210), which starts from the repetition code and its rate
---

A repetition code sends each message symbol $n$ times, and the receiver decides by a majority vote over the $n$ copies. It is the oldest and simplest error-correcting code, the code of "say it again". It corrects up to $\lfloor (n - 1)/2 \rfloor$ errors per block, and its error probability falls exponentially in $n$. But its rate $1/n$ falls too, and it shows what the [channel coding theorem](/channel-coding-theorem/) says better codes avoid: buying reliability with rate.

## Definition

Let $\Sigma$ be an alphabet. The **repetition code** of length $n$ over $\Sigma$ is

$$\mathrm{Rep}_n = \{\, (a, a, \ldots, a) \in \Sigma^n : a \in \Sigma \,\}.$$

The encoder maps the symbol $a$ to $a^n$. Over a field $\mathrm{GF}(q)$ it is the [linear code](/linear-code/) with generator matrix $(1\ 1\ \cdots\ 1)$, of dimension 1 and [minimum distance](/minimum-distance/) $n$, so it is an $[n, 1, n]_q$ code with rate $R = 1/n$.

**Majority decoding.** Given a received block $y$, output the symbol that occurs most often in $y$. This is the codeword nearest to $y$ in [Hamming distance](/hamming-distance/), since $d(y, a^n)$ is $n$ minus the number of copies of $a$. On a [binary symmetric channel](/binary-symmetric-channel/) with $p < 1/2$ it is therefore [maximum likelihood decoding](/maximum-likelihood-decoding/). It takes $O(n)$ time per block. For odd $n$ and binary symbols there is never a tie; for even $n$ a tie of $n/2$ against $n/2$ is broken by a fair coin or reported as a failure.

**What it guarantees.** With $d = n$, the code detects up to $n - 1$ errors (any block that is not constant), corrects up to $t = \lfloor (n - 1)/2 \rfloor$ errors by majority, and fills up to $n - 1$ erasures (any one copy that arrives is enough).

**Exact error probability.** On $\mathrm{BSC}(p)$ the number of flipped copies has the [binomial distribution](/binomial-distribution/) with parameters $n$ and $p$. For odd $n$, majority decoding fails exactly when more than half of the copies flip:

$$P_e(n) = \sum_{i = (n+1)/2}^{n} \binom{n}{i} p^i (1 - p)^{n - i}.$$

For $n = 3$ this is $3p^2(1 - p) + p^3 = 3p^2 - 2p^3$.

**Even lengths do not help.** With fair tie-breaking, $P_e(2k) = P_e(2k - 1)$. *Proof.* Compare the vote on the first $2k - 1$ copies with the vote on all $2k$. The decision changes only if the first $2k - 1$ copies have a margin of one. If $k - 1$ of them flipped (the vote was right) and the last copy flips, the tie costs half an error, with probability $\binom{2k-1}{k-1} p^{k-1} (1 - p)^{k} \cdot p \cdot \frac12$. If $k$ flipped (the vote was wrong) and the last copy is right, the tie saves half an error, with probability $\binom{2k-1}{k} p^{k} (1 - p)^{k-1} \cdot (1 - p) \cdot \frac12$. The two terms are equal, so they cancel.

**Speed of decay.** For $p < 1/2$, a [Chernoff bound](/chernoff-bound/) gives $P_e(n) \le \bigl(4p(1 - p)\bigr)^{n/2} = 2^{-n D(1/2 \,\|\, p)}$, where $D(1/2 \,\|\, p) = -\frac12 \log_2\bigl(4p(1 - p)\bigr)$, and this exponent is the true rate of decay as $n \to \infty$. So to reach an error probability $\delta$, the length must grow like $\log(1/\delta)/D(1/2 \,\|\, p)$, and the rate $1/n$ falls to 0 like $1/\log(1/\delta)$.

## Examples and non-examples

**Examples.**

- **The code R3 on $\mathrm{BSC}(0.1)$.** The bit error rate drops from $0.1$ to $3(0.01) - 2(0.001) = 0.028$, at the price of three channel uses per bit. Lengths 5, 7 and 9 give about $8.6 \times 10^{-3}$, $2.7 \times 10^{-3}$ and $8.9 \times 10^{-4}$.
- **Very small error.** On $\mathrm{BSC}(0.1)$ the least odd length with $P_e \le 10^{-15}$ is $n = 63$, a rate below $0.016$. The capacity is $1 - h(0.1) \approx 0.531$, so the coding theorem promises the same error at a rate more than 30 times higher, with long codes.
- **A perfect code.** For odd $n$ the two balls of radius $(n - 1)/2$ around $0^n$ and $1^n$ contain $2 \sum_{i \le (n-1)/2} \binom{n}{i} = 2^n$ words, so they cover the whole space with no overlap. The binary repetition codes of odd length meet the [Hamming bound](/hamming-bound/) with equality; they are trivial perfect codes.
- **On the [binary erasure channel](/binary-erasure-channel/)** the code fails only when all $n$ copies are erased, with probability $\varepsilon^n$, against a capacity of $1 - \varepsilon$.
- **On the Gaussian channel with soft decisions**, adding the $n$ received values and taking the sign is the best decoder. Each copy has energy $E_b/n$, so the sum has the same signal-to-noise ratio as one uncoded symbol of energy $E_b$, and the coding gain $10 \log_{10}(R\,d) = 10 \log_{10} 1 = 0$ dB is zero. Repetition only helps there with hard decisions or with time diversity on a fading channel.
- **Inside other schemes.** Repeat-accumulate codes, [turbo](/turbo-code/) and [LDPC](/ldpc-code/) designs use repetition as one component, and redundant hardware with majority voting (triple modular redundancy) is a repetition code in space instead of time.

**Non-examples.**

- **Retransmission on request.** In automatic repeat request ([error detection](/error-detection/) with feedback), a copy is sent again only when the receiver reports an error. The number of copies depends on the channel, so this is a protocol, not a block code with a fixed $n$.
- **The single parity check code** $[n, n - 1, 2]$ (a [parity bit](/parity-bit/)) is the dual of the binary repetition code, not a repetition code. It has rate close to 1 and only detects one error.
- **A code that repeats a block of $k$ bits** $n$ times is the [product](/product-codes/) of the trivial code of length $k$ and $\mathrm{Rep}_n$, with rate $1/n$ and distance $n$; it is not better than repeating each bit, it only orders the copies differently. Interleaved copies do help against [burst errors](/burst-errors/), since the copies of a bit are then far apart.

## Related definitions

- [Minimum distance](/minimum-distance/): the repetition code has $d = n$, the largest possible for length $n$, and dimension 1, the smallest.
- [Majority logic decoding](/majority-logic-decoding/): decodes other codes, such as Reed-Muller codes, by majority votes over many parity checks, each a repetition-like estimate of one bit.
- [Hamming code](/hamming-code/): the $[7, 4, 3]$ Hamming code corrects one error like $\mathrm{Rep}_3$, but at rate $4/7$ instead of $1/3$.
- [Channel coding theorem](/channel-coding-theorem/): the reason why repetition is wasteful. Reliable communication at a fixed positive rate needs codes whose number of codewords grows with $n$.

## References
