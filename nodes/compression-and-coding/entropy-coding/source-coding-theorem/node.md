---
tag: 53WS0H
kind: theorem
slug: source-coding-theorem
name: Shannon source coding theorem
aliases:
- noiseless coding theorem
- Shannon's first theorem
area: compression-and-coding/entropy-coding
level: core
summary: A memoryless source of entropy H needs and can reach H bits per symbol. Fixed-length block codes get vanishing error at any rate above H; decodable codes have H <= L* < H + 1.
prereqs: [shannon-entropy, asymptotic-equipartition-property, kraft-inequality]
see_also: [huffman-coding, arithmetic-coding, entropy-rate, lossless-compression, binary-entropy-function, channel-coding-theorem, slepian-wolf-theorem, incompressibility-argument]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Section 9 (The fundamental theorem for a noiseless channel, Theorem 9, and the code built from cumulative probabilities) and Section 7 (Theorem 3 on typical sequences)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 3.2 (Theorem 3.2.1, compression by the typical set), Section 3.3, Section 5.3 (Theorem 5.3.1, L >= H) and Section 5.4 (Theorems 5.4.1 and 5.4.2, H <= L* < H + 1 for symbols and for blocks)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 4 (the source coding theorem for fixed-length block codes) and Chapter 5 (the source coding theorem for symbol codes)
---

The source coding theorem says that the [entropy](/shannon-entropy/) $H$ of a source is the exact limit of lossless compression: $H$ bits per symbol are enough, and fewer are not. It comes in two forms that are proved in different ways and should be kept apart. The *fixed-length* form codes blocks of $n$ symbols into $nR$ bits and allows a small error probability; it uses the [asymptotic equipartition property](/asymptotic-equipartition-property/). The *variable-length* form allows no error and bounds the mean length of a decodable code; it uses the [Kraft inequality](/kraft-inequality/).

## Statement

Notation. $\Sigma$ is a finite alphabet of size $\sigma$. The model is a memoryless source: $X_1, X_2, \ldots$ are independent, each with law $p$ on $\Sigma$, and $H = H(X_1)$ in bits. $X^n = (X_1, \ldots, X_n)$. Logarithms are base 2; with $D$ code letters, replace $H$ by $H_D = H / \log_2 D$.

**Part I: fixed-length block codes.** A *code of rate $R$* for blocks of length $n$ is a pair of maps $f_n : \Sigma^n \to \{0, 1\}^{\lceil nR \rceil}$ and $g_n : \{0, 1\}^{\lceil nR \rceil} \to \Sigma^n$. Its error probability is $P_e^{(n)} = \Pr[g_n(f_n(X^n)) \ne X^n]$.

- **(I.a) Achievability.** If $R > H$, there are codes of rate $R$ with $P_e^{(n)} \to 0$ as $n \to \infty$.
- **(I.b) Converse.** If $R < H$, every sequence of codes of rate $R$ has $P_e^{(n)} \to 1$.

**Part II: variable-length codes with no error.** For a code $C$ on $\Sigma$ with lengths $\ell(x)$, the mean length is $L(C) = \sum_x p(x) \ell(x)$. Let $L^*$ be the least mean length of a [uniquely decodable code](/uniquely-decodable-code/) on $\Sigma$, and $L_n^*$ the least mean length of one on $\Sigma^n$ (one codeword for each block of $n$ symbols).

- **(II.a)** Every uniquely decodable code has $L(C) \ge H$, with equality if and only if $p(x) = 2^{-\ell(x)}$ for all $x$.
- **(II.b)** $H \le L^* < H + 1$, and the bounds are reached by a [prefix code](/prefix-code/).
- **(II.c)** $H \le L_n^* / n < H + 1/n$. So the least mean length per symbol tends to $H$.

## In plain words

Entropy is the true size of the information that a source sends. If we may make a mistake now and then, we can take long blocks of the source, list only the blocks that are likely, and send the number of the block in the list. This list is just big enough when each symbol costs a little more than the entropy, and the chance of a mistake goes to zero as the blocks grow. With a little less than the entropy, the list misses almost every block. If no mistake is allowed, we give short codewords to likely symbols. The mean length can never be less than the entropy, and the best code is less than one bit above it. Coding long blocks shares that one bit among many symbols, so the cost per symbol comes as close to the entropy as we like.

## Proof

**Part I.** Fix $\varepsilon > 0$ and let $A_\varepsilon^{(n)}$ be the typical set of the AEP: the strings $x^n$ with $2^{-n(H + \varepsilon)} \le p(x^n) \le 2^{-n(H - \varepsilon)}$.

(I.a) Take $\varepsilon = R - H > 0$. The typical set has at most $2^{n(H + \varepsilon)} = 2^{nR}$ elements, so $f_n$ can give each typical string a different index of $\lceil nR \rceil$ bits, and send all other strings to the index 0. Let $g_n$ map each index back to its typical string. The code is wrong only when $X^n \notin A_\varepsilon^{(n)}$, so $P_e^{(n)} \le \Pr[X^n \notin A_\varepsilon^{(n)}] \to 0$ by the AEP.

(I.b) Let $B_n$ be the set of strings that the code decodes correctly. Each correct string is $g_n(y)$ for some code word $y$, so $|B_n| \le 2^{\lceil nR \rceil} \le 2^{nR + 1}$. Take $\varepsilon = (H - R)/2 > 0$. Every typical string has probability at most $2^{-n(H - \varepsilon)}$, so

$$1 - P_e^{(n)} = \Pr[B_n] \le \Pr[B_n \cap A_\varepsilon^{(n)}] + \Pr[X^n \notin A_\varepsilon^{(n)}] \le 2^{nR + 1} 2^{-n(H - \varepsilon)} + \Pr[X^n \notin A_\varepsilon^{(n)}].$$

The first term is $2 \cdot 2^{-n(H - R)/2}$ and the second goes to 0 by the AEP, so $1 - P_e^{(n)} \to 0$. $\square$

A lossless version of Part I uses a flag bit: send 0 and the index of a typical string, or 1 and the string itself in $n \lceil \log_2 \sigma \rceil$ bits. The mean length is at most $n(H + \varepsilon) + \varepsilon n \lceil \log_2 \sigma \rceil + 2$ for large $n$ (Cover and Thomas, Theorem 3.2.1), so it is $n(H + \varepsilon')$ for any $\varepsilon' > 0$.

**Part II.** (II.a) Let $K = \sum_x 2^{-\ell(x)}$. By McMillan's theorem ([Kraft inequality](/kraft-inequality/), part (c)), $K \le 1$. Let $q(x) = 2^{-\ell(x)} / K$, a probability law. Then

$$L(C) - H = \sum_x p(x) \log_2 \frac{p(x)}{2^{-\ell(x)}} = \sum_x p(x) \log_2 \frac{p(x)}{q(x)} - \log_2 K \ge 0,$$

because the first sum is a relative entropy, which is at least 0 (by Jensen's inequality, as in [conditional entropy](/conditional-entropy/)), and $\log_2 K \le 0$. Equality needs $q = p$ and $K = 1$, that is, $\ell(x) = \log_2 (1 / p(x))$.

(II.b) The lower bound is (II.a). For the upper bound, let $\ell(x) = \lceil \log_2 (1/p(x)) \rceil$ for each $x$ with $p(x) > 0$ (drop the symbols of probability 0). Then $\sum_x 2^{-\ell(x)} \le \sum_x p(x) = 1$, so by Kraft's converse there is a prefix code with these lengths, the Shannon code. Its mean length is $\sum_x p(x) \lceil \log_2 \frac{1}{p(x)} \rceil < \sum_x p(x) \left(\log_2 \frac{1}{p(x)} + 1\right) = H + 1$.

(II.c) Apply (II.b) to the source whose symbols are blocks of $n$ symbols. Its law is $p(x^n) = \prod_i p(x_i)$, and its entropy is $H(X^n) = nH$ by the additivity of entropy for independent variables. So $nH \le L_n^* < nH + 1$; divide by $n$. $\blacksquare$

## Consequences

- **Optimal symbol codes.** [Huffman coding](/huffman-coding/) finds a prefix code with mean length $L^*$, so its mean length is in $[H, H + 1)$.
- **Coding near the entropy.** Block codes reach $H + 1/n$ per symbol, but the code table grows like $\sigma^n$. [Arithmetic coding](/arithmetic-coding/) codes a whole message of $n$ symbols in less than $nH + 2$ bits on average without any table, which is (II.c) in practice.
- **Sources with memory.** For a stationary ergodic source, the same two parts hold with the [entropy rate](/entropy-rate/) in place of $H$, by the Shannon-McMillan-Breiman form of the AEP.
- **The wrong model costs relative entropy.** A code built for a law $q$ (lengths $\lceil \log_2 \frac{1}{q(x)} \rceil$) has mean length less than $H(p) + D(p \| q) + 1$ on data from $p$, where $D$ is the relative entropy (Cover and Thomas, Theorem 5.4.3).
- **The pair with channel coding.** The [channel coding theorem](/channel-coding-theorem/) is the dual result: a channel can carry information at any rate below its capacity. Together they give the separation theorem: a source of entropy rate $H$ can be sent over a channel of capacity $C > H$, and not over one with $C < H$.

## Tightness

**Part I for a coin.** Take a coin with $p(1) = 0.1$, so $H = h(0.1) = 0.4690$ bits ([binary entropy function](/binary-entropy-function/)). The code on this page builds the typical-set code of (I.a), with $\varepsilon = R - H$, and computes its exact error probability:

| $n$ | bits at $R = 0.6$ | $P_e$ at $R = 0.6$ | bits at $R = 0.8$ | $P_e$ at $R = 0.8$ |
|---|---|---|---|---|
| 50 | 27 | 0.2339 | 34 | 0.00935 |
| 100 | 56 | 0.1301 | 70 | 8.08e-4 |
| 200 | 114 | 0.0439 | 141 | 7.2e-6 |
| 500 | 289 | 0.00233 | 361 | 1.4e-12 |
| 1000 | 583 | 1.74e-5 | 726 | 4.5e-23 |

(The number of bits is $\lceil \log_2 |A_\varepsilon^{(n)}| \rceil$, which is less than $\lceil nR \rceil$.) Below the entropy, even the best code of rate $R$, which keeps the $2^{\lceil nR \rceil}$ most likely strings, decodes correctly with a probability that goes to 0:

| $n$ | best success at $R = 0.4$ | best success at $R = 0.3$ |
|---|---|---|
| 50 | 0.5008 | 0.2596 |
| 100 | 0.3823 | 0.1073 |
| 200 | 0.2508 | 0.01864 |
| 500 | 0.08862 | 1.78e-4 |
| 1000 | 0.01938 | 1.1e-7 |

Both tables show that the threshold is sharp but that the convergence is slow close to $H$: at $R = 0.6$, which is 28% above $H$, blocks of hundreds of symbols are needed.

**The $+1$ in Part II cannot be removed.** For two symbols with probabilities $1 - \delta$ and $\delta$, every code needs 1 bit per symbol, but $H = h(\delta) \to 0$ as $\delta \to 0$. So $L^* - H$ can be as close to 1 as we like. Blocks fix this: for the coin with $p(1) = 0.1$, the Shannon code on blocks of $n$ symbols has a mean length per symbol of 1.3, 0.8, 0.5509, 0.5501 and 0.4918 for $n = 1, 2, 4, 8, 16$, which falls toward $H = 0.469$ but not monotonically.

**Equality needs dyadic probabilities.** $L(C) = H$ only when every $p(x)$ is a power of $1/2$. For $(1/2, 1/4, 1/8, 1/8)$ the code $0, 10, 110, 111$ reaches $H = 1.75$ bits exactly.

**Unique decodability is needed.** If only distinct codewords are asked for, and each symbol is coded alone, the mean length can be below $H$. For $(1/2, 1/4, 1/4)$, the codewords $0, 1, 00$ are distinct and have mean length $1.25 < H = 1.5$. But the code cannot be used for sequences, since $00$ is also $0 \cdot 0$.

## History

Shannon stated both forms in 1948. Theorem 3 (Section 7) is the typical-sequence property that drives Part I, and Theorem 9 (Section 9), the fundamental theorem for a noiseless channel, says that a source of entropy $H$ can be sent over a channel of capacity $C$ at an average rate as close to $C / H$ symbols per second as we like, and no faster. Shannon's proof of the variable-length bound used the code now called the Shannon code, with lengths $\lceil \log_2 (1/p) \rceil$, built from cumulative probabilities. The converse for all uniquely decodable codes needed McMillan's 1956 inequality; before it, the bound was known for prefix codes through Kraft's 1949 inequality. Huffman (1952) found the codes with mean length exactly $L^*$. The name "noiseless coding theorem" comes from the noiseless channel of Shannon's Theorem 9.

## References
