---
tag: T7RZCY
kind: theorem
slug: leftover-hash-lemma
name: Leftover hash lemma
aliases:
- privacy amplification lemma
- randomness extraction by universal hashing
area: randomized/derandomization
level: research
summary: A random function from a universal hash family maps a source of min-entropy k to m bits that are 2^(-(k-m)/2-1)-close to uniform, even when the function is revealed.
prereqs: [universal-hash-family, min-entropy, randomness-extractor, total-variation-distance]
see_also: [seeded-extractor, randomness-extraction, hill-prg-from-one-way-functions, universal-hashing, pairwise-independence, hkdf, trevisan-extractor, two-source-extractor]
sources:
  - paper: doi:10.1145/73007.73009
    title: Russell Impagliazzo, Leonid A. Levin and Michael Luby, Pseudo-random generation from one-way functions, 21st ACM Symposium on Theory of Computing (STOC), 1989
    locator: the lemma that universal hashing extracts almost uniform bits from a source with enough entropy
  - paper: doi:10.1137/S0097539793244708
    title: Johan Hastad, Russell Impagliazzo, Leonid A. Levin and Michael Luby, A pseudorandom generator from any one-way function, SIAM Journal on Computing 28(4), 1999
    locator: the leftover hash lemma as stated and used in the construction of a generator from a one-way function
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 1979
    locator: the definition of universal families of hash functions
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 6 (the leftover hash lemma, its proof by collision probability, and its parameters as an extractor)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 21 (randomness extractors and the leftover hash lemma)
---

The leftover hash lemma says that hashing a weak random source with a function chosen from a [universal hash family](/universal-hash-family/) gives almost uniform bits. If the source has [min-entropy](/min-entropy/) $k$ and the output has $m$ bits, the output, together with the name of the function, is within statistical distance $\frac12\sqrt{2^{m-k}}$ of uniform. So a [strong seeded extractor](/seeded-extractor/) can output $k - 2\log_2(1/\varepsilon)$ bits with error $\varepsilon/2$, and the loss of $2\log_2(1/\varepsilon)$ bits is optimal. The price is a long seed, about $n$ bits. The lemma is due to Impagliazzo, Levin and Luby (1989) and is a key step of [HILL](/hill-prg-from-one-way-functions/); in cryptography it is called privacy amplification.

## Statement

A family $\mathcal{H}$ of functions $h : \{0,1\}^n \to \{0,1\}^m$ is *universal* if $\Pr_{h \in \mathcal{H}}[h(x) = h(x')] \le 2^{-m}$ for all $x \ne x'$, with $h$ uniform in $\mathcal{H}$. A random variable $X$ has *min-entropy* at least $k$ if $\Pr[X = x] \le 2^{-k}$ for every $x$, and *collision probability* $\mathrm{CP}(X) = \sum_x \Pr[X = x]^2 = \Pr[X = X']$ for an independent copy $X'$. The statistical distance is $\Delta(P, Q) = \frac12 \sum_z |P(z) - Q(z)|$.

**Theorem (leftover hash lemma).** Let $\mathcal{H}$ be a universal family of functions from $\{0,1\}^n$ to $\{0,1\}^m$, let $H$ be uniform in $\mathcal{H}$, and let $X$ be independent of $H$ with $\mathrm{CP}(X) \le 2^{-k}$. Then

$$\Delta\big((H, H(X)),\ (H, U_m)\big) \le \frac12 \sqrt{2^{m-k}}.$$

Min-entropy $k$ implies $\mathrm{CP}(X) \le \max_x \Pr[X = x] \le 2^{-k}$, so the bound holds for every source of min-entropy $k$. In the language of extractors: for $\varepsilon > 0$ and $m = k - 2\log_2(1/\varepsilon) + 2$, the map $(x, h) \mapsto h(x)$ is a strong $(k, \varepsilon)$-extractor with seed $\log_2|\mathcal{H}|$.

The lemma is unconditional.

## In plain words

A weak random source gives strings that are not uniform, but no single string is too likely. Pick a hash function at random from a good family and apply it to the source. The output is shorter than the source, and it is almost uniform, even to someone who knows which hash function was used.

The output can be almost as long as the amount of true randomness in the source. One gives up about twice the number of bits of safety one wants: to get an error of one in a million, about 40 bits fewer than the entropy.

## Proof

Let $Z = (H, H(X))$, a random variable on a set of size $N = |\mathcal{H}| \cdot 2^m$.

**Step 1: the collision probability of $Z$.** Let $(H', X')$ be an independent copy of $(H, X)$. A collision $Z = Z'$ needs $H = H'$, which has probability $1/|\mathcal{H}|$, and then $H(X) = H(X')$. Given $H = H'$, the function $H$ is still uniform in $\mathcal{H}$ and independent of $X, X'$. So

$$\mathrm{CP}(Z) = \frac{1}{|\mathcal{H}|} \Pr[H(X) = H(X')] \le \frac{1}{|\mathcal{H}|}\Big(\Pr[X = X'] + \Pr[X \ne X'] \cdot 2^{-m}\Big) \le \frac{1}{|\mathcal{H}|}\big(2^{-k} + 2^{-m}\big),$$

using universality for the pairs with $X \ne X'$.

**Step 2: from collision probability to distance in $\ell_2$.** Let $p$ be the distribution of $Z$ and $u$ the uniform distribution on the $N$ points. Then

$$\|p - u\|_2^2 = \sum_z p(z)^2 - \frac{2}{N}\sum_z p(z) + \frac{N}{N^2} = \mathrm{CP}(Z) - \frac1N \le \frac{2^{-k} + 2^{-m}}{|\mathcal{H}|} - \frac{2^{-m}}{|\mathcal{H}|} = \frac{2^{-k}}{|\mathcal{H}|}.$$

**Step 3: from $\ell_2$ to $\ell_1$.** By the Cauchy-Schwarz inequality, $\|v\|_1 \le \sqrt{N}\,\|v\|_2$ for every vector $v$ with $N$ entries. So

$$\Delta(Z, (H, U_m)) = \frac12\|p - u\|_1 \le \frac12\sqrt{N \cdot \frac{2^{-k}}{|\mathcal{H}|}} = \frac12\sqrt{2^{m - k}}.$$

The distribution of $(H, U_m)$ is $u$, so this is the claim. $\blacksquare$

**The Toeplitz family is universal.** Let $T$ be an $m \times n$ matrix over $\mathrm{GF}(2)$ that is constant on each diagonal, with entry $T_{ij} = t_{i - j + n - 1}$ for a uniform $t \in \{0,1\}^{n+m-1}$, and $h_t(x) = Tx$. For $x \ne x'$, let $z = x \oplus x' \ne 0$ and let $j^*$ be the first coordinate with $z_{j^*} = 1$. Then $h_t(x) = h_t(x')$ if and only if $Tz = 0$. Row $i$ of $Tz$ is $t_{i - j^* + n - 1} \oplus (\text{terms with } t_{i - j + n - 1},\ j > j^*)$. The index $i - j^* + n - 1$ is larger than every other index in row $i$, and it is a new index for each $i$. Fix all bits of $t$ except these $m$ bits: then each row of $Tz$ is its own new bit plus a fixed value, so $Tz$ is uniform in $\{0,1\}^m$ and $\Pr[Tz = 0] = 2^{-m}$ exactly. The seed has $n + m - 1$ bits.

**Exact values.** For $n = 4$, the Toeplitz family and the worst flat source of each size, the distance and the bound of the lemma are:

| $k$ | $m$ | worst distance | bound $\frac12\sqrt{2^{m-k}}$ |
|---|---|---|---|
| 2 | 1 | $3/16 = 0.1875$ | 0.3536 |
| 2 | 2 | $21/64 \approx 0.328$ | 0.5 |
| 3 | 1 | $1/8 = 0.125$ | 0.25 |
| 3 | 2 | $29/128 \approx 0.227$ | 0.3536 |

For $k = 2, m = 1$ one worst source is the uniform distribution on $\{0000, 1000, 0100, 0010\}$ in the order $x_0 x_1 x_2 x_3$, that is, on the integers $0, 1, 2, 4$.

## Consequences

- **A strong extractor with optimal output.** With a universal family, the output length $m = k - 2\log_2(1/\varepsilon) + O(1)$ matches the lower bound of Radhakrishnan and Ta-Shma for every [extractor](/randomness-extractor/), so the entropy loss of the lemma cannot be improved. See [seeded extractor](/seeded-extractor/) for the comparison with constructions that have short seeds.
- **Privacy amplification.** Two parties share a key $X$ about which an adversary knows some information, so $X$ has min-entropy $k$ from the adversary's view. They agree in public on a random $h$ and use $h(X)$. The lemma says the new key is almost uniform even given $h$. This is how quantum key distribution and other protocols finish.
- **HILL.** The construction of a [generator from any one-way function](/hill-prg-from-one-way-functions/) uses the lemma to turn pseudoentropy into pseudorandom bits.
- **Key derivation.** The extract step of [HKDF](/hkdf/) follows the same plan: first condense the entropy of a secret into a short key, then expand it. HKDF uses HMAC instead of a universal family, so its analysis is not the lemma itself.
- **Rényi entropy.** The proof uses only $\mathrm{CP}(X) \le 2^{-k}$, the Rényi entropy of order 2, which is weaker than min-entropy $k$.
- **Many seeds are good.** By Markov's inequality, for all but a fraction $\sqrt{\varepsilon'}$ of the functions $h$, $\Delta(h(X), U_m) \le \sqrt{\varepsilon'}$, where $\varepsilon' = \frac12\sqrt{2^{m-k}}$.

## Tightness

- **Entropy loss.** Every strong or ordinary extractor with error $\varepsilon \le \frac12$ loses at least $2\log_2(1/\varepsilon) - O(1)$ bits of entropy (Radhakrishnan and Ta-Shma 2000). The lemma loses $2\log_2(1/\varepsilon) - 2$ bits, so it is optimal up to an additive constant.
- **Seed length.** The usual universal families have seeds of about $n$ bits or more: $n + m - 1$ bits for Toeplitz matrices and $2n$ bits for $x \mapsto$ the first $m$ bits of $ax + b$ in $\mathrm{GF}(2^n)$. Extractors with seed $O(\log n + \log(1/\varepsilon))$ exist, so the lemma is far from optimal in seed length.
- **Universality is needed.** The family $h_a(x) = (x_0, \ldots, x_{m-1}) \oplus a$ is not universal: two strings with the same first $m$ bits always collide. For the source that fixes the first $m$ bits to 0 and makes the rest uniform, with min-entropy $n - m$, the output is uniform only through $a$, and given $a$ it is constant. Then $\Delta = 1 - 2^{-m}$, much larger than the bound.
- **The bound is not reached by Toeplitz on small cases.** In the table above, the worst distance is between one half and two thirds of the bound.

## History

Carter and Wegman (1979) introduced universal hash families for data structures. Bennett, Brassard and Robert (1988) used hashing for privacy amplification, and Impagliazzo, Levin and Luby (1989) proved the lemma in the form above for the construction of generators from one-way functions. The name "leftover hash lemma" comes from Impagliazzo and Zuckerman (1989). The journal version of HILL (1999) gives the statement and the proof by collision probability. Vadhan's survey and Arora and Barak present it as the first example of a seeded extractor.

## References
