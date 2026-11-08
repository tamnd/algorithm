---
tag: ZRF22N
kind: problem
slug: unbiased-bits-from-biased-coin
name: Unbiased bits from a biased coin
aliases:
- coin flipping with a biased coin
- debiasing
- randomness extraction from a biased coin
area: numerical/random-number-generation
level: intro
summary: Producing fair random bits from a source of independent flips with unknown fixed bias.
prereqs: [independence-of-events, binary-entropy-function, geometric-distribution]
see_also: [von-neumann-debiasing, randomness-extractor, true-random-number-generator, entropy-source, uniform-random-integer-generation, santha-vazirani-source]
sources:
  - paper: "John von Neumann, Various techniques used in connection with random digits, in Monte Carlo Method, National Bureau of Standards Applied Mathematics Series 12, 1951, pages 36 to 38"
    locator: the procedure that maps the pairs 01 and 10 to an output bit and drops 00 and 11
  - paper: doi:10.1214/aos/1176348543
    title: Yuval Peres, Iterating von Neumann's procedure for extracting random bits, Annals of Statistics 20(1), 1992, pages 590 to 597
    locator: the iterated procedure and the theorem that its rate tends to the entropy h(p)
  - paper: doi:10.1214/aoms/1177692552
    title: Peter Elias, The efficient construction of an unbiased random sequence, Annals of Mathematical Statistics 43(3), 1972, pages 865 to 870
    locator: the block procedure, the upper bound h(p) on the rate and procedures that approach it
  - paper: "Manuel Blum, Independent unbiased coin flips from a correlated biased source, a finite state Markov chain, Combinatorica 6(2), 1986, pages 97 to 108"
    locator: the extension of von Neumann's method to a source that is a finite Markov chain with unknown transition probabilities
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 10, Entropy, Randomness, and Information (Section 10.2, entropy and binomial coefficients, and Section 10.3, extracting random bits from a biased coin)
---

The problem of unbiased bits from a biased coin asks for independent fair bits, given independent flips of a coin that shows 1 with an unknown probability $p$, $0 < p < 1$. Von Neumann's method (1951) takes pairs of flips and keeps 01 and 10, which have the same probability $p(1-p)$ whatever $p$ is. No method can produce even one fair bit within a fixed number of flips for every $p$, and no method can give more than $h(p)$ fair bits per flip, the [binary entropy](/binary-entropy-function/) of the coin; Peres's iteration of von Neumann's method reaches this rate in the limit.

## In plain words

You have a bent coin. It falls on heads more often than on tails, but you do not know by how much. Can you still make a fair decision?

Yes. Flip the coin twice. If you get heads then tails, say "heads". If you get tails then heads, say "tails". If both flips are the same, forget them and flip twice again. Heads then tails and tails then heads are equally likely for any coin, because they contain one head and one tail, only in a different order.

The method wastes many flips. Smarter methods reuse the information in the flips that the simple method throws away, and they come close to the best possible rate, which depends on how bent the coin is.

## Definition

**Input.** A sequence $B_1, B_2, \ldots$ of independent bits with $\Pr[B_i = 1] = p$ for each $i$, where $p \in (0, 1)$ is fixed and unknown.

**Output.** One bit $Z$, or a sequence of bits $Z_1, \ldots, Z_L$ of random length $L$, computed by a procedure that does not know $p$. The output must be fair for every $p \in (0, 1)$:

- *one-bit version:* the procedure stops with probability 1 and $\Pr[Z = 1] = 1/2$;
- *block version:* from $n$ flips it outputs $L$ bits, and for each $\ell$ with $\Pr[L = \ell] > 0$ the output, given $L = \ell$, is uniform on $\{0, 1\}^\ell$.

**Cost.** The expected number of flips per output bit, or its inverse, the *rate* $\mathbb{E}[L] / n$.

## Variants

- **Known $p$.** If $p$ is known, arithmetic decoding of the flips gives a rate as close to $h(p)$ as wanted; the difficulty of the main problem is that the procedure must work for all $p$ at once.
- **The reverse problem.** Simulate a $p$-coin from fair bits, which needs about 2 fair bits on average for any $p$ by comparing the bits with the binary expansion of $p$. Its generalization, a coin with probability $f(p)$ from a $p$-coin, is the Bernoulli factory problem.
- **Markov sources.** If the flips form a Markov chain with unknown transitions, Blum (1986) applies von Neumann's pairing to the successive exits from each state.
- **Weak sources.** If each flip may depend on the earlier ones, with a bias bounded by $\delta$ (a [Santha-Vazirani source](/santha-vazirani-source/)), no deterministic procedure can output even one nearly fair bit. A [randomness extractor](/randomness-extractor/) then needs a short truly random seed or several independent sources.
- **A die instead of a coin.** Fair dice from a biased die with $k$ faces: the same pairing idea works on any two distinct faces.

## Examples

**Von Neumann's method.** The flips 1 1 0 1 1 0 0 0 1 0 1 1 form the pairs 11, 01, 10, 00, 10, 11. The method keeps 01, 10 and 10 and outputs the first bit of each: 0, 1, 1. Three output bits from twelve flips.

**Peres's method on the same flips.** Besides the von Neumann output, form two new sequences from the pairs: $u$, the XOR of each pair, which is 0, 1, 1, 0, 1, 0; and $v$, the common bit of each equal pair, which is 1, 0, 1. Apply the method again to $u$ and to $v$, and so on. On these twelve flips the output is 0, 1, 1, 0, 1, 1, 1: seven bits instead of three. The sequences $u$ and $v$ are biased in their own way, but Peres (1992) proved that the combined output is still a sequence of independent fair bits for every $p$, so no fairness is lost.

**Rates for $p = 0.7$.** Von Neumann's method outputs a bit from a pair with probability $2p(1-p) = 0.42$, a rate of $p(1-p) = 0.21$ bits per flip. The best possible rate is $h(0.7) \approx 0.881$. Peres's method with $\nu$ levels of iteration has the rates below; they tend to $h(p)$.

| levels $\nu$ | 1 | 2 | 3 | 4 | 6 | 10 | 14 |
|---|---|---|---|---|---|---|---|
| rate for $p = 0.7$ | 0.210 | 0.370 | 0.493 | 0.586 | 0.712 | 0.826 | 0.864 |
| rate for $p = 0.5$ | 0.250 | 0.438 | 0.578 | 0.684 | 0.822 | 0.944 | 0.982 |

The rate of $\nu$ levels is $R_\nu(p) = pq + \frac12 R_{\nu-1}(2pq) + \frac12 (p^2 + q^2) R_{\nu-1}\!\big(p^2/(p^2 + q^2)\big)$ with $q = 1 - p$ and $R_0 = 0$: the three terms are the von Neumann output, the XOR sequence (one bit per pair, with bias $2pq$) and the sequence of equal pairs.

## Known algorithms

- **[Von Neumann's method](/von-neumann-debiasing/).** Pairs, keep 01 and 10. Exact for every $p$. Rate $p(1-p) \le 1/4$. Expected flips for one bit: $1/(p(1-p))$.
- **Hoeffding and Simons, Stout and Warren.** Variants that use longer blocks and the order of the flips inside a block, with higher rates.
- **Elias's method (1972).** Cut the flips into blocks of length $n$. Strings of a block with the same number of ones are equally likely, so number each class and output a uniform index from it, cut into fair bits. Exact. The rate tends to $h(p)$ as $n$ grows.
- **Peres's method (1992).** Recursive, as in the example above, with $\nu$ levels. Exact for every $p$, $O(n)$ time for $n$ flips with an explicit stack, and the rate tends to $h(p)$ as $\nu \to \infty$.
- **Extractors for weak sources.** When the flips are not independent, see [randomness extractor](/randomness-extractor/); they need extra assumptions or extra randomness.

## Bounds

**No bounded procedure.** Suppose a procedure always stops within $k$ flips and outputs $Z$. Then $\Pr[Z = 1] = \sum_{x \in A} p^{|x|} (1-p)^{k - |x|}$, where $A$ is the set of flip strings of length $k$ (padded) on which it outputs 1 and $|x|$ is the number of ones. This is a polynomial in $p$. As $p \to 0$ it tends to 1 if the all-zero string is in $A$ and to 0 otherwise, so it cannot equal $1/2$ for all $p \in (0, 1)$. Hence every exact procedure has an unbounded number of flips, and its stopping time has a tail, which is geometric for von Neumann's method.

**The entropy bound.** For the block version with $n$ flips $X = (B_1, \ldots, B_n)$ and output $(Z, L)$:

$$\mathbb{E}[L] \le H(X) = n\, h(p), \qquad h(p) = -p \log_2 p - (1-p) \log_2 (1-p).$$

*Proof.* The output is a function of $X$, so $H(X) \ge H(Z, L) = H(L) + H(Z \mid L)$. Given $L = \ell$, $Z$ is uniform on $2^\ell$ strings, so $H(Z \mid L = \ell) = \ell$, and $H(Z \mid L) = \mathbb{E}[L]$. Since $H(L) \ge 0$, $\mathbb{E}[L] \le H(X)$, and $H(X) = n h(p)$ because the flips are independent. $\square$

**Optimality.** Elias (1972) and Peres (1992) give exact procedures whose rate tends to $h(p)$ for every $p$, so the bound is tight in the limit. For $p = 1/2$, $h(p) = 1$, but von Neumann's method still has rate only $1/4$.

## Reductions

- **[Uniform random integers](/uniform-random-integer-generation/)** reduce to fair bits, so a biased coin gives fair dice by composition.
- **Debiasing a physical source.** The conditioning step of a [true random number generator](/true-random-number-generator/) solves this problem when the raw bits are independent; when they are not, it uses a hash or an [extractor](/randomness-extractor/).
- **The reverse problem**, a $p$-coin from fair bits, reduces to comparing a fair binary expansion with that of $p$.

## Applications

Conditioning of hardware noise in [entropy sources](/entropy-source/) (the von Neumann corrector is common in hardware designs), fair decisions with physical coins or dice, teaching examples of [randomness extraction](/randomness-extractor/), and the analysis of randomized algorithms that receive their random bits from an imperfect source.

## References
